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

    
class IRC_member(object):
    
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