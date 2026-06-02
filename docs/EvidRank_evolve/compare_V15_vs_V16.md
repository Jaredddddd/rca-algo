# EvidenceRank Compare V15 vs V16

- Created: 2026-06-02T18:45:17+08:00
- Old: `V15`
- New: `V16`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.638537 | 0.583685 | -0.054852 |
| AC@3 | 0.884669 | 0.877637 | -0.007032 |
| AC@5 | 0.949367 | 0.945851 | -0.003516 |
| MRR | 0.772135 | 0.739592 | -0.032542 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 82 |
| rank_improved | 108 |
| rank_regressed | 118 |
| regressed_from_hit1 | 160 |
| unchanged | 954 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-auth-service-stress-nlpsfx | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-consign-service|ts-config-service | stress | ts-auth-service |
| ts0-ts-basic-service-request-delay-d5jvr6 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-travel2-service|ts-route-plan-service | request-delay | ts-basic-service |
| ts0-ts-inside-payment-service-stress-5qd9rl | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-payment-service|loadgenerator|ts-assurance-service | stress | ts-inside-payment-service |
| ts0-ts-price-service-stress-n787pd | improved_to_hit1 | 2 | 1 | 1.0 | ts-price-service | ts-price-service|ts-basic-service|ts-travel2-service|ts-station-service|ts-travel-service | stress | ts-price-service |
| ts0-ts-route-service-container-kill-tsqgmn | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service | ts-route-service|ts-ui-dashboard|ts-payment-service|loadgenerator|ts-verification-code-service | container-kill | ts-route-service |
| ts0-ts-travel-plan-service-response-replace-body-mns47j | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|loadgenerator|ts-route-plan-service | response-replace-body | ts-travel-plan-service |
| ts0-ts-user-service-pod-failure-b44c7f | improved_to_hit1 | 2 | 1 | 1.0 | ts-user-service | ts-user-service|ts-ui-dashboard|loadgenerator|ts-travel-service|ts-preserve-service | pod-failure | ts-user-service |
| ts1-ts-inside-payment-service-stress-n6mttx | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|loadgenerator|ts-ui-dashboard|ts-consign-price-service|ts-travel-service | stress | ts-inside-payment-service |
| ts1-ts-order-other-service-exception-twstdp | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-security-service|ts-preserve-service|ts-order-service|loadgenerator | exception | ts-order-other-service |
| ts1-ts-order-service-exception-b25hld | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-assurance-service|loadgenerator|ts-ui-dashboard|ts-travel-service | exception | ts-order-service |
| ts1-ts-order-service-exception-fvcrfk | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-preserve-service|loadgenerator|ts-contacts-service|ts-travel-service | exception | ts-order-service |
| ts1-ts-preserve-service-request-abort-x7w9vv | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-security-service|ts-ui-dashboard|loadgenerator|ts-contacts-service | request-abort | ts-preserve-service |
| ts1-ts-route-plan-service-exception-jc7cxv | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-voucher-service|loadgenerator | exception | ts-route-plan-service |
| ts1-ts-route-plan-service-request-replace-method-bn6rxm | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-station-food-service|ts-assurance-service|ts-payment-service | request-replace-method | ts-route-plan-service |
| ts1-ts-route-plan-service-response-replace-code-cqhtpj | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-consign-price-service|ts-travel2-service|ts-price-service | response-replace-code | ts-route-plan-service |
| ts1-ts-route-plan-service-return-2cvc6m | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service | ts-route-plan-service|ts-travel-plan-service|ts-config-service|loadgenerator|ts-route-service | return | ts-route-plan-service |
| ts2-ts-consign-price-service-container-kill-lj9llf | improved_to_hit1 | 2 | 1 | 1.0 | ts-consign-price-service | ts-consign-price-service|ts-consign-service|ts-route-service|ts-train-service|ts-ui-dashboard | container-kill | ts-consign-price-service |
| ts2-ts-consign-service-bandwidth-x9qdzm | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-consign-service | ts-consign-service|ts-ui-dashboard|ts-payment-service|ts-seat-service|loadgenerator | bandwidth | ts-consign-service |
| ts2-ts-food-service-container-kill-jhdf8g | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-preserve-service|ts-order-other-service | container-kill | ts-food-service |
| ts2-ts-food-service-request-replace-method-nfkxm7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-travel-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-train-food-service|ts-basic-service | request-replace-method | ts-food-service |
| ts2-ts-food-service-response-abort-5k6q44 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-train-food-service | ts-food-service|loadgenerator|ts-ui-dashboard|ts-train-food-service|ts-config-service | response-abort | ts-food-service |
| ts2-ts-order-other-service-container-kill-48rlds | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service | ts-order-other-service|ts-travel2-service|ts-seat-service|loadgenerator|ts-execute-service | container-kill | ts-order-other-service |
| ts2-ts-order-service-stress-4hmp6r | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-travel-service|ts-preserve-service|ts-ui-dashboard | stress | ts-order-service |
| ts2-ts-order-service-stress-6bfkzb | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-ui-dashboard|loadgenerator|ts-route-service|ts-travel2-service | stress | ts-order-service |
| ts2-ts-order-service-stress-8vtw2p | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-travel-service|ts-travel-plan-service|loadgenerator | stress | ts-order-service |
| ts2-ts-order-service-stress-967z6d | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service | ts-order-service|ts-seat-service|ts-travel-service|ts-train-service|ts-ui-dashboard | stress | ts-order-service |
| ts2-ts-preserve-service-request-replace-method-nsz4x4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-seat-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-contacts-service | request-replace-method | ts-preserve-service |
| ts2-ts-preserve-service-response-replace-code-bk2689 | improved_to_hit1 | 2 | 1 | 1.0 | ts-contacts-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-contacts-service|ts-security-service | response-replace-code | ts-preserve-service |
| ts2-ts-route-plan-service-request-abort-l264j8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-route-service|loadgenerator | request-abort | ts-route-plan-service |
| ts2-ts-route-plan-service-response-replace-body-t6687x | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-price-service|ts-ui-dashboard|ts-route-service | response-replace-body | ts-route-plan-service |
| ts2-ts-seat-service-request-abort-qk6ntt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-seat-service | ts-seat-service|ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service | request-abort | ts-seat-service |
| ts2-ts-travel-plan-service-request-replace-method-p8lnll | improved_to_hit1 | 2 | 1 | 1.0 | ts-seat-service;ts-travel-plan-service | ts-travel-plan-service|ts-ui-dashboard|loadgenerator|ts-route-plan-service|ts-route-service | request-replace-method | ts-travel-plan-service |
| ts2-ts-travel-service-stress-7bcpcw | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-service | ts-travel-service|ts-route-plan-service|ts-ui-dashboard|ts-order-service|loadgenerator | stress | ts-travel-service |
| ts3-ts-cancel-service-stress-pf77h8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-cancel-service | ts-cancel-service|ts-consign-service|ts-ui-dashboard|ts-travel-service|ts-train-food-service | stress | ts-cancel-service |
| ts3-ts-config-service-stress-8nszx2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-config-service | ts-config-service|ts-seat-service|ts-consign-service|ts-travel2-service|loadgenerator | stress | ts-config-service |
| ts3-ts-food-service-request-replace-method-p4xjxp | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-station-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-route-service|ts-verification-code-service | request-replace-method | ts-food-service |
| ts3-ts-food-service-response-replace-body-nc7tfj | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-train-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-order-service|ts-train-food-service | response-replace-body | ts-food-service |
| ts3-ts-food-service-stress-tjvdb5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service | ts-food-service|ts-ui-dashboard|loadgenerator|ts-route-service|ts-train-food-service | stress | ts-food-service |
| ts3-ts-inside-payment-service-stress-tj2rtz | improved_to_hit1 | 2 | 1 | 1.0 | ts-inside-payment-service | ts-inside-payment-service|ts-ui-dashboard|ts-payment-service|loadgenerator|ts-station-food-service | stress | ts-inside-payment-service |
| ts3-ts-preserve-service-request-replace-method-msns6h | improved_to_hit1 | 2 | 1 | 1.0 | ts-preserve-service;ts-travel-service | ts-preserve-service|ts-ui-dashboard|loadgenerator|ts-basic-service|ts-order-service | request-replace-method | ts-preserve-service |

## Decision Notes

- Explain whether the new version should be accepted.
- Pay special attention to `regressed_from_hit1` cases.
- If accepted, record the general mechanism that improved the ranking.
