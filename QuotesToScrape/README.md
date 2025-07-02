# Quotes to Scrape
Quotes to Scrape is a website that lists quotes from famous people. 
It has many endpoints showing the quotes in many different ways, 
each of them including new scraping challenges for you, as described below.

| Endpoints            |                                                    |
| -------------------- | -------------------------------------------------- |
| Default              | Microdata and pagination                           |
| Scroll               | Infinite scrolling pagination                      |
| JavaScript           | JavaScript generated content                       |
| JavaScript (Delayed) | Same as JavaScript but with a delay (?delay=10000) |
| Tableful             | A table based messed-up layout                     |
| Login                | Login with CSRF token (Any user/password works)    |
| ViewStates           | An AJAX based filter form with ViewStates          |
| Random               | A single random quote                              |

The following data have been scraped:

- Quote Text
- Quote Author

The scraped results are same in the **quotes.csv**.

# Methods

## Default Quotes (Static Web Pages)
Source url: http://quotes.toscrape.com/

This is the most simple case. **Requests** and **BeautifulSoup** are sufficient to scrape it. 
To make it more interesting, a quote guessing game is implemented. 
4 random quotes are picked and one of them is displayed for question. 
User can guess the author from 4 choices.

## Scroll Quotes (Infinitely Scrolling Web Pages)
Source url: http://quotes.toscrape.com/scroll

To scroll the website, **Playwright** is used. 
It has a scroll function `mouse.wheel(deltaX, deltaY)`, so we can run it several time to reach the bottom of the website.

## JavaScript Quotes (Dynamic Web Pages)
Source url: http://quotes.toscrape.com/js/

A simple way to scrape this kind of website is using **Selenium** or **Playwright** to load the website in a webdriver.
In this case, **Playwright** has been used.

## JavaScript (Delayed) Quotes (Dynamic Web Pages with Long Delay)
Source url: http://quotes.toscrape.com/js-delayed/

It is similar to the previous one, but we set a long time to wait for loading.

## Tableful Quotes (Table-Predominant Web Pages)
Source url: http://quotes.toscrape.com/tableful/

Data are stored in a table. **Requests** and **BeautifulSoup** are sufficient to extract these data. 
The "Next" is invisible in this web page, but we can see the `href` in the response. 
So we can go to next page as usual.

## Login Quotes (User Credential Web Pages)
Source url: http://quotes.toscrape.com/login

This is a simple login page. We can use `requests.post` method to send the username and password to login. 

## Viewstate Quotes (Input Form Web Pages)
Source url: http://quotes.toscrape.com/search.aspx

In this page, we have to choose the author and tag to get a quote. 
After choosing the filter, we can see three parts in the payload: `author`, `tag` and `__VIEWSTATE`. 
We can loop over them to get all quotes.

## Random Quotes (Random Web Pages)
Source url: http://quotes.toscrape.com/random

A random quote is displayed in the page. We can make a number of requests until all quotes are scraped.
