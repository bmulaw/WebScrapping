# Project 2 · The Souled Store: product pages with Selenium, then the hidden API

> 💼 **Real scenario:** a merchandising start-up follows the stock of The Souled Store (a big Indian pop-culture
> shop): which sizes are sold out, which are almost gone, at what price. On a product page, `requests` gets the
> title ... but **no price and no sizes**: they arrive later, with JavaScript. You drive a real Chrome with
> **Selenium**, find the calls behind the page with the **Chrome DevTools Protocol** ... and then use them directly.

🌐 **Website:** https://www.thesouledstore.com/product/solids-inkstone-oversized-polos: look at the sizes (one is
crossed out), click "Product Description". Open DevTools ▸ Network ▸ Fetch/XHR and reload: find `pricing` and
`inventory`. Then press `Ctrl+U`: is the price in the HTML?

(The lesson notebook used the **listing** page of the same shop. This project is about the **product** pages.)

## What `main.py` does

```
A. Chrome ──▶ one product page
     ├─ wait for the price                        ₹ 1499
     ├─ read the sizes                            XXS sold out · XS only 1 left · S ... in stock
     ├─ click "Product Description", read it
     └─ network log (CDP) ──▶ GET .../product/<slug>/pricing   and   GET .../product/<slug>/inventory
                              + their answers, read from Chrome ──▶ page and API agree?
B. requests ──▶ the same 2 calls for 5 products ──▶ output/stock_report.csv
```

## Your files

| File | What it is |
|---|---|
| `exercises.py` | **your work**: the settings at the top, then exercises 1 to 13 (parts A, B, C, D) |
| `check.py` | tests your exercises **without internet**: parts A and B start Chrome on a LOCAL COPY of a product page (`samples/local_product_page.html` + a local API with the real answers) |
| `main.py` | the real program: a real product page in Chrome, then the real API |
| `samples/` | `raw_product_page.html` (what requests gets), `rendered_product_page.html` (what Chrome shows), `performance_log.json` (Chrome's network log on the real page), `pricing_*.json` and `inventory_*.json` (real API answers) |

## How to work

1. Do the exercises **in order**. After each one, click Run ▶ on `check.py`. The first run can take ~30 s:
   Selenium downloads the chromedriver that matches your Chrome (once).
2. When everything is ✅, click Run ▶ on `main.py`. Set `HEADLESS = False` at its top to **watch** Chrome.
3. Change `PRODUCT` (a slug from the website) and `HOW_MANY` at the top of `main.py` / `exercises.py`, and run again.

## Questions

1. Open `samples/raw_product_page.html` and `samples/rendered_product_page.html`. What is in both? What is only in
   the second one? Why?
2. In `read_sizes`, the size "S" has a `<section>` with the text "12 Left", but your function returns `"left": None`.
   Why? Is it a bug or a feature?
3. The size list has the class `product-variant-module__V1ijmq__sizelist` **and** `sizelist`. Which one did you use,
   and why?
4. Clicking "Product Description" closes "Product Details". Where is the text of a closed section? What does this
   mean for a scraper?
5. Part D gets the stock of 5 products in ~10 small calls, without a browser. How long would the browser need
   for 100 products? Which one is lighter for the shop?
6. `api.thesouledstore.com/robots.txt` says `Allow: /`. Is that enough to use the API? What else did we check?

✍️ **Your answers:**

