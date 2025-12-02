import numpy as np
import matplotlib.pyplot as plt
import e3_7 # make sure e11.py is in the same directory

# if e11 is somewhere else, say D:/Python/modules, we'd have to do
#import sys
#sys.path.append('D:/Python/modules')
#import e11

from numpy.polynomial import Polynomial as P

from glob import glob

#old-style interface for handling polynomials
#don't use for new code
# array_of_coeficients = np.polyfit(x, y, deg=4)
# y = np.polyval(array_of_coeficients, x)

#find all file names we want to process
files = glob('lots_of_data/*.txt')
print(len(files))

plt.close('all') # clean up previos images
fig, axs = plt.subplots(2, 1) # figure, two subplots in one column

# an empty list to save all backgrounds we can get
# fitting can sometimes fail, we don't know a-priori how many we'll manage to
# get, therefore a list makes more sense here than an array
backgrounds = []
for file in files: # go through files one by one
    d = np.loadtxt(file) # load the file with default separataro and comments
    f, x, y = d.T # split the columns into variables
    r = abs(x + 1j*y) # calculate the absolute response
    axs[0].plot(f, r) # and plot it
    
    # use the solution to e11 to guesstimate the central frequency and fwhm
    f0, fwhm = e3_7.estimate_parameters(f, x, y, plot=False)
    
    # to fit the background, we only want points where are sufficiently far from
    # the resonance
    ix = abs(f - f0) > 3*fwhm # frequencies further from f0 than 3*fwhm
    try: # try fitting the non-peak data with a 4th degree polynomial
        bg = P.fit(f[ix], r[ix], deg=4)
    except ValueError:
        #Fit failed. But we know that P.fit() raises ValueError when the input is
        #empty or the fit didn't converge. We expected this for some files, so
        #we just print a warning and continue with the next file
        print("fit failed")
        continue
    except: # This catches any other exception.
        # We only know how to handle ValueError (i.e., ignoring it). Anything
        # else is a problem and we'll send the exception on it's way further
        # (to probably crash the program)
        print("An unexpected exception occured!")
        # Note that if we didn't have the print in the line above, this kind of
        # exception handler is useless. Unhandled exceptions automatically propagate
        # to higher levels of the program until they are handled or they crash
        # the program.
        raise #re-raise the exception
    
    # fig, ax = plt.subplots()
    # ax.scatter(f, r)
    # ax.scatter(f[ix], r[ix], color='r')
    # ax.plot(f, bg(f), color='g')
    
    #fit went fine, save the object that represents the polynomial
    backgrounds.append(bg)

# basic arithmetic is defined for polynomials (this is called overloading in 
# the language of object-oriented programming, i.e. the + operator is overloaded)
# Since np.mean() only neads basic arithmetic, we can average the polynomials directly
bg_all = np.mean(backgrounds)

for file in files:
    d = np.loadtxt(file)
    f, x, y = d.T
    r = abs(x + 1j*y)
    #polynomials can be called as a function
    axs[1].plot(f, r - bg_all(f))