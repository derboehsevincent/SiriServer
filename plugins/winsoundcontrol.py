#!/usr/bin/python
# -*- coding: utf-8 -*-
#by -dbv- aka derboehsevincent

#create a file for storing current volume
#add path to this file  in Line 14 and 50
#change IP in Line 25 to IP of the socketserver


from plugin import *
import socket
import sys



class server(Plugin):
    
    @register("de-DE", ".*computer.*")
    def volume(self, speech, language):
        if language == 'de-DE':
            parsefile = open("/home/dbv/Desktop/siriserver/plugins/controlwin.conf","r").readlines()
            if len(parsefile) == 0:
                currentvolume = 15000
            else:
                for line in parsefile:
                    currentvolume = line
            
            answer = self.ask(u"Was kann ich für dich tun")
            answer = answer +";" + str(currentvolume)
            answer = answer.encode('utf-8')
            #answer = answer.replace("ä","\xf6")
            HOST, PORT = "192.168.178.27", 9999
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # Connect to server and send data
                sock.connect((HOST, PORT))
                sock.sendall(answer + "\n")
                # Receive data from the server and shut down
                received = sock.recv(1024)
            finally:		
                sock.close()
                parsefile = open("/home/dbv/Desktop/siriserver/plugins/controlwin.conf","w")
                parsefile.write(received)                   
                received = (100*int(received))/65535
                self.say(u"Die aktuelle Lautstärke beträgt nun \"{0}\" %.".format(received))
                self.complete_request()            
                self.complete_request()                

        else:
            self.say("This is still alpha!")
            self.complete_request()
    
    @register("de-DE", ".*Aktuelle.*lautst\xe4rke.*")
    def volumelevel(self, speech, language):
        if language == 'de-DE':
            parsefile = open("/home/dbv/Desktop/siriserver/plugins/controlwin.conf","r").readlines()
            if len(parsefile) == 0:
                currentvolume = 15000
            else:
                for line in parsefile:
                    currentvolume = line 
            currentvolume = (100*int(currentvolume))/65535
            self.say(u"Die aktuelle Lautstärke beträgt\"{0}\" %.".format(currentvolume))