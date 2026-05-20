# REM-008 Covenant Policy-Status Review

Date: 2026-05-13
Scope: Covenant policy-status language for IAM, PaC, secrets, Cloudflare transition, governance/status semantics, subsidiary authority, and public identity.
Status: completed as Covenant-local wording review; no policy status promotion.

Post-review note (2026-05-17): ADR-008 and the paired IAM Spec v0.2.0
amendment were ratified after this review. Treat the IAM status observations
below as the 2026-05-13 pre-ratification baseline; current IAM status is
`identity-and-account-management.md` v0.2.0 with §§1-6 DRAFT -- Accepted for
Validation and §7 ratified via ADR-008 under the Covenant-tier single-Guardian
quorum exception.

## Method

I read Covenant-local authority first: `AGENTS.md`, `CLAUDE.md`, `README.md`,
`PRINCIPLES.md`, `GOVERNANCE.md`, `HUMAN_MANDATE.md`, and
`policies/README.md`.

I then reviewed the high-priority policy/spec surfaces and related ADRs named in
the REM-008 directive. Parent and consumer-repo records were used as comparative
evidence only. No parent, Shield, Citadel, Nexus, Hetzner, Tartan, runner, or
subsidiary repository was edited.

## Comparative Evidence Used

- Parent state vocabulary separates `control_class` from `maturity_state`.
- Runner and ci-runner evidence preserves `usable` as bounded and keeps
  ci-runner policy artifacts advisory/source-defined/source-tested, not
  live-blocking.
- Citadel evidence supports real but narrow enforcement: SEC-003/SEC-004
  blocking Rego paths, native GitHub controls where configured, workflow-policy
  report-only, and secret/agent-authority PaC as design or future work.
- Shield remains planned/not-started IAM contract home, not live IAM or a
  runtime authorization service.
- Nexus Rego is tested source unless request-path loader and deny-path evidence
  exist.
- Hetzner remains a transitional broker for named hosted surfaces; `CONFIRM=1`
  is local friction, not approval.
- Tartan owns public-site source/presentation. Citadel/OpenTofu owns Cloudflare
  infrastructure/control-plane claims; live Pages/security claims remain
  trace-blocked without current provider/Citadel evidence.

## Fixed In This Review

- PaC language now avoids treating every Covenant policy as OPA/Rego or
  live-blocking enforcement. Updated `policies/agt-002-audit-workflows.md`,
  `policies/agt-003-citadel-audit-framework.md`,
  `policies/agt-004-enforcement-checklist.md`,
  `policies/guides/policy-enforcement.md`, `policies/README.md`, and
  `README.md`.
- Synthetic Council, SDR, Sigstore/Rekor, and automated merge-gate language now
  reads as target/proposed governance unless FU-1 and SDR evidence exist.
  Updated `HUMAN_MANDATE.md` and ADR-002.
- Authentik, Infisical, identity federation, secret centralization, and IaC
  coverage wording in ADR-004 now requires owning-repo adoption/evidence before
  being treated as live enforcement.
- SEC-005 now states that automated validation bullets are required evidence
  targets, not Covenant-local proof that all scans, dashboards, webhooks, or
  provider settings are live.

## Left Unchanged Intentionally

- `policies/specs/identity-and-account-management.md` remains `DRAFT -- Accepted
  for Validation`. Comparative Citadel evidence suggests some implementation
  progress, but Covenant-local ACTIVE promotion still requires the spec's own
  second-stage acceptance evidence and Guardian-approved status update.
- `policies/specs/secrets-management.md` remains ACTIVE and remains the higher
  Covenant authority for long-lived material secret rotation cadence. This review
  did not silently relax or supersede its 180-day target.
- `policies/specs/cloudflare-ownership-transition.md` remains accepted as
  transitional custody/ownership policy. It already warns against pretending
  per-suborg accounts or full IAM isolation exist where they do not.
- `policies/specs/subsidiary-authority.md` and ADR-007 remain framed as
  restatement, not inheritance.
- Historical or rewrite-pending IAM/Terraform-era material remains marked as
  historical, conceptual, target-state, or pending rewrite rather than promoted.

## Authority Contradictions

No unresolved Covenant-local authority contradiction required halting the review.
The issues found were overclaiming/status-wording problems that could be fixed
with narrow qualifiers without changing constitutional meaning or policy status.

## Secret And Provider-Output Handling

No secret values, provider tokens, private keys, raw provider logs, dashboard
exports, or live-provider output were copied into this Covenant artifact or the
wording fixes. Comparative evidence containing operational details was used only
to classify status language.

## Validation

- `mise run validate`: passed with 0 errors and 1 warning
  (`.github/workflows/` missing). The warning matches this repository's
  no-automation design.
- `mise run check-naming`: passed with 0 errors and 5 warnings
  (`HUMAN_MANDATE.md`, `.`, dated `audit/2026-05-13`, and dated
  `history/reports/*` directories).
- `mise run check-secrets`: failed with 5 pre-existing placeholder/example
  matches in `.envrc` and `history/reports/2025-11/nash-site-implementation.md`
  (`your-key-here`, `<R2_ACCESS_KEY_ID>`, `<R2_SECRET_ACCESS_KEY>` examples).
  No actual secret value was identified or copied by this review, and this
  review did not change those historical/example files.
- 2026-05-18 recheck: `mise run check-secrets` passed with no obvious secrets
  detected.
- `../.org/tooling/validators/check-secrets.sh audit/2026-05-13/policy-status-review`:
  passed with no obvious secrets detected in this new artifact.
- `git diff --check`: passed.
- Required REM-008 `rg` status-language scan: completed (`2644` matches). The
  scoped review found no remaining unresolved Covenant-local authority
  contradiction after the narrow wording fixes above.
