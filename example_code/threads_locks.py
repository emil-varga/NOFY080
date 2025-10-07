import pyvisa as vi
from threading import Thread, Lock

rm = vi.ResourceManager()
# Assuming that our pico is on the last address (usually the case)
pico = rm.open_resource(rm.list_resources()[-1],
                        read_termination='\n',
                        write_termination='\n')

def readP(lock):
    with lock: # lock is acquired
        # this will run uninterrupted
        P = pico.query(':READ:P?')
        print(P)
    #lock is released

def readT(lock):
    with lock:
        T = pico.query(':READ:T?')
        print(T)

lock = Lock()
t1 = Thread(target=readP, args=(lock,))
t2 = Thread(target=readT, args=(lock,))

t1.start()
t2.start()
t1.join()
t2.join()