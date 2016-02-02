def fetchitems(url):
    msg = []
    feed = feedparser.parse(url)
    for item in feed.entries:
        if item.published_parsed > lastcheck:
            msg.append("New Content By " + item.author + ": " + html_parser.unescape(item.title) + " " + html_parser.unescape(item.link))
            continue
        else:
            break
        break
    return msg

def rssfunc(q, feeds):
    while True:
        for stuff in feeds:
            q.put(fetchitems(stuff))
        lastcheck = time.gmtime()
        sleep(60)
