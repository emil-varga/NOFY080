import numpy as np
import matplotlib.pyplot as plt

from glob import glob
import os
import time

data_dir = '../timeseries_data'
files = glob(os.path.join(data_dir, 'DM*.npy'))

times = []
Ts = []
for file in files:
    print(file)
    time_str = time.strptime(os.path.basename(file), 'DM_%Y%m%d-%H%M%S.npy')
    t = time.mktime(time_str)
    d = np.load(file, allow_pickle=True).item()
    T = 0.5*(d['Ti'] + d['Tf'])
    times.append(t)
    Ts.append(T)

times = np.array(times)
Ts = np.array(Ts)
ix = np.argsort(times)
times = times[ix]
Ts = Ts[ix]
fig, ax = plt.subplots()
ax.scatter((times - times[0])/3600, Ts)
ax.set_xlabel('time (hrs)')
ax.set_ylabel('mean temperature (K)')
fig.tight_layout()
plt.show()








