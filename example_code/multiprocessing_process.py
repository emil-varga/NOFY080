from multiprocessing import Process, Event, Queue
from queue import Empty
import time

class MyProcess(Process):
    def __init__(self, procname, end, data):
        super().__init__()
        self.procname = procname
        self.end = end
        self.data = data
    def run(self):
        while True:
            try:
                msg = self.data.get(timeout=1)
                print(f"{self.procname} received: {msg}")
            except Empty:
                print(f"{self.procname}: Nothing in queue")
                time.sleep(0.1)
            
            if self.end.is_set() and self.data.empty():
                break

if __name__ == '__main__':
    data_queue = Queue()
    end_event = Event()
    process_pool = []
    for k in range(5):
        p = MyProcess(f'proc{k}', end_event, data_queue)
        p.start()
        process_pool.append(p)

    for k in range(10):
        data_queue.put(f"message {k}")
        time.sleep(0.2)

    end_event.set()
    for p in process_pool:
        p.join()