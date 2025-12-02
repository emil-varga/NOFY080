import numpy as np
import matplotlib.pyplot as plt

def plot_different_axscales(N, xi=0.01, xf=5):
    xs = np.linspace(xi, xf, N)
    ys1 = xs
    ys2 = xs**2
    ys3 = np.sqrt(xs)
    
    #create a figure with 4 axes arranged in 1 row
    fig, axs = plt.subplots(1, 4, figsize=(8, 3)) #figsize is (width, height) in inches
    
    #remember that functions can be used as values, so we can simply construct a list of
    #functions and iterate over them, so that we don't have to re-type everything over 
    #and over again
    #function(arg1, arg2, ...) --- calls the function
    #function                  --- use the function as a value
    for plot_function in [axs[0].plot, axs[1].semilogx, axs[2].semilogy, axs[3].loglog]:
        #the third argument is "[line style][marker style]
        #color= self-explanatory, 
        #       the numbers are (red, green, blue, alpha) from 0 to 1, alpha is opacity=(1-transparency)
        #lw = line width
        #ms = marker size
        plot_function(xs, ys1, '-o', color='red', lw=0.25, ms=3)
        plot_function(xs, ys2, ':s', color='green', lw=0.5, ms=3)
        plot_function(xs, ys3, '--^', color=(0.25, 0.0, 0.1, 0.25), lw=1, ms=3)
    
    titles = ['linear', 'semilogx', 'semilogy', 'loglog']
    #zip zips to iterables, e.g.,
    #zip([a, b, c], [1, 2, 3]) == [(a, 1), (b, 2), (c, 3)]
    for ax, title in zip(axs, titles):
        ax.set_title(title)
        ax.set_xlabel('x axis')
        ax.set_ylabel('y axis')
    
    return fig, axs

plt.close('all') #close all previously opened figures
fig, axs = plot_different_axscales(10)
fig.supxlabel("Common x-axis name")
fig.supylabel("Common y-axis name")
#reduce the whitespace around the edges as much as possible
fig.tight_layout()
plt.show()