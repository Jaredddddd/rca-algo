# CREST4 Attempt: Topology-Role Contrast and Non-Hardcoded Role Priors

- Date: 2026-06-06
- Algorithm registry name: `crest`
- Baseline: `CREST3`
- Decision: not accepted into runtime

## Goal

Try to move `crest` from the accepted CREST3 result (`AC@1=0.800281`) toward `AC@1 > 0.84` without using labels, injection metadata, previous outputs, `conclusion.parquet`, external models, LLMs, or CERA's hardcoded ordinal feature tiers in the runtime path.

The main hypothesis was:

```text
Topology-role contrast can transfer neighbor duration/volume victim symptoms back to weak roots with mutation/drop evidence, especially for pod-failure and infrastructure-local misses.
```

## Offline-Only Diagnostics

All diagnostics used labels only to compute metrics. No runtime code path was changed.

### Case-Local Reliability Sweep

The pre-existing long sweep tested concentration, mutation agreement, victim anti-correlation, and rank-ratio feature reliability signals.

Best observed result:

```text
ratio_conc_g0.1 / root_conc_g0.1
AC@1=0.802391, MRR≈0.87628, AC@3=0.944444, AC@5=0.973277
```

This was too close to CREST3 to justify a runtime change.

### Root / Victim Role Terms

Using cached CREST internal scores and role-family burdens, several label-free score adjustments were swept:

- add root mutation/drop/API support;
- penalize victim-only propagation/log evidence;
- conditionally rerank top-k candidates when top1 is victim-heavy;
- transfer neighbor victim symptoms to candidates with stronger mutation/drop evidence.

Best observed result:

```text
score + 0.05 * root_any
AC@1=0.806610, MRR=0.878869, AC@3=0.945851, AC@5=0.973277
```

Best top-k conditional role rule:

```text
K=5, root_score near-tie rerank
AC@1=0.807314, rescues=44, regressions=34
```

These rules were not stable enough: they rescued some rank-2/rank-3 misses but also regressed many existing hit@1 cases.

### CREST Internal Variant Selection

CREST3 ablations have useful complementary hits:

```text
oracle(crest, crest_local, crest_nocf, crest_nocalib) = AC@1=0.874121
```

However, unsupervised selectors over variant top1 candidates were not reliable.

Best observed selector:

```text
switch to crest_nocf top1 when it is a CREST near-tie candidate
AC@1=0.812940, rescues=31, regressions=13
```

This is a real improvement direction, but still far from `0.84`.

### Family-Level and Individual-Feature Role Priors

Family-level random / grid searches over normalized CREST role burdens found an upper bound around:

```text
AC@1=0.819269
```

Individual-feature searches on the CREST-normalized feature matrix did not improve the bound:

```text
best random individual-feature blend: AC@1=0.806610
equal feature sum: AC@1=0.668776
rank fusion: AC@1=0.485935
CERA ordinal shape applied to CREST-normalized matrix: AC@1=0.464135
```

This suggests the CERA gap is not reproduced by simply reweighting CREST's normalized role matrix.

### CERA Rank-Blend Boundary Check

Offline rank blending was used only to estimate how much of the remaining gap depends on CERA's ordinal prior.

```text
crest + full cera rank channel: AC@1=0.850211
best blend of cera modality variants without full cera: AC@1=0.838959
```

These are not accepted for CREST because they depend on CERA's hardcoded ordinal feature-role prior, which is exactly the mechanism CREST is intended to avoid.

## Conclusion

The current evidence does not support accepting a CREST4 runtime change yet.

The strongest clean, label-free CREST-internal direction found in this attempt is a conservative `crest_nocf` near-tie selector (`AC@1=0.812940` offline). It improves CREST3 but does not approach `0.84`, and therefore should remain a research candidate rather than replacing the accepted CREST3 default.

The diagnostic boundary is clear:

- CREST-internal topology-role contrast and variant selection currently top out around `0.81-0.82`.
- Getting to `0.84+` is easy if CERA's ordinal prior is reintroduced.
- Reintroducing that prior would violate the stated CREST novelty constraint.

## Next Hypothesis

The next attempt should learn a label-free role prior from raw log1p feature scale and topology, not from CREST's already-normalized role matrix:

```text
Estimate feature role confidence from incident-local structural rootness:
features whose high values are concentrated on upstream/intervenable nodes and whose downstream neighbors carry propagation-only symptoms should receive higher causal-role confidence; features concentrated on sinks, high-volume fanout nodes, or pure duration/log victims should receive lower confidence.
```

This should be implemented as a raw-feature, topology-aware calibration channel and evaluated against CREST3 before any runtime change is accepted.

## Follow-Up Raw-Feature Probe

Added two offline-only probes:

- `VibeResearchTools/crest_raw_role_probe.py`
- `VibeResearchTools/crest_raw_equal_top_probe.py`

These scripts read labels only for metric computation and do not affect the runtime `crest` algorithm.

### Raw Topology Role Confidence

`crest_raw_role_probe.py` tested feature confidence derived from:

- incident-local feature concentration;
- top feature gap;
- directed-edge upstream-vs-downstream excess;
- sink-vs-source concentration;
- downstream victim transfer back to upstream nodes.

Best standalone result:

```text
raw_equal_parent
AC@1=0.633615, MRR=0.749921, AC@3=0.836146, AC@5=0.911392
```

The explicit topology-rootness variants were worse than raw equal evidence. This rejects the naive hypothesis that incident-local upstream excess alone can recover a CERA-like role prior.

### Raw Equal as Complementary Candidate

Although weak as a primary ranker, `raw_equal_parent` is complementary to CREST3:

```text
raw_equal_parent standalone AC@1=0.633615
raw_equal_parent rescues 77 CREST3 miss cases
oracle(crest, raw_equal_parent)=0.854430
```

The top-candidate selector sweep used:

- raw top1 score gap / gap ratio;
- raw top1's CREST rank and CREST score gap;
- CREST top1 score gap and victim-heavy indicators.

Best selector:

```text
AC@1=0.810127, rescues=27, regressions=13
```

### Combined Raw + NoCF Selector

Combining `raw_equal_parent` and `crest_nocf` candidates gives a large oracle:

```text
oracle(crest, raw_equal_parent, crest_nocf)=0.890295
```

But the best simple no-label selector found was:

```text
AC@1=0.817862, rescues=49, regressions=24
```

This is the strongest clean candidate so far, but it remains far below the `AC@1 > 0.84` target and is not accepted into runtime.

### Updated Conclusion

Raw evidence has useful complementary signal, but the current no-label confidence rules cannot separate its true rescues from its many regressions. The next attempt should focus on selector reliability rather than creating more standalone rankers:

```text
Learn an incident-local confidence test for when CREST's counterfactual structural top1 is over-explaining a victim, using only score gaps, cross-view agreement, and topology role consistency.
```

## Follow-Up Selector Mining

Built `/tmp/crest_selector_candidates.parquet` with one row per candidate switch:

- candidate sources: `raw_equal_parent` and `crest_nocf`;
- candidate features: CREST rank, CREST score ratio, `A/F/S` advantage, root/victim/propagation contrast, raw score gap;
- labels used only offline to mark whether switching would rescue or regress hit@1.

Candidate pool:

```text
raw candidates: 77 rescues, 314 regressions
nocf candidates: 75 rescues, 513 regressions
base CREST3 hit@1: 1138 / 1422
```

The selector has enough oracle headroom:

```text
oracle(crest, raw_equal_parent, crest_nocf)=0.890295
```

However, no label-free rule family found a reliable boundary. Best simplified no-label rules after mining:

```text
combo score_ratio/S_adv/raw_gap selector:
AC@1=0.815752, rescues=38, regressions=16

best previous raw+nocf selector:
AC@1=0.817862, rescues=49, regressions=24
```

An offline sklearn decision tree can separate good/bad candidate switches in-sample:

```text
depth=8, threshold=0.8: good=123, bad=17, net=106
depth=10, threshold=0.8: good=128, bad=20, net=108
```

But this is not accepted because those splits are learned from RCABench labels. Encoding the tree or its label-tuned thresholds into runtime would turn the selector into a supervised dataset-specific component, violating CREST's no-label generalization constraint.

## Blocker

The same blocker has now repeated across topology-role transfer, raw-feature role priors, raw/nocf selector sweeps, and selector mining:

```text
The complementary candidates needed for AC@1 > 0.84 exist, but every clean no-label confidence rule found so far selects too many regressions. The methods that cross the threshold either reintroduce CERA's hardcoded ordinal prior or use label-tuned selector thresholds.
```

To continue toward `AC@1 > 0.84` without violating the stated constraints, the next step needs one of:

- a new genuinely label-free confidence objective beyond the explored score-gap / S-advantage / root-victim contrast features;
- permission to use an offline-trained traditional selector and defend it as statistical ML rather than unsupervised RCA;
- permission to reintroduce a CERA-like ordinal prior in a calibrated or ablated form.
