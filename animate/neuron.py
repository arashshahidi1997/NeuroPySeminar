import LFPy
import numpy as np

cell_params = {
    'morphology': None,
    'length': 200,
    'diam': 2,
    'Ra': 150,
    'cm': 1.0,
    'passive': True,
    'e_pas': -65,
    'v_init': -65,
    'Ra': 150,
}

cell = LFPy.Cell(**cell_params)
synapse = LFPy.Synapse(cell,
    idx=cell.get_closest_idx(x=150),
    syntype='ExpSyn',
    weight=0.001,
    tau=2.0,
    e=0.0)
synapse.set_spike_times(np.array([1.0]))  # 1 ms

cell.simulate(rec_imem=True)
