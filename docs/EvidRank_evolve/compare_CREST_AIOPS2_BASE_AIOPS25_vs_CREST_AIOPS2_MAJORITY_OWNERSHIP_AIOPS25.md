# EvidenceRank Compare CREST_AIOPS2_BASE_AIOPS25 vs CREST_AIOPS2_MAJORITY_OWNERSHIP_AIOPS25

- Created: 2026-06-08T22:13:39+08:00
- Old: `CREST_AIOPS2_BASE_AIOPS25`
- New: `CREST_AIOPS2_MAJORITY_OWNERSHIP_AIOPS25`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.413043 | 0.421739 | 0.008696 |
| AC@3 | 0.678261 | 0.660870 | -0.017391 |
| AC@5 | 0.786957 | 0.778261 | -0.008696 |
| MRR | 0.580494 | 0.586693 | 0.006199 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 4 |
| rank_improved | 24 |
| rank_regressed | 23 |
| regressed_from_hit1 | 2 |
| unchanged | 177 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| aiops2025-009be6db-313-code-error | improved_to_hit1 | 2 | 1 | 1.0 | cartservice | cartservice|frontend|checkoutservice|redis-cart|recommendationservice | unknown | unknown |
| aiops2025-33492fcd-575-cpu-stress | improved_to_hit1 | 2 | 1 | 1.0 | currencyservice | currencyservice|frontend|checkoutservice|cartservice|recommendationservice | stress | 33492fcd-575-cpu |
| aiops2025-4fd42adb-327-memory-stress | improved_to_hit1 | 2 | 1 | 1.0 | adservice | adservice|frontend|checkoutservice|cartservice|recommendationservice | stress | 4fd42adb-327-memory |
| aiops2025-84f4b04a-283-memory-stress | improved_to_hit1 | 2 | 1 | 1.0 | currencyservice | currencyservice|frontend|checkoutservice|cartservice|recommendationservice | stress | 84f4b04a-283-memory |
| aiops2025-0419ba04-373-target-port-misconfig | rank_improved | 9 | 8 | 1.0 | currencyservice | frontend|shippingservice|checkoutservice|recommendationservice|cartservice | unknown | unknown |
| aiops2025-20f9c3bc-558-code-error | rank_improved | 9 | 8 | 1.0 | currencyservice | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-2272a5ff-138-jvm-exception | rank_improved | 9 | 8 | 1.0 | adservice | checkoutservice|frontend|cartservice|recommendationservice|shippingservice | exception | 2272a5ff-138-jvm |
| aiops2025-251c4f53-179-pod-kill | rank_improved | 3 | 2 | 1.0 | cartservice | frontend|cartservice|checkoutservice|shippingservice|productcatalogservice | unknown | unknown |
| aiops2025-2cce5582-215-jvm-cpu | rank_improved | 3 | 2 | 1.0 | adservice | frontend|adservice|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-3d6c95dd-595-target-port-misconfig | rank_improved | 4 | 3 | 1.0 | shippingservice | frontend|checkoutservice|shippingservice|recommendationservice|cartservice | unknown | unknown |
| aiops2025-4be46c92-236-jvm-gc | rank_improved | 3 | 2 | 1.0 | adservice | checkoutservice|adservice|frontend|cartservice|shippingservice | unknown | unknown |
| aiops2025-55759137-403-network-loss | rank_improved | 3 | 2 | 1.0 | cartservice;redis-cart | frontend|cartservice|checkoutservice|shippingservice|redis-cart | loss | 55759137-403-network |
| aiops2025-66cfe1dd-121-cpu-stress | rank_improved | 3 | 2 | 1.0 | emailservice | checkoutservice|emailservice|frontend|cartservice|recommendationservice | stress | 66cfe1dd-121-cpu |
| aiops2025-88b7daff-343-network-delay | rank_improved | 3 | 2 | 1.0 | cartservice;redis-cart | frontend|redis-cart|checkoutservice|cartservice|shippingservice | delay | 88b7daff-343-network |
| aiops2025-9450018e-372-code-error | rank_improved | 5 | 4 | 1.0 | currencyservice | frontend|checkoutservice|cartservice|currencyservice|recommendationservice | unknown | unknown |
| aiops2025-b7177fa5-409-network-corrupt | rank_improved | 3 | 2 | 1.0 | cartservice;redis-cart | frontend|cartservice|checkoutservice|redis-cart|recommendationservice | corrupt | b7177fa5-409-network |
| aiops2025-b9539d8e-345-target-port-misconfig | rank_improved | 3 | 2 | 1.0 | productcatalogservice | frontend|productcatalogservice|recommendationservice|cartservice|checkoutservice | unknown | unknown |
| aiops2025-d124f9b7-379-cpu-stress | rank_improved | 3 | 2 | 1.0 | productcatalogservice | frontend|productcatalogservice|recommendationservice|checkoutservice|cartservice | stress | d124f9b7-379-cpu |
| aiops2025-dc62e30c-113-network-corrupt | rank_improved | 3 | 2 | 1.0 | cartservice;redis-cart | frontend|cartservice|checkoutservice|shippingservice|recommendationservice | corrupt | dc62e30c-113-network |
| aiops2025-fb327034-184-jvm-exception | rank_improved | 9 | 8 | 1.0 | adservice | frontend|cartservice|redis-cart|shippingservice|recommendationservice | exception | fb327034-184-jvm |
| aiops2025-4229b9c5-198-jvm-latency | rank_improved | 9 | 7 | 2.0 | adservice | cartservice|frontend|checkoutservice|recommendationservice|redis-cart | unknown | unknown |
| aiops2025-7513dbaf-190-jvm-latency | rank_improved | 9 | 7 | 2.0 | adservice | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | unknown | unknown |
| aiops2025-a1b60eea-278-jvm-gc | rank_improved | 8 | 6 | 2.0 | adservice | shippingservice|frontend|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-ae4abdbe-103-memory-stress | rank_improved | 5 | 3 | 2.0 | productcatalogservice | frontend|cartservice|productcatalogservice|recommendationservice|checkoutservice | stress | ae4abdbe-103-memory |
| aiops2025-ba74cb57-142-memory-stress | rank_improved | 5 | 3 | 2.0 | productcatalogservice | checkoutservice|frontend|productcatalogservice|cartservice|emailservice | stress | ba74cb57-142-memory |
| aiops2025-de4a919c-126-memory-stress | rank_improved | 6 | 4 | 2.0 | paymentservice | frontend|redis-cart|cartservice|paymentservice|checkoutservice | stress | de4a919c-126-memory |
| aiops2025-df11e2f0-229-cpu-stress | rank_improved | 6 | 4 | 2.0 | adservice | frontend|redis-cart|cartservice|adservice|recommendationservice | stress | df11e2f0-229-cpu |
| aiops2025-cb5815ce-161-jvm-cpu | rank_improved | 7 | 4 | 3.0 | adservice | frontend|checkoutservice|redis-cart|adservice|cartservice | unknown | unknown |
| aiops2025-3600f326-158-jvm-gc | rank_regressed | 6 | 10 | -4.0 | adservice | frontend|paymentservice|checkoutservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-bc9db995-235-pod-kill | rank_regressed | 4 | 7 | -3.0 | adservice | frontend|checkoutservice|cartservice|shippingservice|redis-cart | unknown | unknown |
| aiops2025-81a145a5-394-target-port-misconfig | rank_regressed | 7 | 9 | -2.0 | paymentservice | checkoutservice|frontend|shippingservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-8c1e8ce9-237-jvm-cpu | rank_regressed | 2 | 4 | -2.0 | adservice | frontend|checkoutservice|cartservice|adservice|recommendationservice | unknown | unknown |
| aiops2025-9b0d8a50-187-jvm-exception | rank_regressed | 2 | 4 | -2.0 | adservice | frontend|checkoutservice|recommendationservice|adservice|cartservice | exception | 9b0d8a50-187-jvm |
| aiops2025-ac9112a4-420-code-error | rank_regressed | 2 | 4 | -2.0 | checkoutservice | frontend|shippingservice|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-f62b1785-258-pod-failure | rank_regressed | 2 | 4 | -2.0 | adservice | frontend|checkoutservice|cartservice|adservice|recommendationservice | pod-failure | f62b1785-258 |
| aiops2025-343ba04c-129-jvm-exception | rank_regressed | 8 | 9 | -1.0 | adservice | frontend|paymentservice|cartservice|checkoutservice|shippingservice | exception | 343ba04c-129-jvm |
| aiops2025-36937f85-134-jvm-latency | rank_regressed | 8 | 9 | -1.0 | adservice | redis-cart|frontend|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-4664a5e8-251-jvm-exception | rank_regressed | 6 | 7 | -1.0 | adservice | frontend|checkoutservice|paymentservice|cartservice|recommendationservice | exception | 4664a5e8-251-jvm |
| aiops2025-5d022708-414-target-port-misconfig | rank_regressed | 3 | 4 | -1.0 | shippingservice | checkoutservice|frontend|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-6dee3cf4-590-dns-error | rank_regressed | 2 | 3 | -1.0 | checkoutservice | frontend|shippingservice|checkoutservice|recommendationservice|cartservice | unknown | unknown |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
