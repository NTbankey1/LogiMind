"""Deterministic cheapest-feasible-warehouse greedy baseline."""
from time import perf_counter
from .allocator import fits, evaluate

def solve(data):
    start = perf_counter()
    remaining = {w['id']: dict(w['inventory']) for w in data['warehouses']}
    capacity = {w['id']: w['capacity'] for w in data['warehouses']}
    assignments = {}
    for o in sorted(data['orders'], key=lambda x: x['id']):
        oid = o['id']
        candidates = sorted((float(data['costs'][oid][w['id']]), w['id'])
                            for w in data['warehouses']
                            if w['id'] in data['costs'].get(oid, {})
                            and fits(o, w, remaining[w['id']], capacity[w['id']]))
        if not candidates:
            continue
        cost, wid = candidates[0]
        assignments[oid] = wid
        capacity[wid] -= o['load']
        for sku,qty in o['items'].items():
            remaining[wid][sku] = remaining[wid].get(sku, 0) - qty
    status = 'FEASIBLE' if len(assignments) == len(data['orders']) else 'INFEASIBLE'
    return evaluate(data, assignments, 'baseline', status, perf_counter()-start,
                    message='Greedy is not a proof of global feasibility or optimality')
