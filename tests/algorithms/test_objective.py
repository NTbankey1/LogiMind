from logimind.algorithms import optimize

def test_cost(small):
    for alg in ('BASELINE','MILP'):
        r=optimize(small,alg); assert r['summary']['shipping_cost']==r['summary']['objective_value']==12
