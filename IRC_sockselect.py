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

from functools import partial
from multiprocessing import dummy
import select
import socket
import time
import threading


class IRC_member(object):
    """Class to represnt an individual using IRC, storing (non-sensitive) 
    information
    """
    
    def __init__(self, nick, **kwargs):
        """Constructor for IRC_member.  Stores nickname, realname and ident
        as well as info about servers and channels
        """
        
        self.nick = nick
        self.realname = nick
        self.ident = nick
        
        for key, value in kwargs.iteritems():
            self.__dict__[key] = value
            
        # This is a mapping of server name to socket being used
        # {
        #  "some_server": socket1,
        #  "other_server": socket2
        # }
        self.servers = {}
        
        # This is a mapping of server name to channel name
        # {
        #  "some_server": ["#a_channel", "#another-channel"],
        #  "other_server": ["#lonely-channel"]
        # }
        self.serv_to_chan = {}
        
        # This is a mapping of server name to information if it differs
        # {
        #  "some_server": {
        #                  nick: "Mynick", 
        #                  realname: "realname", 
        #                  etc
        #                 }
        # }
        # All values not in this are assumed to be self.nick, etc
        self.serv_to_data = {}
        
        ## Used to get the replies from all sockets
        self.lock = threading.Lock()
        self.replies = {}
        
    def send_server_message(self, hostname, message): 
        """Sends a message to a server"""
        if hostname not in self.servers:
            print "No such server {}".format(hostname)
            print "Failed to send message {}".format(message[:10] 
                                                      if len(message) > 10
                                                      else message)
            return 1
        
        sock = self.servers[hostname]
        try:
            sock.send("{} \r\n".format(message.rstrip()))
        except socket.error as (errnum, strerr):
            print errnum, strerr
            print "Failed to send message {}".format(message[:10] 
                                                      if len(message) > 10
                                                      else message)
            return 2
        else:
            return 0
        
    def send_channel_message(self, hostname, chan_name, message):
        """Sends a message to a channel"""
        if hostname not in self.servers:
            print "Not connected to server {}".format(hostname)
            print "Failed to send message {}".format(message[:10] 
                                                      if len(message) > 10
                                                      else message)
            return 1

        elif chan_name not in self.serv_to_chan[hostname]:
            print "Not in channel {}".format(chan_name)
            print "Failed to send message {}".format(message[:10] 
                                                      if len(message) > 10
                                                      else message)
            return 2

        else:
            try:
                sock = self.servers[hostname]
                sock.send("PRIVMSG {} :{}\r\n".format(chan_name,
                                                       message.rstrip()))
            except socket.error as (errnum, strerr):
                print errnum, strerr
                print "Failed to send message {}".format(message[:10] 
                                                          if len(message) > 10
                                                          else message)
                return 3
            else:
                return 0
    
    def send_privmsg(self, hostname, username, message):
        """Sends a private message to a user"""
        if hostname not in self.servers:
            print "No such server {}".format(hostname)
            print "Failed to send message {}".format(message[:10] 
                                                      if len(message) > 10
                                                      else message)
            return 1
            
        ## TODO: Have a test to check for valid users
        ## Should return 2
        ## if username not in ____: ...
        
        sock = self.servers[hostname]
        try:
            sock.send("PRIVMSG {} :{}\r\n".format(username, message.rstrip()))
        except socket.error as (errnum, strerr):
            print errnum, strerr
            print "Failed to send message {}".format(message[:10] 
                                                      if len(message) > 10
                                                      else message)
            return 3
        else:
            return 0
            
    def ping_pong(self, sock, data):
        """Pongs the server"""
        try:
            sock.send("PONG {}\r\n".format(data))
        except socket.error as (errnum, strerr):
            print errnum, strerr
            print "Couldn't pong the server"
            return 1
        else:
            return 0        
        
    def join_server(self, hostname, port=6667, **kwargs):
        """Joins a server"""
        if hostname in self.servers:
            print "Already connected to {}".format(hostname)
            return 0
        
        nick = self.nick
        ident = self.ident
        realname = self.realname
        
        ## Checking if the data for this server is different from the defaults
        if kwargs:
            for key, value in kwargs.iteritems():
                self.serv_to_data[hostname] = {}
                if key in ["nick", "ident", "realname"]:
                    self.serv_to_data[hostname][key] = value
                    locals()[key] = value
                else:
                    print "key-value pair {}: {} unusued".format(key, value)
            if not self.serv_to_data[hostname]:
                del self.serv_to_data[hostname]
        
        try:
            ip = socket.gethostbyname(hostname) ## throws gaierror 11004
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            self.servers[hostname] = sock
            self.serv_to_chan[hostname] = []
            sock.settimeout(2)
            #sock.setblocking(0)
            self.send_server_message(hostname, "NICK {}\r\n".format(nick))
            self.send_server_message(hostname, 
                              "USER {} {} bla: {}\r\n".format(nick, 
                                                              ident, 
                                                              realname))
            
        except socket.gaierror as (errnum, strerr): ## couldn't resolve hostname
            print errnum, strerr
            return 1
            
        except socket.error as (errnum, strerr):
            print errnum, strerr
            if port != 6667:
                print "Consider using port 6667 (the defacto IRC port)"
            return 2
        
        else:
            print "Connected to {} on {}".format(hostname, port)
            return 0
            
    def leave_server(self, hostname):
        """Leaves a server"""
        if hostname not in self.servers:
            print "Not connected to {}".format(hostname)
            return 0
            
        try:
            self.send_server_message(hostname, "QUIT\r\n")
        
        except socket.error as (errnum, strerr):
            print errnum, strerr
            print "Failed to leave server {}".format(hostname)
            return 1
            
        else:
            del self.servers[hostname]
            del self.serv_to_chan[hostname]
            if self.serv_to_data[hostname]: del self.serv_to_data[hostname]
            print "Removed server {}".format(hostname)
            return 0
            
    def join_channel(self, hostname, chan_name):
        """Joins a channel"""
        if chan_name in self.serv_to_chan[hostname]:
            print "Already connected to {} on {}".format(hostname, chan_name)
            return 0
            
        if chan_name.startswith("#"):
            try:
                self.send_server_message(hostname, 
                                         "JOIN {}\r\n".format(chan_name))
            except socket.error as (errnum, strerr):
                print errnum, strerr
                print "Failed to connect to {}".format(chan_name)
                return 1
            else:
                self.serv_to_chan[hostname].append(chan_name)
                print "Connected to {}".format(chan_name)
                return 0
        else:
            print "Channel names should look like #{}".format(chan_name)
            return 2
                
    def leave_channel(self, hostname, chan_name):
        """Leaves a channel"""
        if hostname not in self.servers:
            print "No such server {}".format(hostname)
            return 1
        
        elif chan_name not in self.serv_to_chan[hostname]:
            print "No such channel {}".format(chan_name)
            return 0
            
        else:
            try:
                self.send_server_message(hostname, 
                                         "PART {}\r\n".format(chan_name))
            except self.socket.error as (errnum, strerr):
                print errnum, strerr
                print "Failed to leave {}".format(chan_name)
                return 2
            else:
                self.serv_to_chan[hostname].pop(chan_name)
                print "Left channel {}".format(chan_name)
                return 0
                
    def receive_all_messages(self, buff_size=4096):
        """Checks all servers connected to for any messages, then displays any
        that may be waiting"""
        
        ready, _, _ = select.select(self.servers.values(), [], [], 5)
        
        if ready:
            print "ready"
            for i in range(len(ready)):
                for host, sock in self.servers.iteritems():
                    if sock == ready[i]:
                        ready[i] = host
            try:
                pool = dummy.Pool()
                pool.map(partial(self.receive_message,
                                 bsize=buff_size),
                         (tuple(ready),))
                #pool.map(self.receive_message, (tuple(ready),))
                with self.lock:
                    replies, self.replies = self.replies, {}
                for server, reply in replies.iteritems():
                    print "{} :\n\n".format(server)
                    for message in reply:
                        print " {}".format(message)
            except socket.error as (errnum, strerr):
                print errnum, strerr
                print "Failed to get messages"
                return 1
                
        else:
            return 0
            
    def receive_message(self, hostname, bsize=4096):
        """Recieves messages from a single server.  Has already checked that 
        there is a message waiting
        """
        hostname = hostname[0]
        print "Receiving from {}".format(hostname)
        reply = []
        sock = self.servers[hostname]
        
        while True:
            try:
                readbuffer = sock.recv(bsize)
                if not readbuffer: break
                temp = readbuffer.split("\n")
                readbuffer = temp.pop()
    
                for line in temp:
                    line = line.rstrip().split()
                    if (line[0] == "PING"):
                        self.ping_pong(sock, line[1])
                    else:
                        line = " ".join(line)
                        reply.append(line)
            except socket.error: break
        with self.lock:
            try:
                if reply not in self.replies[hostname]: 
                    self.replies[hostname] += reply
            except KeyError:
                self.replies[hostname] = reply
        
    def __del__(self):
        for sock in self.servers.values():
            sock.close()
        
if __name__ == "__main__":
    NICK = "Dannnno" # raw_input("Please enter your nickname ")
    #USER = raw_input("Please enter your user name ")
    #REAL = raw_input("Please enter your 'real' name ")
    HOST = "irc.foonetic.net" # raw_input("Please enter your desired server ")
    CHAN = "#pokemon-eternal" # raw_input("Please enter your desired channel ")
    
    me = IRC_member(NICK)
    me.join_server(HOST)
    time.sleep(1)
    me.receive_all_messages()
    me.join_channel(HOST, CHAN)
    time.sleep(1)
    me.receive_all_messages()
    i = 0
    while i < 100:
        start = time.time()
        msg = raw_input("Would you like to say something? ")
        if msg == 'n': break
        if msg.rstrip():
            me.send_channel_message(HOST, CHAN, msg)
        me.receive_all_messages()
        end = time.time()
        if (end-start) < 5:
            time.sleep(int(5-(end-start)))
        i += 1