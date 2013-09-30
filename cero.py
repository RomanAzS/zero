import socket
import handler2

HOST = "irc.awfulnet.org"
PORT = 6667
NICK = "cero"
IDENT = "zero"
REALNAME = "1.5"

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
            if stuff.startswith("QUIT"): loop = 6
    
