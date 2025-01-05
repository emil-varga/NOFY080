# differential equations - boundary value problems

# Find a specific solution to the stationary Schrodinger equation in infinitely
# deep potential well with a potential barrier in the middle

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp

a = 1
m = 1
w = 0.2
dh = 10
N = 100

#potential well with a barrier in the middle
def potential(x):
    V = np.zeros_like(x)
    ix = np.logical_and(x > -w/2, x < w/2)
    V[ix] = dh
    return V

#right-hand side of the Schrodinger equation
def F(x, psi, p):
    E = p[0]
    V = potential(x)
    dpsidx = psi[1]
    dpsidx2 = (V - E)*psi[0]*2*m
    return np.row_stack((dpsidx, dpsidx2))

#boundary conditions
# the last element ensures that the slope at the endge is non-zero. The solution given
# by solve_bvp is not normalized, so this value is arbitrary and it only ensures that
# the solution is non-zero
def boundaries(ya, yb, p):
    return np.array([ya[0], yb[0], ya[1]-0.0001])

#grid on solve the eqquation
xs = np.linspace(-a, a, N)

#the initial guess of the solution
#the wave function itself
ys0 = np.zeros_like(xs, dtype=complex)
# just so that the initial guess is not identically zero. This choice
# will give us asymmetric solution where the particle is localized in one
# part of the well
ys0[N//4] = 1
#the wave function gradient, we take those simply as zeros
ys1 = np.zeros_like(xs, dtype=complex)
y0 = np.row_stack((ys0, ys1))

#the ground state energy for a well without the barrier
En = (np.pi*1)**2/(8*a**2)

# now try to find the solution
sol_schr = solve_bvp(F, boundaries, xs, y0, p=(En,))

#did the solution converge?
print(sol_schr.success, sol_schr.message)
#how many iterations were necessary
print(sol_schr.niter)
#initial guess and the state energy
print(En, sol_schr.p)

#plot the solution
fig, ax = plt.subplots(1, 1)
ax.set_title("Schrodinger")
# probability density of particle position (non-normalized)
ax.plot(sol_schr.x, abs(sol_schr.y[0])**2)
ax2 = ax.twinx() # y-axis on the right hand side
ax2.plot(xs, potential(xs), '-', color='k') # potential
ax2.axhline(sol_schr.p[0], ls='--', color='r') # energy of the solution
ax2.axvline(-a, color='k') # edges of the potential well
ax2.axvline(a, color='k')

#plot the potential alone
fig_V, ax_V = plt.subplots()
ax_V.plot(xs, potential(xs), '-', color='k') # potential barrier
ax_V.axvline(-a, color='k') # well boundaries
ax_V.axvline(a, color='k')
fig_V.tight_layout()
fig_V.savefig('sch_potential.pdf')

plt.show()