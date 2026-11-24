"""The real program (internet needed). Change the settings below, then click Run ▶.

robots.txt -> listing pages -> product pages -> output/graphics_cards.csv, with a pause between pages.
"""
from pathlib import Path

import exercises
from exercises import CATEGORY_URL, DELAY_SECONDS, ROBOTS_URL, TIMEOUT

OUTPUT = Path(__file__).resolve().parent / "output"


# ----- Settings: change them, then click Run ▶ -----
PAGES = 1                 # listing pages to read (48 cards each; the safety limit is MAX_PAGES in exercises.py)
PRODUCTS = 6              # product pages to read (the safety limit is MAX_PRODUCTS)

PAGES = min(PAGES, exercises.MAX_PAGES)
PRODUCTS = min(PRODUCTS, exercises.MAX_PRODUCTS)
session = exercises.make_session()



# ---- 1. read robots.txt, and test two URLs ----
robots = session.get(ROBOTS_URL, timeout=TIMEOUT).text

for url in (CATEGORY_URL, "https://www.ldlc.com/v4/fr-fr/header/user"):
    print(f"1. robots.txt: {url} -> {'allowed' if exercises.allowed(robots, url) else 'NOT allowed'}")



# ---- 2. the listing page: the cards, and the number of pages ----
listing = exercises.fetch_html(session, CATEGORY_URL, robots)
items = exercises.listing_items(listing)

print(f"\n2. Listing page 1: {len(items)} cards, {len(exercises.page_urls(listing))} pages in total")
for item in items[:3]:
    print("  ", item)



# ---- 3. the prices of the listing (from its JSON-LD, the price boxes are empty) ----
prices = exercises.listing_prices(listing)

print(f"\n3. The price boxes of the cards are EMPTY, but the JSON-LD has {len(prices)} prices:")
for item in items[:3]:
    print(f"   {prices.get(item['url'])} €  {item['name']}")



# ---- 4. the crawl: listing pages, then product pages (a pause between pages) ----
print(f"\n4. Crawl: {PAGES} listing page(s), {PRODUCTS} product pages, {DELAY_SECONDS} s between pages ...")
records = exercises.crawl(session, robots, max_pages=PAGES, max_products=PRODUCTS)

for record in records:
    flag = "" if record["same_price"] else "   <-- HTML and JSON-LD disagree!"
    print(f"   {record['price']:>8} €  {record['memory_gb']} Go  {record['name']}{flag}")



# ---- 5. the best deals: euros per GB of video memory ----
table = exercises.price_table(records)
print("\n5. Euros per GB of video memory:\n", table.to_string(index=False))



# ---- 6. save the table ----
OUTPUT.mkdir(exist_ok=True)
table.to_csv(OUTPUT / "graphics_cards.csv", index=False)
print(f"\n-> {OUTPUT / 'graphics_cards.csv'}")
