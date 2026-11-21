from src.algorithms import optimize

def test_greedy_example(sample):
    r=optimize(sample,'baseline')
    assert r['assignments']=={'A':'K1','B':'K2'}
    assert r['shipping_cost']==40 and r['status']=='FEASIBLE'

def test_tie_break():
    d={'orders':[{'id':'a','items':{'s':1}}], 'warehouses':[
        {'id':'z','capacity':1,'inventory':{'s':1}}, {'id':'a','capacity':1,'inventory':{'s':1}}],
        'costs':{'a':{'z':5,'a':5}},'policy':'A'}
    assert optimize(d,'baseline')['assignments']=={'a':'a'}
