from playwright.sync_api import sync_playwright
import pandas as pd
import time

pw = sync_playwright().start()

browser = pw.firefox.launch(
    headless=False
)

page = browser.new_page()
page.goto("http://quotes.toscrape.com/scroll")

for i in range(30):
    page.mouse.wheel(0,25000)
    time.sleep(2)

# time.sleep(15)

quotes = page.locator(".quote").all()
quotes_list =[]

for quote in quotes:
    text = quote.locator(".text").text_content()
    author = quote.locator(".author").text_content()
    quotes_list.append({
        "quote": text,
        "author": author
    })

df = pd.DataFrame(quotes_list)
df.to_csv("quotes.csv", index=False)

print(len(quotes))

browser.close()