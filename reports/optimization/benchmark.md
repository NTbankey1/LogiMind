# Benchmark TV2 – Policy A

3 lần chạy mỗi thuật toán, trung vị thời gian (giây); SciPy/HiGHS, giới hạn 30 giây. Không có nghiệm đầy đủ: chi phí null, số đơn công bố bằng 0; không tính gán tạm. Gap là tỷ lệ của HiGHS.

| Dataset | Algorithm | Status | Cost | Assigned | Unassigned | Seconds | Gap |
|---|---|---|---:|---:|---:|---:|---:|
| edge_equal_costs.json | BASELINE | FEASIBLE | 12.0 | 2 | 0 | 4.129999433644116e-05 | None |
| edge_equal_costs.json | MILP | OPTIMAL | 12.0 | 2 | 0 | 0.0037687000003643334 | 0.0 |
| edge_infeasible_stock.json | BASELINE | NO_SOLUTION_FOUND | None | 0 | 1 | 1.9700004486367106e-05 | None |
| edge_infeasible_stock.json | MILP | INFEASIBLE | None | 0 | 1 | 1.960000372491777e-05 | None |
| edge_tight_capacity.json | BASELINE | FEASIBLE | 16.0 | 3 | 0 | 2.9199989512562752e-05 | None |
| edge_tight_capacity.json | MILP | OPTIMAL | 16.0 | 3 | 0 | 0.003498400008538738 | 0.0 |
| edge_tight_inventory.json | BASELINE | FEASIBLE | 9.0 | 2 | 0 | 3.359999391250312e-05 | None |
| edge_tight_inventory.json | MILP | OPTIMAL | 9.0 | 2 | 0 | 0.003429099975619465 | 0.0 |
| edge_unavailable_route.json | BASELINE | FEASIBLE | 10.5 | 2 | 0 | 3.0099996365606785e-05 | None |
| edge_unavailable_route.json | MILP | OPTIMAL | 10.5 | 2 | 0 | 0.0017558000108692795 | 0.0 |
| edge_zero_stock.json | BASELINE | FEASIBLE | 11.0 | 2 | 0 | 1.6900012269616127e-05 | None |
| edge_zero_stock.json | MILP | OPTIMAL | 11.0 | 2 | 0 | 0.0015866999747231603 | 0.0 |
| sample_infeasible.json | BASELINE | NO_SOLUTION_FOUND | None | 0 | 3 | 2.6699999580159783e-05 | None |
| sample_infeasible.json | MILP | INFEASIBLE | None | 0 | 3 | 0.0013786999916192144 | None |
| sample_large.json | BASELINE | NO_SOLUTION_FOUND | None | 0 | 60 | 0.0006003000016789883 | None |
| sample_large.json | MILP | OPTIMAL | 406.02 | 60 | 0 | 0.08098449997487478 | 0.0 |
| sample_medium.json | BASELINE | FEASIBLE | 192.82 | 20 | 0 | 0.00014980000560171902 | None |
| sample_medium.json | MILP | OPTIMAL | 172.14000000000001 | 20 | 0 | 0.014485799998510629 | 0.0 |
| sample_small.json | BASELINE | FEASIBLE | 12.0 | 3 | 0 | 1.930000144056976e-05 | None |
| sample_small.json | MILP | OPTIMAL | 12.0 | 3 | 0 | 0.0016106000111903995 | 0.0 |

sample_medium: MILP giảm chi phí so với Baseline; sample_large: Baseline không tìm được nghiệm đầy đủ, không tính % giảm. Không so sánh chi phí khi thiếu nghiệm.
