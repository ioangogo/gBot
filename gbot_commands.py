import urllib.request
from lxml import html
from html import unescape
import json
import random
import requests
import lolol
import traceback
import randwords

def smug(bot):
    """be rude"""
    msg = bot.info['msg'].replace(" ","")
    s = "Fuck you, "
    if (msg not in bot.usrlist) or (str.lower(bot.nick) in str.lower(bot.info['msg'])) or bot.info['msg'].isspace():
        s += bot.info['user']
    else:
        s += msg
    s += "! :]"
    bot.say(s)
def swag(bot):
    bot.say("out of ten!")
def norris(bot):
    """Chuck"""
    msg = bot.info['msg'].split()
    url = "http://api.icndb.com/jokes/random"
    if(len(msg) > 0):
        url += "?firstName=" + msg[0] + "&lastName="
    if(len(msg) > 1):
        url += msg[1]
    req = urllib.request.urlopen(url, timeout=2)
    resp = req.read()
    req.close()
    joke = json.loads(resp.decode('utf8'))
    bot.say(unescape(joke['value']['joke']).replace("  ", " "))
def bacon(bot):
    """give bacon"""
    msg = bot.info['msg'].replace(" ","")
    if(msg in bot.usrlist):
        bot.say("\001ACTION gives " + msg + " a delicious strip of bacon as a gift from " + bot.info['user'] + "! \001")
    else:
        bot.say("\001ACTION gives " + bot.info['user'] + " a delicious strip of bacon.  \001")
def beer(bot):
    """give beer"""
    msg = bot.info['msg'].replace(" ","")
    if(msg in bot.usrlist):
        bot.say("\001ACTION gives " + msg + " a foaming pint of beer from " + bot.info['user'] + "! \001")
    else:
        bot.say("\001ACTION gives " + bot.info['user'] + " foaming pint of beer.  \001")
def coffee(bot):
    """give coffee"""
    msg = bot.info['msg'].replace(" ","")
    if(msg in bot.usrlist):
        user = msg
    else:
        user = bot.info['user']

    actions = [
        "grabs the coffee funnel and advances toward %s",
        "offers %s a fresh espresso",
        "coffees %s",
        "pours coffee into %s",
        ]
    action_template = random.choice(actions)
    action = action_template % user
    bot.say("\001ACTION " + action + " \001")
def lolol_cmd(bot):
    """suggest some nice lists"""
    msg = bot.info['msg'].replace(" ","")
    if(msg in bot.usrlist):
        user = msg
    else:
        user = bot.info['user']
    ITEM_COUNT = 5

    try:
        lists = lolol.get_lists_cached()
    except Exception:
        traceback.print_exc()
        lists = ["Lists of fruits", "Lists of transistor types", "Lists of reasons why !list is annoying"]

    items = [random.choice(lists) for i in range(ITEM_COUNT)]

    # Downcase the first letter, it just looks nicer
    items = ["l" + i[1:] for i in items]

    bot.say("A few ideas for " + user + ": " + ", ".join(items))
def jobebot(bot):
    """misread stuff"""
    word1 = randwords.get_random_word('words')
    word2 = randwords.get_random_word('words')
    bot.say("I read %s as %s" % (word1, word2))
def enhanoxbot(bot):
    """ponder food"""
    word1 = randwords.get_random_word('foods')
    word2 = randwords.get_random_word('foods')
    if word1.endswith("s"):
        phrase = "I wonder if %s go with %s..." % (word1, word2)
    else:
        phrase = "I wonder if %s goes with %s..." % (word1, word2)
    bot.say(phrase)
def listusr(bot):
    """how many users?"""
    bot.say("I reckon there are " + str(len(bot.usrlist)) + " users!")
    print(bot.usrlist)
def btc(bot):
    """BTC conversion rates"""
    money = 0
    cur = 'USD'
    msg = bot.info['msg'].split()
    url = "https://api.bitcoinaverage.com/ticker/global/all"
    req = urllib.request.urlopen(url)
    resp = req.read()
    data = json.loads(resp.decode('utf8'))
    if(len(msg) > 0):
        if(msg[0] in data):
            cur = msg[0]
    bot.say(bot.info['user'] + ": 1 BTC = " + str(data[cur]['ask']) + " " + cur)
def eightball(bot):
    """A 8 ball"""
    responses = ["It is certain","It is decidedly so","Without a doubt","Yes"," definitely","As I see it"," yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","My sources say no","Outlook not so good","Very doubtful"]
    msg = random.choice(responses)
    bot.say(msg)
def wisdom(bot):
    """fake Chopra quotes"""
    page = requests.get('http://wisdomofchopra.com/iframe.php')
    tree = html.fromstring(page.content)
    quote = tree.xpath('//table//td[@id="quote"]//header//h2/text()')
    bot.say(quote[0][1:-3])
def helpcmd(bot):
    """this help"""
    lines = sorted(list(cmdlist.keys()))
    for i in lines:
        function = cmdlist[i]
        helptext = function.__doc__
        if helptext:
            text = "%s: %s" % (i, helptext)
        else:
            text = i
        bot.notice(text, channel=bot.info['user'])

cmdlist ={
    "!smug" : smug,
    "!swag" : swag,
    "!cn" : norris,
    "!bacon" : bacon,
    "!users" : listusr,
    "!btc" : btc,
    "!8ball" : eightball,
    "!wisdom" : wisdom,
    "!beer" : beer,
    "!coffee" : coffee,
    "!list" : lolol_cmd,
    "!jobebot" : jobebot,
    "!enhanoxbot" : enhanoxbot,
    "!help": helpcmd,
}
