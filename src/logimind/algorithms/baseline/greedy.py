from time import perf_counter
from .allocator import eligible
from ..result import result


def solve(dataset):
    start = perf_counter()
    warehouses = {w['warehouse_id']: w for w in dataset['warehouses']}
    stock = {j: dict(w['inventory']) for j,w in warehouses.items()}
    capacity = {j: w['capacity_orders'] for j,w in warehouses.items()}
    assignments = {}
    for o in sorted(dataset['orders'], key=lambda o: o['order_id']):
        options = [j for j,w in warehouses.items() if eligible(o,w) and capacity[j] > 0
                   and all(stock[j][k] >= q for k,q in o['items'].items())]
        if not options:
            return result(dataset,'BASELINE','NO_SOLUTION_FOUND','BASELINE_FAILED',perf_counter()-start,
                          failed_order_id=o['order_id'], temporary_assignments=assignments)
        j = min(options,key=lambda j:(o['shipping_costs'][j],j))
        assignments[o['order_id']] = j
        capacity[j] -= 1
        for k,q in o['items'].items(): stock[j][k] -= q
    return result(dataset,'BASELINE','FEASIBLE','HEURISTIC_COMPLETE',perf_counter()-start,assignments)
