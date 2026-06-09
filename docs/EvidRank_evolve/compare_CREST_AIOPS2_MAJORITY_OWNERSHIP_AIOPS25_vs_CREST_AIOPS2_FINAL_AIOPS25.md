# EvidenceRank Compare CREST_AIOPS2_MAJORITY_OWNERSHIP_AIOPS25 vs CREST_AIOPS2_FINAL_AIOPS25

- Created: 2026-06-09T00:32:02+08:00
- Old: `CREST_AIOPS2_MAJORITY_OWNERSHIP_AIOPS25`
- New: `CREST_AIOPS2_FINAL_AIOPS25`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.421739 | 0.465217 | 0.043478 |
| AC@3 | 0.660870 | 0.695652 | 0.034783 |
| AC@5 | 0.778261 | 0.786957 | 0.008696 |
| MRR | 0.586693 | 0.617852 | 0.031159 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 12 |
| regressed_from_hit1 | 2 |
| unchanged | 216 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| aiops2025-2cce5582-215-jvm-cpu | improved_to_hit1 | 2 | 1 | 1.0 | adservice | adservice|frontend|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-6637fe70-563-cpu-stress | improved_to_hit1 | 2 | 1 | 1.0 | currencyservice | currencyservice|frontend|checkoutservice|cartservice|recommendationservice | stress | 6637fe70-563-cpu |
| aiops2025-abb62970-110-jvm-cpu | improved_to_hit1 | 2 | 1 | 1.0 | adservice | adservice|frontend|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-df892932-168-jvm-cpu | improved_to_hit1 | 2 | 1 | 1.0 | adservice | adservice|frontend|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-0410d710-226-pod-kill | improved_to_hit1 | 4 | 1 | 3.0 | paymentservice | paymentservice|redis-cart|frontend|cartservice|shippingservice | unknown | unknown |
| aiops2025-233e0282-88-cpu-stress | improved_to_hit1 | 4 | 1 | 3.0 | currencyservice | currencyservice|frontend|cartservice|checkoutservice|recommendationservice | stress | 233e0282-88-cpu |
| aiops2025-5d022708-414-target-port-misconfig | improved_to_hit1 | 4 | 1 | 3.0 | shippingservice | shippingservice|checkoutservice|frontend|cartservice|recommendationservice | unknown | unknown |
| aiops2025-8c1e8ce9-237-jvm-cpu | improved_to_hit1 | 4 | 1 | 3.0 | adservice | adservice|frontend|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-cb5815ce-161-jvm-cpu | improved_to_hit1 | 4 | 1 | 3.0 | adservice | adservice|frontend|checkoutservice|redis-cart|cartservice | unknown | unknown |
| aiops2025-de4a919c-126-memory-stress | improved_to_hit1 | 4 | 1 | 3.0 | paymentservice | paymentservice|frontend|redis-cart|cartservice|checkoutservice | stress | de4a919c-126-memory |
| aiops2025-13ebf32d-216-jvm-cpu | improved_to_hit1 | 6 | 1 | 5.0 | adservice | adservice|frontend|redis-cart|cartservice|recommendationservice | unknown | unknown |
| aiops2025-ff15d32c-199-jvm-gc | improved_to_hit1 | 6 | 1 | 5.0 | adservice | adservice|frontend|checkoutservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-7e54232b-275-cpu-stress | regressed_from_hit1 | 1 | 2 | -1.0 | checkoutservice | adservice|checkoutservice|frontend|redis-cart|cartservice | stress | 7e54232b-275-cpu |
| aiops2025-c3f4fde9-330-network-delay | regressed_from_hit1 | 1 | 2 | -1.0 | checkoutservice;emailservice | adservice|checkoutservice|frontend|cartservice|emailservice | delay | c3f4fde9-330-network |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
