# Project 3 · Coolblue: sitemaps + JSON-LD

> 💼 **Real scenario:** a price-tracking service follows the smartphones and laptops sold by Coolblue (a big Dutch
> electronics shop): price, stock, rating. No API ... but the shop gives robots two things: **sitemaps** (the list of
> all its product pages) and **JSON-LD** (the product data, in every page, for Google).

🌐 **Website:** https://www.coolblue.nl/en: open a product, e.g.
https://www.coolblue.nl/en/product/935188/apple-iphone-15-128gb-black.html, press `Ctrl+U` and search `ld+json`.
Then open https://www.coolblue.nl/robots.txt and look at the `Sitemap:` lines at the end.

## What `main.py` does

```
robots.txt ──"Sitemap:" lines──▶ sitemap INDEX (674 category sitemaps)
                                     │ choose one: ".../2093_mobiele-telefoons.xml"
                                     ▼
                                 sitemap URLSET (440 product URLs)
                                     │ for each URL: robots.txt allowed? pause 3 s
                                     ▼
                                 product page (1.5 MB of HTML) ──▶ JSON-LD blocks ──▶ Product ──▶ one row
```

## Your files

| File | What it is |
|---|---|
| `exercises.py` | **your work**: the settings at the top, then exercises 1 to 10 |
| `check.py` | tests your exercises **without internet** (it uses `samples/`) |
| `main.py` | the real program: it follows the pipeline above on the real Coolblue website and writes `output/<category>.csv` |
| `samples/` | real answers from the website, saved. Open them to see what it sends back |

## How to work

1. Do the exercises **in order**, in `exercises.py`. For each one: read what the function must do (the text under `def`), then replace `raise NotImplementedError(...)` with your code.
2. After each exercise, click Run ▶ on `check.py`: ✅ done · ❌ wrong (read the message) · ⬜ not done yet.
3. When everything is ✅, click Run ▶ on `main.py` (10 phones). Then open `output/mobiele-telefoons.csv`.
4. Change the settings at the top of `main.py` and run it again: `CATEGORY = "laptops"`, `LIMIT = 5`.

> Tip: open `samples/robots.txt` (the end), `samples/sitemap_index_en.xml`, and search `ld+json` in `samples/product_892008.html`.

## Questions

1. Coolblue answers **403** to `python-requests/2.34` but **200** to
   `Mozilla/5.0 (compatible; ESILV-Lab-Advanced/1.0; educational use)`. Why is the second one still honest?
   Why must you never use a real browser's User-Agent instead?
2. robots.txt contains `Disallow: /aanmelding/*`, but `allowed(robots, ".../aanmelding/x", ...)` returns `True`.
   Why? How would you protect your crawler?
3. Why is JSON-LD more stable than CSS selectors on the visible price?
4. The page shows 3 ratings (9/10, 9.1/10, 3.8/5). Which one is the phone's? What would a careless scraper store?
5. 440 phones × 1.5 MB × a 3 s pause: how long, how much data? Would you crawl them all every hour?

✍️ **Your answers:**
