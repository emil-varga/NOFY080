import numpy as np
import matplotlib.pyplot as plt

# create a square pulse from t=0.125 to t=0.625
ts = np.linspace(0, 1, 1000)
dt = ts[1] - ts[0]
ys = np.zeros_like(ts)
start = 0.125
ys[np.logical_and(ts > start, ts < start + 0.5)] = 1

plt.close('all')
fig, ax = plt.subplots()
ax.plot(ts, ys, 'k')

#we will represent our signal y(t) with a Fourier series
# y(t) = sum_k A_k sin(2*pi*k*t) + B_k cos(2*pi*k*t)

#to calculate the individual A_k and B_k, we simply have to integrate
#the signal with the the appropriate sine or cosine term
def Ak(ts, ys, k):
    sint = np.sin(2*np.pi*k*ts)
    # we multiply by 2 because sin(...)^2 averaged over a period is 1/2
    return 2*np.sum(ys*sint)*dt

def Bk(ts, ys, k):
    if abs(k) > 0:
        cost = np.cos(2*np.pi*k*ts)
        return 2*np.sum(ys*cost)*dt
    else:
        #if k==0 (cos(...) == 1) the factor 2 is not needed
        return np.sum(ys)*dt

#calculate the first K fourier coefficients A and B
K = 20
As = [Ak(ts, ys, k) for k in range(K)]
Bs = [Bk(ts, ys, k) for k in range(K)]

#total will be the total sum of the Fourier series
total = 0

#prepare a colormap for plotting
cmap = plt.get_cmap('viridis')
norm = plt.Normalize(vmin=0, vmax=K)

#iterate over all coefficients and frequencies
for k, (A, B) in enumerate(zip(As, Bs)):
    sint = A*np.sin(2*np.pi*k*ts)
    cost = B*np.cos(2*np.pi*k*ts)
    
    # plot the oscillating terms with the color given
    # by the frequency
    ax.plot(ts, sint, color=cmap(norm(k)))
    ax.plot(ts, cost, '--', color=cmap(norm(k)))
    
    total += sint + cost

ax.plot(ts, total, '-', color='r')
fig.savefig('../fourier_series_square_pulse.pdf')

#finally, plot the Fouerier spectrum itself. Try changing the phase of the
#signal by changing the start variable on line 7. Individual As and Bs will
#change, but the modulus of the complex number |A + iB| stays the same.
fig_spec, ax_spec = plt.subplots()
ax_spec.plot(range(K), As, '-o', label='sine terms, $A$')
ax_spec.plot(range(K), Bs, '-o', label='cosine terms, $B$')
ax_spec.plot(range(K), np.abs(As + 1j*np.array(Bs)), '-s', label='$|A + iB|$')
ax_spec.legend(loc='best')
plt.show()