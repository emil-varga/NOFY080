from multiprocessing.connection import Listener, Client
from threading import Thread
import time

# we will accept the connections in a separate thread
def handle_connections(listener):
    while True:
        # listener.accept() blocks until someone
        # tries to connect
        try:
            # accept the connection, echo back what we receive
            # and then close the connection (automatically, using 'with')
            with listener.accept() as conn:
                msg = conn.recv()
                print(f"Received {msg}")
                conn.send(f'Echo {msg}')
        except OSError:
             # OSError is raised when we try to accept
             # with a closed listener
             print("Stopping listening")
             break

# the address and port
# 'localhost' is local computer, use empty string ''
# if you want to access it over the netowrk
# port number 0 means automatic assignment by the OS
address = ('localhost', 6000)
password = b'password'
with Listener(address, authkey=password) as listener:
    print('Address :', listener.address)

    t = Thread(target=handle_connections, args=(listener,))
    t.start()
    # now the main thread will just idly sleep, waiting for
    # keyboard interrupt
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Quitting...")
    # this will signal the listener to close, however, it
    # will remain open as long as .accept() is blocking
    listener.close()
    # so create a dummy connection to unblock accept()
    # and let the listener close
    try:
        with Client(address, authkey=password) as c:
            c.send('')
            c.recv()
    except ConnectionRefusedError:
        # someone connected before our dummy connection
        # and the listener shut down, don't do anything
        pass
    t.join()