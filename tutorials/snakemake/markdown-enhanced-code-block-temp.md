```python
# apply Hilbert transform to the bandpass filtered data
import numpy as np
from scipy.signal import hilbert
sig = np.load(snakemake.input[0])
analytic_signal = hilbert(sig)
amplitude_envelope = np.abs(analytic_signal)
instantaneous_phase = np.angle(analytic_signal)
```