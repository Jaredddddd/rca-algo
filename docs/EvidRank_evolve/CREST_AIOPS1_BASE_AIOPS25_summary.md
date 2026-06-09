# EvidenceRank CREST_AIOPS1_BASE_AIOPS25 Summary

- Created: 2026-06-08T20:09:28+08:00
- Source: `CREST_AIOPS1_BASE_AIOPS25`
- Algorithm: `crest`
- Dataset: `aiopschallenge2025_rcabench_service`

## Metrics

| metric | value |
| --- | ---: |
| total | 230 |
| missing_outputs | 0 |
| AC@1 | 0.334783 |
| AC@3 | 0.600000 |
| AC@5 | 0.669565 |
| MRR | 0.503603 |
| avg_rank | 4.160870 |
| top1_miss | 153 |
| top5_miss | 76 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | exception | 10 | 0.000000 | 0.100000 | 0.100000 | 0.135675 | 9 |
| case_service | 0b81a605-339-cpu | 1 | 0.000000 | 0.000000 | 0.000000 | 0.142857 | 1 |
| case_service | 0efb9550-160-memory | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 1003cbad-421-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 11f619f0-285 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 14cf33ba-256-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 192019ef-486-cpu | 1 | 0.000000 | 0.000000 | 0.000000 | 0.100000 | 1 |
| case_service | 1c4a277a-491-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 2272a5ff-138-jvm | 1 | 0.000000 | 0.000000 | 0.000000 | 0.111111 | 1 |
| case_service | 233e0282-88-cpu | 1 | 0.000000 | 0.000000 | 0.000000 | 0.125000 | 1 |
| case_service | 26c9ab68-91-cpu | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 27914c5a-288 | 1 | 0.000000 | 0.000000 | 0.000000 | 0.083333 | 1 |
| case_service | 33492fcd-575-cpu | 1 | 0.000000 | 0.000000 | 1.000000 | 0.250000 | 0 |
| case_service | 3400061d-135 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 343ba04c-129-jvm | 1 | 0.000000 | 0.000000 | 0.000000 | 0.100000 | 1 |
| case_service | 37de08d4-269-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 38ee3d45-82 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 3ae307d9-218-jvm | 1 | 0.000000 | 0.000000 | 0.000000 | 0.125000 | 1 |
| case_service | 3da57a36-286-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 42c6ad6f-136 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| aiops2025-27914c5a-288-pod-failure | paymentservice | 12 | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | pod-failure | 27914c5a-288 |
| aiops2025-6a9a1c00-210-jvm-latency | adservice | 11 | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-74bd0298-209-jvm-latency | adservice | 11 | frontend|recommendationservice|checkoutservice|shippingservice|cartservice | unknown | unknown |
| aiops2025-b06baad3-363-target-port-misconfig | adservice | 11 | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | unknown | unknown |
| aiops2025-bdc8184e-246-jvm-latency | adservice | 11 | frontend|checkoutservice|recommendationservice|cartservice|productcatalogservice | unknown | unknown |
| aiops2025-192019ef-486-cpu-stress | currencyservice | 10 | checkoutservice|frontend|cartservice|recommendationservice|shippingservice | stress | 192019ef-486-cpu |
| aiops2025-343ba04c-129-jvm-exception | adservice | 10 | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | exception | 343ba04c-129-jvm |
| aiops2025-3600f326-158-jvm-gc | adservice | 10 | frontend|checkoutservice|recommendationservice|shippingservice|cartservice | unknown | unknown |
| aiops2025-4664a5e8-251-jvm-exception | adservice | 10 | frontend|checkoutservice|cartservice|recommendationservice|redis-cart | exception | 4664a5e8-251-jvm |
| aiops2025-6add78b2-480-cpu-stress | paymentservice | 10 | frontend|checkoutservice|redis-cart|cartservice|recommendationservice | stress | 6add78b2-480-cpu |
| aiops2025-7984364a-195-jvm-latency | adservice | 10 | frontend|recommendationservice|checkoutservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-d9fb014e-206-jvm-latency | adservice | 10 | frontend|cartservice|checkoutservice|recommendationservice|redis-cart | unknown | unknown |
| aiops2025-e55fb1cb-192-jvm-gc | adservice | 10 | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-0419ba04-373-target-port-misconfig | currencyservice | 9 | frontend|shippingservice|checkoutservice|recommendationservice|cartservice | unknown | unknown |
| aiops2025-14c1047f-366-code-error | currencyservice | 9 | frontend|checkoutservice|shippingservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-20f9c3bc-558-code-error | currencyservice | 9 | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | unknown | unknown |
| aiops2025-2272a5ff-138-jvm-exception | adservice | 9 | checkoutservice|frontend|cartservice|recommendationservice|shippingservice | exception | 2272a5ff-138-jvm |
| aiops2025-36937f85-134-jvm-latency | adservice | 9 | frontend|redis-cart|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-371ba498-375-target-port-misconfig | paymentservice | 9 | frontend|checkoutservice|shippingservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-4229b9c5-198-jvm-latency | adservice | 9 | frontend|cartservice|checkoutservice|recommendationservice|redis-cart | unknown | unknown |
| aiops2025-499d8ec0-211-jvm-gc | adservice | 9 | checkoutservice|frontend|emailservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-4e221a94-277-memory-stress | paymentservice | 9 | checkoutservice|redis-cart|cartservice|frontend|emailservice | stress | 4e221a94-277-memory |
| aiops2025-523bb271-495-target-port-misconfig | adservice | 9 | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-68727566-367-target-port-misconfig | paymentservice | 9 | checkoutservice|frontend|cartservice|shippingservice|redis-cart | unknown | unknown |
| aiops2025-6a643823-196-jvm-latency | adservice | 9 | cartservice|frontend|redis-cart|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-6ef260df-97-jvm-gc | adservice | 9 | checkoutservice|frontend|cartservice|emailservice|recommendationservice | unknown | unknown |
| aiops2025-744d4e2b-106-jvm-cpu | adservice | 9 | frontend|cartservice|redis-cart|recommendationservice|productcatalogservice | unknown | unknown |
| aiops2025-7513dbaf-190-jvm-latency | adservice | 9 | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | unknown | unknown |
| aiops2025-76222cb2-331-code-error | currencyservice | 9 | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | unknown | unknown |
| aiops2025-81a145a5-394-target-port-misconfig | paymentservice | 9 | checkoutservice|frontend|shippingservice|cartservice|recommendationservice | unknown | unknown |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
