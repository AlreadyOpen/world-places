---
pretty_name: World places (official figures for places the World Bank leaves out)
license: other
license_name: per-source
license_link: https://github.com/AlreadyOpen/world-places/blob/main/sources.json
tags:
  - geospatial
  - population
  - official-statistics
---

# World places

Official population figures for places that the World Bank's API leaves out, each from the place's own statistics office
(or the official regional body), rebuilt weekly by [AlreadyOpen/world-places](https://github.com/AlreadyOpen/world-places).
Taiwan, for example, has its own government and population and no World Bank entry at all.

- `index.json`: the bake time, the files, and how many places each holds.
- `<source>.json`, one per source, never merged, so each keeps its own terms: `publisher`, `url`, `licence`, and `places`
  with `iso3`, `name`, `population`, `period`, and where the source publishes it, `aged_65_plus_pct` and `density_per_km2`.
  A figure a source does not publish is left out, never estimated.
- `countries.pmtiles` (bucket and dataset): Natural Earth 1:10m country outlines (public domain) as vector tiles, layer
  `countries`, zooms 0-10, every Natural Earth field. Taiwan, Hong Kong and Macau are their own places.
- `manifest.json`: sha256 and size of every file, the counts and the sources.

| File | Places | Publisher | Terms |
|---|---|---|---|
| `taiwan.json` | Taiwan | Ministry of the Interior (Taiwan), Department of Household Registration | [Open Government Data License](https://data.gov.tw/license) |
| `pacific.json` | Cook Islands, Niue, Wallis and Futuna, Pitcairn Islands | Pacific Community (SPC) | [terms of use](https://pacificdata.org/terms-of-use) |
| `aland.json` | Åland | Statistics and Research Åland (ÅSUB). Källa: ÅSUB | [CC BY 4.0](https://www.asub.ax/sv/om-asub/om-asubax/anvandarvillkor) |
| `norfolk.json` | Norfolk Island | Australian Bureau of Statistics | [CC BY 4.0](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer) |
| `insee.json` | Saint Pierre and Miquelon, Saint-Barthélemy, Saint-Martin | INSEE. Source : Insee | [Licence Ouverte 2.0](https://www.insee.fr/fr/information/2008466) |
| `jersey.json` | Jersey | Statistics Jersey | [Open Government Licence – Jersey v1.0](https://www.gov.je/ServiceManual/opendata/Pages/open-government-licence-jersey-ogl-j-v1-0.aspx) |
| `guernsey.json` | Guernsey | States of Guernsey Data & Analysis | no open licence stated; facts republished with credit ([source](https://www.gov.gg/population)) |
| `northern_cyprus.json` | Northern Cyprus (`CYN`) | TRNC Statistical Institute (İstatistik Kurumu) | no open licence stated ([terms of use](https://stat.gov.ct.tr/Terms)) |
| `anguilla.json` | Anguilla | Anguilla Statistics Department | no open licence stated ([source](https://statistics.gov.ai/AllDocuments/1.1%20Population.xlsx)) |
| `montserrat.json` | Montserrat | Statistics Department Montserrat, Ministry of Finance and Economic Management | no open licence stated ([source](https://statistics.gov.ms/)) |
| `saint_helena.json` | Saint Helena; Tristan da Cunha (`SHN-TA`) | St Helena Government Statistics Office; Tristan da Cunha Association (Tristan) | no open licence stated ([St Helena](https://www.sainthelena.gov.sh/st-helena/statistics/), [Tristan](https://tristandc.com/population.php)) |
| `falklands.json` | Falkland Islands | Falkland Islands Government, Policy Department | no open licence stated ([source](https://www.gov.fk/policy/)) |
| `vatican.json` | Vatican City | Governatorato dello Stato della Città del Vaticano | no open licence stated ([source](https://www.vaticanstate.va/it/stato-e-governo/note-generali/popolazione.html)) |
| `morocco_hcp.json` | Laâyoune-Sakia El Hamra, Dakhla-Oued Ed-Dahab (`ESH`) | Haut-Commissariat au Plan (HCP), Morocco. Source : HCP, RGPH 2024 | [CC BY 4.0 for indicators](https://www.hcp.ma/Conditions-generales-d-utilisation-Version-1-0_a2194.html) |
| `somaliland_manual.json` | Somaliland (`SOL`) | Central Statistics Department, Ministry of Planning and National Development, Somaliland | no open licence stated ([PDF](https://somalilandcsd.org/wp-content/uploads/2022/12/A5-CSD_SOMALILAND-IN-FIGURES.pdf)) |

Files marked "no open licence stated" carry `"licence_note": "no open licence; facts republished with credit"`: the
figures are official facts republished with credit to the publisher, whose terms are linked. Places may carry `notes`
(estimate or projection caveats). Northern Cyprus and Somaliland use Natural Earth's codes `CYN` and `SOL`.
`saint_helena.json` holds Tristan da Cunha as a sub-place `SHN-TA` (Natural Earth has no separate polygon; Ascension publishes
no figures and is absent); its place entry names its own `publisher` and `url`. `morocco_hcp.json` gives Morocco's 2024 census
legal population for the two Moroccan-administered regions side by side, with `scope` and `status_note` ("Status disputed"):
Morocco's regional borders do not match the territory of Western Sahara, so they are never summed into a Western Sahara total.
`somaliland_manual.json` is entered by hand from the PDF (`entered_by_hand` says when) and rechecked yearly.

Taiwan's density uses its land area of 36,197 km² (Ministry of the Interior). The 65+ share is computed from each source's
single-year age counts. Provided as is, with no warranty, and not endorsed by any of the sources.
