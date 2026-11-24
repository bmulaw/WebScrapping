"""Check your exercises, without the internet: click Run ▶"""
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR.parent))

import exercises  # noqa: E402
from _check_tools import FakeResponse, FakeSession, check, load_json, summary  # noqa: E402

SAMPLES = PROJECT_DIR / "samples"
PAGE1 = load_json(SAMPLES / "leslipfrancais_page1.json")
TOO_FAR = load_json(SAMPLES / "leslipfrancais_empty_page.json")


def answer(method, url, params, kwargs):
    """A fake shop with 30 products, served 30 per page (whatever the limit) ... like a tiny catalogue."""
    page, limit = int(params["page"]), int(params["limit"])
    if page * limit > 25000:
        return FakeResponse(400, TOO_FAR)
    products = PAGE1["products"]
    start = (page - 1) * limit
    return FakeResponse(200, {"products": products[start:start + limit]})


def fake():
    return FakeSession(answer)


print("API")
check(1, "page 1: 30 products", lambda: len(exercises.fetch_page(fake(), "www.leslipfrancais.fr", 1, 250)), 30)


def url_and_params():
    session = fake()
    exercises.fetch_page(session, "www.leslipfrancais.fr", 2, 10)
    call = session.calls[0]
    return call["url"], {k: int(v) for k, v in call["params"].items()}, call["kwargs"].get("timeout") is not None


check(1, "url, params, timeout", url_and_params, ("https://www.leslipfrancais.fr/products.json", {"limit": 10, "page": 2}, True))
check(1, "an empty page -> []", lambda: exercises.fetch_page(fake(), "x", 5, 10), [])
check(1, "400 'exceeds the 25000 limit' -> []", lambda: exercises.fetch_page(fake(), "x", 9999, 250), [])


def pages_read(limit):
    session = fake()
    products = exercises.all_products(session, "x", limit=limit, delay=0)
    return len(products), [int(call["params"]["page"]) for call in session.calls]


check(2, "limit 10: 3 full pages, then an empty one", lambda: pages_read(10), (30, [1, 2, 3, 4]))
check(2, "limit 250: one short page is enough", lambda: pages_read(250), (30, [1]))

print("\nVARIANTS")
# rows built here (not with your variant_rows), so exercise 4 can be done alone
rows = []
for product in PAGE1["products"]:
    for v in product["variants"]:
        old = float(v["compare_at_price"]) if v.get("compare_at_price") else None
        price = float(v["price"])
        rows.append({"product": product["title"], "price": price, "available": v["available"],
                     "discount_pct": round(100 * (old - price) / old, 1) if old and old > price else 0.0})
check(3, "131 variants", lambda: len(exercises.variant_rows(PAGE1["products"])), 131)
check(3, "a pack on sale", lambda: exercises.variant_rows(PAGE1["products"])[5],
      {"product": "Lot de 3 paires de socquettes surprise ! - Coloris surprise", "variant": "39/42", "sku": "3666078296720",
       "price": 19.9, "compare_at": 29.7, "discount_pct": 33.0, "available": True})
check(3, "invisible character removed", lambda: exercises.variant_rows(PAGE1["products"])[0]["product"],
      "Boxer Gris Offert dès 85€")
check(3, "no compare_at_price", lambda: exercises.variant_rows([{"title": "T", "variants": [
    {"title": "M", "sku": "1", "price": "10.00", "compare_at_price": None, "available": True}]}])[0],
    {"product": "T", "variant": "M", "sku": "1", "price": 10.0, "compare_at": None, "discount_pct": 0.0, "available": True})

check(4, "promotions: no free gift, all >= 20 %", lambda: all(r["price"] > 0 and r["discount_pct"] >= 20 and r["available"]
                                                              for r in exercises.promotions(rows)), True)
check(4, "sorted: biggest discount first", lambda: [r["discount_pct"] for r in exercises.promotions(rows)]
      == sorted([r["discount_pct"] for r in exercises.promotions(rows)], reverse=True), True)
check(4, "how many", lambda: len(exercises.promotions(rows)), lambda n: n > 0)

summary()
