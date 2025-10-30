# Machine Learning and Analysis of Neural Data

Summer term 2022, Stefan Hausler, Anton Sirota, Martin Stemmler  
Exercise Sheet: Spectral analysis 1. 30.05.22  
Exercise 2.

## Theory:

**Data:** 16 channels of hippocampal LFP time series from a file `lfp_1shank.mat`.  
Matrix `lfps` (1250Hz sampling rate samples × 16 channels)

1. Take a 30s long segment of data on a channel with largest theta power. Compute dynamic spectrum in the low frequency band (<20 Hz) using:
   
   a. multitaper spectrogram with a sliding window (overlap can be large, vary the window size and NW to see the effect on frequency/time resolution). Plot. Describe.
   
   b. using scalogram computed using wavelet transform (e.g. using Morlet wavelet using some package). Plot. Describe.
   
   c. filter the signal in [5 20] Hz band, compute analytic signal using Hilbert transform and extract instantaneous power/phase, compute inst. frequency. Plot. Describe.
