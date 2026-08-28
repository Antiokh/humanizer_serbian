# Public-source baseline

This document tracks public sources usable for the Serbian humanizer. Source authority and function must stay explicit.

## Evidence classes

1. `NORM` — modern Serbian standard-language constraints backed by standardization bodies and language institutions.
2. `NATIVE_USAGE` — attested Serbian usage, collocations, information structure and register.
3. `INTERFERENCE` — contact-language effects, with English and Russian kept separate.
4. `AI_STYLE_SIGNAL` — recurring stylistic patterns associated with LLM-generated Serbian. Diagnostic only; never proof of authorship.

## Normative and institutional sources

### Odbor za standardizaciju srpskog jezika

- https://www.ossj.rs/
- Public decisions, recommendations, corrections, positions and explanations concerning Serbian standard language.
- Treat each decision according to its scope; do not generalize a narrow recommendation without independent support.

### Institut za srpski jezik SANU — Odsek za standardni jezik

- https://www.isj.sanu.ac.rs/odseci/odsek-za-standardni-jezik/
- Institutional work on description and modernization of contemporary Serbian norm.

### Rečnik lingvističkih termina

- https://www.lingvistickitermini.rs/
- Useful for formalized stylistic and linguistic concepts.
- `Birokratski jezik` is described through properties including verbosity, complexity, vagueness, stereotypy, impersonality, generalization and nominalization. Model these as a register cluster, not automatic errors.

## Corpus evidence

### srWaC 1.1

- https://www.clarin.si/repository/xmlui/handle/11356/1063
- Serbian web corpus, approximately 555M tokens / 25.6M sentences / 1.35M texts.
- CC BY-SA 4.0.
- Paragraph-deduplicated, morphosyntactically annotated and lemmatized.
- Intended use: empirical calibration of collocations, phrase frequencies and false-positive rates.
- Corpus frequency supports `NATIVE_USAGE`; it never creates `NORM` by itself.

## Contact linguistics

### Tvrtko Prćić — Engleski u srpskom

- Official digital-library entry: https://digitalna.ff.uns.ac.rs/sadrzaj/2019/978-86-6065-512-9
- Use as research provenance for English-to-Serbian interference.
- Public readability does not imply a license to copy the book text into this repository. Store formalized observations, citations/provenance and original project examples instead.

### Tvrtko Prćić — Srpski sa engleskim

- Author/institution page: https://www.ff.uns.ac.rs/sr-lat/fakultet/odseci/anglistika/zaposleni/tvrtko-prcic
- Candidate source for contact and contrastive mechanisms; process through `studies/` before library integration.

## Public analyses of AI-generated Serbian

### Bojan Viculin — “Razotkrivanje šablona AI (VI) generisanog teksta”, P.U.L.S.E, 25 Apr 2026

- https://pulse.rs/razotkrivanje-sablona-vi-generisanog-teksta/
- Serbian analysis of a long text suspected of heavy LLM generation.
- Recurrent observations include:
  - negative contrast templates: `A nije B, već C`, `A nije samo B, već i C`, `Ne samo A, već i B`;
  - repeated three-part enumerations and three-adjective/adverb descriptions;
  - unusually smooth transitions and formulaic organization;
  - excessive micro-headings;
  - repeated grand metaphors and hyperbole;
  - generic/content-light assertions;
  - contextual English-derived phrases such as `alat za razumevanje`;
  - repetitive sentence architecture and lexical frames.

Encode these as `AI_STYLE_SIGNAL` or `INTERFERENCE`, not `NORM`, unless independent normative evidence establishes an actual language error.

## Community hypothesis material

Community discussions may generate hypotheses and counterexamples but are not normative evidence.

- r/AskSerbia, “Kako prepoznajete Ai tekst?”: punctuation such as em dashes is socially used as an AI cue while human users explicitly report long-standing use. This is evidence against dash-removal rules.
- r/serbia discussions have pointed to exact repetition of section labels across many measures as a conspicuous generation template. This supports document-level repetition metrics.
- r/Serbian discussions sometimes interpret learner errors as evidence that a text is not ChatGPT. Fluency itself therefore has social associations but is not a valid standalone detector signal.

## Source discipline

- Public availability is not the same as an open content license.
- Store provenance, extracted mechanisms, project-authored examples and tests; do not reproduce copyrighted books.
- A stylistic authority cannot create a language error merely by authority.
- Historical advice must be audited against modern Serbian norm before integration.
- Frequency and community opinion are evidence of usage/perception, not norm.
