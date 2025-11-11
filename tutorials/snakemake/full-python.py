FREQS = [5., 10., 20.]
RS = [0.7, 0.8, 0.95]

sample_rate=1000.
seconds=10.
noise_std=0.1

from emd.simulate import ar_oscillator
import numpy as np

for freq in FREQS:
	for r in RS:
		output=f"raw/freq-{freq}_r-{r}.npy"
		osc = ar_oscillator(
			freq, sample_rate, seconds, r, noise_std
		)
		np.save(output, osc)
