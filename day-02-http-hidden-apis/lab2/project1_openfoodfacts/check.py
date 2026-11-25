"""Check your exercises, without the internet: click Run ▶

Your functions get a FakeSession: it answers with the files in samples/ and remembers your requests.
"""
import sys
import tempfile
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR.parent))

from _check_tools import FakeResponse, FakeSession, check, load_json, summary  # noqa: E402
import exercises  # noqa: E402
from exercises import API, SEARCH_A_LICIOUS, STAGING  # noqa: E402

SAMPLES = PROJECT_DIR / "samples"
NUTELLA = load_json(SAMPLES / "product_3017624010701.json")
NOT_FOUND = load_json(SAMPLES / "product_not_found.json")
PAGES = {1: load_json(SAMPLES / "search_breakfast_cereals_page1.json"),
         2: load_json(SAMPLES / "search_breakfast_cereals_page2.json")}
SEARCHALICIOUS = load_json(SAMPLES / "searchalicious_nutella.json")
PAGE_HTML = (SAMPLES / "product_page_3017624010701.html").read_text(encoding="utf-8")


def answer(method, url, params, kwargs):
    """What the fake Open Food Facts server answers."""
    if url == f"{API}/product/3017624010701":
        return FakeResponse(200, NUTELLA)
    if url == f"{API}/product/0000000000000":
        return FakeResponse(200, NOT_FOUND["body"])
    if url == f"{API}/product/1111111111111":
        return FakeResponse(404, {"status": 0, "status_verbose": "product not found"})
    if url == f"{API}/product/5555555555555":
        return FakeResponse(500, text="Internal Server Error")
    if url == f"{API}/search":
        data = dict(PAGES[int(params.get("page", 1))])
        data["count"] = 40          # pretend there are only 40 results: 2 pages of 20
        return FakeResponse(200, data)
    if url == SEARCH_A_LICIOUS:
        return FakeResponse(200, SEARCHALICIOUS)
    if url.endswith(".jpg"):
        return FakeResponse(200, content=bytes(range(256)) * 1000, headers={"Content-Type": "image/jpeg"})
    return FakeResponse(404, text="not in the fake server")


def fake():
    return FakeSession(answer)


print("CLIENT (samples/*.json)")
check(1, "User-Agent header", lambda: exercises.make_session("Test/1.0").headers["User-Agent"], "Test/1.0")
check(1, "Accept header", lambda: exercises.make_session().headers.get("Accept"), "application/json")
check(1, "3 retries", lambda: exercises.make_session().get_adapter("https://x.org").max_retries.total, 3)
check(1, "retry on 429 and 503", lambda: {429, 503} <= set(exercises.make_session().get_adapter("https://x.org")
                                                            .max_retries.status_forcelist), True)

check(2, "Nutella found", lambda: exercises.get_product(fake(), "3017624010701")["product_name"], "Nutella")


def fields_sent():
    session = fake()
    exercises.get_product(session, "3017624010701", fields=["code", "brands"])
    return session.calls[0]["params"].get("fields"), session.calls[0]["kwargs"].get("timeout") is not None


check(2, "fields joined with commas + a timeout", fields_sent, ("code,brands", True))
check(2, "HTTP 200 but status 0 -> None", lambda: exercises.get_product(fake(), "0000000000000"), None)
check(2, "HTTP 404 -> None", lambda: exercises.get_product(fake(), "1111111111111"), None)


def server_error():
    try:
        exercises.get_product(fake(), "5555555555555")
    except NotImplementedError:
        raise
    except Exception:
        return "exception raised"
    return "no exception"


check(2, "HTTP 500 -> exception", server_error, "exception raised")


def search_params():
    session = fake()
    exercises.search_page(session, "breakfast-cereals", "france", page=2, page_size=20)
    params = session.calls[0]["params"]
    return {k: str(params.get(k)) for k in ("categories_tags_en", "countries_tags_en", "page", "page_size", "sort_by")}


check(3, "search parameters", search_params, {"categories_tags_en": "breakfast-cereals", "countries_tags_en": "france",
                                              "page": "2", "page_size": "20", "sort_by": "unique_scans_n"})
check(3, "search answer", lambda: len(exercises.search_page(fake(), "breakfast-cereals", "france")["products"]), 20)

check(4, "7574 results, 20 per page", lambda: exercises.number_of_pages(7574, 20), 379)
check(4, "40 results", lambda: exercises.number_of_pages(40, 20), 2)
check(4, "0 results", lambda: exercises.number_of_pages(0, 20), 0)


def all_pages(max_pages):
    session = fake()
    products = exercises.search_all(session, "breakfast-cereals", "france", max_pages=max_pages, page_size=20, delay=0)
    return len(products), [call["params"].get("page") for call in session.calls]


check(5, "2 pages read, then stop (count = 40)", lambda: all_pages(10), (40, [1, 2]))
check(5, "max_pages=1 is respected", lambda: all_pages(1), (20, [1]))


def download():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "images" / "nutella.jpg"
        session = fake()
        written = exercises.download_image(session, "https://images.openfoodfacts.org/x.jpg", path)
        return written, path.stat().st_size, session.calls[0]["kwargs"].get("stream")


check(6, "image streamed to disk", download, (256000, 256000, True))
check(6, "no url -> 0", lambda: exercises.download_image(fake(), None, Path("nothing.jpg")), 0)

check(7, "5 hits", lambda: len(exercises.full_text_search(fake(), "nutella", 5)), 5)
check(7, "second hit", lambda: exercises.full_text_search(fake(), "nutella", 5)[1],
      {"code": "0098008952506", "name": "Nutella", "brands": "Nutella"})

check(8, "POST to the TEST server", lambda: (exercises.build_edit_request("3017624010701", {"quantity": "400 g"}, "me", "pw")
                                             .method, exercises.build_edit_request("3017624010701", {}, "me", "pw").url),
      ("POST", f"{STAGING}/cgi/product_jqm2.pl"))
check(8, "form body", lambda: exercises.build_edit_request("3017624010701", {"quantity": "400 g"}, "me", "secret").body,
      "code=3017624010701&user_id=me&password=secret&quantity=400+g")
check(8, "Basic auth header", lambda: exercises.build_edit_request("1", {}, "me", "pw").headers["Authorization"],
      "Basic b2ZmOm9mZg==")

print("\nPARSE")
nutella_row = {"code": "3017624010701", "name": "Nutella", "brand": "Ferrero", "nutriscore": "E", "kcal_100g": 539.0,
               "sugars_100g": 56.3, "fat_100g": 30.9, "salt_100g": 0.1075, "proteins_100g": 6.3,
               "image_url": "https://images.openfoodfacts.org/images/products/301/762/401/0701/front_en.100.400.jpg"}
check(9, "Nutella row", lambda: exercises.product_row(NUTELLA["product"]), nutella_row)
check(9, "first brand only", lambda: exercises.product_row(PAGES[1]["products"][0])["brand"], "Quaker")
check(9, "empty product: all None, no KeyError", lambda: set(exercises.product_row({}).values()), {None})
check(9, "nutriscore 'unknown' -> None", lambda: exercises.product_row({"nutriscore_grade": "unknown"})["nutriscore"], None)

check(10, "JSON-LD types", lambda: exercises.jsonld_types(PAGE_HTML), ["WebSite", "Organization"])
check(10, "invalid JSON-LD is skipped", lambda: exercises.jsonld_types(
    '<script type="application/ld+json">{oops</script><script type="application/ld+json">{"@type": "Thing"}</script>'),
    ["Thing"])
check(11, "title from the HTML", lambda: exercises.title_from_html(PAGE_HTML),
      {"name": "Nutella", "brand": "Ferrero", "quantity": "400.0 g"})
check(11, "no <h1>", lambda: exercises.title_from_html("<p>nothing</p>"), {"name": None, "brand": None, "quantity": None})

print("\nANALYSIS")
# the rows are built here (not with your product_row), so exercise 12 can be done before exercise 9
rows = [{"code": p.get("code"), "nutriscore": (p.get("nutriscore_grade") or "").upper() or None,
         "sugars_100g": (p.get("nutriments") or {}).get("sugars_100g")}
        for p in PAGES[1]["products"] + PAGES[2]["products"]]
for row in rows:
    row["nutriscore"] = row["nutriscore"] if row["nutriscore"] in {"A", "B", "C", "D", "E"} else None
check(12, "one line per grade", lambda: list(exercises.sugar_by_grade(rows).index), ["A", "B", "C", "D"])
check(12, "products per grade", lambda: exercises.sugar_by_grade(rows)["products"].tolist(), [15, 9, 12, 4])
check(12, "mean sugars (about 7.3, 16.0, 18.3, 17.05)", lambda: exercises.sugar_by_grade(rows)["mean_sugars"].tolist(),
      lambda got: len(got) == 4 and all(abs(g - e) <= 0.051 for g, e in zip(got, [7.3, 16.0, 18.3, 17.05])))

summary()
