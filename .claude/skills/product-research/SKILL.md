---
name: product-research
description: >
  Screen candidate physical products for dropship/ecommerce viability using a
  four-gate methodology validated over an extended research project in this
  repo. Use this whenever the user asks to find a winning product, evaluate
  whether a product idea is worth pursuing, run a product tournament, check
  if a niche is saturated, or compare several product candidates — even if
  they don't name the gates explicitly (e.g. "is this product oversaturated",
  "what should I dropship", "find me something not everyone is already
  selling"). Also trigger when the user wants to build a candidate list
  across many niches/trends and narrow it down, or when they ask about
  Amazon competition, Google Trends demand, or whether a product idea is
  "played out". This skill exists specifically because naive approaches
  (picking a product because it "looks cool", or judging saturation by
  Amazon result *count* instead of review density) reliably produce false
  winners — read the whole file before screening anything, the ordering and
  the detail-check step are not optional.
---

# Product Research: the four-gate method

This methodology was built and stress-tested across many rounds of a real
product-search project in this repo (see `RESEARCH*.md`, `PLAYBOOK.md`,
`TOURNAMENT-FINAL*.md` for the full history, including the false starts).
Every gate below exists because skipping it produced a wrong answer at some
point in that project. Don't skip steps to save time — the failures were
expensive precisely because they *looked* fine until the next gate caught them.

## The four gates, in this order, no exceptions

Order matters. Each gate is cheaper to run than the next one, and each gate
kills candidates the next one would otherwise waste time on. Running them
out of order (e.g. saturation-checking before angle-gating) wastes API calls
on products that were always going to be disqualified for free.

### Gate 1 — Six distinct angles + kill flags (cheapest, run first)

A product survives only if you can honestly write **six angles that are
genuinely different motivations or audiences**, not six rephrasings of the
same one. "Look younger" and "reduce wrinkles" are the same angle. "Look
younger" and "stop your partner complaining about your snoring" are two.

Why this matters: with a product that supports many real angles, roughly
1 in 10 ad creatives tends to work. With a weak product, it's closer to 1 in
100. The product itself determines your creative hit rate — this is a
selection criterion, not a marketing afterthought you handle later.

Alongside the angle count, kill the candidate outright (regardless of angle
count) if any of these apply:

- **`retail`** — already sold in general retail (Target, CVS, Walmart) today.
  This is the single most common reason a product that looks good on paper
  is actually dead. A product "on paper" checklist means nothing if a
  customer can buy the same thing at a pharmacy. Always ask this explicitly,
  not just "is it on Amazon" — general retail availability kills a product
  even when Amazon data looks open.
- **`policy`** — requires a regulated medical/health claim (FDA clearance,
  drug-adjacent claims) or falls in an ad-platform restricted category
  (health conditions, personal attributes). Kill it or plan for the
  compliance cost explicitly — don't quietly assume you can market around it.
- **`size`** — has size/fit variance (apparel, braces with S/M/L). This
  produces return-rate and ad-approval problems disproportionate to the
  product's appeal, especially for a first product.
- **`old`** — the wow factor has visibly decayed (a product every dropshipper
  already ran two years ago, a "2016 product"). Trend and saturation data
  will usually confirm this if you're unsure, but don't wait for the data if
  it's obvious on inspection.

See `field.py` for 347 worked examples of products scored this way (137
survived) — use it as a calibration reference for how strict "six *distinct*
angles" should be, and reuse its `RAW`/`RAW2`/`RAW3` blocks as a template
when building a new candidate field.

### Gate 2 — Demand (cheap, run second)

Confirm the surviving candidates are actually being searched for or watched,
not just theoretically appealing.

- **Primary: Google Trends**, via `trendcheck.py`. Checks both 12-month and
  5-year slope — a product needs to be rising on *both* windows to count as
  a real trend rather than a seasonal blip or a spike that already peaked.
  A product that's only up on the 12-month view but flat/declining on 5
  years is often just seasonal (boot dryers, seedling mats, holiday items) —
  cross-check the 5-year series before trusting a 12-month spike.

  ```
  python3 trendcheck.py "product search term" "another term" ...
  ```

- **Fallback: short-form (YouTube) view-count percentile**, via
  `hooksweep.py` (batch) or `hookcheck.py` (single/manual). **Google Trends
  rate-limits hard and can stay HTTP 429 for an entire session with no
  recovery** — this happened partway through the project this skill is built
  from, and burned real time before the fallback was built. Don't wait on
  Trends recovering; switch to the short-form gate immediately once you see
  sustained 429s, rather than retrying Trends in a loop.

  This isn't only a fallback of convenience — short-form view count on the
  product's own demo arguably measures the thing that actually matters more
  directly than search volume does: whether the product commands attention
  in the exact format (short video) it will be marketed in. When the two
  signals disagree, weight the short-form one more heavily.

  A known gotcha in the current script: grading originally binned any
  product with fewer than 3 matching videos into "NO SIGNAL" regardless of
  how well those few videos performed, which silently discarded real
  winners (a product with 2 videos and 250k views is not "no signal"). If
  you see a lot of NO SIGNAL results, re-run with more query variants before
  trusting the bucket — don't let a thin sample get treated as evidence of
  no interest.

### Gate 3 — Saturation (moderate cost, run third)

Only now check whether the Amazon shelf is actually open, via `amzsat.py`:

```
python3 amzsat.py "product search term" "another term" ...
```

**The metric is review-density of organic listings, not result count.**
A category with 2,000 results and a median of 30 reviews is more open than
one with 100 results and a median of 5,000 — result count on its own is
close to meaningless and will mislead you if you look at it first.
Categories with median >800 reviews or a sub-$12 price floor are effectively
closed no matter how few total listings there are.

### Gate 4 — Listing-detail check (mandatory, no shortcuts)

**Never trust the aggregate saturation number for a finalist without also
reading its actual top listings.** This is not optional polish — it decided
the outcome of every tournament run under this methodology. Two concrete
cases from this project:

- A category showed a "safe" median review count, but its top listings
  turned out to split cleanly into two different markets under one search
  term — an entrenched market at one price tier (one brand alone held
  10,000+ reviews) and a genuinely open one at a higher tier. The trend data
  mapped specifically to the open tier. A median-only read would have missed
  this entirely, in both directions — it can hide either an entrenched
  incumbent or a real opportunity sitting right next to it.
- A product with the single largest demand signal found in an entire
  100+-product field turned out to be a mature commodity market on
  inspection — several incumbents each holding 1,500–15,000 reviews,
  clustered exactly in the price band a new entrant would use. The
  saturation *median* looked open because of a long tail of dead listings
  diluting it, but the top of the market was completely locked.

To do this: take the surviving candidate(s) from Gate 3, pull their top
10-15 organic Amazon listings by review count (not just the summary stats —
`amzsat.py`'s underlying `fetch`/`parse` functions can be called directly
for this, or re-run the search and read the raw listing titles/review
counts/prices by eye), and ask: are these prices and review counts something
a new entrant could actually compete against? Is there a hidden sub-market
inside this search term that the aggregate number is averaging over?

## Running the whole funnel

1. Build or extend a candidate field (see `field.py` for the format: name,
   niche, angles, kill-flags).
2. Run Gate 1 (`candidates.py` or `field.py`) — expect roughly 15-40% of a
   well-targeted field to survive; a much higher survival rate usually means
   the angle bar was applied too loosely.
3. Run Gate 2 on survivors (`trendcheck.py`, falling back to `hooksweep.py`
   if Trends is rate-limited).
4. Run Gate 3 on the RISING/BREAKOUT (or STRONG/GOOD short-form) subset
   (`amzsat.py`).
5. Run Gate 4 by hand on whatever comes back OPEN or CONTESTED — do not skip
   this even when there's only one or two finalists left and it feels like
   overkill. It has reversed the apparent winner more than once.
6. State the result plainly, including margin math (target ≥2.5x landed
   cost as a floor) and which gates were actually checked vs. assumed.

## Honesty norms for reporting results

Report a real "no clean winner" outcome if that's what the data shows,
rather than dressing up the least-bad survivor as a confident pick — a
tournament that killed 30+ of 30-something checked candidates and left one
weak survivor is itself a meaningful finding (the category is picked over),
not a failure to find something better. Say explicitly which gates were
skipped or assumed (e.g. "Trends was rate-limited for this run, demand is
short-form-only") rather than letting a partial screen read as a full one.
