#!/usr/bin/env python3
"""
Amazon saturation checker.

Saturation is measured from REVIEW DENSITY of organic listings, not result count.
A category with 2,000 results but median 30 reviews is more enterable than one
with 100 results and median 5,000.

Usage:
    python3 amzsat.py "keyword one" "keyword two" ...
    python3 amzsat.py --json out.json "keyword" ...

Requires: curl, beautifulsoup4, lxml.
"""
import sys, re, json, time, urllib.parse, subprocess, statistics

from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def fetch(kw, tries=3):
    url = "https://www.amazon.com/s?k=" + urllib.parse.quote_plus(kw)
    for attempt in range(tries):
        p = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA,
             "-H", "Accept-Language: en-US,en;q=0.9",
             "-H", "Accept: text/html,application/xhtml+xml",
             "--max-time", "70", url],
            capture_output=True)
        html = p.stdout.decode("utf-8", "ignore")
        if len(html) > 50000 and "Enter the characters" not in html:
            return html
        time.sleep(5 * (attempt + 1))
    return None


def money(s):
    if not s:
        return None
    m = re.search(r'([\d,]+\.?\d*)', s)
    return float(m.group(1).replace(',', '')) if m else None


def parse(html):
    soup = BeautifulSoup(html, "lxml")
    m = re.search(r'([0-9,]+)\s*(?:\+)?\s*results', html)
    total = m.group(1) if m else "?"
    rows = []
    for d in soup.select('div[data-asin]'):
        asin = d.get('data-asin')
        if not asin:
            continue
        t = d.select_one('h2')
        title = t.get_text(" ", strip=True) if t else None
        if not title:
            continue
        sponsored = bool(re.search(r'Sponsored', d.get_text(" ", strip=True)[:200]))
        rv = None
        for a in d.select('a[aria-label], span[aria-label]'):
            mm = re.match(r'^([\d,]+)\s+ratings?$', a.get('aria-label', '').strip())
            if mm:
                rv = int(mm.group(1).replace(',', ''))
                break
        po = d.select_one('span.a-price > span.a-offscreen')
        rows.append(dict(asin=asin, title=title[:80], sponsored=sponsored,
                         reviews=rv, price=money(po.get_text(strip=True) if po else None)))
    return total, rows


def verdict(median, frac_big, price_floor):
    """Composite read on enterability."""
    if median is None:
        return "NO DATA"
    if median > 800 or frac_big > 0.4:
        return "CLOSED - entrenched incumbents"
    if price_floor is not None and price_floor < 12 and median > 200:
        return "CLOSED - price war"
    if median > 250:
        return "CROWDED"
    if median > 100:
        return "CONTESTED"
    if price_floor is not None and price_floor < 12:
        return "OPEN but low-ticket"
    return "OPEN"


def report(kw, verbose=True):
    html = fetch(kw)
    if html is None:
        print(f"\n### {kw}\n  BLOCKED after retries")
        return None
    total, rows = parse(html)
    organic = [r for r in rows if not r['sponsored']]
    revs = [r['reviews'] for r in organic if r['reviews'] is not None]
    prices = sorted(p for p in (r['price'] for r in organic) if p)
    if not revs:
        print(f"\n### {kw}\n  no review data parsed")
        return None
    med = int(statistics.median(revs))
    frac_big = sum(1 for r in revs if r > 1000) / len(revs)
    floor = prices[0] if prices else None
    v = verdict(med, frac_big, floor)
    rec = dict(kw=kw, total=total, organic=len(organic), median=med,
               max=max(revs), big=sum(1 for r in revs if r > 1000),
               n=len(revs), price_lo=floor, price_hi=prices[-1] if prices else None,
               verdict=v)
    if verbose:
        print(f"\n### {kw}")
        print(f"  results: {total} | organic: {len(organic)} | median rev: {med} | "
              f"max: {max(revs)} | >1k: {rec['big']}/{rec['n']} | "
              f"price: ${floor}-${rec['price_hi']}")
        print(f"  --> {v}")
        for r in sorted(organic, key=lambda x: (x['reviews'] or 0))[:3]:
            print(f"     [{r['reviews']}rev ${r['price']}] {r['title']}")
    return rec


def main():
    args = sys.argv[1:]
    out = None
    if args and args[0] == "--json":
        out = args[1]
        args = args[2:]
    results = []
    for kw in args:
        r = report(kw)
        if r:
            results.append(r)
        time.sleep(4)
    if results:
        print("\n\n=========== SUMMARY (most open first) ===========")
        order = {"OPEN": 0, "OPEN but low-ticket": 1, "CONTESTED": 2,
                 "CROWDED": 3, "CLOSED - price war": 4,
                 "CLOSED - entrenched incumbents": 5}
        results.sort(key=lambda r: (order.get(r['verdict'], 9), r['median']))
        print(f"{'keyword':44} {'res':>7} {'med':>6} {'>1k':>7} {'price':>14}  verdict")
        for r in results:
            pr = f"${r['price_lo']:.0f}-{r['price_hi']:.0f}" if r['price_lo'] else "-"
            print(f"{r['kw'][:44]:44} {r['total']:>7} {r['median']:>6} "
                  f"{str(r['big'])+'/'+str(r['n']):>7} {pr:>14}  {r['verdict']}")
    if out and results:
        json.dump(results, open(out, "w"), indent=2)
        print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
