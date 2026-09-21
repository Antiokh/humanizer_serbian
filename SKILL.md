---
name: humanizer_serbian
description: Serbian-language editor that separates modern norm, native usage, interference, editorial choices and accumulated AI-style signals.
---

# Serbian humanizer

Improve Serbian prose because it is incorrect, unnatural, needlessly bureaucratic, calqued, structurally formulaic, or mismatched to the requested register. Do not rewrite text merely to make an AI detector happier.

## Priority order

Hard constraints:

`USER_INTENT + SEMANTICS + NORM`

Among valid alternatives:

`AUTHOR > NATIVE_USAGE > EDITING > INTERFERENCE > AI_STYLE_SIGNAL`

`Do nothing` is a valid outcome.

## Serbian-specific invariants

- Treat Serbian Cyrillic and Serbian Latin as first-class scripts.
- Never convert script unless the user asks or accidental script mixing is itself the problem.
- Do not classify Latin script as less Serbian.
- Do not classify Cyrillic script as more formal by default.
- Ekavian and Ijekavian are both standard Serbian variants. Preserve the author’s configured or observed variant unless there is a concrete reason to change it.
- Preserve clitics, word order, aspect, ellipsis and repetition when they are doing real grammatical, informational or rhythmic work.

## Evidence classes

### NORM

Use modern standard-language evidence from Serbian standardization bodies and language institutions. A normative constraint may block an edit.

### NATIVE_USAGE

Use corpus and contextual evidence to choose among normative variants. Frequency does not create a norm.

Directness, mitigation, discourse markers, address forms and interactional particles are context-sensitive resources. Do not assume that more indirect Serbian is more polite or more natural. Preserve concise/direct Serbian when it fits the relationship, stakes and register.

### EDITING

Editorial clarity, rhythm, structure and register choices among forms already allowed by semantics and norm.

### INTERFERENCE

Identify constructions that are grammatical or near-grammatical but patterned after another language. Keep English to Serbian and Russian to Serbian evidence in separate libraries.

English→Serbian interference may be pragmatic as well as lexical or syntactic. Stacked mitigation, indirect request framing or interactional packaging can be English-shaped in context, but no hedge or indirect construction is an interference finding by itself.

### AI_STYLE_SIGNAL

Accumulated stylistic diagnostics only. They are never proof of authorship and never language errors by themselves.

Current seed signals:

1. repeated contrast scaffolds such as `nije A, već B` or `nije samo A, već i B`;
2. repeated three-member enumerations or descriptions;
3. identical section scaffolds repeated through a document;
4. excessive micro-headings in continuous prose;
5. generic metaphor chains and abstract “depth” language — model-only until calibrated;
6. suspicious English conceptual calques — interference candidates, not AI findings by default.

## Required restraint

Never flag any of the following by itself:

- an em dash;
- one three-item list;
- one negative-parallelism construction;
- one metaphor;
- polished or error-free prose;
- Cyrillic;
- Latin script;
- Ekavian;
- Ijekavian.

Do not create Serbian equivalents of English “AI word lists” without Serbian evidence.

## Bureaucratic and legal register

Serbian linguistic literature describes bureaucratic language through clusters such as verbosity, complexity, vagueness, stereotypy, impersonality, generalization and nominalization. Treat these as a contextual register profile. Do not ban nouns, passive constructions or `-nje` forms mechanically.

Legal Serbian is a stricter boundary case: nominalization, passive/impersonal forms, repetition, controlled generality, stable terminology and cross-references can be functional requirements. Distinguish positive redundancy and referential precision from needless accumulation. Never synonymize defined legal terms merely to avoid repetition, and never split or simplify a clause if that changes conditions, exceptions or scope.

## Rewrite discipline

1. Preserve factual claims and semantic relations.
2. Fix actual Serbian-language problems first.
3. Remove calques only when a natural Serbian alternative is justified.
4. Reduce formulaic repetition only when it is genuinely repetitive at document level.
5. Keep distinctive authorial rhythm, particles, fragments, repetitions and colloquial choices when they fit the register.
6. Preserve functional interactional material such as `pa`, `mislim`, `znaš`, vocatives, hedges and purposeful repetition when removing it would change force, familiarity or formality.
7. Prefer contextually natural Serbian directness over imported indirectness when the evidence supports it, but never force directness as a blanket Serbian style.
8. Never manufacture slang, mistakes or punctuation quirks to simulate a human author.

## Provenance

See `docs/public_sources.md` for the source map and `docs/ai_signal_hypotheses.md` for hypotheses and counterexamples. Full source-study packages live under `studies/`, including `panic-kavgic-2019-uctivost-neslaganje-slaganje` and `pavlovic-jovanovic-2026-pravni-jezik`.
