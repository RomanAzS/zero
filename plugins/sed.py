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
    try:
        for message in log:
            try:
                if qual:
                    if re.search(sedregex, message[1]) and re.search(qual, message[1]):
                        return message
                else:
                    if re.search(sedregex, message[1]):
                        return message
            except BaseException:
                pass
    except KeyError:
        pass
    return ""

#@Hook("PRIVMSG")
def sed(user, to, chan, msg, backlog):
    nick = user
    print(msg)
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
        s.msg = get_message(s.to_replace, nick, backlog.backlog[chan.lower()], qual=s.qual)
    else:
        s.msg = get_message(s.to_replace, nick, to)

    if not s.msg:
        pass
#        return (user,to,targ,msg)

    try:
        new_msg = re.sub(s.to_replace, s.replacement, s.msg, s.count, s.flags)
        return  "PRIVMSG %s :<%s> %s" % (channel, nick, new_msg)
#        return (user,to,targ,msg)
    except BaseException:
        traceback.print_exc()

