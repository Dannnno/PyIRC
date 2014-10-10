import unittest
import socket
import sys
import IRC_sockselect
import threading


class server_socket(socket.socket):
    
    def __init__(self):
        super(socket.socket, self).__init__(socket.AF_INET,
                                            socket.SOCK_STREAM)
                                            
        self.bind(('localhost', 80))
        self.listen(5)                                            


class test_sockselect(unittest.TestCase):
    
    def setUp(self): 
        self.serv_sock = server_socket()
        self.lock = threading.Lock()
    
    def tearDown(self): 
        self.serv_sock.close()
    
    
    def test_send_server_message(self): 
        try:
            test_client = IRC_sockselect.IRC_member("Dan")                          
            
            with self.lock:
                (client_socket, address) = self.serv_sock.accept()
                ct = client_thread(clientsocket)
                ct.run()
        finally:
            test_client.close()
    
        
suite = unittest.TestLoader().loadTestsFromTestCase(test_sockselect)
unittest.TextTestRunner(sys.stdout, verbosity=2).run(suite)                                                                                