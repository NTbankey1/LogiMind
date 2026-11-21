"""Create the SciPy/HiGHS MILP model."""
import numpy as np
from scipy.optimize import Bounds
from .constraints import build_constraints
from .objective import build_objective

def build_model(data):
    pairs = [(o['id'],w['id']) for o in data['orders'] for w in data['warehouses']
             if w['id'] in data['costs'].get(o['id'], {})
             and o['load'] <= w['capacity']
             and all(w['inventory'].get(sku,0) >= qty for sku,qty in o['items'].items())]
    unassigned = []
    n = len(pairs)+len(unassigned)
    return {'c': build_objective(data,pairs,unassigned), 'integrality': np.ones(n, dtype=int),
            'bounds': Bounds(np.zeros(n),np.ones(n)),
            'constraints': build_constraints(data,pairs,unassigned),
            'pairs': pairs, 'unassigned': unassigned}
