"""Shared feasibility and result verification."""
from ..result import Result

TOL = 1e-7

def fits(order, warehouse, inventory, remaining_capacity):
    return (order['load'] <= remaining_capacity + TOL and
            all(inventory.get(sku, 0) + TOL >= qty for sku,qty in order['items'].items()))

def evaluate(data, assignments, algorithm, status, elapsed=0, mip_gap=None, message=''):
    orders = {o['id']: o for o in data['orders']}
    warehouses = {w['id']: w for w in data['warehouses']}
    remaining = {w: dict(v['inventory']) for w,v in warehouses.items()}
    capacity = {w: v['capacity'] for w,v in warehouses.items()}
    if set(assignments) - set(orders):
        raise ValueError('Unknown assigned order')
    shipping = 0.0
    for oid,wid in assignments.items():
        if wid not in warehouses or wid not in data['costs'].get(oid, {}):
            raise ValueError('Unknown warehouse or missing cost')
        order = orders[oid]
        if not fits(order, warehouses[wid], remaining[wid], capacity[wid]):
            raise ValueError('Allocation violates inventory or capacity')
        shipping += float(data['costs'][oid][wid]); capacity[wid] -= order['load']
        for sku,qty in order['items'].items():
            remaining[wid][sku] = remaining[wid].get(sku, 0) - qty
    missing = [oid for oid in orders if oid not in assignments]
    if data['policy'] == 'A' and missing and status in ('OPTIMAL','FEASIBLE'):
        raise ValueError('Policy A requires every order allocated')
    penalty = 0.0
    reasons = {}
    for oid in missing:
        o = orders[oid]
        eligible = [w for w in warehouses.values() if w['id'] in data['costs'].get(oid, {})]
        reasons[oid] = ('NO_COST_OPTION' if not eligible else
                        'INSUFFICIENT_RESOURCES' if not any(fits(o,w,remaining[w['id']],capacity[w['id']]) for w in eligible)
                        else 'NOT_SELECTED_BY_OPTIMIZER')
    usage = {wid: {'used': warehouses[wid]['capacity']-capacity[wid],
                   'capacity': warehouses[wid]['capacity'],
                   'utilization_percent': (100*(warehouses[wid]['capacity']-capacity[wid])/warehouses[wid]['capacity']
                                           if warehouses[wid]['capacity'] else 0.0)} for wid in warehouses}
    return Result(algorithm, status, dict(assignments), reasons, shipping, penalty,
                  shipping+penalty, elapsed, mip_gap, usage, message)
