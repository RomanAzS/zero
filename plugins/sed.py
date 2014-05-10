# sed.py: A substitution plugin
# borrowed from frony0 with permission

import re
import traceback

#from hooks import Hook

SED_REGEX = re.compile(r"^(?:(\S+)[:,] )?(?:(.+?)/)?s/(.+?)/(.*?)(?:/([gixs]{0,4}))?$")

def populate(sedobject, groups):
    group_types = ("target", "qual", "to_replace", "replacement", "flags")
    for k, v in zip(group_types, groups):
        setattr(sedobject, k, v)

def set_flags(sedobject, flags):
    i = 0
    count = 1

    if not flags:
        setattr(sedobject, 'flags', i)
        setattr(sedobject, 'count', count)
        return

    for item in flags:
        if item == 'i':
            i |= re.IGNORECASE
        if item == 'x':
            i |= re.X
        if item == 's':
            i |= re.S
        if item == 'g':
            count = 0

    setattr(sedobject, 'flags', i)
    setattr(sedobject, 'count', count)

def get_message(sedregex, nick, log, qual=None):
    print(log)
    try:
        for message in log[1:]:
            print(log)
            print(message)
            print(re.search(sedregex, message))
#            print(re.search(qual, message))
            try:
                if qual:
                    if re.search(sedregex, message) and re.search(qual, message):
                        print(message,1)
                        return message
                else:
                    if re.search(sedregex, message):
                        print(message,2)
                        return message
            except BaseException:
                pass
    except KeyError:
        pass
    return ""

#@Hook("PRIVMSG")
def sed(user, to, chan, msg, backlog):
    print(backlog.backlog)
    log = list(backlog.backlog[chan.lower()])
    log.reverse()
    nick = user
    print(msg)
    msg = msg.rstrip('\r')
    s = type('SedObject', tuple(), {})
    
    if not SED_REGEX.match(msg):
        print(user,to,msg)
        return 

    groups = SED_REGEX.match(msg).groups()
    populate(s, groups)
    set_flags(s, s.flags)

    if s.target:
        nick = s.target

    if s.qual:
        print(s.to_replace,nick,log)
        s.msg = get_message(s.to_replace, nick,log, qual=s.qual)
    else:
        print(s.to_replace,nick,to)
        s.msg = get_message(s.to_replace, nick, log)

    if not s.msg:
        return
#        return (user,to,targ,msg)

    try:
        new_msg = re.sub(s.to_replace, s.replacement, s.msg, s.count, s.flags)
        print(new_msg)
        print("PRIVMSG {0} :{1}".format(chan, new_msg) )# % (chan, new_msg))
        return "PRIVMSG {0} :{1}".format(chan, new_msg) # % (chan, new_msg)
#        return (user,to,targ,msg)
    except BaseException:
        traceback.print_exc()


def main(): pass
