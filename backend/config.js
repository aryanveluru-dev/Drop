// Sources for every listed store + manufacturer coupon issuer.
// Each source points at an OFFICIAL public coupon/deals page. The pipeline fetches
// the page text and asks an LLM to extract structured, currently-listed offers.
//
// IMPORTANT — legal/ToS note:
//   You are responsible for ensuring you may fetch each URL below. Respect each
//   site's Terms of Service and robots.txt. This scaffold makes ONE polite request
//   per source and is meant for personal, low-volume use. Do NOT reproduce or
//   redistribute coupon barcodes — the pipeline only records the OFFER and links
//   back to the official issuer where each user prints/clips their own valid copy.

export const SOURCES = [
  {
    store: "Kroger",
    category: "Grocery",
    // Public digital-coupon + weekly-deal landing pages.
    urls: [
      "https://www.kroger.com/cl/digital-coupons/",
      "https://www.kroger.com/pr/free-friday-download-deal_ent_0610",
    ],
    defaultGet: "clip", // clip in app -> scan Plus card
    scanNote: "Clip in the Kroger app, then scan your Kroger Plus card at checkout.",
  },
  {
    store: "Target",
    category: "General retail",
    urls: ["https://www.target.com/circle"],
    defaultGet: "clip",
    scanNote: "Clip Circle offers in the Target app, then scan your Circle barcode / app Wallet.",
  },
  {
    store: "CVS",
    category: "Pharmacy",
    urls: ["https://www.cvs.com/extracare/home", "https://www.cvs.com/deals-features/deals"],
    defaultGet: "clip",
    scanNote: "Send coupons to your card in the CVS app, then scan your ExtraCare barcode.",
  },
  {
    store: "Walgreens",
    category: "Pharmacy",
    urls: ["https://www.walgreens.com/topic/promotion/coupons.jsp"],
    defaultGet: "clip",
    scanNote: "Clip coupons in the Walgreens app, then scan your myWalgreens barcode.",
  },
  {
    store: "Safeway / Albertsons",
    category: "Grocery",
    urls: ["https://www.safeway.com/foru/coupons-deals.html"],
    defaultGet: "clip",
    scanNote: "Clip 'for U' offers in the app, then scan your Club Card barcode.",
  },
  {
    store: "Publix",
    category: "Grocery",
    urls: ["https://www.publix.com/savings/digital-coupons"],
    defaultGet: "clip",
    scanNote: "Clip digital coupons in the Publix app, then enter your phone / scan your app barcode.",
  },
  {
    store: "Coupons.com",
    category: "Manufacturer",
    urls: ["https://www.coupons.com/printable"],
    defaultGet: "print", // print your own -> printed barcode scans
    scanNote: "Print your own copy; the printed barcode scans at most stores that take paper coupons.",
  },
  {
    store: "P&G brandSAVER",
    category: "Manufacturer",
    urls: ["https://www.pgbrandsaver.com/"],
    defaultGet: "print",
    scanNote: "Print your own copy from P&G brandSAVER; it usually expires the day after printing.",
  },
];

// Curated popular national retailers (slugs present on Coupons.com) for the shipped
// snapshot. The backend can also scrape the FULL sitemap universe with --all.
export const POPULAR_SLUGS = [
  "target","walmart","amazon","cvs","walgreens","kohls","macys","nike","adidas","sephora",
  "ulta","best-buy","homedepot","lowes","wayfair","chewy","doordash","ubereats","grubhub",
  "expedia","hotels-com","priceline","old-navy","gap","jcpenney","michaels","petco","petsmart",
  "gamestop","nordstrom","express","dominos","papa-johns","dell","hp","samsung","ebay","etsy",
  "nordstrom-rack","academy","gnc","vitaminshoppe","victoriassecret","abercrombie","shein","temu",
  "autozone","discount-tire","instacart","shutterfly","vistaprint","dollar-general","kroger",
  "safeway","publix","costco","samsclub","tacobell","carters","crocs","vans","underarmour",
  "reebok","columbia","llbean","rei",
];
