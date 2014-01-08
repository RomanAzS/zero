# -*- coding: utf-8 -*-

import time
import socket
from irc import Recv, Nick, Options, Send
import sys
import argparse
import os.path

isConfig = True

# handles args from command line
parser = argparse.ArgumentParser(description="Azi's bot v 1.5")
parser.add_argument("hostname", help="server hostname to connect to", type=str)
parser.add_argument("-p", "--port", help="specify port number to use",type=int, default=6667)
parser.add_argument("-P", "--pass", help="server password for authentication", type=str)
parser.add_argument("-w", "--warnoff", help="disable warnings", action="store_true")
parser.add_argument("-I", "--ident", help="specify ident", type=str, default='zero')
parser.add_argument("-i", "--identify", help="password for NickServ identification", type=str)
parser.add_argument("-n", "--nick", help="use a different nick than default", type=str, default='cero')
parser.add_argument("-r", "--realname",help="specify bot's realname", type=str, default='1.5')
parser.add_argument("-j", "--join", help="specify channels to join", type=str)
parser.add_argument("-a", "--admin", help="add admin level 4", type=str)
args = parser.parse_args()

if not args.warnoff:
    if not os.path.isfile("cero.conf"): 
        print("WARNING: No config file detected. Run anyway? (y/n)")
        def f():
            anser = input()
            if anser == 'y': 
                isConfig = False
                return
            elif anser == 'n':
                print("Exiting.")
                sys.exit(0)
            else: 
                print("Please input 'y' or 'n'.")
                f()
        f()


    if len(sys.argv) > 2 and isConfig:
        print("WARNING: Some flags may override values set in config. Continue? (y/n)")

# should do the thing with config stuff too sometime
# since there's a warning for it and all

HOST = args.hostname
PORT = args.port 
NICK = args.nick 
IDENT = args.ident 
REALNAME = args.realname 
print(args.join)
print("Connecting to {0}:{1}..." .format(HOST, PORT))

nick = Nick(NICK)
opt = Options()
opt.args(isConfig, args.join, args.identify, args.admin)
print(Nick)
def start(loop):
    s = socket.socket()
    s.settimeout(300)
    s.connect((HOST, PORT)) # connect to host and port
    s.send(("NICK %s\r\n" % NICK).encode()) # send nickname
    s.send(("USER %s 8 *: %s\r\n" % (IDENT, REALNAME)).encode())
    
    sand = Send(s)
    recv = Recv(opt, sand).handler
    recieved = ""
    t = time.time()
    while loop == 0:
        try:
            recieved = recieved + (s.recv(4096)).decode('utf-8', 'ignore')
            messages = recieved.split('\n')
            recieved = messages.pop()

            for line in messages:
                stuff = recv(line, nick)
                if stuff != None: 
                    s.send(stuff.encode('utf-8'))
                    t = round(time.time())
                elif (time.time() - t) > 150:
                    s.send(("PONG %s" % HOST).encode('utf-8'))
                    print('sent pong')
                if line.startswith("ERROR"): loop = 9

        except ConnectionResetError:
            start(0)
            break
        except socket.timeout:
            print('TIMED OUT')
            start(0)
            break

start(0)

# class Connected:
#     def __init__(self, socket, server):
#         self.sock = socket
#         self.serv = server
#         self.connected = True
#         self.timePing = 0
#         self.timePong = 0
#     def sendPing():
#         while self.connected:
#             self.sock.send(("PING %s" % self.serv).encode())
#             self.timePing = time.time()
#             time.sleep(60)
#     def recvPong():
#         self.timePong = time.time()
#         timesince = math.fabs(self.timePong - self.timePing)
#         if (math.fabs(self.timePing - time.time())) > 300: start(0)
