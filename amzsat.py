import sys, re, json, time, urllib.parse, subprocess, statistics
sys.path.insert(0, '/root/.agent-reach-venv/lib/python3.11/site-packages')
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

def fetch(kw):
    url = "https://www.amazon.com/s?k=" + urllib.parse.quote_plus(kw)
    p = subprocess.run(["curl","-sL","--compressed","-A",UA,
                        "-H","Accept-Language: en-US,en;q=0.9",
                        "-H","Accept: text/html,application/xhtml+xml",
                        "--max-time","70", url],
                       capture_output=True)
    return p.stdout.decode("utf-8","ignore")

def parse(html):
    soup = BeautifulSoup(html, "lxml")
    m = re.search(r'([0-9,]+)\s*(?:\+)?\s*results', html)
    total = m.group(1) if m else "?"
    rows = []
    for d in soup.select('div[data-asin]'):
        asin = d.get('data-asin')
        if not asin: continue
        t = d.select_one('h2')
        title = t.get_text(" ", strip=True) if t else None
        if not title: continue
        sponsored = bool(re.search(r'Sponsored', d.get_text(" ", strip=True)[:200]))
        # review count
        rv = None
        for a in d.select('a[aria-label], span[aria-label]'):
            lab = a.get('aria-label','')
            mm = re.match(r'^([\d,]+)\s+ratings?$', lab.strip())
            if mm: rv = int(mm.group(1).replace(',','')); break
        if rv is None:
            mm = re.search(r'>\(?([\d,]{2,})\)?<', str(d.select_one('span.a-size-base.s-underline-text') or ''))
            if mm:
                try: rv = int(mm.group(1).replace(',',''))
                except: pass
        price = None
        po = d.select_one('span.a-price > span.a-offscreen')
        if po: price = po.get_text(strip=True)
        rows.append(dict(asin=asin, title=title[:90], sponsored=sponsored, reviews=rv, price=price))
    return total, rows

def report(kw):
    html = fetch(kw)
    if 'Enter the characters' in html or len(html) < 50000:
        print(f"\n### {kw}\n  BLOCKED/short ({len(html)} chars)"); return
    total, rows = parse(html)
    organic = [r for r in rows if not r['sponsored']]
    revs = [r['reviews'] for r in organic if r['reviews'] is not None]
    print(f"\n### {kw}")
    print(f"  reported results: {total}   listings on p1: {len(rows)}   organic: {len(organic)}   sponsored: {len(rows)-len(organic)}")
    if revs:
        revs_sorted = sorted(revs, reverse=True)
        print(f"  review counts (organic, top10): {revs_sorted[:10]}")
        print(f"  median reviews: {int(statistics.median(revs))}   max: {max(revs)}   #with>1000 reviews: {sum(1 for r in revs if r>1000)}")
    else:
        print("  review counts: not parsed")
    for r in organic[:6]:
        print(f"    - [{r['reviews']}rev {r['price']}] {r['title']}")

for kw in sys.argv[1:]:
    report(kw)
    time.sleep(3)
