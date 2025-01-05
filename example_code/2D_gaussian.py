import numpy as np
import matplotlib.pyplot as plt

#x and y axis
_xs = np.linspace(0, 10, 100)
_ys = np.linspace(0, 10, 100)
#but we need 100 x 100 points for both x and y that sample the 
#the entire interval (0, 10) x (0, 10), this can be done using
#meshgrid
xs, ys = np.meshgrid(_xs, _ys)
zs = np.exp(-(xs - 5)**2 - (ys - 5)**2)

plt.close('all') #closes all figures we have opened so far
fig, ax = plt.subplots()

plot = ax.imshow(zs, cmap='inferno_r', origin='lower') 
# plot = ax.pcolormesh(xs, ys, zs, cmap='inferno_r') 
cbar = fig.colorbar(plot) #the color axis scaling
cbar.set_label('$z$')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
fig.savefig("gaussian_2D.pdf")