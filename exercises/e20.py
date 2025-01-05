import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

from glob import glob
import os
import time

def mean_temperature(fn):
    d = np.load(fn, allow_pickle=True).item()
    return 0.5*(d['Ti'] + d['Tf'])

plt.close('all')

data_dir = '../timeseries_data'
files = glob(os.path.join(data_dir, 'DM*.npy'))
files.sort(key=mean_temperature)

d = np.load(files[0], allow_pickle=True).item()


pulse = d['pulse']
N = d['samples'] # number of sample
sampling_freq = d['rate'] # sampling frequency
dt = 1/sampling_freq # time step
ts = np.arange(0, dt*N, dt)

x = d['timeseries'][0,:]
X = np.fft.rfft(x)
F = np.fft.rfft(pulse)
freqs = np.fft.rfftfreq(N, dt)

fig, ax = plt.subplots()
ax.plot(ts, x)
ax.set_title('signal')
fig.tight_layout()

ix = np.logical_and(freqs < 3000,
                    freqs > 500)

fig_spec, ax_spec = plt.subplots()
ax_spec.plot(freqs[ix], np.real(X/F)[ix])
ax_spec.plot(freqs[ix], np.imag(X/F)[ix])
ax_spec.set_title('spectrum')
fig_spec.tight_layout()

fxx, Pxx = sig.periodogram(x, fs=sampling_freq)
fig_psd, ax_psd = plt.subplots()
ax_psd.plot(fxx, Pxx)
ax_psd.set_title('power spectral density')
fig_psd.tight_layout()
plt.show()
