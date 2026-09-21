# Integration matrix

| Mechanism | Destination | Action | Automation | Rationale |
|---|---|---|---|---|
| legal/admin register detection | `editing` | enrich model guidance | MODEL_ONLY | requires genre/task context |
| legal substyle distinctions | `editing` | provenance/model guidance | MODEL_ONLY | insufficient signal from surface form alone |
| precision + controlled indeterminacy | `editing` | anti-rule / model guidance | MODEL_ONLY | semantic/legal function required |
| positive vs negative redundancy | `editing` | contextual evals | MODEL_ONLY | repetition may be necessary |
| nominalization/passive/impersonality | `editing` | preserve-function guidance | MODEL_ONLY | forms are not errors by themselves |
| legal economy | `editing` | provenance/model guidance | MODEL_ONLY | supports anti-blacklist |
| intertextuality / term repetition | `editing` | preservation guidance | MODEL_ONLY | synonymization can damage meaning |
| administrative formula cluster in explicit plain/conversational profile | `editing` | combined-source support for `sr_register_admin_formula_cluster` | EXTENDED_MECHANICAL | cluster + explicit non-admin profile avoids treating legal/admin formulas as errors in their native register |
| historical Serbian examples | provenance only | retain source-period status | NONE | not modern norm |
| sentence-length threshold | none | reject | NONE | source provides no safe threshold |
| passive/-nje blacklist | none | reject | NONE | invalid across legitimate legal text |

## Runtime decision

- New hard gates: **0**.
- This source supports one **combined-source, profile-gated** mechanical register-mismatch heuristic; it does not justify passive, nominalization or sentence-length checks.
- Model-level guidance: **yes**.
- Source-study evals: **yes**.
- Public-source provenance: **yes**.
