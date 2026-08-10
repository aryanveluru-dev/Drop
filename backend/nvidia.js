// NVIDIA-hosted LLM client (OpenAI-compatible endpoint at build.nvidia.com).
//
// Get a free API key at https://build.nvidia.com  ->  pick any model  ->  "Get API Key".
// Keys look like "nvapi-...". Put it in your environment as NVIDIA_API_KEY (never commit it).
//
// The key is used ONLY to normalize messy coupon-page text into structured offers.
// It does not (and cannot) authenticate to Kroger/Coupons.com etc.

const BASE_URL = process.env.NVIDIA_BASE_URL || "https://integrate.api.nvidia.com/v1";
const MODEL = process.env.NVIDIA_MODEL || "meta/llama-3.3-70b-instruct";

export function hasKey() {
  return !!process.env.NVIDIA_API_KEY;
}

export async function chat(messages, { temperature = 0.1, maxTokens = 2048 } = {}) {
  const key = process.env.NVIDIA_API_KEY;
  if (!key) {
    throw new Error(
      "NVIDIA_API_KEY is not set. Get one at https://build.nvidia.com (Get API Key) " +
      "and export it, e.g.  export NVIDIA_API_KEY=nvapi-..."
    );
  }
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 60_000);
  try {
    const res = await fetch(`${BASE_URL}/chat/completions`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${key}`,
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
      body: JSON.stringify({ model: MODEL, messages, temperature, max_tokens: maxTokens }),
      signal: controller.signal,
    });
    if (!res.ok) {
      const body = await res.text().catch(() => "");
      throw new Error(`NVIDIA API ${res.status} ${res.statusText}: ${body.slice(0, 300)}`);
    }
    const data = await res.json();
    return data.choices?.[0]?.message?.content ?? "";
  } finally {
    clearTimeout(timer);
  }
}

// Ask the model to extract structured coupon offers from raw page text.
// Returns an array of { brand, deal, value, get, category } (source meta added by caller).
export async function extractOffers(rawText, source) {
  const system =
    "You extract retail coupon offers from noisy web page text. " +
    "Return ONLY a compact JSON array, no prose, no markdown fences. " +
    "Each element: {\"brand\": string, \"deal\": string, \"value\": string, \"get\": \"print\"|\"clip\", \"category\": string}. " +
    "\"deal\" is a short human description (e.g. \"$3 off Tide PODS 102-112ct\"). " +
    "\"value\" is the savings if stated (e.g. \"$3.00\", \"FREE\", \"20% off\"), else \"varies\". " +
    "Only include concrete, currently-listed offers. Skip navigation, ads, and generic marketing. " +
    "If none are found, return []. Return at most 12 offers.";
  const user =
    `Store: ${source.store}\nDefault redemption: ${source.defaultGet}\nCategory: ${source.category}\n\n` +
    `PAGE TEXT (truncated):\n${rawText}`;

  const out = await chat([
    { role: "system", content: system },
    { role: "user", content: user },
  ]);

  return safeParseArray(out).map((o) => ({
    brand: String(o.brand || source.store).slice(0, 80),
    deal: String(o.deal || "").slice(0, 200),
    value: String(o.value || "varies").slice(0, 40),
    get: o.get === "print" || o.get === "clip" ? o.get : source.defaultGet,
    category: String(o.category || source.category).slice(0, 40),
  })).filter((o) => o.deal.length > 3);
}

function safeParseArray(text) {
  if (!text) return [];
  // Strip accidental code fences and locate the first JSON array.
  const cleaned = text.replace(/```(?:json)?/gi, "").trim();
  const start = cleaned.indexOf("[");
  const end = cleaned.lastIndexOf("]");
  if (start === -1 || end === -1 || end < start) return [];
  try {
    const arr = JSON.parse(cleaned.slice(start, end + 1));
    return Array.isArray(arr) ? arr : [];
  } catch {
    return [];
  }
}
