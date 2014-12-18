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
    from contextlib import contextmanager
    import asyncore
    import socket
    import sys
    import unittest
    
    from textfixtures import LogCapture
    
    import IRC_sockasyncore as IRC
    
    
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
    
    
class SocketHandler(asyncore.dispatcher_with_send):
    """Just echos the message back to whoever sent it"""
    
    def handle_read(self):
        while True:
            data = self.recv(8192)
            if data:
                self.send(data)
            else:
                break


class ServerSocket(asyncore.dispatcher):
    
    def __init__(self, hostname='localhost', port=10000):
        super(ServerSocket, self).__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = hostname, port
        self.set_reuse_addr()
        self.bind(self.address)
        self.listen(5)
        
    def handle_accept(self):
        socket_, _ = self.accept()
        SocketHandler(socket_)

                
class test_sockasyncore(unittest.TestCase):

    pass
                        
                        
class test_ServerConnection(unittest.TestCase):
    
    pass
        
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_sockasyncore)
    unittest.TextTestRunner(sys.stdout, verbosity=1).run(suite)
