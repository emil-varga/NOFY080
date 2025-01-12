import matplotlib.pyplot as plt
import numpy as np
import taichi as ti

#try running on GPU if possible (NVIDIA CUDA)
#this will default to CPU if GPU is not available
ti.init(ti.gpu)

#the decorator will cause the following function to be compiled
#to run on the GPU (if available) as a compute kernel
@ti.kernel
def newton(rs: ti.types.ndarray(dtype=ti.f64),
           acc: ti.types.ndarray(dtype=ti.f64)): 
    #the types of argument of kernels have to be annotated

    #assume that the array of positions is shape (N, 2)
    N = rs.shape[0]

    for j in range(N):
        # zero out the acceleration of the j'th particle so that we can add to it
        # slices are not supported in taichi
        acc[j,0] = 0
        acc[j,1] = 0

    #this loop runs in parallel, and THERE IS NO SYNCHRONIZATION
    #no mutexes/locks or anything like that. We have to make sure
    #none of the operations we do inside the loop can influence one another
    for j in range(N):
        #only the top-level loop runs in parallel, this one is serialized
        for k in range(N):
            #no self-interaction
            if j != k:
                pk = ti.Vector([rs[k,0], rs[k,1]])
                pj = ti.Vector([rs[j,0], rs[j,1]])

                d = pj - pk
                #this is a cheat, 1e-5 is the minimum possible value
                #this limits the maximum possible velocity for 
                #numerical stability
                r = d.norm(1e-5)

                acc[j,0] += -d[0]/r**3
                acc[j,1] += -d[1]/r**3

@ti.kernel
def step(rs: ti.types.ndarray(dtype=ti.f64),
         vel: ti.types.ndarray(dtype=ti.f64),
         acc: ti.types.ndarray(dtype=ti.f64),
         dt: float):
    N = rs.shape[0]
    for j in range(N):
        for k in range(2):
            rs[j,k] += dt*vel[j,k]
            vel[j,k] += dt*acc[j,k]

           
#encapsulate the state of the simulation in a simple class
class Planets:
    def __init__(self, N, D=1, dt=1e-4):
        self.D = D
        self.dt = dt
        #
        self.t = 0
        #randomly distributed initial positions with normal distribution
        #and spread D
        self.rs = D*np.random.randn(N, 2)
        #velocities -- solid body rotation as initial condition
        #so that the system has some nonzero angular momentum
        self.vels = 50*np.column_stack((-self.rs[:,1], self.rs[:,0]))
        #accelerations
        self.acc = np.zeros_like(self.rs)

    def update_accelerations(self):
        #we can simply pass numpy arrays to the kernel
        #this "function", however, does not run inside Python
        #the acc array will be modified
        newton(self.rs, self.acc)

    def euler_step(self, dt=None):
        #Euler step is very inaccurate and requires small dt
        #replace with something better for actually useful simulation
        if dt is None:
            dt = self.guess_dt()
        step(self.rs, self.vels, self.acc, dt)
        self.t += dt


if __name__ == '__main__':
    import os
    fig, ax = plt.subplots()
    
    #Create 5000 planets
    planets = Planets(5000, D=1)

    # set up plotting
    plot, = ax.plot(planets.rs[:,0], planets.rs[:,1], 'o', ms=1)
    plot_scale = 5
    ax.set_xlim(-plot_scale, plot_scale)
    ax.set_ylim(-plot_scale, plot_scale)
    ax.set_aspect('equal')

    # where to save the result
    os.makedirs('pictures', exist_ok=True)
    try:
        last_save = 0
        frame = 0
        #the simulation simply proceeds by updating the accelerations
        #and then incrementing the positions and velocities, until
        #the simulations is stopped
        while True:
            planets.update_accelerations()
            planets.euler_step(1e-5)

            # update the interactive plot
            plot.set_xdata(planets.rs[:,0])
            plot.set_ydata(planets.rs[:,1])
            plt.pause(1e-3)

            #Only save the picture. In a real simulation we would save the
            #positions and accelerations so that we can further process them.
            if planets.t - last_save > 1e-3:
                last_save = planets.t
                fig.savefig(f'pictures/frame_{frame:08d}.png', dpi=300)
                frame += 1
            print(planets.t)
    except KeyboardInterrupt:
        print("Qutting...")
