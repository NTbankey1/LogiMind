from src.algorithms import optimize
from src.algorithms.milp.objective import build_objective
from src.algorithms.result import normalize

def test_cost_components(sample):
    r=optimize(sample,'milp')
    assert r['total_cost']==r['shipping_cost']==21
    assert r['penalty_cost']==0

def test_objective_coefficients(sample):
    data=normalize(sample)
    assert list(build_objective(data,[('A','K1'),('B','K2')]))==[10,30]
