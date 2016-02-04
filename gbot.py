#!/usr/bin/env python3

import socket
import string
from lxml import html
import requests
import json
import getrss
import importlib
import queue
import threading
import traceback
import re
welcomemsgdone = False
import cfg
import gbot_commands
# this thing is global so it only has to be compiled into a regex object once
URLpattern = re.compile(r"((http(s)?):\/\/|(www\.)|(http(s)?):\/\/(www\.))[?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)")


HOST = cfg.HOST
PORT = cfg.PORT
NICK = cfg.NICK
IDENT = cfg.IDENT
REALNAME = cfg.REALNAME
CHANNEL = cfg.CHANNEL
KEY = cfg.KEY
feeds = cfg.FEEDS

CONNECTED = 0

headers = {
    'User-Agent': 'Ibot: Ioans bot',
}

readbuffer = ""


s=socket.socket( )
s.connect((HOST, PORT))

s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))

def joinch(line):
    global CONNECTED
    if(line[1] == "005"):
        print("Connected! Joining channel")
        s.send(bytes("JOIN %s %s \r\n" % (CHANNEL,KEY), "UTF-8"));
        CONNECTED = 1

def getcmd(line):
    botcmd = ""
    if (len(line) > 3):
        if (line[3][:2] == ":!"):
            botcmd = line[3][1:]
    return (botcmd)

def getusr(line):
    sender = ""
    for char in line:
        if(char == "!"):
            break
        if(char != ":"):
            sender += char
    return (sender)

def getmsg(line):
    size = len(line)
    i = 3
    message = ""
    while(i < size):
        message += line[i] + " "
        i = i + 1
    message.lstrip(":")
    return message[1:]

# Gets XKCD info
def xkcdpharse(url):
        try:
            link = url + "/info.0.json"
            page = requests.get(link, headers=headers, timeout=5)
            page.encoding = 'UTF-8'
            comicinfo = json.loads(page.text)
            return "^ xkcd: " + str(comicinfo["num"]) + " Name: " + comicinfo["safe_title"] + " Img: " + comicinfo["img"] + " Title Text: " + comicinfo["alt"]
        except Exception as e:
            print("Bad url in message: ", link, e)

# get the title from a link and send it to the channel
def getTitle(link, chanel):
    if "xkcd.com" in link:
        say(xkcdpharse(link), channel)
    else:
        try:
            page = requests.get(link, headers=headers, timeout=5)
            page.encoding = 'UTF-8'
            tree = html.fromstring(page.text)
            title = tree.xpath('//title/text()')
            say("^ " + title[0].strip(), channel)
        except Exception:
            print("Bad url in message: ", link)

# checks if given string is a url
# it must start with either http(s):// and/or www. and contain only
# characters that are acceptable in URLs
def isURL(string):
    match = URLpattern.fullmatch(string)
    if match:
        return True
    else:
        return False

class Bot(object):
    usrlist = {}
    channel = CHANNEL
    socket = None

    def say(self, msg, channel=None):
        if channel is None:
            channel = self.channel
        self.socket.send(bytes("PRIVMSG %s :%s\r\n" % (channel, msg), "UTF-8"))

    def notice(self, msg, channel=None):
        if channel is None:
            channel = self.channel
        print((channel, msg))
        self.socket.send(bytes("NOTICE %s :%s\r\n" % (channel, msg), "UTF-8"))

def parse_and_run(state, line):
    #info returned to main loop for further processing
    out = {
        'user' : getusr(line[0]),
            'cmd' : line[1],
        'channel' :line[2],
        'msg' : getmsg(line)[len(getcmd(line)):],
        'botcmd' : getcmd(line)
    }
    #handle userlist here... WIP.
    if (out['cmd'] == "353"):
                    #this is terrible... find a better way later
        newusrs = line[5:]
        newusrs = ' '.join(newusrs).replace('@','').split()
        newusrs = ' '.join(newusrs).replace('%','').split()
        newusrs = ' '.join(newusrs).replace('+','').split()
        newusrs = ' '.join(newusrs).replace(':','').split()
        newusrs = ' '.join(newusrs).replace('~','').split()
        for usr in newusrs:
            state.usrlist[usr] = ""
    if(out['cmd'] == "NICK"):
        state.usrlist[out['channel'][1:]] = state.usrlist[out['user']]
        del state.usrlist[out['user']]
    if (out['cmd'] == "PART" or out['cmd'] == "QUIT"):
        del state.usrlist[out['user']]
    if (out['cmd'] == "JOIN" and out['user'] != NICK):
        state.usrlist[out['user']] = ""
    if (out['cmd'] == "KICK"):
        del state.usrlist[line[3]]
    #run commands
    try:
        in_channel = out['cmd'] == 'PRIVMSG' and out['channel'] == CHANNEL
        in_query = out['cmd'] == 'PRIVMSG' and out['channel'] == NICK
        if in_channel:
            state.channel = CHANNEL
        elif in_query:
            state.channel = out['user']
        state.info = out
        if in_channel or in_query:
            if(out['botcmd'][1:] in state.usrlist.keys()):
                if(out['botcmd'][1:] == out['user']):
                    state.usrlist[out['user']] = out['msg']
                else:
                    if(not state.usrlist[out['botcmd'][1:]].isspace()):
                        state.say(state.usrlist[out['botcmd'][1:]], state.channel)
            elif out['botcmd'] == "!reload":
                global gbot_commands
                gbot_commands = importlib.reload(gbot_commands)
            else:
                gbot_commands.cmdlist[out['botcmd']](state)
    except Exception as FUCK:
        traceback.print_exc()
    return(out)

q = queue.Queue()
bot = Bot()
bot.socket = s
bot.nick = NICK

face = threading.Thread(target=getrss.rssfunc, args = (q,feeds))
face.daemon = True
face.start()
while 1:
    readbuffer = readbuffer+s.recv(1024).decode("UTF-8",'ignore')
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )
    try:
        items = q.get(timeout=1)
    except queue.Empty:
        items = []
    try:
        if items!=[] or items!= None:
            for item in items:
                if item != "":
                    say(item, CHANNEL)
                    print(item)
    except Execption as E:
        if E != q.Empty:
            print(E)
            break
    #Clear the queque
    q.queue.clear()
    for line in temp:
        line = str.rstrip(line)
        #print(line)
        line = str.split(line)
        #must respond to pings to receive new messages
        if(line[0] == "PING"):
            s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        elif(CONNECTED == 0):
            joinch(line)
        #housekeeping done, be a bot
        else:
            x = parse_and_run(bot, line)
            print (x)
            #print(bot.usrlist)
            # check if the message in a channel contains a protocol or or www.
            in_channel = x['cmd'] == 'PRIVMSG' and x['channel'] == CHANNEL
            in_query = x['cmd'] == 'PRIVMSG' and x['channel'] == NICK
            if in_channel:
                channel = CHANNEL
            elif in_query:
                channel = x['user']

            if in_channel or in_query:
              if( x['msg'].find("http") != -1 or x['msg'].find("www.") != -1):
                  msgArray = x['msg'].split(" ")
                  for l in msgArray:
                      if (isURL(l)):
                          # check if the link has a protocol if not add http
                          if not l.lower().startswith("http"):
                              l = 'http://' + l
                          getTitle(l, channel)
