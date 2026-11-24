from time import perf_counter
from math import isfinite
import numpy as np
from scipy.optimize import milp
from .model import build
from ..result import result


def solve(dataset,time_limit):
    start=perf_counter()
    pairs, model=build(dataset)
    def finish(status,reason,assignments=None,**details):
        return result(dataset,'MILP',status,reason,perf_counter()-start,assignments,**details)
    if model is None:
        return finish('INFEASIBLE','NO_ELIGIBLE_WAREHOUSE')
    r=milp(**model,options={'time_limit':time_limit,'mip_rel_gap':0.0})
    details={'solver_message':str(r.message)}
    for field,key in [('mip_gap','mip_gap'),('mip_dual_bound','best_bound')]:
        value=getattr(r,field,None)
        details[key]=float(value) if value is not None and isfinite(value) else None
    if r.status==2: return finish('INFEASIBLE','INFEASIBILITY_PROVEN',**details)
    if r.status not in (0,1): return finish('ERROR','SOLVER_ERROR',**details)
    if r.x is None:
        return finish('NO_SOLUTION_FOUND' if r.status==1 else 'ERROR','TIME_LIMIT' if r.status==1 else 'INVALID_SOLUTION',**details)
    if not np.all(np.isfinite(r.x)) or not np.all(np.abs(r.x-np.rint(r.x))<=1e-6) or np.any(r.x < -1e-6) or np.any(r.x > 1+1e-6):
        return finish('ERROR','INVALID_SOLUTION',**details)
    assignments={}
    for (o,w),x in zip(pairs,r.x):
        if x>0.5:
            i=o['order_id']
            if i in assignments: return finish('ERROR','INVALID_SOLUTION',**details)
            assignments[i]=w['warehouse_id']
    return finish('OPTIMAL' if r.status==0 else 'FEASIBLE','OPTIMALITY_PROVEN' if r.status==0 else 'TIME_LIMIT',assignments,**details)
