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

## Repository structure

- `scripts/` — deterministic checks and utilities.
- `libraries/` — long-lived Serbian knowledge libraries.
- `evidence/` — corpus and external-data providers; evidence is not a reviewer voice.
- `studies/` — source-by-source extraction and audit before integration.
- `evals/` — positive, negative and boundary cases.
- `tests/` — deterministic regression tests and false-positive guards.
- `docs/` — architecture, public sources, hypotheses and project status.

## Current seed

The initial executable pass contains conservative document-level diagnostics for:

- repeated `nije … već/nego …` contrast scaffolds;
- repeated three-member enumerations;
- repeated section-heading scaffolds;
- excessive micro-heading fragmentation.

These are `AI_STYLE_SIGNAL` findings, not `NORM` findings. A single occurrence is intentionally ignored.

```bash
python3 scripts/check.py text.md
python3 scripts/check.py --json text.md
python3 -m unittest discover -s tests
```

See `SKILL.md` for editing policy and `docs/public_sources.md` for the current public-source baseline.
