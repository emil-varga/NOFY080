import threading as th

def func(thread_name):
    print(f"I'm inside {thread_name}")

threads = []
# create and start 5 threads and save them to a list
for k in range(5):
    thread = th.Thread(target=func, args=(f"thread {k}",))
    thread.start()
    threads.append(thread)

# wait for all threads to finish
for thread in threads:
    thread.join()