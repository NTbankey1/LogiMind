"""Reproducible local benchmark; writes only measured results."""
import json
from pathlib import Path
from src.algorithms import optimize

def run():
    data=json.loads(Path('docs/example-input.json').read_text(encoding='utf-8'))
    results={algorithm:optimize(data,algorithm) for algorithm in ('baseline','milp')}
    output={'dataset':'docs/example-input.json','runs':results,
            'note':'Measured locally; replace with TV2 datasets after integration'}
    Path('reports/optimization/benchmark_results.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    return output

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
