# Integration matrix

| Mechanism | Destination | Action | Automation | Rationale |
|---|---|---|---|---|
| directness ≠ impoliteness | `native_usage` | model guidance + anti-rule | MODEL_ONLY | strongly context-dependent |
| Serbian corpus tendency toward pragmatic clarity | `native_usage` | provenance/model guidance | MODEL_ONLY | film-corpus tendency |
| discourse markers/hedges as functional | `native_usage` + `editing` | preserve-function guidance | MODEL_ONLY | lexical presence alone is ambiguous |
| address / familiarity / power | `native_usage` | context model | MODEL_ONLY | requires relationship context |
| English→Serbian indirectness shift | `interference_en` | pragmatic-transfer guidance | MODEL_ONLY | translation/cultural/technical causes overlap |
| stacked mitigation in explicitly plain/conversational profile | `interference_en` | `sr_en_stacked_mitigation` | EXTENDED_MECHANICAL | only fires with explicit profile + ≥3 distinct mitigation markers in one sentence |
| interactional loss in translation | `interference_en` + `editing` | model guidance + evals | MODEL_ONLY | proposition can survive while stance changes |
| `ti/vi` prescriptive choice | `serbian_norm` | no promotion | PROJECT | independent current norm/usage evidence required |
| imperative tolerance claim | `serbian_norm` | no promotion | PROJECT | contrastive claim, not enough for norm |
| film-corpus ratios | provenance only | retain with scope | NONE | not a runtime rule |
| generic directness/hedge regex | none | reject | NONE | false-positive rate inherently high |

## Runtime decision

- New deterministic checks: **1 narrow EXTENDED_MECHANICAL heuristic**.
- New hard gates: **0**.
- The heuristic is opt-in through `plain` / `conversational` profile and suppressed in `auto`, `formal` and other profiles.
- Model-level guidance: **yes**.
- Source-study evals: **yes**.
- Public-source provenance: **yes**.
