"""Run from repository root after pip install -e .[optimization,dev]."""
import json
from pathlib import Path
from statistics import median
from logimind.algorithms import optimize

ROOT=Path(__file__).resolve().parents[2]

def main():
    rows=[]
    for path in sorted((ROOT/'data/samples').glob('*.json')):
        d=json.loads(path.read_text())
        for alg in ('BASELINE','MILP'):
            runs=[optimize(d,alg) for _ in range(3)]
            r=runs[-1]; s=r['summary']; assert r['status']!='ERROR',r
            rows.append(dict(dataset=path.name,algorithm=alg,status=r['status'],cost=s['shipping_cost'],assigned=s['assigned_orders'],unassigned=s['total_orders']-s['assigned_orders'],runtime_seconds=median(x['summary']['solve_time_seconds'] for x in runs),mip_gap=r['diagnostics'].get('mip_gap')))
    out=Path(__file__).parent
    (out/'benchmark_results.json').write_text(json.dumps(rows,indent=2,allow_nan=False)+'\n')
    lines=['# Benchmark TV2 – Policy A','', '3 lần chạy mỗi thuật toán, trung vị thời gian (giây); SciPy/HiGHS, giới hạn 30 giây. Không có nghiệm đầy đủ: chi phí null, số đơn công bố bằng 0; không tính gán tạm. Gap là tỷ lệ của HiGHS.','', '| Dataset | Algorithm | Status | Cost | Assigned | Unassigned | Seconds | Gap |','|---|---|---|---:|---:|---:|---:|---:|']
    for r in rows: lines.append('| '+' | '.join(str(r[k]) for k in ('dataset','algorithm','status','cost','assigned','unassigned','runtime_seconds','mip_gap'))+' |')
    lines+=['','sample_medium: MILP giảm chi phí so với Baseline; sample_large: Baseline không tìm được nghiệm đầy đủ, không tính % giảm. Không so sánh chi phí khi thiếu nghiệm.']
    (out/'benchmark.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
if __name__=='__main__': main()
