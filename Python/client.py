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

import socket, sys, subprocess

if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysClS = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SysCls = 'cls'
else:
	SysCls = 'unknown'

print "\n\n"
print "\t\t________                       ___________.__"
print "\t\t\_____  \ ______   ____   ____ \_   _____/|__|______   ____ "
print "\t\t /   |   \\____ \_/ __ \ /    \ |    __)  |  \_  __ \_/ __ \ "
print "\t\t/    |    \  |_> >  ___/|   |  \|     \   |  ||  | \/\  ___/ "
print "\t\t\_______  /   __/ \___  >___|  /\___  /   |__||__|    \___  >"
print "\t\t        \/|__|        \/     \/     \/                    \/"
print "\t\t                                           Socket Client\n\n"


def help():
    print "\n[#] USAGE: client.py IP PORT"
    print "[#] EX: client.py 111.111.1.11 8000\n"
    print "[+] This is client socket"
    print "[+] Client can easily connect to server and start chatting with server,\n[+] Client can also send commands to server to get executed & vice versa"
    print "[+] To send commands to server : "
    print "[+]      command : command_to_execute"
    print "[+]      like - command : ipconfig"
    print "[=] NOTE : All the cmd commands may not execute currently."

    exit()

try:
    ip = sys.argv[1]
    port = sys.argv[2]
except IndexError:
    print "[=] No enough arguments!"
    help()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))
    print "[+] Connected with server, IP : %s & PORT : %d \n" % (ip, int(port))

    while True:
        try:
            data =  raw_input("Enter text to send to server : ")
        except KeyboardInterrupt:
            print "CTRL^C Pressed, Shutting client"
            sock.close()
            sys.exit()
        sock.send(data)
        while True:
            data_recv = sock.recv(104448)

            if not data_recv:
                print "[=] Connection closed by remote host"
                break
            elif data_recv[:10] == 'command : ':
                print "\n[+] Server sent a command to execute. Command : %s" % data_recv[10:]
                try:
                    if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
                        new_data = subprocess.Popen(["/bin/sh", '-c', data_recv[10:]],stdout=subprocess.PIPE).communicate()[0]
                        sock.send("\n %s " % new_data)
                        print "\nSent Command response to server"
                        continue
                    elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
                        new_data = subprocess.Popen(data_recv[10:],stdout=subprocess.PIPE).communicate()[0]
                        sock.send("\n %s " % new_data)
                        print "\nSent Command response to server"
                        continue
                    else:
                        print "\n[=] System plattform not detected to execute commands."
                        sock.send("Sorry, remote server system plattform not detected to execute commands.")
                        continue
                except Exception as e:
                    sock.send("Seems you sent a wrong command to get executed, Error occured!", e)
                    continue
            else:
                print "\n[+] Server Sent : %s\n" % data_recv
                break




    sock.close()
except KeyboardInterrupt:
    print "CTRL^C Pressed, Shutting client"
    sys.exit()
except Exception as e:
    print "Error occured"
    print "Error => %s" % e