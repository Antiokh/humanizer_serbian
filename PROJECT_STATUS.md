# Project status

## 28 August 2026 — standalone Serbian bootstrap

Canonical repository: `Antiokh/humanizer_serbian`.

The project is Serbian-only. The Russian humanizer is used as an architectural reference but is not a dependency and does not host Serbian rules.

### Operational seed

- Serbian Cyrillic-to-Latin internal normalization for matching without rewriting the source.
- Four conservative document-level `AI_STYLE_SIGNAL` checks:
  - repeated negative/contrast parallelism;
  - repeated triplets;
  - repeated section scaffolds;
  - dense micro-headings.
- Regression tests for both Serbian scripts and explicit anti-rules.
- Public-source provenance map.
- Separate architecture for modern norm, native usage, editing, English interference, Russian interference and AI-style diagnostics.

### Not yet operational

- Serbian normative hard gates.
- Corpus-backed native-usage rules.
- English-to-Serbian interference library.
- Russian-to-Serbian interference library.
- Bureaucratic-register model.
- srWaC calibration provider.
- Model-based contextual review.

These remain `PROJECT` work until their sources, contracts, examples and false-positive behavior are validated.

## Current policy

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Choice among allowed Serbian forms:

`AUTHOR > NATIVE_USAGE > EDITING > INTERFERENCE > AI_STYLE_SIGNAL`

`Do nothing` remains a first-class result.
