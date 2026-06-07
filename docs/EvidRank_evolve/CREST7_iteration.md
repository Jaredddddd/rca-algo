# CREST7 Iteration

## Goal

Remove the low-value CREST calibration channel from the runtime path, keep the modules
that have shown useful signal, and expose modality ablations for metric, trace, log,
and their pairwise combinations.

## Constraints

- Runtime CREST must read only normal/abnormal metric, trace, and log parquet frames under
  `args.input_folder`.
- Runtime CREST must not read labels, injection metadata, previous outputs, perf reports,
  historical rankings, ground truth, or `conclusion.parquet`.
- Modality ablations must use the same scoring semantics as default CREST, changing only
  `enabled_modalities`.

## Hypothesis

The useful CREST contribution is not cross-modal calibration. It is the combination of
incident-local abnormality, trace parent context, counterfactual explain-away, and denoised
support. Calibration adds an extra mechanism with little measured benefit and makes the
paper story less clean, so it should be removed from the default algorithm. Separate
modality ablations can then show which telemetry families drive the remaining gains.

## Code Changes

- Removed runtime calibration from `algorithms/evidencerank/src/evidencerank/crest.py`.
- CREST now scores services as:

```text
score(v) = A(v) * F(v) + S(v)
```

- Diagnostic output from `score_crest_services(...)` now exposes `service`, `A`, `F`, `S`,
  and `score`; the old `C` column is gone.
- Removed the `crest_nocalib` registry entry because the default `crest` is now no-calib.
- Added modality ablation registry entries:
  - `crest_metric`
  - `crest_trace`
  - `crest_log`
  - `crest_metric_trace`
  - `crest_metric_log`
  - `crest_log_trace`
- Kept structural module ablations:
  - `crest_local`
  - `crest_nocf`

## Verification So Far

```bash
python -m py_compile algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py
uv run --package evidencerank python algorithms/evidencerank/main.py --help
uv run --package evidencerank python algorithms/evidencerank/main.py eval batch --help
uv run --package evidencerank ruff check algorithms/evidencerank/src/evidencerank/crest.py algorithms/evidencerank/main.py
uv run --package evidencerank python VibeResearchTools/evidrank_lab.py guard
```

Single-case smoke test on `ts0-mysql-container-kill-9t6n24` confirmed that `crest` and all
six modality ablations return service rankings with columns `service,A,F,S,score`.

## Full Evaluation Command

```bash
LOGURU_LEVEL=WARNING uv run --package evidencerank python algorithms/evidencerank/main.py \
  eval batch \
  -a crest \
  -a crest_local \
  -a crest_nocf \
  -a crest_metric \
  -a crest_trace \
  -a crest_log \
  -a crest_metric_trace \
  -a crest_metric_log \
  -a crest_log_trace \
  -d rcabench --clear --use-cpus 32

uv run --package evidencerank python algorithms/evidencerank/main.py eval perf-report rcabench
uv run --package baro python scripts/combined_report.py rcabench --sort-by AC@1
```

## Next Validation

Run full eval after snapshotting the current accepted CREST output. The expected default
CREST metrics should match the prior `crest_nocalib` line because calibration has been
removed and no other scoring module was changed.
