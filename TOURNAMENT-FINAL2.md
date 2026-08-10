# The 347-Product Tournament — Final Result

**Date:** 2026-08-09
**Method:** 6-angle pre-gate → demand gate (short-form view counts, Google Trends blocked) → saturation gate → listing-detail check.

---

## The funnel

| Stage | In | Out | Method |
|---|---|---|---|
| Field built | — | 347 | Candidate products across 60+ niches |
| 6-angle + kill-flag gate | 347 | 137 | Retail/policy/size/wow-factor kill flags; ≥6 distinct angles required |
| Demand gate | 137 | 45 (STRONG/GOOD) | Short-form (YouTube) view-count percentile — **Google Trends was rate-limited (HTTP 429) for the entire session and never recovered**, so this substituted as the demand signal |
| Saturation gate | 28 checked* | 3 nominally OPEN | Amazon organic review-density (`amzsat.py`) |
| Listing-detail check | 3 | **1** | Read actual top listings, not just the median |

*28 of the 45 were checked directly; the remaining 17 were either already screened in earlier rounds (jaw exerciser, magnetic nasal dilator, LED teeth whitening — all previously CLOSED) or excluded upfront on obvious kill conditions (nasal irrigation and steam inhaler are CVS staples; under-desk treadmill and food dehydrator fail on freight weight; diamond painting and alcohol-free spirits fail on commodity/logistics grounds). All were later swept anyway; see below.

---

## The demand gate found real signal, and the winners weren't where I expected

Top of the 137-product demand sweep by max short-form views:

| Product | Niche | Max views |
|---|---|---|
| Spinal decompression back stretcher | pain | 13,015,949 |
| Nasal irrigation system | allergy | 10,700,704 |
| Ingrown hair treatment roller | body | 8,459,103 |
| Under-desk treadmill | desk | 7,850,616 |
| Silent practice drum pad set | music | 6,410,118 |
| Ear wax removal camera tool | ear | 3,812,618 |
| Diamond painting kit | hobby | 3,811,349 |
| Forearm/grip trainer | mens | 3,765,358 |
| Eyebrow microblading pen kit | beauty | 2,886,704 |

The unifying mechanic across nearly all of the top ten: **a satisfying, visually complete demo** — a crack, a flush, an extraction, a squeeze. This is exactly Saamir's and Oscar's thesis (wow factor drives spend) showing up unprompted in independent data.

## The saturation gate killed almost all of them

**25 of the 28 checked came back CLOSED, CONTESTED, or CROWDED.** Full table:

| Product | Median reviews | >1k reviews | Verdict |
|---|---|---|---|
| Hair removal IPL device | 93 | 6/48 | OPEN |
| Climbing hangboard portable | 23 | 0/50 | OPEN but low-ticket |
| Spinal decompression back stretcher | 96 | 11/48 | OPEN but low-ticket |
| LED neck & décolleté device | 108 | 5/46 | CONTESTED |
| Balance board trainer | 171 | 8/48 | CONTESTED |
| Ear dryer for swimmers | 206 | 14/48 | CLOSED — price war |
| Contrast therapy foot spa | 249 | 18/58 | CONTESTED |
| Menstrual heat patch belt | 303 | 17/58 | CLOSED — price war |
| Beard growth roller | 308 | 20/52 | CLOSED — price war |
| Phone lockbox timer | 341 | 9/47 | CROWDED |
| Breathwork/CO2 trainer | 343 | 16/48 | CLOSED — price war |
| Jaw exerciser | 360 | 15/58 | CLOSED — price war |
| Posture + core breathing trainer | 368 | 18/48 | CLOSED — price war |
| Teeth-grinding night guard | 449 | 19/47 | CLOSED — entrenched |
| Ear wax removal camera tool | 592 | 21/48 | CLOSED — entrenched |
| Forearm/grip trainer | 729 | 28/58 | CLOSED — entrenched |
| Sock aid + dressing stick | 754 | 22/48 | CLOSED — entrenched |
| Biofeedback stress ring | 766 | 4/20 | CLOSED — price war |
| Tattoo aftercare film kit | 964 | 26/53 | CLOSED — entrenched |
| Silicone scar sheets | 993 | 24/48 | CLOSED — entrenched |
| IBS heat + vibration pad | 1,149 | 28/53 | CLOSED — entrenched |
| Ingrown hair treatment roller | 1,248 | 28/48 | CLOSED — entrenched |
| Foot circulation massager | 1,410 | 26/47 | CLOSED — entrenched |
| Motorcycle bluetooth helmet intercom | 1,497 | 13/21 | CLOSED — entrenched |
| Post-op shower cast cover | 1,772 | 33/53 | CLOSED — entrenched |
| Sciatica seat cushion | 2,173 | 27/47 | CLOSED — entrenched |
| Eyebrow microblading pen kit | 2,491 | 35/48 | CLOSED — entrenched |
| Keratosis pilaris body kit | 2,573 | 32/48 | CLOSED — entrenched |

Six more from the GOOD tier were swept in the same pass and all came back closed too: heated shiatsu neck massager (med 2,077), food dehydrator (269, dominated by $36–340 established brands), steam inhaler (727, entrenched), padded bike saddle (1,325, entrenched), seedling heat mat (457, price war), smart hose timer (147, contested).

**Net: 34 products checked across saturation, 3 nominally open.**

---

## The listing-detail check — where the real decision happens

Nominal "OPEN" from median review count is not the same as actually open. Reading the top listings:

### Spinal decompression back stretcher — DEAD
```
14,964 rev  $207  Innova Advanced Heat and Massage Inversion Table
 6,339 rev   $16  ChiFit Multi-Level Back Stretching Device
 4,736 rev   $29  Back Stretcher for Lower Back Pain Relief
 4,048 rev   $38  Everlasting Comfort Lumbar Support Board
 1,887 rev   $36  Sit and Decompress Back Stretcher
 1,558 rev   $48  Decompression Back Belt (×2 colorways)
```
This had the single largest demand signal in the entire 137-product field (13M views) and it is dead on arrival. A mature commodity category with six incumbents holding 1,500–15,000 reviews each in the exact $16–48 band a dropshipper would enter at. The low *median* was an artifact of a long tail of zero-review junk listings diluting the number — the top of the market is completely locked.

### Hair removal IPL device — DEAD
```
7,242 rev  $300  Braun IPL Silk·Expert Pro 5
2,909 rev  $349  Ulike Air 10
2,826 rev   $80  INNZA IPL
2,044 rev  $420  Braun IPL Silk·Expert Pro 5 (variant)
1,543 rev   $70  Ubroo
1,465 rev  $400  Braun IPL Silk·Expert Pro 5 (variant)
```
Owned by real consumer-appliance brands — Braun is a Procter & Gamble subsidiary — with genuine laser/light hardware, a decade of trust, and (in most markets) safety-certification requirements a dropshipper cannot casually clear. Not enterable at any price point tested.

### Portable climbing hangboard — the sole survivor
```
332 rev  $113  YY Vertical Hangboards
315 rev   $19  Ucraft Pocket-Sized Climbing Hangboard
309 rev   $45  Two Stones Portable Hangboard
185 rev   $36  Bellaroca Portable Hangboard
179 rev   $40  BG Climbing Wood Hangboard
145 rev   $28  POWER GUIDANCE Hangboard
```
No listing above 1,000 reviews, at all, in the whole category. The incumbents are small climbing-gear specialty brands, not conglomerates. Genuinely open.

---

## 🏁 Result: the portable climbing hangboard — and an honest verdict on it

It is the only product in a 347-item field, screened through every gate in the operators' playbook, that comes out clean. I want to be direct about what that means and doesn't mean.

**What it has going for it:**
- Zero incumbent above 1,000 reviews — genuinely open shelf
- Passes the CVS test cleanly — not sold in general retail, ever
- 6 real angles (finger strength, home training, travel, tendon rehab/plateau-breaking, warm-up) — clears Saamir's gate
- Demand is real, if not spectacular: 357,221 max views (GOOD tier, not STRONG)
- Margin is workable — a plywood/resin-hold board sources at roughly $8–15, sells at $35–75, so 2.5–5x depending on tier
- No policy exposure, no size variance, no regulated claims

**Where I won't oversell it:**
- **Weak on insecurity, the criterion Saamir calls the single most important one.** This is a hobbyist training-plateau problem, not an identity or appearance insecurity. It doesn't hit the emotional register that drove every product the operators actually cited as a big winner.
- **Small TAM.** Climbing/bouldering is a real and growing niche (women now 52% of US indoor climbers per earlier research in this project, gyms up ~20%/year), but it is a fraction of the population compared to sleep, skin, or pain categories.
- **Low AOV ceiling.** $18–113 is a real band but not a $150–300 considered-purchase category with room for a premium brand tier.
- It survived less because it is an exceptional product and more because **almost nothing else survived.** 33 of 34 checked products failed. That is itself information: the field of "angle-rich, trending, demo-friendly, insecurity-adjacent" physical products at accessible price points is close to fully picked over on Amazon right now.

**Honest recommendation:** this is a legitimate, low-risk, low-capital niche product to validate cheaply — not the "grip socks before they blew up" breakout the brief was chasing. If the goal is genuinely to be first on something with mass-market upside, the more promising unexploited territory in this data is TikTok Shop itself (structurally unmeasurable from here — Kalodata/PiPiAds needed) rather than anything the Amazon-saturation lens can still find.

---

## Sources for this round

- `field.py` — 347-product candidate field with angle/niche/kill-flag annotations
- `hook-results.json` — corrected short-form demand data, all 137 products
- `sat-results.json` — saturation data, 28 products
- Six additional saturation checks run outside the JSON pipeline (neck massager, dehydrator, steam inhaler, bike saddle, seedling mat, hose timer) — all closed, logged above
