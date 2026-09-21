# Loss and overgeneralization audit

## Loss audit

- The complete supplied PDF text was traversed.
- All five major functional styles are represented.
- The theoretical foundation (selection/combination, norm distinction, communication model, information model) is retained rather than reducing the book to style checklists.
- Interstyles, substyles, genres and productive switching are preserved.
- Economy and redundancy are both retained as positive functional tendencies depending on task.
- Positive resources are retained for each style:
  - literary markedness and aesthetic structure;
  - publicistic accessibility/persuasion;
  - scientific abstraction/precision;
  - administrative standardization/reliability;
  - conversational ellipsis/contextual economy.
- Source-period and cross-language limitations are explicit.
- No copyrighted example inventory is copied.

## Overgeneralization audit

Rejected blanket rules:

- “Scientific prose should be simple and short.”
- “Administrative templates are machine-like.”
- “Clichés are always bad style.”
- “Repeated headings imply AI.”
- “Fragments are bad Serbian.”
- “Spoken text is conversational style.”
- “Written text is formal style.”
- “Expressiveness is inappropriate outside literature.”
- “Redundancy is always verbosity.”
- “Economy always improves prose.”
- “One document has one immutable register.”
- “Stylistic norm is as obligatory as language norm.”
- “Features described in 2002 define current Serbian norm.”

## AI-style audit

Structural regularity and formulaic repetition can be legitimate features of high-standardization genres. Existing AI diagnostics therefore remain soft signals. When the caller explicitly supplies `administrative`, `legal` or `documentation`, repeated-section-scaffold and dense-heading findings are now mechanically suppressed.

## Norm boundary

No modern Serbian grammatical/orthographic hard rule is derived from this book.

## Automation audit

Automatic register inference from surface features remains unsafe. Once a profile is supplied externally, however, two safe kinds of automation become possible:

1. **false-positive suppression** for structured genres;
2. **cluster-based register mismatch** in explicitly `plain` / `conversational` text.

A single administrative phrase never triggers the mismatch rule; at least three distinct markers are required.

**Final automation decision: 1 EXTENDED_MECHANICAL finding + 2 DEFAULT_MECHANICAL suppressions; 0 hard gates.**
