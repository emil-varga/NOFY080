import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as intg

a = 2.0/3
b = 4.0/3
c = d = 1

def f(t, zl):
    z, l = zl
    dZdt = a*z - b*l*z
    dLdt = d*l*z - c*l
    return np.array((dZdt, dLdt))

sol = intg.solve_ivp(f, (0, 50), y0=[0.1, 0.1])

fig, (ax, axt) = plt.subplots(1, 2)
ax.plot(sol.t, sol.y[0,:])
ax.plot(sol.t, sol.y[1,:])
axt.plot(sol.y[0,:], sol.y[1,:])
plt.show()
