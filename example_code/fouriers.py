import numpy as np
import scipy.fft as fft
from scipy.signal import periodogram

import matplotlib.pyplot as plt

#first create some signal
N = 200 #total number of points
dt = 0.01 # sampling period, sampling frequency = 1/dt = 100

#time
ts = np.arange(N)*dt
#signal: sum of two sine waves
ys = np.sin(2*np.pi*10*ts + np.pi/7) + np.sin(2*np.pi*13*ts + np.pi/17)

#plot the signal and label the axes
fig, (ax_sig, ax_fft) = plt.subplots(2, 1)
ax_sig.plot(ts, ys)
ax_sig.set_xlabel('time (s)')
ax_sig.set_ylabel('signal')

ax_fft.set_xlabel('frequency (Hz)')
ax_fft.set_ylabel('normalized FFT or PSD')

#compute the discrete Fourier transform of the signal
fft_frequencies = fft.fftfreq(N, dt)
Y_fft = fft.fft(ys)
ax_fft.plot(fft_frequencies, Y_fft.real/abs(Y_fft).max(), label='real')
ax_fft.plot(fft_frequencies, Y_fft.imag/abs(Y_fft).max(), label='imag')

#power spectral density
#periodogram() also returns the frequences
psd_freq, psd = periodogram(ys, fs=1/dt) #fs = sampling frequency
ax_fft.plot(psd_freq, psd/psd.max(), label='PSD')
ax_fft.legend(loc='best', frameon=False)
fig.tight_layout()
fig.savefig('fouriers.pdf')
plt.show()