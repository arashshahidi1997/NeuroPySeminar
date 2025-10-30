from pathlib import Path
datadir = Path("/storage2/arash/teaching/neuropy/data/ds-montgomery-v1")
filename = datadir / "ws_data_1shank.mat"

import scipy.io
data = scipy.io.loadmat(filename)
print(data.keys())