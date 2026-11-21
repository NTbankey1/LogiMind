"""Linear constraints: assignment, per-SKU inventory, warehouse capacity."""
import numpy as np
from scipy.optimize import LinearConstraint

def build_constraints(data, pairs, unassigned):
    n = len(pairs) + len(unassigned)
    rows, lower, upper = [], [], []
    for order in data['orders']:
        oid = order['id']; row = np.zeros(n)
        for k,(i,j) in enumerate(pairs):
            if i == oid: row[k] = 1
        if oid in unassigned: row[len(pairs)+unassigned.index(oid)] = 1
        rows.append(row); lower.append(1); upper.append(1)
    orders = {o['id']:o for o in data['orders']}
    for warehouse in data['warehouses']:
        wid = warehouse['id']
        for sku in sorted({sku for o in data['orders'] for sku in o['items']}):
            row = np.zeros(n)
            for k,(oid,j) in enumerate(pairs):
                if j == wid: row[k] = orders[oid]['items'].get(sku,0)
            rows.append(row); lower.append(-np.inf); upper.append(warehouse['inventory'].get(sku,0))
        row = np.zeros(n)
        for k,(oid,j) in enumerate(pairs):
            if j == wid: row[k] = orders[oid]['load']
        rows.append(row); lower.append(-np.inf); upper.append(warehouse['capacity'])
    return LinearConstraint(np.array(rows).reshape((-1,n)), lower, upper)
