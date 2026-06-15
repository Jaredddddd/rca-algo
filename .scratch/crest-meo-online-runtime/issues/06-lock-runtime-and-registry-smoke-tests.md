# Lock Runtime And Registry Smoke Tests

Status: ready-for-agent
Type: AFK

## Parent

.scratch/crest-meo-online-runtime/PRD.md

## What to build

Update the CREST-MEO smoke and regression tests so they lock the intended online architecture: no old `crest` registry entry, CREST-MEO as the only core algorithm, ablations on the CREST-MEO path, role membership from MEOL, and no extracted fast path in online instantiation.

This slice is complete when tests catch accidental reintroduction of old CREST entry points, Python role constants as runtime source of truth, or name-based extracted materialization.

## Acceptance criteria

- [ ] Registry tests assert `crest` is not registered and `crest_meo` plus ablations remain registered.
- [ ] Canonical module tests assert CREST-MEO algorithm classes live in the CREST-MEO algorithm module, not the old scorer module.
- [ ] Runtime tests assert role membership is read from MEOL specs.
- [ ] Instantiation tests assert deployable MEOL calls generic compiler execution rather than a name-based extracted matrix path.
- [ ] Strict failure tests assert online instantiation raises by default.

## Blocked by

- .scratch/crest-meo-online-runtime/issues/04-switch-online-instantiation-to-strict-generic-path.md
