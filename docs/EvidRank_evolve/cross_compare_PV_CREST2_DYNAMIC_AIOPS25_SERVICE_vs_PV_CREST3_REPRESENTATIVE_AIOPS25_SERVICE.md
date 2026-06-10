# EvidenceRank Compare PV_CREST2_DYNAMIC_AIOPS25_SERVICE vs PV_CREST3_REPRESENTATIVE_AIOPS25_SERVICE

- Created: 2026-06-10T20:45:24+08:00
- Old: `PV_CREST2_DYNAMIC_AIOPS25_SERVICE`
- New: `PV_CREST3_REPRESENTATIVE_AIOPS25_SERVICE`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.526087 | 0.526087 | 0.000000 |
| AC@3 | 0.756522 | 0.782609 | 0.026087 |
| AC@5 | 0.826087 | 0.865217 | 0.039130 |
| MRR | 0.662711 | 0.672613 | 0.009901 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 5 |
| rank_improved | 16 |
| rank_regressed | 3 |
| regressed_from_hit1 | 5 |
| unchanged | 201 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| aiops2025-42c6ad6f-136-pod-failure | improved_to_hit1 | 2 | 1 | 1.0 | shippingservice | shippingservice|currencyservice|adservice|frontend|cartservice | pod-failure | 42c6ad6f-136 |
| aiops2025-7e03b07d-188-pod-failure | improved_to_hit1 | 2 | 1 | 1.0 | shippingservice | shippingservice|currencyservice|frontend|paymentservice|checkoutservice | pod-failure | 7e03b07d-188 |
| aiops2025-eb0c4ea8-182-network-delay | improved_to_hit1 | 6 | 1 | 5.0 | checkoutservice;productcatalogservice | checkoutservice|frontend|cartservice|recommendationservice|productcatalogservice | delay | eb0c4ea8-182-network |
| aiops2025-7bdc4b83-164-jvm-latency | improved_to_hit1 | 8 | 1 | 7.0 | adservice | adservice|frontend|redis-cart|currencyservice|paymentservice | unknown | unknown |
| aiops2025-4664a5e8-251-jvm-exception | improved_to_hit1 | 10 | 1 | 9.0 | adservice | adservice|paymentservice|currencyservice|frontend|checkoutservice | exception | 4664a5e8-251-jvm |
| aiops2025-09b7c00b-344-code-error | rank_improved | 3 | 2 | 1.0 | cartservice | frontend|cartservice|adservice|currencyservice|productcatalogservice | unknown | unknown |
| aiops2025-1193b5d8-230-pod-failure | rank_improved | 3 | 2 | 1.0 | cartservice | adservice|cartservice|paymentservice|recommendationservice|redis-cart | pod-failure | 1193b5d8-230 |
| aiops2025-11f619f0-285-pod-failure | rank_improved | 6 | 5 | 1.0 | productcatalogservice | frontend|adservice|recommendationservice|currencyservice|productcatalogservice | pod-failure | 11f619f0-285 |
| aiops2025-27914c5a-288-pod-failure | rank_improved | 3 | 2 | 1.0 | paymentservice | adservice|paymentservice|frontend|currencyservice|cartservice | pod-failure | 27914c5a-288 |
| aiops2025-4ab999b7-96-cpu-stress | rank_improved | 4 | 3 | 1.0 | shippingservice | adservice|frontend|shippingservice|currencyservice|paymentservice | stress | 4ab999b7-96-cpu |
| aiops2025-53d5d618-289-network-delay | rank_improved | 4 | 3 | 1.0 | cartservice;checkoutservice | adservice|frontend|cartservice|currencyservice|checkoutservice | delay | 53d5d618-289-network |
| aiops2025-757fa56f-263-cpu-stress | rank_improved | 5 | 4 | 1.0 | recommendationservice | paymentservice|productcatalogservice|checkoutservice|recommendationservice|adservice | stress | 757fa56f-263-cpu |
| aiops2025-7e54232b-275-cpu-stress | rank_improved | 7 | 6 | 1.0 | checkoutservice | adservice|currencyservice|redis-cart|cartservice|frontend | stress | 7e54232b-275-cpu |
| aiops2025-a7b21b38-262-pod-failure | rank_improved | 6 | 5 | 1.0 | shippingservice | paymentservice|checkoutservice|frontend|adservice|shippingservice | pod-failure | a7b21b38-262 |
| aiops2025-b9539d8e-345-target-port-misconfig | rank_improved | 6 | 5 | 1.0 | productcatalogservice | frontend|currencyservice|adservice|recommendationservice|productcatalogservice | unknown | unknown |
| aiops2025-c3f4fde9-330-network-delay | rank_improved | 5 | 4 | 1.0 | checkoutservice;emailservice | adservice|frontend|paymentservice|checkoutservice|currencyservice | delay | c3f4fde9-330-network |
| aiops2025-3400061d-135-pod-failure | rank_improved | 5 | 3 | 2.0 | recommendationservice | frontend|adservice|recommendationservice|currencyservice|example-ant | pod-failure | 3400061d-135 |
| aiops2025-a0d5329b-489-dns-error | rank_improved | 8 | 6 | 2.0 | checkoutservice | currencyservice|recommendationservice|cartservice|frontend|adservice | unknown | unknown |
| aiops2025-371ba498-375-target-port-misconfig | rank_improved | 9 | 3 | 6.0 | paymentservice | frontend|checkoutservice|paymentservice|emailservice|adservice | unknown | unknown |
| aiops2025-81a145a5-394-target-port-misconfig | rank_improved | 9 | 2 | 7.0 | paymentservice | checkoutservice|paymentservice|frontend|emailservice|currencyservice | unknown | unknown |
| aiops2025-b06baad3-363-target-port-misconfig | rank_improved | 11 | 2 | 9.0 | adservice | currencyservice|adservice|paymentservice|frontend|cartservice | unknown | unknown |
| aiops2025-96e4b852-189-pod-kill | rank_regressed | 2 | 4 | -2.0 | shippingservice | paymentservice|currencyservice|frontend|shippingservice|adservice | unknown | unknown |
| aiops2025-66cfe1dd-121-cpu-stress | rank_regressed | 3 | 4 | -1.0 | emailservice | currencyservice|adservice|checkoutservice|emailservice|frontend | stress | 66cfe1dd-121-cpu |
| aiops2025-7f595b45-181-network-corrupt | rank_regressed | 2 | 3 | -1.0 | productcatalogservice;recommendationservice | frontend|shippingservice|recommendationservice|checkoutservice|productcatalogservice | corrupt | 7f595b45-181-network |
| aiops2025-6739d066-429-network-loss | regressed_from_hit1 | 1 | 4 | -3.0 | checkoutservice;paymentservice | frontend|cartservice|shippingservice|paymentservice|checkoutservice | loss | 6739d066-429-network |
| aiops2025-80cdc066-374-network-corrupt | regressed_from_hit1 | 1 | 3 | -2.0 | checkoutservice;shippingservice | adservice|frontend|shippingservice|checkoutservice|currencyservice | corrupt | 80cdc066-374-network |
| aiops2025-1d868f8e-347-network-delay | regressed_from_hit1 | 1 | 2 | -1.0 | checkoutservice;frontend | adservice|frontend|checkoutservice|currencyservice|cartservice | delay | 1d868f8e-347-network |
| aiops2025-96fed9c7-427-network-loss | regressed_from_hit1 | 1 | 2 | -1.0 | checkoutservice;paymentservice | frontend|paymentservice|adservice|checkoutservice|shippingservice | loss | 96fed9c7-427-network |
| aiops2025-ad13b37a-146-memory-stress | regressed_from_hit1 | 1 | 2 | -1.0 | recommendationservice | redis-cart|recommendationservice|frontend|productcatalogservice|hipstershop | stress | ad13b37a-146-memory |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
