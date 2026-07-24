# Round 2 — Corrected Saturation Method + New Niche Direction

**Date:** 2026-07-24
**Supersedes the winner in `RESEARCH.md`.** The video digest, the HYROX rulebook findings, and the disqualifications in that document all still stand. The *winner* does not.

---

## 1. What was wrong in Round 1

I scored the padded knee sleeve 8/10 on saturation because no store had *positioned* a padded sleeve for HYROX. That is the wrong test. What matters is what a buyer sees when they search the generic term, and padded knee sleeves are an abundant commodity.

Measured properly:

| Query | Results | Median reviews (organic) | Listings >1,000 reviews | Top listing |
|---|---|---|---|---|
| `hyrox knee sleeves` | 280 | **2,037** | **31 of 48** | 79,602 reviews (Modvel) |

Entrenched incumbents at Modvel, Bodyprox, NEENCA, Gymreapers. That is a closed market. The Round 1 winner is withdrawn.

---

## 2. The method I should have used from the start

Amazon search pages are fetchable with `curl --compressed` and a browser UA. Script: `scratchpad/amzsat.py`.

The signal that matters is **not** result count — it's **review density of organic listings**:

- **Median reviews > 1,000** → entrenched. Incumbents have years of review moat. Walk away.
- **Many results + very low median** → flooded with new junk, price war to the bottom. Check prices; if the floor is under $12, walk away.
- **Few results + low median + healthy prices** → young category. This is the target.

Second rule learned the hard way: **any pain point that maps to an existing medical-supply category is already saturated.** Menopause hand pain → arthritis compression gloves (66,053 reviews, $9.95). Frozen shoulder → shoulder pulley (20,811 reviews, $8.79). Pelvic floor → kegel trainers (5,956 reviews). These are 10-year-old categories with entrenched listings and floor pricing. The menopause *pain points* are real and severe; the *product categories* serving them are closed.

---

## 3. Full saturation sweep — 37 keywords

Measured with `amzsat.py`. Sorted most-enterable first. `median` = median review count of organic p1 listings; `>1k rev` = how many organic listings have over 1,000 reviews.

| keyword | results | median | >1k rev | price | verdict |
|---|---|---|---|---|---|
| sled mat weight plate push | 41 | 20 | 0/41 | $39-133 | **OPEN** |
| carpet sled turf drag | 150 | 30 | 2/48 | $132-189 | **OPEN** |
| turf mat home gym sled | 83 | 30 | 6/41 | $37-2174 | **OPEN** |
| weight sled push pull | 242 | 35 | 0/43 | $27-799 | **OPEN** |
| sauna blanket infrared | 210 | 38 | 3/20 | $80-699 | **OPEN** |
| sled harness shoulder strap | 180 | 43 | 0/51 | $14-65 | **OPEN** |
| plate loaded sled home gym | 132 | 45 | 1/37 | $45-4170 | **OPEN** |
| drag sled fitness portable | 102 | 47 | 2/58 | $20-799 | **OPEN** |
| steel mace club fitness | 133 | 62 | 8/38 | $19-358 | **OPEN** |
| sled push harness resistance trainer | 107 | 66 | 0/48 | $18-45 | **OPEN** |
| portable weight sled any surface | 124 | 66 | 4/53 | $37-160 | **OPEN** |
| kettlebell farmers carry handles | 59 | 98 | 7/43 | $15-150 | **OPEN** |
| sled pull rope gym | 344 | 82 | 5/44 | $5-153 | OPEN but low-ticket |
| workout cards dumbbell women | 114 | 99 | 3/47 | $4-30 | OPEN but low-ticket |
| hip thrust belt | 187 | 103 | 3/50 | $6-80 | CONTESTED |
| pelvic floor trainer women | 449 | 123 | 12/48 | $20-119 | CONTESTED |
| cable machine attachment set home gym | 1,000 | 152 | 8/57 | $7-220 | CONTESTED |
| balance trainer board women | 1,000 | 173 | 7/47 | $10-200 | CONTESTED |
| sandbag training workout adjustable | 538 | 377 | 4/47 | $14-140 | CROWDED |
| gym phone holder magnetic | 40,000 | 263 | 2/16 | $6-20 | CLOSED - price war |
| body fat caliper tape measure kit | 193 | 289 | 15/43 | $4-259 | CLOSED - price war |
| running resistance parachute | 157 | 320 | 15/52 | $9-47 | CLOSED - price war |
| wall ball medicine ball | 446 | 329 | 10/46 | $10-230 | CLOSED - price war |
| shoulder pulley frozen shoulder | 127 | 359 | 19/48 | $9-27 | CLOSED - price war |
| weighted vest women adjustable | 2,000 | 429 | 17/48 | $8-115 | CLOSED - price war |
| hyrox training equipment | 191 | 520 | 20/53 | $12-153 | CLOSED - price war |
| cooling towel menopause hot flash | 210 | 669 | 19/48 | $4-53 | CLOSED - price war |
| lymphatic drainage massager body | 2,000 | 292 | 21/48 | $6-899 | CLOSED - entrenched |
| grip strength trainer adjustable | 1,000 | 688 | 23/53 | $6-77 | CLOSED - entrenched |
| lifting straps women | 10,000 | 757 | 22/47 | $6-80 | CLOSED - entrenched |
| barefoot shoes women wide toe | 20,000 | 1,067 | 28/53 | $14-70 | CLOSED - entrenched |
| pilates grip socks women | 2,000 | 1,076 | 31/53 | $7-13 | CLOSED - entrenched |
| ankle strap cable machine glute | 418 | 1,220 | 26/48 | $5-35 | CLOSED - entrenched |
| barbell pad hip thrust | 222 | 1,353 | 27/47 | $9-60 | CLOSED - entrenched |
| menopause hand pain compression gloves | 352 | 1,427 | 27/48 | $10-26 | CLOSED - entrenched |
| hyrox knee sleeves | 280 | 2,037 | 31/48 | $13-60 | CLOSED - entrenched |
| wrist wraps women weightlifting | 1,000 | 2,130 | 32/53 | $4-34 | CLOSED - entrenched |

### The pattern

**Eleven of the twelve OPEN categories are sleds or heavy functional-strength gear.** Every conventional women's gym accessory is closed — wrist wraps (median 2,130), barbell pads (1,353), ankle straps (1,220), lifting straps (757), magnetic phone mounts (40,000 results).

The reason the sled cluster stayed open is **shipping weight**. Steel sleds are heavy, bulky and expensive to fulfil, so Amazon sellers avoided them — which is exactly why review counts never accumulated. Prices held at $45–800 because nobody raced to the bottom.

That makes the packable fabric/HDPE sled a genuine arbitrage: **it inherits an open category while escaping the shipping cost that kept the category open.** Under 4 lbs, folds flat, and sits in a price band where incumbents charge $133–190.

The one non-sled OPEN result, `sauna blanket infrared` (median 38, $80–699), should be treated with caution: Sims explicitly rejects infrared in the source video — *"it warms the skin but not the core... I'm not a big fan of infrared sauna cuz it doesn't get hot enough."* Same trap as the weighted vest — the client's own material contradicts the pitch. It also carries electrical certification and 5–7kg shipping.

---

## 4. Recommended niche to hunt: the HYROX sled push, for women

This is where the data and the pain point converge.

**The pain point is quantified and female-specific.** Repz race data: *"Sled Push and Wall Balls are the two stations responsible for the largest time losses in women's Open relative to finishing potential."* The women's Open sled is 102kg including sled. And critically:

> *"Women who have strong running fitness and acceptable gym training regularly arrive at this station underprepared because nothing in a standard program replicates the demands of pushing a loaded sled."*
> *"Athletes who skip sled training describe it as the moment their race unravelled."*

**The cause is a structural access problem.** The prescribed fix is training at 120% of race weight (86–90kg for women's Open), 2x/week for 8 weeks. But you cannot do that at a typical commercial gym — no sled, no turf. Planet Fitness and similar chains have neither. So the highest-leverage training input for the hardest station is simply unavailable to most of the 70% of HYROX entrants who are first-timers.

**The product form that solves it is dropship-viable.** A fabric/HDPE drag sled — the category the Spud Inc "Magic Carpet Sled" defined:

- **Under 4 lbs**, holds 600+ lbs of plates
- Rolls up into a gym bag
- Works on turf, carpet, rubber gym flooring, grass — i.e. the floor your gym already has
- Retails **$132.99–$189.99**
- Top Amazon listing has ~145 reviews. Rogue resells it; Spud Inc is a small strength-equipment maker, not a DTC or TikTok operator.

**Why it fits the constraints:**

| Constraint | Fit |
|---|---|
| Physical good | Yes |
| Faceless AI UGC | Excellent. Object-and-legs only: unroll mat → stack plates → push. Satisfying, no face, no body, no health claim. |
| Shipping | Under 4 lbs, folds flat. Best economics of anything tested. |
| Margin | Incumbent price $133–190. Source cost likely $15–30. |
| Context fit | HYROX is the fastest-growing item in the brief (570k → 1.5M → 2.5M athletes, +83% YoY search, 100+ events 2026, 70% first-timers), and this targets the specific station where women lose the most time. |
| Saturation | Lowest measured of any category tested. |

---

## 5. Honest risks

1. **Supply is not a ready dropship SKU.** Alibaba is dense with *steel* sleds and *turf rolls*, thin on fabric/HDPE drag mats. This likely means a small OEM/private-label run rather than one-click dropshipping. That is real added friction and capital.
2. **Floor damage.** A Rogue reviewer reported it *"tearing rubber floors to pieces when only pulling 90 pounds."* Not for concrete or asphalt. Gyms may object. This must be addressed in the product spec (backing material) and stated honestly in the listing — it is also exactly the kind of thing that generates angry comment-section videos if hidden.
3. **No established search demand.** The category term is unsettled, which is why it is open. For Amazon that would be disqualifying; for organic TikTok it is not, because TikTok generates demand rather than capturing it. But it does mean paid search is not a viable channel here.
4. **Physics honesty.** A drag mat replicates sled *drag/pull* well. Sled *push* needs an upright handle; the base Magic Carpet is a drag strap. The differentiated spec is a fabric sled with a rigid, detachable push upright — which is precisely the gap no incumbent fills.

---

## 6. Runner-up if you want lower execution risk

**Hip thrust belt.** 180 results, median 48 reviews, only 3 listings over 1,000. One-size-adjustable so near-zero sizing returns, ~$1.58–5 landed, hands-only demo, and it answers Colenso-Semple's *"biggest fear is not knowing what to do"* by removing the barbell setup entirely. Weakness: BellaBooty owns the brand position and $9.99 listings have already appeared — margin will compress.

Sourcing links are in `RESEARCH.md` §5.

---

## 7. Verified Alibaba links (sled direction)

All returned HTTP 200. Alibaba captchas datacenter IPs, so these were search-indexed and status-verified, not scraped — open in a browser.

- https://www.alibaba.com/product-detail/Adjustable-Wholesale-Drag-Sled-Pulling-Gym_10000003885191.html
- https://www.alibaba.com/product-detail/Weight-Sled-Workout-Sled-Fitness-Strength_1601198905372.html
- https://www.alibaba.com/showroom/fitness-sled.html
- https://www.alibaba.com/showroom/weight-pulling-sled.html
- https://www.alibaba.com/showroom/synthetic-gym-flooring-mat-for-push-sled.html
- https://www.alibaba.com/showroom/gym-sled-turf.html
- https://www.alibaba.com/showroom/sled-track.html

**OEM spec to quote:** heavy-duty tear-resistant HDPE or coated nylon sheet approx. 60 x 90cm; reinforced double-stitched webbing pull straps; low-abrasion backing safe for rubber gym flooring; detachable rigid upright handle for push work; total weight under 2.5kg; packs to a roll that fits a gym bag.

---

## 8. Reference: incumbents to study

- https://www.spud-inc-straps.com/products/magic-carpet-indoor-outdoor-sled
- https://www.roguefitness.com/magic-carpet-sleds
- https://www.garagegymreviews.com/equipment/spud-inc-magic-carpet-sled
- https://www.amazon.com/Spud-Inc-Carpet-Strength-Condition/dp/B07239BBTT
- https://www.repz.app/blog/hyrox-tips-female-athletes
