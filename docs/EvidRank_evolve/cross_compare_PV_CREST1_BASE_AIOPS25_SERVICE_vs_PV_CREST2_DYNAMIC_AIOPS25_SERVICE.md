# EvidenceRank Compare PV_CREST1_BASE_AIOPS25_SERVICE vs PV_CREST2_DYNAMIC_AIOPS25_SERVICE

- Created: 2026-06-10T20:15:02+08:00
- Old: `PV_CREST1_BASE_AIOPS25_SERVICE`
- New: `PV_CREST2_DYNAMIC_AIOPS25_SERVICE`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.334783 | 0.526087 | 0.191304 |
| AC@3 | 0.600000 | 0.756522 | 0.156522 |
| AC@5 | 0.669565 | 0.826087 | 0.156522 |
| MRR | 0.503603 | 0.662711 | 0.159108 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 55 |
| rank_improved | 6 |
| rank_regressed | 12 |
| regressed_from_hit1 | 11 |
| unchanged | 146 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| aiops2025-14cf33ba-256-network-delay | improved_to_hit1 | 2 | 1 | 1.0 | checkoutservice;currencyservice | currencyservice|frontend|hipstershop|adservice|checkoutservice | delay | 14cf33ba-256-network |
| aiops2025-62e9d294-564-network-delay | improved_to_hit1 | 2 | 1 | 1.0 | checkoutservice;currencyservice | currencyservice|frontend|hipstershop|recommendationservice|checkoutservice | delay | 62e9d294-564-network |
| aiops2025-8440ee17-580-target-port-misconfig | improved_to_hit1 | 2 | 1 | 1.0 | shippingservice | shippingservice|frontend|paymentservice|adservice|hipstershop | unknown | unknown |
| aiops2025-cebb47f5-165-pod-kill | improved_to_hit1 | 2 | 1 | 1.0 | paymentservice | paymentservice|currencyservice|adservice|frontend|cartservice | unknown | unknown |
| aiops2025-d99a98a0-233-pod-kill | improved_to_hit1 | 2 | 1 | 1.0 | paymentservice | paymentservice|adservice|currencyservice|shippingservice|cartservice | unknown | unknown |
| aiops2025-20622318-94-jvm-cpu | improved_to_hit1 | 3 | 1 | 2.0 | adservice | adservice|hipstershop|frontend|paymentservice|currencyservice | unknown | unknown |
| aiops2025-47fe21f6-167-jvm-exception | improved_to_hit1 | 3 | 1 | 2.0 | adservice | adservice|frontend|paymentservice|currencyservice|cartservice | exception | 47fe21f6-167-jvm |
| aiops2025-4fd42adb-327-memory-stress | improved_to_hit1 | 3 | 1 | 2.0 | adservice | adservice|frontend|paymentservice|currencyservice|cartservice | stress | 4fd42adb-327-memory |
| aiops2025-84f4b04a-283-memory-stress | improved_to_hit1 | 3 | 1 | 2.0 | currencyservice | currencyservice|adservice|frontend|recommendationservice|cartservice | stress | 84f4b04a-283-memory |
| aiops2025-d0be3c58-178-jvm-cpu | improved_to_hit1 | 3 | 1 | 2.0 | adservice | adservice|redis-cart|frontend|cartservice|currencyservice | unknown | unknown |
| aiops2025-33492fcd-575-cpu-stress | improved_to_hit1 | 4 | 1 | 3.0 | currencyservice | currencyservice|adservice|frontend|hipstershop|cartservice | stress | 33492fcd-575-cpu |
| aiops2025-5d022708-414-target-port-misconfig | improved_to_hit1 | 4 | 1 | 3.0 | shippingservice | shippingservice|checkoutservice|frontend|cartservice|paymentservice | unknown | unknown |
| aiops2025-f887d7ff-238-jvm-cpu | improved_to_hit1 | 4 | 1 | 3.0 | adservice | adservice|currencyservice|paymentservice|recommendationservice|frontend | unknown | unknown |
| aiops2025-6574656a-250-pod-kill | improved_to_hit1 | 5 | 1 | 4.0 | paymentservice | paymentservice|adservice|currencyservice|cartservice|checkoutservice | unknown | unknown |
| aiops2025-6637fe70-563-cpu-stress | improved_to_hit1 | 5 | 1 | 4.0 | currencyservice | currencyservice|adservice|frontend|hipstershop|cartservice | stress | 6637fe70-563-cpu |
| aiops2025-df892932-168-jvm-cpu | improved_to_hit1 | 5 | 1 | 4.0 | adservice | adservice|hipstershop|frontend|cartservice|currencyservice | unknown | unknown |
| aiops2025-abb62970-110-jvm-cpu | improved_to_hit1 | 6 | 1 | 5.0 | adservice | adservice|currencyservice|hipstershop|frontend|cartservice | unknown | unknown |
| aiops2025-04418665-287-jvm-gc | improved_to_hit1 | 7 | 1 | 6.0 | adservice | adservice|frontend|paymentservice|currencyservice|hipstershop | unknown | unknown |
| aiops2025-2cce5582-215-jvm-cpu | improved_to_hit1 | 7 | 1 | 6.0 | adservice | adservice|hipstershop|frontend|cartservice|currencyservice | unknown | unknown |
| aiops2025-97d37c35-186-jvm-exception | improved_to_hit1 | 7 | 1 | 6.0 | adservice | adservice|hipstershop|frontend|paymentservice|currencyservice | exception | 97d37c35-186-jvm |
| aiops2025-0410d710-226-pod-kill | improved_to_hit1 | 8 | 1 | 7.0 | paymentservice | paymentservice|frontend|redis-cart|currencyservice|cartservice | unknown | unknown |
| aiops2025-13ebf32d-216-jvm-cpu | improved_to_hit1 | 8 | 1 | 7.0 | adservice | adservice|hipstershop|frontend|redis-cart|currencyservice | unknown | unknown |
| aiops2025-3ae307d9-218-jvm-exception | improved_to_hit1 | 8 | 1 | 7.0 | adservice | adservice|hipstershop|shippingservice|example-ant|currencyservice | exception | 3ae307d9-218-jvm |
| aiops2025-4be46c92-236-jvm-gc | improved_to_hit1 | 8 | 1 | 7.0 | adservice | adservice|currencyservice|checkoutservice|paymentservice|hipstershop | unknown | unknown |
| aiops2025-578fce7c-166-jvm-gc | improved_to_hit1 | 8 | 1 | 7.0 | adservice | adservice|hipstershop|shippingservice|currencyservice|paymentservice | unknown | unknown |
| aiops2025-c6e9faa0-270-memory-stress | improved_to_hit1 | 8 | 1 | 7.0 | currencyservice | currencyservice|paymentservice|redis-cart|adservice|cartservice | stress | c6e9faa0-270-memory |
| aiops2025-de4a919c-126-memory-stress | improved_to_hit1 | 8 | 1 | 7.0 | paymentservice | paymentservice|frontend|adservice|currencyservice|cartservice | stress | de4a919c-126-memory |
| aiops2025-df11e2f0-229-cpu-stress | improved_to_hit1 | 8 | 1 | 7.0 | adservice | adservice|frontend|currencyservice|cartservice|paymentservice | stress | df11e2f0-229-cpu |
| aiops2025-14c1047f-366-code-error | improved_to_hit1 | 9 | 1 | 8.0 | currencyservice | currencyservice|frontend|shippingservice|hipstershop|checkoutservice | unknown | unknown |
| aiops2025-20f9c3bc-558-code-error | improved_to_hit1 | 9 | 1 | 8.0 | currencyservice | currencyservice|frontend|hipstershop|cartservice|shippingservice | unknown | unknown |
| aiops2025-2272a5ff-138-jvm-exception | improved_to_hit1 | 9 | 1 | 8.0 | adservice | adservice|frontend|currencyservice|checkoutservice|cartservice | exception | 2272a5ff-138-jvm |
| aiops2025-36937f85-134-jvm-latency | improved_to_hit1 | 9 | 1 | 8.0 | adservice | adservice|paymentservice|currencyservice|redis-cart|cartservice | unknown | unknown |
| aiops2025-4229b9c5-198-jvm-latency | improved_to_hit1 | 9 | 1 | 8.0 | adservice | adservice|cartservice|hipstershop|frontend|currencyservice | unknown | unknown |
| aiops2025-499d8ec0-211-jvm-gc | improved_to_hit1 | 9 | 1 | 8.0 | adservice | adservice|frontend|checkoutservice|currencyservice|cartservice | unknown | unknown |
| aiops2025-4e221a94-277-memory-stress | improved_to_hit1 | 9 | 1 | 8.0 | paymentservice | paymentservice|adservice|currencyservice|cartservice|redis-cart | stress | 4e221a94-277-memory |
| aiops2025-6a643823-196-jvm-latency | improved_to_hit1 | 9 | 1 | 8.0 | adservice | adservice|paymentservice|currencyservice|cartservice|hipstershop | unknown | unknown |
| aiops2025-6ef260df-97-jvm-gc | improved_to_hit1 | 9 | 1 | 8.0 | adservice | adservice|currencyservice|paymentservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-744d4e2b-106-jvm-cpu | improved_to_hit1 | 9 | 1 | 8.0 | adservice | adservice|cartservice|currencyservice|redis-cart|frontend | unknown | unknown |
| aiops2025-7513dbaf-190-jvm-latency | improved_to_hit1 | 9 | 1 | 8.0 | adservice | adservice|hipstershop|checkoutservice|frontend|currencyservice | unknown | unknown |
| aiops2025-76222cb2-331-code-error | improved_to_hit1 | 9 | 1 | 8.0 | currencyservice | currencyservice|frontend|hipstershop|cartservice|shippingservice | unknown | unknown |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
