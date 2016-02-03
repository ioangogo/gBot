import feedparser
import time
global lastcheck
import html.parser
html_parser = html.parser.HTMLParser()
from time import sleep
lastcheck = time.gmtime()
print("Get rss Loaded")
def fetchitems(url):
    msg = []
    feed = feedparser.parse(url)
    try:
        for item in feed.entries:
            if item.published_parsed >= lastcheck:
                msg.append("New Content By " + item.author + ": " + html_parser.unescape(item.title) + " " + html_parser.unescape(item.link))
            else:
                break
    except Exception as e:
        msg=[e]
    return msg

def rssfunc(q, feeds):
    q.queue.clear()
    while True:
        for stuff in feeds:
            q.put(fetchitems(stuff))
        lastcheck = time.gmtime()
        sleep(60)
        q.queue.clear()

