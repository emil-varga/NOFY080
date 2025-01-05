import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

rng = np.random.default_rng()

#%% function to fit
def lorentzian(xs, height, center, width):
    return height*center**2*width**2/((center**2 - xs**2)**2 + width**2*xs**2)

#%% generate some data and plot
xs = np.arange(0, 10, 0.1)
height = 0.5
center = 5
width = 2
noise = 0.05
ys = lorentzian(xs, height, center, width) + rng.random(len(xs))*noise

plt.close('all')
fig, ax = plt.subplots()
ax.scatter(xs, ys, label='data')

#%% fit the data
#...
bootstrap_N = 100
parameter_N = 3
data_N = len(xs)
ps = np.empty((bootstrap_N, parameter_N)) # here we will save all fit parameters
for k in range(bootstrap_N):
    ix = rng.choice(range(data_N), data_N) # some data will be omitted, some will occur more than once
    ix.sort()
    popt, _ = curve_fit(lorentzian, xs[ix], ys[ix], p0=[1, 1, 1])
    ps[k,:] = popt

# the fit function does not depend on the sign of the parameters center and width
# and curve_fit will randomly find one or the other. Make sure that we are averaging
# the same signs
ps = abs(ps)
# do the statistics on the set of parameters ps, which is a 2D array. 
# work only along one axis, we don't want to average everything together
popt_bootstrap = np.mean(ps, axis=0) #1st axis (0th) averages the rows
perr_bootstrap = np.std(ps, axis=0) #the same for standard deviation
ax.plot(xs, lorentzian(xs, *popt_bootstrap), color='r', label='fit')

print(f"Estimated height: {popt_bootstrap[0]:.3f} +/- {perr_bootstrap[0]:.3f}")
print(f"Estimated center: {popt_bootstrap[1]:.3f} +/- {perr_bootstrap[1]:.3f}")
print(f"Estimated width: {popt_bootstrap[2]:.3f} +/- {perr_bootstrap[2]:.3f}")