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

from contextlib import closing
from testfixtures import LogCapture
import IRC_sockselect
import logging
import select
import socket
import threading
import unittest


logging.basicConfig(filename='C:/Users/Dan/Desktop/Programming/Github/PyIRC/logger.log',
                    level=logging.DEBUG)
                    
ready = threading.Semaphore(0)

                    
def client_thread(asocket): 
    client_sock = asocket
    client_sock.send('New Thread')
    while True:
        R, _, _ = select.select([client_sock],
                                [],
                                [])
        if R:
            try:
                message = client_sock.recv(1024)
            except socket.error: 
                ## Takes care of race conditions in test_leave_server
                client_sock.close()
                break
            else:
                if 'Done' in message:
                    client_sock.close()
                    break
                elif 'pingpong' in message:
                    client_sock.send('PING 1234567890')
                elif 'PONG 1234567890' in message:
                    client_sock.send('PINGPONG')
                else:
                    client_sock.send(message) 
    ready.release()
    return
            

class server_socket(threading.Thread): 
    
    #def __init__(self, server='localhost', port=10000):
    #    super(server_socket, self).__init__()
    #    self.server = server
    #    self.port = port
    
    def run(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
            ## self.server.bind((self.server, self.port))
            self.server.bind(('localhost', 10000))
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
        finally:
            self.server.close()        
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
        self.IRC.send_server_message('localhost', 'Done')
        
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
        self.IRC.send_server_message('localhost', 'Done')
    
    def test_leave_server(self): 
        self.IRC.join_server('localhost', 10000)
        self.IRC.send_server_message('localhost', 'Done')
        self.assertEqual(self.IRC.leave_server('localhost'),
                         0)        
        
    def test_join_channel(self): 
        self.IRC.join_server('localhost', 10000)
        self.assertEqual(self.IRC.join_channel('localhost', 
                                               '#temp-channel'),
                         0)
        self.IRC.send_server_message('localhost', 'Done')
    
    @unittest.skip("Broken")
    def test_leave_channel(self): ## Throws an error
        try:
            self.IRC.join_server('localhost', 10000)
            self.IRC.join_channel('localhost', '#temp-channel')
            self.assertEqual(self.IRC.leave_channel('localhost', 
                                                    '#temp-channel'),
                            0)
            self.IRC.send_server_message('localhost', 'Done')
        except Exception as e:
            print e
            
    @unittest.skip("Broken")
    def test_ping(self): 
        self.IRC.join_server('localhost', 10000)
        self.IRC.send_server_message('localhost', 'pingpong')
        self.IRC.receive_message('localhost')
        print self.IRC.replies
        
    def test_send_server_message(self): 
        self.IRC.join_server('localhost', 10000)
        self.assertEqual(self.IRC.send_server_message('localhost',
                                                      'anything'),
                         0)
        self.IRC.send_server_message('localhost', 'Done')
        
    def test_send_channel_message(self): 
        self.IRC.join_server('localhost', 10000)
        self.IRC.join_channel('localhost', '#temp-channel')
        self.assertEqual(self.IRC.send_channel_message('localhost',
                                                       '#temp-channel',
                                                       'anything'),
                         0)
        self.IRC.send_server_message('localhost', 'Done')
        
    def test_send_priv_message(self): 
        self.IRC.join_server('localhost', 10000)
        self.assertEqual(self.IRC.send_privmsg('localhost',
                                               'some_user',
                                               'anything'),
                         0)
        self.IRC.send_server_message('localhost', 'Done')
        
    @unittest.skip("Not yet implemented")
    def test_receive_all_messages(self): pass
    @unittest.skip("Not yet implemented")
    def test_receive_message(self): pass
        
    def tearDown(self): 
        self.server.join()
        del self.IRC
        self.l.uninstall()


if __name__ == '__main__':   
    import sys    
    suite = unittest.TestLoader().loadTestsFromTestCase(test_sockselect)
    unittest.TextTestRunner(sys.stdout, verbosity=2).run(suite)
