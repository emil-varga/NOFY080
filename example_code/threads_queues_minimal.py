from threading import Thread
from queue import Queue

def thread_func(q):
    while True:
        # waits until a message becomes available
        msg = q.get()
        print(f"Received message {msg}")
        if msg == 'quit':
            break

q = Queue()
thread = Thread(target=thread_func, args=(q,))
thread.start()

messages = ['hello', 'world', 'quit']
for msg in messages:
    #send the message
    q.put(msg)

thread.join()