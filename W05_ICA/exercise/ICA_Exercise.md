# ICA on Synaptic Inputs

This analysis focuses on applying Independent Component Analysis (ICA) to a segment of Local Field Potential (LFP) data and evaluating its components for synaptic activity and artifact removal.

## Steps

### 1. Load LFP Segment
- **Data Description**: Load a segment of LFP data consisting of 16 channels, with a duration of 50–100 seconds.
- **Objective**: Use this segment as the input for ICA decomposition.
- **Pythonic Hint**: Use `numpy` or `pandas` to load and handle your LFP data. If the data is in a specific file format like `.mat` or `.edf`, consider libraries such as `scipy.io` or `mne`.

---

### 2. Apply ICA Decomposition
- **Method**: Apply ICA decomposition using the FastICA algorithm to the raw LFP data.
  - **Data Structure**: Treat each channel as a feature (dimension) and each time point as a sample. Ensure the input data matrix is organized as 
    $$
    X \in \mathbb{R}^{T \times C},
    $$
    where \( T \) is the number of time points and \( C \) is the number of channels.
  - **Pythonic Hint**:
    ```python
    from sklearn.decomposition import FastICA
    
    # Assuming `lfp_data` is your input matrix with shape (T, C)
    ica = FastICA(n_components=C, random_state=42)
    S = ica.fit_transform(lfp_data)  # Independent components (sources)
    A = ica.mixing_  # Mixing matrix (spatial loadings)
    ```

---

### 3. Analyze ICA Components

#### a. Spatial Profiles of IC Loadings
1. **Matrix \( A \)**:
   - Extract the spatial loadings matrix \( A \) (mixing matrix) from the ICA decomposition.
   - **Plot**: Visualize the spatial profile of the columns of \( A \).
   - **Pythonic Hint**:
     ```python
     import matplotlib.pyplot as plt
     plt.plot(A)
     plt.title("Spatial Profiles of ICA Loadings")
     plt.xlabel("Channels")
     plt.ylabel("Loadings")
     plt.show()
     ```

2. **Current Source Density (CSD)**:
   - Compute the CSD for each column \( A_k(x) \), using the formula:
     $$
     \text{CSD}_k(x) = -\frac{d^2 A_k(x)}{dx^2}.
     $$
   - **Pythonic Hint**:
     ```python
     import numpy as np
     # Numerical second derivative using finite differences
     CSD = -np.diff(A, n=2, axis=0)  # Apply along spatial dimension
     plt.plot(CSD)
     plt.title("Current Source Density (CSD)")
     plt.xlabel("Channels")
     plt.ylabel("CSD")
     plt.show()
     ```

3. **Component Activations**:
   - Extract the activation time series \( s \) for the first \( K \) components.
   - **Plot**: Time series of activations for these components.
   - **Pythonic Hint**:
     ```python
     for k in range(K):
         plt.plot(S[:, k], label=f"Component {k+1}")
     plt.title("Activations for the First K Components")
     plt.xlabel("Time Points")
     plt.ylabel("Activation")
     plt.legend()
     plt.show()
     ```

4. **Power Spectra**:
   - Compute the power spectra of the activations in:
     - **Theta Range**: \( 4 \, \text{Hz} \leq f \leq 8 \, \text{Hz} \)
     - **Gamma Range**: \( 30 \, \text{Hz} \leq f \leq 100 \, \text{Hz} \)
   - **Pythonic Hint**:
     ```python
     from scipy.signal import welch
     fs = 1000  # Sampling frequency (example: 1000 Hz)
     for k in range(K):
         f, Pxx = welch(S[:, k], fs=fs, nperseg=1024)
         plt.semilogy(f, Pxx, label=f"Component {k+1}")
     plt.xlim([0, 100])  # Adjust range to show theta and gamma
     plt.title("Power Spectra of Activations")
     plt.xlabel("Frequency (Hz)")
     plt.ylabel("Power Spectral Density")
     plt.legend()
     plt.show()
     ```

---

#### b. Identify and Remove EMG Artifacts
1. **Identify EMG Components**:
   - Look for components with:
     - A high-frequency spectral peak (\( > 200 \, \text{Hz} \)).
     - Uniform spatial loadings across channels.
   - **Pythonic Hint**:
     ```python
     # Identify EMG components
     emg_components = [k for k in range(C) if max(f[k] > 200) and np.std(A[:, k]) < threshold]
     ```

2. **Remove EMG Components**:
   - Exclude the identified EMG components from the signal.
   - **Pythonic Hint**:
     ```python
     # Reconstruct the signal without EMG components
     cleaned_S = S.copy()
     cleaned_S[:, emg_components] = 0
     cleaned_signal = np.dot(cleaned_S, A.T)
     ```

3. **Compare Spectra Before and After**:
   - Select one channel of LFP data.
   - Compute and compare its power spectra before and after removing the EMG component.
   - **Pythonic Hint**:
     ```python
     # Power spectra comparison
     f_orig, Pxx_orig = welch(lfp_data[:, selected_channel], fs=fs, nperseg=1024)
     f_clean, Pxx_clean = welch(cleaned_signal[:, selected_channel], fs=fs, nperseg=1024)
     
     plt.semilogy(f_orig, Pxx_orig, label="Original")
     plt.semilogy(f_clean, Pxx_clean, label="Cleaned")
     plt.title("Power Spectra Before and After EMG Removal")
     plt.xlabel("Frequency (Hz)")
     plt.ylabel("Power Spectral Density")
     plt.legend()
     plt.show()
     ```

---

### Suggested Libraries
- **Data Handling**: `numpy`, `pandas`
- **Signal Processing**: `scipy`, `mne`, `matplotlib`
- **ICA**: `scikit-learn`