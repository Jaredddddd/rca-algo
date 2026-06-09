# EvidenceRank Compare CREST_AIOPS2_BASE_AIOPS25 vs CREST_AIOPS2_CONTINUOUS_REJECTED_AIOPS25

- Created: 2026-06-08T21:29:24+08:00
- Old: `CREST_AIOPS2_BASE_AIOPS25`
- New: `CREST_AIOPS2_CONTINUOUS_REJECTED_AIOPS25`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.413043 | 0.365217 | -0.047826 |
| AC@3 | 0.678261 | 0.630435 | -0.047826 |
| AC@5 | 0.786957 | 0.700000 | -0.086957 |
| MRR | 0.580494 | 0.532949 | -0.047545 |

## Status Counts

| status | cases |
| --- | ---: |
| rank_improved | 6 |
| rank_regressed | 52 |
| regressed_from_hit1 | 11 |
| unchanged | 161 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| aiops2025-3d6c95dd-595-target-port-misconfig | rank_improved | 4 | 3 | 1.0 | shippingservice | frontend|checkoutservice|shippingservice|recommendationservice|cartservice | unknown | unknown |
| aiops2025-68bbf4fd-332-dns-error | rank_improved | 4 | 3 | 1.0 | checkoutservice | frontend|cartservice|checkoutservice|recommendationservice|redis-cart | unknown | unknown |
| aiops2025-ba74cb57-142-memory-stress | rank_improved | 5 | 4 | 1.0 | productcatalogservice | checkoutservice|frontend|cartservice|productcatalogservice|emailservice | stress | ba74cb57-142-memory |
| aiops2025-cd81a09b-101-pod-kill | rank_improved | 4 | 3 | 1.0 | recommendationservice | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-d44478e6-328-dns-error | rank_improved | 5 | 4 | 1.0 | checkoutservice | frontend|shippingservice|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-ae4abdbe-103-memory-stress | rank_improved | 5 | 3 | 2.0 | productcatalogservice | frontend|cartservice|productcatalogservice|recommendationservice|checkoutservice | stress | ae4abdbe-103-memory |
| aiops2025-9b0d8a50-187-jvm-exception | rank_regressed | 2 | 8 | -6.0 | adservice | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | exception | 9b0d8a50-187-jvm |
| aiops2025-f62b1785-258-pod-failure | rank_regressed | 2 | 8 | -6.0 | adservice | frontend|checkoutservice|cartservice|recommendationservice|redis-cart | pod-failure | f62b1785-258 |
| aiops2025-8c1e8ce9-237-jvm-cpu | rank_regressed | 2 | 7 | -5.0 | adservice | frontend|checkoutservice|cartservice|recommendationservice|productcatalogservice | unknown | unknown |
| aiops2025-91c4c773-252-jvm-cpu | rank_regressed | 4 | 9 | -5.0 | adservice | cartservice|frontend|redis-cart|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-3600f326-158-jvm-gc | rank_regressed | 6 | 10 | -4.0 | adservice | frontend|checkoutservice|recommendationservice|shippingservice|cartservice | unknown | unknown |
| aiops2025-3ae307d9-218-jvm-exception | rank_regressed | 2 | 6 | -4.0 | adservice | frontend|recommendationservice|checkoutservice|shippingservice|cartservice | exception | 3ae307d9-218-jvm |
| aiops2025-4664a5e8-251-jvm-exception | rank_regressed | 6 | 10 | -4.0 | adservice | frontend|checkoutservice|cartservice|recommendationservice|redis-cart | exception | 4664a5e8-251-jvm |
| aiops2025-4e221a94-277-memory-stress | rank_regressed | 5 | 9 | -4.0 | paymentservice | checkoutservice|redis-cart|cartservice|frontend|emailservice | stress | 4e221a94-277-memory |
| aiops2025-bc9db995-235-pod-kill | rank_regressed | 4 | 8 | -4.0 | adservice | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-eaf978d7-208-pod-kill | rank_regressed | 5 | 9 | -4.0 | currencyservice | frontend|checkoutservice|redis-cart|cartservice|recommendationservice | unknown | unknown |
| aiops2025-ff15d32c-199-jvm-gc | rank_regressed | 5 | 9 | -4.0 | adservice | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-0410d710-226-pod-kill | rank_regressed | 4 | 7 | -3.0 | paymentservice | frontend|redis-cart|cartservice|checkoutservice|shippingservice | unknown | unknown |
| aiops2025-0b81a605-339-cpu-stress | rank_regressed | 3 | 6 | -3.0 | paymentservice | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | stress | 0b81a605-339-cpu |
| aiops2025-233e0282-88-cpu-stress | rank_regressed | 4 | 7 | -3.0 | currencyservice | frontend|cartservice|checkoutservice|recommendationservice|productcatalogservice | stress | 233e0282-88-cpu |
| aiops2025-6637fe70-563-cpu-stress | rank_regressed | 2 | 5 | -3.0 | currencyservice | frontend|checkoutservice|recommendationservice|cartservice|currencyservice | stress | 6637fe70-563-cpu |
| aiops2025-76222cb2-331-code-error | rank_regressed | 6 | 9 | -3.0 | currencyservice | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-864797d5-271-jvm-gc | rank_regressed | 5 | 8 | -3.0 | adservice | frontend|redis-cart|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-97d37c35-186-jvm-exception | rank_regressed | 2 | 5 | -3.0 | adservice | frontend|checkoutservice|recommendationservice|cartservice|adservice | exception | 97d37c35-186-jvm |
| aiops2025-aa53ee7c-259-jvm-latency | rank_regressed | 5 | 8 | -3.0 | adservice | frontend|redis-cart|shippingservice|cartservice|checkoutservice | unknown | unknown |
| aiops2025-c6e9faa0-270-memory-stress | rank_regressed | 3 | 6 | -3.0 | currencyservice | frontend|shippingservice|checkoutservice|redis-cart|cartservice | stress | c6e9faa0-270-memory |
| aiops2025-e55fb1cb-192-jvm-gc | rank_regressed | 6 | 9 | -3.0 | adservice | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-04418665-287-jvm-gc | rank_regressed | 5 | 7 | -2.0 | adservice | frontend|checkoutservice|recommendationservice|cartservice|productcatalogservice | unknown | unknown |
| aiops2025-13ebf32d-216-jvm-cpu | rank_regressed | 6 | 8 | -2.0 | adservice | frontend|redis-cart|checkoutservice|recommendationservice|cartservice | unknown | unknown |
| aiops2025-14c1047f-366-code-error | rank_regressed | 6 | 8 | -2.0 | currencyservice | frontend|checkoutservice|shippingservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-2cce5582-215-jvm-cpu | rank_regressed | 3 | 5 | -2.0 | adservice | frontend|cartservice|checkoutservice|recommendationservice|adservice | unknown | unknown |
| aiops2025-343ba04c-129-jvm-exception | rank_regressed | 8 | 10 | -2.0 | adservice | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | exception | 343ba04c-129-jvm |
| aiops2025-4be46c92-236-jvm-gc | rank_regressed | 3 | 5 | -2.0 | adservice | checkoutservice|frontend|cartservice|shippingservice|adservice | unknown | unknown |
| aiops2025-81a145a5-394-target-port-misconfig | rank_regressed | 7 | 9 | -2.0 | paymentservice | checkoutservice|frontend|shippingservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-9f49250a-383-target-port-misconfig | rank_regressed | 2 | 4 | -2.0 | emailservice | checkoutservice|frontend|cartservice|emailservice|shippingservice | unknown | unknown |
| aiops2025-a7ed866b-406-target-port-misconfig | rank_regressed | 5 | 7 | -2.0 | checkoutservice | frontend|shippingservice|cartservice|recommendationservice|productcatalogservice | unknown | unknown |
| aiops2025-aa100326-220-jvm-latency | rank_regressed | 6 | 8 | -2.0 | adservice | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-b4feec3f-413-target-port-misconfig | rank_regressed | 5 | 7 | -2.0 | checkoutservice | frontend|shippingservice|cartservice|recommendationservice|productcatalogservice | unknown | unknown |
| aiops2025-de83df2d-281-pod-failure | rank_regressed | 7 | 9 | -2.0 | adservice | frontend|recommendationservice|checkoutservice|cartservice|productcatalogservice | pod-failure | de83df2d-281 |
| aiops2025-df892932-168-jvm-cpu | rank_regressed | 2 | 4 | -2.0 | adservice | frontend|checkoutservice|recommendationservice|adservice|cartservice | unknown | unknown |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
