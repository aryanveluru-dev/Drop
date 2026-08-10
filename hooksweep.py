#!/usr/bin/env python3
"""
Demand gate via short-form performance — the fallback for a blocked Trends API.

Google Trends 429s at scale. YouTube via yt-dlp does not, and short-form view
counts arguably measure the thing we actually care about better than search
volume does: whether this product commands attention in the format we would
sell it in.

Two query variants per product (plain, and "before after") to keep runtime
sane across 137 products. Results write incrementally; completed products are
skipped on re-run.
"""
import json, os, subprocess, statistics, time, sys

OUT = "/home/user/Drop/hook-results.json"
SURV = "/home/user/Drop/survivors.txt"
MAX_SHORT = 180  # seconds

PRIORITY = ["chronic","skin","face","sleep","body","pain","recovery","womens","hair",
            "mens","nerve","mood","metab","medical","beauty","oral","eyes","ear",
            "allergy","gut","senior","fit","sport","focus","home","nails","work",
            "creator","pet","desk","kitchen","garden","home2","rv","moto","music",
            "maker","aqua","security","yoga","learn","baby2","clean2","car","outdoor",
            "hobby","event","habit"]


def load_terms():
    from sweep import TERMS
    rows = []
    for line in open(SURV):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        prod, niche = parts[0], parts[1]
        rows.append((prod, niche, TERMS.get(prod, prod)))
    rank = {n: i for i, n in enumerate(PRIORITY)}
    rows.sort(key=lambda r: rank.get(r[1], 99))
    return rows


def search(query, n=10):
    try:
        p = subprocess.run(
            ["yt-dlp", "--dump-json", "--flat-playlist", f"ytsearch{n}:{query}"],
            capture_output=True, timeout=180)
    except subprocess.TimeoutExpired:
        return []
    out = []
    for line in p.stdout.decode("utf-8", "ignore").splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        dur = d.get("duration") or 0
        if dur and dur <= MAX_SHORT:
            out.append({"id": d.get("id"), "views": d.get("view_count") or 0,
                        "title": (d.get("title") or "")[:70]})
    return out


def grade(p90, n):
    if n < 3:
        return "NO SIGNAL"
    if p90 >= 1_000_000: return "STRONG"
    if p90 >= 250_000:   return "GOOD"
    if p90 >= 50_000:    return "MODERATE"
    return "WEAK"


def main():
    done = {}
    if os.path.exists(OUT):
        done = {r["product"]: r for r in json.load(open(OUT))}
    rows = [r for r in load_terms() if r[0] not in done]
    print(f"{len(done)} done · {len(rows)} to go", flush=True)

    for i, (prod, niche, term) in enumerate(rows, 1):
        seen, vids = set(), []
        for q in (term, f"{term} before after"):
            for r in search(q):
                if r["id"] and r["id"] not in seen:
                    seen.add(r["id"]); vids.append(r)
            time.sleep(1)
        views = sorted((v["views"] for v in vids), reverse=True)
        if views:
            k = max(0, int(len(views)*0.1) - 1)
            rec = {"product": prod, "niche": niche, "term": term, "n": len(views),
                   "max": views[0], "p90": views[k],
                   "median": int(statistics.median(views)),
                   "total": sum(views), "verdict": grade(views[k], len(views)),
                   "top": sorted(vids, key=lambda x: -x["views"])[:2]}
        else:
            rec = {"product": prod, "niche": niche, "term": term, "n": 0,
                   "verdict": "NO SIGNAL"}
        done[prod] = rec
        json.dump(list(done.values()), open(OUT, "w"), indent=2)
        mx = f"{rec.get('max',0):,}"
        print(f"[{i}/{len(rows)}] {prod[:36]:36} n={rec['n']:<3} max={mx:>10}  {rec['verdict']}", flush=True)

    allr = list(done.values())
    order = {"STRONG":0,"GOOD":1,"MODERATE":2,"WEAK":3,"NO SIGNAL":9}
    allr.sort(key=lambda r: (order.get(r["verdict"],9), -(r.get("p90") or 0)))
    print("\n=========== HOOK SWEEP COMPLETE ===========", flush=True)
    for r in allr:
        print(f"{r['product'][:38]:38} [{r['niche']:8}] "
              f"max={r.get('max',0):>10,}  {r['verdict']}")
    from collections import Counter
    print("\n", dict(Counter(r["verdict"] for r in allr)))


if __name__ == "__main__":
    main()
