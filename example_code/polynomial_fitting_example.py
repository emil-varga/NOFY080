import numpy as np
import matplotlib.pyplot as plt

from numpy.polynomial import Polynomial as P

rng = np.random.default_rng() # random number generator

#%% create some noisy data and plot them
noise_amplitude = 10
xs = np.arange(-5, 5, 0.1)
ys = 0.1*xs**4 - 3*xs**3 + 10*xs + 4 + rng.random(len(xs))*noise_amplitude

fig, ax = plt.subplots()
ax.scatter(xs, ys, label='data')

#%% fit the polynomial
poly = P.fit(xs, ys, deg=4)
ax.plot(xs, poly(xs), color='r', label='polynomial fit')
#the coefficients of poly are scaled for a particular domain/window
#to get the ordinary coefficients we need to use .convert()
coef = poly.convert().coef
poly_string = ' + '.join([f'({c:.1f})*x^{k}' for k, c in enumerate(coef)])
print("The estimated polynomial is", poly_string)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(loc='best')
fig.savefig('polynomial_fit.pdf')