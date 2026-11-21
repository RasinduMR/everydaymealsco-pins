# Everyday Meals Co. – Pinterest pin kit

Assets and tools for making Pinterest pins for https://www.pinterest.com/everydaymealsco/ .
Pins send people to https://everydaymealsco.netlify.app (free recipe pages, the free 7-dinner guide, and the 4 recipe ebooks on Gumroad).

## Files
- `recipes.json` – all 100 recipes in the 4 books (book, id, name, chips like "About $9" or "~45g protein", times, photo). `page_url` is set for the 35 recipes that have a free page on the site; only those have ingredients/steps here.
- `photos/` – one photo per recipe (`b{book}_{id}.jpg`, e.g. `b3_01.jpg`) and the 4 book covers (`b{book}_cover.jpg`). Photos with id 25 are full resolution; the others are about 465 px wide, so use them in collages, lists, cards and week plans, not full-bleed hero pins.
- `logo.png` – transparent brand logo.
- `pin_kit.py` – renders 1000x1500 pins with headless Chrome. Styles: `heroA`, `heroA2` (full-res photo only), `roundup` (collage + big number), `infolist` (10 rows), `magazine` (book cover photo), `card` (recipe card, needs a recipe with a page), `cost` (budget recipes), `weekplan` (Mon–Sun dinner plan). Run `PIN_OUT=/tmp/pins python3 pin_kit.py` for a self-test.
- `pins_log.json` – every pin already posted or scheduled. Check it before making new pins and add new ones to it.

## Links
- Single-recipe pins → that recipe's `page_url`.
- Free guide / week-plan pins → https://everydaymealsco.netlify.app/#free
- Collection / book pins → https://everydaymealsco.netlify.app/#books

## Boards
Easy Dinner Recipes for Family · 30 Minute Dinner Recipes · Easy Ground Beef Recipes · Easy Chicken Dinner Recipes · Easy Crockpot Meals · Make Ahead Freezer Meals · Budget Meals for Families · Healthy Dinner Recipes · High Protein Meals · Meal Prep Ideas for the Week · Christmas Dinner Recipes

## Rules
- Fresh designs only (never re-upload an identical image). Vary the style so no two pins in a row look alike.
- Every pin gets a keyword-rich title, a 2–3 sentence description, a link, a board and alt text.
- Do not tick "Mark as AI-Modified" (owner's choice).
