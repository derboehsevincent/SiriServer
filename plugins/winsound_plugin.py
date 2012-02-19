#!/usr/bin/python
# -*- coding: utf-8 -*-
#by -dbv- aka derboehsevincent

#create a file for storing current volume
#add path to this file  in Line 14 and 50
#change IP in Line 25 to IP of the socketserver


from plugin import *
import socket
import sys
import re


def currentvolume(rw, newvolume):
    if rw =="r":
        parsefile = open("/home/dbv/Desktop/siriserver/plugins/controlwin.conf","r").readlines()
        if len(parsefile) == 0:
            currentvolume = 15000
            return currentvolume
        else:
            for line in parsefile:
                currentvolume = line
            return currentvolume
    else:
        parsefile = open("/home/dbv/Desktop/siriserver/plugins/controlwin.conf","w")
        parsefile.write(newvolume)
        return newvolume

def sockettoserver(command):
    HOST, PORT = "192.168.178.27", 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(command + "\n")
        # Receive data from the server and shut down
        received = sock.recv(1024)
        return received      
    except:
        return 1
    finally:		
        sock.close()

def volumehow(command):
    if len(re.compile("auf").findall(command)) == 1:
        return "auf"
    if len(re.compile("um").findall(command)) == 1:
        return "um"

    
    

class server(Plugin):
    
    @register("de-DE", "(computer)|(computer.* \w+)")
    def volume(self, speech, language):
        if language == 'de-DE':
            if speech.lower() == 'computer':
                self.say("Folgende Befehle stehen zur Verf\xfcgung")
            else:
                firstword, command = speech.split(" ", 1)
                self.say(command)
                if len(re.compile("erh|ste").findall(command)) != 0:
                    level = re.compile("(\d+)").findall(command)[0]
                    print level
                    serverstring = currentvolume("r",0)+";"+volumehow(command)+";"+level+";raise"
                    print serverstring
                    received = sockettoserver(serverstring)
                    if received != 1:
                        self.say("Neu Laustärke beträgt nun \"{0}\" %.".format(received))
                    else:
                        self.say("Verbindung zum SocketServer konnte nicht hergestellt werden")
                if len(re.compile("sen|ver").findall(command)) != 0:
                    level = re.compile("(\d+)").findall(command)[0]
                    print level
                    serverstring = currentvolume("r",0)+";"+volumehow(command)+";"+level+";lower"
                    print serverstring
                    received = sockettoserver(serverstring)
                    if received != 1:
                        self.say("Neu Laustärke beträgt nun \"{0}\" %.".format(received))
                    else:
                        self.say("Verbindung zum SocketServer konnte nicht hergestellt werden")                
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