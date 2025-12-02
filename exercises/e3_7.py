import numpy as np
import matplotlib.pyplot as plt

#we will be using this as a module, so prepare a reusable solution
def estimate_parameters(f, X, Y, plot=False):
    """
    Estimates central frequency and full width at half max of a peak.

    Parameters
    ----------
    f : array
        Frequencies.
    X : array
        X-component of the signal.
    Y : array
        Y-component of the signal.
    plot : bool, optional
        Should we plot? The default is False.

    Returns
    -------
    f0 : float
        Central frequency of the resonance.
    fwhm : float
        Full width at half maximum of the resonance.

    """
    
    #first calculate the magnitude of the response
    R = np.sqrt(X**2 + Y**2)

    if plot: #plot only if asked to
        fig, ax = plt.subplots()
        ax.plot(f, R)

    #now we find the INDEX of the minium and maximum
    ix_max = np.argmax(R)
    ix_min = np.argmin(R)

    if plot:
        #axvline plots a vertical line
        ax.axvline(f[ix_max]) #position of the maximum
        ax.axvline(f[ix_min], ls=':', color='tab:green') #position of the minimum
        
        #axhline plots horizontal line
        ax.axhline(R[ix_max], ls='--', color='tab:orange') #height of the maximum
        
    # now we need to estimate FWHM, which measures the width of the peak at half
    # its maximum value
    
    # first calculate the value of the half maximum, also taking into account an estimate of
    # the background by simply taking the minimum()
    # A more accurate estimation of the background could be achieved with np.percentile()
    T = R.min() + 0.5*(R.max() - R.min()) # = 0.5*(R.max() + R.min())
    if plot:
        ax.axhline(T, color='green')
    
    #now we find all data points where R > T
    fwhm_range_ix = R > T
    # fwhm_range_ix is an ARRAY OF BOOLS of the same size as R (and X, Y, f)
    # which is True where the conditoin R > T is true, and zero otherwise
    # We can use an array like this to create a subset of any other array of the
    # same shape created from only the True positions
    fwhm_range = f[fwhm_range_ix] #these are now the frequencies where R > T
    # now to calculate the full width we just need to know the limits of the interval
    # fwhm_range
    f_left = fwhm_range.min()
    f_right = fwhm_range.max()

    # print(fwhm_range_ix)
    # print(sum(fwhm_range_ix))
    # print(f.shape)
    # print(fwhm_range.shape)

    if plot:
        #highlight the data within FWHM
        ax.plot(fwhm_range, R[fwhm_range_ix], color='magenta', lw=5) #lw=line width
        #and indicate the range
        ax.axvline(f_left, color='red')
        ax.axvline(f_right, color='blue')
        
    #finally, return what we are supposed to return
    f0 = f[ix_max]
    fwhm = f_right - f_left

    return f0, fwhm

if __name__ == '__main__':
    # since we will be importing e11 as a module in e12, we don't want this code to run
    # on import -- hide inside if __name__ == '__main__'
    data = np.loadtxt('data.txt')
    f, X, Y = data.T
    estimate_parameters(f, X, Y, plot=True)
    plt.show()
