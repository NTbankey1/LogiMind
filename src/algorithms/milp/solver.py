"""Solve and safely classify HiGHS results."""
from time import perf_counter
from scipy.optimize import milp
from .model import build_model
from ..baseline.allocator import evaluate
from ..result import Result

def solve(data, time_limit=30.0):
    start = perf_counter()
    if not isinstance(time_limit, (int,float)) or isinstance(time_limit,bool) or not __import__('math').isfinite(time_limit) or time_limit <= 0:
        raise ValueError('time_limit must be positive')
    if not data['orders']:
        return evaluate(data, {}, 'milp', 'OPTIMAL', perf_counter()-start, 0.0)
    model = build_model(data)
    if not len(model['c']):
        return Result('milp','INFEASIBLE', runtime_seconds=perf_counter()-start,
                      message='No possible decision variables')
    try:
        sol = milp(c=model['c'], integrality=model['integrality'], bounds=model['bounds'],
                   constraints=model['constraints'], options={'time_limit':float(time_limit)})
        elapsed = perf_counter()-start
        if sol.status == 2:
            return Result('milp','INFEASIBLE',runtime_seconds=elapsed,message=str(sol.message))
        if sol.x is None or sol.status not in (0,1):
            return Result('milp','ERROR',runtime_seconds=elapsed,message=str(sol.message))
        assignments = {oid:wid for k,(oid,wid) in enumerate(model['pairs']) if sol.x[k] > .5}
        status = 'OPTIMAL' if sol.status == 0 else 'FEASIBLE'
        gap = getattr(sol,'mip_gap',None)
        gap = float(gap) if gap is not None else None
        return evaluate(data,assignments,'milp',status,elapsed,gap,str(sol.message))
    except Exception as exc:
        return Result('milp','ERROR',runtime_seconds=perf_counter()-start,message=str(exc))
