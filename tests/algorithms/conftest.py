import pytest
@pytest.fixture
def sample():
    return {'orders':[{'id':'A','items':{'sku':1}},{'id':'B','items':{'sku':1}}],
            'warehouses':[{'id':'K1','capacity':1,'inventory':{'sku':1}},
                          {'id':'K2','capacity':2,'inventory':{'sku':2}}],
            'costs':{'A':{'K1':10,'K2':11},'B':{'K1':10,'K2':30}},
            'policy':'A'}
