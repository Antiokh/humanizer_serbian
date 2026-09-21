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
| conversational ellipsis/fragments | `native_usage` + `editing` | preserve-function guidance | MODEL_ONLY | context-dependent |
| literary markedness | `editing` | creative-writing restraint | MODEL_ONLY | aesthetic intent required |
| template/cliché AI false positives | `ai_style` docs | counterexample boundary | MODEL_ONLY | genre detection not deterministic |
| exact 2002 frequencies/prescriptions | provenance only | no promotion | NONE | source-period / cross-language |
| register classifier regex | none | reject | NONE | surface form insufficient |
| sentence-length thresholds | none | reject | NONE | false positives across science/legal/publicistic |

## Runtime decision

- New deterministic checks: **0**
- New hard gates: **0**
- New model-level functional-style gate: **yes**
- AI-style false-positive boundary: **yes**
- Source-study evals: **yes**
- Current-NORM promotion: **none**
