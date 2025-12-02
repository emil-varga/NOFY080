import pyvisa as vi
from Pico import Pico
from threading import Thread, Lock, Event
import time

#to synchronize access to the Pico
pico_lock = Lock()

#to signal the threads that they should end
end_event = Event()

#threads run a specific function
#the blinking will be handled by its own function
def blinker(pico, n, T):
    while not end_event.is_set():
        # pico.led() relies on query, which is write() and read()
        # we must not be interrupted by another thread between write() and read()
        # otherwise the communication might become jumbled
        
        # When one thread acquires the lock, all others have to wait before they
        # are allowed to acquire it for themselves
        with pico_lock:
            pico.led(n, 1)
        time.sleep(T/2)
        with pico_lock:
            pico.led(n, 0)
        time.sleep(T/2)

if __name__ == '__main__':
    # to store the thread objects
    threads = []
    # the blinking periods
    periods = [0.1, 0.2, 0.5, 1, 2]
    rm = vi.ResourceManager()
    with Pico(rm) as pico:
        # create the thread objects, start the threads and save them
        for k, T in enumerate(periods):
            t = Thread(target=blinker, args=(pico, k, T))
            t.start()
            threads.append(t)
        
        #threads are running, put the main thread to sleep waiting for an interrupt
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            # keyboard interrupt is not an error, just a way to escape from the
            # infinite while loop
            print("Quitting...")
        
        #we set the event, next time the threads check, event.is_set() will be True
        end_event.set()

        #we clean up the remains of the threads by joining them back into the main thread
        for t in threads:
            t.join()