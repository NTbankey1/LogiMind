"""Single public API for TV5."""
from .result import normalize, Result
from .baseline.greedy import solve as greedy
from .milp.solver import solve as milp_solve

def optimize(data, algorithm='milp', time_limit=30.0):
    if algorithm not in ('baseline','milp'):
        return Result(algorithm,'ERROR',message='Unknown algorithm').to_dict()
    try:
        normalized = normalize(data)
        result = greedy(normalized) if algorithm == 'baseline' else milp_solve(normalized,time_limit)
        return result.to_dict()
    except (ValueError, TypeError, KeyError) as exc:
        return Result(algorithm,'ERROR',message=str(exc)).to_dict()
