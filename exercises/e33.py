import pyvisa as vi
from Pico import Pico
from threading import Thread, Lock, Event
import matplotlib.pyplot as plt
import time

# on my computer tkagg backend doesn't steal focus
# so you can actually type something into the command
# line
import matplotlib
matplotlib.use('tkagg')

data_lock = Lock()

# we will run the user interaction in a separate thread
# We can also define threads by inheriting from the Thread object
class UserInteraction(Thread):
    def __init__(self, times, pressures):
        #initializes the parent object
        super().__init__()
        self.times = times
        self.pressures = pressures
        self._end = Event()
    
    # this is the method that runs when the thread starts
    def run(self):
        while self.keep_running():
            #ask the user for input and process it
            command = input("> ")
            match command:
                case 'quit':
                    self.quit()
                    break
                case 'clear':
                    self.clear_data()
                case u:
                    print(f"Unknown command {u}")
    
    #signal everyone to quit
    def quit(self):
        self._end.set()
    
    #check whether we should keep running
    def keep_running(self):
        return not self._end.is_set()

    def clear_data(self):
        with data_lock:
            self.times.clear()
            self.pressures.clear()        


if __name__ == '__main__':
    #create lists to store the data and plot an empty plot
    times = []
    pressures = []
    fig, ax = plt.subplots()
    line, = ax.plot(times, pressures)
    plt.pause(0.1)

    #create the user interaction thread
    user = UserInteraction(times, pressures)
    rm = vi.ResourceManager()
    try:
        with Pico(rm) as pico:
            #start the user interaction once we have the pico
            user.start()

            try:
                t0 = time.time()
                while user.keep_running():
                    # ALWAYS modify shared data under lock
                    with data_lock:
                        times.append(time.time() - t0)
                        pressures.append(pico.readP())
                    # this sets the data the line is supposed to show
                    # but does not update the axis limits, which we
                    # have to do ourselves
                    line.set_xdata(times)
                    line.set_ydata(pressures)
                    # if we have at least 2 points calculate the min/max
                    if len(times) > 2:
                        xmin, xmax = min(times), max(times)
                        ymin, ymax = min(pressures), max(pressures)
                        ax.set_xlim(xmin, xmax)
                        ax.set_ylim(ymin, ymax)
                    plt.pause(0.1)
            except KeyboardInterrupt:
                # keyboard interrupt is not an error, just a way to escape from the
                # infinite while loop
                print("Quitting...")
            
            # indicate the user interaction thread that it should quit
            # and wait for it to finish
            user.quit()
            user.join()
    finally:
        rm.close()