# world-places

Official population figures for places the World Bank's API leaves out (Taiwan, Jersey, Åland, Cook Islands, ...), from each
place's own statistics office, one JSON per source, published weekly to Hugging Face
([dataset](https://huggingface.co/datasets/alreadyopen/world-places), [bucket](https://huggingface.co/buckets/alreadyopen/world-places)
read by browsers) and mirrored to [Kaggle](https://www.kaggle.com/datasets/helenkwok/world-places). Built from
[pipeline-template](https://github.com/AlreadyOpen/pipeline-template).

Why a pipeline: some sources cannot be read from a browser (Åland's PxWeb answers only a JSON POST and refuses the CORS
preflight; Jersey's open data sends no CORS header). Places with no machine-readable official source are not in here; the map
shows Natural Earth's estimate for them, labelled as such.

    python3 bake.py [taiwan pacific aland jersey]    # data/out/<source>.json + index.json
    python3 publish.py                               # gate, then Hugging Face (HF_TOKEN)
    python3 check.py                                 # data-free checks (CI)

Add a source: a function in `bake.py` returning `[{iso3, name, population, period, ...}]`, an entry in `SOURCES` and in
`sources.json`, and a row in `hf/README.md` crediting the owner.
