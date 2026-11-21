"""TV1 policy A: minimize total shipping cost, sum(c_ij * x_ij)."""
import numpy as np

def build_objective(data, pairs, unassigned=()):
    if unassigned:
        raise ValueError('Policy A has no unassigned decision variables')
    return np.array([float(data['costs'][oid][wid]) for oid, wid in pairs], dtype=float)
