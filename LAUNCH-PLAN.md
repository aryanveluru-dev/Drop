# Launch Plan — Red Light LED Face Mask

**Constraints:** $1–3k capital · no inventory purchase · starting from zero (no entity, no accounts, no store) · fastest possible launch.

**Strategy:** take a sliver of a proven, growing market and win on execution — not find an empty niche. This supersedes the hangboard result in `TOURNAMENT-FINAL2.md`, which optimised for an empty shelf and therefore found a tiny market.

---

## Why this product

| Signal | Value |
|---|---|
| LED face mask market | $333M (2025) → $820M (2033), 11.9% CAGR |
| TikTok Shop "Facial Beauty Device" growth | **+400%** |
| Proven price point | $159 (volume leader holds 3,590 reviews there) |
| Regulatory | Cosmetic claims only — **no 510(k) needed** |
| Insecurity | Anti-aging / skin — deepest consumer vertical there is |
| Seasonality | None. Evergreen. |

### The proof that an unknown brand can win here

The Amazon price ladder, read directly:

```
PREMIUM          Shark CryoGlow        $349    957 rev
                 iRestore              $399    953 rev
                 CurrentBody           $469    621 rev
                 Dr. Dennis Gross      $455    621 rev
                 Therabody             $299    311 rev

VOLUME LEADER    unbranded 4D LED      $159  3,590 rev   <-- market voted here
                 INIA (multi-SKU)   $89-199  ~2,845 rev combined
                 RENPHO                $149    308 rev
                 LifePro               $149    291 rev

BOTTOM           generic 7-in-1         $39    401 rev
```

**INIA is the template.** An unknown brand running a $89 / $99 / $119 / $179 / $199 SKU ladder has stacked more reviews than Shark, Therabody and Dr. Dennis Gross — while charging half. They are not doing anything proprietary: same class of Shenzhen factory, better price laddering, more variants, more creative. The goal is not to beat Shark. The goal is to be INIA.

---

## The plumbing problem, and the fix

**TikTok Shop rejects pure China dropshipping.** Orders must dispatch within 3 business days; TikTok validates tracking against declared dispatch origin, so shipping direct from a Chinese supplier flags as an origin mismatch. Exceeding a 4% late-dispatch rate triggers severe Shop Performance penalties. This is not a rule to work around — it is the rule that ends accounts.

**Three things resolve it:**

1. **No LLC required to start.** TikTok Shop permits *individual* seller accounts: 18+, US resident, new email/phone, matching ID + tax + bank details. The "starting from zero" blocker is smaller than it looks. (A business entity is still worth forming before scaling ad spend.)
2. **Use a US-warehouse dropship agent, not AliExpress direct.** Agents that pre-stock high-velocity SKUs in US warehouses ship domestically in 3–5 days while you still purchase zero inventory up front. LED masks are exactly the kind of SKU they stock. This satisfies the dispatch SLA and keeps capital at zero.
3. **Launch on Shopify + Meta first, add TikTok Shop second.** Shopify has no dispatch SLA and no origin validation, so it absorbs a slower supply chain while the creative is still unproven. Bring TikTok Shop online once a US-warehouse supplier is confirmed.

---

## The 14-day sprint

### Days 1–2 — Foundation
- Shopify trial + domain. One product page, not a general store.
- Order **2–3 samples** from different suppliers. This is non-negotiable: real footage of the actual product is what separates a store that converts from one that doesn't, and it doubles as supplier QC on an electronic device.
- Shortlist agents/suppliers that can confirm **US warehouse stock** and 3–5 day domestic dispatch.

### Days 3–7 — Creative, before spending on distribution
- Build **25+ creatives** minimum. Meta's retrieval stage filters tens of millions of ads down to a few thousand candidates before ranking even begins, so low volume simply does not enter the auction. Near-identical creatives get pooled and suppressed as duplicates, so vary format, scene, and framing — not just the caption.
- **Image-forward, not video-forward.** Image ads run ~3x cheaper on Meta; a real operator account in an enthusiast niche reported ~$10 CPM / $0.91 CPC running 95% image.
- **Method:** Meta Ad Library → filter to long-running ads (longevity implies profitability) → rebuild the *angle and structure* with your own persona and footage. Use Kling / Seedance / Higgsfield for scenes and lifestyle context; use real sample footage for the device itself. AI cannot render your specific product accurately — this was tested directly earlier in the project: the generated person was convincing, the generated product was generic.
- Spread creative across **awareness stages**, not 25 versions of the same offer ad. Cold traffic to a brand-new store is problem-aware or solution-aware at best, never product-aware.

### Days 5–14 — Organic first, paid second
- Post organically to TikTok from day 5. Costs nothing, and it de-risks the creative *before* you pay for distribution — critical when one failed ad round eats half a $2k budget.
- Whatever performs organically becomes the paid creative. This is the cheapest possible creative validation loop.
- Open Meta only once something has already earned attention for free.

---

## Budget — $2,000 worked example

| Line | Cost |
|---|---|
| Shopify (trial → first month) | $40 |
| Domain | $15 |
| Samples (2–3 units) | $140 |
| AI video tooling (Kling / Seedance) | $30 |
| **Meta ad test** | **$1,450** |
| Buffer | $325 |

### Unit economics at $149

```
Retail                     $149
Landed COGS (single-unit)  -$45
Payment fees (~3%)          -$5
                          -----
Contribution before ads     $99
```

Break-even CAC is $99. **Target CAC ≤ $50**, leaving ~$49/sale. At $50 CAC, $1,450 of spend buys ~29 sales ≈ **$1,420 contribution** — roughly a full return of the ad budget on the first test if the creative works.

**Kill line:** if CAC exceeds $75 after $400 spent with no downward trend, stop, rebuild creative, relaunch. That is a creative failure, not a market failure — the market is proven, so the variable that failed is the ad.

---

## Claims discipline — the one hard rule

| Say | Never say |
|---|---|
| glow, radiance, luminosity | treats acne |
| "the appearance of…" | reduces wrinkles |
| brightening, revitalising | heals, cures, repairs |
| self-care ritual, spa-at-home | clinically proven (unless you hold the clearance) |

Therapeutic claims — acne, wrinkle reduction, wound healing, pain — convert an LED mask into a regulated medical device requiring 510(k) clearance. Cosmetic and general-wellness claims do not. FDA warning letters went out in 2024–25 to light-therapy brands making unsubstantiated medical claims. This costs nothing to comply with: "glow" outsells "reduces wrinkles" anyway.

Also: AI-generated ad creative depicting realistic people requires disclosure on Meta. Transform generated output substantially — own persona, own scene, real product footage composited in — rather than posting a lightly-edited generation. That satisfies both the disclosure question and the creative-quality goal at once.

---

## Sequence after launch

1. **Ladder the SKUs like INIA** — $89 entry, $149 core, $199 with neck attachment. Multiple price points capture multiple intents and stack reviews across variants.
2. **TikTok Shop + affiliates** once a US-warehouse supplier is confirmed. Affiliates cost nothing until a sale closes, produce creative for free, and TikTok Shop native checkout converts 35–55% better than off-platform traffic. This is the single highest-leverage channel for this product and the main reason to solve fulfillment properly.
3. **Email/SMS** from the first order. Returns of roughly $36 and $71 per $1 respectively — the highest-margin channel available, and it compounds.

---

## Honest risk register

- **$1–3k is thin for a $149 product.** One failed creative round consumes half the budget. This is precisely why the plan front-loads free organic validation before paid spend.
- **Electronics carry defect risk on dropship.** Samples are mandatory, not optional. Vet suppliers on QC, not price alone.
- **A new store has no trust signals** at a $149 price point. Reviews, real product footage, and a clear returns policy are load-bearing, not polish.
- **The category is competitive** — that is the point of the strategy, not an objection to it. Competition here means proven demand. The bet is on out-executing on creative volume and offer, not on being the only seller.
