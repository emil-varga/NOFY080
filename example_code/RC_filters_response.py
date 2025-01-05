import matplotlib.pyplot as plt
import numpy as np

tau=1
freqs = np.logspace(-2, 1)
low_pass = 1/(1 + 1j*2*np.pi*freqs*tau)
high_pass = 1j*2*np.pi*freqs*tau/(1 + 1j*2*np.pi*freqs*tau)
fig, (axL, axH) = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(4,2.5))
axL.loglog(freqs, abs(low_pass))
axH.loglog(freqs, abs(high_pass))
axL.axvline(1/(2*np.pi*tau))
axH.axvline(1/(2*np.pi*tau))

# axL.set_ylim(ymin=1e-3)
fig.supxlabel('frequency')
fig.supylabel('filter response')
fig.tight_layout()
fig.savefig("../RC_filters.pdf")