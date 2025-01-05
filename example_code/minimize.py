import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optim

def parabola(x, y):
    return 4*x**2 + 2*y**2 + x*y - 6*y -3*x + 5

#the lambda is there to simply turn a function of two parameters into a
#function of a single parameter
xmin = optim.minimize(lambda z: parabola(*z), x0=[0,0])

XX, YY = np.meshgrid(np.linspace(-5, 5), np.linspace(-5, 5))
p = parabola(XX, YY)
fig, ax = plt.subplots()
ax.pcolormesh(XX, YY, p)
ax.plot(*xmin.x, 'x', color='r', ms=10)
fig.savefig('parabola-minimize.pdf')