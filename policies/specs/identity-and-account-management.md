# Identity and Account Management Specification

**Version:** 0.1.0
**Status:** DRAFT
**Date:** 2026-05-03
**Implements:** Principle 5 (Infrastructure as Code), Principle 9 (Zero Trust), Principle 10 (Least Privilege), Principle 15 (Three Circles of Trust)
**Policies:** SEC-005 (Machine Identity), ORG-001 (Subsidiary Authority and Identity Isolation), GOV-003 (Break-Glass)
**Specs:** Secrets Management Specification v1.3.0
**Defers to (broader scope, REWRITE PENDING):** `iam-specification.md`

---

## Purpose

Define how identity and credentials map to The Nash Group's multi-entity case — the gap between SEC-005 (which defines identity *types*) and the per-entity reality of running an organization with five governance scopes (`nash-group`, `jefahnierocks`, `happy-patterns`, `litecky-editing`, `seven-springs`) backed by three real financial entities (personal/family, Happy Patterns LLC, Litecky Editing Services sole prop) plus a sandbox.

This specification is intentionally narrow. It answers exactly what is needed for per-entity scoped credentials to be issuable, used, rotated, audited, and revoked without creating cross-entity drift. It does **not** replace the `iam-specification.md` REWRITE PENDING work; that broader rewrite covers AWS IAM Identity Center, GCP IAM, federated SSO, agent sandbox cages, and break-glass alerting infrastructure — most of which does not apply at the current operational scale.

> **Current-state note (2026-05-03):** This spec lands as **DRAFT**. Guardian review may move it to **DRAFT — Accepted for Validation** (recorded in the changelog and acceptance-criteria checklist). It does NOT promote to **ACTIVE** until the first credential issuance under its contract (per-entity Cloudflare token in MN-1) AND the first end-to-end migration validation (Litecky Editing Services workload per `D5: CREDENTIAL-STRATEGY-RECOMMENDATION-2026-05-02`) both complete. Until then, treat this as the design contract that those steps will validate.

> **Ownership boundary:** This specification defines the multi-entity identity contract (principals, vault structure, rotation cadence, audit destinations, cross-entity prevention). Exact Citadel files, workflow names, commands, and live backend wiring are Citadel-owned implementation details; references below are current-state evidence or expected contracts, not Covenant-run implementation.

---

## Scope

### In scope

- Per-entity provider account model (Cloudflare, Hetzner, GitHub, 1Password, Infisical-when-deployed)
- Credential vault structure and naming convention
- Identity principals per credential (CI principal, owner break-glass principal, audit principal, future synthetic council principal)
- Rotation cadence, triggers, and evidence requirements
- Audit log destinations per entity
- Cross-entity prevention contract (mechanisms that ensure one entity's credentials cannot be used by another entity's workflows)

### Out of scope (and why)

- **Human SSO / Authentik / POC 3** — paused per D5; at the current 2-human scale (Guardian + Litecky co-owner Ahnie), human SSO is over-engineered until a third user, contractor, or compliance trigger emerges.
- **AWS IAM Identity Center / GCP IAM tenant model** — covered by `iam-specification.md` REWRITE PENDING; not currently operational at the multi-tenant scale that spec describes.
- **Federated OIDC for CI → cloud** — defer until 5+ workspaces or a non-trivial AWS/GCP footprint exists; neither true today.
- **Synthetic council credential model details** — slot reserved (see §3 Identity Principals); details land when the council is deployed and its operating model is defined.
- **Per-Worker secret rotation** — Cloudflare Workers' per-Worker secret model is already correct at runtime; this spec covers *deployment* credentials, not Worker runtime secrets.

---

## Six Questions This Spec Answers

### 1. Per-entity provider account model

Each entity has a defined relationship with each provider. The following table records the canonical model as of v0.1.0:

| Entity | Cloudflare | Hetzner | GitHub | 1Password | Infisical (planned) |
|--------|------------|---------|--------|-----------|---------------------|
| `nash-group` | shared parent account; scoped token | shared parent project; scoped credential | `The-Nash-Group` org | `Dev` vault (shared) | parent workspace |
| `jefahnierocks` | shared (transitional per `cloudflare-ownership-transition.md`); scoped token | shared parent (transitional); scoped credential | `jefahnierocks` Free org | `Dev` vault (shared) | per-subsidiary workspace OR continue 1Password (Jefahnierocks-decision) |
| `happy-patterns` | shared interim; **separate account at `scopecam` activation trigger** | per-LLC at activation | `happy-patterns-org` Teams | `Dev` vault → per-LLC vault when activation triggers | per-LLC workspace at activation |
| `litecky-editing` | shared interim; **separate account at next deployment** | per-LLC at activation | `litecky-editing` org | `Dev` vault → per-LLC vault at activation | per-LLC workspace at activation |
| `seven-springs` | shared (pedagogical exception per Subsidiary Authority Spec §7.4); no live resources | n/a | `seven-springs-org` Free | n/a | n/a |

**Rule:** Account separation pressure is *owner-driven* (LLC formation, customer transactions, regulated-data classification, revenue), not parent-driven. The parent does not initiate per-entity account moves; it provides the contract, the placement rule (`cloudflare-ownership-transition.md`), and the implementation slice when the entity owner is ready.

### 2. Credential vault structure

#### Phase A: Canonical logical paths + aliased 1Password item names (current and through synthetic council deployment)

**Canonical naming is the Secrets Management Specification v1.3.0 §3 namespace** — it is the single source of truth:

```
{domain}/{provider-or-resource}/{entity}/{secret-name}
```

(domain ∈ `infra` | `cloudflare` | `services` | `break-glass`; entity per §1; secret-name describes the credential's purpose.)

1Password item names in the shared `Dev` vault are **aliases** to these canonical logical paths. Item names follow a kebab-cased convention so vault listing remains scannable; the logical path remains canonical for cross-reference, audit, and PaC checks.

| Canonical logical path (Secrets Mgmt §3) | 1Password item alias (Dev vault) | Scope |
|------------------------------------------|----------------------------------|-------|
| `cloudflare/<entity>/api-token-rw` | `citadel-cloudflare-<entity>-rw` (e.g. `citadel-cloudflare-litecky-rw`, `citadel-cloudflare-the-nash-group`, `citadel-cloudflare-jefahnierocks-rw`) | per-entity Cloudflare API tokens |
| `infra/hetzner/<entity>/cloud-rw` | `citadel-hetzner-cloud-<entity>` (e.g. `citadel-hetzner-cloud-rw` — parent today; per-entity later) | per-entity Hetzner credentials |
| `infra/github-app/<installation>/private-key` | `citadel-github-app-<installation>` (e.g. `citadel-github-app-the-nash-group`) | per-installation GitHub App credentials |
| `cloudflare/<entity>/acme-dns01-<zone>` | `acme-dns01-<zone>` (e.g. `acme-dns01-jefahnierocks-com`) | per-zone DNS-01 ACME tokens (least-priv) |
| `cloudflare/<entity>/audit-readonly` | `audit-cloudflare-<entity>-readonly` (e.g. `audit-cloudflare-litecky-readonly`) | per-entity read-only audit tokens |
| `cloudflare/<entity>/mcp-readonly` | `<entity>-mcp-readonly` (e.g. `cloudflare-mcp-jefahnierocks` — already exists) | per-entity read-scope tokens for MCP / agent reads |

**Why both:** the canonical path supports backend-agnostic logic (PaC, audit-rotation-log entries, registry lookups). The 1Password alias supports human discoverability in the vault UI. Cross-references in this spec, in `subsidiaries.yaml`, and in audit logs MUST use the canonical path; the 1Password item name is the implementation alias.

**Required convention discipline:**

- No credential MAY exist in the `Dev` vault outside this naming convention without an explicit `1password-out-of-spec.md` entry in the parent registry.
- A credential whose entity scope is unclear is named `unclassified-<purpose>` and is treated as `over-scoped` until reclassified.
- Tokens that span multiple entities (the current `secret:cf-api-token-shared` situation) are flagged for retirement and replaced before any new dependency is added.

#### Phase B: Per-entity vaults (triggered by synthetic council deployment)

When the synthetic council comes online to manage Nash Group governance, the strict-naming model migrates to per-entity vaults:

- `Dev-nash-group` — parent credentials only
- `Dev-jefahnierocks` — Jefahnierocks personal/family credentials
- `Dev-happy-patterns` — Happy Patterns LLC credentials (or a fully separate 1Password account owned by the LLC)
- `Dev-litecky-editing` — Litecky Editing credentials (or a fully separate 1Password account owned by Ahnie)
- `Dev-seven-springs` — sandbox

Migration trigger: synthetic council first session of operation. Migration mechanism: 1Password Connect cross-vault references or service-account tokens with per-vault scope. Until then, strict naming in `Dev` is the operating model.

**Why the Phase A → Phase B sequence:** Phase A is fast (naming convention) and lets the first migration happen. Phase B is structurally cleaner (vault-level isolation) but requires the synthetic council's principal model to be defined before per-vault access boundaries can be specified. Doing both at once would over-engineer ahead of the council's design.

### 3. Identity principals per credential

Every credential issued under this specification MUST define its named principals. No credential lacks a defined principal set.

#### Principal types

| Principal type | Purpose | Example |
|----------------|---------|---------|
| `<entity>-citadel-ci` | Workflow execution principal; receives token at job start via GitHub Actions secret resolution from `workspace-registry.json` | `litecky-citadel-ci` |
| `<entity>-owner-break-glass` | Emergency manual operations by entity owner via 1Password | `litecky-owner-break-glass` (Ahnie) |
| `<entity>-audit-readonly` | Read-only metadata / rotation-evidence audit principal; never holds the rotating token, only the rotation-evidence channel | `litecky-audit-readonly` |
| `nash-synthetic-council-readonly` | (Reserved for synthetic council deployment) Read-only audit across entities under documented quorum rules; never write | (slot reserved) |
| `<entity>-mcp-readonly` | Per-entity MCP / agent read principal | `jefahnierocks-mcp-readonly` (current `cloudflare-mcp-jefahnierocks` token) |

#### Recording

Per-credential principal sets are recorded in:

- The credential's 1Password notes field (logical principal names only; never private identifiers)
- The entity's parent-side registry entry under `principals:` (extension to `subsidiaries.yaml` proposed for v2.8)
- The per-entity audit-rotation-log (see §4)

#### Synthetic council principal slot

The `nash-synthetic-council-readonly` principal is reserved but not yet defined. When the council is deployed, this spec receives a v0.2.0 update defining:

- The council's read scope per entity
- The quorum rule for council read access (e.g., does a single council member read suffice, or does a multi-member quorum apply?)
- The council's write authority (expected: zero; council reads metadata, recommends actions, does not execute writes)
- The council's break-glass exception (if any)

Until then, the slot exists in the principal model so future credential entries leave room for it without retrofitting.

### 4. Rotation contract

Cadences are inherited from **Secrets Management Specification v1.3.0 §5.4** (the active Covenant-tier spec governing rotation targets) and applied per credential type:

| Credential type | Cadence | Trigger | Evidence |
|-----------------|---------|---------|----------|
| Cloudflare API tokens (per-entity scoped) | **180 days** (per Secrets Mgmt v1.3.0 §5.4) | calendar; immediate on owner change, principal addition/removal, or breach suspicion | rotation entry in `<entity>/audit-rotation-log.md` (see §5) |
| Cloudflare API tokens (account-wide; legacy) | retire by next rotation cycle (max 180 days from spec acceptance) | replacement scoped tokens issued | retirement entry; old token revoked |
| GitHub App private keys (PEM) | **180 days** (per Secrets Mgmt v1.3.0 §5.4) | calendar; immediate on breach or platform security alert | rotation evidence in Citadel CI logs + 1Password version history |
| GitHub App installation tokens (IAT) | per-job (1-hour TTL by default; protocol-enforced) | platform-managed | inherent (no rotation needed at the spec level) |
| Hetzner cloud / S3 credentials | **180 days** (per Secrets Mgmt v1.3.0 §5.4) | calendar; immediate on owner change | rotation entry in audit-rotation-log |
| State encryption passphrase (`TOFU_STATE_ENCRYPTION_PASSPHRASE`) | **rotate only on suspected compromise** (per Secrets Mgmt v1.3.0 §5.4 exception) | breach suspicion or key-custody change | incident record + rotation entry |
| ACME DNS-01 tokens (per-zone) | quarterly (90 days) | calendar | renewal evidence in subsidiary scope (HomeNetOps for Jefahnierocks zones; per-entity equivalent for others) |
| OPNsense API users (HomeNetOps) | quarterly (90 days) | calendar; immediate on personnel change or privilege drift detection | OPNsense API user inventory (subsidiary-scope); parent records the contract, not the inventory |
| 1Password vault membership | reviewed at synthetic council deployment; immediate on personnel change | event-driven | 1Password activity log + rotation entry |

**Evidence requirement:** Every rotation produces a non-secret entry in the per-entity audit-rotation-log naming the credential's canonical logical path (per §2), principal set, rotation date, rotation reason, and verification step. **Secret values are never logged.** Logical paths and rotation dates only.

**Cadence rationale:** 180 days is the Secrets Management v1.3.0 target for long-lived material secrets (Cloudflare API tokens, GitHub App PEMs, Hetzner cloud/S3 credentials). Quarterly (90 days) applies where credential blast radius or principal turnover is higher (DNS-01 affects zone-level cert renewal; OPNsense API users gate LAN admin access). State encryption passphrase rotates only on suspected compromise per the Secrets Management v1.3.0 exception. This spec inherits these targets — it does NOT relax them. v0.2.0 may tighten cadence if first-cycle evidence supports it.

### 5. Audit destination per entity

Per-entity audit destinations:

| Surface | Destination | Read access |
|---------|-------------|-------------|
| Cloudflare API token use | Cloudflare audit log per entity scope (account-level for accounts; zone-level for zone-scoped tokens) | Entity owner + `<entity>-audit-readonly` principal |
| Cloudflare resource changes | Cloudflare audit log + Citadel workspace apply log | Entity owner + parent (audit-only via ORG-001) |
| GitHub App use | GitHub Actions logs per workspace + GitHub audit log for the org | Entity GitHub owner + parent (audit-only) |
| Hetzner API use | Hetzner activity log | Entity owner + `<entity>-audit-readonly` principal |
| 1Password reads | 1Password activity log per vault | Vault owner; cross-vault read requires explicit grant |
| OPNsense API use | OPNsense reporting + repo `homenetops` evidence | HomeNetOps subsidiary scope |
| Citadel CI runs | GitHub Actions logs (per workspace) + Hetzner runner logs | Citadel owner + entity (read-only via `<entity>-audit-readonly`) |

**Per-entity audit-rotation-log shape:**

The parent provides a TEMPLATE; each entity maintains its own log in its own scope (per ORG-001 — parent does not write into subsidiary scopes during normal operation).

Template (markdown):

```markdown
# Audit and Rotation Log — <entity>

| Date | Credential | Principal change | Action | Verification |
|------|------------|------------------|--------|--------------|
| 2026-MM-DD | `citadel-cloudflare-litecky-rw` | none | annual rotation | `wrangler whoami` returned expected scope |
| ... | ... | ... | ... | ... |
```

The log is created by each entity at first credential issuance and maintained on each rotation. Parent receives evidence of rotation completion (logical entry only) at the next quarterly review cadence.

**Cross-entity rule:** An entity's audit log is readable only by that entity's owners + the read-only audit principal. The parent does NOT have routine read access to subsidiary audit logs. Audit-tier read access for parent-led contamination scans (per Subsidiary Governance Standard §4) is limited to identifier-scope checks, not full credential-use traces.

### 6. Cross-entity prevention contract

Mechanisms intended to ensure one entity's credentials cannot be used by another entity's workflows. Each entry distinguishes **current state** (what the workflow actually does today) from **target state** (what this spec contracts for) and records the gap.

#### Mechanism A: Workspace-resolved CI authentication

- **Current state — partial.** The Citadel `opentofu.yml` workflow resolves the GitHub App **installation** per workspace (`detect-changes` reads `.github/workspace-registry.json`; `create-github-app-token@v1` mints a per-installation IAT with `owner: matrix.org`). However, the `plan` and `apply` jobs both inject a **single repo-wide `CLOUDFLARE_API_TOKEN`** at the job level (see `.github/workflows/opentofu.yml` lines ~121 and ~335). The same Cloudflare token is therefore reachable from every per-org plan/apply matrix run. **GitHub identity is workspace-scoped today; Cloudflare identity is not.**
- **Target state.** Cloudflare authentication resolved per workspace through the same registry mechanism, with per-entity scoped tokens replacing the repo-wide secret.
- **Gap closure.** D5 step 1 (MN-1) issues per-entity scoped Cloudflare tokens; the workflow's `env:` block at the job level is rewritten to resolve the appropriate token per matrix entry.

#### Mechanism B: GitHub Actions environment gating

- **Current state — in place.** The `apply` job uses the `production` environment, requiring Guardian approval before `tofu apply` runs. Secrets are injected at job-start.
- **Target state.** Same; possibly tightened by adding per-environment secrets after MN-1.
- **Gap.** None on the gating itself; gating's value is reduced while the underlying credential is repo-wide (Mechanism A gap).

#### Mechanism C: Per-token Cloudflare scope

- **Current state — gap.** A single shared `secret:cf-api-token-shared` authenticates parent zone IaC, Jefahnierocks zone settings IaC, and (transitively) HomeNetOps ACME and Pulumi home/device automation.
- **Target state.** Per-entity scoped tokens with explicit zone/account/permission boundaries. No account-wide tokens for production use.
- **Gap closure.** D5 step 1 (MN-1).

#### Mechanism D: 1Password vault access

- **Phase A current state — partial.** The shared `Dev` vault holds all credentials; canonical-path + alias naming (per §2) makes mis-use auditable but not preventable. Anyone with `Dev` vault read access can technically see all entries.
- **Phase B target state.** Per-entity vaults with explicit ACLs at synthetic council deployment. Cross-vault access requires explicit grant.
- **Gap.** Phase A is the operating model today; Phase B awaits synthetic council.

#### Mechanism E: PaC enforcement

- **Current state — not implemented.**
- **Target state.** OPA policy that rejects plans consuming tokens with cross-entity scope. Plan input includes which credential resolved which workspace; policy fails if the credential's scope set does not match the workspace's expected scope set.
- **Gap closure.** Not v0.1.0; identified as the natural next step once Mechanisms A and C are at target state.

**Honest summary of v0.1.0 state:** Mechanism B is operational. Mechanisms A (Cloudflare half), C, D (Phase B), and E are gaps that this spec contracts for; closing them is downstream implementation work tracked in D5. The spec is the **contract** that will govern those closures, not a claim that closures have happened.

---

## Out-of-Spec Credentials Registry

Credentials that exist on workstations or in `Dev` but do not yet conform to this spec **MUST** be tracked in a Citadel-maintained inventory at `the-citadel/docs/identity-and-account-management/out-of-spec-credentials.md`. The inventory does not exist as of spec v0.1.0; **creating it is a required deliverable** of this spec's acceptance — listed in the Acceptance Criteria below and in D5 step 1's preconditions.

Each entry MUST record:

- Credential canonical logical path (per §2; Secrets Mgmt §3 namespace)
- 1Password item alias (if applicable)
- Current scope vs target scope
- Migration pathway (replace, rotate-and-narrow, retire)
- Sunset date (max 90 days per Secrets Management Spec v1.3.0 override rule)
- Justification for continued existence

The registry decreases over time. Initial expected entries on creation:

- `cloudflare/<account>/api-token-shared` (canonical) / `secret:cf-api-token-shared` (current naming) — repo-wide Cloudflare token retired as MN-1 lands
- `infra/hetzner/<account>/cloud-rw` (canonical) / `citadel-hetzner-cloud-rw` (current naming) — account-wide Hetzner credential, narrowed when per-entity Hetzner separation lands
- `homenet/opnsense/monitoring-svc` — over-privileged OPNsense API user (HomeNetOps-scope; tracked here as cross-reference; reduced per D5 MN-3)
- Any credentials surfaced by the `secret:cf-tokens-unenumerated` open question once a user-scoped read token enumerates `/user/tokens` for the personal-custodied Cloudflare account

---

## Implementation Path (v0.1.0)

| Phase | Action | Status transition | Deliverable |
|-------|--------|--------------------|-------------|
| 1 | Spec reviewed by Guardian under the documented Covenant-tier single-Guardian quorum exception (per ADR-007 governance note + STATUS.md §Governance Exceptions) | DRAFT → **DRAFT — Accepted for Validation** | Changelog entry recording acceptance; checklist progress |
| 2 | Citadel creates the out-of-spec credentials registry | (still DRAFT — Accepted for Validation) | `the-citadel/docs/identity-and-account-management/out-of-spec-credentials.md` |
| 3 | Citadel issues per-entity Cloudflare scoped tokens replacing `secret:cf-api-token-shared` (MN-1 from D5); workflow `env:` blocks rewritten to resolve per matrix entry | (still DRAFT — Accepted for Validation) | Tokens at canonical paths with 1P aliases; rotation entry in each entity's audit-rotation-log; updated `opentofu.yml` |
| 4 | Citadel publishes the parent template for `audit-rotation-log.md` | (still DRAFT — Accepted for Validation) | Template in Citadel docs; each entity creates its own log |
| 5 | Litecky Editing Services first-real-workload migration (D5 step 7) exercises the spec end-to-end | DRAFT — Accepted for Validation → **ACTIVE** | Empirical evidence; informs v0.2.0 |
| 6 | Spec updated to v0.2.0 based on first-migration findings | ACTIVE | v0.2.0 with refined cadence, verification, and audit shapes |
| 7 | Happy Patterns LLC migration at activation trigger (D5 step 8) validates v0.2.0 in second context | ACTIVE | Second empirical-evidence cycle |

This is the same shape used for ORG-001 ↔ Subsidiary Authority Specification ↔ restatement log: small spec, validate with real work, refine. **The spec does NOT promote to ACTIVE on Guardian acceptance alone — it promotes after first end-to-end migration validation.**

---

## Acceptance Criteria

### Promotion: DRAFT → DRAFT — Accepted for Validation

The spec moves from DRAFT to **DRAFT — Accepted for Validation** when:

- [ ] Guardian review completed under the Covenant-tier single-Guardian quorum exception (recorded explicitly in `STATUS.md §Governance Exceptions` and noted in this spec's changelog with date and authority basis)
- [ ] Cross-references in `the-covenant/policies/README.md` updated to list this spec
- [ ] D5 references this spec as the foundation for step 1 (MN-1)

Acceptance for validation does **not** authorize the spec as ACTIVE policy. It authorizes implementation work to proceed under the spec's contract, with the explicit understanding that the spec will be refined based on what the work teaches.

### Promotion: DRAFT — Accepted for Validation → ACTIVE

The spec promotes to **ACTIVE** only when ALL of the following hold:

- [ ] Citadel out-of-spec credentials registry exists at `the-citadel/docs/identity-and-account-management/out-of-spec-credentials.md` with at minimum the four expected entries (shared CF token, account-wide Hetzner, OPNsense `monitoring_svc`, unenumerated CF tokens placeholder)
- [ ] First credential issued under this spec's contract: per-entity Cloudflare token replacing `secret:cf-api-token-shared` (MN-1)
- [ ] Citadel `opentofu.yml` workflow `env:` blocks rewritten so the Cloudflare token is resolved per matrix entry, not injected repo-wide (closes Mechanism A's Cloudflare gap and Mechanism C)
- [ ] First per-entity `audit-rotation-log.md` exists (in any entity scope) with at least one entry using canonical logical paths (per §2)
- [ ] First end-to-end migration validated: Litecky Editing Services Cloudflare workspace operating under per-entity scoped credentials (D5 step 7)
- [ ] No regression in cross-entity prevention: Mechanism B remains in place; Mechanisms A and C reach target state; Mechanism D Phase A operating; Mechanism E status-recorded as future work
- [ ] Changelog entry recording the ACTIVE promotion with reference to the validation evidence

---

## Compliance with Higher-Authority Specs

- **Principle 5 (IaC)**: All credential structure is recorded as code (registry, naming convention, audit-rotation-log template). No silent runtime configuration.
- **Principle 9 (Zero Trust)**: Cross-entity credential reach is explicitly prevented (Mechanisms A–E). No implicit trust between workspaces.
- **Principle 10 (Least Privilege)**: Tokens are zone-scoped, account-scoped, or workspace-scoped; account-wide tokens for production use are retired.
- **Principle 15 (Three Circles of Trust)**: Per-entity boundaries enforced at credential level; cross-entity access requires explicit attribution.
- **SEC-005 (Machine Identity)**: This spec extends SEC-005's machine identity types to the multi-entity case; no new identity types are introduced.
- **ORG-001 (Subsidiary Authority)**: The `<entity>-audit-readonly` principal does not violate ORG-001's audit-only parent access — parent retains read access for contamination scans, but per-entity audit logs are entity-scoped.
- **GOV-003 (Break-Glass)**: The `<entity>-owner-break-glass` principal is the per-entity application of GOV-003; cross-entity break-glass remains 24-hour reconciliation per GOV-003.
- **Secrets Management Specification v1.3.0**: This spec inherits classification, lifecycle, and storage rules from Secrets Management. No re-statement of those rules; this spec only adds the per-entity organizational layer.

---

## What This Spec Leaves Explicit (For Future Work)

- **Synthetic council credential model** — slot reserved (§3); details land at v0.2.0 when council is deployed.
- **Per-entity Hetzner credential separation** — naming convention defined (§2); separation timing is per-entity (LLC trigger-driven).
- **Mechanism E (PaC for cross-entity prevention)** — identified as natural next step; not v0.1.0.
- **`iam-specification.md` REWRITE PENDING** — unaffected; this spec is narrower. The broader rewrite covers AWS IAM Identity Center, GCP IAM, federated SSO, agent sandbox cages, and break-glass alerting infrastructure.
- **POC 3 (Authentik) human SSO** — deferred per D5; not addressed here.

---

## References

- **SEC-005 — Machine Identity** — `../sec-005-machine-identity.md` (machine identity types this spec extends to multi-entity)
- **ORG-001 — Subsidiary Authority and Identity Isolation** — `../org-001-subsidiary-authority.md` (entity boundary rules)
- **GOV-003 — Break-Glass Procedures** — `../gov-003-break-glass.md` (emergency credential access)
- **Secrets Management Specification** v1.3.0 — `secrets-management.md` (lifecycle and storage rules inherited)
- **Subsidiary Authority Specification** v1.0.3 — `subsidiary-authority.md` (per-entity authority model)
- **Cloudflare Ownership Transition Specification** v1.1.0 — `cloudflare-ownership-transition.md` (provider account placement rule)
- **iam-specification.md** (REWRITE PENDING) — `iam-specification.md` (broader IAM rewrite, deferred)
- **D5: Credential Strategy Recommendation** — `.claude/orchestration/cloudflare-resource-management/CREDENTIAL-STRATEGY-RECOMMENDATION-2026-05-02.md` (sequencing this spec implements)
- **DIRECTIVE-2026-05-02-routing-inventory-categorization** — `.claude/orchestration/directives/DIRECTIVE-2026-05-02-routing-inventory-categorization.md` (parent directive that produced D5)

---

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2026-05-03 | Agent | Initial DRAFT v0.1.0 — narrow spec answering six questions for multi-entity scoped credentials. Respects D5 sequencing. Reserves synthetic council principal slot. Does not replace `iam-specification.md` REWRITE PENDING work. |
| 2026-05-03 | Agent | DRAFT v0.1.0 refined pre-acceptance based on consult review: (1) §6 Mechanism A reframed from "in place" to current/target/gap (Citadel `opentofu.yml` injects repo-wide `CLOUDFLARE_API_TOKEN` into every plan/apply matrix job — workspace-scoping covers GitHub identity only); (2) §4 rotation cadences corrected from "annual" to **180 days** to inherit Secrets Management Specification v1.3.0 §5.4 targets (no relaxation); (3) §2 vault structure rewritten with canonical Secrets Mgmt §3 logical paths as authoritative + 1Password item names as aliases; (4) Status wording clarified — DRAFT → "Accepted for Validation" → ACTIVE in two distinct promotions, not one; (5) Out-of-Spec Credentials Registry made an explicit required deliverable rather than described as already existing. |
