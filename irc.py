# -*- coding: utf-8 -*-
import random

from plugins.omdb import imdb
from plugins.last import History
from alpaca import dictionary
#from plugins.sed import sed
channels = {}
admins = {"kojiro":4}
botnick = 'cero' 
NICK = None

class Nick:
    def __init__(self, nick):
        self.nick = nick
        print("nick is %s" % self.nick)
    def update(self, nick):
        self.nick = nick
        print("nick changed to %s" % nick)
    def botnick(self): 
        return self.nick

class Options:
    """Gets the args from the command line"""
    def __init__(self):
        self.config = None
        self.ajoin = None
        self.nickserv = None
    def args(self, config, autojoin, identify, admin, zero):
        self.nickserv = identify
        self.ajoin = autojoin
        self.config = config
        self.admins = {}
        if admin:
            ad = admin.split(',')
            for a in ad: self.admins[a.lower()] = 4
#            self.admins = {admin: 4} or {"kojiro": 4}
    def ret(self):
        turn = {'ns': self.nickserv, 'join': self.ajoin, 'conf': self.config}
        return turn

class Admins:
    """Stuff for checking adminship"""
    def __init__(self, opt, chan):
        self.admins = opt.admins
        self.chan = chan
    # 0 is ignored, 1 is normal, 2&3 are admin, 4 is god aka me
    def isAdmin(self, user):
        return self.admins[user.lower()] > 1
    def isIgnored(self, user):
        return self.admins[user.lower()] < 1
    def level(self,user):
        print(self.admins)
        return self.admins[user.lower()]
    #somewhere in this mess, check whether new arrivals are in admin conf
    # start using config files?
    def giveAdmin(self, user):
#        print(config)
        config = False
        user = user.lower()
#        print(self.admins)
        if config:
            # open cofig, get information, havent worked out conf yet
            pass
        else: 
            if user not in self.admins.keys():
                self.admins[user] = 1
#                print(self.admins)
    def changeNick(self, old, new):
        self.admins[new] = self.admins[old]
        del self.admins[old]
    def ignore(self, user):
        self.admins[user] = 0
    def promote(self, user):
        self.admins[user] = self.admins[user] + 1

history = History()
#options = None
class Recv:
    """For dealing with recieved messages"""
    def __init__(self, optobj, send):
        self.channels = channels
        self.options = optobj
#        options = optobj
        self.admins = Admins(self.options, self.channels)
        self.history = history
        self.s = send
        self.privmsg = Privmsg(self.history, self.admins)
        self.handledTypes = {'JOIN': self.user_join, 
                        'INVITE': self.invite,  '352': self.who_reply, 
                        'QUIT': self.user_quat, 'PART': self.user_gone,
                        'KICK': self.user_gone, 'NICK': self.user_nick,
                        '376': self.endof_motd, '422': self.endof_motd,
                        'PRIVMSG': self.privmsg.hook}

    def handler(self, raw_message, nick):
        """Decide what to do with incoming message"""
        NICK = nick
        message = raw_message.split(':', 2)
        try:
            messageType = message[1].split()[1].strip()
            try:
                print(raw_message)
            except UnicodeEncodeError: print(raw_message.encode())
            if messageType in list(self.handledTypes.keys()):
                return self.handledTypes[messageType](message, NICK)
            else: return
        except IndexError:
            messageType = message[0].strip()
            if messageType == 'PING':
                return "PONG %s\r\n" % message[1]
#                self.s.pong(message[1])

    def endof_motd(self, message, NICK):
        print(self.options.ret())
        ret = self.options.ret()
        ns = ret['ns']
        join = ''
        if len(self.channels) == 0 and ret['join'] is not None: 
            join = "JOIN %s\r\n" % ret['join']
        elif len(self.channels) > 0: 
        #bc if it dc'd the chan dict doesnt get deleted so rejoin yeah
            j = ','.join(self.channels.keys())
            join = "JOIN %s\r\n" % j
        
        if ns is not None: 
            return "MODE {0} +B\r\nPRIVMSG NickServ :identify {1}\r\n{2}".format(NICK.botnick(), self.options.nickserv, join)
        return "MODE {0} +B\r\n{1}".format(NICK.botnick(), join)

    def user_join(self, message, NICK):
        nick = NICK.botnick()
#        print(nick)
#        print(message)
        channel = message[2][:-1].lower()
        user = message[1].split('!')[0].lower()
        if user == nick :
            self.channels[channel] = {}
            print("Joined channel " + channel)
            self.history.newchan(channel)
#            return "WHO %s\r\n" % channel
            self.s.who(channel)
        else:
            host = message[1].split('!')[1].split('@')[1].split()[0]
            self.admins.giveAdmin(user)
            print(user)
            self.channels[channel][user] = host

    def invite(self, message, NICK):
        channel = message[2]
        self.s.join(channel)
#        return "JOIN %s\r\n" % channel #WHO %s" % (channel, channel)

    def who_reply(self, message, NICK):
        #    print(message)
        msg = message[1].split()
        channel = msg[3].lower()
        usernick = msg[7].lower()
        userhost = msg[5]
#        userrole = ''
#        if userflags[-1] in ['~', '%', '&', '+', '@']:
#            userrole = userflags[-1]
    #        userflags = userflags[-1:]
    #    print(username, userhost, userrole, userflags)
        self.channels[channel][usernick] =  userhost
        self.admins.giveAdmin(usernick)
        return


    def user_gone(self, message, NICK):
        """User parted/kicked"""
        if message[1].split()[1] == 'PART':
            channel = message[1].split()[-1:][0].lower()
            user = message[1].split('!')[0].lower()
        else: 
            user = message[1].split()[-1:][0].lower()
            channel = message[1].split()[2].lower()
            print(user,channel, self.channels)
        if user != NICK.botnick():
            del self.channels[channel][user]
        else: del self.channels[channel]    

    def user_quat(self, message, NICK):
        user = message[1].split('!')[0].lower()
        for chan in self.channels.keys():
            if user in self.channels[chan].keys(): 
                del self.channels[chan][user]

    def user_nick(self, message, NICK):
        """When a user changes their nick remap their entry in chan dict
        to their new nick"""
        nickorig = message[1].split('!')[0].strip().lower()
        nicknew = message[2].strip().lower()
        if nickorig == NICK.botnick(): NICK.update(nicknew)
        for item in list(self.channels.keys()):
            if nickorig in list(self.channels[item].keys()):
                self.channels[item][nicknew] = self.channels[item][nickorig]
                del self.channels[item][nickorig]
        self.admins.changeNick(nickorig, nicknew)

#    def privmsg(self, message, NICK):
#        Privmsg().hook(message)
        

    def notice(self, message, NICK):
        """For integrating services functionality"""
        pass

#admins = Admins(options)

class Privmsg:
    def __init__(self, historyobj, adminobj):
        # hooks should be commandname: (function, adminlevel)
        self.last = historyobj
        self.admins = adminobj
        self.hooks = {'.imdb': (imdb,1), '.history': (self.last.last, 1), 
                        '``': (self.raw, 4), '.choose': (self.choose, 1), 
                      '.dict': (dictionary.main, 1)}
#        self.prefix = {'norm': '.', 'admin': '^'}
        self.pm = False
    def hook(self, msg, x):
        user = msg[1].split('!')[0]
        host = msg[1].split()[0].split('@')[1]
        channel = msg[1].split()[2].strip().lower()
        print(channel)
        message = msg[2]
        if channel == x.botnick(): self.pm = True
        else: self.last.recv_msg(user, channel, message)
        hook = message.split()[0]
        msgsanshook = message.replace(hook, '', 1).strip()
        if hook not in self.hooks.keys():pass# return self.sed(user,channel, msg)
        elif self.admins.level(user) >= self.hooks[hook][1]:
            return self.hooks[hook][0](user, host, channel, msgsanshook)
    def raw(self, user, host, channel, msg):
        print(msg, self.pm)
        if self.pm: 
            print(msg)
            return msg + '\r\n'
    def choose(self, user, host, channel, msg):
        msg = msg.split(',')
        print("PRIVMSG %s:%s: %s\r\n" % (channel, user, random.choice(msg).strip()))
        return "PRIVMSG %s :%s: %s\r\n" % (channel, user, random.choice(msg).strip())
    def sed(self, user, channel, msg):
        if msg[1][:-1] in self.admins.chan[channel].keys():
            return sed(user, msg[0][:-1], channel, msg[2], self.last)
        else: return sed(user, user, channel, msg[2], self.last)

class Send:
    def __init__(self, sock):
        self.sock = sock
    def msg(self, channel, message):
        self.sock.send(("PRIVMSG %s %s\r\n" % (channel, message)).encode())
    def who(self, target):
        self.sock.send( ("WHO %s\r\n" % target).encode())
    def quit(self, message=None):
        if message is not None: self.sock.send(("QUIT %s\r\n" % message).encode())
        else: self.sock.send(("QUIT Bot 1.5\r\n").encode())
    def join(self, channel):
        self.sock.send(("JOIN %s\r\n" % channel).encode())
    def part(self, channel, message=None):
        if message is not None: self.sock.send("PART {0} {1}\r\n".format(channel, message).encode())
        else: self.sock.send("PART {0} Leaving\r\n".format(channel).encode())
    def cycle(self, channel):
        self.sock.send(("PART %s\r\nJOIN %s\r\n" % (channel, channel)).encode())
    def nick(self, newnick):
        #the bot also needs to have its own nick stored somewhere & this will 
        #change that entry
        self.sock.send(("NICK %s\r\n" % newnick).encode())
    def pong(self, target):
        self.sock.send(("PONG %s\r\n" % target).encode())
    def notice(self, target, message):
        self.sock.send("NOTICE {0} {1}\r\n".format(target, message).encode())
