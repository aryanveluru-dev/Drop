// Offer-refresh pipeline (Coupons.com):
//   1) fetch the retailer directory  2) fetch each retailer's live offers
//   3) (optional) enrich with an NVIDIA-hosted LLM  4) write ../data/offers.json
//
// Deterministic core — NO API key required. The NVIDIA key (from build.nvidia.com,
// read from NVIDIA_API_KEY) is used ONLY if you pass --enrich, to classify offers
// as in-store vs online and tidy categories. Never hardcode keys.
//
// Usage:
//   node backend/build.js                 # scrape + write data/offers.json
//   node backend/build.js --enrich        # also LLM-classify (needs NVIDIA_API_KEY)
//   node backend/build.js --retailers 14 --per 4
//
// No coupon barcodes are reproduced — only offer titles + links to the official
// Coupons.com retailer page, where the code is revealed / the coupon is printed.

import { writeFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { fetchHTML, rscBlob, extractRetailers, extractOffers, parseValue, classify, fetchSitemapRetailers, prettyName } from "./coupons.js";
import { POPULAR_SLUGS } from "./config.js";
import { hasKey, chat } from "./nvidia.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dirname, "..", "data", "offers.json");

const args = process.argv.slice(2);
const opt = (flag, def) => { const i = args.indexOf(flag); return i > -1 && args[i + 1] ? args[i + 1] : def; };
const MODE = args.includes("--all") ? "all" : args.includes("--popular") ? "popular" : "home";
const MAX_RETAILERS = +opt("--retailers", MODE === "all" ? 150 : MODE === "popular" ? 80 : 26);
const PER_RETAILER = +opt("--per", 8);
const ENRICH = args.includes("--enrich");
const DIR_URL = "https://www.coupons.com/printable";

async function getRetailers() {
  if (MODE === "all") {
    console.log("· fetching FULL sitemap universe…");
    return (await fetchSitemapRetailers()).slice(0, MAX_RETAILERS);
  }
  if (MODE === "popular") {
    console.log(`· using ${POPULAR_SLUGS.length} curated popular retailers…`);
    return POPULAR_SLUGS.slice(0, MAX_RETAILERS).map((slug) => ({
      name: prettyName(slug), slug, url: "https://www.coupons.com/coupon-codes/" + slug,
    }));
  }
  console.log("· fetching retailer directory…");
  const dirBlob = rscBlob(await fetchHTML(DIR_URL));
  return extractRetailers(dirBlob).slice(0, MAX_RETAILERS);
}

const HOW = {
  instore: "In-store offer — add it in the retailer's app (e.g. Target Circle), then scan your loyalty/app barcode at checkout; it applies automatically.",
  online: "Reveal the code on Coupons.com, then enter it at online checkout.",
  deal: "Auto-applied sale — opens the deal at the retailer; the discount is already reflected, no code needed.",
};
function hostOf(u) { try { return new URL(u).host.replace(/^www\./, ""); } catch { return "coupons.com"; } }
function monthLabel() { return new Date().toLocaleString("en-US", { month: "short", year: "numeric" }); }
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function run() {
  const retailers = await getRetailers();
  console.log(`  ${retailers.length} retailers`);
  if (!retailers.length) { keepExisting("no retailers parsed"); return; }

  const offers = [];
  for (const r of retailers) {
    try {
      const blob = rscBlob(await fetchHTML(r.url));
      const found = extractOffers(blob).slice(0, PER_RETAILER);
      console.log(`  ${r.name}: ${found.length} offer(s)`);
      for (const o of found) {
        const mode = classify(o, r.name); // "online" | "instore" | "deal"
        offers.push({
          brand: r.name,
          store: r.name,
          deal: o.title,
          value: parseValue(o.title),
          get: mode === "instore" ? "clip" : mode === "online" ? "online" : "deal",
          category: mode === "instore" ? "In-store offer" : mode === "online" ? "Online code" : "Online sale",
          how: HOW[mode],
          url: r.url,
          host: hostOf(r.url),
          endsAt: o.endsAt ? o.endsAt.slice(0, 10) : "",
          reported: monthLabel(),
        });
      }
      await sleep(400); // be polite between requests
    } catch (e) {
      console.warn(`  ${r.name}: skip (${e.message})`);
    }
  }

  if (!offers.length) { keepExisting("no offers extracted"); return; }

  let finalOffers = offers;
  if (ENRICH) {
    if (!hasKey()) console.warn("· --enrich set but NVIDIA_API_KEY missing; skipping enrichment.");
    else finalOffers = await enrich(offers);
  }

  const payload = {
    generatedAt: new Date().toISOString(),
    source: "coupons.com",
    count: finalOffers.length,
    disclaimer:
      "Live offer titles scraped from Coupons.com retailer pages. Codes are revealed on the " +
      "official Coupons.com page (not reproduced here). Offers rotate — verify at source.",
    offers: finalOffers,
  };
  writeFileSync(OUT, JSON.stringify(payload, null, 2) + "\n");
  console.log(`\n✓ Wrote ${finalOffers.length} offers to data/offers.json`);
}

// Optional NVIDIA enrichment: classify in-store vs online + normalize category.
async function enrich(offers) {
  console.log("· enriching with NVIDIA LLM…");
  const list = offers.map((o, i) => `${i}. [${o.brand}] ${o.deal}`).join("\n");
  const sys = "For each numbered offer, reply ONLY a JSON array of " +
    "{\"i\":number,\"inStore\":boolean,\"category\":string}. category is a short retail category.";
  try {
    const out = await chat([{ role: "system", content: sys }, { role: "user", content: list }], { maxTokens: 3000 });
    const start = out.indexOf("["), end = out.lastIndexOf("]");
    const meta = JSON.parse(out.slice(start, end + 1));
    for (const m of meta) {
      if (offers[m.i]) {
        if (typeof m.inStore === "boolean") {
          offers[m.i].get = m.inStore ? "clip" : "online";
          offers[m.i].how = m.inStore
            ? "In-store offer — add it in the retailer's app, then scan your loyalty/app barcode at checkout."
            : "Reveal the code on Coupons.com, then enter it at online checkout.";
        }
        if (m.category) offers[m.i].category = String(m.category).slice(0, 40);
      }
    }
  } catch (e) {
    console.warn("  enrichment failed, using deterministic classification:", e.message);
  }
  return offers;
}

function keepExisting(reason) {
  console.error(`✗ ${reason}. Keeping existing data/offers.json.`);
  if (!existsSync(OUT)) console.error("  (no existing file to keep)");
  process.exit(1);
}

run().catch((e) => { console.error("Pipeline error:", e.message); keepExisting("unexpected error"); });
