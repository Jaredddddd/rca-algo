# EvidenceRank FW_PRIORITY_LINEAR_0_7 Summary

- Created: 2026-06-03T23:32:35+08:00
- Source: `current`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.671589 |
| AC@3 | 0.886076 |
| AC@5 | 0.945148 |
| MRR | 0.789295 |
| avg_rank | 2.039381 |
| top1_miss | 467 |
| top5_miss | 78 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | pod-failure | 24 | 0.125000 | 0.208333 | 0.375000 | 0.237633 | 15 |
| fault_type | response-replace-code | 231 | 0.329004 | 0.783550 | 0.904762 | 0.579046 | 22 |
| fault_type | request-replace-path | 39 | 0.358974 | 0.794872 | 0.948718 | 0.581624 | 2 |
| fault_type | response-replace-body | 51 | 0.392157 | 0.745098 | 0.882353 | 0.588936 | 6 |
| fault_type | request-abort | 60 | 0.400000 | 0.833333 | 0.916667 | 0.623089 | 5 |
| case_service | ts-basic-service | 201 | 0.402985 | 0.746269 | 0.910448 | 0.595957 | 18 |
| time_bucket | ts6 | 28 | 0.464286 | 0.785714 | 0.821429 | 0.637021 | 5 |
| time_bucket | ts7 | 34 | 0.470588 | 0.705882 | 0.852941 | 0.629835 | 5 |
| fault_type | response-abort | 44 | 0.477273 | 0.863636 | 0.954545 | 0.683333 | 2 |
| time_bucket | ts8 | 25 | 0.480000 | 0.760000 | 0.880000 | 0.646286 | 3 |
| fault_type | request-replace-method | 190 | 0.489474 | 0.805263 | 0.931579 | 0.670428 | 13 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.500000 | 0.518188 | 2 |
| time_bucket | ts9 | 23 | 0.521739 | 0.695652 | 0.782609 | 0.647483 | 5 |
| case_service | ts-consign-price-service | 9 | 0.555556 | 0.777778 | 0.888889 | 0.693720 | 1 |
| case_service | ts-ui-dashboard | 165 | 0.563636 | 0.818182 | 0.903030 | 0.711761 | 16 |
| case_service | ts-route-plan-service | 138 | 0.579710 | 0.847826 | 0.913043 | 0.733866 | 12 |
| case_service | ts-travel2-service | 68 | 0.602941 | 0.911765 | 0.955882 | 0.767437 | 3 |
| case_service | ts-security-service | 33 | 0.606061 | 0.969697 | 1.000000 | 0.795455 | 0 |
| time_bucket | ts1 | 179 | 0.620112 | 0.905028 | 0.966480 | 0.767809 | 6 |
| time_bucket | ts3 | 210 | 0.642857 | 0.914286 | 0.966667 | 0.777759 | 7 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 33 | ts-auth-service|ts-train-food-service|ts-station-food-service|ts-security-service|ts-route-service | pod-failure | ts-travel-plan-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 31 | ts-config-service|ts-travel-service|ts-seat-service|ts-order-other-service|ts-order-service | unknown | unknown |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-travel-service|ts-seat-service|loadgenerator|ts-order-other-service | pod-failure | mysql |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 28 | ts-inside-payment-service|ts-ui-dashboard|loadgenerator|ts-station-service|ts-travel-service | return | ts-cancel-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 27 | ts-inside-payment-service|ts-order-other-service|ts-order-service|ts-ui-dashboard|ts-seat-service | pod-failure | ts-payment-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 27 | ts-consign-service|ts-food-service|ts-auth-service|ts-route-plan-service|loadgenerator | stress | ts-cancel-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 25 | ts-food-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-order-service | container-kill | ts-food-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | ts-consign-price-service | 23 | ts-consign-service|ts-ui-dashboard|ts-preserve-service|loadgenerator|ts-seat-service | pod-failure | ts-consign-price-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 21 | ts-travel-service|ts-station-service|ts-basic-service|ts-ui-dashboard|ts-seat-service | pod-failure | ts-assurance-service |
| ts8-ts-food-service-pod-failure-9swgtb | ts-food-service | 21 | ts-order-service|ts-station-service|ts-route-service|ts-seat-service|ts-basic-service | pod-failure | ts-food-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 20 | ts-travel-service|ts-basic-service|ts-ui-dashboard|ts-seat-service|ts-order-other-service | pod-failure | ts-consign-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | ts-station-food-service | 18 | ts-food-service|loadgenerator|ts-ui-dashboard|ts-travel-service|ts-basic-service | pod-failure | ts-station-food-service |
| ts0-mysql-container-kill-9t6n24 | mysql | 17 | ts-train-service|ts-auth-service|ts-ui-dashboard|ts-verification-code-service|loadgenerator | container-kill | mysql |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 17 | ts-ui-dashboard|loadgenerator|ts-travel2-service|ts-seat-service|ts-route-service | response-replace-code | ts-travel-plan-service |
| ts6-ts-route-plan-service-pod-failure-n576ft | ts-route-plan-service | 17 | ts-payment-service|ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-order-other-service | pod-failure | ts-route-plan-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 17 | ts-basic-service|ts-travel-service|ts-travel2-service|ts-travel-plan-service|ts-order-other-service | pod-failure | ts-price-service |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 15 | ts-consign-service|ts-order-service|ts-travel-service|ts-seat-service|ts-basic-service | unknown | unknown |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 15 | ts-order-service|loadgenerator|ts-seat-service|ts-food-service|ts-train-food-service | request-abort | ts-ui-dashboard |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service;ts-travel-plan-service | 15 | ts-ui-dashboard|ts-order-service|ts-seat-service|ts-contacts-service|ts-verification-code-service | bandwidth | ts-route-plan-service |
| ts5-ts-basic-service-response-replace-code-4b7fbz | ts-basic-service;ts-price-service | 15 | ts-payment-service|ts-ui-dashboard|loadgenerator|ts-train-food-service|ts-preserve-service | response-replace-code | ts-basic-service |
| ts2-mysql-pod-kill-xvzmxb | mysql | 14 | ts-travel-service|ts-security-service|ts-auth-service|ts-preserve-service|ts-order-service | unknown | unknown |
| ts2-ts-travel2-service-pod-failure-p8j6xr | ts-travel2-service | 12 | ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-travel-service|loadgenerator | pod-failure | ts-travel2-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 12 | ts-basic-service|ts-consign-service|ts-train-service|ts-route-service|ts-seat-service | request-replace-method | ts-ui-dashboard |
| ts5-ts-travel-plan-service-response-replace-code-k8hf8v | ts-route-plan-service;ts-travel-plan-service | 12 | ts-ui-dashboard|ts-consign-price-service|ts-seat-service|ts-basic-service|ts-travel-service | response-replace-code | ts-travel-plan-service |
| ts6-ts-route-plan-service-response-replace-code-9pfgvr | ts-route-plan-service;ts-route-service | 12 | ts-payment-service|ts-ui-dashboard|ts-consign-service|ts-security-service|ts-travel-service | response-replace-code | ts-route-plan-service |
| ts9-ts-preserve-service-pod-failure-6w29wr | ts-preserve-service | 12 | ts-order-service|loadgenerator|ts-verification-code-service|ts-inside-payment-service|ts-ui-dashboard | pod-failure | ts-preserve-service |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 11 | ts-payment-service|ts-inside-payment-service|ts-assurance-service|ts-order-service|ts-verification-code-service | request-abort | ts-ui-dashboard |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 10 | ts-preserve-service|ts-consign-service|ts-ui-dashboard|ts-seat-service|ts-order-service | bandwidth | ts-station-service |
| ts2-ts-ui-dashboard-request-replace-method-xfx4x5 | ts-food-service;ts-ui-dashboard | 10 | ts-order-service|ts-seat-service|ts-travel-service|ts-basic-service|loadgenerator | request-replace-method | ts-ui-dashboard |
| ts4-ts-basic-service-bandwidth-fn4pnv | ts-basic-service;ts-preserve-service | 10 | ts-ui-dashboard|ts-contacts-service|loadgenerator|ts-order-service|ts-seat-service | bandwidth | ts-basic-service |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
