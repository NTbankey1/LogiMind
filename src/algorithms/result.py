"""Input validation and common result contract for TV5."""
from dataclasses import dataclass, field, asdict
from math import isfinite

STATUSES = ('OPTIMAL', 'FEASIBLE', 'INFEASIBLE', 'ERROR')

@dataclass
class Result:
    algorithm: str
    status: str
    assignments: dict = field(default_factory=dict)
    unallocated: dict = field(default_factory=dict)
    shipping_cost: float = 0.0
    penalty_cost: float = 0.0
    total_cost: float = 0.0
    runtime_seconds: float = 0.0
    mip_gap: float | None = None
    warehouse_usage: dict = field(default_factory=dict)
    message: str = ''

    @property
    def allocated_count(self):
        return len(self.assignments)

    @property
    def unallocated_count(self):
        return len(self.unallocated)

    def to_dict(self):
        return {**asdict(self), 'allocated_count': self.allocated_count,
                'unallocated_count': self.unallocated_count}


def _number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    if value < 0 or (positive and value <= 0):
        raise ValueError(f'{name} must be {"positive" if positive else "nonnegative"}')
    return float(value)


def normalize(data):
    """Canonical input: orders[{id,items:{sku:qty},load?}], warehouses[{id,capacity,inventory:{sku:qty}}], costs[order_id][warehouse_id]."""
    if not isinstance(data, dict):
        raise ValueError('Input must be an object')
    orders, warehouses = data.get('orders'), data.get('warehouses')
    costs = data.get('costs')
    if not isinstance(orders, list) or not isinstance(warehouses, list) or not isinstance(costs, dict):
        raise ValueError('orders, warehouses and costs are required')
    if not warehouses:
        raise ValueError('At least one warehouse is required')
    def unique(rows, label):
        ids = [r.get('id') if isinstance(r, dict) else None for r in rows]
        if any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
            raise ValueError(f'{label}: missing or duplicate id')
    unique(orders, 'orders'); unique(warehouses, 'warehouses')
    norm_orders = []
    for o in orders:
        items = o.get('items')
        if not isinstance(items, dict) or not items:
            raise ValueError(f'order {o["id"]}: nonempty items required')
        if any(not isinstance(k, str) or not k for k in items):
            raise ValueError('Invalid sku')
        norm_orders.append({'id': o['id'], 'items': {k: _number(v, 'quantity', True) for k,v in items.items()},
                            'load': _number(o.get('load', 1), 'load', True)})
    norm_warehouses = []
    for w in warehouses:
        inv = w.get('inventory')
        if not isinstance(inv, dict):
            raise ValueError('warehouse inventory required')
        norm_warehouses.append({'id': w['id'], 'capacity': _number(w.get('capacity'), 'capacity'),
                                'inventory': {k: _number(v, 'inventory') for k,v in inv.items()}})
    for oid, row in costs.items():
        if oid not in {o['id'] for o in norm_orders} or not isinstance(row, dict):
            raise ValueError('Unknown order in costs or invalid cost row')
        for wid, value in row.items():
            if wid not in {w['id'] for w in norm_warehouses}:
                raise ValueError('Unknown warehouse in costs')
            _number(value, 'cost')
    policy = data.get('policy', 'A')
    if policy != 'A':
        raise ValueError('TV1 model supports policy A only (all orders assigned)')
    if data.get('penalties'):
        raise ValueError('Penalty terms are not part of the approved policy A model')
    return {'orders': norm_orders, 'warehouses': norm_warehouses,
            'costs': costs, 'policy': 'A', 'penalties': {}}
