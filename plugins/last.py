from collections import deque

class History:
    def __init__(self):
        self.backlog = {}
    def newchan(self, channel):
        self.backlog[channel] = deque([],maxlen=51)
    def recv_msg(self, user, channel, message):
#        line = "<%s> %s" % (user, message)
        self.backlog[channel].append((user, message))
    def last(self, user, host, channel, message):
        if not (message.isdigit() or message == ''): return
        else: 
            if message == '': n = 10
            elif not 0 < int(message) < 51: n = 10
            else: n = int(message)
            x = list(self.backlog[channel])[-n:]
            xx = ''
            for i in x: xx += 'NOTICE %s <%s> %s\r\n' % (user, i[0], i[1])
            return xx
