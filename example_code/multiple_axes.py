import numpy as np
import matplotlib.pyplot as plt
nrows = 2
ncols = 3
fig, axes = plt.subplots(nrows, ncols, sharex=True, sharey=True,
                         width_ratios=[3, 2, 1], height_ratios=[1,2])
#axes is now a 2D array of axes which all share the same x and y range

xs = np.linspace(0, 1)

axes[0,0].plot(xs, xs)
axes[1, 1].plot(xs, xs**2)
axes[0, 2].plot(xs, np.sqrt(xs))

axes[1,0].plot(-xs, -xs)
axes[0, 1].plot(-xs, -xs**2)
axes[1, 2].plot(-xs, -np.sqrt(xs))

fig.tight_layout()
fig.savefig('multiax.pdf')