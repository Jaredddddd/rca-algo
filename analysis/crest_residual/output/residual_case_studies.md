# CREST-Residual Case Studies

- Residual wins over crest: 32
- Residual losses against crest: 0
- Counterfactual/topology wins over local or nocf pool: 619

## Residual Wins

### ts0-ts-basic-service-request-replace-method-99j798

- Ground truth: ts-basic-service, ts-route-service
- crest: 1:ts-preserve-service, 2:ts-basic-service, 3:ts-travel-service, 4:ts-travel2-service, 5:ts-route-service
- crest_residual: 1:ts-basic-service, 2:ts-preserve-service, 3:ts-travel-service, 4:ts-travel2-service, 5:ts-route-service
- crest_local: 1:ts-preserve-service, 2:ts-travel-service, 3:ts-basic-service, 4:ts-travel2-service, 5:ts-ui-dashboard
- crest_nocf: 1:ts-basic-service, 2:ts-travel-service, 3:ts-ui-dashboard, 4:ts-travel2-service, 5:ts-preserve-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-basic-service | 0.9685 | 0.9969 | 1.0000 | 1.0000 | 0.9976 | 0.0455 | 0.9969 | 1.9881 |
| ts-preserve-service | 1.0000 | 1.0000 | 0.9881 | 1.0000 | 1.0000 | 0.0584 | 1.0000 | 1.9881 |
| ts-travel-service | 0.9795 | 0.9796 | 0.9696 | 0.9561 | 1.0000 | 0.0533 | 0.9796 | 1.9291 |
| ts-travel2-service | 0.9419 | 0.9485 | 0.9404 | 0.7494 | 0.9519 | 0.0404 | 0.9485 | 1.8338 |
| ts-route-service | 0.9055 | 0.9499 | 0.9532 | 0.7960 | 0.5950 | 0.0165 | 0.9499 | 1.8133 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.

### ts0-ts-basic-service-response-replace-code-r727qm

- Ground truth: ts-basic-service, ts-route-service
- crest: 1:ts-travel-service, 2:ts-basic-service, 3:ts-station-service, 4:ts-travel2-service, 5:ts-travel-plan-service
- crest_residual: 1:ts-basic-service, 2:ts-travel-service, 3:ts-station-service, 4:ts-travel2-service, 5:ts-travel-plan-service
- crest_local: 1:ts-travel-service, 2:ts-basic-service, 3:ts-ui-dashboard, 4:ts-station-service, 5:ts-travel2-service
- crest_nocf: 1:ts-basic-service, 2:ts-travel-service, 3:ts-ui-dashboard, 4:ts-station-service, 5:ts-verification-code-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-basic-service | 0.9716 | 0.9974 | 1.0000 | 1.0000 | 0.9116 | 0.0431 | 0.9974 | 1.9941 |
| ts-travel-service | 1.0000 | 1.0000 | 0.9941 | 1.0000 | 1.0000 | 0.0535 | 1.0000 | 1.9941 |
| ts-station-service | 0.9570 | 0.9839 | 0.9924 | 0.9971 | 0.9152 | 0.0300 | 0.9839 | 1.9339 |
| ts-travel2-service | 0.9484 | 0.9640 | 0.9581 | 0.9634 | 0.9270 | 0.0492 | 0.9640 | 1.8724 |
| ts-travel-plan-service | 0.9347 | 0.9610 | 0.9519 | 0.7256 | 0.9205 | 0.0384 | 0.9610 | 1.8502 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.

### ts0-ts-seat-service-response-replace-code-4mpcv7

- Ground truth: ts-order-service, ts-seat-service
- crest: 1:ts-travel-service, 2:ts-seat-service, 3:ts-order-service, 4:ts-route-plan-service, 5:ts-travel-plan-service
- crest_residual: 1:ts-seat-service, 2:ts-travel-service, 3:ts-order-service, 4:ts-route-plan-service, 5:ts-travel-plan-service
- crest_local: 1:ts-travel-service, 2:ts-seat-service, 3:ts-route-plan-service, 4:ts-ui-dashboard, 5:ts-order-service
- crest_nocf: 1:ts-seat-service, 2:ts-order-service, 3:ts-travel-service, 4:ts-ui-dashboard, 5:ts-verification-code-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-seat-service | 0.9962 | 0.9947 | 0.9977 | 1.0000 | 0.8227 | 0.0389 | 0.9947 | 2.0000 |
| ts-travel-service | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0489 | 1.0000 | 2.0000 |
| ts-order-service | 0.9729 | 0.9944 | 0.9997 | 0.6702 | 0.9650 | 0.0198 | 0.9944 | 1.9672 |
| ts-route-plan-service | 0.9750 | 0.9761 | 0.9654 | 0.6206 | 1.0000 | 0.0314 | 0.9761 | 1.9170 |
| ts-travel-plan-service | 0.9537 | 0.9791 | 0.9767 | 0.6574 | 0.9605 | 0.0306 | 0.9791 | 1.9105 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.

### ts0-ts-travel-service-request-abort-g9mc2t

- Ground truth: ts-basic-service, ts-travel-service
- crest: 1:ts-route-plan-service, 2:ts-travel-service, 3:ts-travel-plan-service, 4:ts-seat-service, 5:ts-travel2-service
- crest_residual: 1:ts-travel-service, 2:ts-route-plan-service, 3:ts-travel-plan-service, 4:ts-seat-service, 5:ts-travel2-service
- crest_local: 1:ts-travel-service, 2:ts-route-plan-service, 3:ts-travel-plan-service, 4:ts-ui-dashboard, 5:ts-seat-service
- crest_nocf: 1:ts-travel-service, 2:ts-route-plan-service, 3:ts-seat-service, 4:ts-travel-plan-service, 5:ts-order-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-travel-service | 1.0000 | 0.9649 | 0.9890 | 1.0000 | 1.0000 | 0.0508 | 0.9649 | 1.9765 |
| ts-route-plan-service | 0.9765 | 1.0000 | 1.0000 | 1.0000 | 0.9288 | 0.0560 | 1.0000 | 1.9765 |
| ts-travel-plan-service | 0.9740 | 0.9441 | 0.9263 | 0.9295 | 1.0000 | 0.0545 | 0.9441 | 1.8458 |
| ts-seat-service | 0.8386 | 0.8772 | 0.8973 | 0.3782 | 0.7572 | 0.0139 | 0.8772 | 1.6329 |
| ts-travel2-service | 0.7955 | 0.8765 | 0.8952 | 0.3817 | 0.6663 | 0.0152 | 0.8765 | 1.5924 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.

### ts1-ts-seat-service-request-replace-path-jmcntt

- Ground truth: ts-order-other-service, ts-seat-service
- crest: 1:ts-travel2-service, 2:ts-seat-service, 3:ts-inside-payment-service, 4:ts-order-other-service, 5:ts-travel-plan-service
- crest_residual: 1:ts-seat-service, 2:ts-travel2-service, 3:ts-inside-payment-service, 4:ts-order-other-service, 5:ts-travel-plan-service
- crest_local: 1:ts-seat-service, 2:ts-travel2-service, 3:ts-inside-payment-service, 4:ts-ui-dashboard, 5:ts-order-other-service
- crest_nocf: 1:ts-seat-service, 2:ts-order-other-service, 3:ts-travel2-service, 4:ts-ui-dashboard, 5:ts-route-plan-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-seat-service | 1.0000 | 0.9820 | 0.9961 | 0.9936 | 1.0000 | 0.0474 | 0.9820 | 1.9849 |
| ts-travel2-service | 0.9853 | 1.0000 | 0.9996 | 0.7816 | 1.0000 | 0.0429 | 1.0000 | 1.9849 |
| ts-inside-payment-service | 0.9613 | 0.9919 | 1.0000 | 0.2958 | 0.6246 | 0.0099 | 0.9919 | 1.9535 |
| ts-order-other-service | 0.9470 | 0.9670 | 0.9845 | 1.0000 | 0.9293 | 0.0315 | 0.9670 | 1.9002 |
| ts-travel-plan-service | 0.9293 | 0.9720 | 0.9691 | 0.7035 | 0.8726 | 0.0341 | 0.9720 | 1.8724 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.

## Residual Losses

No cases found.

## Counterfactual Wins

### ts0-mysql-corrupt-jkgn5j

- Ground truth: mysql, ts-order-service
- crest: 1:ts-order-service, 2:ts-travel-service, 3:ts-seat-service, 4:ts-ui-dashboard, 5:ts-travel-plan-service
- crest_residual: 1:ts-order-service, 2:ts-travel-service, 3:ts-seat-service, 4:ts-ui-dashboard, 5:ts-travel-plan-service
- crest_local: 1:ts-order-service, 2:ts-ui-dashboard, 3:ts-seat-service, 4:ts-travel-service, 5:ts-basic-service
- crest_nocf: 1:ts-seat-service, 2:ts-ui-dashboard, 3:ts-order-service, 4:ts-basic-service, 5:ts-travel-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-order-service | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0321 | 1.0000 | 2.0000 |
| ts-travel-service | 0.9530 | 0.9578 | 0.9541 | 0.8027 | 0.9119 | 0.0371 | 0.9578 | 1.8668 |
| ts-seat-service | 0.9574 | 0.9471 | 0.9407 | 0.5189 | 1.0000 | 0.0218 | 0.9471 | 1.8475 |
| ts-ui-dashboard | 0.9615 | 0.9306 | 0.9264 | 0.7373 | 0.9458 | 0.0300 | 0.9306 | 1.8211 |
| ts-travel-plan-service | 0.8780 | 0.9529 | 0.9503 | 0.4734 | 0.7471 | 0.0190 | 0.9529 | 1.7870 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.

### ts0-mysql-loss-hfrvkl

- Ground truth: mysql, ts-security-service
- crest: 1:ts-security-service, 2:ts-preserve-service, 3:ts-basic-service, 4:ts-seat-service, 5:ts-ui-dashboard
- crest_residual: 1:ts-security-service, 2:ts-preserve-service, 3:ts-basic-service, 4:ts-seat-service, 5:ts-ui-dashboard
- crest_local: 1:ts-preserve-service, 2:ts-security-service, 3:ts-ui-dashboard, 4:ts-basic-service, 5:ts-seat-service
- crest_nocf: 1:ts-security-service, 2:ts-seat-service, 3:ts-ui-dashboard, 4:ts-preserve-service, 5:ts-order-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-security-service | 0.9810 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0443 | 1.0000 | 1.9810 |
| ts-preserve-service | 1.0000 | 0.9648 | 0.9734 | 1.0000 | 1.0000 | 0.0518 | 0.9648 | 1.9382 |
| ts-basic-service | 0.8921 | 0.8767 | 0.8998 | 0.7798 | 0.7664 | 0.0271 | 0.8767 | 1.6818 |
| ts-seat-service | 0.8772 | 0.8591 | 0.8833 | 0.3871 | 0.8487 | 0.0152 | 0.8591 | 1.6368 |
| ts-ui-dashboard | 0.9093 | 0.8477 | 0.8654 | 0.5606 | 0.9226 | 0.0234 | 0.8477 | 1.6361 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.

### ts0-mysql-loss-k9xrkf

- Ground truth: mysql, ts-travel-service
- crest: 1:ts-travel-service, 2:ts-preserve-service, 3:ts-ui-dashboard, 4:ts-seat-service, 5:ts-travel-plan-service
- crest_residual: 1:ts-travel-service, 2:ts-preserve-service, 3:ts-ui-dashboard, 4:ts-seat-service, 5:ts-travel-plan-service
- crest_local: 1:ts-travel-service, 2:ts-preserve-service, 3:ts-ui-dashboard, 4:ts-payment-service, 5:ts-seat-service
- crest_nocf: 1:ts-seat-service, 2:ts-travel-service, 3:ts-ui-dashboard, 4:ts-order-service, 5:ts-basic-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-travel-service | 1.0000 | 1.0000 | 0.9930 | 0.5667 | 1.0000 | 0.0278 | 1.0000 | 1.9930 |
| ts-preserve-service | 0.9542 | 0.9935 | 1.0000 | 1.0000 | 0.9773 | 0.0444 | 0.9935 | 1.9480 |
| ts-ui-dashboard | 0.9515 | 0.9429 | 0.9520 | 0.9735 | 0.9356 | 0.0413 | 0.9429 | 1.8492 |
| ts-seat-service | 0.8997 | 0.9427 | 0.9549 | 0.5062 | 0.8657 | 0.0200 | 0.9427 | 1.8030 |
| ts-travel-plan-service | 0.8837 | 0.9490 | 0.9492 | 0.4807 | 1.0000 | 0.0235 | 0.9490 | 1.7879 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.

### ts0-mysql-partition-cfvlsw

- Ground truth: mysql, ts-travel2-service
- crest: 1:ts-travel2-service, 2:ts-travel-plan-service, 3:ts-route-plan-service, 4:ts-basic-service, 5:ts-travel-service
- crest_residual: 1:ts-travel2-service, 2:ts-travel-plan-service, 3:ts-route-plan-service, 4:ts-basic-service, 5:ts-travel-service
- crest_local: 1:ts-travel2-service, 2:ts-travel-plan-service, 3:ts-ui-dashboard, 4:ts-route-plan-service, 5:ts-basic-service
- crest_nocf: 1:ts-basic-service, 2:ts-travel2-service, 3:ts-route-plan-service, 4:ts-ui-dashboard, 5:ts-verification-code-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-travel2-service | 1.0000 | 1.0000 | 0.9983 | 1.0000 | 1.0000 | 0.0483 | 1.0000 | 1.9983 |
| ts-travel-plan-service | 0.9920 | 0.9988 | 1.0000 | 1.0000 | 0.8864 | 0.0514 | 0.9988 | 1.9908 |
| ts-route-plan-service | 0.9827 | 0.9981 | 0.9939 | 0.8915 | 0.8829 | 0.0434 | 0.9981 | 1.9748 |
| ts-basic-service | 0.9581 | 0.9816 | 0.9838 | 0.6039 | 0.8604 | 0.0218 | 0.9816 | 1.9243 |
| ts-travel-service | 0.9499 | 0.9842 | 0.9853 | 0.5303 | 0.8036 | 0.0220 | 0.9842 | 1.9203 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.

### ts0-mysql-partition-fl747g

- Ground truth: mysql, ts-price-service
- crest: 1:ts-price-service, 2:ts-basic-service, 3:ts-travel2-service, 4:ts-verification-code-service, 5:ts-travel-service
- crest_residual: 1:ts-price-service, 2:ts-basic-service, 3:ts-travel2-service, 4:ts-verification-code-service, 5:ts-travel-service
- crest_local: 1:ts-price-service, 2:ts-basic-service, 3:ts-travel2-service, 4:ts-ui-dashboard, 5:ts-travel-service
- crest_nocf: 1:ts-basic-service, 2:ts-verification-code-service, 3:ts-ui-dashboard, 4:ts-price-service, 5:ts-travel2-service

| service | A | F | S | M | P | R | F_residual | final_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-price-service | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0298 | 1.0000 | 2.0000 |
| ts-basic-service | 0.9908 | 0.9894 | 0.9906 | 0.9889 | 1.0000 | 0.0406 | 0.9894 | 1.9709 |
| ts-travel2-service | 0.9858 | 0.9744 | 0.9751 | 0.9749 | 0.9644 | 0.0472 | 0.9744 | 1.9356 |
| ts-verification-code-service | 0.9695 | 0.9683 | 0.9770 | 0.3760 | 0.8376 | 0.0094 | 0.9683 | 1.9158 |
| ts-travel-service | 0.9722 | 0.9682 | 0.9687 | 0.7493 | 0.9008 | 0.0357 | 0.9682 | 1.9100 |

Interpretation: CREST-Residual changes rank only inside a very narrow CREST near-tie when the challenger has stronger mutation ownership, no larger propagation burden, non-weaker F, and top residual eligibility.
