---
title: Covenant Cloudflare One Ontology Audit
status: audit-only
date: 2026-05-20
expires_at: 2026-06-20
authority_tier: Covenant-tier
publication_gate: 2 Watchers + 2 Mentors with 72h debate
source_repo: the-covenant
source_head: 8f736df0f39f609fdaf2dc493de9c3e649647e69
parent_directive: ../.claude/orchestration/directives/directive-2026-05-20-covenant-cloudflare-ontology-audit.md
parent_standard: ../.org/standards/cloudflare-one-ontology.md v1.0.0
authority_inversion_protection: Principle 9 is the Covenant-authoritative source for Zero Trust as a security model; the parent Cloudflare One ontology standard is downstream and must not be used to classify Principle 9 language as drift.
claims_checked:
  - parent directive read in full
  - Citadel structural packet read
  - Hetzner, runner-substrate, Shield, Nexus, and ci-runner precedent packets read
  - parent Cloudflare One ontology standard v1.0.0 read as downstream of Principle 9
  - Covenant current surfaces scanned on main at source_head
  - no remediation performed
---

# Cloudflare One Ontology Audit - 2026-05-20

Status: PASS, audit-only. This packet records repo-local Covenant evidence for
Track 1B Pillar 5 - Final. It does not authorize publication, remediation, or
provider mutation.

Expected shape confirmed: the Covenant is the authoring layer for Principle 9,
so most `Zero Trust` hits are preservation-confirmed security-model language.
No high, medium, or low remediation findings were found.

## Source Snapshot

| Field | Value |
|---|---|
| Repo | `the-covenant` |
| Path | `/Users/verlyn13/Organizations/the-nash-group/the-covenant` |
| Branch | `main` |
| Upstream | `origin/main` |
| HEAD | `8f736df0f39f609fdaf2dc493de9c3e649647e69` |
| Parent directive | `.claude/orchestration/directives/directive-2026-05-20-covenant-cloudflare-ontology-audit.md` |
| Parent merge basis | parent main as of merge commit `d7c6885`, PR #28 |
| Parent standard | `.org/standards/cloudflare-one-ontology.md` v1.0.0 |
| Audit files | `audit/2026-05-20/cloudflare-ontology-audit/README.md`, `findings.tsv` |

## Structural References Read

- `../the-citadel/audit/2026-05-19/cloudflare-ontology-audit/README.md`
- `../the-citadel/audit/2026-05-19/cloudflare-ontology-audit/findings.tsv`
- `../hetzner/docs/reports/cloudflare-ontology-audit-2026-05-19.md`
- `../runner-substrate/docs/evidence/tng-runner-ser9-01/cloudflare-one-ontology-audit-2026-05-20.md`
- `../the-shield/audit/2026-05-20/cloudflare-ontology-audit/README.md`
- `../the-shield/audit/2026-05-20/cloudflare-ontology-audit/findings.tsv`
- `../the-nexus/audit/2026-05-20/cloudflare-ontology-audit/README.md`
- `../the-nexus/audit/2026-05-20/cloudflare-ontology-audit/findings.tsv`
- `../ci-runner/audit/2026-05-20/cloudflare-ontology-audit/README.md`
- `../ci-runner/audit/2026-05-20/cloudflare-ontology-audit/findings.tsv`

## Covenant Surfaces Read

- `AGENTS.md`, `CLAUDE.md`, `README.md`, `PRINCIPLES.md`, `GOVERNANCE.md`,
  `HUMAN_MANDATE.md`
- `policies/`, including constitutional invariants and `policies/specs/`
- `policies/specs/cloudflare-ownership-transition.md`
- `docs/architecture/`, including ADR-003, ADR-004, ADR-005, ADR-007, and
  ADR-008

## Working Ontology For Covenant

| Surface | Treatment |
|---|---|
| Principle 9 / SEC-001 Zero Trust language | Covenant-authoritative security model. Preservation-confirmed by definition. |
| Parent Cloudflare One ontology standard | Downstream parent standard for product/platform terminology in lower layers and provider-specific prose. |
| Cloudflare Access, Workers, Pages, Tunnel, API tokens, `wrangler`, provider resource names | Provider/API/CLI literals or implementation-contract examples; preserve unless the owning implementation layer changes. |
| Historical ADR examples and `history/` reports | Preserve as historical evidence, especially when current-state notes mark older implementation paths. |
| Product-bucket-like `Zero Trust` in transitional Cloudflare specs | Surface as open clarification when needed; do not treat as Principle 9 drift or amend under this audit. |

## Scan Evidence

Directive scans run from repo root:

```bash
rg -lw 'WARP' --hidden -g '!.git/**'
rg -li 'zero.trust' --hidden -g '!.git/**'
rg -li 'magic wan|casb|area 1|gateway polic|warp-to-warp|1\.1\.1\.1 app' --hidden -g '!.git/**'
rg -n 'Cloudflare|Access|Principle|Zero Trust|security model|philosophy|governance|ADR' \
  AGENTS.md CLAUDE.md README.md PRINCIPLES.md GOVERNANCE.md HUMAN_MANDATE.md \
  policies docs .claude \
  --hidden -g '!.git/**' 2>/dev/null
```

Results:

| Scan | Result |
|---|---|
| `WARP` file scan | No hits. |
| `zero.trust` file scan | Hits are concentrated in Principle 9 / SEC-001 / ADR / spec / archive contexts. |
| Retired-term scan | Only `policies/sec-001-zero-trust.md` matched, via lower-case `gateway policies` at line 220. Classified acceptable generic API gateway policy language. |
| Covenant-context scan | Produced 970 matching lines across current docs, policies, specs, ADRs, and history. The local `.claude` path is absent in this repo, so `rg` returned code 2 while still returning matches from existing paths with stderr suppressed. |

## Findings Summary

See `findings.tsv` for exact file and line references.

| Severity | Count |
|---|---:|
| high | 0 |
| medium | 0 |
| low | 0 |
| info | 12 |

| Remediation class | Count |
|---|---:|
| `principle-9-authoritative` | 7 |
| `historical-evidence` | 1 |
| `ambiguous-prose` | 1 |
| `acceptable` | 1 |
| `provider-literal` | 1 |
| `archive` | 1 |

Preservation-confirmed rows: 12. Remediation rows: 0.

## Authority-Inversion Check

Passed. No Principle 9, SEC-001, ADR, or Covenant philosophy language was
classified as Cloudflare-ontology drift.

The audit found one active transitional-spec phrase that can read as a
Cloudflare product bucket: `policies/specs/cloudflare-ownership-transition.md`
uses `Zero Trust resources` and includes `Zero Trust` in a future-controls menu.
This packet does not classify that as drift and does not recommend unilateral
rewrite. If the spec is amended later, parent plus Covenant-tier reviewers
should decide whether the text means Cloudflare One Access controls, identity
resources, or security-model controls.

No detected tension required stopping the audit.

## Governance Lane Mapping

| Lane | Audit treatment |
|---|---|
| Covenant | Principle 9, SEC-001, ADRs, and active specs are authority surfaces. Preserve unless a Covenant-tier amendment or Guardian-approved ADR/spec maintenance explicitly changes them. |
| Citadel | Cloudflare Access examples, OpenTofu resource names, provider versions, and workspace placement are downstream implementation evidence. This audit did not mutate them. |
| Shield | Identity, credential, and permission-binding contracts are referenced where specs say they will migrate or be consumed by Shield; this audit did not pre-activate Shield. |
| Nexus | Runtime admission language remains downstream of Covenant authority; no Nexus runtime claims were made or changed. |
| Meta / parent | Parent `.org/standards/cloudflare-one-ontology.md` governs provider/product terminology downstream of Principle 9. Parent orchestration receives this audit as an evidence packet, not as publication approval. |

## Stop Rules

- Stop if Covenant principle language and the parent standard appear to
  disagree; surface to parent plus Covenant-tier reviewers, do not classify
  Covenant language as drift.
- Stop if the audit would need to classify ratified principle wording,
  ratified ADR text, or active spec text as drift in a way requiring Covenant
  amendment.
- Stop if a Covenant-specific Cloudflare concept appears that the parent
  standard does not cover.
- Stop if Covenant docs conflict on policy-status semantics or governance
  authority matrix versus parent `CLAUDE.md`.
- Stop on operator pause.

No stop rule triggered.

## No-Secrets Statement

No secrets were read, requested, exposed, or inferred. The audit used local
repository text only. No Cloudflare API calls, OpenTofu plan/apply, OPA
state-mutating runs, 1Password reads, dashboard actions, GitHub setting changes,
remote writes, push, PR, merge, amend, rebase, reset, or branch delete occurred.

## Validation

Validation commands were run after authoring:

- `git diff --check`
- `awk -F'\t' 'NR==1 && $0 != "id\tseverity\tfile\tlines\tcurrent_language\tissue\trecommended_action\tremediation_class" { print "bad header"; bad=1 } NR>1 && NF != 8 { print "bad field count line " NR ": " NF; bad=1 } END { exit bad }' audit/2026-05-20/cloudflare-ontology-audit/findings.tsv`
- `../.org/tooling/validators/check-secrets.sh audit/2026-05-20/cloudflare-ontology-audit`
- `git status --short --branch`

Validation result:

| Command | Result |
|---|---|
| `git diff --check` | Pass |
| TSV header and 8-column field-count check | Pass |
| `../.org/tooling/validators/check-secrets.sh audit/2026-05-20/cloudflare-ontology-audit` | Pass; no obvious secrets detected |
| `git status --short --branch` | `## main...origin/main`; untracked `audit/2026-05-20/` only |
