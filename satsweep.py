#!/usr/bin/env python3
"""Saturation sweep over the demand-gate survivors."""
import json, os, sys, time
sys.argv=['x']
exec(open('/home/user/Drop/amzsat.py').read().replace('if __name__ == "__main__":\n    main()',''))

OUT="sat-results.json"
TERMS={
"Spinal decompression back stretcher":"back stretcher spinal decompression",
"Ingrown hair treatment roller":"ingrown hair treatment tool",
"Ear wax removal camera tool":"ear wax removal camera",
"Eyebrow microblading pen kit":"eyebrow microblading pen",
"Forearm/grip trainer":"forearm grip trainer",
"Balance board trainer":"balance board trainer",
"Posture + core breathing trainer":"breathing exercise device",
"Beard growth roller":"beard growth roller",
"Hair removal IPL device":"ipl hair removal device",
"Ear dryer for swimmers":"ear dryer swimmers",
"Contrast therapy foot spa":"foot spa massager",
"Motorcycle bluetooth helmet intercom":"motorcycle bluetooth intercom",
"Phone lockbox timer":"phone lock box timer",
"Breathwork/CO2 trainer":"breathing trainer device",
"Biofeedback stress ring":"stress tracking ring",
"LED neck & décolleté device":"neck firming led device",
"Teeth-grinding night guard":"night guard teeth grinding",
"Sciatica seat cushion":"sciatica seat cushion",
"Climbing hangboard portable":"portable hangboard",
"Menstrual heat patch belt":"period heating pad belt",
"Post-op shower cast cover":"shower cast cover",
"Sock aid + dressing stick":"sock aid dressing stick",
"IBS heat + vibration pad":"stomach heating pad",
"Tattoo aftercare film kit":"tattoo aftercare film",
"Keratosis pilaris body kit":"keratosis pilaris treatment",
"Silicone scar sheets":"silicone scar sheets",
"Jaw exerciser":"jaw exerciser",
"Foot circulation massager":"foot circulation massager",
}
done={}
if os.path.exists(OUT): done={r["kw"]:r for r in json.load(open(OUT))}
todo=[(p,t) for p,t in TERMS.items() if t not in done]
print(f"{len(done)} done · {len(todo)} to go",flush=True)
for i,(prod,term) in enumerate(todo,1):
    r=report(term,verbose=False)
    if r:
        r["product"]=prod; done[term]=r
        json.dump(list(done.values()),open(OUT,"w"),indent=2)
        pr=f"${r['price_lo']:.0f}-{r['price_hi']:.0f}" if r.get('price_lo') else "-"
        print(f"[{i}/{len(todo)}] {prod[:34]:34} med={r['median']:>5} >1k={r['big']}/{r['n']:<3} {pr:>12}  {r['verdict']}",flush=True)
    else:
        print(f"[{i}/{len(todo)}] {prod[:34]:34} BLOCKED",flush=True)
    time.sleep(6)
print("\nSAT SWEEP COMPLETE",flush=True)
