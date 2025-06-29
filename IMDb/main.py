import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from csv import writer
import time

url = "https://www.imdb.com/chart/top/"

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    'Language': 'en-US'
    }

chrome_driver_path = "/Users/zjzhao/python_works/web_scraping_projects/project3/chromedriver-mac-arm64/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument(f"--user-agent={headers['User-Agent']}")
options.add_argument(f"--lang={headers['Language']}")

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
driver.get(url)
time.sleep(10)
page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')

movies = soup.select('h3.ipc-title__text.ipc-title__text--reduced')
movie_titles = []
for movie in movies:
    movie_titles.append(movie.get_text())

movie_titles = movie_titles[1:251]

all_metadata = soup.select('div.sc-dc48a950-7.hMHetG.cli-title-metadata')
year = []
duration = []
restriction = []
for metadata in all_metadata:
    ydr = metadata.find_all(attrs={'class': 'sc-dc48a950-8'})
    if len(ydr) == 3:
        year.append(ydr[0].get_text())
        duration.append(ydr[1].get_text())
        restriction.append(ydr[2].get_text())
    if len(ydr) == 2:
        year.append(ydr[0].get_text())
        duration.append(ydr[1].get_text())
        restriction.append('none')


ratings = soup.find_all(attrs={'class': 'ipc-rating-star--rating'}) 
ratings_list = []
for rating in ratings:
    ratings_list.append(rating.get_text())

votes = soup.find_all(attrs={'class': 'ipc-rating-star--voteCount'})
votes_list = []
for vote in votes:
    votes_list.append(vote.get_text())    

with open("imdb.csv", 'w', encoding='utf-8') as f:
    csvwriter = writer(f)
    for i in range(len(movie_titles)):
        csvwriter.writerow([movie_titles[i], year[i], duration[i], restriction[i], ratings_list[i], votes_list[i]])

