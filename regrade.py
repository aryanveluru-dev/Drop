#!/usr/bin/env python3
"""Re-run the products that failed on SAMPLE SIZE rather than performance.

grade() previously returned NO SIGNAL for n<3 regardless of views, discarding
products whose few shorts performed well. And p90 collapsed to max at these
sample sizes. This re-queries the affected products with more variants and
grades honestly on max, flagging low-confidence rows instead of binning them.
"""
import json, subprocess, statistics, time
from sweep import TERMS

OUT="hook-results.json"
VARIANTS=["{}","{} review","{} before after","{} how to use","{} results"]
MAX_SHORT=180

def search(q,n=10):
    try:
        p=subprocess.run(["yt-dlp","--dump-json","--flat-playlist",f"ytsearch{n}:{q}"],
                         capture_output=True,timeout=180)
    except subprocess.TimeoutExpired: return []
    out=[]
    for line in p.stdout.decode("utf-8","ignore").splitlines():
        try: d=json.loads(line)
        except: continue
        dur=d.get("duration") or 0
        if dur and dur<=MAX_SHORT:
            out.append({"id":d.get("id"),"views":d.get("view_count") or 0,
                        "title":(d.get("title") or "")[:70]})
    return out

def grade(mx,n):
    if mx is None: return "NO SIGNAL"
    if mx>=1_000_000: g="STRONG"
    elif mx>=250_000: g="GOOD"
    elif mx>=50_000:  g="MODERATE"
    else:             g="WEAK"
    return g+(" (low-n)" if n<3 else "")

rows=json.load(open(OUT))
by={r["product"]:r for r in rows}
targets=[r for r in rows if r["verdict"]=="NO SIGNAL"]
print(f"re-running {len(targets)} products with {len(VARIANTS)} variants each",flush=True)

for i,r in enumerate(targets,1):
    term=TERMS.get(r["product"], r["product"]); seen,vids=set(),[]
    for v in VARIANTS:
        for x in search(v.format(term)):
            if x["id"] and x["id"] not in seen: seen.add(x["id"]); vids.append(x)
        time.sleep(1)
    views=sorted((v["views"] for v in vids),reverse=True)
    if views:
        r.update(n=len(views),max=views[0],median=int(statistics.median(views)),
                 total=sum(views),verdict=grade(views[0],len(views)),
                 top=sorted(vids,key=lambda x:-x["views"])[:2])
        r.pop("p90",None)
    print(f"[{i}/{len(targets)}] {r['product'][:36]:36} n={r['n']:<3} max={r.get('max',0):>10,}  {r['verdict']}",flush=True)
    json.dump(list(by.values()),open(OUT,"w"),indent=2)

# regrade everything on max, drop the broken p90
for r in by.values():
    if r.get("max") is not None:
        r["verdict"]=grade(r["max"],r.get("n",0)); r.pop("p90",None)
json.dump(list(by.values()),open(OUT,"w"),indent=2)
from collections import Counter
print("\nREGRADE COMPLETE",dict(Counter(r["verdict"] for r in by.values())),flush=True)
