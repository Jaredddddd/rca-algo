# EvidenceRank PV_CREST2_DYNAMIC_AIOPS25_SERVICE Summary

- Created: 2026-06-10T20:15:01+08:00
- Source: `PV_CREST2_DYNAMIC_AIOPS25_SERVICE`
- Algorithm: `crest`
- Dataset: `aiopschallenge2025_rcabench_service`

## Metrics

| metric | value |
| --- | ---: |
| total | 230 |
| missing_outputs | 0 |
| AC@1 | 0.526087 |
| AC@3 | 0.756522 |
| AC@5 | 0.826087 |
| MRR | 0.662711 |
| avg_rank | 2.847826 |
| top1_miss | 109 |
| top5_miss | 40 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 14 | 0.000000 | 0.571429 | 0.642857 | 0.278458 | 5 |
| case_service | 0b81a605-339-cpu | 1 | 0.000000 | 0.000000 | 0.000000 | 0.142857 | 1 |
| case_service | 0efb9550-160-memory | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 0fccdcad-125-cpu | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 1003cbad-421-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 1193b5d8-230 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 11f619f0-285 | 1 | 0.000000 | 0.000000 | 0.000000 | 0.166667 | 1 |
| case_service | 192019ef-486-cpu | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 1c4a277a-491-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 233e0282-88-cpu | 1 | 0.000000 | 0.000000 | 0.000000 | 0.125000 | 1 |
| case_service | 26c9ab68-91-cpu | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 27914c5a-288 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 3400061d-135 | 1 | 0.000000 | 0.000000 | 1.000000 | 0.200000 | 0 |
| case_service | 342d4820-100-network | 1 | 0.000000 | 0.000000 | 1.000000 | 0.250000 | 0 |
| case_service | 343ba04c-129-jvm | 1 | 0.000000 | 0.000000 | 0.000000 | 0.100000 | 1 |
| case_service | 345fbe93-80-cpu | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 37de08d4-269-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |
| case_service | 38ee3d45-82 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 3da57a36-286-network | 1 | 0.000000 | 1.000000 | 1.000000 | 0.333333 | 0 |
| case_service | 42c6ad6f-136 | 1 | 0.000000 | 1.000000 | 1.000000 | 0.500000 | 0 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| aiops2025-6a9a1c00-210-jvm-latency | adservice | 11 | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-74bd0298-209-jvm-latency | adservice | 11 | frontend|recommendationservice|checkoutservice|shippingservice|cartservice | unknown | unknown |
| aiops2025-b06baad3-363-target-port-misconfig | adservice | 11 | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | unknown | unknown |
| aiops2025-bdc8184e-246-jvm-latency | adservice | 11 | frontend|checkoutservice|recommendationservice|cartservice|productcatalogservice | unknown | unknown |
| aiops2025-343ba04c-129-jvm-exception | adservice | 10 | frontend|checkoutservice|cartservice|recommendationservice|shippingservice | exception | 343ba04c-129-jvm |
| aiops2025-3600f326-158-jvm-gc | adservice | 10 | frontend|checkoutservice|recommendationservice|shippingservice|cartservice | unknown | unknown |
| aiops2025-4664a5e8-251-jvm-exception | adservice | 10 | frontend|checkoutservice|cartservice|recommendationservice|redis-cart | exception | 4664a5e8-251-jvm |
| aiops2025-6add78b2-480-cpu-stress | paymentservice | 10 | frontend|checkoutservice|redis-cart|cartservice|recommendationservice | stress | 6add78b2-480-cpu |
| aiops2025-7984364a-195-jvm-latency | adservice | 10 | frontend|recommendationservice|checkoutservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-d44478e6-328-dns-error | checkoutservice | 10 | adservice|hipstershop|shippingservice|currencyservice|paymentservice | unknown | unknown |
| aiops2025-d9fb014e-206-jvm-latency | adservice | 10 | frontend|cartservice|checkoutservice|recommendationservice|redis-cart | unknown | unknown |
| aiops2025-371ba498-375-target-port-misconfig | paymentservice | 9 | frontend|checkoutservice|shippingservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-523bb271-495-target-port-misconfig | adservice | 9 | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-68727566-367-target-port-misconfig | paymentservice | 9 | checkoutservice|frontend|cartservice|shippingservice|redis-cart | unknown | unknown |
| aiops2025-81a145a5-394-target-port-misconfig | paymentservice | 9 | checkoutservice|frontend|shippingservice|cartservice|recommendationservice | unknown | unknown |
| aiops2025-980853cb-240-jvm-exception | adservice | 9 | frontend|checkoutservice|redis-cart|recommendationservice|productcatalogservice | exception | 980853cb-240-jvm |
| aiops2025-aa100326-220-jvm-latency | adservice | 9 | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-de83df2d-281-pod-failure | adservice | 9 | frontend|recommendationservice|checkoutservice|cartservice|productcatalogservice | pod-failure | de83df2d-281 |
| aiops2025-f35a1832-257-jvm-latency | adservice | 9 | checkoutservice|frontend|cartservice|emailservice|recommendationservice | unknown | unknown |
| aiops2025-f62b1785-258-pod-failure | adservice | 9 | frontend|checkoutservice|cartservice|recommendationservice|redis-cart | pod-failure | f62b1785-258 |
| aiops2025-ff15d32c-199-jvm-gc | adservice | 9 | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | unknown | unknown |
| aiops2025-233e0282-88-cpu-stress | currencyservice | 8 | frontend|cartservice|checkoutservice|recommendationservice|productcatalogservice | stress | 233e0282-88-cpu |
| aiops2025-7bdc4b83-164-jvm-latency | adservice | 8 | frontend|checkoutservice|recommendationservice|cartservice|shippingservice | unknown | unknown |
| aiops2025-8c1e8ce9-237-jvm-cpu | adservice | 8 | frontend|checkoutservice|recommendationservice|cartservice|productcatalogservice | unknown | unknown |
| aiops2025-a0d5329b-489-dns-error | checkoutservice | 8 | currencyservice|recommendationservice|example-ant|cartservice|hipstershop | unknown | unknown |
| aiops2025-fb20d6d2-350-dns-error | checkoutservice | 8 | adservice|currencyservice|frontend|recommendationservice|cartservice | unknown | unknown |
| aiops2025-0b81a605-339-cpu-stress | paymentservice | 7 | frontend|checkoutservice|cartservice|shippingservice|recommendationservice | stress | 0b81a605-339-cpu |
| aiops2025-7e54232b-275-cpu-stress | checkoutservice | 7 | adservice|hipstershop|currencyservice|redis-cart|cartservice | stress | 7e54232b-275-cpu |
| aiops2025-a7ed866b-406-target-port-misconfig | checkoutservice | 7 | frontend|shippingservice|cartservice|recommendationservice|productcatalogservice | unknown | unknown |
| aiops2025-b4feec3f-413-target-port-misconfig | checkoutservice | 7 | frontend|shippingservice|cartservice|recommendationservice|productcatalogservice | unknown | unknown |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
