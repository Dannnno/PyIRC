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
    from contextlib import closing, contextmanager
    import select
    import socket
    import sys
    import threading
    import time
    import unittest
    
    from testfixtures import LogCapture
    
    import IRC_sockselect as IRC
    
    
@contextmanager
def capture():
    oldout, olderr = sys.stdout, sys.stderr
    
    try:
        out=[IO.StringIO(), IO.StringIO()]
        sys.stdout, sys.stderr = out
        yield out
        
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()
    
    
def client_thread(client_socket, client_event):
    while not client_event.isSet():
        ready, _, _ = select.select([client_socket],
                                    [],
                                    [])
        if ready:
            try:
                message = client_socket.recv(1024)
            except socket.error: 
                ## Takes care of race conditions due to test_leave_server
                client_socket.close()
                client_event.set()
            else:
                if 'Done' in message:
                    client_socket.close()
                    client_event.set()
                else:
                    client_socket.send(message) 
    return

    
class ServerSocket(threading.Thread):
    
    def __init__(self, hostname='localhost', port=10000, timeout=100000):
        super(ServerSocket, self).__init__()
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.now = time.time()
        self.event = threading.Event()
        # Maps from a thread ID to a tuple of form 
        # (socket, threading.Event, threading.Thread)
        self.clients = {}
        
    def run(self):
        with closing(socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)) as self.server:
            self.server.bind((self.hostname, self.port))
            self.server.listen(5)
            while not self.event.isSet():
                connection, _ = self.server.accept()
                if connection:
                    event = threading.Event()
                    client = threading.Thread(target=client_thread, 
                                              args=(connection,
                                                    event))
                    client.start()
                    self.clients[client.ident] = connection, event, client
                    
                for id_, (socket_, event_, client_) in self.clients.items():
                    if event_.isSet():
                        client_.join()
                        del self.clients[id_]
                
class test_sockselect(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = ServerSocket()
        cls.server.start()
        cls.log_capture = LogCapture()
        
    @classmethod
    def tearDownClass(cls):
        cls.server.event.set()
        cls.server.join()
        cls.log_capture.uninstall()
        
    def setUp(self):
        self.IRC_ = IRC.IRC_member("Nickname")
        
    def tearDown(self):
        for server in self.IRC_.servers:
            self.IRC_.send_server_message(server, 'Done')
            
    def test_join_server(self): 
        self.assertEqual(self.IRC_.join_server('localhost', 
                                              10000),
                         0)
        map(self.assertEqual,
            [self.IRC_.nick, self.IRC_.ident, self.IRC_.realname],
            ['Nickname']*3
           )
    
    def test_join_server2(self):
        self.assertEqual(self.IRC_.join_server('localhost', 
                                              port=10000,
                                              nick="Nick",
                                              ident="Ident",
                                              realname="Realname"),
                         0)
        map(self.assertEqual,
            [self.IRC_.serv_to_data['localhost']['nick'],
             self.IRC_.serv_to_data['localhost']['ident'],
             self.IRC_.serv_to_data['localhost']['realname'],
            ],
            ['Nick', 'Ident', 'Realname']
           )

    def test_leave_server(self): 
        self.IRC_.join_server('localhost', 10000)
        self.assertEqual(self.IRC_.leave_server('localhost'),
                         0)        
   
    def test_join_channel(self): 
        self.IRC_.join_server('localhost', 10000)
        self.assertEqual(self.IRC_.join_channel('localhost', 
                                               '#temp-channel'),
                         0)

    def test_leave_channel(self): 
        self.IRC_.join_server('localhost', 10000)
        self.IRC_.join_channel('localhost', '#tchannel')
        self.assertEqual(self.IRC_.leave_channel('localhost', '#tchannel'), 0)
           
    def test_send_server_message(self): 
        self.IRC_.join_server('localhost', 10000)
        self.assertEqual(self.IRC_.send_server_message('localhost',
                                                      'anything'),
                         0)
 
    def test_send_channel_message(self): 
        self.IRC_.join_server('localhost', 10000)
        self.IRC_.join_channel('localhost', '#temp-channel')
        self.assertEqual(self.IRC_.send_channel_message('localhost',
                                                       '#temp-channel',
                                                       'anything'),
                         0)
    
    def test_send_priv_message(self): 
        self.IRC_.join_server('localhost', 10000)
        self.assertEqual(self.IRC_.send_privmsg('localhost',
                                               'some_user',
                                               'anything'),
                         0)
    
    def test_receive_all_messages(self): 
        self.IRC_.replies['localhost'] = []
        self.IRC_.join_server('localhost', 10000)
        map(self.IRC_.send_server_message,
            ['localhost']*3,
            ['whatever', 'something else', 'last thing'])
        with capture():
            self.assertEqual(self.IRC_.receive_all_messages(), 0)
    
    def test_receive_message(self): 
        self.IRC_.replies['localhost'] = []
        self.IRC_.join_server('localhost', 10000)
        map(self.IRC_.send_server_message,
            ['localhost']*3,
            ['whatever', 'something else', 'last thing'])
        self.IRC_.receive_message(('localhost',))
        self.assertEqual(self.IRC_.replies['localhost'],
                         [
                          'NICK Nickname',
                          'USER Nickname Nickname bla: Nickname',
                          'whatever',
                          'something else',
                          'last thing'
                         ]
                        )

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_sockselect)
    unittest.TextTestRunner(sys.stdout, verbosity=1).run(suite)
