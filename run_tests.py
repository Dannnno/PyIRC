from contextlib import closing
import logging
import socket
import sys
import threading
import unittest


logging.basicConfig(filename='logger.log',
                    level=logging.DEBUG)


class server_socket(threading.Thread): 
    
    def run(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as self.server:
            self.server.bind(('localhost', 10000))
            self.server.listen(5)
            while True:
                (connection, address) = self.server.accept()
                if connection:
                    print connection, address
                    break
                else:
                    continue
        return

class test_sockselect(unittest.TestCase): 

    def setUp(self):
        self.server = server_socket()
        self.server.start()


if __name__ == '__main__':
    server = server_socket()
    server.start()
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as my_sock:
        my_sock.connect(('localhost', 10000))
