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
- Deterministic register classifier / bureaucratic-register checker.
- srWaC calibration provider.
- Model-based contextual review.

These remain `PROJECT` work until their sources, contracts, examples and false-positive behavior are validated.

## 21 September 2026 — first full source studies

Completed the repository's full source-study protocol for:

- Olga Panić Kavgić (2019), pragmatic agreement/disagreement and English→Serbian subtitle transfer;
- Jelena M. Pavlović Jovanović (2026), Serbian legal-language functional style;
- Branko Tošović (2002), general functional-style theory covering literary, publicistic, scientific, administrative and conversational styles.

Results:

- source-backed model guidance added for Serbian directness/mitigation, discourse markers and English pragmatic interference;
- legal-register boundaries added for nominalization, passive/impersonal forms, repetition, controlled generality, terminology and cross-references;
- a general functional-style gate added: communicative function, genre, audience and channel now precede stylistic cleanup;
- stylistic norm is explicitly separated from standard-language norm;
- administrative/publicistic standardization and recurring templates are recorded as AI-style false-positive boundaries;
- project-authored contextual evals and anti-rules added inside both study packages;
- no source claim was promoted to modern Serbian `NORM`;
- **0 new mechanical checks** were justified by these studies.

The next calibration need is corpus/dialogue evidence for pragmatic transfer and independent current normative evidence for any future hard rule.

## Current policy

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Choice among allowed Serbian forms:

`AUTHOR > NATIVE_USAGE > EDITING > INTERFERENCE > AI_STYLE_SIGNAL`

`Do nothing` remains a first-class result.
