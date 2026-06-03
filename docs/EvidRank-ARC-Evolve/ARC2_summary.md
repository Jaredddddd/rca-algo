# EvidenceRank ARC2 Summary

- Created: 2026-06-03T17:13:02+08:00
- Source: `ARC2`
- Algorithm: `evidencerank_arc`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.720113 |
| AC@3 | 0.940928 |
| AC@5 | 0.973277 |
| MRR | 0.832050 |
| avg_rank | 1.672996 |
| top1_miss | 398 |
| top5_miss | 38 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.500000 | 0.833333 | 0.875000 | 0.679690 | 3 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.526495 | 2 |
| time_bucket | ts9 | 23 | 0.521739 | 0.869565 | 0.956522 | 0.705556 | 1 |
| case_service | ts-basic-service | 201 | 0.527363 | 0.885572 | 0.950249 | 0.701476 | 10 |
| fault_type | response-replace-body | 51 | 0.529412 | 0.862745 | 0.921569 | 0.709322 | 4 |
| fault_type | request-replace-path | 39 | 0.564103 | 0.871795 | 0.974359 | 0.735684 | 1 |
| time_bucket | ts6 | 28 | 0.571429 | 0.785714 | 0.964286 | 0.705952 | 1 |
| fault_type | response-replace-code | 231 | 0.575758 | 0.926407 | 0.978355 | 0.749635 | 5 |
| fault_type | request-replace-method | 190 | 0.578947 | 0.926316 | 0.973684 | 0.750332 | 5 |
| time_bucket | ts7 | 34 | 0.588235 | 0.852941 | 0.911765 | 0.737045 | 3 |
| case_service | unknown | 26 | 0.615385 | 0.807692 | 0.923077 | 0.737651 | 2 |
| fault_type | unknown | 26 | 0.615385 | 0.807692 | 0.923077 | 0.737651 | 2 |
| case_service | ts-travel2-service | 68 | 0.632353 | 0.911765 | 0.970588 | 0.773588 | 2 |
| fault_type | response-abort | 44 | 0.659091 | 0.909091 | 0.977273 | 0.792424 | 1 |
| case_service | ts-travel-service | 92 | 0.663043 | 0.934783 | 0.989130 | 0.808333 | 1 |
| case_service | ts-route-plan-service | 138 | 0.666667 | 0.927536 | 0.971014 | 0.798760 | 4 |
| fault_type | bandwidth | 42 | 0.666667 | 0.880952 | 0.880952 | 0.778283 | 5 |
| case_service | ts-security-service | 33 | 0.666667 | 0.969697 | 1.000000 | 0.820707 | 0 |
| case_service | ts-payment-service | 12 | 0.666667 | 1.000000 | 1.000000 | 0.833333 | 0 |
| case_service | ts-consign-price-service | 9 | 0.666667 | 1.000000 | 1.000000 | 0.833333 | 0 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-ui-dashboard|ts-consign-service|ts-verification-code-service|ts-auth-service|ts-user-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|ts-food-service|ts-route-plan-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 29 | ts-food-service|ts-travel-service|ts-config-service|ts-order-service|ts-order-other-service | unknown | unknown |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 29 | ts-food-service|ts-seat-service|ts-ui-dashboard|loadgenerator|ts-preserve-service | container-kill | ts-food-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 23 | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-order-service|ts-assurance-service | return | ts-cancel-service |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 19 | ts-ui-dashboard|ts-seat-service|ts-auth-service|ts-order-service|ts-order-other-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 16 | ts-payment-service|ts-preserve-service|ts-ui-dashboard|ts-seat-service|loadgenerator | response-replace-code | ts-basic-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 16 | ts-consign-service|ts-food-service|ts-basic-service|ts-route-plan-service|loadgenerator | stress | ts-cancel-service |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 13 | ts-ui-dashboard|loadgenerator|ts-seat-service|ts-food-service|ts-auth-service | bandwidth | ts-basic-service |
| ts5-ts-ui-dashboard-request-abort-kp8d9p | ts-order-other-service;ts-ui-dashboard | 13 | loadgenerator|ts-seat-service|ts-station-food-service|ts-travel2-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-body-jbn747 | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-food-service | response-replace-body | ts-basic-service |
| ts5-ts-basic-service-request-replace-method-c7p9qz | ts-basic-service;ts-price-service | 11 | ts-payment-service|ts-inside-payment-service|ts-consign-price-service|ts-ui-dashboard|ts-route-plan-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-response-replace-code-znlfxx | ts-basic-service;ts-price-service | 11 | ts-preserve-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 10 | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|ts-travel2-service | container-kill | mysql |
| ts4-ts-station-service-bandwidth-nfljv5 | ts-basic-service;ts-station-service | 10 | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service | bandwidth | ts-station-service |
| ts1-ts-seat-service-partition-gtmt4k | ts-seat-service;ts-travel2-service | 9 | ts-order-service|ts-ui-dashboard|ts-consign-price-service|ts-travel-plan-service|ts-inside-payment-service | partition | ts-seat-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 9 | ts-travel-service|ts-security-service|ts-order-service|ts-auth-service|ts-preserve-service | unknown | unknown |
| ts4-ts-ui-dashboard-request-replace-method-npqtdz | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-seat-service|ts-travel2-service|ts-route-plan-service|ts-consign-service|ts-basic-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-travel2-service-response-replace-code-9bzkqw | ts-basic-service;ts-travel2-service | 9 | ts-seat-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard|ts-preserve-service | response-replace-code | ts-travel2-service |
| ts8-ts-ui-dashboard-request-replace-method-xlwbzw | ts-travel-plan-service;ts-ui-dashboard | 9 | ts-payment-service|ts-food-service|ts-consign-service|ts-seat-service|ts-cancel-service | request-replace-method | ts-ui-dashboard |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 9 | ts-payment-service|ts-inside-payment-service|ts-food-service|ts-assurance-service|ts-basic-service | request-abort | ts-ui-dashboard |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 8 | ts-train-food-service|ts-food-service|ts-travel-service|ts-seat-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 8 | ts-route-plan-service|ts-security-service|ts-travel-plan-service|ts-ui-dashboard|ts-seat-service | response-replace-code | ts-basic-service |
| ts4-ts-route-plan-service-bandwidth-q5lcsx | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|loadgenerator|ts-food-service|ts-seat-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-request-replace-method-vqxbgx | ts-basic-service;ts-price-service | 8 | ts-preserve-service|ts-cancel-service|ts-order-service|ts-seat-service|ts-food-service | request-replace-method | ts-basic-service |
| ts5-ts-basic-service-request-replace-path-f7qjfw | ts-basic-service;ts-price-service | 8 | ts-cancel-service|ts-preserve-service|ts-seat-service|ts-consign-price-service|ts-travel-service | request-replace-path | ts-basic-service |
| ts5-ts-ui-dashboard-request-replace-method-dxffln | ts-travel-plan-service;ts-ui-dashboard | 8 | ts-payment-service|ts-basic-service|loadgenerator|ts-security-service|ts-travel2-service | request-replace-method | ts-ui-dashboard |
| ts7-ts-route-plan-service-response-replace-body-g2tfl4 | ts-route-plan-service;ts-travel-service | 8 | ts-ui-dashboard|ts-food-service|ts-payment-service|ts-basic-service|loadgenerator | response-replace-body | ts-route-plan-service |
| ts7-ts-ui-dashboard-request-abort-mwkzh7 | ts-food-service;ts-ui-dashboard | 8 | ts-order-service|ts-seat-service|ts-basic-service|ts-contacts-service|ts-consign-service | request-abort | ts-ui-dashboard |
| ts3-ts-basic-service-response-replace-code-ws6vpb | ts-basic-service;ts-station-service | 7 | ts-preserve-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |

## Research Notes

- ARC2 improves ARC1 by treating local family evidence (`metric + mutation + log`) as a bounded counterweight to high-volume propagation evidence.
- The update is still unsupervised: it uses only current-case p95 family normalization, single-case median family reliability, and trace-derived feature families.
- The largest gains are protocol mutation and pod-failure rank-2 misses where ARC1 already saw the GT service but let a propagation-heavy neighbor stay first.
- Remaining hard cases include sparse infrastructure roots and delay/partition-like faults where propagation-shaped evidence can be the true root signature.
