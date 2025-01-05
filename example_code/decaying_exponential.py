import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft

fig, (axt, axf) = plt.subplots(1, 2, figsize=(5, 2.5))

tau = 1
dt = 0.1
t = np.arange(0, 5, dt)
y = np.exp(-t/tau)*np.sin(2*np.pi*2*t)
axt.plot(t, y)

Y = fft.rfft(y)
freq = fft.rfftfreq(len(t), dt)
axf.plot(freq, Y.real, label='real')
axf.plot(freq, Y.imag, label='imag')

axt.set_xlabel('time')
axt.set_ylabel('signal')

axf.set_xlabel('frequency')
axf.set_ylabel('FT')
axf.legend(loc='best', frameon=False)
fig.tight_layout()

fig.savefig('../decaying_exponential.pdf')