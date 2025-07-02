import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/random"

quotes_set = set()
quotes_list = []

while len(quotes_set) < 100:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    quote = soup.find(attrs={'class': 'quote'})
    text = quote.find(attrs={'class': 'text'}).text
    author = quote.find(attrs={'class': 'author'}).text
    result = {'text': text, 'author': author}
    # print(result)
    if quote not in quotes_set:
        quotes_set.add(quote)
        quotes_list.append(result)
    print(len(quotes_set))

# print(result)
print(len(quotes_list))
df = pd.DataFrame(quotes_list)
df.to_csv("quotes.csv", index=False)