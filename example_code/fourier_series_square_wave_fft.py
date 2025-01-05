import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft

ts = np.linspace(0, 1, 1001)
dt = ts[1] - ts[0]
N = len(ts)
ys = np.zeros_like(ts)
start = 0.125
ys[np.logical_and(ts >= start, ts < start + 0.5)] = 1

plt.close('all')
fig, ax = plt.subplots()
ax.plot(ts, ys, 'k')

# FFT returns all frequencies it can
#ys is real, so we can use rfft
Y = fft.rfft(ys)
frequencies = fft.rfftfreq(N, d=dt)

#how many fourier terms do we want o look at
K = 50

total = 0
cmap = plt.get_cmap('viridis')
norm = plt.Normalize(vmin=0, vmax=K)

for k in range(K):
    #the fourier transform calculates the integral with exp(-i*omega*t)
    #so the signes and real/imag relation to the A and B of the sines and
    #cosines is slightly different
    A = -Y[k].imag/N
    B = Y[k].real/N
    #for oscillating terms we have to double the amplitude for the same
    #reason as when we were calculating A's and B's directly
    if k > 0:
        A *= 2
        B *= 2
    # the 2/N factor comes from the particular normalization used to
    # define fourier transform in SciPy. Various definitions exist.
    sint = A*np.sin(2*np.pi*frequencies[k]*ts)
    cost = B*np.cos(2*np.pi*frequencies[k]*ts)
    
    ax.plot(ts, sint, color=cmap(norm(k)))
    ax.plot(ts, cost, '--', color=cmap(norm(k)))
    
    total += sint + cost
ax.plot(ts, total, '-', color='r')

# However, to get the total sum of the first K fourier terms, we don't
# have to use use the loop explicitly. We can simply calculate the inverse
# fourier transform with frequencies larger than K to zero
#IRfft = inverse real fft
Y_K = np.copy(Y)
Y_K[K:] = 0
# this calculates the inverse fourier transform, i.e., the same sum were
# were building up in the total variable in the for loop
total_irfft = fft.irfft(Y_K, len(ts))
#                            ^^^^^^^
# for INVERSE REAL fft, there is some confusion about what should be the
# correct length of the inverse transform, so it's best to specify the
# expected length of the output explicitly.
ax.plot(ts, total_irfft, ':', color='g', lw=3)