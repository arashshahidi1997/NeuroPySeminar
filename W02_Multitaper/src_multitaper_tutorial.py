from pathlib import Path
import scipy.io
import ghostipy as gsp

datadir = Path("/storage2/arash/teaching/neuropy/data/ds-montgomery-v1")
filename = datadir / "ws_data_1shank.mat"

data = scipy.io.loadmat(filename)
print(data.keys())

lfp = data["lfps"].squeeze()  # shape (n_channels, n_times)
print(lfp.shape)

fs = 1250  # Sampling frequency in Hz
channel = 0  # Select the first channel
signal = lfp[channel, :]

# Read the documentation for the multitaper spectrogram function: gsp.mtm_spectrogram
print(help(gsp.mtm_spectrogram))

# Parameters for multitaper spectral estimation
bandwidth = 4.0  # Time-bandwidth product
nfft = 2048          # Number of FFT points
# ... adjust parameters as needed

# run mtm_spectrogram

# explore and do the exercise!

