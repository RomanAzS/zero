import socket
import handler2
import sys
import argparse

#HOST = "irc.awfulnet.org"
PORT = 6667
NICK = "cero"
IDENT = "zero"
REALNAME = "1.5"

# handles args from command line
parser = argparse.ArgumentParser()
parser.add_argument("hostname", help="server hostname to connect to", type=str)
parser.add_argument("-p", "--port", help="specify port number to use",type=int)
parser.add_argument("-w", "--pass", help="server password for authentication", type=str)
parser.add_argument("-i", "--identify", help="password for NickServ identification", type=str)
parser.add_argument("-n", "--nick", help="use a different nick than default", type=str)
args = parser.parse_args()
HOST = args.hostname
if args.port != None: PORT = args.port
if args.nick != None: NICK = args.nick
print("Connecting to {0} {1}..." .format(HOST, PORT))

s = socket.socket()
s.connect((HOST, PORT)) # connect to host and port
s.send(("NICK %s\r\n" % NICK).encode()) # send nickname
s.send(("USER %s 8 *: %s\r\n" % (IDENT, REALNAME)).encode())

recieved = ""
loop = 0
while loop == 0:
    recieved = recieved + (s.recv(1024)).decode()
    messages = recieved.split('\n')
    recieved = messages.pop()
    
    for line in messages:
        print(line)
        stuff = handler2.handler(line)
        if stuff != None: 
            s.send(stuff.encode())
            if line.startswith("ERROR"): loop = 6
    
