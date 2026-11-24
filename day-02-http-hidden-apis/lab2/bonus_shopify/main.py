"""The real program (internet needed). Change the settings below, then click Run ▶.

The shops checked for this lab (robots.txt allows /products.json, no "no robots" clause in their terms):
    www.percko.com   www.leslipfrancais.fr
Before you use ANOTHER Shopify shop: read its robots.txt AND its terms of service (many forbid robots).
"""
import csv
from pathlib import Path

import pandas as pd

import exercises

OUTPUT = Path(__file__).resolve().parent / "output"

# ----- Settings: change them, then click Run ▶ -----
SHOP = "www.percko.com"          # or "www.leslipfrancais.fr" (the only two shops checked for this lab)
MAX_PAGES = 4                    # at most this many pages of products

CHECKED_SHOPS = ["www.percko.com", "www.leslipfrancais.fr"]
if SHOP not in CHECKED_SHOPS:
    raise SystemExit(f"{SHOP} was not checked: read its robots.txt AND its terms first (see the top of this file).")

session = exercises.make_session()
products = exercises.all_products(session, SHOP, max_pages=MAX_PAGES)
rows = exercises.variant_rows(products)
print(f"{SHOP}: {len(products)} products, {len(rows)} variants")

if rows:
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / f"{SHOP}.csv"
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    table = pd.DataFrame(rows)
    print(f"-> {path}\n\nAvailable: {table['available'].mean():.0%} of the variants. Price: median {table['price'].median()}")
    print("\nBest promotions:")
    for row in exercises.promotions(rows)[:10]:
        print(f"  -{row['discount_pct']:>5}%  {row['price']:>7} (was {row['compare_at']})  {row['product']} / {row['variant']}")
