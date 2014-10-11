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

def client_thread(client_socket): 
    """"""
    thread = threading.Thread(target=client_socket.send,
                              args=("Hi my name is Dan"))
    
    return thread

class test_sockselect(unittest.TestCase):
    
    def setUp(self): 
        self.serv_sock = server_socket()
        self.lock = threading.Lock()
    
    def tearDown(self): 
        self.serv_sock.close()
    
    
    def test_send_server_message(self): 
        try:
            test_client = IRC_sockselect.IRC_member("Dan")   
            test_client.join_server('localhost')                       
            
            with self.lock:
                for i in range(5):
                    (client_socket, address) = self.serv_sock.accept()
                    ct = client_thread(client_socket)
                    ct.run()
        finally:
            test_client.close()
    
        
suite = unittest.TestLoader().loadTestsFromTestCase(test_sockselect)
unittest.TextTestRunner(sys.stdout, verbosity=2).run(suite)                                                                                