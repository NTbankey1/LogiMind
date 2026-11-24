def eligible(order, warehouse):
    return (warehouse['warehouse_id'] in order['shipping_costs']
            and warehouse['capacity_orders'] > 0
            and all(warehouse['inventory'][k] >= q for k, q in order['items'].items()))


def candidates(dataset):
    return [(o, w) for o in sorted(dataset['orders'], key=lambda o: o['order_id'])
            for w in sorted(dataset['warehouses'], key=lambda w: w['warehouse_id'])
            if eligible(o, w)]
