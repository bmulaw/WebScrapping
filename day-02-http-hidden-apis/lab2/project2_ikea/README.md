# Project 2 · IKEA: the hidden API behind the search page

> 💼 **Real scenario:** a furniture price-comparison startup follows the prices of IKEA chairs, by color and by
> country. IKEA has no public API ... but its own website calls one, and your browser shows it to you.

🌐 **Website:** https://www.ikea.com/fr/fr/ (search for `chaise`)

## Your files

| File | What it is |
|---|---|
| `exercises.py` | **your work**: the settings at the top, then exercises 1 to 14 |
| `check.py` | tests your exercises **without internet** (it uses `samples/`) |
| `main.py` | the real program: it calls IKEA's hidden search API and writes `output/<query>.csv` |
| `samples/` | real answers from the website, saved. Open them to see what it sends back |

## How to work

1. **First, in your browser (15 min, no code):** find the API with DevTools, like in notebook 3, section 2. Answer questions 1 to 6 at the end of this file.
2. Do the exercises **in order**, in `exercises.py`. For each one: read what the function must do (the text under `def`), then replace `raise NotImplementedError(...)` with your code.
3. After each exercise, click Run ▶ on `check.py`: ✅ done · ❌ wrong (read the message) · ⬜ not done yet.
4. When everything is ✅, click Run ▶ on `main.py`. Then open `output/chaise.csv`. Run it again within a minute: this time the answers come from the cache (`data/cache/`).
5. Change the settings at the top of `main.py` and run it again: `COLOR = "noir"`, `SORT = "PRICE_LOW_TO_HIGH"`, then `QUERY = "lampe"`.

> Tip: to see what the API sends back, open `samples/search_chaise_fr.json` (VS Code: right-click → *Format Document*).

## Questions

**In the browser, before the exercises:**

1. Search `chaise` with DevTools open (**Fetch/XHR**, filter `sik.search`). Which call returns the products?
   Its **URL**, its **method**, and what it sends (**Payload** tab)?
2. In the **Preview** tab, find the path to the price of the first product.
3. Scroll down and click "Afficher plus". What new call appears? What does it send that the first call did not?
4. Type `cha` in the search box without pressing Enter. Which **second** API appears?
5. Open https://www.ikea.com/robots.txt **and** https://sik.search.blue.cdtapps.com/robots.txt.
   What does each say about search? Why may we call the API?
6. Notebook 3, section 4 removed the headers one by one. Which headers does this API really need?

**After the exercises:**

7. The API is undocumented. What can break, and how do the parsing exercises + `check.py` help you when it does?
8. `search_everything` asks `size=112` in one call instead of 5 calls of 24. Better for whom? Is there a limit?

✍️ **Your answers:**
