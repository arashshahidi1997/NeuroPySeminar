---
title: "Multitaper Spectrogram"
author: "Arash Shahidi"
theme: "black"
width: 1280 
height: 720 
---

# Spectral analysis Lecture 1

# Recommended resources

  * Mitra, P.P., and Pesaran, B. (1999). Analysis of Dynamic Brain Imaging Data. Biophys J 76, 691-708.
  * Digital signal processing using Matlab for students and researchers by John Leis
  * Observed Brain Dynamics by Partha Mitra and Heman Bokil
  * Analyzing Neural Time Series Data (Issues in Clinical and Cognitive Neuropsychology) by Mike Cohen
  * Bruns, A. (2004). Fourier-, Hilbert- and wavelet-based signal analysis: are they really different approaches? J Neurosci Methods 137, 321-332.
  * Pereda, E., Quiroga, R.Q., and Bhattacharya, J. (2005). Nonlinear multivariate analysis of neurophysiological signals. Prog Neurobiol 77, 1-37.
  * <http://ctnsrv.uwaterloo.ca/vandermeerlab/doku.php?id=analysis:course-w16>
  * Chronux and FieldTrip matlab toolboxes (<http://www.fieldtriptoolbox.org/start>)

# Objectives of univariate spectral analysis

Given a signal (e.g. voltage in time from the brain), we want to characterize its frequency content over time. For instance, we would like to

  * Divide it into distinct segments in time
  * Identify interesting frequency bands in each segment
  * Determine when there is above-chance activity in the interesting bands

To do that, we first need a good description of the frequency content of the signal

# Time series – definitions (1)

  * A stochastic process – is a single realization of some PDF where the values are indexed
  * For instance, a continuous time series x(t) is a stochastic (random) process
  * The time series is considered stationary if its PDF does not change when the signal is shifted over time. Then parameters (e.g. mean, variance, and skewness) are fixed over time
  * A process is considered ergodic if its parameters can be determined from a finite sample
  * We usually assume that signals are ergodic but non-stationary

# Time series – definitions (2)

  * What can be assumed is wide-sense stationarity (WSS)

  * This means that the process has a mean and auto-correlation that do not depend on time:
    
    $\\mathbb{E}{x(t)}=m\_{x}(t)=m\_{x}(t+\\tau)\\forall\\tau\\in\\mathbb{R}$
    $\\mathbb{E}{x(t\_{1})x(t\_{2})}=R\_{x}(t\_{1},t\_{2})=R\_{x}(t\_{1}+\\tau,t\_{2}+\\tau)=R\_{x}(t\_{1}-t\_{2},0)\\forall\\tau\\in\\mathbb{R}$
    $r\_{xx}(\\tau)=E\[x(t)x^{\*}(t-\\tau)\]$

  * Although that is a weaker assumption than stationarity, even WSS is unusually not met, so most analyses have to be done in "windows” or segments in which WSS can be assumed

# Sampling a continuous signal (1)

  * In reality, we process signals using digital computers. In the transition from a continuous signal to a computerized representation there are two steps
    1.  Digitization – division of the ordinate (values) of the signal into a reduced set. This is called analog-to-digital (AD) conversion and is mathematically equivalent to division and rounding
    2.  Discretization – sampling the signal in discrete points in time (division of the abscissa). For instance, if we sample x(t) every $\\Delta t$ sec, we then have a sampled (discretized) signal x\[n\]=x(n$\\Delta t$), with n=1,2,...,N. In that case the sampling frequency is fs =1/$\\Delta t$
  * Digitization only causes loss of resolution, but discretization can cause errors in the spectral estimation (aliasing or folding)

# Sampling a continuous signal (2)

  * Nyquist-Shannon sampling theorem states that signals that are band-limited (their maximal frequency is f) can be reconstructed perfectly from the sampled version if fs $\\ge 2^{\*}f$

  * The reconstruction is done by Whittaker-Shannon interpolation – multiplying each sample by a sinc function
    
    $x(t)=\\sum\_{n=-\\infty}^{\\infty}x\[n\]\\cdot sinc(\\frac{t-nT}{T})$

  * The maximal frequency that can be represented by sampling without aliasing is thus fs/2; this is called the Nyquisit frequency

  * Since in general signals are not band-limited, a low-pass filter is usually applied prior to sampling to avoid aliasing

# Fourier transform (1)

  * For a given frequency f, the continuous FT is a complex function of the signal x(t):
    
    $X(f)=\\int\_{-\\infty}^{\\infty}x(t)\\cdot e^{-i2\\pi ft}dt.$

  * Interpretations:
    
      * Basis change – the FT can be regarded as a change of basis from time to frequency
      * Decomposition – the FT describes x(t) in terms of complex exponentials; because $e^{\\wedge}(ix)=cos\~x+i\~sin\~x$ it is equivalent to describing x(t) as a weighted sum of cosines and sines

# Fourier transform (2)

  * Since we usually use sampled (discretized) signals for which the FT is not defined, an approximation, the discrete-time FT (DTFT), is defined as
    
    $X(\\omega)=\\sum\_{n=-\\infty}^{\\infty}x\[n\]e^{-i\\omega n}.$

  * Or, for a finite signal, as:
    
    $X(\\omega)=\\sum\_{n=0}^{L-1}x\[n\]e^{-i\\omega n}$

  * In practice we use the discrete FT, or DFT, which also discretizes the frequency axis (from f-\>k/n):
    
    $X\_{k}=\\sum\_{n=0}^{N-1}x\_{n}e^{-\\frac{2\\pi i}{N}kn} k=0,...,N-1$

  * All transforms are invertible, and the inverse DFT (IDFT) is defined as
    
    $x\_{n}=\\frac{1}{N}\\sum\_{k=0}^{N-1}X\_{k}e^{\\frac{2\\pi i}{N}kn} n=0,...,N-1.$

  * Computationally, we use a recursive algorithm called fast Fourier transform (FFT) to compute the DFT of a finite- length, digitized and discretized signal
    
    $X\_{k}=\\sum\_{n=0}^{N-1}x\_{n}e^{-\\frac{2\\pi i}{N}kn} k=0,...,N-1$

# Spectral energy density

  * Spectral density of a signal is defined as the square of its FT:
    
    $S(f)=|\\frac{1}{\\sqrt{2\\pi}}\\sum\_{n=-\\infty}^{\\infty}X\_{n}e^{-2\\pi inf}|^{2}$

  * Wiener-Khinchin theorem: the PSD of a WSS stochastic process is the FT of the auto- correlation function:
    
    $S\_{xx}(f)=\\sum\_{k=-\\infty}^{\\infty}r\_{xx}\[k\]e^{-j2\\pi kf}$
    
    $r\_{xx}\[k\]=E\[x\[n\]x^{\*
    }\[n-k\]\]$
    \=\>PSD exists only if the signal is WSS and thus the auto- correlation can be written as a function of one variable

# Properties of the FT and spectral density

  * Linearity: if h(x)=af(x)+bg(x), then
    
    $\\hat{h}(\\xi)=a\\cdot\\hat{f}(\\xi)+b\\cdot\\hat{g}(\\xi).$

  * Convolution:
    if $h(x)=(f\*g)(x)=\\int\_{-\\infty}^{\\infty}f(y)g(x-y)dy,$
    then $\\hat{h}(\\xi)=\\hat{f}(\\xi)\\cdot\\hat{g}(\\xi).$

  * Parseval's theorem (energy conservation):
    
    $\\int\_{-\\infty}^{\\infty}|f(x)|^{2}dx=\\int\_{-\\infty}^{\\infty}|\\hat{f}(\\xi)|^{2}d\\xi.$

# Real data – no assumptions are met

  * Nonstationarity (at most piece-wise weak-sense stationarity)
  * Nonlinearity
  * Nongaussianity

# Time-frequency localization or spectral concentration problem

If we had a discrete time series for infinite time, we would be able to evaluate its Fourier transform X(f), where

$X(f)=\\sum\_{-\\infty}^{\\infty}x(t)e^{-2\\pi ift}$

However, we only get finite segments of data (and if the process is nonstationary, then even smaller segments). Therefore, we can only evaluate the truncated or short-time DFT

$X\_{T}(f)=\\sum\_{-T/2}^{T/2}x(t)e^{-2\\pi jt}$

Plugging in the Fourier representation of x(t) we find that finite data results in convolution of the spectrum with Dirichlet kernel. The Dirichlet kernel is the Fourier transform of a rectangular window.

$X\_{T}(f)=\\int\_{-1/(2\\Delta t)}^{1/(2\\Delta t)}D\_{T}(f-f^{\\prime})X(f^{\\prime})df^{\\prime}$
$D\_{T}(f)=\\frac{sin(\\pi fT)}{sin(\\pi f)}$

Problem: time-frequency localization Heisenberg-Gabor uncertainty principle

$\\Delta f\~\\Delta t\>1/(4\\pi)$

# Narrowband and broadband bias

<br>

<br>
Two problems caused by the finite window:
(a) central lobe has finite width, $\Delta f=2/T$ (&quot;narrowband bias&quot;)
(b) Large side lobes: height of first side lobe is 20% of central lobe (&quot;broadband bias&quot;). Doesn&#39;t decrease with increase of T.

# Bias reduction

"Tapering" the data with a smooth function (hanning, hamming, etc) is a tradeoff of narrowband and broadband biases. Tapering – replacing Dirichlet kernel with Fourier transform of the taper

  * increases the central lobe width (decrease frequency resolution)
  * reduces the sidelobe height (decrease broadband bias)
  * Tradeoff between central lobe width and sidelobe height

<br>
Tapering causes us to down- weight the edges of the data window (we lose data). Is there a way of recovering this information?
Does not reduce the variance.
What is the optimal taper?

# Variance reduction tradeoffs

  * Segmentation into small windows increases the narrowband bias
  * Increasing window size hits nonstationarity problem.
  * Uncontrolled smoothing is bad if the spectrum is mixed (spectral lines on a smooth background).
  * Smoothers are nonlinear, since smoothers work on the raw spectrum estimation, phase information is lost and not used, and line detection is less efficient.
  * What is the optimal way to reduce the variance and keep the bias low?

# Direct estimators: fight with bias and variance

  * Periodogram (equivalent to autocovariance in time domain) Spectrum convolved with the Dirichlet kernel. Biased, inconsistent.
    
    $\\hat{S}*{D}(f)=|\\sum*{n=0}^{N-1}x(n)D\_{n}e^{-2\\pi ifn}|^{2}$

  * Bartlett Method : Averaging Periodograms
    
      * Data is sub-divided into non-overlapping segments and spectrum is estimated from this ensemble. Increases bias, reduces variance.

  * Welch Method : Averaging Modified Periodograms Same as Bartlett, but
    
      * Data segments may overlap . reduces variance.
      * Applying data window (taper). Reduces bias.

  * Blackman & Tuckey Method : Smoothed Periodogram
    
      * Performs smoothing of the square magnitude of the DFT in the frequency domain without segmentation and averaging.
    
    $\\tilde{S}(f)=\\hat{S}\_{D}(f)\*G(f)$

  * Or any combination of segmentation, windowing and smoothing.. But what is the optimal way to control bias and variance?

# Multitaper framework for Spectral Concentration Problem

Find strictly time localized functions $W\_{t}, t=1..T$ whose Fourier transforms are maximally localized on a frequency interval $\[-W,W\]$. This gives a basis set (Slepian functions) used for spectral estimation on finite time segments

Find functions $W\_{t}$ whose Fourier Transform U(f)
Are maximally concentrated in the frequency interval $\[-W,W\]$. To do this, maximize $\\lambda$ (spectral concentration) given by

$U(f)=\\sum\_{t=1}^{T}w\_{t}e^{-2\\pi jt}$
$\\lambda\_{z}=\\frac{\\int\_{-\\infty}^{\\infty}|U(f)|^{f}df}{\\int\_{-\\infty}^{\\infty}U(f)|^{2}df}$

Maximizing the spectral concentration ratio gives rise to an eigenvalue equation for a symmetric matrix

$\\sum\_{t=1}^{T}\\frac{sin\[2\\pi W(t-t^{\\prime})\]}{\\pi(t-t^{\\prime})}w(t^{\\prime})=\\lambda w(t)$

Eigenvectors = Slepian sequences - optimal tapers, Eigenvalues – their spectral concentration

# Spectral and statistical properties of the Slepian functions

  * K=2WT Eigenvalues are close to 1 (rest close to 0), corresponding to 2WT functions concentrated within $\[-W,W\]$ – yield an ensemble of estimates
  * Slepian sequences are orthonormal on $\[0, T\]$
  * Slepian functions (Fourier transform of Slepian sequences) are orthonormal on $\[-1/2 1/2\]$ and orthogonal on $\[-W,W\]$ – yield independent statistical estimates

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

# Multitaper spectral estimator

$S\_{MT}=\\frac{1}{K}\\sum\_{k=1}^{K}||x\_{k}(f)||^{2}$

where $x\_{k}(f)=\\sum\_{t=1}^{N}w\_{t}(k)x\_{t}e^{-2\\pi ift}$
wt, k=1.. K – Slepian sequences

Replaces Dirichlet kernel with $H(f)=\\frac{1}{k}\\sum\_{k=1}^{K}|U\_{k}(f)|^{2}$ boxcar-shaped kernel

In practice, one could do: weighting by $1/\\lambda\_{k,.}$ or better adaptive iterative weighting procedure

$S\_{dHf}(f)=\\frac{\\sum\_{k=1}^{k}|d\_{k}(f)x\_{k}(f)|^{2}}{\\sum\_{k=1}^{k}|d\_{k}(f)|^{2}}d\_{k}(f)=\\frac{\\sqrt{2\_{\_{k}}}S\_{k,,}(f)}{\\lambda\_{k}S\_{k,,(f)+(1-\\delta\_{k})\\sigma^{2}}$

# Illustration of multitaper estimator

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
Multitaper (9 tapers) vs theoretical spectrum
<br>

# Illustration: Periodogram vs multitaper estimator

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

# Illustration: Effect of number of windows/trials

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

# Statistical issues

  * The classical theoretical framework for the statistical analysis of univariate spectral measures is Gaussian
  * The underlying assumption is not that the process X is Gaussian but rather that its FT is Gaussian
  * This is motivated by the fact that the DFT is a sum of many terms and is therefore approximately Gaussian (central limit theorem)
  * Assuming that spectra have been estimated using M windows (Welch method and/or multi-taper method), the confidence limits under a Gaussian assumption are obtained by computing the SD and taking e.g. for a 95% confidence limit, 1.96 SDs around the mean (or expected value)

# Statistical analysis of the spectrum

Under utopian conditions the estimate of the spectrum has a Chi-squared distribution with d.f. =2\*2WT Useful: the variance of the In(spectrum) doesn't depend on frequency (trigamma function).
Can use Bartlet's test for homogeneity of variance (M-statistics)

$M=Kv\[ln(\\frac{1}{K}\\sum\_{k=1}^{K}\\tilde{S}*{k})-\\frac{1}{K}\\sum*{k=1}^{K}ln(\\tilde{S}*{k})\]$ ,where $S*{k\_{\\prime}}, k=1..K$ - independent estimates

with v d.f., M is \~ Chi-sq distributed

  * Presence of a sharp line in a continuum spectrum: F-statistics (local LSE minimization from Slepian eigendecomposition)
  * Thomson: “Gaussianity and stationarity are fairy tales invented for the amusement of undergraduates”.
  * In real life one can estimate bias/variance and construct error bars using the jackknife over ensemble of spectrum estimates.

# Non-Gaussian statistics: the jackknife

  * The Gaussian framework (and central limit theorem) assume that the terms are iid, which is rarely the case for serially-correlated time series
  * An alternative framework is non-parametric. The simplest of these is the jackknife (leave-one-out)
  * Using the jackknife, M statistics Oik are computed, each based on M- 1 samples (e.g. all but one of the tapers, or all but one of the Welch windows)

# Jackknife bias and variance

  * the JK bias
    
    $bias^{jk}=(M-1)(\\langle\\theta\_{i}^{jk}\\rangle\_{i=1.M}-\\hat{\\theta}/M)$

  * the JK variance
    
    $var^{jk}=(M-1)\\langle(\\theta\_{i}^{jk}-\\langle\\theta^{jk}\\rangle\_{i=1..M})^{2}\\rangle\_{i=1.M}$

  * This method can be applied to spectra, as well as other measures (to be discussed later)

  * Useful related measure : pseudovalue
    
    $PV(S)*{i}=nS(X)-(n-1)S(X*{i})$
