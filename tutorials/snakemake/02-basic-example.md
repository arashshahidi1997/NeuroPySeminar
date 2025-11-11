
# Basic Example

## create a `Snakefile` under directory `workflow`.

In the working directory, create a new file called Snakefile with an editor of your choice. We propose to use the integrated development environment (IDE) tool Visual Studio Code, since it provides a good syntax highlighting Snakemake extension and a remote extension for directly using the IDE on a remote server. In the Snakefile, define the following rule:

# Step 0: Generate Raw Data
```python
rule generate_data:
    output:
        "raw/freq-{freq}_r-{r}.npy"
    params:
        freq=lambda wildcards: float(wildcards.freq),
        r=lambda wildcards: float(wildcards.r),
        sample_rate=1000.,
        seconds=10.,
        noise_std=0.1
    run:
        from emd.simulate import ar_oscillator
        import os
        import numpy as np
        osc = ar_oscillator(
            params.freq, params.sample_rate, params.seconds, params.r, params.noise_std
        )
        os.makedirs(os.path.dirname(output[0]), exist_ok=True)
        np.save(output[0], osc)
```

For now don't worry about the details of this rule, we will explain it later in the tutorial. Now at the top of your Snakefile, add the following code to specify the parameters for generating the data:

```python
FREQS = [5., 10., 20.]
RS = [0.5, 0.7, 0.9]
rule all:
    input:
        expand("raw/freq-{freq}_r-{r}.npy", freq=FREQS, r=RS)
```

---

At this point your Snakefile should look like this:

```python
FREQS = [5., 10., 20.]
RS = [0.5, 0.7, 0.9]
rule all:
    input:
        expand("raw/freq-{freq}_r-{r}.npy", freq=FREQS, r=RS)

rule generate_data:
    output:
        "raw/freq-{freq}_r-{r}.npy"
    params:
        freq=lambda wildcards: float(wildcards.freq),
        r=lambda wildcards: float(wildcards.r),
        sample_rate=1000.,
        seconds=10.,
        noise_std=0.1
    run:
        from emd.simulate import ar_oscillator
        import os
        import numpy as np
        osc = ar_oscillator(
            params.freq, params.sample_rate, params.seconds, params.r, params.noise_std
        )
        os.makedirs(os.path.dirname(output[0]), exist_ok=True)
        np.save(output[0], osc)
```

try running the workflow with the command:

first a dry-run to see what will be executed:
```bash
snakemake -n
```

```bash
job              count
-------------  -------
all                  1
generate_data        9
total               10
```

---

Now run the workflow for real:
```bash
snakemake --cores 1
```
or in short:
```bash
snakemake -c 1
```

You can dedicate more CPU cores to speed up the execution. For example, to use 4 cores, run:
```bash
snakemake -c 4
```

---

# Step 1: Bandpass Filter
```python
rule bandpass:
    input:
        "raw/freq-5.0_r-0.5.npy",
    output:
        "derivatives/bandpass/freq-5.0_r-0.5.npy"
    params:
        freq=5
    script:
        "../scripts/bandpass.py"
```

create a new file `scripts/bandpass.py` with the following content:

```python
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
```

Update the `rule all` to include the output of this new rule:

```python
rule all:
    input:
        "derivatives/bandpass/freq-5.0_r-0.5.npy"
```

rerun the workflow:
```bash
snakemake -c 4
```

---

# Step 2: Bandpass Filter (Genralized)

```python
rule bandpass:
    input:
        "raw/freq-{freq}_r-{r}.npy",
    output:
        "derivatives/bandpass/freq-{freq}_r-{r}.npy"
    params:
        freq=lambda wildcards: float(wildcards.freq),
    script:
        "../scripts/bandpass.py"
```

No need to change the script `scripts/bandpass.py`. The wildcards `{freq}` and `{r}` will be replaced with the actual values when the Snakefile is executed.

Now update the `rule all` to include all combinations of frequencies and r values:

```python
rule all:
    input:
        expand("derivatives/bandpass/freq-{freq}_r-{r}.npy", freq=FREQS, r=RS)
```

---

# Step 3: Hilbert Transform

```python
rule hilbert:
    input:
        "derivatives/bandpass/freq-{freq}_r-{r}.npy"
    output:
        amp="derivatives/hilbert/freq-{freq}_r-{r}_amplitude.npy",
        phase="derivatives/hilbert/freq-{freq}_r-{r}_phase.npy"
    params:
        freq=lambda wildcards: float(wildcards.freq),
    script:
        "../scripts/hilbert.py"
```

create a new file `scripts/hilbert.py` with the following content:

```python
# apply Hilbert transform to the bandpass filtered data
import numpy as np
from scipy.signal import hilbert
sig = np.squeeze(np.load(snakemake.input[0]))
analytic_signal = hilbert(sig)
amplitude_envelope = np.abs(analytic_signal)
instantaneous_phase = np.angle(analytic_signal)
np.save(snakemake.output.amp, amplitude_envelope)
np.save(snakemake.output.phase, instantaneous_phase)
```

update the `rule all` to include the outputs of this new rule:

```python
rule all:
    input:
        expand("derivatives/hilbert/freq-{freq}_r-{r}_amplitude.npy", freq=FREQS, r=RS)
```

---

# Step 4: Plot Results

```python
rule plot_with_python:
    input:
        "derivatives/hilbert/freq-{freq}_r-{r}_amplitude.npy"
    output:
        "figures/python-plot/freq-{freq}_r-{r}_amplitude.png"
    script:
        "../scripts/plot.py"
```

create a new file `scripts/plot.py` with the following content:

```python
import numpy as np
import matplotlib.pyplot as plt
sig = np.squeeze(np.load(snakemake.input[0]))
plt.figure(figsize=(10, 4))
plt.plot(sig)
plt.title('Hilbert Transform Result')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.savefig(snakemake.output[0])
```

update the `rule all` to include the outputs of this new rule:

```python
rule all:
    input:
        expand("figures/python-plot/freq-{freq}_r-{r}_amplitude.png", freq=FREQS, r=RS)
```

---

# Step 5: Complete Snakefile

```python
FREQS = [5., 10., 20.]
RS = [0.5, 0.7, 0.9]

rule all:
    input:
        expand("figures/python-plot/freq-{freq}_r-{r}_amplitude.png", freq=FREQS, r=RS)

rule generate_data:
    output:
        "raw/freq-{freq}_r-{r}.npy"
    params:
        freq=lambda wildcards: float(wildcards.freq),
        r=lambda wildcards: float(wildcards.r),
        sample_rate=1000.,
        seconds=10.,
        noise_std=0.1
    run:
        from emd.simulate import ar_oscillator
        import os
        import numpy as np
        osc = ar_oscillator(
            params.freq, params.sample_rate, params.seconds, params.r, params.noise_std
        )
        os.makedirs(os.path.dirname(output[0]), exist_ok=True)
        np.save(output[0], osc)


rule bandpass:
    input:
        "raw/freq-{freq}_r-{r}.npy",
    output:
        "derivatives/bandpass/freq-{freq}_r-{r}.npy"
    params:
        freq=lambda wildcards: float(wildcards.freq),
    script:
        "../scripts/bandpass.py"

rule hilbert:
    input:
        "derivatives/bandpass/freq-{freq}_r-{r}.npy"
    output:
        amp="derivatives/hilbert/freq-{freq}_r-{r}_amplitude.npy",
        phase="derivatives/hilbert/freq-{freq}_r-{r}_phase.npy"
    params:
        freq=lambda wildcards: float(wildcards.freq),
    script:
        "../scripts/hilbert.py"

rule plot_with_python:
    input:
        "derivatives/hilbert/freq-{freq}_r-{r}_amplitude.npy"
    output:
        "figures/python-plot/freq-{freq}_r-{r}_amplitude.png"
    script:
        "../scripts/plot.py"
```