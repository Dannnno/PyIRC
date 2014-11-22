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

try:
    import cStringIO as IO
except ImportError:
    import StringIO as IO
finally:
    import asyncore
    import datetime
    import logging
    import socket
    import threading
    from multiprocessing import dummy


now = datetime.datetime.now()
logging.basicConfig(filename=''.join(map(str,
                                         ["Logs/",
                                          now.year,
                                          now.month,
                                          now.day,
                                          ".log"])), 
                    level=logging.INFO)  


class ServerConnection(asyncore.dispatcher):
    
    def __init__(self, hostname, port, buff_size=1024):
        super(ServerConnection, self).__init__()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = hostname, port
        self.buff_size = buff_size
        self.closed=False
        self.connect(self.address)
        self.settimeout(2)
        self.write_buffer = ""
        self.read_buffer = IO.StringIO()

    def handle_connect(self):
        logging.log("Connected to {} on {}".format(*self.address))

    def handle_close(self):
        self.closed=True
        self.close()
        logging.log("Left server {}".format(self.address[0]))

    def handle_read(self):
        self.write_buffer.write((self.buff_size))

    def handle_write(self):
        sent = self.send(self.write_buffer)
        self.write_buffer = self.write_buffer[sent:]

    def writable(self):
        return len(self.write_buffer) > 0
        
    def handle_accept(self):
        raise AttributeError("Not a server, just a client")
        
    
class IRC_member(object):
    MESSAGE = "{} \r\n"
    PRIVMSG = "PRIVMSG {} :{}\r\n"
    PONG = "PONG {}\r\n"
    NICK = "NICK {}\r\n"
    USER = "USER {} {} bla: {}\r\n"
    QUIT = "QUIT\r\n"
    JOIN = "JOIN {}\r\n"
    PART = "PART {}\r\n"
    
    def __init__(self, nick, **kwargs):
        """Constructor for IRC_member.  Stores nickname, realname and ident
        as well as info about servers and channels
        """
        
        self.nick = nick
        self.realname = nick
        self.ident = nick
        
        for key, value in kwargs.iteritems():
            self.__dict__[key] = value
            
        self.servers = {}
        self.serv_to_chan = {}
        self.serv_to_data = {}
        
        self.lock = threading.Lock()
        self.replies = {}
        
    def join_server(self, hostname, port, **kwargs):
        
        if hostname in self.servers:
            logging.warn("Already connected to {}".format(hostname))
            return 0
        
        nick = self.nick
        ident = self.ident
        realname = self.realname
        
        address = (hostname, port)
        socket_ = ServerConnection(hostname, port)
        #self.servers[address] = socket_
        self.servers[hostname] = socket_
        self.serv_to_chan[hostname] = []
        
        ## Checking if the data for this server is different from the defaults
        if kwargs:
            self.serv_to_data[hostname] = {}
            for key, value in kwargs.items():
                if key in self.__dict__:
                    self.serv_to_data[hostname][key] = value
                    locals()[key] = value
                else:
                    logging.info("key-value pair {}: {} unusued".format(key, value))
            if not self.serv_to_data[hostname]:
                del self.serv_to_data[hostname]
        
        try:
            self.send_server_message(hostname, self.NICK.format(nick))
            self.send_server_message(hostname, 
                                     self.USER.format(nick, ident, realname))
                                     
        except socket.gaierror as e:
            logging.exception(e)
            return 1
            
        except socket.error as e:
            logging.exception(e)
            return 2
            
        else:
            logging.info("Connected to {} on {}".format(*address))
            
    def leave_server(self, hostname):
        
        if hostname not in self.servers:
            logging.warning("Not connected to {}".format(hostname))
            return 0
            
        try:
            self.send_server_message(hostname, "QUIT\r\n")
            self.servers[hostname].close()
        
        except socket.error as e:
            logging.exception(e)
            logging.warning("Failed to leave server {}".format(hostname))
            return 1
            
        else:
            try:
                del self.servers[hostname]
            finally:
                try:
                    del self.serv_to_chan[hostname]
                finally:
                    try:
                        if self.serv_to_data[hostname]: 
                            del self.serv_to_data[hostname]
                    finally:
                        logging.info("Left server {}".format(hostname))
                        return 0