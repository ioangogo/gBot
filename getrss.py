import feedparser
import time
import datetime
global lastcheck
import html.parser
html_parser = html.parser.HTMLParser()
from time import sleep
lastcheck = datetime.datetime.now()
print("Get rss Loaded")
def fetchitems(url):
    msg = []
    feedcount=0
    feed = feedparser.parse(url)
    print(lastcheck)
    try:
        for item in feed.entries:
            if datetime.datetime.fromtimestamp(time.mktime(item.published_parsed)) >= lastcheck:
                msg.append("New Content By " + item.author + ": " + html_parser.unescape(item.title) + " " + html_parser.unescape(item.link))
                feedcount += 1
