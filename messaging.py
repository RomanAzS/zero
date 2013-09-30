def msg(channel, message):
    return "PRIVMSG %s %s\r\n" (channel, message)

def who(target):
    return "WHO %s\r\n" % target

def quit(message):
    return "QUIT %s\r\n" % message

def join(channel):
    return "JOIN %s\r\n" % channel

def part(channel):
    return "PART %s\r\n" % channel

def cycle(channel):
    return "PART %s\r\nJOIN %s\r\n" % (channel, channel)

def nick(newnick):
    return "NICK %s\r\n" % newnick

def pong(target):
    return "PONG %s\r\n" % target
