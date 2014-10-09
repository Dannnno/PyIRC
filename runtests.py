import unittest
import socket
import sys
import IRC_sockselect
import threading


class test_sockselect(unittest.TestCase):
    
    def setUp(self): 
        self.serversocket = socket.socket(socket.AF_INET, 
                                          socket.SOCK_STREAM)
        self.serversocket.bind(('localhost', 80))
        self.serversocket.listen(5)
        self.lock = threading.Lock()
    
    def tearDown(self): 
        self.serversocket.close()
    
    
    def test_send_server_message(self): 
        
        test_client = IRC_sockselect.IRC_member("Dan")                          
        
        with self.lock:
            (client_socket, address) = self.serversocket.accept()
            ct = client_thread(clientsocket)
            ct.run()
            
    
        
suite = unittest.TestLoader().loadTestsFromTestCase(test_sockselect)
unittest.TextTestRunner(sys.stdout, verbosity=2).run(suite)                                                                                