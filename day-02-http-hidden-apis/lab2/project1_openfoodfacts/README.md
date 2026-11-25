# Project 1 · Open Food Facts: a nutrition comparator

> 💼 **Real scenario:** a health app compares the breakfast cereals sold in France: sugar, fat, Nutri-Score.
> It needs clean data, every week, from a source it is allowed to use.

🌐 **Website:** https://world.openfoodfacts.org (open data, with an official API:
https://openfoodfacts.github.io/openfoodfacts-server/api/)

## Your files

| File | What it is |
|---|---|
| `exercises.py` | **your work**: the settings at the top, then exercises 1 to 12 |
| `check.py` | tests your exercises **without internet** (it uses `samples/`) |
| `main.py` | the real program: it calls the real Open Food Facts API and writes `output/products.csv` |
| `samples/` | real answers from the website, saved. Open them to see what it sends back |

## How to work

1. In `exercises.py`, put **your e-mail** in `USER_AGENT` (Open Food Facts asks for it).
2. Do the exercises **in order**, in `exercises.py`. For each one: read what the function must do (the text under `def`), then replace `raise NotImplementedError(...)` with your code.
3. After each exercise, click Run ▶ on `check.py`: ✅ done · ❌ wrong (read the message) · ⬜ not done yet.
4. When everything is ✅, click Run ▶ on `main.py`. Then open `output/products.csv`.
5. Change the settings at the top of `main.py` (`CATEGORY`, `PAGES`, `IMAGES`) and run it again. Category names: https://world.openfoodfacts.org/categories

> Tip: to see what the API sends back, open `samples/product_3017624010701.json` (VS Code: right-click → *Format Document*).

## Questions

1. The API answers **200** for barcode `0000000000000`. Why is it a problem if you only check the status code?
2. Why do retries apply to 429 and 503, but **not** to 400 or 404?
3. Exercise 11 gets the name and the brand from the HTML too. Give two reasons to prefer the API.
4. robots.txt of Open Food Facts says `Disallow: /api`. Why may your program still call the API?

✍️ **Your answers:**
