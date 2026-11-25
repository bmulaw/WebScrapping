"""Check your exercises, without the internet: click Run ▶

Your functions get a FakeSession: it answers with the files in samples/ and remembers your requests.
"""
import json
import sys
import tempfile
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR.parent))

from _check_tools import FakeResponse, FakeSession, check, load_json, summary  # noqa: E402
import exercises  # noqa: E402

SAMPLES = PROJECT_DIR / "samples"
CHAISE = load_json(SAMPLES / "search_chaise_fr.json")
CHAIR_US = load_json(SAMPLES / "search_chair_us.json")
ERROR = load_json(SAMPLES / "error_offset.json")
SEARCHBOX = load_json(SAMPLES / "searchbox_cha.json")
API = "https://sik.search.blue.cdtapps.com"


def answer(method, url, params, kwargs):
    """What the fake IKEA API answers. Like the real one: unknown parameters -> 400."""
    allowed = {"q", "size", "types", "sort"} | {k for k in params if k.startswith("f-")}
    if url.endswith("/search-result-page"):
        unknown = set(params) - allowed
        if unknown:
            return FakeResponse(400, {**ERROR["body"], "detail": f"Unrecognized parameter: {sorted(unknown)[0]}"})
        data = json.loads(json.dumps(CHAIR_US if "/us/en/" in url else CHAISE))
        main = data["searchResultPage"]["products"]["main"]
        main["items"] = main["items"][:int(params.get("size", 24))]
        main["end"] = len(main["items"])
        return FakeResponse(200, data)
    if url.endswith("/search-box"):
        return FakeResponse(200, SEARCHBOX)
    return FakeResponse(404, text="<html>Not found</html>")


def fake():
    return FakeSession(answer)


print("CLIENT")
check(1, "France", lambda: exercises.api_url("search-result-page"), f"{API}/fr/fr/search-result-page")
check(1, "USA, autocomplete", lambda: exercises.api_url("search-box", "us", "en"), f"{API}/us/en/search-box")

check(2, "simple", lambda: exercises.search_params("chaise"), {"q": "chaise", "size": 24, "types": "PRODUCT"})
check(2, "sort + filter", lambda: exercises.search_params("chaise", 10, sort="PRICE_LOW_TO_HIGH", filters={"f-colors": "10139"}),
      {"q": "chaise", "size": 10, "types": "PRODUCT", "sort": "PRICE_LOW_TO_HIGH", "f-colors": "10139"})

check(3, "the API explains a 400", lambda: exercises.api_error(FakeResponse(400, ERROR["body"])),
      "400 Bad Request: Unrecognized parameter: offset")
check(3, "not an error -> None", lambda: exercises.api_error(FakeResponse(200, {"ok": True})), None)
check(3, "error that is not JSON", lambda: exercises.api_error(FakeResponse(503, text="Service Unavailable")),
      "503 Service Unavailable")

check(4, "24 items", lambda: len(exercises.search(fake(), "chaise")["searchResultPage"]["products"]["main"]["items"]), 24)


def sent():
    session = fake()
    exercises.search(session, "chaise", size=5)
    return session.calls[0]["url"], session.calls[0]["params"], session.calls[0]["kwargs"].get("timeout") is not None


check(4, "url, params and a timeout", sent, (f"{API}/fr/fr/search-result-page", {"q": "chaise", "size": 5, "types": "PRODUCT"}, True))


def bad_parameter():
    try:
        exercises.search(fake(), "chaise", filters={"offset": 24})
    except ValueError as error:
        return str(error)
    return "no ValueError"


check(4, "400 -> ValueError with the API message", bad_parameter, "400 Bad Request: Unrecognized parameter: offset")


def everything():
    session = fake()
    data = exercises.search_everything(session, "chaise", delay=0)
    return [call["params"]["size"] for call in session.calls], len(exercises.products(data))


check(5, "2 calls: size 24 then size 112 (but the sample has only 24)", everything, ([24, 112], 24))


def limited():
    session = fake()
    exercises.search_everything(session, "chaise", max_items=50, delay=0)
    return [call["params"]["size"] for call in session.calls]


check(5, "max_items is respected", limited, [24, 50])

check(6, "suggestions for 'cha'", lambda: exercises.autocomplete(fake(), "cha"),
      ["chaise", "chaise bureau", "chambre", "chaussure", "chaise enfant", "chauffeuse"])

print("\nCACHE")
check(7, "same key in any order", lambda: exercises.cache_key("https://x/s", {"q": "chaise", "size": 24})
      == exercises.cache_key("https://x/s", {"size": 24, "q": "chaise"}), True)
check(7, "16 characters", lambda: len(exercises.cache_key("https://x/s", {})), 16)
check(7, "different params -> different key", lambda: exercises.cache_key("https://x/s", {"q": "a"})
      != exercises.cache_key("https://x/s", {"q": "b"}), True)


def cache_story():
    with tempfile.TemporaryDirectory() as folder:
        session = fake()
        url, params = f"{API}/fr/fr/search-box", {"q": "cha"}
        clock = [time.time()]                            # a clock we control: now, then 61 seconds later
        first = exercises.cached_get_json(session, url, params, folder, max_age=60, now=lambda: clock[0])
        exercises.cached_get_json(session, url, params, folder, max_age=60, now=lambda: clock[0])
        calls_after_two = len(session.calls)
        path = Path(folder) / f"{exercises.cache_key(url, params)}.json"
        clock[0] = path.stat().st_mtime + 61             # 61 seconds later: too old
        exercises.cached_get_json(session, url, params, folder, max_age=60, now=lambda: clock[0])
        return calls_after_two, len(session.calls), "searchBox" in first


check(8, "1 request for 2 calls, a new one after 61 s", cache_story, (1, 2, True))

print("\nPARSE (samples/search_chaise_fr.json)")
check(9, "24 products", lambda: len(exercises.products(CHAISE)), 24)
check(9, "first product", lambda: exercises.products(CHAISE)[0]["name"], "SANDSBERG")
check(9, "empty answer", lambda: exercises.products({}), [])
check(10, "112 results in total", lambda: exercises.total_results(CHAISE), 112)
check(11, "first row", lambda: exercises.product_row(exercises.products(CHAISE)[0]),
      {"item_no": "30605423", "name": "SANDSBERG", "type": "Chaise", "price": 14.99, "currency": "EUR", "rating": 3.8,
       "rating_count": 17, "colors": "noir", "category": "Chaises de table",
       "url": "https://www.ikea.com/fr/fr/p/sandsberg-chaise-noir-30605423/"})
check(11, "empty product: no KeyError", lambda: exercises.product_row({})["category"], None)
check(12, "sorts", lambda: exercises.sort_ids(CHAISE)[:4], ["RELEVANCE", "PRICE_LOW_TO_HIGH", "PRICE_HIGH_TO_LOW", "NEWEST"])
check(13, "filter COLOR noir", lambda: exercises.filter_param(CHAISE, "COLOR", "noir"), {"f-colors": "10139"})


def unknown_filter():
    try:
        exercises.filter_param(CHAISE, "COLOR", "violet fluo")
    except KeyError:
        return "KeyError"
    return "no KeyError"


check(13, "unknown value -> KeyError", unknown_filter, "KeyError")


def simple_rows(data):
    """Rows built here (not with your functions), so exercise 14 can be done alone."""
    return [{"item_no": item["product"]["itemNo"], "name": item["product"]["name"],
             "price": item["product"]["salesPrice"]["numeral"], "currency": item["product"]["salesPrice"]["currencyCode"]}
            for item in data["searchResultPage"]["products"]["main"]["items"]]


fr_rows, us_rows = simple_rows(CHAISE), simple_rows(CHAIR_US)
check(14, "4 products in both countries", lambda: [c["item_no"] for c in exercises.compare_markets(fr_rows, us_rows)],
      ["00457235", "00590480", "30605423", "80349671"])
check(14, "SANDSBERG in France and in the USA", lambda: exercises.compare_markets(fr_rows, us_rows)[2],
      {"item_no": "30605423", "name": "SANDSBERG", "price_a": 14.99, "currency_a": "EUR", "price_b": 15.0,
       "currency_b": "USD"})

summary()
