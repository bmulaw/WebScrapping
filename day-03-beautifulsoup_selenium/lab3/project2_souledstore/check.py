"""Check your exercises, without the internet: click Run ▶

Parts A and B start Chrome on a LOCAL COPY of a product page (samples/local_product_page.html + a local API that
answers with the real answers saved in samples/). Parts C and D use the saved files and a FakeSession.
No request reaches the shop.
"""
import json
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR.parent))

from _browser_tools import LocalSite, test_driver, wait_until  # noqa: E402
from _check_tools import FakeResponse, FakeSession, check, load_json, summary  # noqa: E402
import exercises  # noqa: E402
from exercises import PRODUCT_API, USER_AGENT  # noqa: E402

SAMPLES = PROJECT_DIR / "samples"
INKSTONE, DOOM, GOKU = ("solids-inkstone-oversized-polos", "dr-doom-doomsday-men-oversized-t-shirts",
                        "dragon-ball-z-goku-men-oversized-jersey")
NAMES = {INKSTONE: "Solids: Inkstone", DOOM: "Dr. Doom: Doomsday", GOKU: "Dragon Ball Z: Goku"}
ANSWERS = {(slug, what): load_json(SAMPLES / f"{what}_{slug}.json") for slug in NAMES for what in ("pricing", "inventory")}
LOG = load_json(SAMPLES / "performance_log.json")
PAGE = (SAMPLES / "local_product_page.html").read_text(encoding="utf-8")


def local_answer(slug, what):
    def route(body, query):
        time.sleep(0.4)                                 # like a real network: the data does not come instantly
        data = ANSWERS.get((slug, what))
        return (200, data) if data else (404, {"title": "404 Not Found"})
    return route


# ------------------------------------------------------------------ PART A + B: Chrome on the local copy
pages = {f"/product/{slug}": PAGE.replace("__NAME__", name) for slug, name in NAMES.items()}
pages["/product/no-such-product"] = PAGE.replace("__NAME__", "No such product")
routes = {f"GET /api/v2/product/{slug}/{what}": local_answer(slug, what)
          for slug in list(NAMES) + ["no-such-product"] for what in ("pricing", "inventory")}
site = LocalSite(pages=pages, routes=routes)
print("Starting Chrome (headless) on a local copy of the product page ...")
try:
    driver = test_driver()
except Exception as error:
    driver = None
    print(f"  ❌ Chrome could not start: {error!r}\n     Install Google Chrome, then run check.py again.")


def with_driver(function):
    def run():
        if driver is None:
            raise RuntimeError("no Chrome")
        return function()
    return run


def fresh_page(slug=INKSTONE):
    """Open the local page and wait (the check's own wait) until the sizes are drawn."""
    driver.get(site.url(f"/product/{slug}"))
    wait_until(lambda: len(driver.find_elements("css selector", "ul.sizelist > li")) > 0)


print("\nPART A · THE BROWSER")


def your_driver():
    mine = exercises.make_driver(headless=True)
    try:
        mine.get(site.url(f"/product/{INKSTONE}"))
        return (mine.execute_script("return navigator.userAgent"), mine.get_window_size()["width"],
                isinstance(mine.get_log("performance"), list))
    finally:
        mine.quit()


check(1, "User-Agent, window width, network log", your_driver, (USER_AGENT, 1400, True))


def price_now():
    driver.get(site.url(f"/product/{INKSTONE}"))           # NO sleep: your wait must do the waiting
    return exercises.wait_for_price(driver, timeout=10)


check(2, "1499, waited for (no sleep before)", with_driver(price_now), 1499)


def no_price():
    driver.get(site.url("/product/no-such-product"))        # the API answers 404: the price never comes
    start = time.time()
    try:
        exercises.wait_for_price(driver, timeout=2)
    except NotImplementedError:
        raise
    except Exception as error:
        return type(error).__name__, time.time() - start < 6
    return "no exception", True


check(2, "no price -> TimeoutException after the timeout", with_driver(no_price), ("TimeoutException", True))


def sizes_now():
    driver.get(site.url(f"/product/{INKSTONE}"))
    return exercises.read_sizes(driver)


check(3, "8 sizes, in order", with_driver(lambda: [s["size"] for s in sizes_now()]),
      ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"])
check(3, "sold out, few left, hidden stock", with_driver(lambda: [s for s in sizes_now() if s["size"] in ("XXS", "XS", "XXXL")]),
      [{"size": "XXS", "available": False, "left": None}, {"size": "XS", "available": True, "left": 1},
       {"size": "XXXL", "available": True, "left": None}])


def sections():
    fresh_page()
    description = exercises.open_section(driver, "Product Description")
    states = [b.get_attribute("aria-expanded") for b in driver.find_elements("css selector", "button[aria-expanded]")]
    details = exercises.open_section(driver, "Product Details")
    return description[:32], states, "100% Cotton" in details


check(4, "open a closed section, then another one", with_driver(sections),
      ("This polo's got your back (and s", ["false", "true", "false"], True))


def inventory_from_chrome():
    driver.get_log("performance")                       # forget the old events
    fresh_page(DOOM)
    time.sleep(0.5)
    request_id = None                                   # found with the check's own code (not your exercise 6)
    for entry in driver.get_log("performance"):
        message = json.loads(entry["message"])["message"]
        if message["method"] == "Network.requestWillBeSent" and message["params"]["request"]["url"].endswith("/inventory"):
            request_id = message["params"]["requestId"]
    data = exercises.response_json(driver, request_id)
    return len(data["variant"]), data["variant"][0]["attributes"][0]["value"]


print("\nPART B · CHROME DEVTOOLS PROTOCOL (samples/performance_log.json: the real page)")
check(5, "only the Network events", lambda: len(exercises.network_events(
    LOG + [{"message": json.dumps({"message": {"method": "Page.loadEventFired", "params": {}}})}])), len(LOG))
check(5, "the first event", lambda: exercises.network_events(LOG)[0]["method"], "Network.requestWillBeSent")

EVENTS = [json.loads(entry["message"])["message"] for entry in LOG]       # not your exercise 5
check(6, "the 2 calls of the real page", lambda: [(c["method"], c["url"].rsplit("/", 1)[-1], c["status"], c["body"])
                                                  for c in exercises.find_api_calls(EVENTS, f"/product/{INKSTONE}/")],
      [("GET", "pricing", 200, None), ("GET", "inventory", 200, None)])
check(6, "a POST body is read as JSON", lambda: exercises.find_api_calls([
    {"method": "Network.requestWillBeSent", "params": {"requestId": "1", "request": {
        "url": "https://x/api/list", "method": "POST", "postData": "{\"page\": 2}"}}}], "/api/"),
    [{"request_id": "1", "method": "POST", "url": "https://x/api/list", "body": {"page": 2}, "status": None}])
check(7, "the inventory answer, read from Chrome", with_driver(inventory_from_chrome), (8, "XXS"))

if driver is not None:
    driver.quit()
site.close()

print("\nPART C · THE TWO ANSWERS (samples/pricing_*.json, samples/inventory_*.json)")
check(8, "8 sizes", lambda: len(exercises.sizes_from_inventory(ANSWERS[(INKSTONE, "inventory")])), 8)
check(8, "the first two", lambda: exercises.sizes_from_inventory(ANSWERS[(INKSTONE, "inventory")])[:2],
      [{"size": "XXS", "stock": 0, "available": False}, {"size": "XS", "stock": 1, "available": True}])
check(8, "the size attribute is not always first", lambda: exercises.sizes_from_inventory({"variant": [
    {"stock": 3, "attributes": [{"name": "color", "value": "red"}, {"name": "size", "value": "M"}]}]}),
    [{"size": "M", "stock": 3, "available": True}])
check(9, "Inkstone", lambda: exercises.price_row(ANSWERS[(INKSTONE, "pricing")]),
      {"price": 1499, "mrp": 1799, "member_price": 1399, "discount_pct": 17})
check(9, "Dr. Doom", lambda: exercises.price_row(ANSWERS[(DOOM, "pricing")])["discount_pct"], 21)
check(9, "no mrp", lambda: exercises.price_row({"price": 999.0, "exclusive_price": 899.0})["discount_pct"], 0)

print("\nPART D · BACK TO requests (a FakeSession)")
check(10, "pricing URL", lambda: exercises.api_url(INKSTONE, "pricing"), f"{PRODUCT_API}/{INKSTONE}/pricing")


def bad_what():
    try:
        exercises.api_url(INKSTONE, "reviews")
    except ValueError:
        return "ValueError"
    return "no ValueError"


check(10, "anything else -> ValueError", bad_what, "ValueError")


def answer(method, url, params, kwargs):
    """The fake API: the 3 saved products; any other slug -> 404; 'broken' -> 500."""
    slug, what = url.removeprefix(PRODUCT_API + "/").split("/")
    if slug == "broken":
        return FakeResponse(500, text="Internal Server Error")
    data = ANSWERS.get((slug, what))
    return FakeResponse(200, data) if data else FakeResponse(404, {"title": "404 Not Found"})


def fake():
    return FakeSession(answer)


def fetched():
    session = fake()
    data = exercises.fetch_json(session, f"{PRODUCT_API}/{INKSTONE}/pricing")
    return data["price"], session.calls[0]["kwargs"].get("timeout") is not None


check(11, "a JSON answer, with a timeout", fetched, (1499.0, True))
check(11, "404 -> None", lambda: exercises.fetch_json(fake(), f"{PRODUCT_API}/no-such-product/pricing"), None)


def server_error():
    try:
        exercises.fetch_json(fake(), f"{PRODUCT_API}/broken/pricing")
    except NotImplementedError:
        raise
    except Exception as error:
        return type(error).__name__
    return "no error"


check(11, "500 -> HTTPError", server_error, "HTTPError")


def report():
    session = fake()
    rows = exercises.product_report(session, [INKSTONE, "no-such-product", GOKU], delay=0)
    return rows, len(session.calls)


check(12, "Inkstone's row", lambda: report()[0][0],
      {"slug": INKSTONE, "price": 1499, "mrp": 1799, "member_price": 1399, "discount_pct": 17,
       "in_stock": "XS S M L XL XXL XXXL", "sold_out": "XXS", "few_left": "XS"})
check(12, "the unknown product is skipped; 2 calls per product", lambda: ([r["slug"] for r in report()[0]], report()[1]),
      ([INKSTONE, GOKU], 6))

# rows written here (not with your exercises 3 and 8), so exercise 13 can be done alone
page = [{"size": "S", "available": True}, {"size": "M", "available": False}, {"size": "L", "available": True}]
api_same = [{"size": "S", "available": True}, {"size": "M", "available": False}, {"size": "L", "available": True}]
api_diff = [{"size": "S", "available": True}, {"size": "M", "available": True}, {"size": "L", "available": False}]
check(13, "the same", lambda: exercises.compare_sizes(page, api_same),
      {"same": True, "only_page_available": [], "only_api_available": []})
check(13, "different", lambda: exercises.compare_sizes(page, api_diff),
      {"same": False, "only_page_available": ["L"], "only_api_available": ["M"]})

summary()
