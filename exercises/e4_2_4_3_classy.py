"""
Solution to excercises 4.2 and 4.3 using classes.

Note that classes in this example are perhaps a bit overused
(but that depends on your taste), the goal is to illustrate how
can they be used to make the program easier to read.
"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

import e3_7
import os
from glob import glob

from functools import total_ordering

rng = np.random.default_rng()

#
# Note, the definition of classes like this would usually be in its own file
#

# the @something is called a Decorator
# This one helps with defining ordering operators, ie, <, >, != etc
@total_ordering
class DataFile:
    """Class to represent the data file.
    
    Allows for chosing how to sort a list (or other container)
    of files -- 'fileno' (file number; default) or 'rmax' (maximum reponse).
    """
    def __init__(self, filename, ordering='fileno'):
        self.filename = filename
        self.basename = os.path.basename(self.filename)
        
        #To define the sorting, we will use an internal numerical variable
        #self._sort to specify ordering.
        #self._sort is a internally-used variable we will use for sorting
        #the leading underscore _ indicates a "private" variable that
        #the calling code shouldn't use, it's for internal use only
        
        #match is a nicer way deal with multiple if - elif - elif - else
        match ordering:
            case 'fileno':
                self._sort = self.file_number()
            case 'rmax':
                self._sort = self.rmax()
            case _:
                raise ValueError(f"Unsupported ordering type {ordering}")
    
    def __repr__(self):
        return f"DataFile({self.basename})"
    
    #now we will define the comparison function
    #less than
    def __lt__(self, other):
        return self._sort < other._sort
    #equal
    def __eq__(self, other):
        return self._sort == other._sort
    #The total_ordering decorator defines the rest of the comparison operators for us.
    #If we didn't use it, we'd have to define all of the rich comparison methods
    #(https://docs.python.org/3.5/reference/datamodel.html#object.__lt__)
    #corresponding to <, >, <=, >=, !=, ==
    
    #helper functions for sorting files according to their number
    def file_number(self):
        id_str = self.basename.split('_')[1].split('.')[0]
        return int(id_str)
    
    #or maximum value
    def rmax(self):
        self.d = np.loadtxt(self.filename)
        return abs(self.d[:,1] + 1j*self.d[:,2]).max()
    
    def get_data(self):
        # does self.d exist?
        # variables behind the dots are called "attributes",
        #so we check whether self has an attribute d
        if not hasattr(self, 'd'):
            #if yes, data was not loaded so do that
            self.d = np.loadtxt(self.filename)
        f, x, y = self.d.T
        
        #note that here and in rmax() when we loaded the data
        #we saved in *self*, so it will exist in memory as long
        #as *self* exists in memory. The data we are loading is
        #only a few MBytes, so it's not a problem, but this would
        #be a bad idea if we had gigabytes of data to process.
        return f, x, y
        

class Peak:
    #let's use a type hint that we expect file to be a DataFile
    #or at least something that behaves similarly
    # The type hint for p0 indicates that p0 is either numpy array or None
    # the default is None
    def __init__(self, file: DataFile, p0: np.ndarray|None = None):
        self.file = file
        self.f, self.x, self.y = file.get_data()
        self.r = np.abs(self.x + 1j*self.y)
        self.p0 = p0
    
    #fit function
    #staticmethod is another decorator, which makes the method 'static'
    #it doesn't work on any particular object and doesn't need self as
    #the first argument. It is basically an ordinary function that "lives"
    #inside a class
    @staticmethod
    def lorentz(f, f0, A, g, b1, b2, b3):
        peak = A*f0*g/(f**2 - f0**2 - 1j*f*g)
        bg = b1 + b2*f + b3*f**2
        return abs(peak) + bg

    #performs the fit, indices are used for bootstrap
    def fit(self, plot=False, indices=None):
        if plot:
            #by saving fig and ax in self, we make them
            #accessible to the calling code
            self.fig, self.ax = plt.subplots()
            self.ax.scatter(self.f, self.r)
        
        #initial guess of the fit parameter values
        f0, fwhm = e3_7.estimate_parameters(self.f, self.x, self.y)
        if self.p0 is None:
            #if we don't supply one, do the standard estimation
            A0_guess = np.max(self.r) - np.min(self.r)
            b1_guess = np.min(self.r)       
            init_guess = (f0, A0_guess, fwhm, b1_guess, 0, 0)
        else:
            #if we do supply one, only update the estimate the central frequency
            init_guess = self.p0
            init_guess[0] = f0
        
        if plot:
            #when debugging fitting it's useful to plot the initial estimate
            #We need to put self. in front of all variables/attributes that were defined in __init__
            #othervise python would try to look for first, a local variable and next a global
            #variable
            self.ax.plot(self.f, self.lorentz(self.f, *init_guess), '--', color='tab:orange')
        
        if indices is None:
            popt, pcov = curve_fit(self.lorentz, self.f, self.r, p0=init_guess)
            #save the fit variables in self as well
            #but only if we are not doing bootstrap
            self.popt = popt
            self.f0 = popt[0]
            self.A0 = popt[1]
            self.fwhm = popt[2]
            self.bg_poly = popt[3:]
        else:
            #higlight the bootstrap samples
            if plot:
                self.ax.scatter(self.f[indices], self.r[indices], color='tab:green')
            popt, pcov = curve_fit(self.lorentz, self.f[indices], self.r[indices], p0=init_guess)
        
        if plot:
            #plot the final fit
            self.ax.plot(self.f, self.lorentz(self.f, *popt), color='r')
        
        return popt

    def bootstrap(self, B=100, plot=False):
        if plot:
            self.fig, self.ax = plt.subplots()
            self.ax.scatter(self.f, self.r)
            if self.p0 is not None:
                self.ax.plot(self.f, self.lorentz(self.f, *self.p0), '--', color='tab:orange')
        
        popts = np.empty((B, 6)) #stores all the optimized parameters
        all_idx = np.arange(len(self.f), dtype=int) #array of all valid indices
        for b in range(B):
            #generate a subset of all indices by random choice with replacement
            fit_ix = rng.choice(all_idx, len(all_idx), replace=True)
            popt = self.fit(indices=fit_ix, plot=False)
            popts[b, :] = popt #save the b'th optimized parameters
        

        #and now we can do statistics on all rows
        popt = np.mean(popts, axis=0)
        perr = np.std(popts, axis=0)
        
        self.popt = perr
        self.popt = popt
        self.f0 = popt[0]
        self.A0 = popt[1]
        self.fwhm = popt[2]
        self.bg_poly = popt[3:]
        if plot:
            self.ax.plot(self.f, self.lorentz(self.f, *self.popt), color='r')
    
        return popt, perr
    

#create a list of DataFiles
files = [DataFile(filename=f, ordering='rmax') for f in glob('../lots_of_data/*.txt')]
#sort() internally uses <, > etc, which will now use the __lt__ and __eq__ which we
#defined for our class DataFile
files.sort()
print(files)

plt.close('all')
fig, ax = plt.subplots()
p0 = None
parameters = []
errors = []
every = 5

rmaxs = [fn.rmax() for fn in files]
norm = plt.Normalize(vmin=min(rmaxs), vmax=max(rmaxs))
cmap = plt.get_cmap('viridis')

#to save central frequencies and widths
f0s = []
fwhms = []
for k, file in enumerate(files):
    peak = Peak(file, p0=p0)
        
    if k % every == 0:
        ax.scatter(peak.f, peak.r, color=cmap(norm(peak.r.max())), s=2)
    
    try:
        popt, perr = peak.bootstrap(plot=True)
        p0 = peak.popt
        #since we assined the fit parameters to individual attributes
        #on lines 184--187, we can do following:
        f0s.append(peak.f0)
        fwhms.append(peak.fwhm)
        if k % every == 0:
            #notice ethat we can use Peak.lorentz() without any particular object
            ax.plot(peak.f, Peak.lorentz(peak.f, *peak.popt), color=cmap(norm(peak.r.max())))
    except RuntimeError:
        print(f"Fit failed in {file}. Skipping")

#plot the full widths as a function of f0, as in e12
fig_final, ax_final = plt.subplots()
ax_final.plot(f0s, fwhms, '-o')