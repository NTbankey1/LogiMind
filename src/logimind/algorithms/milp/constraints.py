import numpy as np
from scipy.optimize import LinearConstraint
from scipy.sparse import lil_matrix


def constraints(dataset, pairs):
    orders, warehouses, skus = dataset['orders'], dataset['warehouses'], dataset['skus']
    rows = []
    for o in orders: rows.append(('order',o['order_id'],None,1,1))
    for w in warehouses:
        j = w['warehouse_id']
        rows.append(('capacity',j,None,0,w['capacity_orders']))
        for k in skus:
            s = k['sku_id']
            rows.append(('stock',j,s,0,w['inventory'][s]))
    matrix = lil_matrix((len(rows),len(pairs)),dtype=float)
    for r,(kind,key,sku,lo,hi) in enumerate(rows):
        for c,(o,w) in enumerate(pairs):
            if kind == 'order': matrix[r,c] = int(o['order_id']==key)
            elif w['warehouse_id']==key: matrix[r,c] = 1 if kind=='capacity' else o['items'].get(sku,0)
    return LinearConstraint(matrix.tocsr(),np.array([r[3] for r in rows]),np.array([r[4] for r in rows]))
