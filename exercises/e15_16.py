import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

import e11
import os
from glob import glob

rng = np.random.default_rng()

#helper functions for sorting files according to their number
def file_number(fn):
    basename = os.path.basename(fn)
    id_str = basename.split('_')[1].split('.')[0]
    return int(id_str)

#or maximum value
def rmax(fn):
    d = np.loadtxt(fn)
    return abs(d[:,1] + 1j*d[:,2]).max()

#fit function
def lorentz(f, f0, A, g, b1, b2, b3):
    peak = A*f0*g/(f**2 - f0**2 - 1j*f*g)
    bg = b1 + b2*f + b3*f**2
    return abs(peak) + bg

#performs the fit
def fit(f, x, y, p0=None, plot=False):
    r = np.sqrt(x**2 + y**2)
    
    if plot:
        fig, ax = plt.subplots()
        ax.scatter(f, r)
    
    if p0 is None:
        #initial guess of the fit parameter values
        f0, fwhm = e11.estimate_parameters(f, x, y)
        #if we don't supply one, do the standard estimation
        A0_guess = np.max(r) - np.min(r)
        b1_guess = np.min(r)       
        init_guess = (f0, A0_guess, fwhm, b1_guess, 0, 0)
    else:
        init_guess = p0
    
    if plot:
        #when debugging fitting it's useful to plot the initial estimate
        ax.plot(f, lorentz(f, *init_guess), '--', color='tab:orange')
    
    popt, pcov = curve_fit(lorentz, f, r, p0=init_guess)
    
    if plot:
        #plot the final fit
        ax.plot(f, lorentz(f, *popt), color='r')
    
    return popt

def bootstrap(f, x, y, B=100, p0=None, plot=False):
    if plot:
        r = abs(x + 1j*y)
        fig, ax = plt.subplots()
        ax.scatter(f, r)
        if p0 is not None:
            ax.plot(f, lorentz(f, *p0), '--', color='tab:orange')
    
    popts = np.empty((B, 6)) #stores all the optimized parameters
    all_idx = np.arange(len(f), dtype=int) #array of all valid indices
    
    #even if p0 is not None, calculate the central frequency estimate explicitly
    if p0 is not None:
        f0, fwhm = e11.estimate_parameters(f, x, y)
        p0[0] = f0
    
    for b in range(B):
        #generate a subset of all indices by random choice with replacement
        fit_ix = rng.choice(all_idx, len(all_idx), replace=True)
        popt = fit(f[fit_ix], x[fit_ix], y[fit_ix], p0=p0)
        popts[b, :] = popt #save the b'th optimized parameters
    
    #finally we want to average everything HOWEVER,
    #the fitting functino lorentz() has the unfortunate property that
    #if we change the sign of any two parameters of the trio A, f0 and g
    #it's value is unchanged, and hence the fit is equally good. Averaging
    #over changing signs is of course incorrect, therefore we have to take
    #the absolute value of these before averaging. Background coefficnents
    #are uniquely determined, thus we leave them as they were
    popts[:,:-3] = np.abs(popts[:,:-3])
    #and now we can do statistics on all rows
    popt = np.nanmean(popts, axis=0)
    perr = np.nanstd(popts, axis=0)
    if plot:
        ax.plot(f, lorentz(f, *popt), color='r')

    return popt, perr
    

files = glob('../lots_of_data/*.txt')
files.sort(key=rmax, reverse=True)

plt.close('all')
fig, ax = plt.subplots()
p0 = None
parameters = []
errors = []
every = 5

rmaxs = [rmax(fn) for fn in files]
norm = plt.Normalize(vmin=min(rmaxs), vmax=max(rmaxs))
cmap = plt.get_cmap('viridis')


for k, file in enumerate(files):
    print(file)
    data = np.loadtxt(file)
    freq, x, y = data.T
    r = np.sqrt(x**2 + y**2)
    
    if k % every == 0:
        ax.scatter(freq, r, color=cmap(norm(r.max())), s=2)
    
    try:
        # without bootstrap
        # popt = fit(freq, x, y, p0=p0, plot=True)
        popt, perr = bootstrap(freq, x, y, p0=p0, plot=False)
        p0 = np.copy(popt)
        if k % every == 0:
            ax.plot(freq, lorentz(freq, *popt), color=cmap(norm(r.max())))
    except RuntimeError:
        print(f"Fit failed in {file}. Skipping")