# Architecture

`humanizer_serbian` is Serbian-only. `humanizer_russian` is an architectural reference, not a runtime dependency.

## Decision hierarchy

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Selection among allowed forms:

`AUTHOR > NATIVE_USAGE > EDITING > INTERFERENCE > AI_STYLE_SIGNAL`

## Layers

### `libraries/serbian_norm`
Modern Serbian norm and language constraints. Only independently supported normative findings may become hard gates.

### `libraries/native_usage`
Natural Serbian usage, information structure, collocation, register, ellipsis, repetition, clitics and variant choice. Corpus frequency is evidence here, not norm.

### `libraries/editing`
Serbian editorial principles that operate among already valid alternatives.

### `libraries/interference_en`
English-to-Serbian transfer and calques.

### `libraries/interference_ru`
Russian-to-Serbian transfer and calques. Kept separate because the mechanisms and false positives differ from English interference.

### `libraries/ai_style`
Accumulated document-level diagnostics associated with formulaic LLM prose. Never proof of authorship.

### `evidence/`
External corpus/data providers. Evidence providers do not become reviewer voices.

### `studies/`
Source ingestion area. Every substantial book/source should be processed here before integration: provenance, scope, claims, counterexamples, modern-norm audit, automation feasibility, eval cases, integration mapping.

## Script handling

Rules may normalize Cyrillic and Latin to a common matching representation, but findings must preserve the original text surface. Script conversion is never an implicit edit.

## Variant handling

Ekavian and Ijekavian are first-class variants. A future profile may configure one for consistency, but the other remains valid unless the task explicitly requires normalization.

## Automation levels

- `HARD_GATE`: independently established language constraints only.
- `DEFAULT_MECHANICAL`: high-precision deterministic findings with explicit negative tests.
- `EXTENDED_MECHANICAL`: useful but noisier deterministic diagnostics.
- `MODEL_ONLY`: contextual judgments unsafe to reduce to regex/counts.
- `PROJECT`: planned source/provider not yet operational.

## Promotion rule

No candidate becomes a mechanical rule merely because it appears in a book, corpus, detector article or community complaint. Promotion requires a defined phenomenon, source provenance, counterexamples, false-positive tests and a justified automation level.
