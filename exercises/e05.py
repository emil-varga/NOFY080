import time # to measure time

# Recursive implementation of the Fibonacci sequence, including a docstring
def fib(k): #triple quote """ indicates a string which spans multiple lines
    """Calculates the k-th Fibonacci number using a recursive algorithm
    
    Parameters
    ---------
    k : positive integer
        The Fibonacci number to calculate  
    
    Returns
    -----
    positive integer
         k-th Fibonacci number
    
    """
    if k < 3: #boundary condition, F_1 = 1, F_2 = 1
        return 1
    return fib(k-1) + fib(k-2)

def fibi(k): # iterative implementation
    #if the docstring is short, simple quotes are enough
    "Calculate the k-th Fibonacci number using iterations." 
    if k < 3:
        return 1
    fk_1 = 1 #F_(k-1)
    fk_2 = 1 #F_(k-2)
    for k in range(2, k):
        fk = fk_1 + fk_2
        fk_2 = fk_1
        fk_1 = fk
    return fk

#function time.time() returns the number of seconds (with microsecond resolution) from
#midnight 1.1.1970 (the so-called Unix Epoch), which, by itself, is not particularly useful
#but the difference between two calls to time.time() gives the elapsed time

t0_recursion = time.time() #time stamp just before the calculation
f_rec = fib(20)      #calculate the 20th Fk
t1_recursion = time.time() #time stamp at the end
total_time_rec = t1_recursion - t0_recursion

#similarly for iterations
t0_iter = time.time() 
f_iter = fibi(20)
t1_iter = time.time()
total_time_iter = t1_iter - t0_iter

print(f"Recursive: {f_rec}, time: {total_time_rec} s.")
print(f"Iterative: {f_iter}, time: {total_time_iter} s.")
