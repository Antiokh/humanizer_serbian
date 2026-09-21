# Integration matrix

| Mechanism | Destination | Action | Automation | Rationale |
|---|---|---|---|---|
| directness ≠ impoliteness | `native_usage` | model guidance + anti-rule | MODEL_ONLY | strongly context-dependent |
| Serbian corpus tendency toward pragmatic clarity | `native_usage` | provenance/model guidance | MODEL_ONLY | film-corpus tendency |
| discourse markers/hedges as functional | `native_usage` + `editing` | preserve-function guidance | MODEL_ONLY | lexical presence alone is ambiguous |
| address / familiarity / power | `native_usage` | context model | MODEL_ONLY | requires relationship context |
| English→Serbian indirectness shift | `interference_en` | new pragmatic-transfer phenomenon | MODEL_ONLY | translation/cultural/technical causes overlap |
| interactional loss in translation | `interference_en` + `editing` | model guidance + evals | MODEL_ONLY | proposition can survive while stance changes |
| `ti/vi` prescriptive choice | `serbian_norm` | no promotion | PROJECT | independent current norm/usage evidence required |
| imperative tolerance claim | `serbian_norm` | no promotion | PROJECT | contrastive claim, not enough for norm |
| film-corpus ratios | provenance only | retain with scope | NONE | not a runtime rule |
| directness/hedge regex | none | reject | NONE | false-positive rate inherently high |

## Runtime decision

- New deterministic checks: **0**
- New hard gates: **0**
- Model-level guidance: **yes**
- Source-study evals: **yes**
- Public-source provenance: **yes**
