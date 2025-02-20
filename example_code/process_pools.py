import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import time


def fib(x):
    if x < 2:
        return 1
    return fib(x-1) + fib(x-2)

def calc_fibs(z, nproc):
    with Pool(nproc) as pool:
        fibs = pool.map(fib, z)
    return fibs

def timeit(z, nproc):
    t0 = time.time()
    fibs = calc_fibs(z, nproc)
    t1 = time.time()
    print(f"Calculation with {nproc} processes took {t1 - t0:.3f} s")

z = np.arange(35)
timeit(z, 1)
timeit(z, 2)
timeit(z, 4)
timeit(z, 8)
timeit(z, 16)
    