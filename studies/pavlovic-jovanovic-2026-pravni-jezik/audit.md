# Loss and overgeneralization audit

## Loss audit

- All 12 pages of the supplied article were traversed.
- The legal-theory background was not mistaken for runtime grammar rules.
- Administrative/legal substyles, precision/indeterminacy, economy, redundancy, intertextuality and formalism are represented.
- Positive legal-language resources were preserved, not only “bad bureaucracy” examples.
- Historical material remains explicitly source-period.
- Secondary-literature nature of many claims is retained.

## Overgeneralization audit

Rejected blanket rules:

- “Nominalizations are bureaucratic errors.”
- “Passive is bad Serbian.”
- “Long legal sentences should always be split.”
- “Repetition is poor style.”
- “Vagueness should always be removed.”
- “Legal language is one uniform register.”
- “Anything common in legal prose is correct.”
- “Historical examples represent current standard Serbian.”

## Norm boundary

No modern normative constraint is derived from this article alone.

## Automation audit

Surface checks for `-nje`, passive morphology, sentence length, repeated nouns or legal connectives remain rejected.

A narrower combined-source heuristic is acceptable only when the caller **already states** that the target is `plain` or `conversational`: three or more distinct administrative formula markers can then flag a probable register mismatch. The same language is suppressed in administrative/legal profiles.

**Final automation decision: support `sr_register_admin_formula_cluster` as EXTENDED_MECHANICAL under explicit non-admin profiles; 0 hard gates.**
