# Source-study template

Copy this folder to `studies/<source-slug>/` and replace this file with `source.md` when beginning a new source.

Expected study package:

- `source.md`
- `coverage.md`
- `concepts.md`
- `claims.md`
- `observations.jsonl` or chunked `observations-partN.json`
- `current-norm.md` when normative claims exist
- `counterexamples.md` or `counterexamples.jsonl`
- `eval-map.json`
- `evals.json` or `evals.jsonl`
- `interactions.md`
- `integration-matrix.md`
- `audit.md`

Completion gate: runtime integration is blocked until coverage, current-norm boundaries, false-positive evals, interaction analysis, integration mapping, and the loss/overgeneralization audit are complete or explicitly marked not applicable.