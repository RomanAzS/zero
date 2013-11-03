import time
import socket
from events import Recv, initialize
import sys
import argparse
import os.path

PORT = 6667
NICK = "cero"
IDENT = "zero"
REALNAME = "1.5"

config = True

# handles args from command line
parser = argparse.ArgumentParser(description="Azi's bot v 1.5")
parser.add_argument("hostname", help="server hostname to connect to", type=str)
parser.add_argument("-p", "--port", help="specify port number to use",type=int)
parser.add_argument("-P", "--pass", help="server password for authentication", type=str)
parser.add_argument("-w", "--warnoff", help="disable warnings", action="store_true")
parser.add_argument("-I", "--ident", help="specify ident", type=str)
parser.add_argument("-i", "--identify", help="password for NickServ identification", type=str)
parser.add_argument("-n", "--nick", help="use a different nick than default", type=str)
parser.add_argument("-r", "--realname",help="specify bot's realname", type=str)
args = parser.parse_args()

if not args.warnoff:
    if not os.path.isfile("cero.conf"): 
        print("WARNING: No config file detected. Run anyway? (y/n)")
        def f():
            anser = input()
            if anser == 'y': 
                config = False
                return
            elif anser == 'n':
                print("Exiting.")
                sys.exit(0)
            else: 
                print("Please input 'y' or 'n'.")
                f()
        f()

    if len(sys.argv) > 2 and config:
        print("WARNING: Some flags may override values set in config. Continue? (y/n)")

HOST = args.hostname
if args.port != None: PORT = args.port
if args.nick != None: NICK = args.nick
if args.ident != None: IDENT = args.ident
if args.realname != None: REALNAME = args.realname
print("Connecting to {0} {1}..." .format(HOST, PORT))

def start(loop):
    s = socket.socket()
    s.connect((HOST, PORT)) # connect to host and port
    s.send(("NICK %s\r\n" % NICK).encode()) # send nickname
    s.send(("USER %s 8 *: %s\r\n" % (IDENT, REALNAME)).encode())
    #s.send(("MODE {0} +B".format(NICK)).encode())

    #if args.identify != None: 
    #    time.sleep(2)
    #    s.send(("PRIVMSG NickServ identify {}".format(args.identify)).encode())
    initialize(NICK, config, args.identify)
    recieved = ""
    loop = 0
    while loop == 0:
        recieved = recieved + (s.recv(1024)).decode()
        messages = recieved.split('\n')
        recieved = messages.pop()

        for line in messages:
    #        print(line)
            stuff = Recv().handler(line)
            if stuff != None: 
                s.send(stuff.encode())
            if line.startswith("ERROR"): loop = 19
    
start(0)
