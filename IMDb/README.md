# IMDb
IMDb, historically known as the Internet Movie Database, 
is an online database of information related to films, television series, podcasts, home videos, video games, 
and streaming content online – including cast, production crew and biographies, plot summaries, trivia, ratings, and fan and critical reviews.

# Method
The **Selenium** and **Chrome web driver** are used to load the website. 
**BeautifulSoup** is used to find data in the page. 
The following data of movies are scraped:
* Title
* Year
* Duration
* Retriction Level
* Rating
* Votes

A script is used to clean data. The final results are stored in the **imdb_clean.csv** file.
