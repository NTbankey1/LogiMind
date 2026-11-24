import copy
import pytest
from logimind.algorithms import optimize
from types import SimpleNamespace
import importlib

@pytest.mark.parametrize('field',['order_id','items','shipping_costs'])
def test_invalid(small,field):
    del small['orders'][0][field]; assert optimize(small)['status']=='ERROR'

def test_no_mutation(small):
    original=copy.deepcopy(small); optimize(small,'BASELINE'); optimize(small); assert small==original

def test_timeout(small,monkeypatch):
    solver=importlib.import_module('logimind.algorithms.milp.solver')
    monkeypatch.setattr(solver,'milp',lambda **kw: SimpleNamespace(status=1,x=None,message='Time limit'))
    assert optimize(small)['status']=='NO_SOLUTION_FOUND'

def test_tie(small):
    for o in small['orders']: o['shipping_costs']={j:1 for j in o['shipping_costs']}
    assert optimize(small,'BASELINE')['allocations'][0]['warehouse_id']=='WH-01'
