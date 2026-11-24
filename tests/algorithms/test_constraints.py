import pytest
from logimind.algorithms.result import verify
from logimind.algorithms import optimize

def test_capacity(tv1):
    with pytest.raises(ValueError): verify(tv1,{'A':'K1','B':'K1','C':'K1'})
    tv1['warehouses'][1]['capacity_orders']=0
    assert optimize(tv1)['status']=='INFEASIBLE'

def test_stock(tv1):
    with pytest.raises(ValueError): verify(tv1,{'A':'K1','B':'K2','C':'K1'})

def test_missing(small):
    with pytest.raises(ValueError): verify(small,{})
