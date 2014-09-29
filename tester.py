import socket
import multiprocessing as mp
import types
import copy_reg
import pickle


def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

class a(object):
    
    def __init__(self):
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect((socket.gethostbyname("irc.foonetic.net"),
                                                            6667))
        self.servers = {}
        self.servers["irc.foonetic.net"] = sock1
    
    def method(self, thingy):
        self.servers[thingy].send("JOIN DAN\r\n")
        return "1"
        
    def oth_method(self):
        pool = mp.Pool()
        print pickle.dumps(self.method)
        a = pool.map(self.method, self.servers.keys())
        pool.close()
        pool.join()

if __name__ == "__main__":
    b = a()
    b.oth_method()