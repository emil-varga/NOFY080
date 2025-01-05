import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

plt.close('all')

#low-pass and high-pass RC filters
def Hlpf(f, tau):
    "response of a low-pass RC filter with a time constant tau"
    w = 2*np.pi*f
    return 1/(1 + 1j*w*tau)
def Hhpf(f, tau):
    "response of a high-pass RC filter with a time constant tau"
    w = 2*np.pi*f
    return 1j*w*tau/(1 + 1j*w*tau)

def apply_filter(x, fs, H, tau):
    """
    filter signal x sampled at sampling frequency fs and
    transfer function H(f, tau)
    """
    X = np.fft.fft(x)
    freqs = np.fft.fftfreq(len(x), 1/fs)
    h = H(freqs, tau)
    return np.fft.ifft(X*h)


#load file a usual
file = '../noisy_signal.npy'
d = np.load(file, allow_pickle=True).item()

x = d['data'] # data
fs = d['rate'] # sampling frequency
T = d['time'] # total measurement time

times = np.arange(0, T, 1/fs) # time array
freqs, Pxx = sig.periodogram(x, fs=fs) # power spectral density

#first plot everything
fig1, (axt, axf) = plt.subplots(2, 1)
fig1.suptitle("signal and the PSD")
axt.plot(times, x)
axt.set_xlabel('time (s)')
axt.set_ylabel('signal (V)')
axf.semilogy(freqs, Pxx, label='original signal')
axf.set_xlabel('frequency (Hz)')
axf.set_ylabel('PSD (V$^2$/Hz)')
fig1.tight_layout()

# next plot the result after applying the filter
fig2, axs = plt.subplots(4, 1, sharex=True)
axs[0].plot(times, x)
axs[0].set_title('original signal')
tau_200Hz = 1/(2*np.pi*200)
tau_1000Hz = 1/(2*np.pi*1000)
axs[1].plot(times, apply_filter(x, fs, Hlpf, tau_200Hz))
axs[1].set_title('low-pass, 200 Hz')
axs[2].plot(times, apply_filter(x, fs, Hhpf, tau_1000Hz))
axs[2].set_title('high-pass, 1000 Hz')

# now use the bandpass filter
sos = sig.iirfilter(4, (4321-10, 4321+10), btype='band', fs=fs, output='sos')
xfilt = sig.sosfilt(sos, x)
axs[3].plot(times, xfilt)
axs[3].set_title('butterowrth band-pass 4321$\\pm$10 Hz')
fig2.tight_layout

_, Pxxfilt = sig.periodogram(xfilt, fs=fs)
#compare the original and filtered
axt.plot(times, xfilt)
axf.plot(freqs, Pxxfilt, label='band-pass')
axf.legend(loc='best', frameon=False)
fig1.tight_layout()


#
# Calculating signal envelope
#

#We'll calculate the envelope in two ways:

#1. demodulation + low-pass filter
#first define the low-pass filter we want to use
soslp = sig.iirfilter(4, 100, fs=fs, btype='lowpass', output='sos')

#we want to demodulate on the carrier frequency 4321
f_c = 4321
wc = 2*np.pi*f_c
#first we calculate the mixed signal, where we simply multiply the signal
#with a complex exponential. Using the complex takes care of the unknown phase
#try, for example, demodulating with np.sin(wc*times + phi) for different phases phi

x_mix = xfilt*np.exp(-1j*wc*times)

# the mixed signal contains the modulating signal, which we want, and components
# on 2*f_c, which we don't want so we remove with with the low-pass filter
x_demod = sig.sosfilt(soslp, x_mix)*2 # multiplying by 2 because cos^2(x) = 1/2*(1 - cos(2x))
#x_demod is the (complex) time-dependent amplitude of the signal at frequency f_c
#the envelope is thus simply
env = np.abs(x_demod)

#alternative is the Hilbert transform which calculates the analytic signal 
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.hilbert.html
xh = sig.hilbert(xfilt)
env_hilbert = np.abs(xh)

#And plot everything. Notice that in the case of demodulation a small
#delay develops between signal and envelope. How could this be removed?
#Hint: something on line 97
fig3, ax_demod = plt.subplots()
ax_demod.plot(times, xfilt, label='filtered signal')
ax_demod.plot(times, env, label='envelope, demodulation')
ax_demod.plot(times, env_hilbert, label='envelope, Hilbert')
ax_demod.legend(loc='best')
fig3.tight_layout()
