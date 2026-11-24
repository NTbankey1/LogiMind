import json
from pathlib import Path
import pytest
from logimind.algorithms import optimize
from logimind.algorithms.result import verify
from itertools import product

@pytest.mark.parametrize('path',sorted((Path(__file__).resolve().parents[2]/'data/samples').glob('*.json')))
def test_tv2(path):
    d=json.loads(path.read_text()); r=optimize(d)
    if 'infeasible' in path.stem:
        assert r['status']=='INFEASIBLE'; assert r['summary']['shipping_cost'] is None; assert not r['allocations']
    else:
        assert r['status']=='OPTIMAL'; assert r['diagnostics']['mip_gap']==0
        a={x['order_id']:x['warehouse_id'] for x in r['allocations']}; assert verify(d,a)[1]==r['summary']['shipping_cost']
        if len(d['orders'])<=5:
            costs=[]
            for js in product([w['warehouse_id'] for w in d['warehouses']],repeat=len(d['orders'])):
                try: costs.append(verify(d,dict(zip([o['order_id'] for o in d['orders']],js)))[1])
                except ValueError: pass
            assert r['summary']['shipping_cost']==min(costs)

def test_tv1(tv1):
    r=optimize(tv1); assert r['status']=='OPTIMAL'; assert r['summary']['shipping_cost']==34
