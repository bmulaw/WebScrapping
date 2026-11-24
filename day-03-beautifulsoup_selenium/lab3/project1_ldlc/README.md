# Project 1 · LDLC: BeautifulSoup on a real shop

> 💼 **Real scenario:** a gamer association wants the best graphics card for its budget: price, video memory,
> frequency. LDLC (a big French computer shop) has no API for that ... but its pages are plain server HTML:
> **requests + BeautifulSoup** are enough. No browser needed (and you will check that this is true).

🌐 **Website:** https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/: press `Ctrl+U`
(the HTML the server sends) and search `pdt-item`. Open a product, scroll to *Fiche technique*. Then open
https://www.ldlc.com/robots.txt.

## What `main.py` does

```
robots.txt ──(your own wildcard matcher)──▶ allowed?
     │
listing page 1 ──▶ 48 cards (name, link, stars, reviews) + the pagination ──▶ pages 2, 3, 4
     │          └──▶ the price? the card's <div> is EMPTY ... but the JSON-LD "ItemList" has all 48 prices
     ▼  for each product link: allowed? pause 3 s
product page ──▶ price (HTML) + technical sheet (a table with rowspan) + JSON-LD ──▶ one row ──▶ €/GB table
```

## Your files

| File | What it is |
|---|---|
| `exercises.py` | **your work**: the settings at the top, then exercises 1 to 15 |
| `check.py` | tests your exercises **without internet** (it uses `samples/`) |
| `main.py` | the real program, on the real LDLC website: writes `output/graphics_cards.csv` |
| `samples/` | real pages of the website, saved (scripts removed). Open them in VS Code |

## How to work

1. Do the exercises **in order**, in `exercises.py`. For each one: read the text under `def`, then replace
   `raise NotImplementedError(...)` with your code.
2. After each exercise, click Run ▶ on `check.py`: ✅ done · ❌ wrong (read the message) · ⬜ not done yet.
3. When everything is ✅, click Run ▶ on `main.py`. Then change `PAGES` and `PRODUCTS` at its top.

> Tip: in `samples/product_PB00686694.html`, search `product-parameters` (the technical sheet) and `Sorties vidéo`:
> look at the `rowspan` and at the row with ONE cell.

## Questions

1. Open the listing page in Chrome: every card shows a price. In `samples/listing_page1.html` (what `requests`
   receives), `<div class="price">` is empty. On the real page, press `Ctrl+U` and search `969€`: where is the price,
   and who puts it in the `<div>`? Did we need a browser, or another API call, to get it?
2. `urllib.robotparser` answers `True` for `https://www.ldlc.com/fiche/PB1/stocks/`. Your `allowed()` answers
   `False`. Which one is right, and why?
3. The technical sheet has `rowspan`. What would a scraper that "takes cell 1 as the label and cell 2 as the value"
   store for the row `1 X HDMI Femelle`?
4. The price is in the HTML **and** in the JSON-LD. Which one would you trust in a scraper that runs every day? Why
   compare both?
5. `star-9` = 4.5 stars. Why do sites encode data in CSS classes, and why is it fragile for us?

✍️ **Your answers:**

