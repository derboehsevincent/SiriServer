# -*- coding: UTF-8 -*-
#by -dbv- aka derboehsevincent

#change path to nircmd.exe in line 10
#nircmd can be found here http://www.nirsoft.net/utils/nircmd.html
#change, if you want, default volume to your nedds (mine is 17k which equals 25%) in line 51
#change IP in Line 70 to IP of the socketserver
import SocketServer
import unicodedata
import subprocess

def setvolume(status, value):
    path = "C:\\nircmd.exe"
    subprocess.call([path, status, value])


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def newvolume(self, newvolume):
        return self.newvolume
    

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        self.data = self.data.decode('utf-8')
        self.data = unicodedata.normalize('NFKD', self.data).encode('ascii','ignore')
        print "{} wrote:".format(self.client_address[0])
        print self.data
        print type(self.data)
        print self.data.split("Lautstarke")
        currentvolume = int(self.data.split(";")[1].strip())
        print currentvolume
        try:
            if len(self.data.split("Lautstarke"))>1:
                if len(self.data.split("Lautstarke")[1].split("erhohen")) > 1:
                    volup =int(self.data.split("Lautstarke")[1].split("erhohen")[0].split("prozent")[0].split(" ")[2].strip())
                    newvolume = (currentvolume / 100 * volup) + currentvolume
                    status = "setsysvolume"
                    print newvolume
                    setvolume(status, str(newvolume))
                    newvolume = str(newvolume)
                if len(self.data.split("Lautstarke")[1].split("verringern")) > 1:
                    volup =int(self.data.split("Lautstarke")[1].split("verringern")[0].split("prozent")[0].split(" ")[2].strip())
                    newvolume = currentvolume - (currentvolume / 100 * volup) 
                    status = "setsysvolume"
                    print newvolume
                    setvolume(status, str(newvolume))
                    newvolume = str(newvolume)
                if len(self.data.split("Lautstarke")[1].split("normal")) > 1:
                    newvolume = 17000
                    status = "setsysvolume"
                    setvolume(status, str(newvolume))
                    print "normal"
                    newvolume = str(newvolume)
                
    
                    
        except:
            pass
        #changestatus ={"aus":"mutesysvolume", "erhÃ¶hen":"changeysvolume", "verringern":"changesysvolume", "normal":"setsysvolume"}
        # just send back the same data, but upper-cased
        self.request.sendall(str(newvolume))


if __name__ == "__main__":
    HOST, PORT = "192.168.178.27", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
