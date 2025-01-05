import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

g = 9.81 #m/s^2
rho_air = 1 #kg / m^3
ball_r = 0.1 #m
#drag coefficient, https://en.wikipedia.org/wiki/Drag_coefficient
CD = 0.47
A_ball = 2*np.pi*ball_r**2

#differentiation of position and velocity
def F(t, z, CD=0):
    x, y, vx, vy = z
    
    #total velocity
    v_tot = np.sqrt(vx**2 + vy**2)
    
    air_resistance = 0.5*rho_air*v_tot**2*CD*A_ball
    
    dxdt = vx
    dydt = vy
    dvxdt = -air_resistance*vx/v_tot
    dvydt = -g - air_resistance*vy/v_tot
    return np.array([dxdt, dydt, dvxdt, dvydt])

# events of interest can be signaled during the calculation
# by functions which change sign when the event happens.
# In this case, the even is the object falling on the ground
def impact(t, z, CD=0):
    return z[1]
# setting the terminal attribute to 0 will cause the calculation
# to end when the event happens
impact.terminal = True

def ballistic(initial_condition, CD=0):
    solution = solve_ivp(F, (0, 10), y0=initial_condition,
                       events=impact, dense_output=True, args=(CD,))
    dt = 1e-3
    print(solution.t_events)
    time = np.arange(0, solution.t_events[0][0]+dt, dt)
    z = solution.sol(time)
    x = z[0,:]
    y = z[1,:]
    return x, y

initial_condition=[0, 0.01, 3, 3]
# without air resistance
x, y = ballistic(initial_condition)
# with air resistance
xvz, yvz = ballistic(initial_condition, CD)
fig, ax = plt.subplots()
ax.plot(x, y, label="Without air resistance")
ax.plot(xvz, yvz, label="With air resistance")
ax.legend(loc='best')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
fig.tight_layout()
fig.savefig('ballistic.png')