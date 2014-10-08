import unittest
import mock
import sys
import IRC_sockselect


class test_sockselect(unittest.TestCase):
    
    def setUp(self): pass
    
    def tearDown(self): pass
    
    
    @mock.patch('IRC_sockselect.socket.send')
    @mock.patch('IRC_sockselect.socket')
    def test_send_server_message(self, 
                                  mock_socket, 
                                  mock_send): 
                                  
        my_irc = IRC_sockselect.IRC_member("Dan")
        
        my_socket = mock_socket.socket(mock_socket.AF_INET,
                                       mock_socket.SOCK_STREAM)

        my_irc.servers["irc.foonetic.net"] = my_socket.connect((
                                        mock_socket.gethostbyname("irc.foonetic.net"),
                                        6667))

        sys.stdout.write(str( my_irc))
        sys.stdout.write(str( my_socket))
        my_socket.mock_send("Hello")
        my_socket.recv()
        
suite = unittest.TestLoader().loadTestsFromTestCase(test_sockselect)
unittest.TextTestRunner(sys.stdout, verbosity=2).run(suite)                                                                                