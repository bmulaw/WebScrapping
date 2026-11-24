"""Project 1 · Open Food Facts: all the exercises, in one file.

The settings are at the top, then the exercises in order. Fill in each exercise
(replace its `raise NotImplementedError(...)`), then click Run ▶ on check.py.
"""
import json
import math
import time

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import requests
from requests import session


# ==============================================================================
# Settings: change them here
# The settings of the project. Change USER_AGENT: put your own e-mail (Open Food Facts asks for it).
# ==============================================================================

# Open Food Facts asks every app to say who it is: "AppName/Version (ContactEmail)".
# An app without a User-Agent can be blocked. https://openfoodfacts.github.io/openfoodfacts-server/api/
USER_AGENT = "ESILV-Lab-Advanced/1.0 (educational use; student@example.com)"

API = "https://world.openfoodfacts.org/api/v2"               # the main API (read)
SEARCH_A_LICIOUS = "https://search.openfoodfacts.org/search"  # the new full-text search API
STAGING = "https://world.openfoodfacts.net"                   # the TEST server: write here, never on .org
STAGING_AUTH = ("off", "off")                                 # the test server is behind a simple password

TIMEOUT = 20          # seconds. ALWAYS give a timeout: without one, a request can wait forever
DELAY_SECONDS = 6     # between two search pages. The search API allows about 10 requests per minute

# Ask only for what you use: smaller answers, faster, kinder to the server.
PRODUCT_FIELDS = ["code", "product_name", "brands", "nutriscore_grade", "nutriments", "image_front_url", "quantity"]
SEARCH_FIELDS = ["code", "product_name", "brands", "nutriscore_grade", "nutriments", "image_front_url"]


# ==============================================================================
# HTTP: everything that talks to the Open Food Facts servers.
#
# Every function receives the `session` it must use. In main.py it is a real requests.Session;
# in check.py it is a FakeSession that answers with the files in samples/ (no internet needed).
# So: never call requests.get() directly here, always session.get(...).
# ==============================================================================

def make_session(user_agent=USER_AGENT, retries=3):
    """A requests.Session ready for a polite API client.

    - header "User-Agent" = user_agent, header "Accept" = "application/json"
    - automatic retries for https:// URLs: `retries` times, on the statuses 429, 500, 502, 503, 504,
      only for GET, waiting longer and longer (backoff_factor=1 -> 0 s, 2 s, 4 s ...),
      and respecting the "Retry-After" header when the server sends one.

        session = make_session()
        session.headers["User-Agent"]                      -> "ESILV-Lab-Advanced/1.0 (...)"
        session.get_adapter("https://x").max_retries.total -> 3
    """
    # ----- Exercise 1: make_session -----
    session = requests.Session()
    session.headers.update({
        "User-Agent": user_agent,
        "Accept": "application/json"
    })
    Retry(total=retries,
            backoff_factor=1, 
            status_forcelist=[429, 500, 502, 503, 504], 
            allowed_methods=["GET"], 
            respect_retry_after_header=True)
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session
    # raise NotImplementedError("Exercise 1 (make_session): not done yet")


def get_product(session, barcode, fields=PRODUCT_FIELDS):
    """One product by its barcode -> the "product" dict, or None if Open Food Facts does not know it.

    GET {API}/product/{barcode}?fields=code,product_name,...     (the fields joined with commas)

    Careful: for an unknown or invalid barcode, the server can answer HTTP 200 (!) with
    {"status": 0, "status_verbose": "no code or invalid code"}, or HTTP 404. Both mean: None.
    Any other error status (500 ...) must raise an exception (raise_for_status).

        get_product(session, "3017624010701")["product_name"]  -> "Nutella"
        get_product(session, "0000000000000")                   -> None
    """
    # ----- Exercise 2: get_product -----
    # session.get(url, params={"fields": ...}, timeout=TIMEOUT)
    # 404 -> None ; then response.raise_for_status() ; then look at data["status"]
    raise NotImplementedError("Exercise 2 (get_product): not done yet")


def search_page(session, category, country, page=1, page_size=20, fields=SEARCH_FIELDS):
    """One page of a search -> the JSON answer (a dict with "count", "page", "page_size", "products").

    GET {API}/search with these query parameters:
        categories_tags_en = category      (e.g. "breakfast-cereals")
        countries_tags_en  = country       (e.g. "france")
        fields             = the fields joined with commas
        page, page_size
        sort_by            = "unique_scans_n"   (the most scanned products first: a stable order)
    Raise an exception for an error status.
    """
    # ----- Exercise 3: search_page -----
    raise NotImplementedError("Exercise 3 (search_page): not done yet")


def number_of_pages(count, page_size):
    """How many pages for `count` results, `page_size` per page?

    Careful: in the answer of the search API, "page_count" is NOT the number of pages
    (it is the number of products on THIS page). Compute it yourself.

        number_of_pages(7574, 20) -> 379
        number_of_pages(40, 20)   -> 2
        number_of_pages(0, 20)    -> 0
    """
    # ----- Exercise 4: number_of_pages -----
    raise NotImplementedError("Exercise 4 (number_of_pages): not done yet")


def search_all(session, category, country, max_pages=5, page_size=20, delay=DELAY_SECONDS):
    """All the products of a search, page after page (pagination with a page NUMBER).

    Read page 1, 2, 3 ... with search_page(). Stop when:
      - you have read the last page (use number_of_pages with the "count" of the first answer), or
      - you have read max_pages pages (a safety limit: never download 7574 products by mistake), or
      - a page has no products.
    Wait `delay` seconds BETWEEN two pages (time.sleep), not after the last one.
    Return one list with the products of all the pages read.
    """
    # ----- Exercise 5: search_all -----
    raise NotImplementedError("Exercise 5 (search_all): not done yet")


def download_image(session, url, path, chunk_size=64 * 1024):
    """Download a (possibly big) file without keeping it all in memory -> the number of bytes written.

    Use stream=True and response.iter_content(chunk_size): write each chunk to the file.
    `path` is a pathlib.Path; create its folder if needed. url None or "" -> write nothing, return 0.
    Raise an exception for an error status.
    """
    # ----- Exercise 6: download_image -----
    # with session.get(url, stream=True, timeout=TIMEOUT) as response: ...
    # with open(path, "wb") as file: file.write(chunk)
    raise NotImplementedError("Exercise 6 (download_image): not done yet")


def full_text_search(session, query, page_size=10):
    """The NEW search API (search-a-licious): search by words, like a search box.

    GET {SEARCH_A_LICIOUS}?q=<query>&page_size=<page_size>
    The answer has a list "hits". Return, for each hit, a small dict:
        {"code": ..., "name": hit["product_name"], "brands": the list hit["brands"] joined with ", "}
    (a hit without brands -> "", without a name -> None)

        full_text_search(session, "nutella", 5)[1] -> {"code": "0098008952506", "name": "Nutella", "brands": "Nutella"}
    """
    # ----- Exercise 7: full_text_search -----
    raise NotImplementedError("Exercise 7 (full_text_search): not done yet")


def build_edit_request(barcode, changes, user_id, password):
    """PREPARE (do not send!) a POST that edits a product on the TEST server -> a requests.PreparedRequest.

    Writing is serious: you build the request, you LOOK at it, and only then you send it (to the test server).
        method  POST
        url     {STAGING}/cgi/product_jqm2.pl
        data    a FORM (not JSON): {"code": barcode, "user_id": user_id, "password": password, **changes}
        auth    STAGING_AUTH  (HTTP Basic authentication: an "Authorization: Basic ..." header)

    requests.Request(method, url, data=..., auth=...).prepare() builds it without sending it.

        request = build_edit_request("3017624010701", {"quantity": "400 g"}, "me", "secret")
        request.body    -> "code=3017624010701&user_id=me&password=secret&quantity=400+g"
        request.headers["Content-Type"] -> "application/x-www-form-urlencoded"
    """
    # ----- Exercise 8: build_edit_request -----
    raise NotImplementedError("Exercise 8 (build_edit_request): not done yet")


# ==============================================================================
# PARSE: JSON (or HTML) in -> clean Python values out. No internet here: easy to test.
# ==============================================================================

def to_float(value):
    """A number from the API -> float, or None. (Given: you can use it.)

        to_float(56.3) -> 56.3     to_float("12") -> 12.0     to_float(None) -> None     to_float("") -> None
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def product_row(product):
    """One product of the API (a nested dict) -> one FLAT row for a table (CSV, pandas).

        {
          "code": "3017624010701",
          "name": "Nutella",
          "brand": "Ferrero",             # only the FIRST brand of "brands" ("Quaker, Cruesli" -> "Quaker"), stripped
          "nutriscore": "E",              # UPPER case; missing, "unknown" or "not-applicable" -> None
          "kcal_100g": 539.0,             # nutriments["energy-kcal_100g"]
          "sugars_100g": 56.3,            # nutriments["sugars_100g"]
          "fat_100g": 30.9,
          "salt_100g": 0.1075,
          "proteins_100g": 6.3,
          "image_url": "https://images.openfoodfacts.org/...jpg",   # image_front_url, or None
        }
    Any missing value -> None (use .get() everywhere, and to_float for the numbers). Never a KeyError.
    """
    # ----- Exercise 9: product_row -----
    raise NotImplementedError("Exercise 9 (product_row): not done yet")


def jsonld_types(html):
    """The "@type" of every JSON-LD block of an HTML page, in order.

    JSON-LD = <script type="application/ld+json"> { ... } </script>: structured data for search engines.
    Many shops put the whole product there (name, price ...). Open Food Facts? Let us see.

        jsonld_types(<the Nutella page>) -> ["WebSite", "Organization"]
    A block that is not valid JSON is skipped.
    """
    # ----- Exercise 10: jsonld_types -----
    # BeautifulSoup(html, "lxml").select('script[type="application/ld+json"]'), then json.loads(tag.string)
    raise NotImplementedError("Exercise 10 (jsonld_types): not done yet")


def title_from_html(html):
    """The product page title <h1> "Nutella – Ferrero – 400.0 g" -> {"name": ..., "brand": ..., "quantity": ...}.

    The parts are separated by " – " (a long dash with spaces). A missing part -> None. No <h1> -> all None.

        title_from_html(<the Nutella page>) -> {"name": "Nutella", "brand": "Ferrero", "quantity": "400.0 g"}

    Trap: HTML pages often use a NON-BREAKING space ("\xa0", &nbsp;) that looks like a space but is not " ".
    print(repr(text)) shows it. Replace it with a normal space.

    Compare with the API: same information, but here it depends on the page design (it can change any day).
    """
    # ----- Exercise 11: title_from_html -----
    raise NotImplementedError("Exercise 11 (title_from_html): not done yet")


# ==============================================================================
# ANALYSIS: the rows (product_row) in a pandas table, and one question to the data.
# ==============================================================================

def sugar_by_grade(rows):
    """Is a better Nutri-Score really less sugar? -> a DataFrame, one line per grade.

        rows: a list of dicts made by product_row()
        index:   the grade "A" ... "E" (sorted), only grades that appear; rows without a grade are ignored
        columns: "products"     how many products have this grade
                 "mean_sugars"  the mean of sugars_100g (ignore missing values), rounded to 1 decimal

    pandas: DataFrame(rows), dropna(subset=[...]), groupby("nutriscore").agg(products=(...), mean_sugars=(...))
    """
    # ----- Exercise 12: sugar_by_grade -----
    raise NotImplementedError("Exercise 12 (sugar_by_grade): not done yet")
