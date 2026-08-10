#!/usr/bin/env python3
"""
100-product tournament field with the 6-angle pre-gate.

Per Saamir: angle count is a PRODUCT selection criterion, upstream of marketing.
A good product yields ~1 winning creative in 10; a weak one 1 in 100. So a product
that cannot support six genuinely distinct angles never reaches the tournament.

An "angle" = a distinct motivation or audience, not a rephrasing.
"Look younger" and "reduce wrinkles" are ONE angle. "Look younger" and
"stop your partner complaining about your snoring" are two.

kill flags applied before scoring (from Biaheza / Saamir / Welch):
  retail  = sold in CVS/Target today -> dead regardless of numbers
  size    = size variance -> returns + ad approval pain
  old     = wow factor decayed / "2016 product"
  policy  = regulated claim or restricted ad category
"""

# (name, niche, angles[], kill_flags[])
P = [
 # ---------------- sleep & breathing ----------------
 ("Magnetic nasal dilator","sleep",["partner/snoring","energy & brain fog","jawline/mouth-breathing","athletic performance","dry mouth","longevity/sleep quality"],[]),
 ("Internal nasal vent","sleep",["partner/snoring","deviated septum relief","athletic breathing","allergy season","travel sleep","dry mouth"],[]),
 ("Jaw support strap","sleep",["mouth breathing","snoring","jawline/face shape","dry mouth","CPAP adjunct","travel"],[]),
 ("Mouth tape","sleep",["snoring","jawline","morning energy","dry mouth","oral health","athletic"],["retail"]),
 ("Anti-snore positional trainer","sleep",["partner/snoring","back-sleep training","apnea adjunct","travel","posture","sleep quality"],["policy"]),
 ("Tongue retaining device","sleep",["snoring","apnea","partner","dry mouth"],["policy"]),
 ("Weighted sleep mask","sleep",["insomnia","migraine","travel","light sleeper","anxiety","skin/eye pressure"],["retail"]),
 ("Sunrise alarm clock","sleep",["waking groggy","winter blues","no-phone bedroom","kids","shift work"],["retail"]),
 ("Cooling mattress pad","sleep",["night sweats","menopause","partner temp war","sleep quality"],[]),
 ("Smart sleep ring","sleep",["sleep score","recovery","HRV","longevity","fitness"],[]),

 # ---------------- hair & scalp ----------------
 ("Red light hair cap","hair",["thinning","postpartum shed","male pattern","confidence","scalp health","non-drug alternative"],["policy"]),
 ("Scalp massager brush","hair",["growth","dandruff","relaxation","shampoo lather","tension headache"],["retail","old"]),
 ("Derma stamp scalp roller","hair",["thinning","minoxidil absorption","beard","scars","confidence"],[]),
 ("Hair fiber powder","hair",["instant coverage","thinning","photos/events","confidence"],["old"]),
 ("Scalp SPF","hair",["part-line burn","hair loss prevention","aging","outdoor sport"],[]),
 ("Silk bonnet","hair",["frizz","breakage","curly care","sleep"],["retail"]),

 # ---------------- face & skin ----------------
 ("Microcurrent facial device","face",["jawline lift","aging","puffiness","makeup prep","non-tox alternative to filler","confidence"],[]),
 ("Red light face mask","face",["wrinkles","acne","aging","pores","glow","non-invasive alt to botox"],[]),
 ("Ice/cryo roller","face",["puffiness","hangover","migraine","makeup prep","redness"],["retail","old"]),
 ("Under-eye microcurrent wand","face",["dark circles","bags","tired look","aging","zoom face"],[]),
 ("Blackhead vacuum","face",["pores","satisfying demo","acne","confidence"],["old"]),
 ("Jaw exerciser","face",["jawline","double chin","mewing","confidence","TMJ","facial symmetry"],[]),
 ("Face slimming strap","face",["double chin","jawline","post-op","sleep"],["old"]),
 ("Sleep-line face tape","face",["sleep wrinkles","side sleeper","aging"],[]),

 # ---------------- body & aesthetic ----------------
 ("Cellulite vacuum cups","body",["cellulite","lymphatic","recovery","circulation","satisfying demo"],["old"]),
 ("Lymphatic drainage body tool","body",["bloating","cellulite","puffiness","post-surgery","circulation","detox"],[]),
 ("Dry brush","body",["cellulite","circulation","exfoliation","lymphatic"],["retail","old"]),
 ("Sauna blanket","body",["detox","recovery","weight","menopause","relaxation","skin"],[]),
 ("Compression recovery boots","body",["recovery","circulation","swelling","athletes","travel legs","varicose"],[]),
 ("Waist trainer","body",["shape","posture","postpartum"],["size","policy"]),
 ("Posture corrector","body",["back pain","confidence/height","desk work","tech neck","appearance","breathing"],["size"]),
 ("Height insoles","body",["height","confidence","dating","interviews"],["size"]),

 # ---------------- oral ----------------
 ("LED teeth whitening kit","oral",["stains","confidence","dating","photos","coffee/wine","wedding"],[]),
 ("Water flosser","oral",["gums","breath","braces","dentist cost"],["retail"]),
 ("Tongue scraper","oral",["breath","oral microbiome","taste"],["retail","old"]),

 # ---------------- men's ----------------
 ("Beard growth roller","mens",["patchy beard","density","confidence","masculinity","scars"],[]),
 ("Beard straightener","mens",["frizz","volume","grooming speed","appearance"],["old"]),
 ("Body groomer trimmer","mens",["manscaping","hygiene","appearance","partner"],["retail"]),
 ("Forearm/grip trainer","mens",["forearm size","grip strength","climbing","tennis elbow","aesthetics"],[]),
 ("Chest compression top","mens",["gyno","confidence","posture"],["size","policy"]),

 # ---------------- fitness & recovery ----------------
 ("Massage gun","fit",["soreness","recovery","knots","athletes","gift"],["retail","old"]),
 ("Tib bar","fit",["shin splints","knee health","runners","ATG"],[]),
 ("Hip thrust belt","fit",["glutes","no-barbell","home gym","hip bruising","women lifting"],[]),
 ("Knee sleeves","fit",["squat support","knee pain","HYROX/crossfit","warmth"],["size"]),
 ("Portable drag sled","fit",["sled training","no turf","HYROX","conditioning","home gym"],[]),
 ("Resistance band set","fit",["home gym","travel","rehab","glutes"],["retail","old"]),
 ("Adjustable dumbbells","fit",["space saving","home gym","cost vs gym"],[]),

 # ---------------- nervous system & stress ----------------
 ("Vagus nerve stimulator","nerve",["anxiety","sleep","HRV","focus","gut","burnout"],["policy"]),
 ("Weighted blanket","nerve",["anxiety","insomnia","ADHD","sensory"],["retail","old"]),
 ("Acupressure mat","nerve",["back pain","stress","sleep","circulation","cheap massage"],["old"]),
 ("Breathwork/CO2 trainer","nerve",["anxiety","athletic","sleep","focus","lung capacity","HRV"],[]),
 ("Cold plunge tub","nerve",["recovery","mood","discipline","inflammation","metabolism"],[]),
 ("Grounding sheet","nerve",["sleep","inflammation","anxiety"],["policy"]),

 # ---------------- gut & bloat ----------------
 ("Abdominal massage roller","gut",["bloating","constipation","cortisol belly","lymphatic","post-meal"],[]),
 ("Castor oil pack","gut",["bloating","liver detox","period pain","sleep"],["policy"]),
 ("Bloating relief belt","gut",["bloating","posture","period"],["size"]),

 # ---------------- feet ----------------
 ("Toe spacers","feet",["bunions","foot pain","barefoot training","posture","runners"],["old"]),
 ("Plantar fasciitis night splint","feet",["heel pain","morning pain","runners","standing job"],["size"]),
 ("Electric callus remover","feet",["calluses","sandal season","satisfying demo","diabetic care"],["retail"]),
 ("Foot peel mask","feet",["dead skin","satisfying reveal","sandal season"],["retail","old"]),

 # ---------------- eyes ----------------
 ("Heated eye mask","eyes",["dry eye","screen fatigue","sleep","migraine","styes","puffiness"],[]),
 ("Eye massager device","eyes",["screen fatigue","dark circles","migraine","sleep","puffiness"],[]),
 ("Blue light glasses","eyes",["screen fatigue","sleep","headache"],["retail","old","policy"]),

 # ---------------- hands & nails ----------------
 ("Nail fungus laser device","nails",["fungus","sandal shame","diabetic","recurrence"],["policy"]),
 ("Electric nail drill kit","nails",["salon cost","gel removal","hobby","cuticles"],[]),

 # ---------------- women's health ----------------
 ("Pelvic floor trainer","womens",["leaking","postpartum","menopause","lifting","confidence","intimacy"],["policy"]),
 ("Period heat/TENS device","womens",["cramps","drug-free","work/school","endometriosis"],["policy"]),
 ("Menstrual cup","womens",["cost","eco","sport","tampon anxiety"],["retail"]),
 ("Postpartum belly binder","womens",["diastasis","support","posture"],["size"]),

 # ---------------- neck / TMJ / posture tech ----------------
 ("Neck traction device","neck",["neck pain","tech neck","posture","headache","disc","desk work"],[]),
 ("TMJ jaw massage device","neck",["jaw clenching","headache","dental cost","stress","jawline"],[]),
 ("Cervical/neck hump corrector","neck",["dowager hump","posture","appearance","pain"],["size"]),

 # ---------------- home gadgets ----------------
 ("Wireless portable humidifier","home",["dry air","skin","sleep","desk","travel","plants"],[]),
 ("Pocket thermal printer","home",["journaling","study notes","photos","labels","gift"],[]),
 ("Electric spin scrubber","home",["bathroom","satisfying demo","back strain","grout"],["old"]),
 ("Robot window cleaner","home",["high windows","safety","time","satisfying"],[]),
 ("Portable blender","home",["gym","travel","smoothies","office"],["retail","old"]),
 ("Under-sink water filter","home",["taste","microplastics","cost vs bottled","health"],[]),
 ("Air quality monitor","home",["allergies","mould","kids","VOCs","sleep"],[]),
 ("Shower head filter","home",["hair","skin","hard water","chlorine"],[]),

 # ---------------- pets ----------------
 ("Pet hair remover roller","pet",["shedding","furniture","car","clothes"],["retail","old"]),
 ("Dog nail grinder","pet",["nail anxiety","groomer cost","quick-cutting fear","noise-free"],[]),
 ("Pet water fountain","pet",["hydration","kidney health","cats","filter"],["retail"]),
 ("Slow feeder bowl","pet",["bloat","gulping","enrichment"],["retail"]),
 ("Pet dental water additive","pet",["breath","vet cost","plaque"],["policy"]),

 # ---------------- baby & parent ----------------
 ("Electric nasal aspirator","baby",["congestion","sleep","sick season","gentler than bulb"],[]),
 ("Bottle washer/sterilizer","baby",["time","hygiene","newborn"],[]),
 ("Baby white noise machine","baby",["sleep","travel","naps"],["retail","old"]),

 # ---------------- car ----------------
 ("Cordless car vacuum","car",["crumbs","pets","kids","detailing","resale"],["retail"]),
 ("Car scratch remover","car",["scratches","resale","lease return","satisfying demo"],[]),
 ("Headrest hooks","car",["organization","bags"],["old"]),

 # ---------------- kitchen ----------------
 ("Vacuum sealer","kitchen",["food waste","bulk buying","sous vide","freezer burn"],["retail"]),
 ("Garlic chopper","kitchen",["prep speed","smell"],["retail","old"]),
 ("Herb stripper","kitchen",["prep speed"],["old"]),
 ("Electric salt/pepper grinder","kitchen",["one-hand","arthritis","gift"],["retail"]),

 # ---------------- tech / EDC ----------------
 ("Magnetic gym phone mount","tech",["filming form","hands free","gym"],["old"]),
 ("Bluetooth tracker tag","tech",["keys","luggage","wallet","pets"],["retail"]),
 ("Cable organizer","tech",["desk mess"],["old"]),
 ("Portable power bank","tech",["travel","festival","emergency"],["retail","old"]),
 ("Laptop stand","tech",["neck","posture","desk"],["retail"]),

 # ---------------- misc wellness ----------------
 ("Infrared knee massager","misc",["knee pain","arthritis","athletes","aging parents","surgery recovery"],["policy"]),
 ("Scalp/head massager claw","misc",["relaxation","headache","ASMR","gift"],["retail","old"]),
 ("Posture training wearable","misc",["slouching","tech neck","confidence","back pain","desk work"],[]),
 ("Shoulder brace/support","misc",["shoulder pain","posture","gym"],["size"]),
]

MIN_ANGLES = 6

def main():
    print(f"FIELD SIZE: {len(P)} products\n")
    passed, failed_angles, killed = [], [], []
    for name, niche, angles, kills in P:
        if kills:
            killed.append((name, niche, len(angles), kills)); continue
        if len(angles) < MIN_ANGLES:
            failed_angles.append((name, niche, len(angles))); continue
        passed.append((name, niche, angles))

    print(f"{'='*70}\nKILLED ON FLAGS: {len(killed)}")
    from collections import Counter
    fc = Counter(f for _,_,_,ks in killed for f in ks)
    print("  flag counts:", dict(fc))
    for n,ni,a,ks in killed:
        print(f"   x {n:34} [{ni:6}] angles={a} kills={','.join(ks)}")

    print(f"\n{'='*70}\nFAILED 6-ANGLE GATE: {len(failed_angles)}")
    for n,ni,a in sorted(failed_angles,key=lambda r:-r[2]):
        print(f"   - {n:34} [{ni:6}] angles={a}")

    print(f"\n{'='*70}\nPASSED TO TOURNAMENT: {len(passed)}")
    for n,ni,angles in passed:
        print(f"   + {n:34} [{ni:6}] {len(angles)} angles")
    print(f"\nSURVIVAL RATE: {len(passed)}/{len(P)} = {len(passed)/len(P)*100:.0f}%")
    open('/home/user/Drop/survivors.txt','w').write("\n".join(n for n,_,_ in passed))

if __name__ == "__main__":
    main()
