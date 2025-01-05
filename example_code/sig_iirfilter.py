import matplotlib.pyplot as plt
import numpy as np

plt.close('all')
fig, (axH, axsig) = plt.subplots(1, 2)

import scipy.signal as sig
N = 4  # filter order, this would be 24 dB/oct
fs = 1024 # samplig frequency
Wn = [200, 300] # corner frequencies of a band-pass filter

# sos = second order sections
# internal representation of the transfer function
# recommended by scipy
sos = sig.iirfilter(N, Wn, fs=fs, btype='bandpass', output='sos')

#create some signal and filter it
ts = np.arange(0, 1, 1/fs)
ys = np.sin(2*np.pi*50*ts) + np.cos(2*np.pi*250*ts)
ys_filt = sig.sosfilt(sos, ys)

freq, H = sig.sosfreqz(sos, fs=fs)
axH.plot(freq, abs(H))
axsig.plot(ts, ys, label='original')
axsig.plot(ts, ys_filt, label='filtered')

axsig.legend(loc='best')

axsig.set_xlim(0.5, 0.55)
axsig.set_xlabel('time')
axsig.set_ylabel('signal')

axH.set_xlabel('frequency')
axH.set_ylabel('filter response')
fig.tight_layout()

fig.savefig('../butter.pdf')