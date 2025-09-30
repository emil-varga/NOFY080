#we want to find all prime numbers less than N using
#the Sieve of Eratosthenes

import numpy as np
N = 100

#we want to select prime numbers out of this array
numbers = np.arange(1, N+1) # = [1, 2, 3, ..., N]
#is_prime[k] will be True if numbers[k] is prime
#let's start by simply creating an array of the same sizes filled with True
is_prime = np.ones_like(numbers, dtype=bool)
#by default, np.ones_like(arr) will create an array filled with ones
#specifiying dtype=bool (data type) will map any non-zero number to True
#and zeros to False

#1st index represents number 1, which is not prime
is_prime[0] = False
for k, p in enumerate(is_prime): #k is the index, p is the value, i.e., p = is_prime[k]
    if p: # is numbers[k] prime? p is already True/False we can use it in if directly
        x = k + 1 #x is the number we are checking (one bigger than the index, since indexing starts from 0)
        for ix in range(k+x, N, x): #now go from the first 2*x up to N by steps of x
            is_prime[ix] = False # and cross each multiple out
        #the for loop is equivalent to:
        # ix = k + x
        # while ix < N:
        #     is_prime[ix] = False
        #     ix += x

#We can use the array filled with boolean values to create a
#new array which only contains elements where is_prime was True
z = numbers[is_prime]
print(z)