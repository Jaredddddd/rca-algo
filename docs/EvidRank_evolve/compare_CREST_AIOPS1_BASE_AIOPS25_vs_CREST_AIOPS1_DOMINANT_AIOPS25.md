# EvidenceRank Compare CREST_AIOPS1_BASE_AIOPS25 vs CREST_AIOPS1_DOMINANT_AIOPS25

- Created: 2026-06-08T20:54:26+08:00
- Old: `CREST_AIOPS1_BASE_AIOPS25`
- New: `CREST_AIOPS1_DOMINANT_AIOPS25`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.334783 | 0.413043 | 0.078261 |
| AC@3 | 0.600000 | 0.678261 | 0.078261 |
| AC@5 | 0.669565 | 0.786957 | 0.117391 |
| MRR | 0.503603 | 0.580494 | 0.076891 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 18 |
| rank_improved | 62 |
| rank_regressed | 4 |
| unchanged | 146 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| aiops2025-26c9ab68-91-cpu-stress | improved_to_hit1 | 2 | 1 | 1.0 | emailservice | emailservice|frontend|checkoutservice|cartservice|recommendationservice | stress | 26c9ab68-91-cpu |
| aiops2025-42c6ad6f-136-pod-failure | improved_to_hit1 | 2 | 1 | 1.0 | shippingservice | shippingservice|frontend|checkoutservice|cartservice|recommendationservice | pod-failure | 42c6ad6f-136 |
| aiops2025-4ab999b7-96-cpu-stress | improved_to_hit1 | 2 | 1 | 1.0 | shippingservice | shippingservice|frontend|checkoutservice|cartservice|recommendationservice | stress | 4ab999b7-96-cpu |
| aiops2025-7d23b182-577-memory-stress | improved_to_hit1 | 2 | 1 | 1.0 | checkoutservice | checkoutservice|frontend|cartservice|redis-cart|shippingservice | stress | 7d23b182-577-memory |
| aiops2025-7e03b07d-188-pod-failure | improved_to_hit1 | 2 | 1 | 1.0 | shippingservice | shippingservice|checkoutservice|frontend|emailservice|cartservice | pod-failure | 7e03b07d-188 |
| aiops2025-7e54232b-275-cpu-stress | improved_to_hit1 | 2 | 1 | 1.0 | checkoutservice | checkoutservice|frontend|redis-cart|cartservice|shippingservice | stress | 7e54232b-275-cpu |
| aiops2025-8440ee17-580-target-port-misconfig | improved_to_hit1 | 2 | 1 | 1.0 | shippingservice | shippingservice|frontend|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-88f808ff-426-cpu-stress | improved_to_hit1 | 2 | 1 | 1.0 | cartservice | cartservice|frontend|checkoutservice|redis-cart|shippingservice | stress | 88f808ff-426-cpu |
| aiops2025-96e4b852-189-pod-kill | improved_to_hit1 | 2 | 1 | 1.0 | shippingservice | shippingservice|frontend|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-cebb47f5-165-pod-kill | improved_to_hit1 | 2 | 1 | 1.0 | paymentservice | paymentservice|frontend|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-d99a98a0-233-pod-kill | improved_to_hit1 | 2 | 1 | 1.0 | paymentservice | paymentservice|checkoutservice|frontend|recommendationservice|cartservice | unknown | unknown |
| aiops2025-20622318-94-jvm-cpu | improved_to_hit1 | 3 | 1 | 2.0 | adservice | adservice|frontend|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-38ee3d45-82-pod-failure | improved_to_hit1 | 3 | 1 | 2.0 | cartservice | cartservice|shippingservice|frontend|redis-cart|recommendationservice | pod-failure | 38ee3d45-82 |
| aiops2025-47fe21f6-167-jvm-exception | improved_to_hit1 | 3 | 1 | 2.0 | adservice | adservice|frontend|checkoutservice|cartservice|recommendationservice | exception | 47fe21f6-167-jvm |
| aiops2025-56c934bb-205-pod-failure | improved_to_hit1 | 3 | 1 | 2.0 | cartservice | cartservice|shippingservice|frontend|redis-cart|productcatalogservice | pod-failure | 56c934bb-205 |
| aiops2025-f887d7ff-238-jvm-cpu | improved_to_hit1 | 4 | 1 | 3.0 | adservice | adservice|frontend|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-6574656a-250-pod-kill | improved_to_hit1 | 5 | 1 | 4.0 | paymentservice | paymentservice|cartservice|checkoutservice|frontend|redis-cart | unknown | unknown |
| aiops2025-578fce7c-166-jvm-gc | improved_to_hit1 | 8 | 1 | 7.0 | adservice | adservice|frontend|cartservice|shippingservice|checkoutservice | unknown | unknown |
| aiops2025-0efb9550-160-memory-stress | rank_improved | 3 | 2 | 1.0 | productcatalogservice | frontend|productcatalogservice|recommendationservice|cartservice|checkoutservice | stress | 0efb9550-160-memory |
| aiops2025-36937f85-134-jvm-latency | rank_improved | 9 | 8 | 1.0 | adservice | redis-cart|frontend|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-4fd42adb-327-memory-stress | rank_improved | 3 | 2 | 1.0 | adservice | frontend|adservice|checkoutservice|cartservice|recommendationservice | stress | 4fd42adb-327-memory |
| aiops2025-5d022708-414-target-port-misconfig | rank_improved | 4 | 3 | 1.0 | shippingservice | checkoutservice|frontend|shippingservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-6a643823-196-jvm-latency | rank_improved | 9 | 8 | 1.0 | adservice | cartservice|frontend|redis-cart|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-6add78b2-480-cpu-stress | rank_improved | 10 | 9 | 1.0 | paymentservice | frontend|redis-cart|checkoutservice|cartservice|recommendationservice | stress | 6add78b2-480-cpu |
| aiops2025-744d4e2b-106-jvm-cpu | rank_improved | 9 | 8 | 1.0 | adservice | cartservice|frontend|redis-cart|recommendationservice|productcatalogservice | unknown | unknown |
| aiops2025-7bdc4b83-164-jvm-latency | rank_improved | 8 | 7 | 1.0 | adservice | frontend|checkoutservice|redis-cart|cartservice|recommendationservice | unknown | unknown |
| aiops2025-84f4b04a-283-memory-stress | rank_improved | 3 | 2 | 1.0 | currencyservice | frontend|currencyservice|checkoutservice|cartservice|recommendationservice | stress | 84f4b04a-283-memory |
| aiops2025-959cfb67-502-target-port-misconfig | rank_improved | 9 | 8 | 1.0 | currencyservice | frontend|checkoutservice|redis-cart|cartservice|shippingservice | unknown | unknown |
| aiops2025-980853cb-240-jvm-exception | rank_improved | 9 | 8 | 1.0 | adservice | frontend|redis-cart|checkoutservice|recommendationservice|productcatalogservice | exception | 980853cb-240-jvm |
| aiops2025-a1b60eea-278-jvm-gc | rank_improved | 9 | 8 | 1.0 | adservice | frontend|shippingservice|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-a7b21b38-262-pod-failure | rank_improved | 6 | 5 | 1.0 | shippingservice | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | pod-failure | a7b21b38-262 |
| aiops2025-b06baad3-363-target-port-misconfig | rank_improved | 11 | 10 | 1.0 | adservice | frontend|currencyservice|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-b9319370-341-code-error | rank_improved | 4 | 3 | 1.0 | productcatalogservice | frontend|checkoutservice|productcatalogservice|recommendationservice|shippingservice | unknown | unknown |
| aiops2025-c9832b3e-191-pod-failure | rank_improved | 7 | 6 | 1.0 | checkoutservice | frontend|shippingservice|cartservice|recommendationservice|redis-cart | pod-failure | c9832b3e-191 |
| aiops2025-cc3b1830-139-jvm-gc | rank_improved | 9 | 8 | 1.0 | adservice | cartservice|frontend|checkoutservice|recommendationservice|shippingservice | unknown | unknown |
| aiops2025-d0be3c58-178-jvm-cpu | rank_improved | 3 | 2 | 1.0 | adservice | redis-cart|adservice|frontend|currencyservice|cartservice | unknown | unknown |
| aiops2025-d0ecec7e-381-target-port-misconfig | rank_improved | 7 | 6 | 1.0 | checkoutservice | frontend|cartservice|shippingservice|redis-cart|recommendationservice | unknown | unknown |
| aiops2025-f066e1dd-145-pod-kill | rank_improved | 4 | 3 | 1.0 | shippingservice | frontend|checkoutservice|shippingservice|recommendationservice|cartservice | unknown | unknown |
| aiops2025-04418665-287-jvm-gc | rank_improved | 7 | 5 | 2.0 | adservice | frontend|checkoutservice|cartservice|recommendationservice|adservice | unknown | unknown |
| aiops2025-13ebf32d-216-jvm-cpu | rank_improved | 8 | 6 | 2.0 | adservice | frontend|redis-cart|cartservice|recommendationservice|checkoutservice | unknown | unknown |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
