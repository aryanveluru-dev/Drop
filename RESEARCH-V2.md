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

## 3. Full saturation sweep

| Query | Results | Median rev | >1,000 rev | Price range | Verdict |
|---|---|---|---|---|---|
| `pilates grip socks women` | 2,000 | 1,076 | 31/53 | $6.99–12.99 | **Dead.** Saturated + floor pricing |
| `menopause hand pain compression gloves` | 352 | 1,427 | 27/48 | $9.95–25.95 | **Dead.** Medical category |
| `hyrox knee sleeves` | 280 | 2,037 | 31/48 | $12.99–59.99 | **Dead.** Entrenched |
| `shoulder pulley frozen shoulder` | 127 | 359 | 19/48 | $8.79–26.99 | **Dead.** Medical, floor priced |
| `pelvic floor trainer women` | 449 | 123 | 12/48 | $19.78–119.20 | Crowded; regulated/insertable |
| `hip thrust belt` | 180 | **48** | 3/48 | $9.99–49.99 | **Open-ish**, but price war starting at $9.99 |
| `sled push harness resistance trainer` | 107 | **66** | **0/48** | $17.98–44.99 | **Open** |
| `carpet sled turf drag` | 150 | **30** | 2/48 | $132–189 | **Open + high price** |
| `sled mat weight plate push` | **41** | **20** | **0/41** | $39–133 | **Most open found** |

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
