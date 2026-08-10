// Offer-refresh pipeline: fetch each source -> LLM-normalize -> write ../data/offers.json
//
// Usage:
//   export NVIDIA_API_KEY=nvapi-...      # from https://build.nvidia.com
//   node backend/build.js
//
// Safe by design: if the key is missing or every source fails, the existing
// data/offers.json is left untouched (we never overwrite good data with nothing).

import { writeFileSync, readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { SOURCES } from "./config.js";
import { fetchText } from "./scrape.js";
import { extractOffers, hasKey } from "./nvidia.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dirname, "..", "data", "offers.json");

function hostOf(url) {
  try { return new URL(url).host.replace(/^www\./, ""); } catch { return ""; }
}

async function run() {
  if (!hasKey()) {
    console.error("✗ NVIDIA_API_KEY not set. Get one at https://build.nvidia.com and export it.");
    console.error("  Leaving data/offers.json unchanged.");
    process.exit(1);
  }

  const collected = [];
  for (const source of SOURCES) {
    const primaryUrl = source.urls[0];
    let text = "";
    for (const url of source.urls) {
      try {
        const t = await fetchText(url);
        if (t) { text += "\n\n" + t; }
        console.log(`· fetched ${url} (${t.length} chars)`);
      } catch (e) {
        console.warn(`· skip ${url}: ${e.message}`);
      }
    }
    if (!text.trim()) { console.warn(`  no text for ${source.store} — skipping`); continue; }

    try {
      const offers = await extractOffers(text, source);
      console.log(`  ${source.store}: extracted ${offers.length} offer(s)`);
      for (const o of offers) {
        collected.push({
          ...o,
          store: source.store,
          how: source.scanNote,
          url: primaryUrl,
          host: hostOf(primaryUrl),
          reported: monthLabel(),
        });
      }
    } catch (e) {
      console.warn(`  ${source.store}: LLM extract failed — ${e.message}`);
    }
  }

  const deduped = dedupe(collected);

  if (deduped.length === 0) {
    console.error("✗ No offers extracted from any source. Keeping existing data/offers.json.");
    process.exit(1);
  }

  const payload = {
    generatedAt: new Date().toISOString(),
    count: deduped.length,
    disclaimer:
      "Offers reported from official issuer pages; they rotate often. No barcodes are " +
      "reproduced — each links to where you print/clip your own valid copy. Verify at source.",
    offers: deduped,
  };
  writeFileSync(OUT, JSON.stringify(payload, null, 2) + "\n");
  console.log(`\n✓ Wrote ${deduped.length} offers to data/offers.json`);
}

function dedupe(offers) {
  const seen = new Set();
  const out = [];
  for (const o of offers) {
    const key = (o.store + "|" + o.deal).toLowerCase().replace(/\s+/g, " ").trim();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(o);
  }
  return out;
}

function monthLabel() {
  return new Date().toLocaleString("en-US", { month: "short", year: "numeric" });
}

run().catch((e) => {
  console.error("Pipeline error:", e.message);
  // Never clobber good data on an unexpected crash.
  if (existsSync(OUT)) console.error("Existing data/offers.json left in place.");
  process.exit(1);
});
