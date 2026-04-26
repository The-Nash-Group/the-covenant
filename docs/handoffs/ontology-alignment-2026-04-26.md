# Ontology Alignment Handoff

**Date:** 2026-04-26
**Repo:** `the-covenant`
**Requested by:** parent ontology, role, and ownership audit
**Governance level:** Covenant for meaning changes; documentation cleanup may proceed as a scoped proposal but still requires Guardian review before merge.

## Mission

Align Covenant-facing language with the current parent operating model without
changing the meaning of the Covenant unless a human explicitly approves that
governance change.

The Covenant remains the source of truth for principles, governance, and human
responsibility. Parent `.org/ontology/` files consume and map Covenant meaning;
they do not supersede this repository.

## Review Status - 2026-04-26

**Approved for alignment commit.** The repo-level remediation cleared the
current-state Terraform wording from active Covenant-facing docs.

The remaining `terraform` match is an intentional `.tf` backend filename in
`PRINCIPLES.md` paired with OpenTofu wording, not an active Terraform
implementation claim.

## Target Files

Review at minimum:

- `CLAUDE.md`
- `README.md`
- `HUMAN_MANDATE.md`
- `GOVERNANCE.md`
- `PRINCIPLES.md` only if an existing wording conflict is unavoidable

## Required Work

1. Replace active implementation references to `Terraform` with `OpenTofu` or
   provider-neutral `Infrastructure as Code`, as appropriate.
   - Examples to fix: "Terraform code translates philosophy into enforcement",
     "Terraform plan", "Writes Terraform resources".
   - Preserve `Terraform` only when the text is explicitly historical, a file
     path, a legacy product name, or part of a quoted/historical ADR context.

2. Clarify role semantics where needed.
   - Guardian archetypes are functional hats, not approval teams.
   - Immortals, Mentors, and Watchers are formal governance tiers.
   - Synthetic agents are delegates and recommendation engines, not Guardians
     and not final approvers.

3. Keep the Human Mandate as the conceptual role source.
   - Do not make `HUMAN_MANDATE.md` subordinate to `.org/ontology/roles.yaml`.
   - It is acceptable to add a short note that machine-readable mappings live
     outside this repo, but the Covenant text remains the normative source.

4. Reconcile "implementation path" wording.
   - Use `the-citadel` as the enforcement repository.
   - Use OpenTofu/IaC/Policy as Code wording rather than Terraform-specific
     wording unless the text is intentionally historical.

## Resolved Review Items

1. `README.md` still presents current operation as Terraform-driven.
   - Review `README.md:16`, `README.md:17`, `README.md:100`,
     `README.md:109`, `README.md:168`, and `README.md:169`.
   - Replace current-state Terraform wording with OpenTofu, IaC, or
     provider-neutral enforcement language.

2. `HUMAN_MANDATE.md` still uses Terraform for current Guardian workflows.
   - Review `HUMAN_MANDATE.md:70` through `HUMAN_MANDATE.md:100`,
     plus `HUMAN_MANDATE.md:136` and `HUMAN_MANDATE.md:322`.
   - Preserve the Guardian role model, but describe current enforcement
     artifacts as OpenTofu/IaC/Policy as Code where applicable.

3. `CLAUDE.md` still contains current-state Terraform references.
   - Review `CLAUDE.md:26`, `CLAUDE.md:77`, `CLAUDE.md:178`, and
     `CLAUDE.md:234`.
   - If any reference is intentionally historical, label it explicitly.

4. `GOVERNANCE.md` still describes Citadel operational approval as Terraform.
   - Review `GOVERNANCE.md:69`.
   - Use current Citadel/OpenTofu wording without changing the approval matrix.

5. `PRINCIPLES.md` contains Terraform references that need careful handling.
   - Review `PRINCIPLES.md:137`, `PRINCIPLES.md:140`, and
     `PRINCIPLES.md:351`.
   - If these are examples of current implementation, update to OpenTofu/IaC.
   - If changing the term would alter a principle's meaning, stop and flag the
     item for explicit Guardian review instead of silently rewriting it.

## Out Of Scope

- Do not rewrite the 16 principles unless a human explicitly asks for a
  Covenant-level amendment.
- Do not change approval thresholds.
- Do not add CI or automation to this repo.
- Do not edit parent `.org/` files from this repo session.

## Acceptance Criteria

- `CLAUDE.md`, `README.md`, and `HUMAN_MANDATE.md` no longer describe current
  implementation through Terraform-specific wording.
- Any remaining `Terraform` references are clearly historical, path-specific,
  or otherwise intentional.
- Role language does not confuse functional archetypes with approval roles.
- Agent language preserves human final authority.
- The repo still presents Covenant as the source of philosophy and governance,
  not as an implementation repo.
- Active current-state Terraform references are corrected or intentionally
  scoped to filename/historical context.

## Validation Record - 2026-04-26

- `rg -n "Terraform|terraform" CLAUDE.md README.md HUMAN_MANDATE.md GOVERNANCE.md PRINCIPLES.md`:
  only the intentional `.tf` backend filename remains, with OpenTofu wording.
- `rg -n "Terraform code|Terraform plan|Writes Terraform|Citadel Terraform|Terraform-backed|HashiCorp Cloud" CLAUDE.md README.md HUMAN_MANDATE.md GOVERNANCE.md PRINCIPLES.md`:
  no matches.
- `../.org/tooling/validators/validate-naming.sh .`: passed with warnings for
  existing naming exceptions.
- `../.org/tooling/validators/check-secrets.sh .`: passed; no obvious secrets
  detected.

## Suggested Checks

```bash
rg -n "Terraform|terraform" CLAUDE.md README.md HUMAN_MANDATE.md GOVERNANCE.md PRINCIPLES.md
rg -n "final decision|recommendation|Synthetic|Guardian|Mentor|Watcher|Immortal" HUMAN_MANDATE.md GOVERNANCE.md CLAUDE.md
../.org/tooling/validators/validate-naming.sh .
../.org/tooling/validators/check-secrets.sh .
```

Manually inspect any `Terraform` hits. The goal is not zero matches; the goal is
no current-state semantic drift.

## Review Notes

Flag any proposed change that would alter the meaning of a principle, approval
rule, or human role. Those are Covenant-level changes and need explicit review,
not opportunistic wording cleanup.
