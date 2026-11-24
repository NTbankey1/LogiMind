from logimind.algorithms import optimize

def test_tv1(tv1):
    r=optimize(tv1,'BASELINE'); assert r['status']=='FEASIBLE'; assert r['summary']['shipping_cost']==46

def test_failure_not_proof(tv1):
    tv1['orders']= [dict(order_id='A',items={'X':1},shipping_costs={'K1':1,'K2':2}),dict(order_id='B',items={'Y':1},shipping_costs={'K1':1,'K2':3})]
    tv1['warehouses'][0].update(capacity_orders=1,inventory={'X':1,'Y':1}); tv1['warehouses'][1].update(capacity_orders=1,inventory={'X':1,'Y':0})
    r=optimize(tv1,'BASELINE'); assert r['status']=='NO_SOLUTION_FOUND'; assert r['allocations']==[]; assert r['summary']['shipping_cost'] is None
    assert optimize(tv1)['summary']['shipping_cost']==3
