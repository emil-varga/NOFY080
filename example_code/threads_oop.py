import threading as th

class MyThread(th.Thread):
    def __init__(self, thread_name):
        # It is necessary to initialize the parent class as well
        super().__init__()
        self.thread_name = thread_name
    def run(self):
        print(f"I'm inside {self.thread_name}")

threads = []
for k in range(5):
    thread = MyThread(f"thread {k}")
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()