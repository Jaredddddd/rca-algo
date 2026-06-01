# EvidenceRank V3 Summary

- Created: 2026-06-01T15:30:35+08:00
- Source: `V3`
- Algorithm: `evidencerank`
- Dataset: `rcabench`

## Metrics

| metric | value |
| --- | ---: |
| total | 1422 |
| missing_outputs | 0 |
| AC@1 | 0.559072 |
| AC@3 | 0.789030 |
| AC@5 | 0.888186 |
| MRR | 0.698007 |
| avg_rank | 2.639944 |
| top1_miss | 627 |
| top5_miss | 159 |

## Weak Groups

| group_type | group | cases | AC@1 | AC@3 | AC@5 | MRR | top5_miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fault_type | response-replace-code | 231 | 0.251082 | 0.606061 | 0.805195 | 0.476697 | 45 |
| fault_type | response-abort | 44 | 0.318182 | 0.704545 | 0.840909 | 0.534261 | 7 |
| fault_type | bandwidth | 42 | 0.333333 | 0.571429 | 0.666667 | 0.485018 | 14 |
| time_bucket | ts8 | 25 | 0.360000 | 0.600000 | 0.760000 | 0.540762 | 6 |
| case_service | ts-ui-dashboard | 165 | 0.375758 | 0.690909 | 0.824242 | 0.567628 | 29 |
| time_bucket | ts7 | 34 | 0.382353 | 0.735294 | 0.823529 | 0.579378 | 6 |
| case_service | ts-basic-service | 201 | 0.383085 | 0.671642 | 0.835821 | 0.566122 | 33 |
| fault_type | request-replace-path | 39 | 0.384615 | 0.717949 | 0.871795 | 0.585836 | 5 |
| case_service | ts-travel-plan-service | 72 | 0.388889 | 0.777778 | 0.875000 | 0.603720 | 9 |
| time_bucket | ts6 | 28 | 0.392857 | 0.642857 | 0.928571 | 0.580102 | 2 |
| case_service | ts-route-plan-service | 138 | 0.413043 | 0.623188 | 0.811594 | 0.570370 | 26 |
| fault_type | response-replace-body | 51 | 0.431373 | 0.725490 | 0.862745 | 0.609689 | 7 |
| time_bucket | ts9 | 23 | 0.434783 | 0.695652 | 0.826087 | 0.589191 | 4 |
| fault_type | request-abort | 60 | 0.450000 | 0.833333 | 0.883333 | 0.641466 | 7 |
| time_bucket | ts5 | 258 | 0.465116 | 0.744186 | 0.872093 | 0.629894 | 33 |
| fault_type | request-replace-method | 190 | 0.473684 | 0.689474 | 0.815789 | 0.623310 | 35 |
| case_service | ts-security-service | 33 | 0.484848 | 0.787879 | 0.939394 | 0.644755 | 2 |
| case_service | ts-cancel-service | 4 | 0.500000 | 0.500000 | 0.750000 | 0.571759 | 1 |
| fault_type | response-delay | 89 | 0.505618 | 0.820225 | 0.943820 | 0.685019 | 5 |
| time_bucket | ts4 | 274 | 0.525547 | 0.762774 | 0.901460 | 0.674030 | 27 |

## Hard False Cases

| datapack | gt | best_rank | top5 | fault_type | case_service |
| --- | --- | ---: | --- | --- | --- |
| ts0-ts-travel-plan-service-pod-failure-sxz5ll | ts-travel-plan-service | 35 | ts-auth-service|ts-train-food-service|ts-station-food-service|ts-security-service|ts-payment-service | pod-failure | ts-travel-plan-service |
| ts3-mysql-pod-failure-58qts5 | mysql | 31 | ts-auth-service|ts-seat-service|ts-travel-service|ts-route-plan-service|ts-order-other-service | pod-failure | mysql |
| ts1-ts-consign-service-time-hslmgs | ts-consign-service | 30 | ts-config-service|ts-seat-service|ts-travel-service|ts-order-other-service|ts-order-service | unknown | unknown |
| ts2-ts-cancel-service-return-7qlbbz | ts-cancel-service | 27 | ts-inside-payment-service|ts-travel-service|ts-seat-service|ts-auth-service|ts-basic-service | return | ts-cancel-service |
| ts2-ts-consign-price-service-stress-7r95bt | ts-consign-price-service | 27 | ts-payment-service|ts-preserve-service|ts-security-service|ts-seat-service|ts-ui-dashboard | stress | ts-consign-price-service |
| ts4-ts-food-service-container-kill-lv5htg | ts-config-service | 24 | ts-food-service|ts-ui-dashboard|ts-seat-service|ts-order-service|ts-travel-service | container-kill | ts-food-service |
| ts5-ts-travel-plan-service-response-replace-code-7626tx | ts-route-plan-service;ts-travel-plan-service | 21 | ts-consign-price-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-auth-service | response-replace-code | ts-travel-plan-service |
| ts3-ts-consign-service-bandwidth-pmdbk7 | mysql;ts-consign-service | 20 | ts-ui-dashboard|ts-seat-service|ts-verification-code-service|ts-travel2-service|ts-auth-service | bandwidth | ts-consign-service |
| ts4-ts-inside-payment-service-return-x4gr5r | ts-inside-payment-service | 20 | ts-station-food-service|ts-seat-service|ts-assurance-service|ts-verification-code-service|ts-travel-service | return | ts-inside-payment-service |
| ts2-ts-consign-price-service-container-kill-lj9llf | ts-consign-price-service | 19 | ts-seat-service|ts-basic-service|ts-ui-dashboard|ts-auth-service|ts-order-service | container-kill | ts-consign-price-service |
| ts2-ts-ui-dashboard-response-replace-code-475jm4 | ts-assurance-service;ts-ui-dashboard | 19 | ts-consign-price-service|ts-route-plan-service|ts-station-food-service|ts-travel2-service|ts-order-service | response-replace-code | ts-ui-dashboard |
| ts3-mysql-bandwidth-5xvc22 | mysql;ts-consign-service | 18 | ts-travel-plan-service|ts-route-service|ts-food-service|ts-ui-dashboard|ts-seat-service | bandwidth | mysql |
| ts3-ts-ui-dashboard-request-abort-7z5bcm | ts-preserve-service;ts-ui-dashboard | 18 | ts-seat-service|ts-order-service|ts-travel-service|ts-train-food-service|ts-food-service | request-abort | ts-ui-dashboard |
| ts1-mysql-bandwidth-2xj2mq | mysql;ts-consign-service | 17 | ts-order-service|ts-route-service|ts-ui-dashboard|ts-food-service|ts-preserve-service | bandwidth | mysql |
| ts2-ts-consign-service-partition-xbv84t | mysql;ts-consign-service | 17 | ts-seat-service|ts-ui-dashboard|ts-travel-service|ts-order-service|ts-route-plan-service | partition | ts-consign-service |
| ts4-ts-ui-dashboard-request-replace-method-gbwc6b | ts-assurance-service;ts-ui-dashboard | 17 | ts-seat-service|ts-basic-service|ts-order-service|ts-auth-service|ts-travel-service | request-replace-method | ts-ui-dashboard |
| ts1-ts-food-service-response-patch-body-qjhx5h | ts-food-service;ts-train-food-service | 16 | ts-payment-service|ts-verification-code-service|ts-seat-service|ts-travel-service|ts-order-service | unknown | unknown |
| ts2-mysql-partition-5zrq5z | mysql;ts-contacts-service | 16 | ts-ui-dashboard|ts-seat-service|ts-basic-service|ts-travel-service|ts-order-service | partition | mysql |
| ts9-ts-ui-dashboard-request-abort-vl9sqj | ts-train-service;ts-ui-dashboard | 16 | ts-payment-service|ts-inside-payment-service|ts-verification-code-service|ts-basic-service|ts-order-service | request-abort | ts-ui-dashboard |
| ts6-ts-route-plan-service-response-replace-code-9pfgvr | ts-route-plan-service;ts-route-service | 15 | ts-payment-service|ts-consign-price-service|ts-security-service|ts-consign-service|ts-ui-dashboard | response-replace-code | ts-route-plan-service |
| ts8-ts-food-service-response-replace-code-lsl65n | ts-food-service;ts-station-food-service | 15 | ts-ui-dashboard|ts-seat-service|ts-auth-service|ts-travel-plan-service|ts-travel-service | response-replace-code | ts-food-service |
| ts3-mysql-bandwidth-kpqsfl | mysql;ts-contacts-service | 14 | ts-ui-dashboard|ts-route-plan-service|loadgenerator|ts-seat-service|ts-order-service | bandwidth | mysql |
| ts3-ts-contacts-service-loss-6lcnb9 | mysql;ts-contacts-service | 14 | ts-ui-dashboard|ts-auth-service|ts-seat-service|ts-travel-service|ts-basic-service | loss | ts-contacts-service |
| ts5-ts-food-service-request-replace-path-c4fd88 | ts-food-service;ts-station-food-service | 14 | ts-order-service|ts-seat-service|ts-basic-service|ts-preserve-service|ts-travel-service | request-replace-path | ts-food-service |
| ts4-ts-basic-service-response-replace-code-qh8wkz | ts-basic-service;ts-train-service | 13 | ts-security-service|ts-seat-service|ts-route-plan-service|ts-ui-dashboard|ts-auth-service | response-replace-code | ts-basic-service |
| ts5-ts-food-service-request-replace-method-x5ljcx | ts-food-service;ts-train-food-service | 13 | ts-seat-service|ts-auth-service|ts-travel-plan-service|ts-route-plan-service|ts-ui-dashboard | request-replace-method | ts-food-service |
| ts5-ts-food-service-response-abort-28kwzb | ts-food-service;ts-station-food-service | 13 | ts-consign-service|ts-seat-service|ts-travel-plan-service|ts-auth-service|ts-travel2-service | response-abort | ts-food-service |
| ts5-ts-preserve-service-request-replace-method-gvn4ls | ts-contacts-service;ts-preserve-service | 13 | ts-security-service|ts-ui-dashboard|ts-seat-service|ts-travel2-service|ts-order-other-service | request-replace-method | ts-preserve-service |
| ts5-ts-security-service-request-replace-method-7xn7ks | ts-order-other-service;ts-security-service | 13 | ts-order-service|ts-verification-code-service|ts-seat-service|ts-price-service|ts-food-service | request-replace-method | ts-security-service |
| ts0-ts-station-service-bandwidth-bp5k94 | mysql;ts-station-service | 12 | ts-preserve-service|ts-seat-service|ts-order-service|ts-ui-dashboard|ts-basic-service | bandwidth | ts-station-service |

## Research Notes

- V3 fixed part of the propagation/volume dominance problem: topology degree is no longer positive root evidence, and family weights prevent metric/log magnitude from overwhelming trace-path evidence.
- Remaining weak groups still include `response-replace-code`, `response-abort`, `bandwidth`, `request-replace-path`, and services that sit near user-facing or route-planning paths. These look like endpoint-symptom and topology-direction ambiguity rather than missing scalar weights.
- The main regression pattern is central true roots in request/response mutation and a small number of pod-failure cases. A uniform degree penalty is too blunt for those roots.
- Next reusable direction: neighbor contrast that compares a service's self anomaly to upstream/downstream anomaly, with no `conclusion.parquet` reading and no service/fault-specific branches.
