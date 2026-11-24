"""Check your exercises, without the internet: click Run ▶

Your functions get a FakeSession: it answers with the files in samples/ and remembers your requests.
"""
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR.parent))

from bs4 import BeautifulSoup  # noqa: E402

from _check_tools import FakeResponse, FakeSession, check, summary  # noqa: E402
import exercises  # noqa: E402
from exercises import CATEGORY_URL, SITE  # noqa: E402

SAMPLES = PROJECT_DIR / "samples"
ROBOTS = (SAMPLES / "robots.txt").read_text(encoding="utf-8")
PAGE1 = (SAMPLES / "listing_page1.html").read_text(encoding="utf-8")
PAGE2 = (SAMPLES / "listing_page2.html").read_text(encoding="utf-8")
PRODUCTS = {path.stem.split("_")[1]: path.read_text(encoding="utf-8") for path in SAMPLES.glob("product_*.html")}
RX9060 = PRODUCTS["PB00686694"]
RX9060_URL = f"{SITE}/fiche/PB00686694.html"


def answer(method, url, params, kwargs):
    """The fake LDLC: 2 listing pages, 3 real product pages (any other product -> the RX 9060 XT page)."""
    if url == CATEGORY_URL:
        return FakeResponse(200, text=PAGE1)
    if url == CATEGORY_URL + "page2/":
        return FakeResponse(200, text=PAGE2)
    if "/fiche/" in url:
        return FakeResponse(200, text=PRODUCTS.get(url.rsplit("/", 1)[-1].removesuffix(".html"), RX9060))
    return FakeResponse(404, text="<h1>Page introuvable</h1>")


def fake():
    return FakeSession(answer)


print("ROBOTS.TXT (samples/robots.txt)")
check(1, "a plain prefix", lambda: exercises.rule_matches("/v4/", "/v4/fr-fr/header/user"), True)
check(1, "not a prefix", lambda: exercises.rule_matches("/recherche/", "/informatique/"), False)
check(1, "* = any characters", lambda: exercises.rule_matches("*/stocks/", "/fiche/PB1/stocks/"), True)
check(1, "$ = the end", lambda: (exercises.rule_matches("/*.pdf$", "/doc/cgv.pdf"),
                                 exercises.rule_matches("/*.pdf$", "/doc/cgv.pdf?x=1")), (True, False))
check(1, "a dot is not 'any character'", lambda: exercises.rule_matches("/a.b", "/axb"), False)
check(1, "empty rule", lambda: exercises.rule_matches("", "/anything"), False)

check(2, "a product page", lambda: exercises.allowed(ROBOTS, RX9060_URL), True)
check(2, "listing page 2", lambda: exercises.allowed(ROBOTS, CATEGORY_URL + "page2/"), True)
check(2, "the JSON calls of the page (Disallow: /v4/ and /mb)",
      lambda: (exercises.allowed(ROBOTS, f"{SITE}/v4/fr-fr/prices"), exercises.allowed(ROBOTS, f"{SITE}/mb?zone=x")),
      (False, False))
check(2, "a wildcard rule: */stocks/", lambda: exercises.allowed(ROBOTS, f"{SITE}/fiche/PB1/stocks/"), False)
check(2, "the longest rule wins", lambda: (exercises.allowed("User-agent: *\nDisallow: /a\nAllow: /a/b", "https://x/a/b/c"),
                                           exercises.allowed("User-agent: *\nDisallow: /a\nAllow: /a/b", "https://x/a/c")),
      (True, False))
check(2, "rules for another robot do not count",
      lambda: exercises.allowed("User-agent: AhrefsBot\nDisallow: /\n\nUser-agent: *\nDisallow: /cart/", "https://x/p"), True)

print("\nLISTING (samples/listing_page1.html)")
check(3, "star-10", lambda: exercises.rating_from_class("star-10"), 5.0)
check(3, "star-9", lambda: exercises.rating_from_class("star-9"), 4.5)
check(3, "not a star", lambda: (exercises.rating_from_class("big"), exercises.rating_from_class(None)), (None, None))
check(4, "5 avis", lambda: exercises.count_from_text("5 avis"), 5)
check(4, "a narrow non-breaking space", lambda: exercises.count_from_text("1 234 avis"), 1234)
check(4, "nothing", lambda: exercises.count_from_text(""), 0)

check(5, "48 cards", lambda: len(exercises.listing_items(PAGE1)), 48)
check(5, "the first card", lambda: exercises.listing_items(PAGE1)[0],
      {"id": "AR202505270061", "name": "ASRock AMD Radeon RX 9060 XT Challenger 16GB OC", "url": RX9060_URL,
       "description": "16 Go GDDR6 - HDMI/Dual-DisplayPort - PCI Express (AMD Radeon RX 9060 XT)",
       "rating": 5.0, "reviews": 5})
check(5, "4.5 stars", lambda: exercises.listing_items(PAGE1)[5]["rating"], 4.5)
check(5, "a card without reviews", lambda: [(i["rating"], i["reviews"]) for i in exercises.listing_items(PAGE1)
                                             if i["id"] == "AR202611160002"], [(None, 0)])
check(5, "absolute urls", lambda: all(i["url"].startswith(SITE + "/fiche/") for i in exercises.listing_items(PAGE1)), True)

FOUR_PAGES = [CATEGORY_URL, CATEGORY_URL + "page2/", CATEGORY_URL + "page3/", CATEGORY_URL + "page4/"]
check(6, "4 pages, from page 1", lambda: exercises.page_urls(PAGE1), FOUR_PAGES)
check(6, "the same 4 pages, from page 2", lambda: exercises.page_urls(PAGE2), FOUR_PAGES)
check(6, "no pagination", lambda: exercises.page_urls("<p>no pagination</p>"), [CATEGORY_URL])
LAST_PAGE = ('<ul class="pagination"><li><a data-page="1" href="/x/">1</a></li><li><a data-page="3" href="/x/page3/">3'
             '</a></li><li class="active"><span>4 <span class="visually-hidden">(current)</span></span></li></ul>')
check(6, "on the LAST page, the current page counts", lambda: len(exercises.page_urls(LAST_PAGE)), 4)

check(7, "48 prices, without opening a product page", lambda: len(exercises.listing_prices(PAGE1)), 48)
check(7, "the RX 9060 XT", lambda: exercises.listing_prices(PAGE1)[RX9060_URL], 969.95)
CARD_URLS = [SITE + a["href"] for a in BeautifulSoup(PAGE1, "lxml").select("li.pdt-item h3 a")]   # not your exercise 5
check(7, "the same urls as the cards, in order", lambda: list(exercises.listing_prices(PAGE1)) == CARD_URLS, True)
check(7, "no ItemList", lambda: exercises.listing_prices(RX9060), {})

print("\nPRODUCT PAGE (samples/product_*.html)")
check(8, "969€ 95", lambda: exercises.parse_price("969€ 95"), 969.95)
check(8, "a non-breaking space", lambda: exercises.parse_price("1\xa0129€95"), 1129.95)
check(8, "the usual French format", lambda: exercises.parse_price("1 329,95 €"), 1329.95)
check(8, "no cents / nothing", lambda: (exercises.parse_price("969€"), exercises.parse_price("")), (969.0, None))
check(9, "the product price (not a similar product)", lambda: exercises.main_price(RX9060), 969.95)
check(9, "a price over 1000 €", lambda: exercises.main_price(PRODUCTS["PB00715126"]), 1329.95)

check(10, "9 sections", lambda: list(exercises.spec_table(RX9060)),
      ["Informations générales", "Chipset graphique", "Mémoire", "Architecture", "Spécifications techniques",
       "Affichage", "Connectique", "Design", "Garanties"])
check(10, "spaces cleaned", lambda: exercises.spec_table(RX9060)["Chipset graphique"]["Fréquence boostée"], "3290 MHz")
check(10, "the hidden <label> removed", lambda: exercises.spec_table(RX9060)["Informations générales"]["Marque"], "ASRock")
check(10, "a 1-cell row (rowspan)", lambda: exercises.spec_table(RX9060)["Connectique"]["Sorties vidéo"],
      "2 X DisplayPort Femelle, 1 X HDMI Femelle")

check(11, "JSON-LD", lambda: exercises.jsonld_product(RX9060),
      {"name": "ASRock AMD Radeon RX 9060 XT Challenger 16GB OC", "gtin13": "4711581491205", "brand": "ASRock",
       "price": 969.95, "currency": "EUR", "in_stock": True})
check(11, "no Product block", lambda: exercises.jsonld_product("<html></html>"), None)

check(12, "the record", lambda: exercises.product_record(RX9060, RX9060_URL),
      {"id": "PB00686694", "name": "ASRock AMD Radeon RX 9060 XT Challenger 16GB OC", "brand": "ASRock",
       "chipset": "AMD Radeon RX 9060 XT", "memory_gb": 16, "boost_mhz": 3290, "price": 969.95,
       "price_jsonld": 969.95, "same_price": True, "url": RX9060_URL})
check(12, "an empty page: None everywhere, no KeyError", lambda: exercises.product_record("<html></html>", "x"),
      {"id": None, "name": None, "brand": None, "chipset": None, "memory_gb": None, "boost_mhz": None, "price": None,
       "price_jsonld": None, "same_price": False, "url": "x"})

print("\nCRAWL (a fake LDLC)")
check(13, "a page", lambda: len(exercises.fetch_html(fake(), RX9060_URL, ROBOTS)) > 1000, True)


def refused():
    session = fake()
    try:
        exercises.fetch_html(session, f"{SITE}/v4/fr-fr/prices", ROBOTS)
    except PermissionError:
        return "PermissionError", len(session.calls)
    return "no PermissionError", len(session.calls)


check(13, "Disallow -> PermissionError, and NO request sent", refused, ("PermissionError", 0))


def not_found():
    try:
        exercises.fetch_html(fake(), f"{SITE}/informatique/nothing/", ROBOTS)
    except NotImplementedError:
        raise
    except Exception as error:
        return type(error).__name__
    return "no error"


check(13, "404 -> HTTPError", not_found, "HTTPError")


def timeout_sent():
    session = fake()
    exercises.fetch_html(session, RX9060_URL, ROBOTS)
    return session.calls[0]["kwargs"].get("timeout") is not None


check(13, "a timeout", timeout_sent, True)


def crawled():
    session = fake()
    records = exercises.crawl(session, ROBOTS, max_pages=2, max_products=3, delay=0)
    return [call["url"].removeprefix(SITE) for call in session.calls], [r["id"] for r in records]


check(14, "2 listing pages, then 3 products", crawled,
      (["/informatique/pieces-informatique/carte-graphique-interne/c4684/",
        "/informatique/pieces-informatique/carte-graphique-interne/c4684/page2/",
        "/fiche/PB00686694.html", "/fiche/PB00671036.html", "/fiche/PB00715126.html"],
       ["PB00686694", "PB00671036", "PB00715126"]))


def one_page():
    session = fake()
    exercises.crawl(session, ROBOTS, max_pages=1, max_products=50, delay=0)
    return len(session.calls)


check(14, "max_pages=1: 1 listing page + 48 products", one_page, 49)

print("\nANALYSIS")
# records written here (not with your product_record), so exercise 14 can be done alone
records = [{"name": "A", "chipset": "x", "memory_gb": 16, "price": 969.95},
           {"name": "B", "chipset": "y", "memory_gb": 8, "price": 299.0},
           {"name": "C", "chipset": "z", "memory_gb": None, "price": 100.0},
           {"name": "D", "chipset": "w", "memory_gb": 12, "price": None},
           {"name": "E", "chipset": "v", "memory_gb": 16, "price": 1329.95}]
check(15, "best deal first", lambda: exercises.price_table(records)["name"].tolist(), ["B", "A", "E"])
check(15, "columns and euros per GB", lambda: (list(exercises.price_table(records).columns),
                                               exercises.price_table(records)["eur_per_gb"].tolist()),
      (["name", "chipset", "memory_gb", "price", "eur_per_gb"], [37.38, 60.62, 83.12]))

summary()
