import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.ndimage as nd
import os
from glob import glob

def mean_temperature(fn):
    d = np.load(fn, allow_pickle=True).item()
    return 0.5*(d['Ti'] + d['Tf'])

plt.close('all')

data_dir = '../timeseries_data'
files = glob(os.path.join(data_dir, 'DM*.npy'))
files.sort(key=mean_temperature)

d = np.load(files[0], allow_pickle=True).item()
img = []
temperatures = []
for file in files:
    d = np.load(file, allow_pickle=True).item()
    fs = d['rate']
    x = d['timeseries'][0,:]
    T = mean_temperature(file)
    freq, Pxx = sig.periodogram(x, fs=fs)
    temperatures.append(T)
    img.append(Pxx)

# exercise 22
avg_window = 0.05 # average with sliding window of 50 mK
img = np.array(img)
temperatures = np.array(temperatures)
img_avg = np.zeros_like(img)
for k, T in enumerate(temperatures):
    ix = abs(temperatures - T) < avg_window/2
    # if we wanted to average only directly neighbouring lines
    #if k == 0:
    #    ix = [0, 1]
    #elif k == len(temperatures) - 1:
    #    ix = [-2, -1]
    #else:
    #    ix = [k-1, k, k+1]
    img_avg[k,:] = np.average(img[ix,:], axis=0)

fig, (ax, ax_avg) = plt.subplots(1, 2, sharex=True,
                                 sharey=True)

#img = nd.gaussian_filter(img, (1, 10)) #
im = ax.imshow(img, aspect='auto', origin='lower',
               vmax=1e-4,
               extent=[freq.min(), freq.max(),
                       min(temperatures), max(temperatures)])

im_avg = ax_avg.imshow(img_avg, aspect='auto', origin='lower',
                       vmax=1e-4,
                       extent=[freq.min(), freq.max(),
                       min(temperatures), max(temperatures)])

cbar = fig.colorbar(im_avg)
ax.set_xlabel('freq')
ax.set_ylabel('$T$ (K)')
cbar.set_label('amplituda')
plt.show()
