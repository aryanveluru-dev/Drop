// Deterministic Coupons.com extractor.
// Coupons.com is a Next.js app that embeds its data as RSC payloads
// (self.__next_f.push([1,"..."])). We reconstruct those strings, then read the
// retailer list and each retailer's live voucher/offer titles straight from the
// embedded GraphQL objects — no API key required, no barcode reproduced.
//
// We record only the OFFER (title, value, expiry) and link back to the official
// Coupons.com retailer page, where the code is revealed / the coupon is printed.

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";

export async function fetchHTML(url, timeoutMs = 25_000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { headers: { "User-Agent": UA, "Accept": "text/html" }, signal: controller.signal, redirect: "follow" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.text();
  } finally {
    clearTimeout(timer);
  }
}

// Reconstruct and unescape the concatenated RSC string payload.
export function rscBlob(html) {
  const chunks = [];
  const re = /self\.__next_f\.push\(\[1,"/g;
  let m;
  while ((m = re.exec(html))) {
    let i = re.lastIndex, out = "", esc = false;
    for (; i < html.length; i++) {
      const ch = html[i];
      if (esc) { out += ch; esc = false; continue; }
      if (ch === "\\") { out += ch; esc = true; continue; }
      if (ch === '"') break;
      out += ch;
    }
    chunks.push(out);
  }
  let blob = chunks.join("");
  try { blob = JSON.parse('"' + blob.replace(/"/g, '\\"') + '"'); }
  catch { blob = blob.replace(/\\n/g, " ").replace(/\\"/g, '"').replace(/\\\\/g, "\\"); }
  return blob;
}

// Retailer directory from the homepage / printable page.
export function extractRetailers(blob) {
  const re = /"activeVouchersCount":(\d+),"activeGiftCard":[^,]*,"activeCashback":\{[^}]*\},"__typename":"Retailer"\},"retailerLandingPage":\{"url":"(coupon-codes\/[^"]+)"/g;
  const rows = [];
  let m;
  while ((m = re.exec(blob))) {
    const count = +m[1], slug = m[2];
    const seg = blob.slice(Math.max(0, m.index - 400), m.index);
    const names = [...seg.matchAll(/"name":"([^"]+)"/g)];
    const name = names.length ? names[names.length - 1][1] : titleize(slug.split("/")[1]);
    rows.push({ name: decode(name), count, url: "https://www.coupons.com/" + slug, slug });
  }
  return dedupeBy(rows, (r) => r.url).sort((a, b) => b.count - a.count);
}

// Live offer titles for a single retailer page.
// Real per-retailer offers are objects shaped like:
//   "idPool":"<dashed-uuid>","voucher":{"title":"...","description":...,
//    "termsAndConditions":"...", ... "voucherType":N ... "endTime":"..." }
// (A promotional cross-sell banner uses a non-dashed idPool, so we skip it.)
export function extractOffers(blob) {
  const re = /"idPool":"[0-9a-f]{8}-[0-9a-f-]{20,}","voucher":\{"title":"([^"]{4,120})"/g;
  const out = [];
  let m;
  while ((m = re.exec(blob))) {
    const title = decode(m[1]);
    if (/^(top offers|mobile offers|printable coupons|browser extension)$/i.test(title)) continue;
    const win = blob.slice(m.index, m.index + 1400);
    const vt = win.match(/"voucherType":(\d+)/);
    const end = win.match(/"endTime":"([^"]*)"/);
    const terms = (win.match(/"termsAndConditions":"([^"]{0,400})"/) || [])[1] || "";
    const inStore = /in[- ]?store|mobile app|scan|at the register|show (?:this|the) (?:coupon|barcode)/i.test(title + " " + terms);
    out.push({
      title,
      type: vt && +vt[1] === 2 ? "code" : "deal",
      inStore,
      endsAt: end ? end[1] : "",
    });
  }
  return dedupeBy(out, (o) => o.title.toLowerCase());
}

export function parseValue(title) {
  if (/\bbogo\b|buy\s*\d+[,\s]*get|buy\s*one[,\s]*get/i.test(title)) return "BOGO";
  if (/free\s+(shipping|delivery)/i.test(title)) return "Free ship";
  const dollar = title.match(/\$\s?(\d+(?:\.\d+)?)/);
  if (dollar) return "$" + dollar[1] + (/\boff\b/i.test(title) ? " off" : "");
  const pct = title.match(/(\d+)%\s*off/i);
  if (pct) return pct[1] + "% off";
  if (/\bfree\b/i.test(title)) return "FREE";
  return "See offer";
}

// ---- helpers ----
function titleize(s) { return String(s).replace(/[-_]/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()); }
function decode(s) {
  return String(s)
    .replace(/\\u0026/g, "&").replace(/&amp;/g, "&")
    .replace(/\\u2019|’/g, "'").replace(/\\'/g, "'")
    .replace(/\s+/g, " ").trim();
}
function dedupeBy(arr, keyFn) {
  const seen = new Set(), out = [];
  for (const x of arr) { const k = keyFn(x); if (seen.has(k)) continue; seen.add(k); out.push(x); }
  return out;
}
