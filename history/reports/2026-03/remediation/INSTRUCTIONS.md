# The Covenant — Remediation Instructions

**Repo Role**: Philosophy & Governance — the "Why"
**Audit Date**: 2026-03-01
**Agent Scope**: Internal fixes only. Do NOT move files to other repos.

---

## Phase 1 Tasks (Internal Remediation)

Execute these in order. Record each completed task in `REMEDIATION-REPORT.md`.

### Critical

#### C1. Prepare OPA/Terraform files for migration

The `policies/terraform/` directory contains executable code (.rego files, .tf test fixtures) that violates the Covenant's "no automation" principle. Do NOT delete these files — they need to move to the-citadel.

**Action**:
1. Create `MIGRATION-MANIFEST.md` in this `.claude/remediation/` directory
2. List every file under `policies/terraform/` with its intended destination:
   - `.rego` files → `the-citadel/policies/opa/`
   - `.tf` test files → `the-citadel/policies/opa/tests/`
3. Add a note in each `.rego` and `.tf` file header: `# PENDING MIGRATION: This file will move to the-citadel per 2026-03-01 audit`
4. Document what references these files (e.g., ADR-003, any cross-repo CI paths)

---

### Major

#### M1. Consolidate ADRs to a single location

ADRs currently exist in THREE places:
- `docs/architecture/` (ADR-000, 001, 003)
- `adrs/drafts/` (ADR-002)
- `REFERENCE/decisions/` (different ADR-001, ADR-002)

**Action**:
1. Designate `docs/architecture/` as the canonical ADR home
2. Move `adrs/drafts/ADR-002-governed-agentic-development.md` to `docs/architecture/` — renumber if needed (it should be ADR-004 if 002 was intentionally skipped, or ADR-002 if the gap was accidental)
3. In `REFERENCE/decisions/`, add a header to each file: `> **ARCHIVED**: This is a legacy decision record. Current ADRs live in `docs/architecture/`.`
4. Delete the empty `adrs/` directory tree after migration
5. Update any README or index references to point to `docs/architecture/`

#### M2. Clean up history/ directory

`history/reports/2025-11/` contains 27 files, most of which are operational noise (Homebrew cleanup plans, site implementation docs, execution guides). These are not governance artifacts.

**Action**:
1. Review each file in `history/reports/2025-11/`
2. Files that document governance decisions or architectural history: KEEP
3. Files that are operational plans, site specs, or workstation maintenance: List in MIGRATION-MANIFEST.md for relocation to `.archive/` at the parent level
4. Specifically flag: `nash-site-spec-approved.md`, `nash-site-implementation.md`, `nash-site-style-guide.md` — the-tartan references these; note in the manifest that they need a stable location

#### M3. Fix policy file naming conventions

Three files violate kebab-case:
- `policies/AGENT_AUDIT_WORKFLOWS.md` → assign a policy ID and rename (e.g., `agt-002-audit-workflows.md`)
- `policies/CITADEL_AUDIT_FRAMEWORK.md` → rename (e.g., `agt-003-citadel-audit-framework.md`)
- `policies/ENFORCEMENT_VERIFICATION_CHECKLIST.md` → rename (e.g., `agt-004-enforcement-checklist.md`)
- `policies/AGENT-GOVERNANCE.md` → already has AGT-001 in its header; rename to `agt-001-agent-governance.md`

**Action**:
1. Rename all four files following the `category-nnn-name.md` pattern
2. Update `policies/README.md` to reflect the new names
3. Check for any cross-references within this repo and update them
4. Note: the parent-level validator (`.org/tooling/validators/validate-naming.sh`) has a whitelist for the old names — add to MIGRATION-MANIFEST.md that the validator whitelist needs updating

#### M4. Update CLAUDE.md

**Action**:
1. Replace ALL instances of `citadel-config` with `the-citadel` (there are 6+ occurrences)
2. Remove or genericize the "Model Context" section — remove specific model version numbers. Use this template:
   ```markdown
   ## For Claude Code
   This repository is **The Covenant** — philosophy and governance.
   See `../CLAUDE.md` for full organizational context and the three-pillar architecture.
   ```
3. Update `Last Updated` date to `2026-03-01`
4. Verify the repository structure diagram matches reality — update if not

#### M5. Update README.md structure diagram

The README shows a structure that doesn't match reality. It's missing `adrs/`, `docs/architecture/`, `history/`, `policies/`, `schemas/`.

**Action**: Update the structure diagram to reflect the actual current directory tree.

#### M6. Fix REFERENCE/index.md

**Action**:
1. Remove references to files that don't exist (000-template.md, 003-005 decisions, deprecated/* files)
2. Replace `citadel-config` references with `the-citadel`
3. Mark the REFERENCE/decisions/ directory as a legacy archive
4. Update ADR-001 implementation checklist to reflect actual current state

---

### Minor

#### m1. Address gov-009 gap

**Action**: Add a comment in `policies/README.md` explaining that gov-009 was either intentionally skipped or reserved. If it was deleted, note what it was.

#### m2. Fix .envrc

**Action**: Remove `PATH_add node_modules/.bin` from `.envrc` — this repo has no JavaScript.

#### m3. Fix CHANGELOG.md

**Action**: Either populate with meaningful entries from git history, or replace content with:
```markdown
# Changelog

This project's changelog is maintained via git history. See `git log --oneline` for the full change history.
```

#### m4. Fix hardcoded identity in Rego policy

**Action**: In `policies/terraform/sec-003-least-privilege.rego`, the pattern `"jeffrey@"` is hardcoded. Add a comment: `# TODO: Extract to configuration variable during migration to the-citadel`

---

## Phase 3 (Verification & Final Cleanup)

**Context**: Phase 1 completed 11 internal tasks. Phase 2 moved OPA files out (Migration 2), brought policy docs in (Migration 3), brought role-mapping in (Migration 4), and copied history specs to the-tartan (Migration 5). The Phase 2 verification audit found remaining issues.

### Verify Phase 1 + 2 Results

- [ ] `policies/terraform/` directory no longer exists (Migration 2 removed it)
- [ ] `policies/opa/` does NOT exist here (OPA code now lives in the-citadel)
- [ ] `policies/guides/policy-enforcement.md` exists (received from Migration 3)
- [ ] `policies/specs/iam-specification.md` exists (received from Migration 3)
- [ ] `docs/role-mapping.md` exists (received from Migration 4)
- [ ] Only one ADR location: `docs/architecture/` (Phase 1 consolidated this)
- [ ] All policy files follow `category-nnn-name.md` naming (Phase 1 renamed 4 files)
- [ ] CLAUDE.md contains no `citadel-config` references (Phase 1 fixed 6 occurrences)
- [ ] REFERENCE/index.md has no dead links (Phase 1 cleaned up)

### Fix Remaining Issues

#### V1. Bulk replace `citadel-config` in policy files (HIGH)

Phase 1 flagged ~25 policy .md files that still contain `citadel-config` in code examples and path references. These were intentionally skipped because they're embedded in code blocks.

**Action**: Replace all remaining `citadel-config` → `the-citadel` in policy .md files. Skip files in `history/` and `REFERENCE/decisions/` (those are historical records). Skip ADR-001 (it documents the rename itself).

#### V2. Fix stale paths in policy-enforcement.md (HIGH)

`policies/guides/policy-enforcement.md` (received from the-citadel in Migration 3) contains 8 example commands referencing the old `the-covenant/policies/terraform/` path. These must be updated to `the-citadel/policies/opa/`.

**Action**: In `policies/guides/policy-enforcement.md`, replace all occurrences of `the-covenant/policies/terraform/` with `the-citadel/policies/opa/`. Also replace `policies/terraform/` (without prefix) with `the-citadel/policies/opa/` where it appears in commands.

#### V3. Update README structure diagram

**Action**: Verify the README.md structure tree reflects the current state:
- `policies/guides/` and `policies/specs/` should be present
- `policies/terraform/` should NOT be listed
- `docs/role-mapping.md` should be present

#### V4. Verify history/ is governance content only

Phase 1 moved 7 operational files and 6 tartan specs out via Migration 5. 14 files were kept. Verify the remaining files in `history/reports/2025-11/` are genuinely governance/architecture/strategy content, not operational noise that was missed.

### Record Results

Record all findings and actions in `.claude/remediation/VERIFICATION-REPORT.md`.
