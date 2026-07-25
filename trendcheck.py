#!/usr/bin/env python3
"""
Google Trends demand gate.

Answers the question amzsat.py cannot: is interest RISING, flat, or dying?
Finding "grip socks before they were popular" needs low saturation AND rising demand.

Usage:
    python3 trendcheck.py "keyword one" "keyword two" ...
    python3 trendcheck.py --json out.json --tf "today 5-y" "keyword" ...
"""
import sys, json, time, statistics

from pytrends.request import TrendReq


def slope(series):
    """Mean of last quarter vs mean of first quarter, as % change."""
    if len(series) < 8:
        return None
    q = max(2, len(series) // 4)
    first = statistics.mean(series[:q])
    last = statistics.mean(series[-q:])
    if first == 0:
        return 999.0 if last > 0 else 0.0
    return round((last - first) / first * 100, 1)


def classify(g12, g5, peak_recent):
    if g12 is None:
        return "NO DATA"
    if g12 > 60 and peak_recent:
        return "BREAKOUT - rising fast, near peak now"
    if g12 > 25:
        return "RISING"
    if g12 > -10:
        return "FLAT"
    if g12 > -40:
        return "COOLING"
    return "DECLINING"


def check(kw, pt, tf12="today 12-m", tf5="today 5-y", geo="US"):
    out = {"kw": kw}
    for label, tf in (("12m", tf12), ("5y", tf5)):
        for attempt in range(4):
            try:
                pt.build_payload([kw], timeframe=tf, geo=geo)
                df = pt.interest_over_time()
                if df.empty:
                    out[label] = None
                    break
                s = [int(v) for v in df[kw].tolist()]
                out[label] = s
                break
            except Exception as e:
                if attempt == 3:
                    out[label] = None
                    out.setdefault("errors", []).append(f"{label}:{type(e).__name__}")
                time.sleep(8 * (attempt + 1))
        time.sleep(3)
    s12, s5 = out.get("12m"), out.get("5y")
    out["g12"] = slope(s12) if s12 else None
    out["g5"] = slope(s5) if s5 else None
    # is the recent period at/near the all-time high of the 5y window?
    peak_recent = False
    if s5:
        tail = max(s5[-8:]) if len(s5) >= 8 else max(s5)
        peak_recent = tail >= 0.85 * max(s5)
    out["peak_recent"] = peak_recent
    out["current"] = s12[-2] if s12 and len(s12) > 1 else None
    out["verdict"] = classify(out["g12"], out["g5"], peak_recent)
    return out


def main():
    args = sys.argv[1:]
    out_path, tf12 = None, "today 12-m"
    while args and args[0].startswith("--"):
        if args[0] == "--json":
            out_path = args[1]; args = args[2:]
        elif args[0] == "--tf":
            tf12 = args[1]; args = args[2:]
        else:
            args = args[1:]
    pt = TrendReq(hl="en-US", tz=360)
    res = []
    for kw in args:
        r = check(kw, pt, tf12=tf12)
        res.append(r)
        print(f"{r['kw'][:40]:40} 12m:{str(r['g12']):>8}%  5y:{str(r['g5']):>8}%  "
              f"now:{str(r['current']):>4}  {r['verdict']}")
    if res:
        print("\n=========== TREND SUMMARY (most rising first) ===========")
        order = {"BREAKOUT - rising fast, near peak now": 0, "RISING": 1,
                 "FLAT": 2, "COOLING": 3, "DECLINING": 4, "NO DATA": 9}
        res.sort(key=lambda r: (order.get(r['verdict'], 9), -(r['g12'] or -999)))
        print(f"{'keyword':40} {'12m %':>9} {'5y %':>9}  verdict")
        for r in res:
            print(f"{r['kw'][:40]:40} {str(r['g12']):>9} {str(r['g5']):>9}  {r['verdict']}")
    if out_path and res:
        json.dump(res, open(out_path, "w"), indent=2)
        print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
