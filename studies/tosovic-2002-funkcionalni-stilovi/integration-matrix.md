# Integration matrix

| Mechanism | Destination | Action | Automation | Rationale |
|---|---|---|---|---|
| style = selection + organization | `editing` / SKILL | core model guidance | MODEL_ONLY | text-level/contextual |
| language norm vs stylistic norm | architecture / SKILL | hard conceptual boundary | MODEL_ONLY | prevents style→NORM promotion |
| five functional-style profiles | `editing` / SKILL | profile taxonomy | MODEL_ONLY | real texts can mix profiles |
| interstyles/substyles/genres | `editing` | mixed-profile support | MODEL_ONLY | boundaries are porous |
| sender/receiver/channel/code | `editing` | context model | MODEL_ONLY | requires task/user context |
| economy vs redundancy | `editing` | balancing principle | MODEL_ONLY | no universal threshold |
| publicistic information/persuasion | `editing` | register guidance | MODEL_ONLY | genre-dependent |
| scientific abstraction/complex syntax | `editing` | register guidance | MODEL_ONLY | semantic/logical dependency required |
| administrative standardization | `editing` | register guidance + anti-rule | MODEL_ONLY | forms/templates can be functional |
| administrative formula cluster in explicit plain/conversational profile | `editing` | `sr_register_admin_formula_cluster` | EXTENDED_MECHANICAL | profile converts surface cluster into a narrow register-mismatch signal |
| conversational ellipsis/fragments | `native_usage` + `editing` | preserve-function guidance | MODEL_ONLY | context-dependent |
| literary markedness | `editing` | creative-writing restraint | MODEL_ONLY | aesthetic intent required |
| template/cliché AI false positives | `ai_style` runtime | suppress scaffold/heading signals for administrative/legal/documentation profiles | DEFAULT_MECHANICAL safeguard | structured genres are explicit counterexamples |
| exact 2002 frequencies/prescriptions | provenance only | no promotion | NONE | source-period / cross-language |
| automatic register classifier | none | reject | NONE | surface form insufficient to infer profile safely |
| sentence-length thresholds | none | reject | NONE | false positives across science/legal/publicistic |

## Runtime decision

- New finding check: **1 profile-gated EXTENDED_MECHANICAL register-mismatch heuristic**.
- New mechanical false-positive safeguards: **2 profile suppressions** for structural AI checks.
- New hard gates: **0**.
- New model-level functional-style gate: **yes**.
- Current-NORM promotion: **none**.
