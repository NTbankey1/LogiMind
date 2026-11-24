from time import perf_counter
from math import isfinite
from pathlib import Path
import importlib.util
from .result import result
from .baseline.greedy import solve as greedy
from .milp.solver import solve as milp_solve


def optimize(dataset, algorithm='MILP', time_limit=30.0, *, time_limit_seconds=None):
    """Accept TV2 canonical dataset directly; return TV5 API result payload."""
    start=perf_counter()
    algorithm=str(algorithm).upper()
    try:
        if algorithm not in ('BASELINE','MILP'): raise ValueError('Unknown algorithm')
        limit=time_limit if time_limit_seconds is None else time_limit_seconds
        if isinstance(limit,bool) or not isinstance(limit,(int,float)) or not isfinite(limit) or limit<=0:
            raise ValueError('Invalid time limit')
        # Reuse TV2 validator unchanged, from the repository checkout.
        root=Path(__file__).resolve().parents[3]
        spec=importlib.util.spec_from_file_location('tv2_validator',root/'scripts/validate_dataset.py')
        validator=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        valid, errors=validator.validate_dataset_data(dataset)
        if not valid:
            return result(dataset,algorithm,'ERROR','VALIDATION_ERROR',perf_counter()-start,errors=errors)
        return greedy(dataset) if algorithm=='BASELINE' else milp_solve(dataset,limit)
    except Exception as exc:
        return result(dataset,algorithm,'ERROR','EXECUTION_ERROR',perf_counter()-start,message=str(exc))
