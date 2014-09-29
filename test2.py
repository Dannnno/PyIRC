import socket
import time
import threading
import select
import Queue
import multiprocessing as mp
from multiprocessing import dummy as dum

class a(object):
    
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((socket.gethostbyname("irc.foonetic.net"), 6667))
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect((socket.gethostbyname("irc.binhex.org"), 6667))
        sock.setblocking(0)
        sock2.setblocking(0)
        sock.send("JOIN Dan\r\n")
        sock2.send("JOIN Dan\r\n")
        self.servers = {}
        self.servers["foonetic"] = sock
        self.servers["binhex"] = sock2
        self.lock = threading.Lock()
        self.items = []
        
    def send_mess(self, sock):
        a = sock.recv(4096)
        with self.lock:
            self.items.append(a)
        
    def my_method(self):
        ready, _, _ = select.select(self.servers.values(), [], [], 5)
        
        if ready:
            pool = dum.Pool()
            pool.map(self.send_mess, ready)
            
            with self.lock:
                items, self.items = self.items, []
            for item in items:
                print item                                          
            
if __name__ == "__main__":
    b = a()
    time.sleep(10)
    b.my_method()
                                                
                
        