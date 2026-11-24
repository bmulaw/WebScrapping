"""The real program (internet needed). Change the settings below, then click Run ▶.

A. Chrome opens ONE real product page: price, sizes, a section, and the network calls behind them.
B. requests calls the same two APIs for MANY products, without a browser. -> output/stock_report.csv
"""
import csv
from pathlib import Path

import exercises
from exercises import PRODUCT

OUTPUT = Path(__file__).resolve().parent / "output"


# ----- Settings: change them, then click Run ▶ -----
HEADLESS = True          # False: watch Chrome open the page and click the section
SECTION = "Product Description"
HOW_MANY = 5             # products in the report (the safety limit is MAX_PRODUCTS in exercises.py)



# ==============================================================================
# A. THE BROWSER: one product page
# ==============================================================================

driver = exercises.make_driver(headless=HEADLESS)
try:

    # ---- open the product page ----
    driver.get(exercises.product_url(PRODUCT))
    print("A1. Page:", driver.title)


    # ---- wait for the price (it arrives after the page) ----
    print("A2. Price: ₹", exercises.wait_for_price(driver))


    # ---- read the size buttons: sold out? only a few left? ----
    page_sizes = exercises.read_sizes(driver)
    print("A3. Sizes on the page:")
    for size in page_sizes:
        status = "sold out" if not size["available"] else (f"only {size['left']} left" if size["left"] else "in stock")
        print(f"      {size['size']:5} {status}")


    # ---- click a closed section and read it ----
    text = exercises.open_section(driver, SECTION)
    print(f"A4. {SECTION}: {text[:150]} ...")


    # ---- CDP: which calls brought the price and the sizes? ----
    events = exercises.network_events(driver.get_log("performance"))
    calls = exercises.find_api_calls(events, f"/product/{PRODUCT}/")
    print("A5. The page called:")
    for call in calls:
        print(f"      {call['status']} {call['method']} {call['url']}")


    # ---- read the inventory answer from Chrome, compare it with the page ----
    inventory_call = next(call for call in calls if call["url"].endswith("/inventory"))
    api_sizes = exercises.sizes_from_inventory(exercises.response_json(driver, inventory_call["request_id"]))
    print("A6. Page vs API:", exercises.compare_sizes(page_sizes, api_sizes))

finally:
    # ---- always close Chrome ----
    driver.quit()



# ==============================================================================
# B. BACK TO requests: the same two APIs, for many products
# ==============================================================================

session = exercises.make_session()


# ---- the slugs of the first t-shirts (the listing API of the lesson) ----
slugs = exercises.listing_slugs(session, min(HOW_MANY, exercises.MAX_PRODUCTS))
print(f"\nB1. {len(slugs)} products:", slugs)


# ---- pricing + inventory for each one (a pause between calls) ----
rows = exercises.product_report(session, slugs)
print("B2. Stock report:")
for row in rows:
    print(f"      ₹{row['price']:<5} (-{row['discount_pct']}%)  sold out: {row['sold_out'] or '-':10} "
          f"few left: {row['few_left'] or '-':10} {row['slug']}")


# ---- save the report ----
OUTPUT.mkdir(exist_ok=True)
with open(OUTPUT / "stock_report.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f"\n-> {OUTPUT / 'stock_report.csv'}")
