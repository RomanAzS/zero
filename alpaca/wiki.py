import urllib.request, urllib.error
import re
import json
import sys

class Wikipedia:
    def __init__(self):
        self.cache = {}
        self.DNE = "Page does not exist"
        self.ERR = "An unknown error occured."
    def get(self, query, tail=None):
#        try:
            query = query.replace(' ','%20')
#            req = urllib.request.Request("http://en.wikipedia.org/w/index.php?action=render&title=%s"  %  query)
            req = urllib.request.Request("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles=%s&format=json&redirects" % query)
            req.add_header("User-agent", "Mozilla 5.10")
        
            response = urllib.request.urlopen(req)
            response = response.read().decode()
            pageid = re.findall('\d+', response)[0]

            response = json.loads(response)
            pages = response['query']['pages']
            pid = list(pages.items())[0][0]
            if pid == '-1': 
                return self.search(query)
            extract = pages[pid]["extract"]
            if "may refer to" in extract.lower():
                return self.search(query)
            return (extract,tail)
#        except:
#            print(sys.exc_info()[0])
#            return self.ERR

    def search(self, query):
        query = query.replace(' ', '%20')
        req = urllib.request.Request("http://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=%s&srprop=timestamp&format=json&srwhat=text" % query)
        req.add_header("User-agent", "Mozilla 5.10")

        response = urllib.request.urlopen(req)
        response = json.loads(response.read().decode())
        results = response['query']['search']
        r = [n["title"] for n in results if 'disambiguation' not in n["title"].lower()]
        def until_100(qs):
            aggr = 0
            index = 0
            for i in qs:
                if len(i) + aggr < 90:
                    aggr = aggr + len(i)
                    index +=1
            return len(qs) - index 
        windex = len(r) - (until_100(r[1:]) - 1)
        print(windex)
        print(r[1:windex])
        tail = "Not what you were looking for? Try %s" % ' | '.join(r[1:windex])
        return self.get(r[0], tail)

    def parse(self, extract):
        maxlen = 425
        ext = re.sub('<b>|</b>', '\x02', extract[0])
        ext = re.sub('<i>|</i>', '\x1f', ext)
        ext = re.sub('<p>|</p>|<[/]{0,1}su[bp]>|\n', '', ext)
        print(ext)
        ext = re.sub('<.+?>', '', ext)
        print(ext)
        sentences = re.findall(".+?(?<!Dr|Mr|Jr|Sr| \w|\.\w)[.!?]\s", ext)
#        sentagg = ''
        if extract[1] is not None:
            maxlen = maxlen - len(extract[1]) - 1
        i = 0
        agg = ''
        for word in ext.split():
            if (len(agg) + len(word) + 1) > maxlen:
                break
            else:
                agg = "%s%s " % (agg, word)
        if len(agg) < len(ext):
            agg = "%s [...] " % agg
        # while len(sentagg) < maxlen and i < len(sentences): 
        #     sentagg_ = sentagg + sentences[i]
        #     if len(sentagg_) > maxlen: break
        #     else: sentagg = sentagg_
        #     print(sentagg)
        #     i+=1
        # print(len(sentagg))
        agg = agg.lstrip()
        if extract[1] is not None:
            return agg + extract[1]
        else: return agg

    def wiki(self, user, host, channel, msg):
        return "PRIVMSG %s :%s\r\n" % (channel, self.parse(self.get(msg)))
