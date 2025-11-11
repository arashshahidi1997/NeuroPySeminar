import numpy as np
import matplotlib.pyplot as plt
sig = np.squeeze(np.load(snakemake.input[0]))
plt.figure(figsize=(10, 4))
plt.plot(sig)
plt.title('Hilbert Transform Result')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.savefig(snakemake.output[0])
