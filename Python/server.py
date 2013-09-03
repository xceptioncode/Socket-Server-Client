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
# Copyright:   (c) Xception 2013
# Licence:     Open Source
#-------------------------------------------------------------------------------

import socket, sys

try:
    port_bind = int(raw_input("Enter port to bind : "))
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", port_bind))
    server_sock.listen(4)
except Exception as e:
    print e

try:
    print "\n[#] Waiting for a client to connect on port : %d " % port_bind

    (client, (ip, port)) = server_sock.accept()

    print "[#] Received connection from a client"
    print "[#] Client : ( %s : %s )" % (str(ip), str(port))

    print "[+] Server ready to receive data from client.. \n"

    data = "anything"

    while len(data) :

        data = client.recv(2048)
        if not data: break
        print "\n[+] Client sent: %s \n" % data
        client.send(raw_input("Enter text to send to client : "))



    print "[=] Connection closed by client.."
    client.close()

    print "[=] Shutting server socket.. "
    server_sock.close()
except KeyboardInterrupt:
    print "CTRL^C Pressed, Shutting server"
    sys.exit()
except Exception as e:
    print "Error occured"
    print "Error => %s" % e