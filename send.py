def msg(channel, message):
    return "PRIVMSG %s %s\r\n" % (channel, message)

def who(target):
    return "WHO %s\r\n" % target

def quit(message=None):
    if message is not None: return "QUIT %s\r\n" % message
    else: return "QUIT Bot 1.5\r\n"

def join(channel):
    return "JOIN %s\r\n" % channel

def part(channel, message=None):
    if message is not None: return "PART {0} {1}\r\n".format(channel, message)
    else: return "PART {0} Leaving\r\n".format(channel)

def cycle(channel):
    return "PART %s\r\nJOIN %s\r\n" % (channel, channel)

def nick(newnick):
    #the bot also needs to have its own nick stored somewhere & this will 
    #change that entry
    return "NICK %s\r\n" % newnick

def pong(target):
    return "PONG %s\r\n" % target

def notice(target, message):
    return "NOTICE {0} {1}\r\n".format(target, message)
