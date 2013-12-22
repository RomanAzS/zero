# -*- coding: utf-8 -*-

channels = {}
admins = {"kojiro":4}
botnick = 'cero' 
NICK = None

class Nick:
    def __init__(self, nick):
        self.nick = nick
        print("nick is %s" % self.nick)
        pass
    def update(self, nick):
        self.nick = nick
        print("nick changed to %s" % nick)
    def botnick(self): 
        return self.nick

class Recv:
    def __init__(self):
        self.channels = channels
        self.handledTypes = {'JOIN': self.user_join, 
                        'INVITE': self.invite,  '352': self.who_reply, 
                        'QUIT': self.user_quat, 'PART': self.user_gone,
                        'KICK': self.user_gone, 'NICK': self.user_nick,
                        '376': self.endof_motd}
    def handler(self, raw_message, nick):
        NICK = nick
        try:
            print(raw_message)
        except UnicodeEncodeError: print(raw_message.encode())
        message = raw_message.split(':')
        try:
            messageType = message[1].split()[1].strip()
            if messageType in list(self.handledTypes.keys()):
                return self.handledTypes[messageType](message, NICK)
            else: return
        except IndexError:
            messageType = message[0].strip()
            if messageType == 'PING':
                return "PONG %s\r\n" % message[1]

    def endof_motd(self, message, NICK):
#        return "MODE {0} +B".format(botnick)
        pass

    def user_join(self, message, NICK):
        print(Nick)
        nick = NICK.botnick()
        print(nick)
        print(message)
        channel = message[2][:-1]
        #print(channel)
        user = message[1].split('!')[0]
        if user == nick :
            self.channels[channel] = {}
            print("Joined channel " + channel)
            return "WHO %s\r\n" % channel
        else:
            return "WHO %s\r\n" % user

    def invite(self, message, NICK):
        channel = message[2]
        return "JOIN %s\r\n" % channel #WHO %s" % (channel, channel)

    def who_reply(self, message, NICK):
        #    print(message)
        msg = message[1].split()
        channel = msg[3]; 
        usernick = msg[7];
        username = msg[4];
        userhost = msg[5]
        userflags = msg[8]
        userrole = ''
        if userflags[-1] in ['~', '%', '&', '+', '@']:
            userrole = userflags[-1]
    #        userflags = userflags[-1:]
    #    print(username, userhost, userrole, userflags)
        self.channels[channel][usernick] = {'uname': username, 
            'uhost': userhost, 'urole': userrole, 'uflags': userflags}
#        Admins.giveAdmin(usernick)
#        print(self.channels)
        return


    def user_gone(self, message, NICK):
        """User parted/kicked"""
        channel = message[2][:-1]
        if message[1].split()[1] == PART:
            user = message[1].split('!')[0]
        else: user = message[1].split()[-1:]
        if user != NICK.botnick():
            del self.channels[channel][user]
        else: del self.channels[channel]    
        pass

    def user_quat(self, message, NICK):
        # checked; server kills/klines are also QUITs 
        channel = message[2][:-1]
        user = message[1].split('!')[0]
        if user != NICK.botnick():
            del self.channels[channel][user]
        pass

    def user_nick(self, message, NICK):
        """When a user changes their nick remap their entry in chan dict
        to their new nick"""
        nickorig = message[1].split('!')[0].strip()
        nicknew = message[2].strip()
    #    print(channels)
        if nickorig == NICK.botnick(): NICK.update(nicknew)
        for item in list(self.channels.keys()):
            if nickorig in list(self.channels[item].keys()):
                self.channels[item][nicknew] = self.channels[item][nickorig]
                del self.channels[item][nickorig]

    def privmsg(self, message, NICK):

        pass

    def notice(self, message, NICK):
        """For integrating services functionality"""
        pass

class Admins:
    """Stuff for checking adminship"""
    def __init__(self):
        self.admins = admins

    def isAdmin(self, user):
        if self.admins[user] > 1: return True

    def level(self,user):
        return self.admins[user]
    #somewhere in this mess, check whether new arrivals are in admin conf
    # start using config files?
    def giveAdmin(self, user):
        print(config)
        user = user.lower()
        print(self.admins)
        if config:
            # open cofig, get information, havent worked out conf yet
            pass
        else: 
            if user not in self.admins.keys():
                self.admins[user] = 1
                print(self.admins)

class Privmsg:
    def __init__(self):
        self.commands = set()


