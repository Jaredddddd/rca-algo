# Compare CREST10_DEFAULT vs CREST10_VICTIM_SUPPRESSION

## Overall Metrics

| metric | old `crest` | new `crest_victim_suppression` | delta |
| --- | ---: | ---: | ---: |
| total | 1422 | 1422 | 0 |
| error | 0 | 0 | 0 |
| AC@1 | 0.800281 | 0.757384 | -0.042897 |
| MRR | 0.875326 | 0.841618 | -0.033708 |
| AC@3 | 0.944444 | 0.917018 | -0.027426 |
| AC@5 | 0.971871 | 0.950070 | -0.021800 |

## Change Counts

- `improved_to_hit1`: 24
- `regressed_from_hit1`: 85
- `rank_improved`: 41
- `rank_regressed`: 46
- `unchanged`: 1226

## Hit@1 Changes By Fault Type

| change_type | fault_type | count |
| --- | --- | --- |
| improved_to_hit1 | response-replace-code | 9 |
| improved_to_hit1 | request-replace-method | 5 |
| improved_to_hit1 | delay | 3 |
| improved_to_hit1 | request-replace-path | 2 |
| improved_to_hit1 | stress | 2 |
| improved_to_hit1 | corrupt | 1 |
| improved_to_hit1 | loss | 1 |
| improved_to_hit1 | response-abort | 1 |
| regressed_from_hit1 | response-delay | 16 |
| regressed_from_hit1 | loss | 13 |
| regressed_from_hit1 | partition | 13 |
| regressed_from_hit1 | request-delay | 13 |
| regressed_from_hit1 | corrupt | 8 |
| regressed_from_hit1 | request-replace-method | 8 |
| regressed_from_hit1 | bandwidth | 3 |
| regressed_from_hit1 | delay | 3 |
| regressed_from_hit1 | response-replace-code | 3 |
| regressed_from_hit1 | container-kill | 2 |
| regressed_from_hit1 | stress | 2 |
| regressed_from_hit1 | request-abort | 1 |

## Improved To Hit@1

| datapack | gt | fault_type | top1_old | top1_new | best_rank_old | best_rank_new | rank_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ts2-ts-basic-service-response-replace-code-qf2qml | ts-basic-service;ts-price-service | response-replace-code | ts-travel-service | ts-basic-service | 3 | 1 | -2 |
| ts3-ts-ui-dashboard-request-replace-method-wkh6t7 | ts-travel-plan-service;ts-ui-dashboard | request-replace-method | ts-basic-service | ts-travel-plan-service | 3 | 1 | -2 |
| ts1-ts-basic-service-request-replace-method-2b57wf | ts-basic-service;ts-price-service | request-replace-method | ts-travel-service | ts-basic-service | 2 | 1 | -1 |
| ts1-ts-seat-service-response-replace-code-dk84t5 | ts-order-service;ts-seat-service | response-replace-code | ts-travel-service | ts-seat-service | 2 | 1 | -1 |
| ts2-mysql-delay-d427wn | mysql;ts-route-service | delay | ts-ui-dashboard | ts-route-service | 2 | 1 | -1 |
| ts2-ts-basic-service-response-replace-code-92j5cs | ts-basic-service;ts-train-service | response-replace-code | ts-travel2-service | ts-basic-service | 2 | 1 | -1 |
| ts2-ts-travel-service-request-replace-method-5snzk5 | ts-route-service;ts-travel-service | request-replace-method | ts-food-service | ts-travel-service | 2 | 1 | -1 |
| ts2-ts-ui-dashboard-request-replace-method-jrt2mv | ts-train-service;ts-ui-dashboard | request-replace-method | ts-seat-service | ts-train-service | 2 | 1 | -1 |
| ts3-mysql-corrupt-4kplqx | mysql;ts-travel2-service | corrupt | ts-ui-dashboard | ts-travel2-service | 2 | 1 | -1 |
| ts3-ts-basic-service-response-replace-code-bvqv9z | ts-basic-service;ts-station-service | response-replace-code | ts-travel2-service | ts-basic-service | 2 | 1 | -1 |
| ts4-ts-inside-payment-service-stress-gc2kcm | ts-inside-payment-service | stress | ts-payment-service | ts-inside-payment-service | 2 | 1 | -1 |
| ts4-ts-order-other-service-delay-mpwtgz | mysql;ts-order-other-service | delay | ts-ui-dashboard | ts-order-other-service | 2 | 1 | -1 |
| ts4-ts-route-service-delay-h9prcp | mysql;ts-route-service | delay | ts-ui-dashboard | ts-route-service | 2 | 1 | -1 |
| ts4-ts-ui-dashboard-response-replace-code-5s6j28 | ts-food-service;ts-ui-dashboard | response-replace-code | ts-payment-service | ts-ui-dashboard | 2 | 1 | -1 |
| ts5-mysql-loss-q42phw | mysql;ts-auth-service | loss | ts-ui-dashboard | ts-auth-service | 2 | 1 | -1 |
| ts5-ts-food-service-response-replace-code-bgr2hd | ts-food-service;ts-travel-service | response-replace-code | ts-consign-service | ts-food-service | 2 | 1 | -1 |
| ts5-ts-inside-payment-service-stress-tbb7h6 | ts-inside-payment-service | stress | ts-payment-service | ts-inside-payment-service | 2 | 1 | -1 |
| ts5-ts-preserve-service-request-replace-method-v2qhvn | ts-order-service;ts-preserve-service | request-replace-method | ts-seat-service | ts-preserve-service | 2 | 1 | -1 |
| ts5-ts-route-plan-service-response-replace-code-2w8c9x | ts-route-plan-service;ts-travel2-service | response-replace-code | ts-cancel-service | ts-route-plan-service | 2 | 1 | -1 |
| ts5-ts-ui-dashboard-response-replace-code-dww7g8 | ts-travel-plan-service;ts-ui-dashboard | response-replace-code | ts-seat-service | ts-ui-dashboard | 2 | 1 | -1 |
| ts5-ts-ui-dashboard-response-replace-code-mdt2gw | ts-travel2-service;ts-ui-dashboard | response-replace-code | ts-payment-service | ts-ui-dashboard | 2 | 1 | -1 |
| ts8-ts-basic-service-response-abort-fwndhj | ts-basic-service;ts-station-service | response-abort | ts-price-service | ts-basic-service | 2 | 1 | -1 |
| ts8-ts-route-plan-service-request-replace-path-xxpxdq | ts-route-plan-service;ts-travel2-service | request-replace-path | ts-cancel-service | ts-route-plan-service | 2 | 1 | -1 |
| ts9-ts-route-plan-service-request-replace-path-9dg8qf | ts-route-plan-service;ts-travel-service | request-replace-path | ts-payment-service | ts-route-plan-service | 2 | 1 | -1 |

## Regressed From Hit@1

| datapack | gt | fault_type | top1_old | top1_new | best_rank_old | best_rank_new | rank_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ts4-ts-assurance-service-partition-m4gbzn | ts-assurance-service;ts-ui-dashboard | partition | ts-ui-dashboard | ts-consign-service | 1 | 17 | 16 |
| ts4-ts-assurance-service-loss-5nnml6 | ts-assurance-service;ts-ui-dashboard | loss | ts-ui-dashboard | ts-seat-service | 1 | 11 | 10 |
| ts5-ts-ui-dashboard-partition-czfh8c | ts-assurance-service;ts-ui-dashboard | partition | ts-ui-dashboard | ts-order-other-service | 1 | 11 | 10 |
| ts4-ts-ui-dashboard-partition-rtqqjj | ts-travel2-service;ts-ui-dashboard | partition | ts-ui-dashboard | ts-verification-code-service | 1 | 10 | 9 |
| ts7-ts-ui-dashboard-loss-sz9kk8 | ts-assurance-service;ts-ui-dashboard | loss | ts-ui-dashboard | ts-food-service | 1 | 10 | 9 |
| ts5-ts-ui-dashboard-corrupt-x6ghbz | ts-travel-service;ts-ui-dashboard | corrupt | ts-ui-dashboard | ts-consign-service | 1 | 9 | 8 |
| ts4-ts-ui-dashboard-partition-jmlxcg | ts-assurance-service;ts-ui-dashboard | partition | ts-ui-dashboard | ts-food-service | 1 | 8 | 7 |
| ts4-ts-assurance-service-partition-nj8rh5 | ts-assurance-service;ts-ui-dashboard | partition | ts-ui-dashboard | loadgenerator | 1 | 7 | 6 |
| ts4-ts-travel-plan-service-loss-ttgbmd | ts-travel-plan-service;ts-ui-dashboard | loss | ts-ui-dashboard | ts-security-service | 1 | 7 | 6 |
| ts4-ts-ui-dashboard-partition-hssb5r | ts-consign-service;ts-ui-dashboard | partition | ts-ui-dashboard | ts-verification-code-service | 1 | 7 | 6 |
| ts5-ts-route-service-partition-rn9lhb | ts-route-service;ts-ui-dashboard | partition | ts-ui-dashboard | ts-order-other-service | 1 | 7 | 6 |
| ts5-ts-seat-service-response-delay-l2kbb2 | ts-config-service;ts-seat-service | response-delay | ts-seat-service | ts-preserve-service | 1 | 7 | 6 |
| ts6-ts-ui-dashboard-partition-7q5gf6 | ts-train-service;ts-ui-dashboard | partition | ts-ui-dashboard | ts-order-other-service | 1 | 7 | 6 |
| ts8-ts-ui-dashboard-corrupt-5wlgpm | ts-food-service;ts-ui-dashboard | corrupt | ts-ui-dashboard | ts-seat-service | 1 | 7 | 6 |
| ts0-ts-ui-dashboard-request-delay-s2z79x | ts-route-service;ts-ui-dashboard | request-delay | ts-ui-dashboard | ts-verification-code-service | 1 | 6 | 5 |
| ts4-ts-seat-service-response-delay-tl8vdx | ts-config-service;ts-seat-service | response-delay | ts-seat-service | ts-travel-service | 1 | 6 | 5 |
| ts4-ts-ui-dashboard-loss-hb2fkr | ts-ui-dashboard;ts-verification-code-service | loss | ts-ui-dashboard | ts-consign-service | 1 | 6 | 5 |
| ts4-ts-ui-dashboard-loss-krrnpv | ts-travel-service;ts-ui-dashboard | loss | ts-ui-dashboard | ts-travel-plan-service | 1 | 6 | 5 |
| ts5-mysql-corrupt-k6788t | mysql;ts-order-service | corrupt | ts-order-service | ts-seat-service | 1 | 6 | 5 |
| ts5-ts-seat-service-corrupt-v8cmmz | ts-order-service;ts-seat-service | corrupt | ts-seat-service | ts-config-service | 1 | 6 | 5 |
| ts5-ts-basic-service-response-delay-wwd22h | ts-basic-service;ts-station-service | response-delay | ts-basic-service | ts-preserve-service | 1 | 5 | 4 |
| ts3-ts-travel-service-response-delay-4rdh8b | ts-seat-service;ts-travel-service | response-delay | ts-travel-service | loadgenerator | 1 | 4 | 3 |
| ts4-ts-consign-service-bandwidth-6rx829 | ts-consign-service;ts-ui-dashboard | bandwidth | ts-ui-dashboard | ts-auth-service | 1 | 4 | 3 |
| ts4-ts-seat-service-response-delay-svgkqb | ts-order-other-service;ts-seat-service | response-delay | ts-seat-service | ts-inside-payment-service | 1 | 4 | 3 |
| ts4-ts-station-service-corrupt-j2zgbd | ts-basic-service;ts-station-service | corrupt | ts-basic-service | ts-travel-plan-service | 1 | 4 | 3 |
| ts5-ts-order-other-service-delay-bp64zk | ts-order-other-service;ts-seat-service | delay | ts-seat-service | ts-preserve-service | 1 | 4 | 3 |
| ts5-ts-travel-plan-service-bandwidth-w6w6c2 | ts-travel-plan-service;ts-ui-dashboard | bandwidth | ts-ui-dashboard | ts-auth-service | 1 | 4 | 3 |
| ts9-ts-order-service-partition-msxm42 | ts-order-service;ts-seat-service | partition | ts-seat-service | ts-travel-plan-service | 1 | 4 | 3 |
| ts9-ts-payment-service-container-kill-mnvc8v | ts-payment-service | container-kill | ts-payment-service | ts-consign-price-service | 1 | 4 | 3 |
| ts9-ts-ui-dashboard-loss-tzrlzc | ts-order-service;ts-ui-dashboard | loss | ts-ui-dashboard | loadgenerator | 1 | 4 | 3 |
| ts0-ts-travel-service-request-delay-z8wzcp | ts-seat-service;ts-travel-service | request-delay | ts-travel-service | ts-food-service | 1 | 3 | 2 |
| ts2-ts-ui-dashboard-request-replace-method-x2wq96 | ts-contacts-service;ts-ui-dashboard | request-replace-method | ts-ui-dashboard | ts-consign-service | 1 | 3 | 2 |
| ts3-ts-travel-service-request-replace-method-dpcc9t | ts-route-service;ts-travel-service | request-replace-method | ts-travel-service | ts-food-service | 1 | 3 | 2 |
| ts4-ts-basic-service-response-delay-hzjzvv | ts-basic-service;ts-train-service | response-delay | ts-basic-service | ts-preserve-service | 1 | 3 | 2 |
| ts4-ts-basic-service-response-delay-srn98p | ts-basic-service;ts-route-service | response-delay | ts-basic-service | ts-preserve-service | 1 | 3 | 2 |
| ts4-ts-seat-service-request-delay-xfh49m | ts-order-other-service;ts-seat-service | request-delay | ts-seat-service | ts-route-plan-service | 1 | 3 | 2 |
| ts4-ts-ui-dashboard-response-delay-fzgvbz | ts-travel2-service;ts-ui-dashboard | response-delay | ts-ui-dashboard | loadgenerator | 1 | 3 | 2 |
| ts5-ts-basic-service-response-replace-code-fqg54d | ts-basic-service;ts-price-service | response-replace-code | ts-basic-service | ts-travel-plan-service | 1 | 3 | 2 |
| ts5-ts-basic-service-response-replace-code-h6kpzp | ts-basic-service;ts-price-service | response-replace-code | ts-basic-service | ts-preserve-service | 1 | 3 | 2 |
| ts5-ts-seat-service-loss-5kglkt | ts-order-other-service;ts-seat-service | loss | ts-seat-service | ts-travel2-service | 1 | 3 | 2 |

## Decision

Reject `crest_victim_suppression` as a default change. The pairwise suppression operation is too broad: it removes score from many already-correct roots and causes large AC@1, AC@3, AC@5, and MRR regressions. Future work must not apply generic suppression to all adjacent mutation/propagation contrasts; it needs a stronger root-victim eligibility model before altering the final score.
