import numpy as np
import matplotlib.pyplot as plt
import e11 #import solution to excercise 11

from glob import glob

# glob() finds all filenames that match a certain pattern
# the "wildcard" character * substitutes any number of any characters
files = glob('lots_of_data/*.txt')

# the files are named ..., data_9.txt, data_10.txt, ...
# sorting on strings (i.e., filenames) works alphabeticaly, which places data_10 before data_9
# if we want to sort them according to their numerical labels, we have to specify the sorting key
# which is a function, which takes whatever is inside the list and returns something sortable (usually a number)
from os.path import basename #strips the directory name from the beginning
from re import split #splits a string according to given rules (re stands for Regular Expressions)
files.sort(key=lambda s: int(split('[_.]', basename(s))[1]))
# whenever you see a complex function call, you should read it inside out, i.e.
# let's assume that s is 'lots_of_data/data_9.txt', the evaluation goes as follows
# 1. basename('lots_of_data/data_9.txt') = 'data_9.txt'
# 2. split('[_.]', 'data_9.txt') = ['data', '9', 'txt']
# 3. (['data', '9', 'txt'])[1] = '9'
# 4. int('9') = 9

# The function split() splits according to any regular expression, which can be quite complex
# Here, the simple "[_.]" means that it should split at any of the characters inside []

#check the length and create empty arrays to save the results of the calculation
N = len(files)
f0s, fwhms = np.empty((2, N))

plt.close('all') #close all previously opened figures
fig_all, ax_all = plt.subplots() #we'll also plot all files
for k, file in enumerate(files): # 
    #load the file as in e11
    data = np.loadtxt(file)
    freq, X, Y = data.T
    
    #and now use the solution to e11 as an external module
    f0, fwhm = e11.estimate_parameters(freq, X, Y, plot=False)
    #and save the results into prepared arrays
    #we used indexing because the arrays already have the length we need
    #we could also use lists (replace line 30 with f0s = [] and similarly for fwhms) and
    #then .append() the results
    f0s[k] = f0
    fwhms[k] = fwhm
    
    #plot all R(freq) in a common plot
    R = np.sqrt(X**2 + Y**2)
    ax_all.plot(freq, R)
    ax_all.axvline(f0)

#plot the processed data
fig, ax = plt.subplots()
ax.plot(f0s, fwhms, 'o')
    