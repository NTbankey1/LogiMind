from src.algorithms import optimize

def test_optimal_manual_example(sample):
    r=optimize(sample,'milp')
    assert r['status']=='OPTIMAL' and r['shipping_cost']==21
    assert r['assignments']=={'A':'K2','B':'K1'}
    assert r['mip_gap'] is not None and r['mip_gap'] < 1e-6

def test_infeasible_a(sample):
    sample['warehouses'][0]['capacity']=0
    sample['warehouses'][1]['capacity']=1
    assert optimize(sample,'milp')['status']=='INFEASIBLE'

