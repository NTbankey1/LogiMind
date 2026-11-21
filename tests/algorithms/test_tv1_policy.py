from src.algorithms import optimize

def test_no_split_and_full_assignment(sample):
    result=optimize(sample,'milp')
    assert result['status']=='OPTIMAL'
    assert set(result['assignments'])=={'A','B'}

def test_greedy_failure_is_not_milp_infeasibility(sample):
    sample['orders']=[{'id':'A','items':{'sku':1}},{'id':'B','items':{'sku':1}}]
    sample['warehouses']=[{'id':'K1','capacity':1,'inventory':{'sku':1}}, {'id':'K2','capacity':1,'inventory':{'sku':1}}]
    sample['costs']={'A':{'K1':1,'K2':2},'B':{'K1':1}}
    assert optimize(sample,'baseline')['status']=='INFEASIBLE'
    assert optimize(sample,'milp')['status']=='OPTIMAL'

def test_no_warehouse_can_cover_order(sample):
    sample['orders'][0]['items']={'sku':99}
    assert optimize(sample,'milp')['status']=='INFEASIBLE'
