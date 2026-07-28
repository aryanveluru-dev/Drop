#!/usr/bin/env python3
"""
Expanded tournament field. Goal: find 100 products that SURVIVE the 6-angle gate.

Format per row:  name | niche | angle1;angle2;... | killflags
An angle = a distinct motivation or audience, not a rephrasing.
Kill flags: retail (on a CVS/Target shelf), size (size variance),
            old (wow factor decayed), policy (regulated claim / restricted ads)

The standard is unchanged from the 104-product run. Only the field is larger,
and deliberately weighted toward categories that are structurally angle-rich:
devices with multiple symptom targets, products spanning several life stages,
and items with both aesthetic and functional payoffs.
"""

RAW = """
# ---------------- SLEEP & BREATHING ----------------
Magnetic nasal dilator|sleep|partner snoring;energy & brain fog;jawline/mouth-breathing;athletic performance;dry mouth;sleep quality|
Internal nasal vent|sleep|snoring;deviated septum;athletic breathing;allergy season;travel sleep;dry mouth|
Jaw support strap|sleep|mouth breathing;snoring;face shape;dry mouth;CPAP adjunct;travel|
Anti-snore side-sleep trainer|sleep|partner snoring;back-sleep training;travel;posture;sleep quality;reflux|policy
Weighted sleep mask|sleep|insomnia;migraine;travel;light sleeper;anxiety;eye puffiness|retail
Cooling mattress topper|sleep|night sweats;menopause;partner temp war;sleep quality;hot climate;memory foam heat|
Smart sleep tracker mat|sleep|sleep score;snoring detection;recovery;longevity;partner;shift work|
White noise + blackout travel kit|sleep|travel;shift work;noisy neighbours;baby;focus;hotel|retail
Bed wedge pillow|sleep|reflux;snoring;congestion;post-surgery;reading;circulation|
Sunrise alarm|sleep|groggy waking;winter blues;phone-free bedroom;kids;shift work|retail
Mouth tape|sleep|snoring;jawline;morning energy;dry mouth;oral health;athletic|retail
CPAP cleaning device|sleep|hygiene;odour;compliance;travel;infection;partner|
Knee pillow side sleeper|sleep|hip pain;back pain;pregnancy;sciatica;posture;partner disturbance|
Anti-snore smart pillow|sleep|snoring;partner;neck pain;sleep quality;travel;apnea adjunct|policy
Sleep headphone headband|sleep|insomnia;travel;partner noise;meditation;side sleeper;tinnitus|

# ---------------- HAIR & SCALP ----------------
Red light hair cap|hair|thinning;postpartum shed;male pattern;confidence;scalp health;drug-free option|policy
Derma stamp scalp roller|hair|thinning;serum absorption;beard;scars;confidence;eyebrows|
Scalp SPF spray|hair|part-line burn;hair loss;aging;outdoor sport;bald head;kids|
Scalp cooling cap|hair|chemo shed;heat damage;inflammation;itch;post-colour|policy
Heatless curl set|hair|heat damage;overnight styling;time saving;breakage;travel;kids hair|old
Hair steamer cap|hair|deep conditioning;curly care;dryness;salon cost;scalp health;colour retention|
Scalp exfoliating serum applicator|hair|dandruff;buildup;growth;itch;oily roots;colour prep|
Beard growth roller|mens|patchy beard;density;confidence;scars;masculinity;grooming|
Hair fiber powder|hair|instant coverage;thinning;events;confidence|old
Laser comb|hair|thinning;portability;drug-free;confidence;beard|policy

# ---------------- FACE DEVICES ----------------
Microcurrent facial device|face|jawline lift;aging;puffiness;makeup prep;filler alternative;confidence|
Red light face mask|face|wrinkles;acne;aging;pores;glow;botox alternative|
Under-eye microcurrent wand|face|dark circles;bags;tired look;aging;video calls;hangover|
Jaw exerciser|face|jawline;double chin;mewing;confidence;TMJ;facial symmetry|
Cryo face globes|face|puffiness;redness;hangover;makeup prep;migraine;rosacea|old
Facial steamer|face|congestion;pores;skincare absorption;sinus;dry skin;at-home facial|
High-frequency wand|face|acne;scalp;wound healing;oil control;salon alternative|
Face yoga tool kit|face|jawline;wrinkles;puffiness;TMJ;confidence;drug-free|
LED neck & décolleté device|face|neck lines;tech neck;sun damage;aging;chest wrinkles;confidence|
Nano mist sprayer|face|hydration;makeup setting;travel;dry office;summer|old

# ---------------- SKIN & BODY TREATMENT ----------------
Body red light panel|body|recovery;skin;pain;circulation;mood;sleep|policy
Cellulite vacuum cups|body|cellulite;lymphatic;recovery;circulation;satisfying demo|old
Lymphatic drainage body tool|body|bloating;cellulite;puffiness;post-op;circulation;detox|
Ice bath tub|body|recovery;mood;discipline;inflammation;metabolism;sleep|
Sauna blanket|body|detox;recovery;weight;menopause;relaxation;skin|
Body exfoliating glove system|body|KP/chicken skin;ingrowns;tan prep;dead skin;circulation|retail
Stretch mark microneedle roller|body|stretch marks;postpartum;scars;cellulite;absorption;confidence|
Back acne treatment applicator|body|bacne;reach;confidence;summer;shoulders;scarring|
Ingrown hair treatment roller|body|ingrowns;razor bumps;bikini line;beard;legs;confidence|
Hand & foot paraffin bath|body|arthritis;dry skin;circulation;salon cost;nails;relaxation|

# ---------------- RECOVERY & CIRCULATION ----------------
Compression recovery boots|recovery|recovery;circulation;swelling;endurance athletes;travel legs;varicose|
Percussion massage gun|recovery|soreness;knots;athletes;warm-up;gift|retail old
Heated shiatsu neck massager|recovery|neck pain;desk work;tension headache;stress;gift;driving|
Foot circulation massager|recovery|diabetic feet;standing job;swelling;plantar;elderly;circulation|
Arm compression sleeves|recovery|recovery;lymphatic;post-op;athletes;swelling;travel|size
Handheld deep tissue roller|recovery|calves;IT band;plantar;travel;desk;pre-workout|old
Infrared knee wrap|recovery|knee pain;arthritis;athletes;post-op;aging;circulation|policy
Cupping therapy set|recovery|back pain;recovery;cellulite;circulation;athletes|old
Contrast therapy foot spa|recovery|standing job;circulation;plantar;swelling;relaxation;diabetic|
Vibrating foam roller|recovery|soreness;mobility;IT band;warm-up;travel|old

# ---------------- ORAL & DENTAL ----------------
LED teeth whitening kit|oral|stains;confidence;dating;photos;coffee/wine;wedding|
Water flosser cordless|oral|gums;breath;braces;implants;dentist cost;travel|retail
Teeth-grinding night guard|oral|bruxism;jaw pain;headache;dental cost;partner noise;TMJ|
Tongue scraper|oral|breath;microbiome;taste|retail old
Electric toothbrush UV sanitiser|oral|hygiene;travel;gum health;kids;braces|retail
Dental calculus remover|oral|tartar;dentist cost;satisfying demo;stains;breath;confidence|policy
Whitening pen travel|oral|touch-up;travel;events;coffee;dating|retail

# ---------------- MEN'S ----------------
Body groomer trimmer|mens|manscaping;hygiene;appearance;partner;sport;summer|retail
Forearm/grip trainer|mens|forearm size;grip strength;climbing;tennis elbow;aesthetics;rehab|
Chest compression top|mens|gyno;confidence;posture|size policy
Beard straightener brush|mens|frizz;volume;speed;appearance|old
Hair loss microneedle + serum kit|mens|thinning;absorption;drug-free;confidence;beard;temples|policy
Posture shirt|mens|slouching;confidence;back pain;desk|size
Cologne sample discovery set|mens|dating;signature scent;gifting;trying before buying;confidence|
Shoe height insoles|mens|height;confidence;dating;interviews|size

# ---------------- FITNESS & STRENGTH ----------------
Portable drag sled|fit|sled training;no turf;HYROX;conditioning;home gym|
Hip thrust belt|fit|glutes;no-barbell;home gym;hip bruising;women lifting|
Tib bar|fit|shin splints;knee health;runners;ATG|
Adjustable kettlebell|fit|space;home gym;travel;cost vs set;beginner;progression|
Wrist wraps|fit|wrist pain;pressing;confidence;rehab|retail
Resistance band door anchor system|fit|home gym;travel;rehab;glutes;apartment;beginner|
Weighted vest|fit|walking;calisthenics;rucking;bone;cardio|old
Blood flow restriction cuffs|fit|hypertrophy;rehab;low load;post-op;time efficiency;aging|policy
Balance board trainer|fit|ankle rehab;core;ski prep;surf;desk;proprioception|
Grip strength dynamometer|fit|longevity metric;rehab;tracking;climbing;aging|

# ---------------- MOBILITY & PAIN ----------------
Neck traction device|pain|neck pain;tech neck;posture;headache;disc;desk work|
TMJ jaw massage device|pain|clenching;headache;dental cost;stress;jawline;ear pain|
Spinal decompression back stretcher|pain|back pain;sciatica;desk work;posture;disc;drug-free|
Posture training wearable|pain|slouching;tech neck;confidence;back pain;desk work|
Shoulder pulley|pain|frozen shoulder;post-op;rotator cuff;aging;rehab cost|retail
Sciatica seat cushion|pain|sciatica;driving;desk;pregnancy;tailbone;haemorrhoids|
Plantar fasciitis night splint|pain|heel pain;morning pain;runners;standing job|size
Carpal tunnel wrist brace|pain|typing;pregnancy;gaming;night pain;post-op|size
Knee decompression brace|pain|knee pain;arthritis;sport;aging;post-op;stairs|size
Heat + vibration back belt|pain|back pain;period cramps;kidney;desk;driving;cold weather|

# ---------------- NERVOUS SYSTEM & STRESS ----------------
Vagus nerve stimulator|nerve|anxiety;sleep;HRV;focus;gut;burnout|policy
Breathwork/CO2 trainer|nerve|anxiety;athletic;sleep;focus;lung capacity;HRV|
Acupressure mat|nerve|back pain;stress;sleep;circulation;cheap massage|old
Weighted blanket|nerve|anxiety;insomnia;ADHD;sensory|retail old
Red light + sound meditation lamp|nerve|sleep;anxiety;focus;circadian;mood;evening wind-down|
Biofeedback stress ring|nerve|anxiety;HRV;focus;sleep;burnout;wearable tracking|
Sensory fidget desk set|nerve|ADHD;focus;anxiety;quitting smoking;meetings|old

# ---------------- GUT & DIGESTION ----------------
Abdominal massage roller|gut|bloating;constipation;cortisol belly;lymphatic;post-meal|
Castor oil pack|gut|bloating;liver;period pain;sleep|policy
Heated abdominal belt|gut|bloating;cramps;IBS;back;cold;post-meal|
Posture + core breathing trainer|gut|bloating;diaphragm;posture;anxiety;pelvic floor;singing|

# ---------------- FEET & LOWER LIMB ----------------
Toe spacers|feet|bunions;foot pain;barefoot training;posture;runners|old
Electric callus remover|feet|calluses;sandal season;satisfying demo;diabetic|retail
Arch support insoles|feet|plantar;flat feet;standing job;knee pain;runners;back pain|size
Ingrown toenail correction kit|feet|ingrowns;pain;podiatrist cost;recurrence;diabetic|policy
Foot alignment socks|feet|bunions;plantar;posture;runners;recovery|size
Compression socks|feet|travel;standing job;varicose;pregnancy;swelling;athletes|retail size

# ---------------- EYES & VISION ----------------
Heated eye mask|eyes|dry eye;screen fatigue;sleep;migraine;styes;puffiness|
Eye massager device|eyes|screen fatigue;dark circles;migraine;sleep;puffiness|
Blue light glasses|eyes|screen;sleep;headache|retail old policy
Eyelid hygiene cleanser wand|eyes|blepharitis;styes;dry eye;makeup;contact lens;demodex|policy

# ---------------- HANDS & NAILS ----------------
Electric nail drill kit|nails|salon cost;gel removal;hobby;cuticles|
Nail fungus laser|nails|fungus;sandal shame;diabetic;recurrence|policy
Hand therapy putty + grip kit|nails|arthritis;post-op;climbing;stress;kids OT;typing|
UV gel starter kit|nails|salon cost;hobby;gifting;chip resistance;length|

# ---------------- WOMEN'S HEALTH ----------------
Pelvic floor trainer|womens|leaking;postpartum;menopause;lifting;confidence;intimacy|policy
Period TENS device|womens|cramps;drug-free;work;endometriosis|policy
Menstrual heat patch belt|womens|cramps;back;work;drug-free;travel;endometriosis|
Breast pump wearable|womens|hands-free;work;discretion;supply;travel;comfort|
Postpartum belly binder|womens|diastasis;support;posture|size
Perineal cooling pack|womens|postpartum;swelling;stitches;haemorrhoids;comfort|
Menopause cooling neck wrap|womens|hot flushes;night sweats;work;sleep;travel;exercise|

# ---------------- PREGNANCY & BABY ----------------
Pregnancy support belt|baby|back pain;pelvic girdle;walking;work;second pregnancy|size
Electric nasal aspirator|baby|congestion;sleep;sick season;gentler than bulb|
Baby bottle washer|baby|time;hygiene;newborn|
Baby food maker|baby|cost;nutrition control;allergens;weaning;waste|
Toddler stair gate|baby|safety;pets;renters;travel|retail
Baby sleep sack weighted|baby|sleep;startle reflex;safety;transition;temperature|policy

# ---------------- SENIOR / AGING ----------------
Bed rail assist handle|senior|falls;getting up;post-op;confidence;caregiver;disability|
Medication dispenser alarm|senior|adherence;dementia;caregiver;multiple meds;travel|
Stair-free reacher grabber|senior|mobility;back;post-op;disability;cleaning|retail
Fall detection pendant|senior|falls;living alone;caregiver peace of mind;dementia|policy
Adaptive jar opener|senior|arthritis;grip;independence;one-handed;kitchen|retail
Shower grab bar suction|senior|falls;renters;travel;post-op;pregnancy;disability|
Bed transfer swivel cushion|senior|car transfer;hip replacement;caregiver;mobility;independence|

# ---------------- PET ----------------
Dog nail grinder|pet|nail anxiety;groomer cost;quick fear;noise-free|
Pet deshedding vacuum attachment|pet|shedding;allergies;grooming cost;mess;bonding;car|
Cat water fountain|pet|hydration;kidney disease;picky cats;filter;multi-pet|retail
Pet dental finger brush|pet|breath;vet cost;plaque;small dogs|policy
Dog training e-collar|pet|recall;barking;safety;off-leash|policy
Pet paw cleaner cup|pet|muddy paws;floors;allergies;winter salt;apartment|
Slow feeder bowl|pet|bloat;gulping;enrichment|retail
Pet stroller|pet|elderly dogs;post-op;small breeds;travel;anxiety;multi-pet|

# ---------------- HOME AIR & WATER ----------------
Air quality monitor|home|allergies;mould;kids;VOCs;sleep|
Under-sink water filter|home|taste;microplastics;cost vs bottled;health|
Shower head filter|home|hair;skin;hard water;chlorine|
Dehumidifier compact|home|mould;damp;allergies;laundry drying;musty smell;renters|
Wireless portable humidifier|home|dry air;skin;sleep;desk;travel;plants|
HEPA air purifier desk|home|allergies;pets;smoke;office;kids;odour|retail
Radon/CO detector|home|safety;renters;peace of mind;selling home|retail policy

# ---------------- CLEANING & HOME ----------------
Electric spin scrubber|home|bathroom;satisfying demo;back strain;grout|old
Robot window cleaner|home|high windows;safety;time;satisfying|
Steam cleaner handheld|home|sanitising;grout;mattress;pets;allergies;chemical-free|
Grout pen & repair kit|home|stains;renters;selling home;cheap reno;satisfying|
Drain snake / clog tool|home|clogs;plumber cost;hair;satisfying demo;bathroom|retail
Mattress vacuum UV|home|dust mites;allergies;asthma;bed bugs;odour;kids|
Laundry lint / pet hair catcher|home|pet hair;lint;clothes life;washing machine|retail old

# ---------------- KITCHEN ----------------
Vacuum sealer|kitchen|food waste;bulk;sous vide;freezer burn|retail
Countertop ice maker nugget|kitchen|nugget ice;entertaining;cost vs fridge;RV;office|
Electric jar/can opener|kitchen|arthritis;one-handed;seniors;grip|retail
Food dehydrator|kitchen|snacks;jerky;waste;camping;herbs;pet treats|
Kitchen composter electric|kitchen|smell;waste;garden;eco;apartment;council rules|
Cold brew maker|kitchen|coffee cost;acidity;batch;summer;gifting|retail

# ---------------- CAR & TRAVEL ----------------
Car scratch remover|car|scratches;resale;lease return;satisfying demo|
Cordless car vacuum|car|crumbs;pets;kids;detailing;resale|retail
Car seat gap filler|car|dropped items;crumbs;phone;organisation|old
Tyre inflator portable|car|flat tyre;safety;bikes;sports balls;fuel economy;RV|
Travel luggage scale|travel|overweight fees;packing;frequent flyer|retail old
Neck pillow memory foam|travel|flight sleep;neck pain;car;office nap|retail old
Packing cube compression set|travel|space;organisation;carry-on only;family;laundry separation|retail
Universal travel adapter|travel|international;multi-device;work trips|retail

# ---------------- DESK & ERGONOMICS ----------------
Under-desk treadmill|desk|steps;WFH;weight;energy;back;focus|
Laptop riser + docking|desk|neck;posture;desk space;cable mess|retail
Footrest rocker|desk|circulation;posture;fidget;short legs;back|
Monitor light bar|desk|eye strain;glare;desk space;night work;aesthetics|
Anti-fatigue standing mat|desk|standing desk;back;knees;circulation;kitchen|

# ---------------- OUTDOOR & HOBBY ----------------
Portable power station|outdoor|camping;blackout;RV;work site;photography;emergency|
Solar camp lantern|outdoor|camping;blackout;kids;garden;emergency|retail
Bug repellent wearable|outdoor|mosquitoes;kids;garden;camping;chemical-free;travel|policy
Fishing line spooler|hobby|line changes;tackle shop cost;time;beginners|
Resin art starter kit|hobby|craft;gifting;side income;kids;jewellery|
Diamond painting kit|hobby|relaxation;anxiety;gifting;seniors;kids;screen-free|
Electric wood carving pen|hobby|craft;gifting;side income;beginners;precision|

# ---------------- KIDS & LEARNING ----------------
Kids drawing tablet LCD|kids|screen-free;travel;restaurant;paper waste;homework|old
Montessori busy board|kids|fine motor;screen-free;travel;autism;toddler|
Kids posture chair|kids|posture;homework;growth;desk;back|size
Reading pen translator|kids|dyslexia;ESL;homework;vocabulary;independence|
"""

RAW2 = """
# ---------------- SKIN CONDITIONS ----------------
Eczema wet-wrap sleeve set|skin|eczema;kids scratching;sleep;steroid reduction;winter;sensitive skin|
Rosacea LED redness device|skin|rosacea;flushing;confidence;makeup reduction;sensitivity;winter|
Psoriasis scalp applicator|skin|psoriasis;flaking;itch;hair;confidence;steroid delivery|policy
Silicone scar sheets|skin|surgery scars;C-section;acne scars;burns;tattoo removal;keloids|
Keratosis pilaris body kit|skin|chicken skin;arms;confidence;summer;exfoliation;kids|
Hyperpigmentation LED spot device|skin|dark spots;melasma;acne marks;aging;confidence;sun damage|
Tattoo aftercare film kit|skin|healing;colour retention;infection;showering;artist recommendation;fading|
Fungal acne scalp/back kit|skin|folliculitis;bacne;gym;sweat;confidence;summer|policy

# ---------------- HEARING & EAR ----------------
Ear wax removal camera tool|ear|wax;hearing;doctor cost;satisfying demo;kids;hearing aid users|
Musician ear plugs|ear|concerts;tinnitus prevention;drummers;motorcycles;sleep;sensory|
Tinnitus masking device|ear|tinnitus;sleep;focus;anxiety;hearing loss|policy
Ear dryer for swimmers|ear|swimmers ear;infections;kids;hearing aid moisture;showering;surfers|
Kids noise-cancelling earmuffs|ear|autism/sensory;concerts;fireworks;study;flights;lawnmower|

# ---------------- SPORT-SPECIFIC ----------------
Golf swing tempo trainer|sport|slice fix;tempo;indoor practice;winter;handicap;warm-up|
Cycling bike fit laser tool|sport|knee pain;power;saddle sore;new bike;bike fit cost|
Swim paddles + tempo trainer|sport|technique;shoulder;stroke rate;triathlon;endurance|
Running gait sensor insole|sport|injury prevention;cadence;form;shin splints;marathon training;shoe choice|
Climbing hangboard portable|sport|finger strength;home training;travel;tendon;plateau;warm-up|
Boxing reflex ball|sport|reflexes;cardio;stress;kids;small space;coordination|old
Basketball shooting form sleeve|sport|form;wrist;youth coaching;consistency;confidence|size
Tennis elbow compression strap|sport|tennis elbow;golfers elbow;lifting;typing;trades;rehab|size
Ski/snowboard boot dryer|sport|wet boots;odour;blisters;frostbite;hockey;work boots|
Archery/shooting stability trainer|sport|steadiness;breathing;focus;hunting;competition|policy

# ---------------- OCCUPATIONAL ----------------
Nurse compression shoe insole|work|12-hour shifts;plantar;back pain;swelling;standing;varicose|size
Anti-vibration work gloves|work|trades;HAVS;grip;cold;blisters;power tools|size
Welding/trades knee pads|work|kneeling;flooring;gardening;joint damage;concrete|size
Truck driver lumbar cushion|work|long haul;sciatica;posture;fatigue;desk;flights|
Chef anti-slip clogs insole|work|standing;grease;back;shifts;knees|size
Teacher voice amplifier|work|voice strain;large rooms;tour guides;fitness instructors;hearing students|
Hairdresser wrist support|work|RSI;scissors;shifts;tendonitis;grip|size

# ---------------- CONTENT & CREATOR ----------------
Teleprompter phone rig|creator|scripts;eye contact;UGC;courses;interviews;confidence|
Portable ring light + diffuser|creator|UGC;video calls;makeup;photography;travel|retail old
Lavalier wireless mic|creator|audio quality;interviews;UGC;courses;vlogging;podcasts|
Green screen collapsible|creator|backgrounds;WFH calls;streaming;UGC;small space|
Phone gimbal stabiliser|creator|walking shots;vlogs;UGC;travel;real estate|

# ---------------- GAMING ----------------
Gaming wrist rest cooling|gaming|RSI;sweat;long sessions;desk;aesthetics|
Controller thumb grips|gaming|slip;sweat;precision;wear;aesthetics|old
Gaming posture chair cushion|gaming|back pain;long sessions;posture;desk;height|
Blue-blocking gaming glasses|gaming|eye strain;sleep;headache|retail old policy

# ---------------- SMOKING / HABIT ----------------
Nicotine habit fidget device|habit|quitting;oral fixation;anxiety;hands;driving;meetings|policy
Alcohol-free spirit sampler|habit|dry january;sober curious;pregnancy;driving;gifting;hosting|

# ---------------- WEIGHT & METABOLIC ----------------
Smart body composition scale|metab|body fat;muscle;progress tracking;family;GLP-1 users;longevity|
Portion control plate set|metab|portions;kids;diabetes;GLP-1;bariatric;mindful eating|policy
Food scale nutrition tracker|metab|macros;baking;portions;diabetes;meal prep;GLP-1|
Calf/leg elevation wedge|metab|swelling;circulation;varicose;post-op;pregnancy;back|

# ---------------- POST-SURGICAL & MEDICAL-ADJACENT ----------------
Post-op shower cast cover|medical|showering;casts;PICC lines;wound care;swimming;kids|
Sock aid + dressing stick|medical|hip replacement;back;pregnancy;arthritis;disability;independence|
Ice therapy shoulder wrap|medical|post-op;rotator cuff;athletes;arthritis;swelling;migraine|
Leg elevation post-surgery pillow|medical|post-op;swelling;varicose;pregnancy;back;circulation|
Pill crusher & splitter|medical|swallowing;seniors;pets;dosing;caregiver|retail

# ---------------- GARDEN & OUTDOOR HOME ----------------
Garden kneeler seat|garden|knees;back;getting up;seniors;planting;tool storage|
Soil moisture/pH meter|garden|plant death;overwatering;lawn;houseplants;veg;beginners|
Electric weed burner|garden|chemical-free;pets;kids;paving;time;eco|
Rain barrel diverter kit|garden|water bill;drought;eco;plants;council rebate|
Hose splitter smart timer|garden|holidays;water bill;consistency;lawn;veg;forgetfulness|

# ---------------- ALLERGY & IMMUNE ----------------
Nasal irrigation system|allergy|allergies;sinusitis;congestion;kids;post-nasal drip;dry air|
Dust mite mattress encasement|allergy|allergies;asthma;eczema;bed bugs;kids;odour|
Allergen-blocking nasal balm|allergy|pollen;pets;drug-free;pregnancy;kids;travel|policy
Steam inhaler|allergy|congestion;sinus;cold season;kids;asthma;dry air|

# ---------------- ORAL/FACIAL AESTHETIC (extended) ----------------
Lip plumping device|beauty|lip volume;filler alternative;aging;confidence;photos;lipstick|
Eyebrow microblading pen kit|beauty|sparse brows;salon cost;aging;alopecia;confidence;symmetry|
Eyelash growth applicator|beauty|sparse lashes;extension damage;aging;confidence;mascara reduction|policy
At-home dermaplaning tool|beauty|peach fuzz;makeup application;exfoliation;salon cost;skincare absorption|retail
Hair removal IPL device|beauty|shaving time;ingrowns;salon cost;PCOS;sensitive skin;confidence|

# ---------------- FOCUS & PRODUCTIVITY ----------------
Pomodoro focus timer cube|focus|ADHD;procrastination;study;WFH;screen-free;meetings|
Phone lockbox timer|focus|screen addiction;study;family dinner;sleep;kids;work|
Noise-masking desk speaker|focus|open office;WFH;tinnitus;study;privacy;sleep|
"""

RAW = RAW + RAW2


def parse():
    rows = []
    for line in RAW.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) < 3:
            continue
        name, niche, angles = parts[0], parts[1], parts[2]
        kills = parts[3].split() if len(parts) > 3 and parts[3].strip() else []
        rows.append((name.strip(), niche.strip(),
                     [a.strip() for a in angles.split(";") if a.strip()], kills))
    return rows


MIN_ANGLES = 6

def main():
    P = parse()
    passed, failed, killed = [], [], []
    for name, niche, angles, kills in P:
        if kills:
            killed.append((name, niche, len(angles), kills))
        elif len(angles) < MIN_ANGLES:
            failed.append((name, niche, len(angles)))
        else:
            passed.append((name, niche, angles))

    from collections import Counter
    print(f"FIELD SIZE            : {len(P)}")
    print(f"killed on flags       : {len(killed)}")
    print(f"failed 6-angle gate   : {len(failed)}")
    print(f"SURVIVORS             : {len(passed)}  ({len(passed)/len(P)*100:.0f}%)\n")
    print("kill-flag counts      :", dict(Counter(f for _,_,_,ks in killed for f in ks)))
    print("survivors by niche    :", dict(Counter(n for _,n,_ in passed)))

    print(f"\n{'='*72}\nSURVIVORS ({len(passed)})\n{'='*72}")
    for i,(n,ni,a) in enumerate(passed,1):
        print(f"{i:>3}. {n:38} [{ni:8}] {len(a)} angles")

    with open('/home/user/Drop/survivors.txt','w') as f:
        for n,ni,a in passed:
            f.write(f"{n}\t{ni}\t{'; '.join(a)}\n")

if __name__ == "__main__":
    main()
