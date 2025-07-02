from playwright.sync_api import sync_playwright
import pandas as pd
import time

pw = sync_playwright().start()

browser = pw.firefox.launch(
    headless=False, 
    slow_mo=2000
)

base_url = "http://quotes.toscrape.com"
page_url = "/js-delayed/page/1/"

quotes_list = []
page = browser.new_page()

while page_url:
    url = base_url + page_url
    page.goto(url)

    page.wait_for_selector("#quotesPlaceholder", timeout=10000)
    quotes = page.locator(".quote").all()

    for quote in quotes:
        text = quote.locator(".text").text_content()
        author = quote.locator(".author").text_content()
        quotes_list.append({
            "quote": text,
            "author": author
        })
    
    try:
        next_button = page.locator(".next")
        page_url = next_button.get_by_role("link").get_attribute("href") if next_button else None
        time.sleep(2)
    except:
        page_url = None
        page.close()

df = pd.DataFrame(quotes_list)
df.to_csv("quotes.csv", index=False)

print(len(quotes_list))

browser.close()