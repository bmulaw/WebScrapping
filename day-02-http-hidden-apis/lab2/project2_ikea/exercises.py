"""Project 2 · IKEA: all the exercises, in one file.

The settings are at the top, then the exercises in order. Fill in each exercise
(replace its `raise NotImplementedError(...)`), then click Run ▶ on check.py.
"""
from pathlib import Path
from urllib.parse import urlencode
import hashlib
import json
import time

import requests


# ==============================================================================
# Settings: change them here
# The settings of the project.
# ==============================================================================

# An honest robot name, in the standard format of search-engine robots ("Mozilla/5.0 (compatible; Name/Version; info)").
# We do NOT pretend to be a browser: we say who we are.
USER_AGENT = "Mozilla/5.0 (compatible; ESILV-Lab-Advanced/1.0; educational use)"

# The API host. Its robots.txt (https://sik.search.blue.cdtapps.com/robots.txt) says: User-agent: *  Allow: /
API_HOST = "https://sik.search.blue.cdtapps.com"

TIMEOUT = 20
DELAY_SECONDS = 2                     # between two calls to the API
CACHE_DIR = Path(__file__).resolve().parent / "data" / "cache"
CACHE_SECONDS = 60                    # the API itself says "Cache-Control: max-age=60"


# ==============================================================================
# HTTP: call the hidden API the way the IKEA website does (you found these calls in DevTools, part 1 of the README).
#
# Every function receives the `session` to use (a real one in main.py, a FakeSession in check.py).
# ==============================================================================

def make_session(user_agent=USER_AGENT):
    """A Session with our User-Agent. (Given.) In part 1 you found that the API needs NO other header."""
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})
    return session


def api_url(endpoint, market="fr", language="fr"):
    """The URL of an API endpoint for one country (market) and one language.

        api_url("search-result-page")              -> "https://sik.search.blue.cdtapps.com/fr/fr/search-result-page"
        api_url("search-box", "us", "en")          -> "https://sik.search.blue.cdtapps.com/us/en/search-box"
    """
    # ----- Exercise 1: api_url -----
    raise NotImplementedError("Exercise 1 (api_url): not done yet")


def search_params(query, size=24, sort=None, filters=None):
    """The query parameters of a product search, as the website sends them.

        search_params("chaise")  -> {"q": "chaise", "size": 24, "types": "PRODUCT"}
        search_params("chaise", 10, sort="PRICE_LOW_TO_HIGH", filters={"f-colors": "10139"})
            -> {"q": "chaise", "size": 10, "types": "PRODUCT", "sort": "PRICE_LOW_TO_HIGH", "f-colors": "10139"}
    "sort" only when a sort is given; the filters are added as they are.
    """
    # ----- Exercise 2: search_params -----
    raise NotImplementedError("Exercise 2 (search_params): not done yet")


def api_error(response):
    """The error message of the API, or None when the answer is not an error (status < 400).

    This API explains its errors in JSON: {"status": 400, "title": "Bad Request", "detail": "Unrecognized parameter: offset"}
        -> "400 Bad Request: Unrecognized parameter: offset"
    If the error body is not JSON: "<status> <the first 100 characters of the text>".
    """
    # ----- Exercise 3: api_error -----
    raise NotImplementedError("Exercise 3 (api_error): not done yet")


def search(session, query, market="fr", language="fr", size=24, sort=None, filters=None):
    """One search -> the JSON answer (a dict). If the API answers an error, raise ValueError(api_error(response)).

    GET api_url("search-result-page", market, language) with search_params(...) and a timeout.
    """
    # ----- Exercise 4: search -----
    raise NotImplementedError("Exercise 4 (search): not done yet")


def search_everything(session, query, market="fr", language="fr", max_items=1000, sort=None, filters=None,
                      delay=DELAY_SECONDS):
    """ALL the results of a search, in at most 2 calls.

    The API has no "page" or "offset" parameter (try it: it answers 400). But it tells you how many results
    exist: data["searchResultPage"]["products"]["main"]["max"]. And the "size" parameter can be big.
    So:
      1. search with size=24 (like the website) and read "max";
      2. if there are more results than you received, wait `delay` seconds, then search again with
         size = min(max, max_items) (max_items: a safety limit).
    Return the JSON of the last call.

        a search with max=112 -> 2 calls: size=24, then size=112
    """
    # ----- Exercise 5: search_everything -----
    raise NotImplementedError("Exercise 5 (search_everything): not done yet")


def autocomplete(session, prefix, market="fr", language="fr"):
    """The suggestions of the search box (a second hidden API, found in DevTools when you TYPE in the box).

    GET api_url("search-box", market, language)?q=<prefix>
    The answer: {"searchBox": {"universal": [ ... ]}}. Some entries have a "completion" (a word to search),
    others a "category" or a "product". Return the texts of the completions, in order.

        autocomplete(session, "cha") -> ["chaise", "chaise bureau", "chambre", "chaussure", "chaise enfant", "chauffeuse"]
    """
    # ----- Exercise 6: autocomplete -----
    raise NotImplementedError("Exercise 6 (autocomplete): not done yet")


# ==============================================================================
# CACHE: do not ask the same question twice in one minute.
#
# The API says "Cache-Control: max-age=60": its answers stay valid 60 seconds. While you develop, you run
# your code again and again: a cache on disk saves the server (and your time). One answer = one JSON file.
# ==============================================================================

def cache_key(url, params):
    """A short file name for one request: the same url + params -> always the same key, in any order.

    Sort the params, build "url?a=1&b=2" (urlencode), hash it with hashlib.sha1, keep the first 16 hex characters.

        cache_key("https://x/s", {"q": "chaise", "size": 24}) == cache_key("https://x/s", {"size": 24, "q": "chaise"})
        len(cache_key("https://x/s", {})) -> 16
    """
    # ----- Exercise 7: cache_key -----
    raise NotImplementedError("Exercise 7 (cache_key): not done yet")


def cached_get_json(session, url, params, cache_dir, max_age=60, timeout=20, now=time.time):
    """GET url with params -> JSON, but use the file cache_dir/<cache_key>.json if it is younger than max_age seconds.

    - the file exists and now() - its modification time (path.stat().st_mtime) < max_age -> read it, no request;
    - else: session.get(url, params=params, timeout=timeout), raise_for_status, save the JSON in the file
      (create cache_dir if needed), return the JSON.
    `now` is a function that returns the current time (check.py replaces it to travel in time).
    """
    # ----- Exercise 8: cached_get_json -----
    raise NotImplementedError("Exercise 8 (cached_get_json): not done yet")


# ==============================================================================
# PARSE: the JSON of the API -> clean rows. No internet here.
#
# Where are the products? Open samples/search_chaise_fr.json in VS Code (right-click → Format Document) and follow:
#     data["searchResultPage"]["products"]["main"]["items"][0]["product"]
# ==============================================================================

def products(data):
    """The list of product dicts of one answer (items without a "product" key are skipped).

        len(products(<search_chaise_fr.json>)) -> 24
        products(<search_chaise_fr.json>)[0]["name"] -> "SANDSBERG"
    """
    # ----- Exercise 9: products -----
    raise NotImplementedError("Exercise 9 (products): not done yet")


def total_results(data):
    """How many products match the search in total (not only in this answer).

        total_results(<search_chaise_fr.json>) -> 112
    """
    # ----- Exercise 10: total_results -----
    raise NotImplementedError("Exercise 10 (total_results): not done yet")


def product_row(product):
    """One product (a nested dict) -> one FLAT row.

        {
          "item_no": "30605423",
          "name": "SANDSBERG",
          "type": "Chaise",                     # typeName
          "price": 14.99,                       # salesPrice -> numeral (a float)
          "currency": "EUR",                    # salesPrice -> currencyCode
          "rating": 3.8,                        # ratingValue (None if missing)
          "rating_count": 17,                   # ratingCount (None if missing)
          "colors": "noir",                     # the names of all the colors, joined with ", "
          "category": "Chaises de table",       # the LAST name of categoryPath (the most precise), or None
          "url": "https://www.ikea.com/fr/fr/p/sandsberg-chaise-noir-30605423/",   # pipUrl
        }
    """
    # ----- Exercise 11: product_row -----
    raise NotImplementedError("Exercise 11 (product_row): not done yet")


def sort_ids(data):
    """The sorts the API offers (it describes itself!): the "id" of each value of products -> sortOrders -> values.

        sort_ids(<search_chaise_fr.json>)[:3] -> ["RELEVANCE", "PRICE_LOW_TO_HIGH", "PRICE_HIGH_TO_LOW"]
    """
    # ----- Exercise 12: sort_ids -----
    raise NotImplementedError("Exercise 12 (sort_ids): not done yet")


def filter_param(data, filter_id, value_name):
    """Build the query parameter of a filter, from what the API says about its own filters.

    In products -> filters, each filter has an "id" ("COLOR"), a "parameter" (the URL parameter name, "f-colors")
    and "values" ({"name": "noir", "id": "10139", "count": 43} ...).

        filter_param(data, "COLOR", "noir")  -> {"f-colors": "10139"}
        filter_param(data, "COLOR", "violet fluo") -> raise KeyError (the API does not offer it)
    """
    # ----- Exercise 13: filter_param -----
    raise NotImplementedError("Exercise 13 (filter_param): not done yet")


def compare_markets(rows_a, rows_b):
    """The same product in two countries: the rows (product_row) of two searches -> the products found in BOTH.

    Match them by item_no. Return a list sorted by item_no of:
        {"item_no": ..., "name": ..., "price_a": ..., "currency_a": ..., "price_b": ..., "currency_b": ...}
    """
    # ----- Exercise 14: compare_markets -----
    raise NotImplementedError("Exercise 14 (compare_markets): not done yet")
