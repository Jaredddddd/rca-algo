# EvidenceRank CREST_AIOPS1_AIOPS25 Summary

- Created: 2026-06-08T20:30:50+08:00
- Source: `CREST_AIOPS1_AIOPS25`
- Algorithm: `crest`
- Dataset: `aiopschallenge2025_rcabench_service`

## Metrics

| metric | value |
| --- | ---: |
| total | 230 |
| missing_outputs | 0 |
| AC@1 | 0.413043 |
| AC@3 | 0.678261 |
| AC@5 | 0.786957 |
| MRR | 0.580494 |
| avg_rank | 3.286957 |
| top1_miss | 135 |
| top5_miss | 49 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| case_service | 0b81a605-339-cpu | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 0efb9550-160-memory | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 1003cbad-421-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 11f619f0-285 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 14cf33ba-256-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 192019ef-486-cpu | 1 | 0.000000 | 0.000000 | 0.000000 | 0.100000 | 1 |
| case_service | 1c4a277a-491-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 2272a5ff-138-jvm | 1 | 0.000000 | 0.000000 | 0.000000 | 0.111111 | 1 |
| case_service | 233e0282-88-cpu | 1 | 0.000000 | 0.000000 | 1.000000 | 0.250000 | 0 |
| case_service | 27914c5a-288 | 1 | 0.000000 | 0.000000 | 0.000000 | 0.083333 | 1 |
| case_service | 33492fcd-575-cpu | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 3400061d-135 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 343ba04c-129-jvm | 1 | 0.000000 | 0.000000 | 0.000000 | 0.125000 | 1 |
| case_service | 37de08d4-269-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 3ae307d9-218-jvm | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 3da57a36-286-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 4664a5e8-251-jvm | 1 | 0.000000 | 0.000000 | 0.000000 | 0.166667 | 1 |
| case_service | 4e221a94-277-memory | 1 | 0.000000 | 0.000000 | 1.000000 | 0.200000 | 0 |
| case_service | 4fd42adb-327-memory | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 53d5d618-289-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| aiops2025-27914c5a-288-pod-failure | paymentservice | 12 | frontend|checkoutservice|cartservice|adservice|recommendationservice | pod-failure | 27914c5a-288 |
| aiops2025-6a9a1c00-210-jvm-latency | adservice | 11 | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-74bd0298-209-jvm-latency | adservice | 11 | frontend|shippingservice|recommendationservice|checkoutservice|cartservice | unknown | unknown |
| aiops2025-bdc8184e-246-jvm-latency | adservice | 11 | frontend|checkoutservice|recommendationservice|cartservice|redis-cart | unknown | unknown |
| aiops2025-192019ef-486-cpu-stress | currencyservice | 10 | checkoutservice|frontend|cartservice|recommendationservice|shippingservice | stress | 192019ef-486-cpu |
| aiops2025-7984364a-195-jvm-latency | adservice | 10 | frontend|recommendationservice|cartservice|checkoutservice|shippingservice | unknown | unknown |
| aiops2025-b06baad3-363-target-port-misconfig | adservice | 10 | frontend|currencyservice|checkoutservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-d9fb014e-206-jvm-latency | adservice | 10 | frontend|cartservice|checkoutservice|recommendationservice|redis-cart | unknown | unknown |
| aiops2025-0419ba04-373-target-port-misconfig | currencyservice | 9 | frontend|shippingservice|checkoutservice|recommendationservice|cartservice | unknown | unknown |
| aiops2025-20f9c3bc-558-code-error | currencyservice | 9 | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-2272a5ff-138-jvm-exception | adservice | 9 | checkoutservice|frontend|cartservice|recommendationservice|shippingservice | exception | 2272a5ff-138-jvm |
| aiops2025-371ba498-375-target-port-misconfig | paymentservice | 9 | frontend|checkoutservice|shippingservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-4229b9c5-198-jvm-latency | adservice | 9 | frontend|cartservice|checkoutservice|recommendationservice|redis-cart | unknown | unknown |
| aiops2025-499d8ec0-211-jvm-gc | adservice | 9 | checkoutservice|frontend|cartservice|emailservice|shippingservice | unknown | unknown |
| aiops2025-523bb271-495-target-port-misconfig | adservice | 9 | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-68727566-367-target-port-misconfig | paymentservice | 9 | checkoutservice|frontend|redis-cart|cartservice|shippingservice | unknown | unknown |
| aiops2025-6add78b2-480-cpu-stress | paymentservice | 9 | frontend|redis-cart|checkoutservice|cartservice|recommendationservice | stress | 6add78b2-480-cpu |
| aiops2025-6ef260df-97-jvm-gc | adservice | 9 | checkoutservice|frontend|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-7513dbaf-190-jvm-latency | adservice | 9 | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | unknown | unknown |
| aiops2025-87b43d57-223-jvm-exception | adservice | 9 | checkoutservice|frontend|cartservice|shippingservice|recommendationservice | exception | 87b43d57-223-jvm |
| aiops2025-dac96ecf-483-memory-stress | adservice | 9 | frontend|checkoutservice|cartservice|redis-cart|recommendationservice | stress | dac96ecf-483-memory |
| aiops2025-ee69c707-234-jvm-gc | adservice | 9 | frontend|shippingservice|recommendationservice|cartservice|checkoutservice | unknown | unknown |
| aiops2025-f35a1832-257-jvm-latency | adservice | 9 | checkoutservice|frontend|cartservice|emailservice|shippingservice | unknown | unknown |
| aiops2025-fb327034-184-jvm-exception | adservice | 9 | frontend|redis-cart|cartservice|shippingservice|recommendationservice | exception | fb327034-184-jvm |
| aiops2025-343ba04c-129-jvm-exception | adservice | 8 | frontend|paymentservice|cartservice|checkoutservice|shippingservice | exception | 343ba04c-129-jvm |
| aiops2025-36937f85-134-jvm-latency | adservice | 8 | redis-cart|frontend|cartservice|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-6a643823-196-jvm-latency | adservice | 8 | cartservice|frontend|redis-cart|checkoutservice|recommendationservice | unknown | unknown |
| aiops2025-744d4e2b-106-jvm-cpu | adservice | 8 | cartservice|frontend|redis-cart|recommendationservice|productcatalogservice | unknown | unknown |
| aiops2025-959cfb67-502-target-port-misconfig | currencyservice | 8 | frontend|checkoutservice|redis-cart|cartservice|shippingservice | unknown | unknown |
| aiops2025-980853cb-240-jvm-exception | adservice | 8 | frontend|redis-cart|checkoutservice|recommendationservice|productcatalogservice | exception | 980853cb-240-jvm |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
