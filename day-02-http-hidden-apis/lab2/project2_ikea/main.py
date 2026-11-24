"""The real program (internet needed). Change the settings below, then click Run ▶.

Writes output/<query>.csv. Answers are cached 60 s in data/cache/ (run it twice: the second run is instant).
"""
import csv
import time
from pathlib import Path

import pandas as pd

import exercises
from exercises import CACHE_DIR, CACHE_SECONDS, DELAY_SECONDS

OUTPUT = Path(__file__).resolve().parent / "output"

# ----- Settings: change them, then click Run ▶ -----
QUERY = "chaise"                 # what you search, e.g. "lampe"
COLOR = None                     # a color name offered by the API, e.g. "noir" (None = all colors)
SORT = None                      # e.g. "PRICE_LOW_TO_HIGH" (see the list printed below; None = IKEA's order)
COMPARE = "us/en/chair"          # market/language/query to compare prices with

session = exercises.make_session()

# 1. the second hidden API: autocomplete
print("1. Autocomplete for", repr(QUERY[:3]), "->", exercises.autocomplete(session, QUERY[:3]))
time.sleep(DELAY_SECONDS)

# 2. a first search, through the cache: what does the API offer?
url = exercises.api_url("search-result-page")
first = exercises.cached_get_json(session, url, exercises.search_params(QUERY), CACHE_DIR, max_age=CACHE_SECONDS)
print(f"\n2. {QUERY!r}: {exercises.total_results(first)} results. Sorts offered: {exercises.sort_ids(first)}")

# 3. everything, with the filter and the sort asked
filters = exercises.filter_param(first, "COLOR", COLOR) if COLOR else None
time.sleep(DELAY_SECONDS)
data = exercises.search_everything(session, QUERY, sort=SORT, filters=filters)
rows = [exercises.product_row(product) for product in exercises.products(data)]
OUTPUT.mkdir(exist_ok=True)
path = OUTPUT / f"{QUERY}.csv"
with open(path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0]) if rows else ["item_no"])
    writer.writeheader()
    writer.writerows(rows)
print(f"\n3. {len(rows)} products (filters={filters}, sort={SORT}) -> {path}")

# 4. analysis
table = pd.DataFrame(rows)
if not table.empty:
    print("\n4. Price by category:")
    print(table.groupby("category")["price"].agg(["count", "median", "min", "max"]).sort_values("count", ascending=False)
          .head(8))
    good = table[(table["rating_count"].fillna(0) >= 20)].sort_values(["rating", "price"], ascending=[False, True])
    print("\n   Best rated (20 reviews or more), cheapest first:")
    print(good[["name", "type", "price", "rating", "rating_count"]].head(5).to_string(index=False))

# 5. the same products in another country
market, language, query = COMPARE.split("/")
time.sleep(DELAY_SECONDS)
other = exercises.search(session, query, market, language, size=100)
common = exercises.compare_markets(rows, [exercises.product_row(p) for p in exercises.products(other)])
print(f"\n5. In both France and {market.upper()} ({len(common)} products):")
for item in common[:10]:
    print(f"   {item['name']:<12} {item['item_no']}  {item['price_a']:>8} {item['currency_a']}  "
          f"{item['price_b']:>8} {item['currency_b']}")
