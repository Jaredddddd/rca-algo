# EvidenceRank V1 Summary

- Created: 2026-06-01T14:00:24+08:00
- Source: `V1`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.530239 |
| AC@3 | 0.778481 |
| AC@5 | 0.877637 |
| MRR | 0.679202 |
| avg_rank | 3.133615 |
| top1_miss | 668 |
| top5_miss | 174 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | bandwidth | 42 | 0.238095 | 0.523810 | 0.714286 | 0.416129 | 12 |
| fault_type | response-replace-code | 231 | 0.264069 | 0.606061 | 0.822511 | 0.487916 | 41 |
| time_bucket | ts8 | 25 | 0.280000 | 0.560000 | 0.760000 | 0.486051 | 6 |
| fault_type | response-abort | 44 | 0.318182 | 0.704545 | 0.863636 | 0.546051 | 6 |
| time_bucket | ts6 | 28 | 0.321429 | 0.642857 | 0.892857 | 0.528753 | 3 |
| time_bucket | ts7 | 34 | 0.323529 | 0.705882 | 0.794118 | 0.542928 | 7 |
| case_service | ts-travel-plan-service | 72 | 0.361111 | 0.763889 | 0.888889 | 0.592168 | 8 |
| case_service | mysql | 72 | 0.375000 | 0.625000 | 0.680556 | 0.522508 | 23 |
| time_bucket | ts9 | 23 | 0.391304 | 0.652174 | 0.782609 | 0.550699 | 5 |
| case_service | ts-ui-dashboard | 165 | 0.393939 | 0.684848 | 0.842424 | 0.583131 | 26 |
| case_service | ts-route-plan-service | 138 | 0.398551 | 0.594203 | 0.789855 | 0.555369 | 29 |
| fault_type | request-replace-path | 39 | 0.410256 | 0.769231 | 0.871795 | 0.610073 | 5 |
| time_bucket | ts5 | 258 | 0.410853 | 0.717054 | 0.837209 | 0.597737 | 42 |
| fault_type | corrupt | 46 | 0.413043 | 0.760870 | 0.804348 | 0.609406 | 9 |
| fault_type | pod-failure | 24 | 0.416667 | 0.416667 | 0.416667 | 0.433073 | 14 |
| case_service | ts-basic-service | 201 | 0.417910 | 0.711443 | 0.850746 | 0.600097 | 30 |
| case_service | ts-security-service | 33 | 0.424242 | 0.727273 | 0.939394 | 0.608310 | 2 |
| fault_type | loss | 48 | 0.458333 | 0.812500 | 0.854167 | 0.640500 | 7 |
| case_service | ts-food-service | 54 | 0.462963 | 0.759259 | 0.796296 | 0.629116 | 11 |
| fault_type | request-replace-method | 190 | 0.463158 | 0.715789 | 0.821053 | 0.628277 | 34 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-user-service-pod-failure-b44c7f | ts-user-service | 47 | ts-auth-service|ts-verification-code-service|ts-delivery-service|loadgenerator|mysql | pod-failure | ts-user-service |
| ts2-ts-travel-service-pod-failure-jqk2bj | ts-travel-service | 47 | ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-seat-service|ts-verification-code-service | pod-failure | ts-travel-service |
| ts2-ts-travel2-service-pod-failure-p8j6xr | ts-travel2-service | 47 | ts-ui-dashboard|ts-price-service|ts-travel-plan-service|ts-seat-service|ts-basic-service | pod-failure | ts-travel2-service |
| ts6-ts-route-plan-service-pod-failure-n576ft | ts-route-plan-service | 46 | ts-payment-service|ts-seat-service|ts-ui-dashboard|ts-basic-service|ts-verification-code-service | pod-failure | ts-route-plan-service |
| ts1-ts-station-food-service-pod-failure-td2qj4 | ts-station-food-service | 45 | ts-travel-service|ts-food-service|ts-order-other-service|ts-basic-service|ts-verification-code-service | pod-failure | ts-station-food-service |
| ts7-ts-price-service-pod-failure-vg4fh6 | ts-price-service | 45 | ts-seat-service|ts-travel-service|ts-basic-service|ts-order-other-service|ts-order-service | pod-failure | ts-price-service |
| ts9-ts-preserve-service-pod-failure-6w29wr | ts-preserve-service | 44 | ts-seat-service|ts-basic-service|ts-ui-dashboard|ts-verification-code-service|ts-order-service | pod-failure | ts-preserve-service |
| ts3-ts-payment-service-pod-failure-fnlgp6 | ts-payment-service | 43 | ts-inside-payment-service|ts-order-other-service|ts-seat-service|ts-route-plan-service|ts-basic-service | pod-failure | ts-payment-service |
| ts2-ts-consign-price-service-container-kill-lj9llf | ts-consign-price-service | 39 | ts-seat-service|ts-basic-service|ts-ui-dashboard|ts-verification-code-service|ts-order-service | container-kill | ts-consign-price-service |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 38 | ts-config-service|ts-seat-service|ts-travel-service|ts-order-other-service|ts-basic-service | unknown | unknown |
| ts2-ts-consign-price-service-stress-7r95bt | ts-consign-price-service | 38 | ts-preserve-service|ts-security-service|ts-seat-service|ts-ui-dashboard|ts-consign-service | stress | ts-consign-price-service |
| ts3-ts-consign-price-service-pod-failure-bfznw7 | ts-consign-price-service | 38 | ts-preserve-service|ts-consign-service|ts-ui-dashboard|ts-seat-service|ts-verification-code-service | pod-failure | ts-consign-price-service |
| ts5-ts-cancel-service-stress-d8xbsn | ts-cancel-service | 38 | ts-consign-service|ts-station-food-service|ts-basic-service|ts-route-plan-service|ts-auth-service | stress | ts-cancel-service |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 37 | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-basic-service|ts-auth-service | return | ts-cancel-service |
| ts3-ts-consign-service-pod-failure-8cb7mp | ts-consign-service | 37 | ts-travel-service|ts-seat-service|ts-basic-service|ts-order-other-service|ts-travel-plan-service | pod-failure | ts-consign-service |
| ts8-ts-food-service-pod-failure-9swgtb | ts-food-service | 37 | ts-seat-service|ts-order-service|ts-ui-dashboard|ts-travel-service|ts-basic-service | pod-failure | ts-food-service |
| ts2-ts-assurance-service-pod-failure-fvnkqg | ts-assurance-service | 31 | ts-route-plan-service|ts-seat-service|ts-basic-service|ts-travel-service|ts-travel-plan-service | pod-failure | ts-assurance-service |
| ts2-ts-consign-service-partition-xbv84t | mysql;ts-consign-service | 27 | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-order-service|ts-route-plan-service | partition | ts-consign-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 26 | ts-auth-service|ts-seat-service|ts-travel-service|ts-route-plan-service|ts-basic-service | pod-failure | mysql |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 25 | ts-food-service|ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-order-service | container-kill | ts-food-service |
| ts1-mysql-partition-gcgbzp | mysql;ts-order-service | 22 | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-travel-plan-service|ts-route-plan-service | partition | mysql |
| ts2-ts-order-service-loss-lp8wln | mysql;ts-order-service | 20 | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-travel-plan-service|ts-route-plan-service | loss | ts-order-service |
| ts0-mysql-partition-cfvlsw | mysql;ts-travel2-service | 19 | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-verification-code-service|ts-travel-service | partition | mysql |
| ts2-mysql-loss-4fvjb6 | mysql;ts-order-other-service | 19 | ts-preserve-service|ts-travel2-service|ts-security-service|ts-ui-dashboard|ts-travel-service | loss | mysql |
| ts3-mysql-partition-4hh8bj | mysql;ts-travel-service | 19 | ts-travel-plan-service|ts-ui-dashboard|ts-route-plan-service|ts-seat-service|ts-order-service | partition | mysql |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 19 | ts-seat-service|ts-order-service|ts-travel-service|ts-basic-service|ts-food-service | request-abort | ts-ui-dashboard |
| ts4-ts-inside-payment-service-return-x4gr5r | ts-inside-payment-service | 19 | ts-assurance-service|ts-station-food-service|ts-seat-service|ts-verification-code-service|ts-travel-service | return | ts-inside-payment-service |
| ts2-mysql-bandwidth-fws9rx | mysql;ts-travel2-service | 18 | ts-ui-dashboard|ts-travel-plan-service|ts-route-plan-service|ts-verification-code-service|ts-travel-service | bandwidth | mysql |
| ts2-mysql-partition-5zrq5z | mysql;ts-contacts-service | 18 | ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-travel-service|ts-order-service | partition | mysql |
| ts3-mysql-corrupt-wgvhdb | mysql;ts-config-service | 18 | ts-seat-service|ts-travel-service|ts-travel2-service|ts-route-service|ts-ui-dashboard | corrupt | mysql |

## Research Notes

- Write the suspected general failure mechanism here.
- Do not add case/service/fault hardcoding to the algorithm.
- Convert observations into a reusable signal, normalization, topology rule, or rank fusion idea.
