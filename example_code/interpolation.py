import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as intp

x_raw = np.linspace(0, 1, 20)
y_raw = np.sin(4*np.pi*x_raw) + 2*np.random.normal(scale=0.1, size=len(x_raw))

y_lin = intp.interp1d(x_raw, y_raw, kind='linear')
y_cubic = intp.interp1d(x_raw, y_raw, kind='cubic')

x_interp = np.linspace(0, 1, 100)
y_noiseless = np.sin(4*np.pi*x_interp)
fig, ax = plt.subplots()
ax.plot(x_raw, y_raw, 'o', label='raw data')
ax.plot(x_interp, y_noiseless, '--', label='without noise')
ax.plot(x_interp, y_lin(x_interp), label='linear interpolation')
ax.plot(x_interp, y_cubic(x_interp), label='cubic interpolation')
ax.legend(loc='best')
fig.savefig('notes/figures/interpolation.pdf')

fig, ax = plt.subplots()
ax.plot(x_raw, y_raw, 'o', label='raw data')
ax.plot(x_interp, y_noiseless, '--', label='without noise')
for s in np.linspace(0, 3, 3):
    y_cubic_s = intp.make_splrep(x_raw, y_raw, k=3, s=s)
    ax.plot(x_interp, y_cubic_s(x_interp), label=f"s={s:.1f}")
ax.legend(loc='best')
fig.savefig('notes/figures/interpolation_s.pdf')

fig, ax = plt.subplots()
for s in np.linspace(0, 3, 3):
    y_cubic_s = intp.make_splrep(x_raw, y_raw, k=3, s=s)
    ax.plot(x_interp, y_cubic_s.derivative()(x_interp), label=f"s={s:.1f}")
ax.legend(loc='best')
fig.savefig('notes/figures/interpolation_diff.pdf')

from scipy.signal import savgol_filter
fig, ax = plt.subplots()
ax.plot(x_raw, y_raw, 'o', label='raw data')
for w in [5, 10, 15]:
    y_filt = savgol_filter(y_raw, window_length=w, polyorder=3)
    ax.plot(x_raw, y_filt, label=f"w={w:d}")
ax.legend(loc='best')
fig.savefig('notes/figures/savgol.pdf')

plt.show()