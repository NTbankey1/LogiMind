from src.algorithms import optimize

def test_bad_data(sample):
    sample['orders'][0]['items']['sku']=-1
    assert optimize(sample)['status']=='ERROR'

def test_reject_policy_b(sample):
    sample['policy']='B'
    assert optimize(sample)['status']=='ERROR'

def test_missing_cost_is_infeasible(sample):
    sample['costs']['A']={}
    assert optimize(sample,'milp')['status']=='INFEASIBLE'

def test_empty_orders(sample):
    sample['orders']=[];sample['costs']={}
    assert optimize(sample)['status']=='OPTIMAL'

def test_unknown_algorithm(sample):
    assert optimize(sample,'other')['status']=='ERROR'
