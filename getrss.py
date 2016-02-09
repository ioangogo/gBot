import feedparser
import time
import datetime
lastcheck = datetime.datetime.now()
import html.parser
html_parser = html.parser.HTMLParser()
from time import sleep
import requests
import traceback


headers = {
    'User-Agent': 'Ibot: Ioans bot',
}

print("Get rss Loaded")
def downloadtxt(url):
    page = requests.get(url, headers=headers)
    return page.text
def fetchitems(url, prevcheck):
    msg = []
    feedcount=0
    feed = feedparser.parse(downloadtxt(url))
    try:
        for item in feed.entries:
            if datetime.datetime.fromtimestamp(time.mktime(item.published_parsed)) >= prevcheck:
                msg.append("New " + feed.feed.title + " Content: " + html_parser.unescape(item.title) + " " + html_parser.unescape(item.link))
                print("Published: " + str(datetime.datetime.fromtimestamp(time.mktime(item.published_parsed))) + " Last Checked: " + str(prevcheck))
                feedcount += 1
            else:
                break
    except Exception as e:
        traceback.print_exc()
    return msg


def rssfunc(q, feeds):
    global lastcheck
    while True:
        returnmsg=[]
        print("Feed Fetch Start")
        for stuff in feeds:
            returnmsg += fetchitems(stuff, lastcheck)
        q.put(returnmsg)
        print("Feed Fetch Done")
        lastcheck = datetime.datetime.now()
#        print(str(lastcheck))
        sleep(120)
