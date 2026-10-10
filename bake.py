"""Official population figures for places the World Bank leaves out (Helen, 2026-10-10: "Taiwan has its own government and
population"; then option 4: each place's own official statistics, Natural Earth's estimate only where none exists).
One JSON per source (never merged: each keeps its own terms), plus index.json listing them:
  out/<id>.json  {"source", "publisher", "url", "licence", "places": [{"iso3", "name", "population", "aged_65_plus_pct",
                  "density_per_km2", "period"}]}      (a figure the source does not publish is left out, never estimated)
Usage: python3 bake.py [<source id> ...]     (default: every source)"""
import csv, datetime, io, json, os, sys, urllib.request
import sources

UA = {'User-Agent': 'AlreadyOpen world-places (https://github.com/AlreadyOpen/world-places)'}


def get(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def taiwan():
    """Ministry of the Interior, household registration: every village, by single year of age (ODRP014, monthly)."""
    now = datetime.date.today()
    for back in range(6):
        y, m = divmod(now.year * 12 + now.month - 1 - back, 12)
        ym = f'{y - 1911}{m + 1:02d}'
        url = lambda pg: f'https://www.ris.gov.tw/rs-opendata/api/v1/datastore/ODRP014/{ym}?page={pg}'
        first = json.loads(get(url(1)))
        if not first.get('responseData'):
            continue                                                       # that month is not out yet
        rows = first['responseData'] + [r for pg in range(2, int(first['totalPage']) + 1) for r in json.loads(get(url(pg)))['responseData']]
        people = sum(int(r['people_total']) for r in rows)
        old = sum(int(v or 0) for r in rows for k, v in r.items() if k.startswith('people_age_') and int(k[11:14]) >= 65)
        return [{'iso3': 'TWN', 'name': 'Taiwan', 'population': people, 'aged_65_plus_pct': round(100 * old / people, 2),
                 'density_per_km2': round(people / 36197, 1), 'period': f'{y}-{m + 1:02d}'}]   # land area 36,197 km² (MOI)
    raise RuntimeError('Taiwan: no month in the last six')


def pacific():
    """Pacific Community (SPC) .Stat, mid-year population estimates (DF_POP_PROJ)."""
    spc = {'CK': ('COK', 'Cook Islands'), 'NU': ('NIU', 'Niue'), 'WF': ('WLF', 'Wallis and Futuna'), 'PN': ('PCN', 'Pitcairn Islands')}
    text = get(f'https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_POP_PROJ,3.0/A.{"+".join(spc)}.MIDYEARPOPEST._T._T'
               f'?endPeriod={datetime.date.today().year}&lastNObservations=1&format=csv').decode()
    return [{'iso3': spc[r['GEO_PICT']][0], 'name': spc[r['GEO_PICT']][1], 'population': int(float(r['OBS_VALUE'])),
             'period': r['TIME_PERIOD']} for r in csv.DictReader(io.StringIO(text))]


def aland():
    """Statistics and Research Åland (ÅSUB) PxWeb BE001: 31 December population by single year of age."""
    q = {'query': [{'code': 'år', 'selection': {'filter': 'top', 'values': ['1']}},
                   {'code': 'ålder', 'selection': {'filter': 'all', 'values': ['*']}},
                   {'code': 'kommun', 'selection': {'filter': 'item', 'values': ['MK21']}},
                   {'code': 'kön', 'selection': {'filter': 'item', 'values': ['0']}}], 'response': {'format': 'json-stat2'}}
    d = json.loads(get('https://pxweb.asub.ax/PXWeb/api/v1/sv/Statistik/BE/Befolkningens%20storlek%20och%20struktur/BE001.px',
                       json.dumps(q).encode(), {'Content-Type': 'application/json'}))
    age, v = d['dimension']['ålder']['category']['index'], d['value']
    total = v[age['SSS']]; old = sum(v[i] for k, i in age.items() if k != 'SSS' and int(k) >= 65)
    return [{'iso3': 'ALA', 'name': 'Åland', 'population': total, 'aged_65_plus_pct': round(100 * old / total, 2),
             'period': f"{next(iter(d['dimension']['år']['category']['index']))}-12-31"}]


def jersey():
    """Statistics Jersey, annual population estimates by single year of age and sex (Jersey open data)."""
    meta = json.loads(get('https://opendata.gov.je/api/3/action/package_show?id=jersey-population-estimate-by-age-and-sex-2010-to-present'))
    rows = list(csv.DictReader(io.StringIO(get(meta['result']['resources'][0]['url']).decode('utf-8-sig'))))
    year = max(r['Year'] for r in rows); rows = [r for r in rows if r['Year'] == year]
    n = lambda r: int(r['Male'] or 0) + int(r['Female'] or 0)
    total = sum(n(r) for r in rows); old = sum(n(r) for r in rows if int(r['Age']) >= 65)
    return [{'iso3': 'JEY', 'name': 'Jersey', 'population': total, 'aged_65_plus_pct': round(100 * old / total, 2), 'period': year}]


# id: (function, publisher, licence, url people can follow)
SOURCES = {
    'taiwan': (taiwan, 'Ministry of the Interior (Taiwan), Department of Household Registration',
               'https://data.gov.tw/license', 'https://www.ris.gov.tw/app/portal/346'),
    'pacific': (pacific, 'Pacific Community (SPC), Statistics for Development Division',
                'https://pacificdata.org/terms-of-use', 'https://stats.pacificdata.org'),
    'aland': (aland, 'Statistics and Research Åland (ÅSUB)', 'https://www.asub.ax/sv/om-asub/om-asubax/anvandarvillkor', 'https://www.asub.ax/sv/statistik/befolkning'),
    'jersey': (jersey, 'Statistics Jersey, Government of Jersey', 'https://www.gov.je/ServiceManual/opendata/Pages/open-government-licence-jersey-ogl-j-v1-0.aspx',
               'https://opendata.gov.je/dataset/jersey-population-estimate-by-age-and-sex-2010-to-present'),
}


def main(ids):
    os.makedirs(sources.OUT, exist_ok=True)
    failed = []
    for sid in ids:
        f, publisher, licence, url = SOURCES[sid]
        try:
            places = f()
        except Exception as e:                                             # keep the last good file; the gate notices a gap
            failed.append(f'{sid}: {e}'); print(f'{sid}: FAILED {e}', file=sys.stderr); continue
        json.dump({'source': sid, 'publisher': publisher, 'url': url, 'licence': licence, 'places': places},
                  open(os.path.join(sources.OUT, f'{sid}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(sid, [(p['iso3'], p['population'], p['period']) for p in places])
    files = sorted(f[:-5] for f in os.listdir(sources.OUT) if f.endswith('.json') and f[:-5] in SOURCES)
    places = {f: len(json.load(open(os.path.join(sources.OUT, f + '.json')))['places']) for f in files}
    idx = {'built': datetime.datetime.now().isoformat(timespec='seconds'), 'counts': places,
           'files': [f + '.json' for f in files], 'failed': failed}
    json.dump(idx, open(os.path.join(sources.OUT, 'index.json'), 'w'), indent=1)
    if failed and len(failed) == len(ids):
        sys.exit('every source failed')


if __name__ == '__main__':
    main(sys.argv[1:] or list(SOURCES))
