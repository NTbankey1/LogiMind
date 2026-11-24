from math import fsum, isfinite


def verify(dataset, assignments):
    orders = {o['order_id']: o for o in dataset['orders']}
    warehouses = {w['warehouse_id']: w for w in dataset['warehouses']}
    if set(assignments) != set(orders):
        raise ValueError('Incomplete or unknown orders')
    stock = {j: dict(w['inventory']) for j, w in warehouses.items()}
    used = dict.fromkeys(warehouses, 0)
    allocations = []
    for i, j in sorted(assignments.items()):
        o = orders[i]
        if j not in warehouses or j not in o['shipping_costs']:
            raise ValueError('Forbidden route')
        used[j] += 1
        if used[j] > warehouses[j]['capacity_orders']:
            raise ValueError('Capacity exceeded')
        for k, q in o['items'].items():
            stock[j][k] -= q
            if stock[j][k] < 0:
                raise ValueError('Inventory exceeded')
        allocations.append(dict(order_id=i, warehouse_id=j, shipping_cost=o['shipping_costs'][j]))
    utilization = [dict(warehouse_id=j, used_capacity_orders=used[j],
                        capacity_orders=w['capacity_orders'],
                        utilization_pct=100*used[j]/w['capacity_orders'] if w['capacity_orders'] else None)
                   for j,w in sorted(warehouses.items())]
    return allocations, fsum(a['shipping_cost'] for a in allocations), utilization, stock


def result(dataset, algorithm, status, reason, runtime, assignments=None, **diagnostics):
    allocations, cost, utilization, stock = [], None, [], None
    if status in ('OPTIMAL', 'FEASIBLE'):
        allocations, cost, utilization, stock = verify(dataset, assignments)
    return dict(dataset_id=dataset.get('dataset_id') if isinstance(dataset, dict) else None,
                policy='A', algorithm=algorithm, status=status, termination_reason=reason,
                summary=dict(total_orders=len(dataset['orders']) if isinstance(dataset, dict) and isinstance(dataset.get('orders'), list) else None,
                             assigned_orders=len(allocations), shipping_cost=cost,
                             objective_value=cost, solve_time_seconds=runtime),
                allocations=allocations, warehouse_utilization=utilization,
                diagnostics=dict(remaining_stock=stock, **diagnostics))
