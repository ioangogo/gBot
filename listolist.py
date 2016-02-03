"""Get items from Wikipedia: List of lists of lists

Call get_lists_cached() to retrieve the list. It will not be updated after the
first load (I don't imagine it's particularly critical to keep this data
current...)
"""

import json
import urllib.request
import re

list_re = re.compile(r'\* \[\[(Lists? of [\w ]+)\]\]')

URL='https://en.wikipedia.org/w/api.php?action=query&titles=List%20of%20lists%20of%20lists&prop=revisions&rvprop=content&format=json'

lists = []

def download_lolol(url=URL):
    with urllib.request.urlopen(URL) as conn:
        return json.loads(conn.read(102400).decode('utf8'))

def get_lists(data):
    pages = data['query']['pages']
    page = pages[list(pages.keys())[0]]
    pagerev = page['revisions'][0]
    text = pagerev['*']
    lines = text.split('\n')

    matches = []
    for line in lines:
        match = list_re.match(line)
        if match is not None:
            matches.append(match.group(1))
    return matches

def get_lists_cached():
    global lists
    if not lists:
        lists = get_lists(download_lolol())
    return lists

if __name__ == '__main__':
    L = get_lists_cached()
    import random
    for i in range(3):
        print(random.choice(L))
