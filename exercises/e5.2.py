import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.fft as fft

from glob import glob
import os

def mean_temperature(fn):
    d = np.load(fn, allow_pickle=True).item()
    return 0.5*(d['Ti'] + d['Tf'])

plt.close('all')

data_dir = '../timeseries_data'
files = glob(os.path.join(data_dir, 'DM*.npy'))
files.sort(key=mean_temperature)

d = np.load(files[0], allow_pickle=True).item()

pulse = d['pulse']
N = d['samples'] # number of samples
sampling_freq = d['rate'] # sampling frequency
dt = 1/sampling_freq # time step
total_length = N*dt
ts = np.arange(0, total_length, dt) #time array


#plot the signal directly
fig, ax = plt.subplots()
ax.plot(ts, pulse)
ax.set_xlabel('time (s)')
ax.set_ylabel('signal (V)')
ax.set_title('pulse')

#power spectral density using periodogram
freqs, Pxx = sig.periodogram(pulse, sampling_freq)
fig_psd, ax_psd = plt.subplots()
ax_psd.plot(freqs, Pxx)
ax_psd.set_title('Power Spectral Density')
ax_psd.set_xlabel('frequency (Hz)')
ax_psd.set_ylabel('PSD (V$^2$/Hz)')

# general and real-signal fourier transforms
pulse_fft = fft.fft(pulse)
pulse_rfft = fft.rfft(pulse)

#fft frequencies
fft_freqs = fft.fftfreq(N, d=dt)
rfft_freqs = fft.rfftfreq(N, d=dt)

# shift the arrays so that the frequencies are not
# 0, fs/N, 2fs/N, ... (N/2)fs/N, (-N/2+1)fs/N, (-N/2+2)fs/N, ... -fs/N
# but
# (-N/2+1)fs/N, (-N/2+2)fs/N, ... -fs/N, 0, fs/N, 2fs/N, ... (N/2)fs/N
# note however, that if we want to use inverse FFT, we have to shift them back
# to original ordering
fft_freqs = fft.fftshift(fft_freqs)
pulse_fft = fft.fftshift(pulse_fft)

fig_fft, ax_fft = plt.subplots()
ax_fft.plot(rfft_freqs, pulse_rfft.real, label='real')
ax_fft.plot(rfft_freqs, pulse_rfft.imag, label='imaginary')
ax_fft.set_title('fourier transform')
ax_fft.set_xlabel('frequency (Hz)')
ax_fft.set_ylabel('spectrum (V/Hz)')
ax_fft.legend(loc='best')

ax_psd.plot(fft_freqs, np.abs(pulse_fft)**2/N*dt*2, '--')
fig_psd.tight_layout()

fig_rtheta, ax_rtheta = plt.subplots(2, 1, sharex=True)
ax_rtheta[0].plot(rfft_freqs, abs(pulse_rfft))
ax_rtheta[1].plot(rfft_freqs, np.unwrap(np.angle(pulse_rfft)))
ax_rtheta[1].set_xlabel('frequency (Hz)')
ax_rtheta[1].set_ylabel('amplitude spectrum')
ax_rtheta[0].set_ylabel('amplitude spectrum')
ax_rtheta[1].set_ylabel('phase')
fig_rtheta.tight_layout()
plt.show()
