# Migration Manifest — The Covenant
**Created**: 2026-03-01
**Purpose**: Track files that need to move out of the-covenant to their proper homes.
**Rule**: Do NOT move files during Phase 1. This manifest documents intent for Phase 2.

---

## 1. OPA/Terraform Files → the-citadel

These files are executable code (`.rego` policies, `.tf` test fixtures) that violate the Covenant's "no automation" principle. They must migrate to the-citadel.

| Source (the-covenant) | Destination (the-citadel) | Type |
|----------------------|--------------------------|------|
| `policies/terraform/gov-010-labeling.rego` | `the-citadel/policies/opa/gov-010-labeling.rego` | OPA Rego policy |
| `policies/terraform/sec-003-least-privilege.rego` | `the-citadel/policies/opa/sec-003-least-privilege.rego` | OPA Rego policy |
| `policies/terraform/sec-004-cloudflare-baseline.rego` | `the-citadel/policies/opa/sec-004-cloudflare-baseline.rego` | OPA Rego policy |
| `policies/terraform/tests/sec-003-compliant.tf` | `the-citadel/policies/opa/tests/sec-003-compliant.tf` | Terraform test fixture |
| `policies/terraform/tests/sec-003-violations.tf` | `the-citadel/policies/opa/tests/sec-003-violations.tf` | Terraform test fixture |
| `policies/terraform/tests/sec-004/compliant-zone.tf` | `the-citadel/policies/opa/tests/sec-004/compliant-zone.tf` | Terraform test fixture |
| `policies/terraform/tests/sec-004/violation-examples.tf` | `the-citadel/policies/opa/tests/sec-004/violation-examples.tf` | Terraform test fixture |

### Cross-References
- **ADR-003** (`docs/architecture/003-establish-cloudflare-governance-baseline.md`) references `sec-004-cloudflare-baseline.rego`
- **policies/sec-003-least-privilege.md** references the Rego enforcement file
- **policies/gov-010-labeling-standard.md** references the Rego enforcement file
- **policies/sec-004-security-baseline.md** references the Rego enforcement file
- No CI/CD paths reference these files (the-covenant has no GitHub Actions)

### Notes
- After migration, the corresponding `policies/*.md` files in the-covenant should update their "Implementation" sections to reference the new location in the-citadel
- The `policies/terraform/` directory should be deleted after successful migration

---

## 2. History Files → Archive or the-tartan

Files in `history/reports/2025-11/` that are operational noise (not governance artifacts).

### For Archival (→ parent-level `.archive/`)

| File | Reason |
|------|--------|
| `history/reports/2025-11/CHIEF-OF-STAFF-ASSESSMENT-2025-11-10.md` | Operational status report |
| `history/reports/2025-11/EXECUTIVE-BRIEFING-2025-11-10.md` | Operational briefing with metrics |
| `history/reports/2025-11/HOMEBREW-CLEANUP-PLAN.md` | Workstation maintenance |
| `history/reports/2025-11/HOMEBREW-CLEANUP-REPORT-2025-11-22.md` | Workstation maintenance execution |
| `history/reports/2025-11/WEEK-1-SPRINT-PLAN-2025-11-10.md` | Sprint planning (tactical) |
| `history/reports/2025-11/ORG-ROOT-CLEANUP-PLAN.md` | File system maintenance |
| `history/reports/2025-11/OPTION-2-EXECUTION-GUIDE.md` | Execution procedure |

### For the-tartan (website specifications — need stable location)

These files are referenced by `the-tartan` and need a stable location there.

| File | Reason |
|------|--------|
| `history/reports/2025-11/nash-site-spec-approved.md` | Site architecture spec v2.0 |
| `history/reports/2025-11/nash-site-implementation.md` | Site implementation guide v2.1 |
| `history/reports/2025-11/nash-site-style-guide.md` | Site style guide (Hermetic Institutionalism) |
| `history/reports/2025-11/nash-site-technical-advisory.md` | Site technical advisory |
| `history/reports/2025-11/official-site-plan-approved.md` | Site project deliverables index |
| `history/reports/2025-11/OFFICIAL-SITE-REPOSITORY-PLAN.md` | Site repository plan |

**Note**: These files should be copied (not moved) to `the-tartan/docs/` or similar location. Keep originals in history until the-tartan confirms receipt.

---

## 3. Validator Whitelist Update

The parent-level validator (`.org/tooling/validators/validate-naming.sh`) has a whitelist for the old policy file names that were in UPPERCASE_SNAKE_CASE. After M3 renames are complete, the whitelist entry for these files should be removed:
- `AGENT_AUDIT_WORKFLOWS.md` (now `agt-002-audit-workflows.md`)
- `CITADEL_AUDIT_FRAMEWORK.md` (now `agt-003-citadel-audit-framework.md`)
- `ENFORCEMENT_VERIFICATION_CHECKLIST.md` (now `agt-004-enforcement-checklist.md`)
- `AGENT-GOVERNANCE.md` (now `agt-001-agent-governance.md`)
