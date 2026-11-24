"""BONUS: the catalogue API of every Shopify shop: https://<shop>/products.json

Thousands of shops run on Shopify (Percko, Le Slip Français ...). They all have the same undocumented endpoint:
    /products.json?limit=250&page=1   -> {"products": [ ... up to 250 products with their variants ... ]}
One program, many shops. But: Shopify limits requests per IP address ACROSS ALL its shops (429 + Retry-After).
"""
import time

import requests

USER_AGENT = "Mozilla/5.0 (compatible; ESILV-Lab-Advanced/1.0; educational use)"
TIMEOUT = 20
DELAY_SECONDS = 3


def make_session():
    """(Given.)"""
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def fetch_page(session, shop, page, limit=250):
    """One page of the catalogue -> the list of products ([] when there are no more).

    GET https://<shop>/products.json?limit=<limit>&page=<page>
    Two ways to say "no more products":
      - status 200 with {"products": []}
      - status 400 with {"errors": "Page * Limit exceeds the 25000 limit."}   (very far pages)
    -> both: return []. Any other error: raise an exception.
    """
    # ----- Exercise 1: fetch_page -----
    raise NotImplementedError("Exercise 1 (fetch_page): not done yet")


def all_products(session, shop, limit=250, max_pages=10, delay=DELAY_SECONDS):
    """Page 1, 2, 3 ... until a page is empty (or max_pages). Wait `delay` seconds between pages.

    There is no "count" here: you only know you are done when a page comes back EMPTY.
    """
    # ----- Exercise 2: all_products -----
    raise NotImplementedError("Exercise 2 (all_products): not done yet")


def variant_rows(products):
    """One row per VARIANT (a size, a color ...): a product has 1 or many variants, each with its own price.

        {"product": product["title"].strip(), "variant": variant["title"], "sku": variant["sku"],
         "price": float(variant["price"]),
         "compare_at": float(variant["compare_at_price"]) or None when it is missing or empty,
         "discount_pct": round(100 * (compare_at - price) / compare_at, 1) when compare_at > price, else 0.0,
         "available": variant["available"]}

    "compare_at_price" is the old price (crossed out on the page): when it is higher, the variant is on sale.
    Careful: some titles start with an invisible character ("\\u200d"): strip() does not remove it, remove it yourself.
    """
    # ----- Exercise 3: variant_rows -----
    raise NotImplementedError("Exercise 3 (variant_rows): not done yet")


def promotions(rows, min_discount=20.0):
    """The rows that are available AND at least min_discount % off, the biggest discount first
    (same discount: the cheapest first). Free gifts (price 0) are not promotions: skip them."""
    # ----- Exercise 4: promotions -----
    raise NotImplementedError("Exercise 4 (promotions): not done yet")
