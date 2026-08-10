# Channel Strategy — Platforms, Economics, and the AI-Creative Question

**Date:** 2026-07-25 (campaign-execution section added 2026-08-09)
**Scope:** both products side by side, minimum viable budget per channel, platform mix, MCP tooling assessment.

---

## Addendum — campaign execution mechanics (applied to the hangboard, transfers to any product)

Two source videos, applied and corrected against each other rather than taken at face value.

### Image ads, not video, as the default format

Image ads on Meta run roughly **3x cheaper CPM/CPC than video**. One creator's own account (a hobbyist-apparel niche — golf, structurally similar to climbing gear: enthusiast audience, not mass-market) ran 95% image ads over 18 months, $1.7M spend, at **$10 CPM / $0.91 CPC** against a $12.68 niche-average CPM. Cheaper impressions compound into cheaper cost-per-purchase, and the stated reasoning tracks: short-form video is oversaturated across every platform, so a static image with bold text is now the pattern-interrupt, not the hook-driven video.

Redoing this project's CAC estimate with an image-ad-forward assumption instead of the blended-video-and-image benchmark used earlier: **CAC likely lands closer to $20-25** rather than the ~$30 estimated from blended-format benchmarks. This is directionally supported, not niche-verified — no climbing-specific ad-cost data exists — but the format-cost multiplier is a property of the ad type, not the vertical, so it should transfer.

### Creative production workflow (concrete, replaces "make a few ads")

1. Search Meta Ad Library (or the free wrapper adlibrary.io) for competitor or adjacent-brand ads. Filter to "winners" — ads that have run for a long time, which is presumptive evidence of profitability, since brands don't keep paying for ads that lose money.
2. Pick a structurally strong one (clear product shot, room for bold headline text, not overly busy).
3. Recreate it with an image-gen model, explicitly changing the avatar, scene, and removing all original text — not a copy, a same-structure original.
4. Finish in Canva: add your own headline, logo, and CTA text.

### The AI-disclosure tension — do not resolve this the easy way

The workflow above surfaces exactly the compliance risk flagged in the platform-policy section of this document. One tactic seen in the source material: export the AI-generated image from ChatGPT and it carries metadata that flags it as AI to Meta (weaker delivery, possible AI-content labeling); routing it through Canva before upload strips that metadata.

**Do not adopt this as "strip the metadata to dodge detection."** Meta's stated policy requires a visible label on AI-generated content depicting realistic scenarios or synthetic people; evading that detection is a different act than the legitimate reason to touch the image in Canva anyway (adding your own text and branding, which every ad needs regardless of how the base image was produced). The compliant and the good-creative paths are the same path here: substantially transform the AI output — new avatar, new scene, real composited text and branding — rather than lightly editing an otherwise-unmodified generation. If the image is genuinely transformed, the disclosure question resolves itself along with it; if it is not, stripping the metadata does not make the underlying issue go away, it just makes it undetected.

### Creative volume and diversity — 25 minimum, not 4

A four-ad test (one campaign, one ad set, two image, two video) is the right scale for a small local-lead-gen account with warm, search-driven intent. It is **not enough for a cold national ecommerce audience**, per how Meta's delivery pipeline actually works:

1. **Retrieval** (internally "Andromeda") filters tens of millions of active ads down to a few thousand candidates per auction — a gatekeeper stage your ad has to clear before it's even scored.
2. **Ranking** scores the survivors on bid × estimated action rate (Meta's prediction of conversion likelihood) × ad quality (hide-rate, clickbait signals, landing-page load speed and message-to-landing-page congruence).
3. **Auction** sets winners and price from the ranked pool.

The practical takeaway: **you need real volume (≥25 creatives) to compete at the retrieval stage at all**, and real *diversity* — ads that share a format/background/style get pooled together and effectively treated as duplicates and suppressed, even when the underlying content differs. Volume without diversity does close to nothing; the two requirements are separate and both mandatory. As spend scales, creative needs to refresh continuously — rising cost-per-conversion on an ad set is the signal that its creative has fatigued and the pool needs new inputs, not a signal to raise the bid.

### Awareness-stage messaging — the more important half of this

Most advertisers, per this source, only produce ads aimed at the "most aware" audience segment — people who already recognize the brand — which is typically only **3-5% of the addressable market** for an established brand, and is close to zero for a brand-new store with no organic following. The classic five-stage breakdown (unaware → problem-aware → solution-aware → product-aware → most-aware) means a cold audience for a new brand needs creative that **educates and introduces**, not creative that assumes recognition.

Applied to the hangboard: cold Meta traffic is realistically problem-aware (they know their finger strength has plateaued) or solution-aware (they know training tools for this exist) at best — never product-aware or most-aware, because nobody has heard of this specific store yet. The 25-creative minimum above should be built across these stages deliberately, not as 25 versions of the same "buy this" offer ad — mix in educational/problem-aware creative (why plateaus happen, what actually builds finger strength) alongside straightforward product and offer ads. This is also the argument, independently, for the organic-first phase already in this plan: organic community content is what moves a niche audience from problem-aware to product-aware cheaply, before paid spend tries to convert them.

### Net effect on the phased plan

The gated structure (bundle to raise AOV → organic validation → capped paid test → $25 CAC decision gate) is unchanged by any of this — this addendum is entirely about how Phase 4 (the paid test) should be executed once the earlier phases justify reaching it. Revise Phase 4's creative brief to: image-ad-forward, 25 creatives minimum sourced via the Ad Library → AI-recreate → Canva workflow above, spread deliberately across awareness stages rather than concentrated on product/most-aware messaging.

---

## 0. Headline: the gate isn't demographics, it's ad policy

You assumed TikTok's demographic was the problem. The data says otherwise — TikTok's 35–54 share is **25.6%**, essentially identical to Instagram (24.1%) and Pinterest (26.1%). On a base of ~1B users that is a very large absolute audience.

The real constraint is **advertising policy**, and it splits the two products onto different channels.

| Platform | Hair cap ($149) | Beauty pillow ($69) |
|---|---|---|
| **Meta** | Heavily restricted | Workable |
| **Google/YouTube** | Restricted targeting | Workable |
| **TikTok** | **Permitted with 510(k)** | Workable |
| **Pinterest** | Workable | **Best fit** |

---

## 1. The policy gate in detail

### Meta — hostile to the hair cap
- The **Personal Attributes policy** prohibits ads that directly *or indirectly* imply sensitive personal details about the viewer, explicitly including **health**. "Struggling with thinning hair?" is a violation by construction.
- The **2026 update** added AI image analysis that identifies transformation sequences even when unlabeled — flagging "changes in lighting, posture, body composition framing, or facial expression." Date-stamped image sequences are now treated as implied timeline claims.
- **Hair treatment is explicitly named** among the high-risk industries alongside weight loss and cosmetic procedures.

Net: on Meta you cannot address the sufferer, and you cannot show the result. That removes both halves of the persuasive case for the hair cap.

For the **pillow**, skincare is also a named risk category, so avoid over-time before/after. But the crease demo is a *same-moment* physical demonstration, not a claimed transformation over weeks — a materially different and far safer creative.

### Google / YouTube — targeting crippled for the hair cap
- **Health is a sensitive interest category**; you cannot target users based on health conditions or treatments.
- You **cannot remarket healthcare-to-healthcare** — building an audience from people who watched a hair-loss ad and re-serving them hair-loss ads is classed as "health condition inference" and violates policy. You may only remarket with non-healthcare messaging.
- June 2026 update extended these serving implications to Demand Gen and Discovery.

Net: YouTube has the oldest audience (47.4% are 35+) but the retargeting loop — the thing that makes paid acquisition economic — is closed for the hair cap.

### TikTok — the most permissive for the hair cap
- **Medical devices and OTC products are permitted** provided they comply with local law and have FDA clearance where required.
- Claim language is the constraint: **"supports" is acceptable; "repairs" and "reverses" are not.** Hair-growth claims must not imply medical outcomes.

Net: TikTok is the *only* major paid channel where the hair cap can be advertised close to its actual value proposition — and it is contingent on the 510(k) route already recommended in Round 5. The regulatory work unlocks the channel as well as the shelf.

---

## 2. Demographics — the real numbers

| Platform | 35–54 share | Female | Note |
|---|---|---|---|
| YouTube | **47.4% are 35+** | 51.2% (US) | Oldest audience by far |
| Facebook | 35.0% | — | Largest older base on social |
| Pinterest | 26.1% | **70%** | Most female-skewed |
| TikTok | 25.6% | 54.8% | Not the teen platform of 2020 |
| Instagram | 24.1% | 47.5% | Youngest of the four |

TikTok is only marginally younger than Instagram or Pinterest. The "TikTok is for teenagers" assumption is roughly three years out of date.

---

## 3. Channel economics

| Platform | CPM | CPC | CPA / CVR | ROAS |
|---|---|---|---|---|
| **Meta** | ~$14.19 median | $0.78 avg | ecommerce CPA $29.99; **beauty $25.49** | **4.2x — best on social** |
| **TikTok** | $6–13.26 | $1.02 (beauty $0.74); Spark $1.41 | Spark CVR **2.6%**; TikTok Shop storefronts **35–55% higher CVR** than external sites | target ≥2.5x |
| **Pinterest** | **$2–5** | $0.50–1.50 (beauty **$0.40–0.60**) | beauty CPA **$7–10**; CVR 2–4%, **5–8% home goods** | 15% higher with shopping ads |
| Email | — | — | — | **$36 per $1** |
| SMS | — | — | response ~45%, CVR **21–30%** optimised | **$71 per $1** |

Two things stand out.

**Pinterest is the cheapest traffic in the category** — purchase-intent index runs **5.6x the social average**, and its home-goods conversion band (5–8%) is the highest of any paid channel here. That is the beauty pillow's exact category. The caveat is honest: Pinterest's narrower audience and less mature conversion algorithm mean total CPA often lands similar to or above Meta despite the cheap clicks, so it is a discovery channel, not a closing one.

**Owned channels dominate everything.** SMS at $71:$1 and email at $36:$1 are an order of magnitude better than any paid channel, and **texting has now overtaken email as the preferred channel for 50+ adults**, 9 in 10 of whom own smartphones. For a $149 product aimed at a 45–65 woman, the winning structure is cheap paid traffic to capture the contact, then owned channels to convert and repeat.

---

## 4. The AI-creative question — read this part carefully

### The tooling works. I tested it.

Higgsfield generated the sample in `hf-test-haircap.png` from a text prompt alone, on the **budget model** (`nano_banana`, 1 credit — the account had 1.54 credits, so the flagship Marketing Studio model at 2 credits was out of reach; this is a conservative read of quality).

**Honest assessment:**
- The subject reads as a genuine ~50-year-old — real skin texture, visible fine lines, natural grey. It avoids the plastic-smooth AI face that usually gives the game away.
- Hands are anatomically correct, which is the classic tell and it passed.
- Lighting, depth of field and composition are commercially usable.
- **But the product is generic.** It rendered a plausible black cap, not a red light therapy cap — no LEDs, no emission. AI cannot invent *your specific product* accurately.

**Practical conclusion:** use AI for the person, the setting, and the context; composite or image-to-image your real product photography for the product itself. Higgsfield's Marketing Studio supports exactly this via `product_ids` and reference media. Text-to-image alone will not produce product-accurate ads.

### The disclosure problem — this undercuts the strategy as stated

Your framing was an older demographic "more prone to falling for AI ads." Three hard obstacles:

1. **TikTok auto-detects it.** TikTok integrated **C2PA Content Credentials in January 2025** and automatically labels AI content from embedded metadata. Penalties escalate: warning → 7-day posting restriction → 30-day suspension → **permanent ban**. Labels are required for synthetic faces, AI backgrounds, and photorealistic products.
2. **Meta requires a visible label** on paid content with synthetic people or AI-altered product demonstrations. Non-disclosure means rejection; repeat offences mean account-level restrictions.
3. **Regulators are live.** New York's synthetic performer law (mid-2026) charges $1,000 then $5,000 per violation. The EU AI Act reaches €15M or 3% of worldwide turnover.

So undisclosed AI creative is not a durable edge — it is an account-termination risk on the one platform where the hair cap can legally be advertised at all.

There is also a plain commercial argument. A customer who buys because they were deceived refunds, charges back, and leaves a review saying so. At 25% net margin a chargeback wipes out three sales. Deception-led acquisition is the most expensive kind.

**The version that works:** AI as a *production-cost* advantage, disclosed. You generate 50 creative variants for the price of one photoshoot, label them, and win on testing volume rather than on fooling anyone. That advantage is real, large, and doesn't put the account at risk.

---

## 5. Recommended stack

### Beauty pillow ($69) — Pinterest-led
1. **Pinterest** as primary. Cheapest CPM ($2–5), beauty CPA $7–10, home-goods CVR 5–8%, 70% female, 26% aged 35–54. The product is visual, aspirational, and home-category — the exact profile Pinterest converts best.
2. **Meta retarget.** Pinterest discovers, Meta closes at 4.2x ROAS. Standard split is 70–80% Meta / 20–30% Pinterest, but invert it early while creative is unproven, since Pinterest clicks are a third the price.
3. **Email capture from day one.**

### Hair cap ($149) — TikTok-led, owned-channel-closed
1. **TikTok Shop** as primary, once 510(k) sourcing is confirmed. It is the only channel that permits the actual message, and native checkout converts **35–55% better** than sending to an external site.
2. **YouTube for depth.** 47.4% aged 35+. Long-form explainer content is where a $149 considered purchase gets justified. Organic first — paid targeting is crippled by the sensitive-category rules.
3. **SMS + email to close.** At $149 with a 45% SMS response rate and 21–30% conversion, the economics work far better than trying to close cold on paid.
4. **Meta only for cold reach with non-attribute creative** — product-in-context, no sufferer address, no before/after.

---

## 6. Minimum viable budget

Floor spend to get a statistically valid read, not to scale.

| Channel | Minimum test | What it buys | Read |
|---|---|---|---|
| **Pinterest** | **$300** (~$10/day × 30d) | ~500 clicks at $0.60 | Enough for a directional CVR at 2–4% |
| **TikTok Spark Ads** | **$600** (~$20/day × 30d) | ~425 clicks at $1.41 | ~11 conversions at 2.6% — thin but readable |
| **Meta** | **$900** (~$30/day × 30d) | ~1,150 clicks at $0.78 | Needs ~50 conversions for the algo to exit learning |
| **Organic + email** | **$0–50** | Klaviyo free tier to 250 contacts | Should run regardless |

**Cheapest valid path to first conversion: $300 on Pinterest with the pillow.** Lowest CPC in the set, highest intent index, best category fit, and no policy exposure.

**Recommended first month: ~$350** — $300 Pinterest + email tooling. Do not open Meta until you have a creative that already converts somewhere cheaper; Meta's learning phase burns roughly $900 before it tells you anything.

If the hair cap is the pick, the first spend isn't ads at all — it's supplier diligence to confirm 510(k). Without it TikTok is closed, and TikTok is the only channel where the product can be sold properly.

---

## 7. MCP / tooling assessment

**Available and useful now:**
- **Higgsfield** — image and video generation, Marketing Studio with product/avatar binding, TikTok publishing, shorts studio, and a **virality predictor** that scores hook strength and retention risk before you post. The virality predictor is the highest-leverage piece: it lets you kill weak creative before spending distribution on it. *Blocked at present by credits (1.54 remaining; Marketing Studio needs 2 per image).*
- **Gmail** — outreach to suppliers and affiliates.

**Worth adding:**
- A **Klaviyo or Postscript MCP** for email/SMS. Given SMS returns $71:$1 and outperforms every paid channel, this is the biggest gap in the current stack.
- A **Shopify MCP** for catalogue, orders, and conversion data — required to close the loop between ad spend and revenue.
- A **TikTok Shop / Kalodata or FastMoss** source for the saturation blind spot flagged earlier. `amzsat.py` measures Amazon only; TikTok Shop saturation is currently unmeasured, and those are paid tools.

**Honest gap:** nothing in the current stack measures TikTok Shop competition. That remains the weakest evidence in the whole project.

---

## 8. What I'd do this week

1. Top up Higgsfield credits and generate a proper Marketing Studio test with a real product reference image — the text-only test proves the people are convincing but the product is not.
2. Post the five pillow hooks organically. Free, and it settles the hook question from Round 5.
3. Open Pinterest at $10/day against the pillow. Cheapest valid signal available.
4. In parallel, run hair cap supplier RFQs requiring documented 510(k). That single document decides whether the higher-margin product has a channel at all.
5. Set up email capture before any of the above sends traffic anywhere.
