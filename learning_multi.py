import threading
import Queue
import time
def producer(n, q):
 while n > 0:
  q.put(n)
  #time.sleep(5)
  n -= 1
 q.put(None)
def consumer(q):
 while True:
 # Get item
  item = q.get()
  if item is None:
   break
  print "t-minus", item
 print "blastoff"
if __name__ == "__main__":
 # Launch threads
 q = Queue.Queue()
 prod_thread = threading.Thread(target=producer, args=(10, q))
 prod_thread.start()
 cons_thread = threading.Thread(target=consumer, args=(q,))
 cons_thread.start()
 cons_thread.join()