# humanizer_serbian

Serbian editor/humanizer focused on natural, precise Serbian rather than AI-detector evasion.

The project is a standalone Serbian sibling of `humanizer_russian`: it reuses the architectural principles, source discipline and evaluation approach, but it does **not** import Russian rules, libraries or runtime files.

## Core policy

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Choice among valid Serbian alternatives:

`AUTHOR > NATIVE_USAGE > EDITING > INTERFERENCE > AI_STYLE_SIGNAL`

`Do nothing` is a valid result.

## Serbian-specific principles

- Serbian Cyrillic and Serbian Latin are first-class scripts.
- Ekavian and Ijekavian are legitimate standard variants.
- Preserve the author’s script and variant unless an explicit request or concrete language problem requires a change.
- Keep modern norm separate from corpus frequency, editorial taste, contact-language interference and AI-style diagnostics.
- Keep English-to-Serbian and Russian-to-Serbian interference as independent libraries.
- Treat AI-looking patterns as accumulated document-level signals, never proof of authorship.
- Do not create blacklists of punctuation, common Serbian words or normal rhetorical constructions.
- Treat functional profile as an input/context signal rather than pretending that register can be inferred safely from a few surface markers.

## Repository structure

- `scripts/` — deterministic checks and utilities.
- `libraries/` — long-lived Serbian knowledge libraries.
- `evidence/` — corpus and external-data providers; evidence is not a reviewer voice.
- `studies/` — source-by-source extraction and audit before integration.
- `evals/` — positive, negative and boundary cases.
- `tests/` — deterministic regression tests and false-positive guards.
- `docs/` — architecture, public sources, hypotheses and project status.

## Current executable pass

Document-level `AI_STYLE_SIGNAL` diagnostics:

- repeated `nije … već/nego …` contrast scaffolds;
- repeated three-member enumerations;
- repeated section-heading scaffolds;
- excessive micro-heading fragmentation.

Profile-gated `EXTENDED_MECHANICAL` diagnostics:

- `sr_register_admin_formula_cluster` — accumulated administrative formulae in explicitly `plain` / `conversational` text;
- `sr_en_stacked_mitigation` — at least three distinct mitigation/indirectness markers in one sentence in explicitly `plain` / `conversational` text.

Mechanical false-positive guards:

- `administrative`, `legal` and `documentation` profiles suppress repeated-section-scaffold and dense-heading AI signals because structural regularity can be genre-functional.

Register/interference heuristics do **not** run in `auto`; the caller must explicitly supply a profile. All findings are soft diagnostics, not `NORM` findings.

```bash
python3 scripts/check.py text.md
python3 scripts/check.py --json text.md
python3 scripts/check.py --profile conversational text.md
python3 scripts/check.py --profile administrative text.md
python3 -m unittest discover -s tests
```

See `SKILL.md` for editing policy and `docs/public_sources.md` for the current public-source baseline.
