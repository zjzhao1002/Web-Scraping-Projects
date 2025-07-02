import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
from random import choice, sample

base_url = "https://quotes.toscrape.com/"

page_url = "page/1/"

quotes_list = []

while page_url:
    page = requests.get(f"{base_url}{page_url}")
    soup = BeautifulSoup(page.text, "html.parser")
    quotes = soup.find_all(attrs={'class':'quote'})
    for quote in quotes:
        text = quote.find(attrs={'class': 'text'}).text
        author = quote.find(attrs={'class': 'author'}).text
        quotes_list.append({'text': text, 'author': author})

    next_button = soup.find(attrs={'class': 'next'})
    page_url = next_button.find('a')['href'] if next_button else None
    sleep(2)

quotes_for_choice = sample(quotes_list, 4)
quote_for_question = choice(quotes_for_choice)
print("Here is a quote: ")
print(quote_for_question['text'])
print("This quote is said by one of the following persons: ")
i = 1
for quote in quotes_for_choice:
    print(i, quote['author'])
    i += 1

answer = input("Who said this quote? Please input a number: ")
if int(answer) not in range(1, 5):
    raise Exception("Please input a number from 1 to 4")

if quotes_for_choice[int(answer)-1]['author'] == quote_for_question['author']:
    print("Congratulations! You got it right!")
else:
    for i in range(len(quotes_for_choice)):
        if quotes_for_choice[i]['author'] == quote_for_question['author']:
            print(f"Sorry, you are wrong. The correction answer is {i+1} {quote_for_question['author']}")


with open("quotes.csv", 'w', encoding='utf-8') as f:
    csvwriter = writer(f)
    for quote in quotes_list:
        csvwriter.writerow([quote['text'], quote['author']])