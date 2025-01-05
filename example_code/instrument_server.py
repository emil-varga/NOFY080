from multiprocessing.connection import Listener, Client
from threading import Thread, Lock, Event
import time

import pyvisa as visa

#for wrong passwords
from multiprocessing.context import AuthenticationError

rm = visa.ResourceManager()
pico = rm.open_resource(rm.list_resources()[-1],
                        write_termination='\n',
                        read_termination='\n')
pico_lock = Lock()

handlers_lock = Lock()
client_handlers = []

class ClientHandler(Thread):
    def __init__(self, conn, name=None):
        super().__init__()
        self.name = name
        self.conn = conn
        self._end = Event()
    
    def stop(self):
        self._end.set()
    
    def run(self):
        try:
            while not self._end.is_set():
                if self.conn.poll():
                    msg = self.conn.recv()
                    print(f"Received : {msg}")
                    if msg == '':
                        self.conn.send('')
                    else:
                        with pico_lock:
                            resp = pico.query(msg)
                        self.conn.send(resp)
                time.sleep(0.1)
        except EOFError:
            print(f"Client {self.name} quit")
        finally:
            self.conn.close()
            with handlers_lock:
                client_handlers.remove(self)

def run(listener):
    while True:
        try:
            print("Waiting for connection")
            conn = listener.accept()
            if hasattr(listener, 'last_accepted'):
                client_name = listener.last_accepted
            else:
                client_name = None
            handler = ClientHandler(conn, client_name)
            handler.start()
            client_handlers.append(handler)
        except OSError:
             print("Stopping listening")
             break
        except AuthenticationError:
             print("Connection attempt with wrong password.")

address = ('', 0)
password = b'NOFY080_2024'
try:
    with Listener(address, authkey=password) as listener:
        actual_address = listener.address
        print('Address :', actual_address)

        t = Thread(target=run, args=(listener,))
        t.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Quitting...")

        listener.close()

        try:
            #dummy connection to force the listener to close
            with Client(actual_address, authkey=password) as c:
                c.send('')
                c.recv()
        except ConnectionRefusedError:
            pass
        t.join()
        for handler in client_handlers:
            handler.stop()

        for handller in client_handlers:
            handler.join()
finally:
    pico.close()
    rm.close()
