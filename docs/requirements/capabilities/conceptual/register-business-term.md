# Capability: Register Conceptual Business Term ⚡

- **URI**: `req://conceptual/register-business-term`
- **Bounded Context**: `conceptual`
- **Lifecycle**: `ACTIVE`

## 1. Human Purpose & Intent
Authoritatively registers an enterprise business term with formal definitions, business context, synonyms, and governance stewardship.

## 2. Operational Contract

### Preconditions (Required State Prior to Execution)
- **Term slug must be lowercase alphanumeric with hyphens**
  - Expression: `term.slug.matches("^[a-z0-9_-]+$")`
- **Business definition must not be empty**
  - Expression: `len(term.definition.strip()) > 10`

### Postconditions (Guaranteed State Upon Success)
- **Term is registered under data://conceptual/<slug>**
  - Expression: `catalog.has_term(term.slug) == True`

### State Transitions
*No explicit state transitions.*

## 3. Explicit Failure Modes & Error Recovery
Formal error branches that must be handled by autonomous implementations:

| Error Name | Domain Error Code | Trigger Condition | Recovery Action |
| :--- | :--- | :--- | :--- |
| **`DuplicateTermError`** | `CONCEPTUAL_001` | Term slug is already registered in conceptual catalog | Prompt user for synonym alias or disambiguated namespace slug |

## 4. Governance, Decisions & Invariant Guardrails
### Governing Architectural Decisions (ADRs)
- **decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance** (`decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance`)
### Active Invariant Guardrails
- ⚠️ **Mandatory Plain-Language Business Definition** (`constraint://groundtruth/mandatory-business-definition`)
  *Remediation*: Add a descriptive business definition explaining the real-world business meaning of this term.
