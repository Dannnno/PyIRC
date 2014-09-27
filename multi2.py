import multiprocessing as mp
import time

def producer(n, q):
    while n > 0:
        q.put(n)
        time.sleep(1)
        n -= 1
    q.put(None)
    
def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print "T-minus {}".format(item)
    print "Blastoff"
    
if __name__ == "__main__":
    q = mp.Queue()
    prod_process = mp.Process(target=producer, args=(10, q))
    prod_process.start()
    
    cons_process = mp.Process(target=consumer, args=(q,))
    cons_process.start()
    cons_process.join()