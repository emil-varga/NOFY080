import pyvisa as vi
from threading import Thread, Lock, Event
import time()

rm = vi.ResourceManager()
pico = rm.open_resource(rm.list_resources()[-1],
                        read_termination='\n',
                        write_termination='\n')

def keep_reading_P(lock, end_event):
    #keep running until the end_event is set
    while not end_event.is_set():
        with lock: # lock is acquired
            # this will run uninterrupted
            P = pico.query(':READ:P?')
            print(P)
        #lock is released
        time.sleep(1)

lock = Lock()
end = Event()
thr = Thread(target=keep_reading_P, args=(lock,end))
t0 = time.time()
thr.start()
# measure for five second and then signal the thread to end
while True:
    if time.time() - t0 > 5:
        end.set()
        break
    time.sleep(0.1)
thr.join()