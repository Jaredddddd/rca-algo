# EvidenceRank Compare ARC_BASELINE vs ARC1

- Created: 2026-06-03T15:11:10+08:00
- Old: `ARC_BASELINE`
- New: `ARC1`

## Metric Delta

| metric | old | new | delta |
| --- | ---: | ---: | ---: |
| AC@1 | 0.670886 | 0.705345 | 0.034459 |
| AC@3 | 0.925457 | 0.940225 | 0.014768 |
| AC@5 | 0.973980 | 0.971167 | -0.002813 |
| MRR | 0.801983 | 0.823675 | 0.021692 |

## Status Counts

| status | cases |
| --- | ---: |
| improved_to_hit1 | 87 |
| rank_improved | 67 |
| rank_regressed | 42 |
| regressed_from_hit1 | 38 |
| unchanged | 1188 |

## Important Case Deltas

| datapack | status | old_rank | new_rank | rank_delta | gt | new_top5 | fault_type | case_service |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| ts0-ts-basic-service-request-replace-path-576b9q | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-train-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-travel2-service|ts-ui-dashboard | request-replace-path | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-lmnjw7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-basic-service-response-replace-code-v9z47n | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts0-ts-route-plan-service-request-abort-7rfdzb | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-seat-service|ts-travel-service | request-abort | ts-route-plan-service |
| ts0-ts-route-plan-service-request-replace-path-7v499h | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-payment-service | request-replace-path | ts-route-plan-service |
| ts0-ts-route-plan-service-response-replace-code-nsmpv4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-order-service|loadgenerator | response-replace-code | ts-route-plan-service |
| ts0-ts-ui-dashboard-response-delay-nqtssr | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-assurance-service|ts-preserve-service|ts-basic-service | response-delay | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-lflx8j | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-price-service|ts-cancel-service|loadgenerator|ts-train-food-service | response-replace-code | ts-ui-dashboard |
| ts0-ts-ui-dashboard-response-replace-code-rm7j85 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-price-service|ts-travel-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-ui-dashboard |
| ts1-ts-basic-service-request-abort-c7t479 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-route-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-preserve-service|ts-ui-dashboard | request-abort | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-htkcsw | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-route-plan-service|ts-travel-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-basic-service-response-replace-code-v225t5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-ui-dashboard|ts-travel2-service|ts-route-plan-service | response-replace-code | ts-basic-service |
| ts1-ts-preserve-service-response-replace-code-wpdr2x | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-preserve-service | ts-preserve-service|ts-ui-dashboard|ts-basic-service|loadgenerator|ts-travel-service | response-replace-code | ts-preserve-service |
| ts1-ts-route-plan-service-request-replace-path-8b97qc | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-route-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel-service|ts-inside-payment-service | request-replace-path | ts-route-plan-service |
| ts1-ts-route-plan-service-response-abort-5l599d | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel2-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-travel-service | response-abort | ts-route-plan-service |
| ts1-ts-seat-service-request-replace-path-jmcntt | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-inside-payment-service|ts-ui-dashboard|ts-travel-plan-service | request-replace-path | ts-seat-service |
| ts1-ts-security-service-request-replace-method-xv2ncg | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-basic-service | request-replace-method | ts-security-service |
| ts1-ts-station-service-stress-jzbbjv | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-travel-service | stress | ts-station-service |
| ts1-ts-travel2-service-response-replace-code-swdpv2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-ui-dashboard|ts-travel-plan-service|ts-basic-service | response-replace-code | ts-travel2-service |
| ts1-ts-ui-dashboard-request-delay-d56qn8 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-user-service|ts-travel-service|ts-preserve-service | request-delay | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-5cjdfh | improved_to_hit1 | 2 | 1 | 1.0 | ts-auth-service;ts-ui-dashboard | ts-ui-dashboard|ts-station-service|ts-auth-service|ts-seat-service|loadgenerator | response-replace-code | ts-ui-dashboard |
| ts1-ts-ui-dashboard-response-replace-code-prqgf5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-ui-dashboard | ts-ui-dashboard|ts-assurance-service|ts-travel-service|ts-order-service|ts-seat-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-auth-service-loss-5k6gqr | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-auth-service | ts-auth-service|ts-ui-dashboard|loadgenerator|ts-verification-code-service|ts-order-service | loss | ts-auth-service |
| ts2-ts-basic-service-response-replace-code-plcrpl | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service|ts-price-service | response-replace-code | ts-basic-service |
| ts2-ts-food-service-bandwidth-b5qvk5 | improved_to_hit1 | 2 | 1 | 1.0 | ts-food-service;ts-ui-dashboard | ts-ui-dashboard|ts-consign-service|ts-assurance-service|ts-seat-service|ts-verification-code-service | bandwidth | ts-food-service |
| ts2-ts-route-plan-service-response-abort-6xqqsz | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-travel-service|ts-basic-service|ts-seat-service | response-abort | ts-route-plan-service |
| ts2-ts-route-plan-service-response-replace-code-7z5jgz | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-plan-service;ts-travel-service | ts-route-plan-service|ts-travel-plan-service|ts-ui-dashboard|ts-travel2-service|ts-basic-service | response-replace-code | ts-route-plan-service |
| ts2-ts-seat-service-request-abort-bkttwc | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-seat-service | ts-seat-service|ts-travel2-service|ts-travel-plan-service|ts-route-plan-service|ts-order-service | request-abort | ts-seat-service |
| ts2-ts-security-service-request-abort-55q6h2 | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-other-service;ts-security-service | ts-security-service|ts-preserve-service|ts-ui-dashboard|ts-order-service|ts-travel-service | request-abort | ts-security-service |
| ts2-ts-station-service-dns-nn49s2 | improved_to_hit1 | 2 | 1 | 1.0 | mysql;ts-station-service | ts-station-service|ts-consign-service|ts-ui-dashboard|ts-seat-service|ts-food-service | unknown | unknown |
| ts2-ts-station-service-stress-mzxgqn | improved_to_hit1 | 2 | 1 | 1.0 | ts-station-service | ts-station-service|ts-basic-service|ts-ui-dashboard|ts-travel-service|ts-travel-plan-service | stress | ts-station-service |
| ts2-ts-travel-service-response-replace-code-8c25qw | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-route-plan-service|ts-travel-plan-service|ts-basic-service|ts-ui-dashboard | response-replace-code | ts-travel-service |
| ts2-ts-travel-service-response-replace-code-rkfmdr | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel-service | ts-travel-service|ts-preserve-service|ts-route-plan-service|ts-basic-service|ts-ui-dashboard | response-replace-code | ts-travel-service |
| ts2-ts-travel2-service-request-abort-g79sj7 | improved_to_hit1 | 2 | 1 | 1.0 | ts-route-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-travel-plan-service|ts-seat-service|ts-travel-service | request-abort | ts-travel2-service |
| ts2-ts-travel2-service-response-replace-body-hbpngf | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-travel2-service | ts-travel2-service|ts-route-plan-service|ts-basic-service|ts-travel-plan-service|ts-order-other-service | response-replace-body | ts-travel2-service |
| ts2-ts-ui-dashboard-response-abort-kv4mqz | improved_to_hit1 | 2 | 1 | 1.0 | ts-order-service;ts-ui-dashboard | ts-ui-dashboard|loadgenerator|ts-order-service|ts-order-other-service|ts-train-food-service | response-abort | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-475jm4 | improved_to_hit1 | 2 | 1 | 1.0 | ts-assurance-service;ts-ui-dashboard | ts-ui-dashboard|ts-cancel-service|ts-travel2-service|ts-consign-price-service|ts-route-plan-service | response-replace-code | ts-ui-dashboard |
| ts2-ts-ui-dashboard-response-replace-code-ms2qf9 | improved_to_hit1 | 2 | 1 | 1.0 | ts-travel-plan-service;ts-ui-dashboard | ts-ui-dashboard|ts-seat-service|ts-payment-service|ts-basic-service|ts-config-service | response-replace-code | ts-ui-dashboard |
| ts3-ts-basic-service-request-replace-method-spzxcr | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-price-service | ts-basic-service|ts-travel-service|ts-preserve-service|ts-consign-service|ts-price-service | request-replace-method | ts-basic-service |
| ts3-ts-basic-service-response-replace-code-lbw8bl | improved_to_hit1 | 2 | 1 | 1.0 | ts-basic-service;ts-station-service | ts-basic-service|ts-travel-service|ts-travel2-service|ts-ui-dashboard|ts-route-plan-service | response-replace-code | ts-basic-service |

## Decision Notes

- Accept `ARC1` as the current EvidRank-ARC iteration.
- Metrics: AC@1 improves by `+0.034459`, MRR by `+0.021692`, and AC@3 by `+0.014768`; AC@5 drops slightly by `-0.002813`.
- Case movement: `87` cases improved to Hit@1, `38` regressed from Hit@1, and the net Hit@1 gain is `+49`.
- Main positive mechanism: single-case feature reliability was over-amplifying propagation symptoms; using reliability as an active-feature mask plus trace-direction caller-victim contrast lifts many rank-2 protocol mutation roots above neighboring caller/high-traffic services.
- Main regression risk: pod/infrastructure, partition, bandwidth, and a few protocol cases can need a sharper concentrated signal; active-mask neutralization can flatten that signal and let adjacent services move ahead.
- Next step: add a no-label reliability confidence gate that preserves learned reliability only when cross-family agreement and topology contrast both support it.
