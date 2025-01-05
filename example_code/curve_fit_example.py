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

fig, ax = plt.subplots()
ax.scatter(xs, ys, label='data')

#%% fit the data
popt, pcov = curve_fit(lorentzian, xs, ys, p0=[1, 1, 1])
# curve_fit returns the optimized parameters (popt) and the covariance matric (pcov)
# the diagonal of the covariance matrix can be used as simple error estimates of the parameters
ax.plot(xs, lorentzian(xs, *popt), color='r', label='fit')
#                          ^ this substitutes (positionally) elements of the iterable into the function call

print(f"Estimated height: {popt[0]:.3f} +/- {np.sqrt(pcov[0,0]):.3f}")
print(f"Estimated center: {popt[1]:.3f} +/- {np.sqrt(pcov[1,1]):.3f}")
print(f"Estimated width: {popt[2]:.3f} +/- {np.sqrt(pcov[2,2]):.3f}")

ax.legend(loc='best')
fig.savefig('curve_fit.pdf')