import re
import time
import datetime
import feedparser
import pandas as pd
from typing import List, Dict

def get_arxiv_update(keywords: List[str], new_only: bool=False) -> List[Dict]:
    feed_url = "https://rss.arxiv.org/rss/hep-ph"
    feed = feedparser.parse(feed_url)

    entries = feed.entries
    articles = []
    # print(type(entries[10]))
    for entry in entries:
        if new_only:
            if "Announce Type: new" in entry.description:
                articles.append({
                    'title': entry.title,
                    'authors': entry.author,
                    'link': entry.link
                })               
        else:
            articles.append({
                'title': entry.title,
                'authors': entry.author,
                'link': entry.link
            }) 
    if not keywords:
        result = articles
    else:
        result = []
        pattern = '|'.join(keywords)
        for i in range(len(articles)):
            if re.search(pattern, articles[i]['title']):
                result.append(articles[i])
    return result

if __name__ == "__main__":
    while True:
        keywords = []
        new_only = True
        today = str(datetime.date.today())
        result = get_arxiv_update(keywords=keywords, new_only=new_only)
        df = pd.DataFrame(result)
        df.to_csv(f"arxiv_{today}.csv", index=False)
        time.sleep(86400)