import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://quotes.toscrape.com"

page_url = "/tableful/page/1/"

quotes_list = []

while page_url:
    url = base_url+page_url
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")
    quotes = soup.find_all("td", {"style": "padding-top: 2em;"})
    for quote in quotes:
        text = quote.text
        text_split = str(text).split("Author:")
        quote_text = text_split[0].strip()
        author = text_split[1].strip()
        quotes_list.append({
            "text": quote_text,
            "author": author
        })

    buttons = soup.find_all("a", href=True)
    for button in buttons:
        if "Next" in str(button.text):
            page_url = button['href']
            break
        else: 
            page_url = None
    print(page_url)

print(len(quotes_list))
df = pd.DataFrame(quotes_list)
df.to_csv("quotes.csv", index=False)        