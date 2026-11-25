"""Project 1 · LDLC: all the exercises, in one file.

The settings are at the top, then the exercises in order. Fill in each exercise
(replace its `raise NotImplementedError(...)`), then click Run ▶ on check.py.
"""
import json
import re
import time
from urllib.parse import urljoin, urlsplit

import pandas as pd
import requests
from bs4 import BeautifulSoup


# ==============================================================================
# Settings: change them here
# ==============================================================================

# The honest robot format (see lab 2): it says "I am a robot called ESILV-Lab-Advanced". Never a copied browser one.
USER_AGENT = "Mozilla/5.0 (compatible; ESILV-Lab-Advanced/1.0; educational use)"

SITE = "https://www.ldlc.com"
CATEGORY_URL = f"{SITE}/informatique/pieces-informatique/carte-graphique-interne/c4684/"   # graphics cards
ROBOTS_URL = f"{SITE}/robots.txt"

TIMEOUT = 20
DELAY_SECONDS = 3          # a pause between two pages: one small shop server, 30 students
MAX_PAGES = 2              # safety limits for main.py: at most 2 listing pages ...
MAX_PRODUCTS = 12          # ... and 12 product pages


# ==============================================================================
# PART 1 · ROBOTS.TXT
#
# LDLC's robots.txt has rules with wildcards, for example:    Disallow: */stocks/        Disallow: /v4/
# Python's urllib.robotparser does not understand "*" and "$" in a rule. So you write your own check.
# The rules (the same as Google's):
#     - "*" means "any characters (or none)";
#     - "$" at the end of a rule means "the path must end here";
#     - a rule matches when the path STARTS with it;
#     - if several rules match, the LONGEST rule wins; if an Allow and a Disallow have the same length, Allow wins;
#     - if no rule matches, the page is allowed.
# ==============================================================================

def rule_matches(rule, path):
    """Say if one robots.txt rule matches a path.

    Input:  a rule (the text after "Allow:" or "Disallow:") and a path (the part of the URL after the site name).
    Return: True or False.

    Examples:
        rule_matches("/v4/", "/v4/fr-fr/header/user")          -> True    (the path starts with the rule)
        rule_matches("/recherche/", "/informatique/")           -> False
        rule_matches("*/stocks/", "/fiche/PB1/stocks/")         -> True    ("*" = any characters)
        rule_matches("/*.pdf$", "/doc/cgv.pdf")                 -> True
        rule_matches("/*.pdf$", "/doc/cgv.pdf?x=1")             -> False   ("$" = the path must end there)
        rule_matches("/a.b", "/axb")                            -> False   (a "." is just a dot)
        rule_matches("", "/anything")                           -> False   (an empty rule matches nothing)
    """
    # ----- Exercise 1: rule_matches -----
    raise NotImplementedError("Exercise 1 (rule_matches): not done yet")


def rules_for_everyone(robots_text):
    """(Given.) The rules of the "User-agent: *" groups, as a list of ("allow" | "disallow", rule).

    A group is: one or more "User-agent:" lines, then its rules. Comments (# ...) and empty rules are ignored.
    """
    rules, agents, in_rules = [], [], False
    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()
        name, _, value = line.partition(":")
        name, value = name.strip().lower(), value.strip()
        if name == "user-agent":
            if in_rules:                       # a new group starts
                agents, in_rules = [], False
            agents.append(value)
        elif name in ("allow", "disallow"):
            in_rules = True
            if "*" in agents and value:
                rules.append((name, value))
    return rules


def allowed(robots_text, url):
    """Say if robots.txt allows us to download this URL.

    Input:  the text of robots.txt, and a full URL.
    Return: True (allowed) or False (not allowed).

    What to check: the path of the URL, WITH its query string if it has one ("/a?b=1", not just "/a").
    Use the rules for all robots (the given function rules_for_everyone) and exercise 1.
    Follow the rules written above PART 1: the longest matching rule wins, Allow wins a tie, no match = allowed.

    Examples (samples/robots.txt is LDLC's real robots.txt):
        allowed(LDLC robots, "https://www.ldlc.com/fiche/PB00686694.html")    -> True
        allowed(LDLC robots, "https://www.ldlc.com/v4/fr-fr/prices")          -> False   (Disallow: /v4/)
        allowed(LDLC robots, "https://www.ldlc.com/x/stocks/y")               -> False   (Disallow: */stocks/)
        allowed("User-agent: *\\nDisallow: /a\\nAllow: /a/b", "https://x/a/b/c") -> True  (the longer rule wins)
    """
    # ----- Exercise 2: allowed -----
    raise NotImplementedError("Exercise 2 (allowed): not done yet")


# ==============================================================================
# PART 2 · THE LISTING PAGE: 48 graphics cards per page, plain HTML from the server.
#
# One card (simplified; open samples/listing_page1.html and search "pdt-item"):
#   <li class="pdt-item" data-id="AR202505270061" ...>
#     <h3 class="title-3"><a href="/fiche/PB00686694.html">ASRock AMD Radeon RX 9060 XT ...</a></h3>
#     <p class="desc">16 Go GDDR6 - HDMI/Dual-DisplayPort - PCI Express ...</p>
#     <div class="ratingClient"><a href="..."><span class="star-10"></span>5 avis</a></div>
#     <div class="price"></div>              <- EMPTY! But the price IS somewhere in the page: exercise 7
#   </li>
#
# The pages of the list (at the bottom of each page):
#   <ul class="pagination">
#     <li class="active"><span>1 (current)</span></li>         <- the page you are on: not a link
#     <li><a data-page="2" href=".../c4684/page2/">2</a></li> ...
# ==============================================================================

def rating_from_class(class_name):
    """Turn the CSS class of the stars into a rating out of 5.

    The stars of a card are a class "star-N": N is a number of HALF stars. So the rating is N / 2.
    Return: the rating as a float, or None if the class is not "star-" + a number.

    Examples:
        rating_from_class("star-10") -> 5.0
        rating_from_class("star-9")  -> 4.5
        rating_from_class("big")     -> None
        rating_from_class(None)      -> None
    """
    # ----- Exercise 3: rating_from_class -----
    raise NotImplementedError("Exercise 3 (rating_from_class): not done yet")


def count_from_text(text):
    """Read the number in a short text, like "5 avis" (5 reviews).

    Return: the number as an int. No number in the text: 0.
    Careful: in French, big numbers have a space inside ("1 234"), and this space is often a special
    invisible one: "\\xa0" or "\\u202f".

    Examples:
        count_from_text("5 avis")          -> 5
        count_from_text("1\\u202f234 avis") -> 1234
        count_from_text("")                -> 0
    """
    # ----- Exercise 4: count_from_text -----
    raise NotImplementedError("Exercise 4 (count_from_text): not done yet")


def listing_items(html):
    """Read all the cards of a listing page.

    Input:  the HTML of a listing page.
    Return: one dict per card, in the order of the page. Example (the first card of samples/listing_page1.html):
        {"id": "AR202505270061",                                   # the data-id of the card
         "name": "ASRock AMD Radeon RX 9060 XT Challenger 16GB OC",
         "url": "https://www.ldlc.com/fiche/PB00686694.html",     # a FULL url (the page gives "/fiche/...")
         "description": "16 Go GDDR6 - HDMI/Dual-DisplayPort - PCI Express (AMD Radeon RX 9060 XT)",
         "rating": 5.0,                                            # from the stars class (exercise 3); None if no stars
         "reviews": 5}                                             # from the "5 avis" text (exercise 4); 0 if none
    """
    # ----- Exercise 5: listing_items -----
    raise NotImplementedError("Exercise 5 (listing_items): not done yet")


def page_urls(html, category_url=CATEGORY_URL):
    """Find the URLs of ALL the pages of the list, from any one of them.

    Read the page numbers in the pagination. The last page is the biggest number. Careful: the page you are on is
    not a link, so on the LAST page, the biggest link is not the last page.
    Page 1 is `category_url`. Page N is `category_url` + "pageN/".
    Return: the list of all the page URLs, from page 1 to the last one.

    Examples:
        page_urls(<listing_page1.html>)    -> [".../c4684/", ".../c4684/page2/", ".../c4684/page3/", ".../c4684/page4/"]
        page_urls(<listing_page2.html>)    -> the same 4 URLs
        page_urls("<p>no pagination</p>")  -> [category_url]
    """
    # ----- Exercise 6: page_urls -----
    raise NotImplementedError("Exercise 6 (page_urls): not done yet")


def listing_prices(html):
    """Find the prices of the listing page, WITHOUT opening the 48 product pages.

    The price box of each card is empty. But open samples/listing_page1.html and search "969": the prices are in the
    page, in a JSON-LD block (a <script type="application/ld+json">) of type "ItemList", written for Google:
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": 1,
             "item": {"@type": "Product", "name": "...", "url": "https://www.ldlc.com/fiche/PB00686694.html",
                      "offers": {"@type": "Offer", "price": "969.95", "priceCurrency": "EUR", ...}}},
            ...]}
    Return: a dict {product url: price as a float}, for each product that has a price. No ItemList: {}.
    Skip a JSON-LD block that is not valid JSON.

    Example: listing_prices(<listing_page1.html>)["https://www.ldlc.com/fiche/PB00686694.html"] -> 969.95
    """
    # ----- Exercise 7: listing_prices -----
    raise NotImplementedError("Exercise 7 (listing_prices): not done yet")


# ==============================================================================
# PART 3 · THE PRODUCT PAGE: price, technical sheet, JSON-LD (open samples/product_PB00686694.html)
# ==============================================================================

def parse_price(text):
    """Turn a French price text into a float.

    LDLC writes the cents AFTER the euro sign, and puts spaces in many places (normal or invisible ones).
    Return: the price as a float, or None if the text is not a price.

    Examples:
        parse_price("969€ 95")        -> 969.95
        parse_price("1\\xa0129€95")     -> 1129.95
        parse_price("1 329,95 €")     -> 1329.95      (the usual French way)
        parse_price("969€")           -> 969.0
        parse_price("")               -> None
    """
    # ----- Exercise 8: parse_price -----
    raise NotImplementedError("Exercise 8 (parse_price): not done yet")


def main_price(html):
    """Find THE price of the product on its page.

    Careful: a product page shows many prices (the product, but also "similar products" at the bottom).
    The product's own price is the first element with the class "price" inside the box with the class
    "product-infoPrice".
    Return: the price as a float (use exercise 8), or None if there is no price.

    Example: main_price(<product_PB00686694.html>) -> 969.95
    """
    # ----- Exercise 9: main_price -----
    raise NotImplementedError("Exercise 9 (main_price): not done yet")


def spec_table(html):
    """Read the technical sheet of the product (the table with id "product-parameters").

    Return: a dict of dicts {section: {label: value}}.
    Example: spec_table(page)["Mémoire"]["Taille mémoire vidéo"]  -> "16 Go"

    The table uses ROWSPAN, so the rows do not all have the same number of cells:
        - 3 cells: a section name, a label, a value       -> a new section starts
        - 2 cells: a label, a value                       -> the same section as the row above
        - 1 cell:  a value                                -> one MORE value for the label above:
                                                             add it with ", " ("2 X DisplayPort Femelle, 1 X HDMI Femelle")
    Two traps:
        - many spaces inside the texts: "3290           MHz" must become "3290 MHz";
        - the value cell of "Marque" contains a hidden <label> that REPEATS the name ("ASRock ASRock"):
          the value must be "ASRock". Do not keep the text of <label> tags in the value cells.
    Look at the rows near "Sorties vidéo" and "Marque" in samples/product_PB00686694.html.
    """
    # ----- Exercise 10: spec_table -----
    raise NotImplementedError("Exercise 10 (spec_table): not done yet")


def jsonld_product(html):
    """Read the JSON-LD block of type "Product" of a product page.

    Return: a small dict, or None if the page has no "Product" block:
        {"name": "ASRock AMD Radeon RX 9060 XT Challenger 16GB OC",
         "gtin13": "4711581491205",
         "brand": "ASRock",            # in the JSON, "brand" is a dict with a "name"
         "price": 969.95,              # from "offers" (a dict, or a list: then use the first one), as a float
         "currency": "EUR",            # from "offers"
         "in_stock": True}             # True when the "availability" of "offers" ends with "InStock"
    """
    # ----- Exercise 11: jsonld_product -----
    raise NotImplementedError("Exercise 11 (jsonld_product): not done yet")


def first_number(text):
    """(Given.) The first number of a text, as an int: "16 Go" -> 16, "3290 MHz" -> 3290, None -> None."""
    match = re.search(r"\d+", text or "")
    return int(match.group()) if match else None


def product_record(html, url):
    """Put together everything we know about one product, from its page.

    Input:  the HTML of a product page, and its URL.
    Return: one flat dict. Example (samples/product_PB00686694.html):
        {"id": "PB00686694",                          # the code in the URL: ".../fiche/PB00686694.html"
         "name": "ASRock AMD Radeon RX 9060 XT Challenger 16GB OC",     # the main title (<h1>)
         "brand": "ASRock",                           # technical sheet: "Informations générales" > "Marque"
         "chipset": "AMD Radeon RX 9060 XT",          # technical sheet: "Chipset graphique" > "Chipset graphique"
         "memory_gb": 16,                             # technical sheet: "Mémoire" > "Taille mémoire vidéo" (a number)
         "boost_mhz": 3290,                           # technical sheet: "Chipset graphique" > "Fréquence boostée" (a number)
         "price": 969.95,                             # the price shown on the page (exercise 9)
         "price_jsonld": 969.95,                      # the price of the JSON-LD (exercise 11)
         "same_price": True,                          # True when the two prices are equal (False if one is missing)
         "url": url}
    Use exercises 9, 10 and 11 and the given function first_number.
    If something is missing in the page, its value is None: the function must never crash.
    """
    # ----- Exercise 12: product_record -----
    raise NotImplementedError("Exercise 12 (product_record): not done yet")


# ==============================================================================
# PART 4 · THE CRAWL: robots.txt -> listing pages -> product pages, with pauses.
# ==============================================================================

def make_session(user_agent=USER_AGENT):
    """(Given.) A Session with our honest User-Agent and French as the language."""
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent, "Accept-Language": "fr-FR,fr;q=0.9"})
    return session


def fetch_html(session, url, robots_text):
    """Download one page, politely, and return its HTML text.

    1. First ask robots.txt (exercise 2). If the URL is not allowed: raise a PermissionError, and do NOT send
       the request.
    2. Download the page with the session, with a timeout (TIMEOUT).
    3. If the server answers with an error (404, 500 ...): raise an HTTPError.
    4. Return the HTML text.
    """
    # ----- Exercise 13: fetch_html -----
    raise NotImplementedError("Exercise 13 (fetch_html): not done yet")


def crawl(session, robots_text, category_url=CATEGORY_URL, max_pages=MAX_PAGES, max_products=MAX_PRODUCTS,
          delay=DELAY_SECONDS):
    """Do the whole crawl and return the list of product records (exercise 12), in the order of the list.

    1. Download page 1 of the list. Find the other pages (exercise 6). Read at most `max_pages` pages in total.
    2. Collect the product URLs of these pages (exercise 5), in order, without duplicates.
    3. Download the first `max_products` product pages, and make one record per product.
    Use exercise 13 for every download, and wait `delay` seconds before every download except the first one.
    """
    # ----- Exercise 14: crawl -----
    raise NotImplementedError("Exercise 14 (crawl): not done yet")


# ==============================================================================
# PART 5 · ANALYSIS
# ==============================================================================

def price_table(records):
    """Make a table of the best deals: the price for each GB of video memory.

    Input:  a list of product records (exercise 12).
    Return: a pandas DataFrame with the columns name, chipset, memory_gb, price, eur_per_gb, where
            eur_per_gb = price / memory_gb, rounded to 2 decimals.
    Rules:
        - leave out the records with no price or no memory_gb;
        - sort by eur_per_gb, the smallest (the best deal) first;
        - the index must be 0, 1, 2 ... in the new order.
    """
    # ----- Exercise 15: price_table -----
    raise NotImplementedError("Exercise 15 (price_table): not done yet")
