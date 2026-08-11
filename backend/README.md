# Couponly backend — offer refresh pipeline

Keeps `data/offers.json` current for all listed stores. The frontend (`index.html`)
loads that file at runtime; when it's absent (e.g. the offline artifact) it falls back
to a baked-in snapshot.

## How it works

```
backend/config.js   →  official coupon/deals URLs per store (Kroger, Target, CVS,
                       Walgreens, Safeway/Albertsons, Publix, Coupons.com, P&G)
backend/scrape.js   →  one polite fetch per URL, HTML stripped to text
backend/nvidia.js   →  NVIDIA-hosted LLM turns that text into structured offers
backend/build.js    →  orchestrates, dedupes, writes ../data/offers.json
```

No coupon barcodes are ever reproduced. Each offer records the **deal** and links to
the **official issuer**, where each user prints/clips their own valid, in-system copy.

## Run it

The scraper needs **no API key** — it reads Coupons.com's embedded data directly.

```bash
node backend/build.js               # homepage retailers (~26)
node backend/build.js --popular     # curated ~66 popular national retailers (shipped snapshot)
node backend/build.js --all         # FULL sitemap universe (1600+ retailers; capped by --retailers)
node backend/build.js --all --retailers 400 --per 10   # go big
```

Writes `data/offers.json`. If every fetch fails, the existing file is left untouched —
it never overwrites good data with nothing.

### Optional NVIDIA enrichment

Pass `--enrich` to sharpen the in-store/online classification and categories with an
NVIDIA-hosted LLM:

1. Get a free key at **https://build.nvidia.com** → pick any model → **Get API Key** (`nvapi-...`).
2. `export NVIDIA_API_KEY=nvapi-xxxxxxxx` (never commit it).
3. `node backend/build.js --popular --enrich`

Optional overrides: `NVIDIA_BASE_URL`, `NVIDIA_MODEL` (default `meta/llama-3.3-70b-instruct`).

## Automate it (weekly)

`.github/workflows/refresh-coupons.yml` runs the pipeline every Monday and commits any
change. Add your key as a repo secret named `NVIDIA_API_KEY`
(Settings → Secrets and variables → Actions).

## Serve it

Any static host works, since the app is one HTML file plus `data/offers.json`:

```bash
python3 -m http.server 8000    # then open http://localhost:8000/
```

## ⚠️ Legal / ToS

- You are responsible for complying with each source site's **Terms of Service** and
  **robots.txt**. This scaffold is conservative (one request per source, personal use).
- Do **not** reproduce, alter, or redistribute coupon barcodes — that is coupon fraud.
  This pipeline only surfaces offers and links to official issue-your-own sources.
- NVIDIA keys are used solely for LLM text normalization; they do not access retailer data.
