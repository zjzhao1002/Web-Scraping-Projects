import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

login_url = "http://quotes.toscrape.com/login"

payload = {
    "username": "abcdef",
    "password": "123456"
}

response = requests.post(login_url, data=payload)
quotes_list = []

base_url = response.url
url = base_url
while url:
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all(attrs={'class':'quote'})
    for quote in quotes:
        text = quote.find(attrs={'class': 'text'}).text
        author = quote.find(attrs={'class': 'author'}).text
        quotes_list.append({'text': text, 'author': author})

    next_button = soup.find(attrs={'class': 'next'})
    page_url = next_button.find('a')['href'] if next_button else None
    if page_url == None:
        break
    url = base_url + page_url
    response = requests.get(url)
    print("Scraping ", url)
    sleep(2)

print(len(quotes_list))
df = pd.DataFrame(quotes_list)
df.to_csv("quotes.csv", index=False)