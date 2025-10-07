from threading import Thread
from queue import Queue

# function that the thread will run
def thread_func(q):
    while True:
        # waits until a message becomes available
        msg = q.get()
        print(f"Received message {msg}")
        if msg == 'quit':
            break

# create the queue and start the thread
q = Queue()
thread = Thread(target=thread_func, args=(q,))
thread.start()

messages = ['hello', 'world', 'quit']
for msg in messages:
    # send the message
    q.put(msg)

thread.join()