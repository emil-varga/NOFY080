import numpy as np
import matplotlib.pyplot as plt
import time

#iterate the series from the definition of the Mandelbrot set
def zn(c, max_iter=1000):
    z = 0
    for k in range(max_iter):
        z = z**2 + c
        if abs(z) > 2: # the series will definitely diverge
            return k #at what point did we become certain that it diverges (i.e., a measure of how far it is from the set)
    #otherwise we return max_iter which we will understand as "probably in the set"
    return max_iter

def mandelbrot(reals, imags, max_iter=1000):
    Nx = len(reals)
    Ny = len(imags)
    zs = np.empty((Nx, Ny))
    # we will explicitly calculate the convergence of the series for every point c
    for kx in range(Nx):
        for ky in range(Ny):
            c = reals[kx] + 1j*imags[ky]
            zs[ky, kx] = zn(c, max_iter=max_iter)
    return zs

# If x and y are numpy arrays, expressions like x + y are internally turned into a loop that
# adds all elements together. However, this loop is written in C in the numpy library and uses
# a bunch of tricks to run as fast as possible (e.g., so-called SIMD instructions, https://en.wikipedia.org/wiki/Streaming_SIMD_Extensions)
# and as a result runs much faster than a Python loop.

# A solution which uses only vector-like manipulation of arrays without explicitly looping over them is
# called vectorized, and can be substantially faster. For example, the above explicit loop can be rewritten as
def mandelbrot_vectorized(cs, max_iter=1000):
    #cs is a matrix of complex numbers c which we want to check whether they
    #belong to the mandelbrot set or not
    shape = cs.shape # remember the shape of the matrix
    cs = cs.flatten() # and turn it into single 1D array
    zs = np.zeros_like(cs, dtype=complex) # the values in the series
    ks = np.zeros_like(cs, dtype=int) # iteration number, stop incrementing once abs(z) > 2
    remaining = np.ones_like(zs, dtype=bool) # which points still need to be iterated?
    for k in range(max_iter):
        #the series from the definition of the set, but calculate it 
        zs[remaining] = zs[remaining]**2 + cs[remaining]
        ks[remaining] += 1
        remaining = abs(zs) < 2 # stop iterating cs which lead to diverging zn
        if not any(remaining): #stop if nothing's left
            break
    #return the iteration numbers in the shape of the original matrix
    return ks.reshape(shape)

Nx = 300
Ny = 300

#this range fits the entire set
# reals = np.linspace(-2, 1, Nx)
# imags = np.linspace(-1, 1, Ny)

#this zoomed view is pretty
reals = np.linspace(0.1, 0.15, Nx)
imags = np.linspace(0.6, 0.65, Ny)

#let's time the two solutions
t0_loop = time.time()
zs1 = mandelbrot(reals, imags)
t1_loop = time.time()

t0_vec = time.time()
#create the 2D matrix of the complex numbers c
CR, CI = np.meshgrid(reals, imags)
cs = CR + 1j*CI
zs2 = mandelbrot_vectorized(cs)
t1_vec = time.time()

print(f"Explicit loop: {t1_loop - t0_loop} s") # ~10 s on my PC
print(f"Vectorized: {t1_vec - t0_vec} s") # ~0.7 s

extent = [reals.min(), reals.max(), imags.min(), imags.max()]

plt.close('all')
fig1, ax1 = plt.subplots()
ax1.imshow(zs1, origin='lower', extent=extent)
ax1.set_title('explicit loop')

fig2, ax2 = plt.subplots()
ax2.imshow(zs2, origin='lower', extent=extent)
ax2.set_title('vectorized')