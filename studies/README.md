# Source-study protocol

Every substantial Serbian source must be processed here before any claim enters a runtime library. The protocol is intentionally stricter than a normal book summary: its job is to prove what was actually read, preserve provenance, separate author opinion from current norm, expose counterexamples, and prevent loss or overgeneralization during integration.

The Russian humanizer is an architectural precedent only. Serbian studies must use Serbian evidence, Serbian norm and Serbian examples.

## Required source folder

Create `studies/<source-slug>/` and produce the following artifacts as applicable.

### 1. `source.md` — source identity and access

Record:
- author, title, edition, year, publisher/host;
- ISBN/DOI/stable URL where available;
- exact digital artifact actually used (PDF/EPUB/HTML/scans/etc.);
- whether text is embedded, OCR-derived or image-only;
- licensing/access notes;
- scope available to the project and any inaccessible portions;
- edition-specific risks.

Never reconstruct missing text from a table of contents, reviews or citations.

### 2. `coverage.md` — completeness proof

Prove traversal rather than saying “book reviewed”. Record, as applicable:
- pages available / pages traversed;
- chapters/sections/paragraphs available / traversed;
- table-of-contents reconciliation;
- missing pages, unread tails, corrupt scans or OCR gaps;
- structural map of source blocks to project decision areas.

If coverage is partial, every downstream artifact must say so.

### 3. `concepts.md` — source model

Extract the source’s reusable conceptual model in project language:
- what distinctions the author makes;
- what the author treats as norm, style, register, meaning, rhetoric or usage;
- what mechanisms recur across chapters;
- what positive resources should be preserved, not merely what should be removed.

Do not turn examples into rules at this stage.

### 4. `claims.md` — claims ledger

Create a traceable ledger of material claims. For each claim record:
- normalized claim;
- source location;
- claim type (`NORM_CANDIDATE`, `NATIVE_USAGE`, `EDITORIAL`, `INTERFERENCE`, `AI_STYLE_SIGNAL`, historical/source-period claim, etc.);
- current project handling;
- confidence and unresolved questions where relevant.

A source claim is not automatically a language rule.

### 5. `observations*.json` or `observations.jsonl` — atomic source cards

For substantial structured works, create atomic observations at the smallest useful source unit (section, numbered paragraph, phenomenon, or equivalent).

Each observation should retain at least:
- stable observation ID;
- source location;
- phenomenon;
- author claim/observation in paraphrase;
- examples represented minimally or replaced with project-authored examples when copyright requires it;
- project classification;
- candidate target library;
- current-norm status;
- automation feasibility;
- counterexample/boundary notes.

Atomic coverage should reconcile with `coverage.md`.

### 6. `current-norm.md` — modern Serbian norm audit

Any prescriptive, grammatical, orthographic, lexical-government, punctuation or standard-language claim that may become `NORM` must be independently checked against current Serbian normative/institutional evidence.

Record statuses explicitly, for example:
- `CURRENT_CONFIRMED`;
- `CURRENT_CONFIRMED_WITH_BOUNDARY`;
- `SOURCE_PERIOD`;
- `EDITORIAL_ONLY`;
- `CONFLICTING_SOURCES`;
- `UNVERIFIED`.

Historical authority, author prestige and corpus frequency do not create current norm.

### 7. `counterexamples.md` or `counterexamples.jsonl` — anti-rules

Record cases that invalidate naive generalization. Typical examples:
- a construction criticised in one register but legitimate in another;
- a pattern that is wrong only under a specific government/meaning boundary;
- a stylistic tendency that must not become a blacklist;
- a phenomenon valid in both Ekavian and Ijekavian variants;
- ordinary Cyrillic/Latin behavior that must not be treated as an error;
- examples where preserving complexity, repetition, ellipsis or rhetoric is correct.

### 8. `eval-map.json` and `evals.json` / `evals.jsonl` — executable evaluation plan

Map source mechanisms to project eval IDs, then create project-authored positive, negative and boundary cases.

No mechanical rule may be promoted without negative tests designed to catch its most plausible false positives.

### 9. `interactions.md` — overlap and conflict analysis

Compare the source with existing Serbian libraries and other reviewed sources:
- duplicate mechanisms;
- complementary mechanisms;
- genuine disagreement;
- narrower/wider scope;
- norm vs editorial conflicts;
- English-interference vs Russian-interference distinctions;
- cases where one long-lived rule should gain provenance instead of creating a duplicate reviewer voice.

### 10. `integration-matrix.md` — destination decision

For every source area or atomic mechanism decide:
- existing rule/library to enrich;
- new phenomenon identity if genuinely unique;
- provenance-only;
- eval-only;
- model-only;
- deterministic candidate;
- rejected/no-op.

State the proposed automation level (`HARD_GATE`, `DEFAULT_MECHANICAL`, `EXTENDED_MECHANICAL`, `MODEL_ONLY`, `PROJECT`) and why.

### 11. `audit.md` — loss and overgeneralization audit

Before integration, explicitly test two failure modes.

**Loss audit:**
- Were all traversed structural units represented?
- Did any unique mechanism disappear because it looked similar to an existing rule?
- Were positive expressive resources preserved?
- Were source-period inventories retained as provenance even if not promoted?

**Overgeneralization audit:**
- Which tempting blanket rules are invalid?
- Which register-specific claims must remain contextual?
- Which current-norm boundaries block a mechanical implementation?
- Which examples would become false positives under a regex/word-list implementation?

Conclude with an automation decision, including `0 mechanical checks` when that is the correct result.

## Processing order

1. Acquire and identify the exact source.
2. Establish coverage and structural map.
3. Extract concepts, claims and atomic observations.
4. Audit current Serbian norm where applicable.
5. Build counterexamples and evals.
6. Compare against existing libraries and source conflicts.
7. Produce integration matrix.
8. Run loss/overgeneralization audit.
9. Only then modify runtime libraries or deterministic checks.

## Global rules

1. Do not reconstruct inaccessible chapters or missing pages.
2. Publicly readable copyrighted works are research sources, not text to copy into the repository.
3. Prefer paraphrase, formalized observations and project-authored examples; retain precise source locations for provenance.
4. A source observation is not automatically `NORM`.
5. Corpus frequency supports `NATIVE_USAGE`; it does not create norm.
6. Repeated mechanisms enrich one long-lived library instead of creating duplicate reviewer voices.
7. Source conflicts remain explicit until resolved by stronger evidence or a scope distinction.
8. Serbian Cyrillic/Latin and Ekavian/Ijekavian boundaries must be respected during source interpretation.
9. English→Serbian and Russian→Serbian interference are separate evidence tracks.
10. `Do nothing` and `provenance only` are valid integration results.