"""Import smoke test — keeps the pixi env honest.

If a week's library was removed from `pixi.toml` or fails to install on a
platform, the corresponding test will fail fast.
"""

import importlib

import pytest

WEEK_MODULES = {
    "W01_EMD": "emd",
    "W02_Multitaper": "scipy.signal",
    "W03_AR": "statsmodels.tsa.arima.model",
    "W04_PCA": "sklearn.decomposition",
    "W05_ICA": "sklearn.decomposition",
    "W06_UMAP": "umap",
    "W07_CCA": "sklearn.cross_decomposition",
    "W08_NNMF": "sklearn.decomposition",
    "W09_GPFA": "elephant.gpfa",
    "W10_SINDy": "pysindy",
    "W11_Network": "networkx",
}

CORE_MODULES = ["numpy", "scipy", "pandas", "matplotlib", "seaborn"]


@pytest.mark.parametrize("module", CORE_MODULES)
def test_core_imports(module):
    importlib.import_module(module)


@pytest.mark.parametrize("week,module", sorted(WEEK_MODULES.items()))
def test_week_imports(week, module):
    importlib.import_module(module)
