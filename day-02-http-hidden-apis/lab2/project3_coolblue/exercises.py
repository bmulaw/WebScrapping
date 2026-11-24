"""Project 3 · Coolblue: all the exercises, in one file.

The settings are at the top, then the exercises in order. Fill in each exercise
(replace its `raise NotImplementedError(...)`), then click Run ▶ on check.py.
"""
from urllib import robotparser
import json
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


# ==============================================================================
# Settings: change them here
# The settings of the project.
# ==============================================================================

# Coolblue answers 403 to "python-requests/2.x" and to "ESILV-Lab/1.0", but accepts the standard robot format:
# "Mozilla/5.0 (compatible; <name>/<version>; <info>)" (the format of Googlebot, Bingbot ...).
# It is HONEST: it says "I am a robot called ESILV-Lab-Advanced". We never copy a real browser's User-Agent.
USER_AGENT = "Mozilla/5.0 (compatible; ESILV-Lab-Advanced/1.0; educational use)"

SITE = "https://www.coolblue.nl"
ROBOTS_URL = f"{SITE}/robots.txt"

TIMEOUT = 30
DELAY_SECONDS = 3          # product pages are big (1.5 MB): be gentle
MAX_PRODUCTS = 15          # a safety limit for main.py


# ==============================================================================
# DISCOVER: robots.txt -> sitemaps -> product URLs. No HTML pages to crawl, no "Next" button to click.
#
# A sitemap is an XML file the site publishes FOR robots: "here are all my pages".
#     - a sitemap INDEX lists other sitemaps:  <sitemapindex><sitemap><loc>...xml</loc></sitemap>...</sitemapindex>
#     - a URL SET lists pages:                 <urlset><url><loc>https://.../product/...html</loc></url>...</urlset>
# Both use the namespace http://www.sitemaps.org/schemas/sitemap/0.9 (see the README, part 2).
# ==============================================================================

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def sitemaps_from_robots(robots_text):
    """All the "Sitemap:" URLs written in a robots.txt, in order. ("Sitemap:" or "sitemap:", any case.)

        sitemaps_from_robots("User-agent: *\\nSitemap: https://a/x.xml\\nsitemap: https://a/y.xml")
            -> ["https://a/x.xml", "https://a/y.xml"]
    """
    # ----- Exercise 1: sitemaps_from_robots -----
    raise NotImplementedError("Exercise 1 (sitemaps_from_robots): not done yet")


def allowed(robots_text, url, user_agent):
    """May this user_agent fetch this url, according to robots.txt? (urllib.robotparser)

    Careful: Python's robotparser does NOT understand the "*" and "$" wildcards inside paths
    (Coolblue uses some: "Disallow: */api/*"). For those rules, read robots.txt yourself.
    """
    # ----- Exercise 2: allowed -----
    raise NotImplementedError("Exercise 2 (allowed): not done yet")


def parse_sitemap(xml_text):
    """A sitemap -> ("index", [the sitemap URLs]) or ("urlset", [the page URLs]).

    Use xml.etree.ElementTree: root = ET.fromstring(xml_text). The tag of root tells you the kind:
    "{http://www.sitemaps.org/schemas/sitemap/0.9}sitemapindex" or "...}urlset".
    root.findall(".//sm:loc", NS) finds every <loc>. Strip the spaces around each URL.

        parse_sitemap(<sitemap_index_en.xml>)    -> ("index", [674 URLs ending in .xml])
        parse_sitemap(<sitemap_mobile_phones.xml>) -> ("urlset", [440 product URLs])
    """
    # ----- Exercise 3: parse_sitemap -----
    raise NotImplementedError("Exercise 3 (parse_sitemap): not done yet")


def category_sitemaps(index_urls, word):
    """The sitemaps of the index whose FILE NAME contains `word` (lower case comparison).

    The file names look like ".../products/2093_mobiele-telefoons.xml" (Dutch names, even in English!).

        category_sitemaps(index, "laptops") -> [".../17632_laptops.xml", ...]
    """
    # ----- Exercise 4: category_sitemaps -----
    raise NotImplementedError("Exercise 4 (category_sitemaps): not done yet")


def product_id(url):
    """The product number in a product URL, as an int. Not a product URL -> None.

        product_id("https://www.coolblue.nl/en/product/892008/apple-iphone-13-128gb-white-gold.html") -> 892008
    """
    # ----- Exercise 5: product_id -----
    raise NotImplementedError("Exercise 5 (product_id): not done yet")


# ==============================================================================
# EXTRACT: the JSON-LD blocks of a product page -> a clean product record. No internet here.
#
# JSON-LD (https://schema.org) is structured data that shops put in their pages for Google:
#     <script type="application/ld+json"> {"@type": "Product", "name": ..., "offers": {"price": ...}} </script>
# It is much more stable than CSS classes: the shop needs it to be correct (Google shows it in the results).
# ==============================================================================

def jsonld_blocks(html):
    """Every JSON-LD object of a page, as a flat list of dicts.

    - find every <script type="application/ld+json">, json.loads its text;
    - a block can be ONE dict, a LIST of dicts, or a dict with "@graph": [dicts]: flatten them all;
    - a block that is not valid JSON is skipped (it happens on real sites).

        [block["@type"] for block in jsonld_blocks(<product_892008.html>)]
            -> ["BreadcrumbList", "Product", "AggregateRating", "AggregateRating"]
    """
    # ----- Exercise 6: jsonld_blocks -----
    raise NotImplementedError("Exercise 6 (jsonld_blocks): not done yet")


def has_type(block, wanted):
    """True if the block's "@type" is `wanted`. (Given.) "@type" can be a string or a list of strings."""
    kind = block.get("@type")
    return wanted in kind if isinstance(kind, list) else kind == wanted


def find_product(blocks):
    """The first block of type "Product", or None."""
    # ----- Exercise 7: find_product -----
    raise NotImplementedError("Exercise 7 (find_product): not done yet")


def product_record(product, url):
    """A JSON-LD Product -> one flat record.

        {
          "sku": "892008",
          "name": "Apple iPhone 13 128GB White Gold",
          "brand": "Apple",                     # brand can be a dict {"@type": "Brand", "name": ...} or a string
          "price": 500.0,                       # offers -> price, as a float ("offers" can also be a LIST: take the first)
          "currency": "EUR",                    # offers -> priceCurrency
          "in_stock": False,                    # offers -> availability == "https://schema.org/InStock"
          "rating": 9.0,                        # aggregateRating -> ratingValue (float), None if no rating
          "best_rating": 10,                    # aggregateRating -> bestRating: a 9 out of 10, not out of 5!
          "reviews": 112,                       # aggregateRating -> reviewCount
          "url": url,
        }
    """
    # ----- Exercise 8: product_record -----
    raise NotImplementedError("Exercise 8 (product_record): not done yet")


def shop_ratings(blocks):
    """THE TRAP: the page has 3 ratings. The product's is INSIDE the Product block.
    The 2 separate "AggregateRating" blocks rate the SHOP Coolblue (itemReviewed is an Organization), not the phone.

    Return the shop ratings: for each AggregateRating block whose itemReviewed has "@type" "Organization":
        {"source": the domain of its "url" without "www." ("kiyoh.com", "trustpilot.com"),
         "rating": ratingValue, "best_rating": bestRating, "reviews": reviewCount}

        shop_ratings(blocks)[1] -> {"source": "trustpilot.com", "rating": 3.8, "best_rating": 5, "reviews": 160252}
    """
    # ----- Exercise 9: shop_ratings -----
    raise NotImplementedError("Exercise 9 (shop_ratings): not done yet")


def breadcrumb(blocks):
    """The category path of the product, from the BreadcrumbList block: the "name" of each itemListElement,
    in order of "position". No BreadcrumbList -> [].

        breadcrumb(<product_892008.html blocks>)[:3] -> ["Telephony", "Mobile phones", "Smartphones"]
    """
    # ----- Exercise 10: breadcrumb -----
    raise NotImplementedError("Exercise 10 (breadcrumb): not done yet")
