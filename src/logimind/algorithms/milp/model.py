import numpy as np
from scipy.optimize import Bounds
from ..baseline.allocator import candidates
from .constraints import constraints
from .objective import objective


def build(dataset):
    pairs = candidates(dataset)
    if {o['order_id'] for o,w in pairs} != {o['order_id'] for o in dataset['orders']}:
        return pairs, None
    n = len(pairs)
    return pairs, dict(c=objective(pairs), integrality=np.ones(n), bounds=Bounds(0,1),
                       constraints=constraints(dataset,pairs))
