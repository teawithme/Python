#! /usr/bin/env python3

import sys
import getopt
import socket

try:
    optlist, args = getopt.getopt(sys.argv[1:], '', ["host=", "port="])
except:
    print('Parameter Error')
    sys.exit(1)

if len(optlist) != 2:
    print('Parameter Error')
    sys.exit(1)

host = optlist[0][1]
portlist = optlist[1][1].split('-')
ports = []

if len(portlist) == 2:
    port_start = int(portlist[0])
    port_end = int(portlist[1])
    for i in range(port_start,(port_end + 1)):
        ports.append(i)
else:
    ports.append(int(portlist[0]))

if len(host.split('.')) != 4:
    print('Parameter Error')
    sys.exit(1)

def connect(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)

    try:
        s.connect((host,port))
        s.sendall(b'Hello, world')
        print(port, 'open')
    except OSError as msg:
        s.close()
        s = None
        print(port, 'closed')

for port in ports:
    connect(host,port)
