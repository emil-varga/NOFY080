import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as intp

#create "continuous" data (very high sampling rate)
T = 10 #total length of data in "time" units
xs = np.linspace(0, T, 10000)
ys = np.sin(2*np.pi*xs + 7*np.pi/3)

#interpolate the signal at high sampling rates
signal = intp.interp1d(xs, ys)

def sample(signal, dx, T=T):
    """
    Samples the quasi-continuous signal with 
    total length T with sample spacing dx
    """
    xs = np.arange(0, T, dx)
    return xs, signal(xs)

fig, ax = plt.subplots()
ax.plot(xs, ys, '-', label='true data ($f = 1$)')

ax.plot(*sample(signal, 0.13), '--o', 
        label=r'sufficiently sampled ($f_s\approx 7.69$)')
ax.plot(*sample(signal, 0.5), ':s',
        label=r'sampled at $f_N$ ($f_s = 2$)')
#this signal will be aliased
ax.plot(*sample(signal, 0.9), '-x',
        label=r'undersampled ($f_s \approx 1.11$)')

ax.set_xlabel('time')
ax.set_ylabel('signal')

ax.legend(ncol=2, frameon=False, 
          loc='lower left', bbox_to_anchor=(0.0, 1.01))
fig.tight_layout()
fig.savefig('sampling.pdf')