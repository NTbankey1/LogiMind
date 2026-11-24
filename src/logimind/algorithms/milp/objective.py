import numpy as np


def objective(pairs):
    return np.array([o['shipping_costs'][w['warehouse_id']] for o,w in pairs], dtype=float)
