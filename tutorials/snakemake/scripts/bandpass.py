# apply bandpass filter to the raw data
from scipy.signal import butter, filtfilt
import numpy as np

sig = np.squeeze(np.load(snakemake.input[0]))
freq = snakemake.params.freq

fs = 1000  # sample rate
lowcut = freq - 2
highcut = freq + 2
order = 4

b, a = butter(
    order, [lowcut, highcut], fs=fs, btype='band'
)
filtered_sig = filtfilt(b, a, sig)

np.save(snakemake.output[0], filtered_sig)