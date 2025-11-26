import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import time

# corners of the rectangle which contains the set
z1 = -2 - 1j #z1.real == -2; z1.imag == -1
z2 = 1 + 1j 
R = 500

# check the convergence of the series for a given c
def conv(c, Nmax=100):
    z = 0
    for n in range(1, Nmax+1):
        z = z**2 + c
        if abs(z) > 2:
            break
    return n

# Since all "pixels" of the image are calculated independently,
# we can decide how do we want to split the workload across CPUs
# But we also want to limit the number of processes to something 
# comparable to the actual number of CPUs. So we will split the
# work along lines:

# calculate the k-th line of the image
def func(k):
    ns = np.zeros(R+1)
    for l in range(R + 1):
        ckl_re = z1.real + k/R*(z2.real - z1.real)
        ckl_im = z1.imag + l/R*(z2.imag - z1.imag)
        ckl = ckl_re + 1j*ckl_im
        n = conv(ckl)
        ns[l] = n
    return ns

if __name__ == '__main__':
    Ns = np.zeros((R+1, R+1))

    t0 = time.time()
    with mp.Pool(4) as p:
        Ns = np.array(p.map(func, range(R+1)))
    t1 = time.time()
    print(f" Calculation took {t1-t0} seconds.")

    t0 = time.time()
    Ns_ = np.array([line for line in map(func, range(R+1))])
    t1 = time.time()
    print(f" Non-parallel calculation took {t1-t0} seconds.")

    fig, ax = plt.subplots()
    ax.imshow(Ns.transpose(), cmap='inferno')
    plt.show()
