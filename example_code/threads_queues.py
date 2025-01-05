import pyvisa as vi
import matplotlib.pyplot as plt
from threading import Thread, Event
from queue import Queue
import time

class Plotter(Thread):
    def __init__(self, queue):
        super().__init__()
        self.fig, self.ax = plt.subplots()
        self.xdata = []
        self.ydata = []
        self.line, = self.ax.plot(self.xdata, self.ydata, '-o')
        self.queue = queue
        self.end = Event()
    
    def update_plot(self):
        if len(self.xdata) > 0:
            self.line.set_xdata(self.xdata)
            self.line.set_ydata(self.ydata)
            xmin, xmax = min(self.xdata), max(self.xdata)
            ymin, ymax = min(self.ydata), max(self.ydata)
            xmid = 0.5*(xmin + xmax)
            ymid = 0.5*(ymin + ymax)
            dx = xmax - xmin
            dy = ymax - ymin
            self.ax.set_xlim(xmid - 0.55*dx, xmid + 0.55*dx)
            self.ax.set_ylim(ymid - 0.55*dy, ymid + 0.55*dy)
            # plt.draw()

    def pull_data(self):
        # keep reading the data from the queue as long
        # as anything is available
        while not self.queue.empty():
            # if get() is called on an empty queue, it blocks
            # until something becomes available (or a timeout occurs)
            data = self.queue.get()
            print("Received ", data)
            #we can send anything through the queue, for example
            #either a data point or a command to quit
            match data:
                case (x, y):
                    self.xdata.append(x)
                    self.ydata.append(y)
                case 'quit':
                    print("Quitting")
                    self.end.set()
    
    def run(self):
        while not self.end.is_set():
            self.pull_data()
            self.update_plot()
            time.sleep(0.5)


rm = vi.ResourceManager()
pico = rm.open_resource(rm.list_resources()[-1],
                        read_termination='\n',
                        write_termination='\n')

data_queue = Queue()
plotter = Plotter(data_queue)
plotter.start()
try:
    t0 = time.time()
    while True:
        t = time.time() - t0
        P = float(pico.query(':READ:P?'))
        print("Sending ", t, P)
        data_queue.put((t, P))
        # the following line updates all open matplotlib plots
        # it MUST be run from the main thread
        plt.pause(0.01)
finally:
    data_queue.put('quit')
    plotter.join()