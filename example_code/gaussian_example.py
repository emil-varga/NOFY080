import numpy as np
import matplotlib.pyplot as plt

xs = np.linspace(0, 10, 100)
ys = np.exp(-(xs - 5)**2)

plt.close('all') #closes all figures we have opened so far
fig, ax = plt.subplots()

y2 = np.sort(ys)

ax.plot(xs, ys, '--s', ms=5, lw=2, color='magenta', label='ax.plot($e^{-x^2}$)')
ax.scatter(xs, ys, s=ys*10, marker='o', color='cyan', zorder=3, label=r'ax.scatter($e^{-x^2}$)')

ax.set_xlabel('$x$ values')
ax.set_ylabel(r'the gaussian $e^{-(x-5)^2}$')
#where to put the legend, we can also use "best" and let matplotlib guess
ax.legend(loc='upper left')

fig.tight_layout() #reduces some of the whitespace around edges
fig.savefig('gaussian.pdf')