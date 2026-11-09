# Stop Slop → Serbian: source audit and pilot

Source: [Hardik Pandya, *Stop Slop*](https://github.com/hardikpandya/stop-slop) (MIT; consulted 2026-11-09).
Source files examined: `SKILL.md`, `references/structures.md`, `references/phrases.md`, `references/examples.md`.
This is a project-authored analysis and set of Serbian examples, not a translation or wholesale copy of the upstream rules.

## What the source actually claims

Stop Slop flags metacommentary, repeated contrast/negative patterns, rhythmic sameness, vague significance claims, pseudo-aphorisms and ostensibly agentless events. It also advocates global removal of adverbs, passive voice, em dashes, three-item lists and wh-question openings. Those universal bans are editorial preference, **not** evidence of Serbian ungrammaticality or AI authorship.

One upstream before/after example deletes *most* from *most teams*, widening a quantified claim. We explicitly reject that operation.

## Integration matrix

| Phenomenon | Serbian classification | Decision | Overlap / reason |
|---|---|---|---|
| Repeated negative contrasts | `AI_STYLE_SIGNAL` | Already operational | `sr_ai_negative_parallelism_density` |
| Repeated triplets | `AI_STYLE_SIGNAL` | Already operational | `sr_ai_triplet_density`; individual triplets protected |
| Repeated section templates | `AI_STYLE_SIGNAL` | Already operational | `sr_ai_repeated_section_scaffold` |
| Excessive micro-headings | `AI_STYLE_SIGNAL` | Already operational | `sr_ai_heading_fragmentation` |
| Repeated explicit editorial self-announcements | `AI_STYLE_SIGNAL` | **Pilot**, soft, document-level | New `sr_ai_metadiscourse_density` |
| Repeated rhetorical question immediately answered | `AI_STYLE_SIGNAL` | Research candidate | FAQ, interview, polemic and dialogue controls needed |
| Identical paragraph punchlines / rhythm | `METRIC_ONLY` initially | Research candidate | Genre and author voice influence rhythm |
| Claim of significance without a referent | `EDITING` / `MODEL_ONLY` | Research candidate | Needs preceding/following context and exact claim scope |
| Human agent hidden by abstraction | `EDITING` / `MODEL_ONLY` | Research candidate | Legitimate impersonal and metonymic Serbian |
| Generic philosophical aphorism | `EDITING` / `MODEL_ONLY` | Research candidate | Philosophical register is not a defect |
| Ban adverbs, passive, long dash, wh-openers | None | **Rejected** | Normal Serbian usage; can change agency, modality or focus |

## Pilot rule: repeated explicit metadiscourse

Only count conspicuous sentence-initial announcements of the writing process, not every `važno je`, `zato` or rhetorical question. Examples of candidate surface families: `U nastavku ćemo objasniti...`, `Hajde da pogledamo...`, `Kao što ćemo videti...`.

A single natural occurrence is clean. The pilot requires at least **eight prose sentences** and at least **`max(3, ceil(N/6))` instances**, where `N` is the number of prose sentences; it excludes Markdown headings, list items, Markdown blockquotes and fenced code, and returns a **soft** candidate only. It is disabled by default; run with `python scripts/check.py --experimental text.md` or `review(text, experimental=True)`. These numbers are conservative initial gates for a pilot, **not calibrated population thresholds**. The finding must not trigger an automatic edit or imply AI authorship. The original Cyrillic/Latin surface is preserved in the evidence.

Counterexamples: course instructions (`U nastavku ćemo...` as a real navigation aid), academic metadiscourse, intentional recurring catchphrases, transcripts, scripts and lesson plans. These require contextual review even above the threshold.

## Hard invariants

- `USER_INTENT + SEMANTICS + NORM` always wins.
- Preserve negation, quantifiers (`većina`, `neki`, `svi`), agency, modality, attribution, register, argument structure and factual claims.
- Do not generate facts, actors or numbers merely to make prose more specific.
- Preserve Ekavian/Ijekavian and both Serbian scripts.
- Do nothing when a candidate has a rhetorical function.
- A pattern is not proof of machine authorship.

## Validation and next gate

The opt-in pilot is an `AI_STYLE_SIGNAL` inside the existing Serbian runtime; positive, negative, boundary and script-preservation tests accompany it. This source has not undergone external corpus calibration. Measure false-positive cases across editorial, educational, political, technical and literary Serbian before tightening thresholds or promoting other source hypotheses. No numerical human-likeness score.

## Implementation notes after review

- Do not extrapolate a local cluster from the global document density. The 1/6 gate is provisional and not corpus-validated; local-window analysis needs its own tests.
- The parser preserves blank-line paragraph boundaries but treats soft-wrapped lines in the same paragraph as continuous prose.
- Ekavian and Ijekavian forms (`videti`/`vidjeti`, `sledećem`/`sljedećem`) are accepted without rewriting the original script.
- Markdown fences close only on the same marker type, with at least the opening length and no trailing info string.
- JSONL evaluations are executed by a dedicated unittest rather than being merely stored examples.

## Additional parser regression coverage

- The experimental sentence denominator ignores common Serbian abbreviations (including npr.) and decimal points (for example, 3.14); the four existing operational checks retain their prior parser.
- Markdown thematic breaks, Setext headings and indented code blocks at block boundaries do not count as prose sentences.
- Seed JSONL tests reject unexpected positive findings, except for explicitly declared allowed_extra rule IDs for overlapping diagnostics.
- These remain conservative heuristics and do not replace a linguistically validated sentence segmenter.
