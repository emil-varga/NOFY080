import numpy as np

def gauss(n):
    """
    The Gauss' formula for summing 1 + 2 + 3 + ... + n

    Parameters
    ----------
    n : integer

    Returns
    -------
    integer
        The sum.
    """
    return n*(n+1)/2

def sum_up_to(n):
    """
    Sums numbers 1 + 2 + 3 + ... + n

    Parameters
    ----------
    n : int
        Up to where to sum.

    Returns
    -------
    total_sum : int
        The sum.

    """
    #first we want to create an array containing [1, 2, 3, ... n]
    #that is handled simply using np.arange(start, stop, step)
    arr = np.arange(1, n+1) #remember that the stop is NOT included, hence n+1
    
    #equivalently, we could do this
    # np.empty() creates an array of size n, but leaves it uninitialized
    # i.e., any garbage that was in the memory when we created it is
    # still there
    # arr = np.empty(n)
    # for k in range(1, n+1): # and now we have to initialize it by hand
    #     arr[k] = k
    
    # we'll sum everything together in a loop, make a variable that will
    # accumulate the total sum, whicih start at zero
    total_sum = 0
    for x in arr:
        total_sum += x #and now just add every element to the total_sum
    
    #or we could simply do return arr.sum()
    return total_sum

#test it out
print(gauss(54) == sum_up_to(54))