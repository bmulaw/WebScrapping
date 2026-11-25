"""The real program (internet needed). Change the settings below, then click Run ▶.

robots.txt -> sitemap index -> category sitemap -> product pages -> JSON-LD -> output/<category>.csv
"""
import csv
import time
from pathlib import Path

import pandas as pd
import requests

import exercises
from exercises import DELAY_SECONDS, MAX_PRODUCTS, ROBOTS_URL, TIMEOUT, USER_AGENT

OUTPUT = Path(__file__).resolve().parent / "output"

# ----- Settings: change them, then click Run ▶ -----
CATEGORY = "mobiele-telefoons"   # a word of the sitemap file name (Dutch!), e.g. "laptops"
LIMIT = 10                       # how many products to download

limit = min(LIMIT, MAX_PRODUCTS)

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})


def get(url):
    """GET with a timeout, an error for a bad status, and a pause after (be polite)."""
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    time.sleep(DELAY_SECONDS)
    return response


# 1. robots.txt: the rules AND the list of sitemaps
robots = get(ROBOTS_URL).text
index_url = next(url for url in exercises.sitemaps_from_robots(robots) if "/en/products" in url)
print("1. robots.txt -> English product index:", index_url)

# 2. the index -> the sitemap of one category
kind, category_urls = exercises.parse_sitemap(get(index_url).text)
matches = exercises.category_sitemaps(category_urls, CATEGORY)
print(f"2. {kind}: {len(category_urls)} category sitemaps; matching {CATEGORY!r}:")
for url in matches:
    print("     ", url)
chosen = next((url for url in matches if url.rsplit("/", 1)[-1].split("_", 1)[-1] == f"{CATEGORY}.xml"), matches[0])

# 3. the category sitemap -> product URLs
kind, product_urls = exercises.parse_sitemap(get(chosen).text)
print(f"3. {chosen.rsplit('/', 1)[-1]}: {len(product_urls)} products. Reading the first {limit} ...")

# 4. each product page -> JSON-LD -> one record
records = []
for url in product_urls[:limit]:
    if not exercises.allowed(robots, url, USER_AGENT):
        print("   robots.txt says no:", url)
        continue
    blocks = exercises.jsonld_blocks(get(url).text)
    product = exercises.find_product(blocks)
    if product is None:
        print("   no Product JSON-LD:", url)
        continue
    record = exercises.product_record(product, url)
    record["category"] = " > ".join(exercises.breadcrumb(blocks)[:3])
    records.append(record)
    print(f"   {record['price']:>8} {record['currency']}  {'in stock ' if record['in_stock'] else 'sold out '} {record['name']}")

if records:
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / f"{CATEGORY}.csv"
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"\n4. {len(records)} products -> {path}")
    table = pd.DataFrame(records)
    print("\n5. By brand:")
    print(table.groupby("brand").agg(products=("sku", "size"), mean_price=("price", "mean"),
                                     in_stock=("in_stock", "mean")).round(2))
    print("\n6. The trap: the shop's own ratings on the last page (NOT the product):", exercises.shop_ratings(blocks))
