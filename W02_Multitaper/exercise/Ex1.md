# Machine Learning and Analysis of Neural Data

Summer term 2022, Stefan Hausler, Anton Sirota, Martion Stemmler Exercise Sheet: Spectral analysis 1. 30.05.22 Exercise 1.

# Theory:

1.  prove that $\\int\_{-\\infty}^{\\infty}X(f^{\\prime})Y(f-f^{\\prime})=F(x(t)\*y(t))$
2.  derive Fourier transform of the gaussian, step function.

# Hands on analysis:

Data: 16 channels of hippocampal LFP time series from a file lfp\_1shank.mat. Matrix lfps (1250Hz sampling rate samples x 16 channels)

1.  Extract a short segment of data for any one channel. Implement and compute periodogram spectrum estimate from 1 to 100 Hz. Explore the effect of window size choice.
2.  Implement/compute estimate using Welch estimator (dividing the data into multiple overlapping windows). Implement zero padding (nFFT=$2^{\*}N$). Compute spectrum to be able to see clear theta (8-10 Hz) and gamma (30-80 Hz) bands
      * Study the effect of number of windows on variance and spectral resolution Study the effect of window size and nFFT on resolution of spectral peaks. Gradually increase the data segment size and study the effect on variance.
3.  Implement/compute multitaper spectral estimate.
      * Explore the effect of time-frequency bandwidth (NW) on variance and resolution when computing on short data segment (1 sec), compare to periodogram/Welch.
      * Using data segment of 10 seconds length, explore the effect of the window length, zero padding and NW on resolvable spectral features in the power spectrum for theta and gamma bands.
      * Vary the analysis across channels. Plot power spectra (average across windows) across depth to appreciate changes in the spectral content in depth, described what you see.
