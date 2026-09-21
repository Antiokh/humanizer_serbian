# Loss and overgeneralization audit

## Loss audit

- Full artifact structure was traversed.
- Core empirical blocks for disagreement, agreement, cross-language comparison, context and subtitle translation are represented.
- Positive Serbian resources were retained: directness, particles, address, concise contradiction, repetition and solidarity markers.
- Subtitle findings were not reduced to “Serbian is more direct”; interactional loss and technical constraints are retained.
- Source limitations (film dialogue, qualitative sample, prosody/non-verbal exclusions) are explicit.
- No copyrighted dialogue inventory was copied.

## Overgeneralization audit

Rejected blanket rules:

- “Serbian should be direct.”
- “Indirect Serbian is an English calque.”
- “Direct disagreement is rude.”
- “Hedges make text artificial.”
- “Discourse markers are filler.”
- “Use `vi` in formal-looking text.”
- “Subtitles reveal native preference independent of technical constraints.”
- “Film-corpus ratios describe Serbian speakers generally.”

## Norm boundary

No source observation is promoted to modern Serbian `NORM`.

## Automation audit

Generic directness or hedge detection remains unsafe. One narrower pattern is mechanically useful after adding an explicit functional profile: a single sentence containing at least three **distinct** mitigation/indirectness markers in `plain` or `conversational` text. The same text stays clean in `auto` and `formal`.

This is an `INTERFERENCE` review signal, not a language error and not evidence of AI authorship.

**Final automation decision: 1 EXTENDED_MECHANICAL check — `sr_en_stacked_mitigation`; 0 hard gates.**
