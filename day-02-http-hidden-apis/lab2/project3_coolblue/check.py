"""Check your exercises, without the internet: click Run ▶"""
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR.parent))

from _check_tools import check, summary  # noqa: E402
import exercises  # noqa: E402
from exercises import USER_AGENT  # noqa: E402

SAMPLES = PROJECT_DIR / "samples"
ROBOTS = (SAMPLES / "robots.txt").read_text(encoding="utf-8")
INDEX = (SAMPLES / "sitemap_index_en.xml").read_text(encoding="utf-8")
PHONES = (SAMPLES / "sitemap_mobile_phones.xml").read_text(encoding="utf-8")
IPHONE13 = (SAMPLES / "product_892008.html").read_text(encoding="utf-8")
IPHONE15 = (SAMPLES / "product_935188.html").read_text(encoding="utf-8")
IPHONE13_URL = "https://www.coolblue.nl/en/product/892008/apple-iphone-13-128gb-white-gold.html"

print("SITEMAPS (samples/robots.txt, samples/*.xml)")
check(1, "small example", lambda: exercises.sitemaps_from_robots("User-agent: *\nSitemap: https://a/x.xml\nsitemap: https://a/y.xml"),
      ["https://a/x.xml", "https://a/y.xml"])
check(1, "Coolblue: 15 sitemaps", lambda: len(exercises.sitemaps_from_robots(ROBOTS)), 15)
check(1, "the English product index", lambda: exercises.sitemaps_from_robots(ROBOTS)[1],
      "https://sitemaps.coolblue.nl/www.coolblue.nl/en/products_1.xml")

check(2, "a product page is allowed", lambda: exercises.allowed(ROBOTS, IPHONE13_URL, USER_AGENT), True)
check(2, "a simple Disallow", lambda: exercises.allowed("User-agent: *\nDisallow: /private", "https://a.com/private/x", "Bot"),
      False)
check(2, "the wildcard trap: robotparser says True for /aanmelding/x (Disallow: /aanmelding/*)",
      lambda: exercises.allowed(ROBOTS, "https://www.coolblue.nl/aanmelding/x", USER_AGENT), True)

check(3, "the index", lambda: (exercises.parse_sitemap(INDEX)[0], len(exercises.parse_sitemap(INDEX)[1])), ("index", 674))
check(3, "a URL set", lambda: (exercises.parse_sitemap(PHONES)[0], len(exercises.parse_sitemap(PHONES)[1])), ("urlset", 440))
check(3, "first product URL (no spaces)", lambda: exercises.parse_sitemap(PHONES)[1][0], IPHONE13_URL)

check(4, "laptops", lambda: exercises.category_sitemaps(exercises.parse_sitemap(INDEX)[1], "laptops")[-1],
      "https://www.coolblue.nl/sitemap/nl_en/products/17632_laptops.xml")
check(4, "upper case word", lambda: len(exercises.category_sitemaps(exercises.parse_sitemap(INDEX)[1], "MOBIELE-TELEFOONS")), 6)
check(4, "only the file name counts", lambda: exercises.category_sitemaps(["https://x/laptops/12_tv.xml"], "laptops"), [])

check(5, "product id", lambda: exercises.product_id(IPHONE13_URL), 892008)
check(5, "not a product", lambda: exercises.product_id("https://www.coolblue.nl/en/laptops"), None)

print("\nJSON-LD (samples/product_*.html)")
check(6, "4 blocks", lambda: [b["@type"] for b in exercises.jsonld_blocks(IPHONE13)],
      ["BreadcrumbList", "Product", "AggregateRating", "AggregateRating"])
check(6, "a list and a @graph are flattened, bad JSON skipped", lambda: [b["@type"] for b in exercises.jsonld_blocks(
    '<script type="application/ld+json">[{"@type": "A"}, {"@type": "B"}]</script>'
    '<script type="application/ld+json">{"@graph": [{"@type": "C"}]}</script>'
    '<script type="application/ld+json">{broken</script>')], ["A", "B", "C"])

check(7, "the Product block", lambda: exercises.find_product(exercises.jsonld_blocks(IPHONE13))["sku"], "892008")
check(7, "@type as a list", lambda: exercises.find_product([{"@type": ["Thing", "Product"], "sku": "1"}])["sku"], "1")
check(7, "no product", lambda: exercises.find_product([{"@type": "Organization"}]), None)

check(8, "iPhone 13 record", lambda: exercises.product_record(exercises.find_product(exercises.jsonld_blocks(IPHONE13)), IPHONE13_URL),
      {"sku": "892008", "name": "Apple iPhone 13 128GB White Gold", "brand": "Apple", "price": 500.0, "currency": "EUR",
       "in_stock": False, "rating": 9.0, "best_rating": 10, "reviews": 112, "url": IPHONE13_URL})
check(8, "iPhone 15 price", lambda: exercises.product_record(exercises.find_product(exercises.jsonld_blocks(IPHONE15)), "")["price"],
      734.0)
check(8, "offers as a list, brand as a string, no rating", lambda: exercises.product_record(
    {"sku": "1", "brand": "Acme", "offers": [{"price": "9.99", "priceCurrency": "EUR",
                                              "availability": "https://schema.org/InStock"}]}, "u"),
    {"sku": "1", "name": None, "brand": "Acme", "price": 9.99, "currency": "EUR", "in_stock": True, "rating": None,
     "best_rating": None, "reviews": None, "url": "u"})

check(9, "the 2 shop ratings (not the phone!)", lambda: exercises.shop_ratings(exercises.jsonld_blocks(IPHONE13)),
      [{"source": "kiyoh.com", "rating": 9.1, "best_rating": 10, "reviews": 136484},
       {"source": "trustpilot.com", "rating": 3.8, "best_rating": 5, "reviews": 160252}])

check(10, "breadcrumb", lambda: exercises.breadcrumb(exercises.jsonld_blocks(IPHONE13))[:3], ["Telephony", "Mobile phones", "Smartphones"])
check(10, "sorted by position", lambda: exercises.breadcrumb([{"@type": "BreadcrumbList", "itemListElement": [
    {"position": 2, "name": "b"}, {"position": 1, "name": "a"}]}]), ["a", "b"])
check(10, "no breadcrumb", lambda: exercises.breadcrumb([]), [])

summary()
