import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

import scipy.integrate as intg

#define the lorenz system
def lorenz(t, xyz, sigma, rho, beta):
    x, y, z = xyz
    dxdt = sigma*(y - x)
    dydt = x*(rho - z) - y
    dzdt = x*y - beta*z
    return np.array([dxdt, dydt, dzdt])

#solve the equation 
#you can specify time points where you want to know the solution using
#t_eval keyword argument
sol_lorenz = intg.solve_ivp(lorenz, (0, 100), y0=[1,1,1], args=(10, 28, 8./3),
                            t_eval=np.linspace(0, 100, 5000))

fig, ax = plt.subplots(1, 1)
def normalize(x):
    xmin = np.min(x)
    xmax = np.max(x)
    return (x - xmin)/(xmax - xmin)
ax.set_title('Lorenz model')
cmap = plt.get_cmap('viridis')
#scatter plot can color every point differently
ax.scatter(sol_lorenz.y[0], sol_lorenz.y[2], color=cmap(normalize(sol_lorenz.y[1])), alpha=0.5, s=30)
ax.plot(sol_lorenz.y[0], sol_lorenz.y[2], '-', color='k', lw=0.5)

# 3D plot
fig3d = plt.figure()
ax3d = fig3d.add_subplot(projection='3d')
ax3d.plot(sol_lorenz.y[0], sol_lorenz.y[1], sol_lorenz.y[2], lw=0.5)