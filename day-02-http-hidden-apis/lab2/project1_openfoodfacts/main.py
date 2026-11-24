"""The real program (internet needed). Change the settings below, then click Run ▶.

Writes output/products.csv and output/images/. Change the settings at the top of exercises.py (put YOUR e-mail in USER_AGENT).
"""
import csv
from pathlib import Path

import exercises

OUTPUT = Path(__file__).resolve().parent / "output"

# ----- Settings: change them, then click Run ▶ -----
CATEGORY = "breakfast-cereals"   # try "chocolate-spreads" (list: https://world.openfoodfacts.org/categories)
COUNTRY = "france"
PAGES = 3                        # at most this many pages of 20 products
IMAGES = 0                       # download the image of the first N products

session = exercises.make_session()
print(f"User-Agent: {session.headers['User-Agent']}\n")

# 1. one product by barcode
nutella = exercises.get_product(session, "3017624010701")
print("1. Barcode 3017624010701 ->", exercises.product_row(nutella) if nutella else "not found")
print("   Barcode 0000000000000 ->", exercises.get_product(session, "0000000000000"))

# 2. search, all pages (with a pause between pages)
print(f"\n2. Search: {CATEGORY} in {COUNTRY}, at most {PAGES} pages ...")
products = exercises.search_all(session, CATEGORY, COUNTRY, max_pages=PAGES)
rows = [exercises.product_row(product) for product in products]
OUTPUT.mkdir(exist_ok=True)
with open(OUTPUT / "products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0]) if rows else ["code"])
    writer.writeheader()
    writer.writerows(rows)
print(f"   {len(rows)} products -> {OUTPUT / 'products.csv'}")

# 3. analysis
print("\n3. Sugar by Nutri-Score grade:")
print(exercises.sugar_by_grade(rows) if rows else "   no data")

# 4. images (streamed)
for row in rows[:IMAGES]:
    size = exercises.download_image(session, row["image_url"], OUTPUT / "images" / f"{row['code']}.jpg")
    print(f"   image {row['code']}: {size} bytes")

# 5. the other search API
print("\n5. Full-text search 'nutella' (search-a-licious):")
for hit in exercises.full_text_search(session, "nutella", 5):
    print("  ", hit)

# 6. API or HTML? The same product, from the HTML page
page = session.get("https://world.openfoodfacts.org/product/3017624010701", timeout=20)
print("\n6. HTML page: JSON-LD types =", exercises.jsonld_types(page.text), "| <h1> =", exercises.title_from_html(page.text))

# 7. a POST, prepared but NOT sent
request = exercises.build_edit_request("3017624010701", {"quantity": "400 g"}, "your-test-account", "your-password")
print(f"\n7. Prepared (not sent): {request.method} {request.url}\n   body: {request.body}")
print("   To send it to the TEST server: session.send(request). Never on world.openfoodfacts.org!")
