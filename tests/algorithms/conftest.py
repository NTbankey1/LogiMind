import json
from pathlib import Path
import pytest

@pytest.fixture
def small():
    return json.loads((Path(__file__).resolve().parents[2]/'data/samples/sample_small.json').read_text())

@pytest.fixture
def tv1(small):
    small.update(dataset_id='tv1-example',skus=[dict(sku_id=k,name=k) for k in 'XY'],warehouses=[dict(warehouse_id='K1',name='K1',capacity_orders=2,inventory={'X':3,'Y':3}),dict(warehouse_id='K2',name='K2',capacity_orders=1,inventory={'X':4,'Y':2})],orders=[dict(order_id=i,items=q,shipping_costs={'K1':a,'K2':b}) for i,q,a,b in [('A',{'X':2,'Y':1},10,14),('B',{'X':1,'Y':2},11,12),('C',{'X':2},9,25)]])
    return small
