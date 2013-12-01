#-------------------------------------------------------------------------------
# Name:        server.py
# Purpose:      Server to recieve connection from client
#
# Author:      Shubham Raj (http://www.facebook.com/xceptioncode)
#
# Website:      http://www.openfire-security.net
# Forum:        http://forum.openfire-security.net
#
# Created:     03/09/2013
# Last_Update: 01/12/2014
# Copyright:   (c) Xception 2013
# Licence:     Open Source
#-------------------------------------------------------------------------------

import socket, sys, os, subprocess

if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
    SysClS = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
    SysCls = 'cls'
else:
    SysCls = 'unknown'

os.system(SysCls)

print "\n\n"
print "\t\t________                       ___________.__"
print "\t\t\_____  \ ______   ____   ____ \_   _____/|__|______   ____ "
print "\t\t /   |   \\____ \_/ __ \ /    \ |    __)  |  \_  __ \_/ __ \ "
print "\t\t/    |    \  |_> >  ___/|   |  \|     \   |  ||  | \/\  ___/ "
print "\t\t\_______  /   __/ \___  >___|  /\___  /   |__||__|    \___  >"
print "\t\t        \/|__|        \/     \/     \/                    \/"
print "\t\t                                           Socket Server\n\n"

def help():
    print "\n[#] USAGE: server.py"
    print "[#] EX: server.py"
    print "[+] After executing you will need to give a PORT to get bind & after binding it will start listening for connections"
    print "[+] This is server socket"
    print "[+] Client can easily connect to server and start chatting with server,\n[+] Server can also send commands to client to get executed & vice versa"
    print "[+] To send commands to client : "
    print "[+]      command : command_to_execute"
    print "[+]      like - command : ipconfig"
    print "[=] NOTE : All the cmd commands may not execute currently."

try:
    port_bind = int(raw_input("Enter port to bind : "))
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", port_bind))
    server_sock.listen(10)
except Exception as e:
    print "It seems you entered alpha character. PORT must be numeric (integer)"
    sys.exit()
except KeyboardInterrupt:
    print "\nCTRL^C pressed, Shutting program"
    sys.exit()


try:
    while True:
        print "\n[#] Waiting for a new client to connect on port : %d " % port_bind

        (client, (ip, port)) = server_sock.accept()

        print "[#] Received new connection from a client"
        print "[#] Client : ( %s : %s )" % (str(ip), str(port))

        print "[+] Server ready to receive data from client.. \n"

        data = "anything"

        while len(data) :

            data = client.recv(2048)
            if not data:
                break
            elif data[:10] == 'command : ':
                print "\n[+] Client sent a command to execute. Command : %s" % data[10:]
                try:
                    if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
                        new_data = subprocess.Popen(["/bin/sh", '-c', data[10:]],stdout=subprocess.PIPE).communicate()[0]
                        client.send("\n %s " % new_data)
                        print "Sent Command response to client"
                        continue
                    elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
                        new_data = subprocess.Popen(data[10:],stdout=subprocess.PIPE, shell=True).communicate()[0]
                        client.send("\n %s " % new_data)
                        print "Sent Command response"
                        continue
                    else:
                        print "[=] System plattform not detected to execute commands."
                        continue
                except Exception as e:
                    client.send("Seems you sent a wrong command to get executed, Error occured!", e)
                    continue
            print "\n[+] Client sent: %s \n" % data
            data_send = raw_input("Enter text to send to client : ")
            if data_send == "shut down server":
                print "[=] User asked to shut down server"
                print "[=] Shutting server socket.. "
                server_sock.close()
                sys.exit()
            else:
                client.send(data_send)


        print "[=] Connection closed by client.."
        client.close()
except KeyboardInterrupt:
    print "CTRL^C Pressed, Shutting server"
    sys.exit()
except Exception as e:
    print "Error occured"
    print "Error => %s" % e
