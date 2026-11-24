"""Project 2 · The Souled Store, PRODUCT pages: all the exercises, in one file.

The settings are at the top, then the exercises in order. Fill in each exercise
(replace its `raise NotImplementedError(...)`), then click Run ▶ on check.py.
"""
import base64
import json
import re
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# ==============================================================================
# Settings: change them here
# ==============================================================================

USER_AGENT = "Mozilla/5.0 (compatible; ESILV-Lab-Advanced/1.0; educational use)"

SITE = "https://www.thesouledstore.com"
PRODUCT = "solids-inkstone-oversized-polos"          # the "slug": the end of the product URL
PRODUCT_API = "https://api.thesouledstore.com/api/v2/product"   # found in part B
LISTING_API = "https://api.thesouledstore.com/api/v2/pre-order/products/listing"   # the lesson's API

TIMEOUT = 20
DELAY_SECONDS = 2          # between two API calls
MAX_PRODUCTS = 10          # safety limit for main.py


def product_url(slug=PRODUCT):
    """(Given.) https://www.thesouledstore.com/product/solids-inkstone-oversized-polos"""
    return f"{SITE}/product/{slug}"


# ==============================================================================
# PART A · THE BROWSER on ONE product page.
#
# requests gets the title of the product ... but NO price and NO sizes (open samples/raw_product_page.html).
# JavaScript asks the server for them after the page loads. In Chrome the page becomes
# (samples/rendered_product_page.html, simplified):
#
#   <div class="product-info-module__nOltAa__nonmembershipProductPrice fbold"><span>₹ </span>1499</div>
#
#   <ul class="product-variant-module__V1ijmq__sizelist sizelist">
#     <li class="... oval ... outstock ...">   (a SOLD OUT size)
#         <input disabled> <label><span>XXS</span></label>
#         <section class="... total-stock" style="display: none;">0 Left</section>
#     </li>
#     <li class="... oval ...">                (an available size, only 1 left: the text is SHOWN)
#         <input> <label><span>XS</span></label>
#         <section class="... total-stock" style="display: block;">1 Left</section>
#     </li>
#     ...
#
#   <div class="card">                        (an accordion section, OPEN)
#     <div class="card-header"><h2><button aria-expanded="true">Product Details</button></h2></div>
#     <div class="card-block"> ... the text of the section ... </div>
#   </div>
#   <div class="card">                        (a CLOSED section: no "card-block" at all)
#     <div class="card-header"><h2><button aria-expanded="false">Product Description</button></h2></div>
#   </div>
#
# Classes like "product-variant-module__V1ijmq__sizelist" are GENERATED: the "V1ijmq" part changes with each new
# version of the site. Build your selectors on the stable parts ("sizelist", "oval", "outstock", the end of the
# price class ...), never on the generated ones.
# ==============================================================================

def make_driver(headless=True, user_agent=USER_AGENT, log_network=True):
    """Start a Chrome driven by Selenium and return the driver.

    The Chrome must:
        - run without a window when `headless` is True (with a window when it is False);
        - have a window of 1400 x 1000 pixels;
        - send `user_agent` as its User-Agent;
        - when `log_network` is True, record its network events, so that driver.get_log("performance") works
          (lesson 2, section 1).
    """
    # ----- Exercise 1: make_driver -----
    raise NotImplementedError("Exercise 1 (make_driver): not done yet")


def wait_for_price(driver, timeout=10):
    """Wait until the price is shown on the page, then return it as an int.

    The driver is already on a product page, but the price may not be there yet: it arrives after the page.
    Wait (an explicit wait, no sleep) until the price element exists AND its text contains a number.

    Return: the price as an int.            "₹ 1499"  ->  1499
    No price after `timeout` seconds: let Selenium's TimeoutException go up (do not catch it).
    """
    # ----- Exercise 2: wait_for_price -----
    raise NotImplementedError("Exercise 2 (wait_for_price): not done yet")


def read_sizes(driver):
    """Read the size buttons of the page: one dict per size, in page order.

    First wait until the size buttons are on the page (they also arrive after the page).
    For each size:
        "size"       the size written on the button ("XXS", "XS", "S" ...)
        "available"  False if the size is sold out (its <li> has the class "outstock"), else True
        "left"       the number of the "N Left" text, ONLY when that text is visible on the page, else None

    Example (samples, product "Solids: Inkstone"):
        [{"size": "XXS", "available": False, "left": None},     # sold out
         {"size": "XS",  "available": True,  "left": 1},        # "1 Left" is visible
         {"size": "S",   "available": True,  "left": None},     # "12 Left" exists in the HTML but is hidden
         ...]
    Think: what does Selenium give you for the text of an element that is hidden?
    """
    # ----- Exercise 3: read_sizes -----
    raise NotImplementedError("Exercise 3 (read_sizes): not done yet")


def open_section(driver, title, timeout=10):
    """Open one section of the accordion and return its text.

    `title` is the text of the section's button: "Product Details", "Product Description" or "Artist's Details".
    The page keeps ONE section open at a time, and a closed section has no text in the page at all.

    1. Click the button whose text is `title`.
    2. Wait (explicit wait) until the text of THAT section is visible: the panel appears after the click, and is
       filled a moment later.
    3. Return the text of the section, without spaces around it.

    Example: open_section(driver, "Product Description") -> "This polo's got your back (and style game) covered. ..."
    """
    # ----- Exercise 4: open_section -----
    raise NotImplementedError("Exercise 4 (open_section): not done yet")


# ==============================================================================
# PART B · CHROME DEVTOOLS PROTOCOL: where do the price and the sizes come from?
#
# driver.get_log("performance") gives Chrome's network events (lesson 2, section 6). Each entry is a dict whose
# "message" is a JSON TEXT. Once decoded, a message looks like:
#     {"method": "Network.requestWillBeSent",
#      "params": {"requestId": "17460.195", "type": "Fetch",
#                 "request": {"url": "https://...", "method": "GET", "postData": "..." (only when a body is sent)}}}
#     {"method": "Network.responseReceived",
#      "params": {"requestId": "17460.195", "response": {"url": "https://...", "status": 200}}}
# The same requestId = the same request. Open samples/performance_log.json: it was recorded on the real page.
# ==============================================================================

def network_events(log_entries):
    """Keep only the network events of a Chrome log.

    Input:  the list returned by driver.get_log("performance").
    Return: the list of the decoded "message" dicts whose "method" starts with "Network.", in the same order.
    """
    # ----- Exercise 5: network_events -----
    raise NotImplementedError("Exercise 5 (network_events): not done yet")


def find_api_calls(events, url_part):
    """List the requests of the page whose URL contains `url_part`, with their answer status.

    Input:  network events (exercise 5) and a piece of URL.
    Return: one dict per matching request, in order:
        {"request_id": "17460.195",
         "method": "GET",
         "url": "https://api.thesouledstore.com/api/v2/product/solids-inkstone-oversized-polos/pricing",
         "body": None,      # the body the request sent, decoded from JSON (a POST); None when there is none
         "status": 200}     # the status of the answer with the same requestId; None when there is no answer

    Example (samples/performance_log.json, url_part "/product/solids-inkstone-oversized-polos/"):
        two calls: GET .../pricing (200) and GET .../inventory (200)
    """
    # ----- Exercise 6: find_api_calls -----
    raise NotImplementedError("Exercise 6 (find_api_calls): not done yet")


def response_json(driver, request_id):
    """Read, from Chrome itself, the JSON answer of one request the page made.

    Input:  the driver, and the request_id of a call (exercise 6).
    Return: the answer, decoded from JSON (a dict or a list).
    Use the Chrome DevTools command that returns the body of a response (lesson 2, section 6). Careful: Chrome may
    give the body encoded in base64 (it tells you so in its answer): decode it first in that case.
    """
    # ----- Exercise 7: response_json -----
    raise NotImplementedError("Exercise 7 (response_json): not done yet")


# ==============================================================================
# PART C · READ THE TWO ANSWERS (open samples/pricing_*.json and samples/inventory_*.json)
#
#   pricing:   {"price": 1499.0, "spl_price": 0.0, "exclusive_price": 1399.0, "mrp": 1799.0, ...}
#   inventory: {"stock": 0, "prod_qty": 12, "variant": [
#                 {"id": 1, "name": "...", "stock": 0,
#                  "attributes": [{"name": "size", "value": "XXS"}, {"name": "color", "value": ""}]},
#                 ...]}
# ==============================================================================

def sizes_from_inventory(inventory):
    """Turn the inventory answer into one dict per size, in order.

    Return: [{"size": "XXS", "stock": 0, "available": False},
             {"size": "XS",  "stock": 1, "available": True}, ...]
    "size" is the value of the attribute NAMED "size" (it is not always the first attribute).
    "available" is True when the stock is above 0.
    """
    # ----- Exercise 8: sizes_from_inventory -----
    raise NotImplementedError("Exercise 8 (sizes_from_inventory): not done yet")


def price_row(pricing):
    """Turn the pricing answer into a small dict of ints.

    Return: {"price": 1499, "mrp": 1799, "member_price": 1399, "discount_pct": 17}
        price         the "price"
        mrp           the "mrp" (the price before the discount); 0 when it is missing
        member_price  the "exclusive_price" (the price for members); 0 when it is missing
        discount_pct  the discount from mrp to price, in %, rounded to an int (0 when there is no mrp)
    """
    # ----- Exercise 9: price_row -----
    raise NotImplementedError("Exercise 9 (price_row): not done yet")


# ==============================================================================
# PART D · BACK TO requests: the same two answers, for MANY products, without a browser.
# ==============================================================================

def make_session(user_agent=USER_AGENT):
    """(Given.) A Session with our honest User-Agent."""
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent, "Accept": "application/json"})
    return session


def listing_slugs(session, how_many=10):
    """(Given: the API of the lesson.) The slugs of the first t-shirts of the listing, e.g. ["dr-doom-doomsday-...", ...]."""
    body = {"category": "t-shirts", "tags": "", "artist": "", "filters": {"sort": "Relevance"}, "page": 1,
            "offset": how_many, "tiptile": 1, "is_exclusive": 0, "gender_type": 3}
    response = session.post(LISTING_API, json=body, timeout=TIMEOUT)
    response.raise_for_status()
    return [product["product_slug"] for product in response.json()["products"]]


def api_url(slug, what):
    """Build the URL of one answer of the API.

    `what` is "pricing" or "inventory". Anything else: raise a ValueError.
    Example: api_url("solids-inkstone-oversized-polos", "pricing")
             -> "https://api.thesouledstore.com/api/v2/product/solids-inkstone-oversized-polos/pricing"
    """
    # ----- Exercise 10: api_url -----
    raise NotImplementedError("Exercise 10 (api_url): not done yet")


def fetch_json(session, url):
    """Download one JSON answer with the session.

    - always with a timeout (TIMEOUT);
    - 404 (no such product): return None;
    - any other error status (500 ...): raise an HTTPError;
    - otherwise: return the decoded JSON.
    """
    # ----- Exercise 11: fetch_json -----
    raise NotImplementedError("Exercise 11 (fetch_json): not done yet")


def product_report(session, slugs, delay=DELAY_SECONDS):
    """Build one row per product: its prices and its stock, from the two answers of the API.

    For each slug, download its pricing and its inventory (exercises 10 and 11), then make the row:
        {"slug": "solids-inkstone-oversized-polos",
         "price": 1499, "mrp": 1799, "member_price": 1399, "discount_pct": 17,     # exercise 9
         "in_stock": "XS S M L XL XXL XXXL",     # the available sizes, separated by one space
         "sold_out": "XXS",                       # the sizes with no stock ("" when there is none)
         "few_left": "XS"}                        # the available sizes with a stock of 5 or less ("" when none)
    Rules:
        - a product whose pricing or inventory does not exist (404) is left out of the report;
        - wait `delay` seconds before every request except the very first one.
    """
    # ----- Exercise 12: product_report -----
    raise NotImplementedError("Exercise 12 (product_report): not done yet")


def compare_sizes(page_sizes, api_sizes):
    """Do the page (exercise 3) and the API (exercise 8) agree on which sizes are available?

    Both inputs are lists of dicts with at least "size" and "available".
    Return: {"same": True when both lists have the same sizes AND the same available ones,
             "only_page_available": the sizes available on the page but not in the API, sorted,
             "only_api_available": the sizes available in the API but not on the page, sorted}
    """
    # ----- Exercise 13: compare_sizes -----
    raise NotImplementedError("Exercise 13 (compare_sizes): not done yet")
