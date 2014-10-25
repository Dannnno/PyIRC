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
    from testfixtures import LogCapture
    import IRC_sockselect
    import select
    import socket
    import sys
    import threading
    import unittest

                    
ready = threading.Semaphore(0)

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
                    
def client_thread(asocket): 
    client_sock = asocket
    while True:
        R, _, _ = select.select([client_sock],
                                [],
                                [])
        if R:
            try:
                message = client_sock.recv(1024)
            except socket.error: 
                ## Takes care of race conditions due to test_leave_server
                client_sock.close()
                break
            else:
                if 'Done' in message:
                    client_sock.close()
                    break
                else:
                    client_sock.send(message) 
    ready.release()
    return
            

class server_socket(threading.Thread): 
    
    def __init__(self, server='localhost', port=10000):
        super(server_socket, self).__init__()
        self.hostname = server
        self.port = port        
    
    def run(self):
        with closing(socket.socket(
                                    socket.AF_INET,
                                    socket.SOCK_STREAM
                                   )) as self.server:
        
            self.server.bind((self.hostname, self.port))
            self.server.listen(5)
            while True:
                connection, _ = self.server.accept()
                if connection:
                    client = threading.Thread(target=client_thread,
                                              args=(connection,))
                    client.start()
                    break                        
                else:
                    continue
            ready.acquire()
            client.join()       
        return


class test_sockselect(unittest.TestCase): 

    def setUp(self):
        self.server = server_socket()
        self.server.start()
        self.IRC = IRC_sockselect.IRC_member("Nickname")
        self.l = LogCapture()
        
    def test_join_server(self): 
        self.assertEqual(self.IRC.join_server('localhost', 
                                              10000),
                         0)
        map(self.assertEqual,
            [self.IRC.nick, self.IRC.ident, self.IRC.realname],
            ['Nickname']*3
           )
        
    def test_join_server2(self):
        self.assertEqual(self.IRC.join_server('localhost', 
                                              port=10000,
                                              nick="Nick",
                                              ident="Ident",
                                              realname="Realname"),
                         0)
        map(self.assertEqual,
            [self.IRC.serv_to_data['localhost']['nick'],
             self.IRC.serv_to_data['localhost']['ident'],
             self.IRC.serv_to_data['localhost']['realname'],
            ],
            ['Nick', 'Ident', 'Realname']
           )
    
    def test_leave_server(self): 
        self.IRC.join_server('localhost', 10000)
        self.assertEqual(self.IRC.leave_server('localhost'),
                         0)        
        
    def test_join_channel(self): 
        self.IRC.join_server('localhost', 10000)
        self.assertEqual(self.IRC.join_channel('localhost', 
                                               '#temp-channel'),
                         0)
    
    def test_leave_channel(self): 
        self.IRC.join_server('localhost', 10000)
        self.IRC.join_channel('localhost', '#tchannel')
        self.assertEqual(self.IRC.leave_channel('localhost', '#tchannel'), 0)
            
    def test_ping(self): 
        self.IRC.join_server('localhost', 10000)
        self.assertEqual(self.IRC.ping_pong(self.IRC.servers['localhost'], 
                                            "1234567890"),
                         0)
        
    def test_send_server_message(self): 
        self.IRC.join_server('localhost', 10000)
        self.assertEqual(self.IRC.send_server_message('localhost',
                                                      'anything'),
                         0)
     
    def test_send_channel_message(self): 
        self.IRC.join_server('localhost', 10000)
        self.IRC.join_channel('localhost', '#temp-channel')
        self.assertEqual(self.IRC.send_channel_message('localhost',
                                                       '#temp-channel',
                                                       'anything'),
                         0)
        
    def test_send_priv_message(self): 
        self.IRC.join_server('localhost', 10000)
        self.assertEqual(self.IRC.send_privmsg('localhost',
                                               'some_user',
                                               'anything'),
                         0)
        
    def test_receive_all_messages(self): 
        self.IRC.replies['localhost'] = []
        self.IRC.join_server('localhost', 10000)
        map(self.IRC.send_server_message,
            ['localhost']*3,
            ['whatever', 'something else', 'last thing'])
        with capture():
            self.assertEqual(self.IRC.receive_all_messages(), 0)
        
        
    
    def test_receive_message(self): 
        self.IRC.replies['localhost'] = []
        self.IRC.join_server('localhost', 10000)
        map(self.IRC.send_server_message,
            ['localhost']*3,
            ['whatever', 'something else', 'last thing'])
        self.IRC.receive_message(('localhost',))
        self.assertEqual(self.IRC.replies['localhost'],
                         [
                          'NICK Nickname',
                          'USER Nickname Nickname bla: Nickname',
                          'whatever',
                          'something else',
                          'last thing'
                         ]
                        )
        
    def tearDown(self): 
        for server in self.IRC.servers:
            self.IRC.send_server_message(server, 'Done')
        self.server.join()
        del self.IRC
        self.l.uninstall()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_sockselect)
    unittest.TextTestRunner(sys.stdout, verbosity=1).run(suite)
