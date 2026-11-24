# Bonus · Shopify: one hidden API, thousands of shops

> 💼 **Real scenario:** thousands of online shops run on **Shopify**, and every one of them answers at the same address:
> `https://<shop>/products.json?limit=250&page=1`. One program works for all of them.

🌐 **Try it in your browser:** https://www.percko.com/products.json?limit=2

## Your files

| File | What it is |
|---|---|
| `exercises.py` | **your work**: the settings at the top, then exercises 1 to 4 |
| `check.py` | tests your exercises **without internet** (it uses `samples/`) |
| `main.py` | the real program: it reads all the products of one shop and writes `output/<shop>.csv` |
| `samples/` | real answers from the website, saved. Open them to see what it sends back |

## How to work

1. Do the exercises **in order**, in `exercises.py`. For each one: read what the function must do (the text under `def`), then replace `raise NotImplementedError(...)` with your code.
2. After each exercise, click Run ▶ on `check.py`: ✅ done · ❌ wrong (read the message) · ⬜ not done yet.
3. When everything is ✅, click Run ▶ on `main.py`. Then open `output/www.percko.com.csv`.
4. To try the other shop, set `SHOP = "www.leslipfrancais.fr"` at the top of `main.py` and run it again.

## Careful

- Shopify limits requests **per IP address, across all its shops**: after a few fast requests it answers
  `429` (with `Retry-After: 60`). Run `main.py` once, not in a loop.
- `main.py` only accepts the two shops we checked (robots.txt allows `/products.json`, and their terms do not forbid
  robots, in November 2026). Many Shopify shops **forbid robots in their terms** (Kith, Allbirds, Death Wish Coffee,
  Jimmy Fairly): read them before you add a shop.
