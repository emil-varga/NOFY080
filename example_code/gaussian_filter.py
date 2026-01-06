import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

xs = np.linspace(-1, 1, 100)
ys = np.linspace(-1, 1, 100)
XX, YY = np.meshgrid(xs, ys)
Z = np.zeros_like(XX)
Z[np.sqrt(XX**2 + YY**2) < 0.25] = 1

fig, ax = plt.subplots(2, 3, sharex=True, sharey=True,
                       layout='constrained')
ax[0, 0].imshow(Z)
ax[0, 1].imshow(gaussian_filter(Z, sigma=1))
ax[0, 2].imshow(gaussian_filter(Z, sigma=2))
ax[1, 0].imshow(gaussian_filter(Z, sigma=(0, 5)))
ax[1, 1].imshow(gaussian_filter(Z, sigma=(5, 0)))
ax[1, 2].imshow(gaussian_filter(Z, sigma=(5, 2)))

ax[0, 0].set_title('original')
ax[0, 1].set_title('$\sigma$=1')
ax[0, 2].set_title('$\sigma$=2')
ax[1, 0].set_title('$\sigma$=(0,5)')
ax[1, 1].set_title('$\sigma$=(5,0)')
ax[1, 2].set_title('$\sigma$=(5,2)')

fig.savefig('notes/figures/gaussian_filter.pdf')
plt.show()