import random
import sys

wordlists = {}

def load_word_list(fn):
    try:
        with open(fn) as f:
            lines = [i.strip() for i in f.readlines()]
    except FileNotFoundError:
        print('cannot load word list: %r' % fn, file=sys.stderr)
        return []
    else:
        return lines

wordlists['words'] = load_word_list('/usr/share/dict/words')
wordlists['foods'] = load_word_list('foods.txt')

def get_random_word(wordlist):
    if wordlist not in wordlists:
        print('invalid word list: %r' % wordlist, file=sys.stderr)
        return ""
    else:
        return random.choice(wordlists[wordlist])

