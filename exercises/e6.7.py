import pyvisa as vi
import numpy as np
import matplotlib.pyplot as plt
import time

from Pico import Pico

rm = vi.ResourceManager()

fig, ax = plt.subplots(layout='constrained')

t0 = time.time()
ts = [] # to store measurement times
Ps = [] # to store measured pressures
plot = ax.plot(ts, Ps)
ax.set_xlabel('time (s)')
ax.set_ylabel('pressure (Pa)')
tau = 1 #s, time constant for smoothing
try:
    with (open("pressure.txt", "w") as file,
          Pico(rm, 'ASRL/dev/ttyACM1::INSTR') as pico):
        file.write("#time(s)\tPressure(Pa)\t")
        while True:
            t = time.time() - t0
            P = pico.readP()
            print(t, P)

            # save data
            file.write(f"{t}\t{P}\n")

            # update the smoothed P
            ts.append(t)
            if len(ts) > 1:
                alpha = np.exp(-(t - ts[-2])/tau)
                Pnew = (1 - alpha)*P + alpha*Ps[-1]
            else:
                Pnew = P
            Ps.append(Pnew)

            # update the plot
            plot[0].set_data(ts, Ps)
            ax.relim()
            ax.autoscale_view()
            plt.pause(0.01)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass # keyboard interrupt is OK, all other exceptions should crash
finally:
    rm.close()