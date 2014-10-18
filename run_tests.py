from contextlib import closing
import IRC_sockselect
import logging
import select
import socket
import sys
import threading
import unittest


logging.basicConfig(filename='C:/Users/Dan/Desktop/Programming/Github/PyIRC/logger.log',
                    level=logging.DEBUG)
                    
ready = threading.Semaphore(0)

                    
def client_thread(asocket): 
    with closing(asocket) as client_sock:
        client_sock.send('New Thread')
        while True:
            receiving, _, _ = select.select([client_sock],
                                            [],
                                            [])
            logging.debug('ready')
            if receiving:
                client_sock.send('Ready')
                break
        ready.release()
    return
            

class server_socket(threading.Thread): 
    
    def run(self):
        with closing(socket.socket( 
                                   socket.AF_INET,
                                   socket.SOCK_STREAM
                                   )
                     ) as self.server:
                 
            self.server.bind(('localhost', 10000))
            self.server.listen(5)
            while True:
                connection, _ = self.server.accept()
                if connection:
                    client = threading.Thread(target=client_thread,
                                              args=(connection,))
                    client.start()
                    ready.acquire()
                    client.join()
                else:
                    continue
                
        return

class test_sockselect(unittest.TestCase): 

    def setUp(self):
        self.server = server_socket()
        self.server.start()
        self.IRC = IRC_sockselect.IRC_member("Nickname")
        
    def test_join_server(self): 
        self.assertEqual(self.IRC.join_server('localhost', 
                                              10000),
                         0)
        map(self.assertEqual,
            [self.IRC.nick, self.IRC.ident, self.IRC.realname],
            ['Nickname']*3
           )
        self.server.join()
        self.server = server_socket()
        self.server.start()
        del self.IRC
        self.IRC = IRC_sockselect.IRC_member("Nickname")
    
    def test_leave_server(self): pass
        
    def test_join_channel(self): pass
    
    def test_leave_channel(self): pass
        
    def test_ping(self): pass
    
    def test_send_server_message(self): pass
    
    def test_send_channel_message(self): pass
    
    def test_send_priv_message(self): pass
    
    def test_receive_all_messages(self): pass
    	
    def test_receive_message(self): pass
        
    def tearDown(self): 
        self.server.join()


if __name__ == '__main__':                  
    #suite = unittest.TestLoader().loadTestsFromTestCase(test_sockselect)
    #unittest.TextTestRunner(sys.stdout, verbosity=2).run(suite)

    server = server_socket()
    server.start()
    with closing(socket.socket(
                               socket.AF_INET,
                               socket.SOCK_STREAM
                              )
                 ) as my_sock:
        my_sock.connect(('localhost', 10000))
        logging.debug(my_sock.recv(1024))
        my_sock.send('Hello')
        logging.debug(my_sock.recv(1024))
    server.join()