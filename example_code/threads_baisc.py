import threading as th

def func(thread_name):
    print(f"I'm inside {thread_name}")

threads = []
for k in range(5):
    thread = th.Thread(target=func, args=(f"thread {k}",))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()