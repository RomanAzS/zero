import json
import urllib.request
import re
from collections import deque

ERR_NOTFOUND = "Query not found" 
ERR_UNSPECIFIED = "An error occured" 
ERR_INDEX = "Invalid index"

cache = deque([], maxlen=20)

def dictionary(query):
    pos_flags = {'-adj': 'Adjective', '-v': 'Verb', '-n': 'Noun', '-pro':'Pronoun',
                 '-pre': 'Preposition', '-adv': 'Adverb'}
    args = False; flag = None; num = None
    q = query.split()
    for i in pos_flags.keys(): 
        for x in q: 
            if i in x: 
                args = True; 
                flag = i
                query = query.replace(x, '', 1)
    for i in q: 
        if i.isdigit(): 
            args = True 
            num = i
            
    print(flag, args, num)
    
    if num: query = query.replace(num, '', 1).strip()
#    if flag: query = query.replace(flag, '', 1).strip()
    print(query)

    for i in cache: 
        if i[0] == query: 
            res = i[1]
            print('using cached thing')
            break
    else: 
        try:
            req = urllib.request.urlopen("http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&sl=en&tl=en&restrict=pr%%2Cde&client=te&q=%s" % query)
        except urllib.error.HTTPError:
            return ERR_NOTFOUND
        response = req.read().decode()[25:-10].replace("\\x", "\\u00")
        res = json.loads(response)
        cache.append((query, res))

#    default = 

    if flag:
        for i in res['primaries']: 
            if pos_flags[flag] == i['terms'][0]['labels'][0]['text']:
                pos = pos_flags[flag]
                if num: 
                    try: 
                        r = i['entries'][int(num)]['terms'][0]['text']
                        print(r)
                        ret = "%s. [%s]" % (pos_flags[flag], num) + r
                    except IndexError: return ERR_INDEX
                else: ret = "%s. [1] %s" %(pos,i['entries'][1]['terms'][0]['text'])
        else: return ERR_NOTFOUND
    else: # i'm really sorry i know this is terrible and i should be shot
        data = [[[n["text"] for n in d["terms"]] for d in i["entries"]] for i in res["primaries"]]
        try:
            entry1 = data[0][1][0]
            try:
                entry2 = data[0][2][0]
                entryTestLen = len(entry1) + len(entry2)
                if entryTestLen > 420:
                    entry1 = entry1
                else:
                    entry1 = "[1]%s. [2]%s" % (entry1, entry2)
                    try:
                        entry3 = data[0][3][0]
                        entryTestLen = len(entry1) + len(entry3)
                        if entryTestLen > 420:
                            entry1 = entry1
                        else:
                            entry1 = "%s. [3]%s" % (entry1, entry3)
                    except IndexError:
                        pass
            except IndexError:
                pass
        except IndexError:
            entry1 = data[0][0][0]
        ret ="%s. %s"%(res['primaries'][0]['terms'][0]['labels'][0]['text'],entry1)

    return "\002%s\002: %s" % (query, ret)

def main(user, host, channel, message):
    try: 
        return "PRIVMSG %s :%s\r\n" % (channel, dictionary(message))
    except KeyError: return "PRIVMSG %s :%s\r\n" % (channel, ERR_NOTFOUND)
    except: return "PRIVMSG %s :%s\r\n" % (channel, ERR_UNSPECIFIED)
