#-------------------------------------------------------------------------------
# Name:        Client.py
# Purpose:      Client to connect to server
#
# Author:      Shubham Raj (http://www.facebook.com/xceptioncode)
#
# Website:      http://www.openfire-security.net
# Forum:        http://forum.openfire-security.net
#
# Created:     03/09/2013
# Copyright:   (c) Xception 2013
# Licence:     Open Source
#-------------------------------------------------------------------------------

import socket, sys

def help():
    print "USAGE: client.py IP PORT"
    print "EX: client.py 111.111.1.11 8000"
    exit()

try:
    ip = sys.argv[1]
    port = sys.argv[2]
except IndexError:
    print " No enough arguments!"
    help()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))
    print "[+] Connected with server, IP : %s & PORT : %d \n" % (ip, int(port))

    while True:
        data =  raw_input("Enter text to send to server : ")
        sock.send(data)
        print "\n[+] Server Sent : %s\n" % sock.recv(2048)


    sock.close()
except KeyboardInterrupt:
    print "CTRL^C Pressed, Shutting client"
    sys.exit()
except Exception as e:
    print "Error occured"
    print "Error => %s" % e