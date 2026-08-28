# Serbian AI-style hypotheses

Status: research hypotheses for calibration. None of these signals proves AI authorship.

## H1 — contrast-template density

Repeated Serbian contrast frames such as `A nije B, već C`, `A nije samo B, već i C`, `Ne samo A, već i B`, and `Ne A, već B` may become formulaic at high density or in near-identical syntactic positions.

Source seed: Bojan Viculin, P.U.L.S.E, 2026.

Counterexample requirement: one occurrence is normal Serbian and must not trigger a finding.

## H2 — repeated triplets

Repeated three-member lists and descriptions with three coordinated adjectives/adverbs may form a document-level scaffold.

Source seed: Bojan Viculin, P.U.L.S.E, 2026.

Counterexample requirement: ordinary rhetorical triplets and factual lists are valid Serbian.

## H3 — structural over-regularity

Identical section labels, paragraph openings or internal mini-templates repeated across many sections are a stronger signal than individual “AI words”. Measure repetition/entropy rather than blacklist vocabulary.

## H4 — micro-heading density

Headings every few lines can make continuous generated prose mechanically partitioned.

Counterexample requirement: documentation, FAQs, API docs and slide-like notes legitimately use dense headings.

## H5 — generic metaphor chains

Repeated generic metaphors (`tkivo`, `arena`, `bojno polje`, `ogledalo`, `mašina`, etc.) combined with abstract claims may create an inflated generic register.

Status: model-only until calibrated. Individual metaphors are not findings.

## H6 — English conceptual calques

Literal conceptual transfers such as contextual `alat za razumevanje` may be grammatical yet unnatural in Serbian.

Classification: `INTERFERENCE`, not AI detection. Requires context and corpus validation.

## Rejected naive signals

### Em dash

Dash presence is a social stereotype and a required negative test, not a rule.

### Error-free prose

Polished grammar cannot be treated as evidence of AI authorship.

### Cyrillic vs Latin

Both scripts are normal Serbian. Script choice is not an AI signal.

### Ekavian vs Ijekavian

Both are legitimate standard variants and cannot be used as AI signals by themselves.
