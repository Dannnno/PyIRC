"""
Copyright (c) 2014 Dan Obermiller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

You should have received a copy of the MIT License along with this program.
If not, see <http://opensource.org/licenses/MIT>
"""

"""Program to work on and develop an IRC client in python using the builtin
sockets module
"""

#Just the imports I can foresee needing
import sys
import socket
import multiprocessing
import time
import select
import errno


class IRC_member(object): 

    def __init__(self, nick, **kwargs):
        self.nick = nick
        self.ident = self.nick
        self.realname = self.nick
        self.password = None
        self.user = "USER {} {} bla :{}\r\n".format(self.nick, self.ident, self.realname)
        for keyword, value in kwargs.iteritems():
            self.__dict__[keyword] = value
        
        self.servers = {}
        self.channels = {}
        
        self.ready_read, self.ready_write, _ = select.select(
                                                             self.servers.values(),
                                                             self.servers.values(),
                                                             [],
                                                             60)
        
    def join_server(self, host, port):
        
        if host in self.servers:
            print "Already connected to this server"
            return
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print "Socket Created"                        
            self.servers[host] = s
            self.channels[host] = []    
            print self.servers
            print self.channels
            remote_ip = socket.gethostbyname(host)
            s.connect((remote_ip, port))
            print "Socket connected to {} on ip {}".format(host, remote_ip)
            
        except socket.error as (errnum, strerr):
            print "Failed to create socket to {} on {} from {}".format(
                   host, remote_ip, port)
            print errnum
            print strerr
            if port != 6667:
                print "Consider using port 6667 instead"
                   
        except socket.gaierror as (errnum, strerr):
            print "Hostname could not be resolved. Exiting"
            print errnum
            print strerr
            
        else:
            s.settimeout(2)
            s.setblocking(0)
            # API: string hostname, should be key in self.servers, string formatted
            self.send_message(host, "NICK {}\r\n".format(self.nick))
            self.send_message(host, "USER {} {} bla :{}\r\n".format(
                                        self.ident, host, self.realname))
            if self.password is not None:
                self.send_message(host, "MSG NickServ identify {}".format(self.password))
                
        
    def leave_server(self, host):
        if host in self.servers:
            self.send_message(self.servers[host], "QUIT\r\n")
            del self.servers[host]
            
            for chan in self.channels[host]:
                self.leave_channel(host, chan)
            del self.channels[host]
        else:
            print "Not connected to this server"
        
    def join_channel(self, host, chan_name):
        print self.servers
        print self.channels
        if chan_name.startswith("#"):
            if chan_name not in self.channels[host]:
                self.channels[host].append(chan_name)
                self.send_message(host, "JOIN {}\r\n".format(chan_name))
            else:
                print "Already a member of this channel"
        else:
            print "Invalid channel {}".format(chan_name)
        
    def leave_channel(self, host, chan_name):
        if chan_name in self.channels[host]:
            self.send_message(host, "PART\r\n")
            self.channels[host].pop(chan_name)        
        else:
            print "Not connected to channel {}".format(chan_name)
            
    def send_message(self, host, message):
        try:
            if host in self.servers:
                my_socket = self.servers[host]
                sent = my_socket.send(message)
                if sent == 0:
                    raise RuntimeError("Socket connection broken while sending {}".format(message))
            else:
                print "Host {} not connected to".format(host)
        except socket.error as (errnum, strerr):
            print errnum
            print strerr
            
    def recieve_messages(self, host, buff_size=4096):
        my_socket = self.servers[host]
        
        while True:
            try:
                readbuffer = my_socket.recv(buff_size)
                if not readbuffer:
                    raise RuntimeError("Socket connection broken while receiving")
    
                temp = readbuffer.split("\n")
                readbuffer = temp.pop()
    
                for line in temp:
                    line = line.rstrip().split()
                    if (line[0] == "PING"):
                        self.ping_pong(host, line[1])
                    else:
                        line = " ".join(line)
                        print line
            except socket.error:
                pass

        
    def ping_pong(self, host, data):
        my_sock = self.servers[host]
        my_sock.send("PONG {}\r\n".format(data))
        
    def __str__(self):
        return "IRC_member {}".format(self.nick)
   
def work1():
    global my_user
    print my_user
    print work1
    HOST = "irc.foonetic.net"
    my_user.recieve_messages(HOST, buff_size=516)

def work2():
    global my_user
    print my_user
    print work2
    HOST = "irc.foonetic.net"
    my_user.join_channel(HOST, "#poke-eternal")
    my_user.recieve_messages(HOST)   
    
if __name__ == "__main__":
    HOST = "irc.foonetic.net"
    PORT = 6667
    NICK = "my_user"
    IDENT = "test_user"
    REALNAME = "Dan Obermiller"
    PASSWORD = None #raw_input("What is your password? ")
    
    my_user = IRC_member(NICK, ident=IDENT, realname=REALNAME, password=PASSWORD)
    my_user.join_server(HOST, PORT)
    print my_user, 1
    print globals()["my_user"], 1
    
    jobs = []
    p = multiprocessing.Process(target=work1)
    jobs.append(p)
    p.start()
    time.sleep(10)
    p = multiprocessing.Process(target=work2)
    jobs.append(p)
    p.start()
    