from multiprocessing import Pool

def function(x):
    return some_calculation(x)

z = [... data ...]

with Pool(6) as pool:
    result = pool.map(function, z)