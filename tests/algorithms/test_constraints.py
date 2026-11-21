import pytest
from src.algorithms.baseline.allocator import evaluate
from src.algorithms.result import normalize

def test_inventory_and_capacity(sample):
    d=normalize(sample)
    with pytest.raises(ValueError): evaluate(d,{'A':'K1','B':'K1'},'test','FEASIBLE')

def test_multi_sku(sample):
    sample['orders'][0]['items']={'sku':1,'other':2}
    from src.algorithms import optimize
    assert optimize(sample,'milp')['status']=='INFEASIBLE'
