#!/usr/bin/env python3
"""
Trend sweep over all 6-angle survivors.

Product names are not search terms. This maps each survivor to the phrase a
real buyer would type, then runs it through the Google Trends gate.

Writes results incrementally to sweep-results.json so a rate-limit stall
still leaves usable data.
"""
import json, os, sys, time, statistics
from pytrends.request import TrendReq

OUT = "/home/user/Drop/sweep-results.json"

# survivor -> consumer search term
TERMS = {
"Magnetic nasal dilator":"nasal dilator","Internal nasal vent":"nose vents snoring",
"Jaw support strap":"chin strap snoring","Cooling mattress topper":"cooling mattress topper",
"Smart sleep tracker mat":"sleep tracker mat","Bed wedge pillow":"wedge pillow",
"CPAP cleaning device":"cpap cleaner","Knee pillow side sleeper":"knee pillow",
"Sleep headphone headband":"sleep headphones headband","Derma stamp scalp roller":"derma stamp hair",
"Scalp SPF spray":"scalp sunscreen","Hair steamer cap":"hair steamer cap",
"Scalp exfoliating serum applicator":"scalp serum applicator","Beard growth roller":"beard roller",
"Microcurrent facial device":"microcurrent facial device","Red light face mask":"led face mask",
"Under-eye microcurrent wand":"under eye wand","Jaw exerciser":"jaw exerciser",
"Facial steamer":"facial steamer","Face yoga tool kit":"face yoga tool",
"LED neck & décolleté device":"neck firming device","Lymphatic drainage body tool":"lymphatic drainage tool",
"Ice bath tub":"ice bath tub","Sauna blanket":"sauna blanket",
"Stretch mark microneedle roller":"stretch mark roller","Back acne treatment applicator":"back acne applicator",
"Ingrown hair treatment roller":"ingrown hair treatment","Hand & foot paraffin bath":"paraffin wax bath",
"Compression recovery boots":"compression boots recovery","Heated shiatsu neck massager":"neck massager",
"Foot circulation massager":"foot circulation massager","Contrast therapy foot spa":"foot spa massager",
"LED teeth whitening kit":"teeth whitening kit","Teeth-grinding night guard":"night guard teeth grinding",
"Forearm/grip trainer":"grip strengthener","Adjustable kettlebell":"adjustable kettlebell",
"Resistance band door anchor system":"resistance bands door anchor","Balance board trainer":"balance board",
"Neck traction device":"neck traction device","TMJ jaw massage device":"tmj massager",
"Spinal decompression back stretcher":"back stretcher","Sciatica seat cushion":"sciatica cushion",
"Heat + vibration back belt":"heated back massager belt","Breathwork/CO2 trainer":"breathing trainer device",
"Red light + sound meditation lamp":"meditation light","Biofeedback stress ring":"stress ring",
"Heated abdominal belt":"heating pad belt","Posture + core breathing trainer":"breathing exerciser",
"Heated eye mask":"heated eye mask","Hand therapy putty + grip kit":"therapy putty",
"Menstrual heat patch belt":"period heating pad","Breast pump wearable":"wearable breast pump",
"Menopause cooling neck wrap":"cooling neck wrap","Bed rail assist handle":"bed rail for elderly",
"Shower grab bar suction":"suction grab bar","Pet deshedding vacuum attachment":"pet grooming vacuum",
"Pet stroller":"pet stroller","Dehumidifier compact":"small dehumidifier",
"Wireless portable humidifier":"portable humidifier","Steam cleaner handheld":"handheld steam cleaner",
"Mattress vacuum UV":"mattress vacuum","Food dehydrator":"food dehydrator",
"Kitchen composter electric":"electric composter","Tyre inflator portable":"portable tire inflator",
"Under-desk treadmill":"under desk treadmill","Portable power station":"portable power station",
"Diamond painting kit":"diamond painting","Eczema wet-wrap sleeve set":"eczema sleeves",
"Rosacea LED redness device":"led mask rosacea","Silicone scar sheets":"silicone scar sheets",
"Keratosis pilaris body kit":"keratosis pilaris treatment","Hyperpigmentation LED spot device":"dark spot device",
"Tattoo aftercare film kit":"tattoo aftercare film","Ear wax removal camera tool":"ear wax removal camera",
"Musician ear plugs":"musician ear plugs","Ear dryer for swimmers":"ear dryer",
"Kids noise-cancelling earmuffs":"kids ear defenders","Golf swing tempo trainer":"golf swing trainer",
"Running gait sensor insole":"running insole sensor","Climbing hangboard portable":"portable hangboard",
"Ski/snowboard boot dryer":"boot dryer","Truck driver lumbar cushion":"lumbar support cushion car",
"Teleprompter phone rig":"teleprompter for phone","Lavalier wireless mic":"wireless lavalier mic",
"Alcohol-free spirit sampler":"non alcoholic spirits","Smart body composition scale":"body composition scale",
"Food scale nutrition tracker":"nutrition food scale","Calf/leg elevation wedge":"leg elevation pillow",
"Post-op shower cast cover":"cast cover shower","Sock aid + dressing stick":"sock aid",
"Ice therapy shoulder wrap":"shoulder ice wrap","Leg elevation post-surgery pillow":"post surgery leg pillow",
"Garden kneeler seat":"garden kneeler","Soil moisture/pH meter":"soil ph meter",
"Electric weed burner":"weed burner","Hose splitter smart timer":"hose timer",
"Nasal irrigation system":"nasal irrigation","Dust mite mattress encasement":"dust mite mattress cover",
"Steam inhaler":"steam inhaler","Lip plumping device":"lip plumper device",
"Eyebrow microblading pen kit":"eyebrow pen","Hair removal IPL device":"ipl hair removal",
"Pomodoro focus timer cube":"pomodoro timer","Phone lockbox timer":"phone lock box",
"Noise-masking desk speaker":"white noise machine office",
"Diabetic foot inspection mirror":"foot inspection mirror","Migraine cooling head wrap":"migraine cap",
"Chronic fatigue shower chair":"shower chair","IBS heat + vibration pad":"stomach heating pad",
"Incontinence bed pad washable":"washable bed pads","SAD light therapy lamp":"light therapy lamp",
"Mood tracking journal + prompts":"mood journal","Anxiety weighted lap pad":"weighted lap pad",
"Motorcycle bluetooth helmet intercom":"motorcycle bluetooth headset","Bike seat pressure-relief saddle":"comfort bike saddle",
"RV tank level monitor":"rv tank monitor","Van life diesel heater":"diesel heater van",
"Portable compost toilet":"composting toilet","12V portable fridge":"12v fridge",
"Automatic chicken coop door":"automatic chicken door","Water storage + filter kit":"emergency water filter",
"Seed starting heat mat":"seedling heat mat","Solar generator panel kit":"solar generator",
"Silent practice drum pad set":"practice drum pad","Vocal steam inhaler":"vocal steamer",
"3D printer filament dryer":"filament dryer","Airbrush cleaning station":"airbrush cleaning pot",
"Aquarium auto water changer":"aquarium water changer","Reptile thermostat controller":"reptile thermostat",
"Bridal emergency kit":"bridal emergency kit","Smart water leak sensor":"water leak detector",
"Window vibration alarm":"window alarm","Pilates reformer bar home":"pilates bar home",
"Splits/flexibility trainer":"leg stretcher machine","Spaced repetition flashcard box":"flashcard box",
"Toddler step stool foldable":"toddler step stool","Ultrasonic cleaner":"ultrasonic cleaner",
}


def slope(s):
    if not s or len(s) < 8: return None
    q = max(2, len(s)//4)
    a, b = statistics.mean(s[:q]), statistics.mean(s[-q:])
    if a == 0: return 999.0 if b > 0 else 0.0
    return round((b-a)/a*100, 1)


def classify(g12, peak):
    if g12 is None: return "NO DATA"
    if g12 > 60 and peak: return "BREAKOUT"
    if g12 > 25: return "RISING"
    if g12 > -10: return "FLAT"
    if g12 > -40: return "COOLING"
    return "DECLINING"


def main():
    done = {}
    if os.path.exists(OUT):
        done = {r["product"]: r for r in json.load(open(OUT))}
    pt = TrendReq(hl="en-US", tz=360)
    items = [(p, t) for p, t in TERMS.items() if p not in done]
    print(f"{len(done)} already done · {len(items)} to go", flush=True)

    for i, (prod, term) in enumerate(items, 1):
        rec = {"product": prod, "term": term}
        for label, tf in (("s12", "today 12-m"), ("s5", "today 5-y")):
            series = None
            for attempt in range(4):
                try:
                    pt.build_payload([term], timeframe=tf, geo="US")
                    df = pt.interest_over_time()
                    series = [int(v) for v in df[term].tolist()] if not df.empty else None
                    break
                except Exception:
                    time.sleep(10*(attempt+1))
            rec[label] = series
            time.sleep(2)
        s12, s5 = rec.get("s12"), rec.get("s5")
        rec["g12"], rec["g5"] = slope(s12), slope(s5)
        peak = bool(s5 and max(s5[-8:]) >= 0.85*max(s5))
        rec["current"] = s12[-2] if s12 and len(s12) > 1 else None
        rec["verdict"] = classify(rec["g12"], peak)
        for k in ("s12", "s5"): rec.pop(k, None)
        done[prod] = rec
        json.dump(list(done.values()), open(OUT, "w"), indent=2)
        print(f"[{i}/{len(items)}] {prod[:38]:38} {str(rec['g12']):>8}% {rec['verdict']}", flush=True)
        time.sleep(2)

    rows = list(done.values())
    order = {"BREAKOUT":0,"RISING":1,"FLAT":2,"COOLING":3,"DECLINING":4,"NO DATA":9}
    rows.sort(key=lambda r: (order.get(r["verdict"],9), -(r["g12"] or -999)))
    print("\n=========== SWEEP COMPLETE ===========")
    for r in rows:
        print(f"{r['product'][:40]:40} {str(r['g12']):>9} {str(r['g5']):>9}  {r['verdict']}")
    from collections import Counter
    print("\n", dict(Counter(r["verdict"] for r in rows)))


if __name__ == "__main__":
    main()
