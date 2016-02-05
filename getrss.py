import feedparser
import time
import datetime
global lastcheck
import html.parser
html_parser = html.parser.HTMLParser()
from time import sleep
lastcheck = datetime.datetime.now()
print("Get rss Loaded")
import urllib


headers = {
    'User-Agent': 'Ibot: Ioans bot',
}

def downloadtxt(url):
    getstuff = urllib.request.openurl(url)
    return getstuff
def fetchitems(url):
    msg = []
    feedcount=0
    feed = feedparser.parse(url)
    print(lastcheck)
    try:
        for item in feed.entries:
            if datetime.datetime.fromtimestamp(time.mktime(item.published_parsed)) >= lastcheck:
                msg.append("New Content By " + item.author + ": " + html_parser.unescape(item.title) + " " + html_parser.unescape(item.link))
                print("Published: " + datetime.datetime.fromtimestamp(time.mktime(item.published_parsed)) + " Last Checked: " + lastcheck)
                feedcount += 1
            else:
                break
    except Exception as e:
        print(e)
    return msg


def rssfunc(q, feeds):
    while True:
        returnmsg=[]
        print("Feed Fetch Start")
        for stuff in feeds:
            returnmsg += fetchitems(stuff)
#        print(returnmsg)
        q.put(returnmsg)
        print("Feed Fetch Done")
        lastcheck = datetime.datetime.now()
        sleep(120)
