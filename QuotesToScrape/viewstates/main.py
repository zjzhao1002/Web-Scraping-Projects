import requests
import pandas as pd 
from bs4 import BeautifulSoup

def get_author(response):
    soup = BeautifulSoup(response.text, "html.parser")
    viewstate = soup.find("input", id="__VIEWSTATE").get("value")
    items = soup.find("select", id="author").find_all("option")[1:]
    for item in items:
        author = item.get("value")
        yield {"author": author, "__VIEWSTATE": viewstate}

def get_tag(response, author):
    soup = BeautifulSoup(response.text, "html.parser")
    viewstate = soup.find("input", id="__VIEWSTATE").get("value")
    items = soup.find("select", id="tag").find_all("option")[1:]
    for item in items:
        tag = item.get("value")
        yield {"author": author, "tag": tag, "__VIEWSTATE": viewstate}

def get_data(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())
    quotes = soup.find_all(attrs={'class':'quote'})
    for quote in quotes:
        text = quote.find(attrs={'class': 'content'}).text
        author = quote.find(attrs={'class': 'author'}).text
        yield {"text": text, "author": author}


def main():
    base_url = "http://quotes.toscrape.com/"
    search_url = "search.aspx"
    filter_url = "filter.aspx"

    response = requests.get(base_url+search_url)
    quote_list = []
    quote_set = set()
    for author in get_author(response):
        author_response = requests.post(base_url+filter_url, data=author)
        for tag in get_tag(author_response, author['author']):
            quote_response = requests.post(base_url+filter_url, data=tag)
            for data in get_data(quote_response):
                if data['text'] not in quote_set:
                    quote_set.add(data['text'])
                    quote_list.append(data)

    df = pd.DataFrame(quote_list)
    df.to_csv("quotes.csv", index=False)

if __name__ == "__main__":
    main()