#!/usr/bin/env python3
"""
Hook gate — does this product actually demo well in short form?

trendcheck.py measures whether people want it. amzsat.py measures whether the
shelf is free. Neither tells you if the thing can be sold in 3 silent seconds,
which is what decides organic short-form. This measures that empirically:
short-form view counts for a product are a proxy for how well it demos.

A product with a real visible mechanism accumulates high-view shorts.
A product whose benefit is invisible or slow does not, no matter how much
search demand it has.

Usage:
    python3 hookcheck.py --json out.json "product one" "product two"
"""
import sys, json, subprocess, statistics, time

VARIANTS = ["{}", "{} before after", "{} review", "{} does it work", "{} how to use"]
MAX_SHORT_SECONDS = 90


def search(query, n=12):
    p = subprocess.run(
        ["yt-dlp", "--dump-json", "--flat-playlist", f"ytsearch{n}:{query}"],
        capture_output=True, timeout=200)
    out = []
    for line in p.stdout.decode("utf-8", "ignore").splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        dur = d.get("duration") or 0
        vc = d.get("view_count") or 0
        if dur and dur <= MAX_SHORT_SECONDS:
            out.append({"views": vc, "dur": dur,
                        "title": (d.get("title") or "")[:70],
                        "id": d.get("id")})
    return out


def grade(p90, median, n):
    """Hook strength from short-form performance."""
    if n < 3:
        return "NO SIGNAL - too few shorts exist"
    if p90 >= 1_000_000:
        return "STRONG - proven viral demo"
    if p90 >= 250_000:
        return "GOOD - demos well"
    if p90 >= 50_000:
        return "MODERATE - works with good creative"
    return "WEAK - does not demo"


def check(product):
    seen, vids = set(), []
    for v in VARIANTS:
        try:
            for r in search(v.format(product)):
                if r["id"] and r["id"] not in seen:
                    seen.add(r["id"])
                    vids.append(r)
        except Exception:
            pass
        time.sleep(1)
    views = sorted((v["views"] for v in vids), reverse=True)
    if not views:
        return {"product": product, "n": 0, "verdict": "NO SIGNAL - no shorts found"}
    k = max(0, int(len(views) * 0.1) - 1)
    p90 = views[k]
    med = int(statistics.median(views))
    return {"product": product, "n": len(views), "max": views[0], "p90": p90,
            "median": med, "total": sum(views),
            "top": [v for v in sorted(vids, key=lambda x: -x["views"])[:3]],
            "verdict": grade(p90, med, len(views))}


def main():
    args = sys.argv[1:]
    out = None
    if args and args[0] == "--json":
        out, args = args[1], args[2:]
    res = []
    for prod in args:
        r = check(prod)
        res.append(r)
        if r["n"]:
            print(f"\n### {prod}")
            print(f"  shorts:{r['n']}  max:{r['max']:,}  p90:{r['p90']:,}  "
                  f"median:{r['median']:,}  total:{r['total']:,}")
            print(f"  --> {r['verdict']}")
            for t in r["top"]:
                print(f"     {t['views']:>10,}  {t['title']}")
        else:
            print(f"\n### {prod}\n  {r['verdict']}")
    if res:
        print("\n\n=========== HOOK SUMMARY (strongest first) ===========")
        order = {"STRONG - proven viral demo": 0, "GOOD - demos well": 1,
                 "MODERATE - works with good creative": 2, "WEAK - does not demo": 3}
        res.sort(key=lambda r: (order.get(r.get("verdict"), 9), -(r.get("p90") or 0)))
        print(f"{'product':38} {'n':>4} {'max':>12} {'p90':>11}  verdict")
        for r in res:
            if not r["n"]:
                print(f"{r['product'][:38]:38} {0:>4} {'-':>12} {'-':>11}  {r['verdict']}")
                continue
            print(f"{r['product'][:38]:38} {r['n']:>4} {r['max']:>12,} {r['p90']:>11,}  {r['verdict']}")
    if out and res:
        json.dump(res, open(out, "w"), indent=2)
        print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
