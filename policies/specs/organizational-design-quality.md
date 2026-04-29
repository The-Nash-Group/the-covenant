# Organizational Design Quality Specification

**Version:** 0.1.0
**Status:** DRAFT
**Date:** 2026-04-29
**Authority:** Draft Covenant-owned anchor specification; not yet ratified as an active policy
**Catalog IDs:** `ODQ-*` identifiers are design-review and catalog identifiers only. They are not formal Covenant policy IDs.
**Implements:** Principle 5 (Infrastructure as Code), Principle 6 (No Committed Secrets), Principle 9 (Zero Trust), Principle 10 (Least Privilege), Principle 11 (Measure Everything), Principle 12 (Executable Runbooks), Principle 13 (Code Without Docs is Incomplete), Principle 14 (Progress Without Breakage), Principle 15 (Three Circles of Trust), Principle 16 (Living Law)
**Related Policies:** INF-001, SEC-001, SEC-002, SEC-003, SEC-004, SEC-005, OPS-001, OPS-002, OPS-004, OPS-005, OPS-010, DOC-001, DEP-001, DEP-002, GOV-002, GOV-003, GOV-007, GOV-010, AGT-001, ORG-001
**Related Specifications:** Subsidiary Authority, Secrets Management, Cloudflare Ownership Transition, GitHub Machine Identity, IAM Specification

---

## 1. Metadata

This document is a Covenant-owned anchor specification for organizational design quality. It sets the quality bar for classifying, approving, operating, and retiring organizational control surfaces across parent, subsidiary, and project tiers.

It does not create a new policy ID. If the Council later decides a formal policy is required, that policy must be created through the Covenant amendment process in GOV-002.

The `ODQ-*` identifiers used here and in parent catalog artifacts are review handles. They help reviewers map requirements, gaps, and evidence. They do not compete with existing Covenant policy families such as `SEC-005`, `GOV-010`, or `ORG-001`.

> No organizational system, integration, identity, agent, model, tool, data surface, vendor relationship, domain, repository, network path, or infrastructure component may enter or remain in production unless it has a named owner, documented purpose, least-privilege access, auditable change path, monitored runtime behavior, recoverable state, reviewed dependencies, and a defined lifecycle.

---

## 2. Purpose

This specification defines the Nash Group's organization-wide quality bar for design approval and control-surface classification.

It answers four questions:

1. What must be known before a control surface is allowed into production?
2. Who owns the control surface, its risk, its cost, its data, and its retirement?
3. What evidence proves the control surface remains within the quality bar?
4. Which gaps require smaller domain specifications instead of being hidden inside one omnibus document?

This is not a product-selection document and does not choose vendors, tools, platforms, or implementation paths. Implementation belongs in the appropriate repository, usually `the-citadel` for shared infrastructure enforcement and the owning subsidiary or project repository for local evidence.

This specification must not duplicate existing policy. Where existing policies already define requirements, this document references them and only defines how they fit into design quality review.

---

## 3. Audience and Scope

### 3.1 Audience

| Audience | Uses This Specification To |
|---|---|
| Parent L0 Guardians and agents | Publish the quality bar, classify parent-owned control surfaces, maintain schemas and catalogs, and audit adoption state |
| Subsidiary L1 stewards | Restate adopted requirements in their own voice and maintain subsidiary-owned inventories and evidence |
| Project L2 maintainers and agents | Implement repo-local controls, tests, runbooks, evidence, and lifecycle work inside the subsidiary boundary |
| Reviewers | Decide whether a design is ready, blocked, accepted with exception, or out of scope |

### 3.2 Scope

This specification applies to organizational control surfaces, including:

- repositories, services, APIs, CI workflows, and runner groups;
- human identities, machine identities, agents, MCP servers, tools, connectors, models, and model providers;
- cloud accounts, SaaS tenants, vendor integrations, OAuth clients, webhooks, secrets, certificates, and keys;
- domains, DNS zones, email domains, network segments, devices, infrastructure components, observability surfaces, backups, and incident playbooks;
- data stores, datasets, data classes, policy controls, and other resources that carry operational authority or organizational risk.

The requirement scales by risk tier, not by headcount alone. A sole-developer entity may keep lightweight evidence for low-risk work, but a single-person owner does not exempt customer-facing, financial, sensitive-data, shared-identity, or critical infrastructure surfaces from stronger controls.

### 3.3 Out of Scope

This specification does not:

- define detailed data privacy rules;
- define AI model evaluation, MCP server review, API security, network governance, or vendor risk in full;
- place sensitive subsidiary metadata, bank or tax values, private account values, credentials, or raw vendor evidence in git;
- give parent-scoped agents runtime authority over subsidiary-scoped sessions;
- add automation to this repository.

Those gaps are named in Section 13 for follow-up domain specifications.

---

## 4. Authority and Restatement

The authority model follows ORG-001 and the Subsidiary Authority Specification.

| Tier | Authority | Design Quality Responsibility |
|---|---|---|
| Parent L0 | Publishes specs, schemas, catalogs, shared standards, and cross-entity audit expectations | Defines this quality bar, maintains parent-side catalog schema, records restatement status, and audits cross-entity control surfaces |
| Subsidiary L1 | Owns its governance, voice, repositories, CI, seats, evidence, and operating procedures | Restates adopted requirements in its own voice and maintains its own control-surface inventory and evidence |
| Project L2 | Owns code, tests, runbooks, deployment path, and repo-local controls | Implements the restated L1 requirements and produces project-local evidence |

Parent publication is not session inheritance. A subsidiary-scoped agent must not read this parent specification during normal operation. The correct flow is:

1. Parent publishes this specification and any migration packet.
2. A human relays the adoption task into the subsidiary context.
3. The subsidiary authors its own restatement in its own voice and on its own authority.
4. Parent records adoption and drift state in the parent restatement log.

Parent agents may read subsidiary repositories for approved audit, but parent write access to subsidiary repositories remains forbidden except under explicit break-glass or cross-entity approval as defined by ORG-001 and GOV-003.

---

## 5. Control Surface Classification

Every R1+ control surface must be represented by an inventory entry compatible with the parent control-surface catalog schema when it is visible to parent audit, unless an explicit exception is recorded. R0 entries may remain lighter, but they still need owner, purpose, lifecycle state, and a no-secrets-in-git posture.

### 5.1 Classification Axes

| Axis | Required Fields |
|---|---|
| Authority | `authority_tier`, `governance_level`, `semantic_owner`, `current_host`, `target_home`, `transfer_trigger` |
| Object | `object_class`, `risk_tier`, `lifecycle_phase`, production/public/agent/spend flags where applicable |
| Purpose | documented purpose, business purpose where applicable, environments, dependencies, graduation criteria, decommission criteria |
| Ownership | accountable owner, technical owner, and additional owner roles required by Section 6 |
| Governance | principle references, policy/spec references, review cadence, restatement requirement, exceptions |
| Identity | human access, machine identities, break-glass path, credential types |
| Data | classification, retention, storage locations, sharing boundaries, privacy obligations |
| Network | ingress, egress, admin path, DNS zones |
| Evidence | design reviews, plans, audit logs, access reviews, restore tests, runtime observations, and other current evidence |

### 5.2 Object Classes

The parent schema currently recognizes these object classes:

`api`, `agent`, `backup`, `certificate`, `ci-runner`, `ci-workflow`, `cloud-account`, `data-class`, `data-store`, `device`, `dns-zone`, `domain`, `email-domain`, `integration`, `machine-identity`, `mcp-server`, `mcp-tool`, `model`, `model-provider`, `network-segment`, `observability-surface`, `policy-control`, `repository`, `saas-tenant`, `secret`, `service`, `vendor`, and `webhook`.

Adding an object class is a schema change. Schema changes must be reviewed with the same care as other parent semantic changes because downstream catalogs and subsidiary restatements may depend on them.

### 5.3 Lifecycle Phases

Lifecycle state must be explicit. The current allowed phases are:

`proposed`, `concept`, `experimental`, `planned`, `active`, `paused`, `restricted`, `deprecated`, `superseded`, `archived`, and `retired`.

A production control surface with no lifecycle phase fails design review.

---

## 6. Ownership Requirements

Every R1+ control surface must record named ownership. At small scale, one human may hold multiple roles, but each role must still be explicit.

| Role | Required When | Responsibility |
|---|---|---|
| Accountable owner | Always for R1+ | Owns the control surface and accepts residual risk |
| Backup owner | R2+; recommended for R1 | Can respond when the accountable owner is unavailable |
| Business sponsor | R2+ or spend/customer impact | Owns the business purpose and priority |
| Technical owner | Always for R1+ | Owns implementation, maintenance, and technical decisions |
| Security owner | R2+; always for identity, data, public, agent, or vendor surfaces | Owns risk review, least privilege, and security evidence |
| Operational owner | R2+ | Owns runtime health, alerts, runbooks, and incident readiness |
| Data steward | Data-bearing surfaces | Owns data classification, retention, access, and deletion obligations |
| Cost owner | Spend-bearing surfaces | Owns budget, quotas, anomaly response, and cleanup |
| Decommissioning owner | R2+; recommended for R1 | Owns retirement criteria and cleanup completion |

Ownership records must not contain private account values, bank or tax identifiers, credentials, or raw vendor evidence. Store sensitive material only in the approved secrets authority. Git-tracked records may contain pointers, attestations, and non-sensitive summaries.

---

## 7. Risk Tiers

Risk tier controls the depth of review and evidence required.

| Tier | Definition | Minimum Posture |
|---|---|---|
| R0 | Personal, local, non-production, no sensitive data, no material spend | Owner, purpose, lifecycle, no secrets in git |
| R1 | Internal or experimental organizational surface | Inventory entry, scoped credentials, repo or runbook, annual review |
| R2 | Production low-risk surface | Review gates, SSO/MFA where feasible, logs, backups, access review |
| R3 | Customer, financial, sensitive-data, public, or agent-enabled production surface | IaC/Policy as Code where feasible, drift detection, central logs, restore test, threat model |
| R4 | Shared identity, cross-entity, critical infrastructure, or high-risk autonomous agent surface | Short-lived identity where feasible, continuous evidence, tabletop or GameDay, human approval gates |

### 7.1 Tier Escalation Rules

A control surface must move to at least R3 if it is customer-facing, public-facing, data-bearing with sensitive or financial data, production agent-enabled, or responsible for financial processing.

A control surface must move to R4 if it controls shared identity, cross-entity access, critical infrastructure, high-risk autonomous production action, or a central authority boundary used by multiple subsidiaries.

### 7.2 Sole-Developer Scaling Rule

Sole-developer and small-entity realities are expected. Scaling down means reducing ceremony for low-risk surfaces, not removing explicit ownership or hiding risk.

At sole-developer scale:

- one human may hold multiple owner roles;
- R0 and R1 evidence may be lightweight;
- R2+ production evidence must still exist;
- R3 and R4 controls may be phased, but any missing control needs an exception owner, compensating control, review date, and expiration date.

---

## 8. Maturity Levels

Maturity is evidence-based, not self-declared.

| Level | Name | Definition |
|---|---|---|
| 0 | Ad hoc | Control exists in practice but is not documented or repeatable |
| 1 | Documented | Owner, purpose, lifecycle, and basic operating notes exist |
| 2 | Controlled | Review gates, access boundaries, runbooks, and backup expectations are documented and used |
| 3 | Automated | IaC/Policy as Code, validation, drift detection, logging, and evidence collection are automated where practical |
| 4 | Adaptive | Continuous evidence, exercises, metrics, feedback loops, and risk-based improvements are active |

Minimum target maturity by risk tier:

| Risk Tier | Minimum Target |
|---|---|
| R0 | Level 1 when retained beyond local experimentation |
| R1 | Level 1 |
| R2 | Level 2 |
| R3 | Level 3 target, with documented exceptions for controls not yet automated |
| R4 | Level 4 target, with human approval gates and continuous evidence for critical controls |

Reviewers must score maturity from evidence such as design records, plans, audit logs, access reviews, backup restore tests, policy checks, and incident exercises. A maturity label without supporting evidence is not accepted.

---

## 9. Required Artifacts by Risk Tier

| Artifact | R0 | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| Named owner and purpose | Required | Required | Required | Required | Required |
| Lifecycle phase and decommission criteria | Required | Required | Required | Required | Required |
| No secrets in git | Required | Required | Required | Required | Required |
| Inventory entry | Optional | Required | Required | Required | Required |
| Scoped credential record | If credentials exist | Required if credentials exist | Required | Required | Required |
| Repo README, runbook, or operating note | Optional | Required | Required | Required | Required |
| Design review gates | Optional | Recommended | Required | Required | Required |
| SSO/MFA where feasible | Optional | Recommended | Required where feasible | Required where feasible | Required where feasible |
| Access review | Optional | Annual | At least annual | At least semi-annual | At least quarterly or continuous |
| Runtime logs and audit trail | Optional | Recommended | Required | Centralized where feasible | Continuous evidence required |
| Backup and restore evidence | Optional | If stateful | Required if stateful | Restore test required | Restore test and exercise required |
| Threat model | Optional | Recommended for novel risk | Required for external, identity, data, or agent surfaces | Required | Required |
| IaC/Policy as Code | Optional | Recommended | Required where feasible | Required or exception | Required or exception |
| Drift detection | Optional | Optional | Recommended | Required where feasible | Required |
| Cost owner and budget guardrail | If spend-bearing | If spend-bearing | Required if spend-bearing | Required | Required |
| Human approval gates | Optional | Optional | Required for risky changes | Required | Required |
| Incident exercise | Optional | Optional | Recommended | Required for critical/customer-facing surfaces | Required |

Existing policy sources remain authoritative for their domains:

- secret storage and rotation: Secrets Management Specification, SEC-002, SEC-005;
- machine identity: SEC-005 and GitHub Machine Identity Specification;
- infrastructure placement and drift: INF-001 and Cloudflare Ownership Transition Specification;
- review and change management: OPS-001, OPS-002, GOV-002;
- documentation and runbooks: DOC-001, OPS-005;
- subsidiary identity boundaries: ORG-001 and Subsidiary Authority Specification.

---

## 10. Design Review Gate DAG

Design review gates are dependent gates, not a flat checklist.

```text
G1 Purpose and ownership
  -> G2 Threat model
      -> G3 Identity and access
      -> G4 Infrastructure, DNS, network, and routing
      -> G5 Data controls
      -> G6 Supply chain
          -> G7 Observability and audit
              -> G8 Recovery and incident response
                  -> G9 Cost and sustainability
                      -> G10 Exception review
```

G2 must precede G3 through G7. G10 is a release blocker for unresolved risk, not a cleanup step after approval.

| Gate | ODQ Handle | Required Question | Primary Existing Coverage |
|---|---|---|---|
| G1 Purpose and ownership | ODQ-GATE-01 | Is the purpose clear, and are owner roles named? | ORG-001, GOV-010, this specification |
| G2 Threat model | ODQ-GATE-02 | What can go wrong, who can cause it, and what boundaries matter? | SEC-001, SEC-004; follow-up threat-modeling spec needed |
| G3 Identity and access | ODQ-GATE-03 | Who or what can act, by which identity, with what scope, and for how long? | SEC-001, SEC-003, SEC-005 |
| G4 Infrastructure, DNS, network, and routing | ODQ-GATE-04 | Where does it run, how is traffic routed, and which authority owns placement? | INF-001, Cloudflare Ownership Transition; follow-up network and domain specs needed |
| G5 Data controls | ODQ-GATE-05 | What data exists, where does it flow, who can access it, and how long is it retained? | Secrets Management for secret material; follow-up data/privacy spec needed |
| G6 Supply chain | ODQ-GATE-06 | What code, dependencies, vendors, tools, models, or connectors are trusted? | DEP-002; follow-up supply-chain, vendor, model, and MCP specs needed |
| G7 Observability and audit | ODQ-GATE-07 | Can runtime behavior and change actors be reconstructed? | OPS-004, AGT-001 |
| G8 Recovery and incident response | ODQ-GATE-08 | Can state be restored and incidents contained? | OPS-005, OPS-010, GOV-003 |
| G9 Cost and sustainability | ODQ-GATE-09 | Who owns spend, quotas, anomaly response, and cleanup? | Follow-up FinOps and agent cost spec needed |
| G10 Exception review | ODQ-GATE-10 | Are unresolved controls owned, time-bound, compensated, and reviewed? | GOV-003, GOV-007; exception register fields in catalog schema |

For R0 and R1, gate evidence may be concise. For R2+, a reviewer must be able to trace gate decisions to evidence. For R3 and R4, missing gate evidence requires an explicit exception.

---

## 11. Minimum Failure Modes

A design fails review if any of the following are true and no approved exception exists:

1. A production control surface has no named owner.
2. Production trust depends on network position instead of identity, posture, and policy.
3. Shared human accounts are used for routine work.
4. Machine or agent credentials lack owner, scope, and review date.
5. DNS, firewall, IAM, CI, or routing changes cannot be traced to an approval and actor.
6. Agents can act in production without distinct identity, scoped permissions, logs, and a shutdown path.
7. Production cannot be reconstructed from documented configuration and backups.
8. A critical service has no tested restore path.
9. Secrets appear in git, tickets, chat, docs, or unprotected local files.
10. Reviewers cannot tell what data exists, where it flows, who can access it, and how long it is retained.
11. A vendor, SaaS tenant, OAuth client, webhook, MCP connector, model provider, or tool has production access without a named owner and removal path.
12. A spend-bearing surface has no cost owner or anomaly response path.
13. A deprecated or retired surface leaves behind active credentials, DNS records, firewall rules, storage, alerts, subscriptions, or vendor access.

---

## 12. Evidence and Continuous Compliance

Evidence must be current enough for review. Stale evidence is not evidence.

Accepted evidence types include:

- inventory entries;
- ADRs and design review records;
- reviewed OpenTofu plans or equivalent implementation plans;
- pull requests and approval records;
- policy tests and static validation results;
- drift checks and configuration exports;
- access reviews;
- threat models and risk registers;
- data classification maps and data-flow diagrams;
- runtime observations, logs, alerts, and audit trails;
- backup restore tests;
- incident exercises, tabletop results, or GameDay results;
- SBOMs and artifact attestations;
- vendor attestations and non-sensitive vendor review summaries;
- domain registrar evidence and certificate/key inventories;
- maturity assessments and KPI reports.

Evidence records must not contain raw credentials, bank/tax/private account values, sensitive subsidiary metadata, or raw vendor materials that are not appropriate for git. Git-tracked evidence may contain non-sensitive summaries, timestamps, hashes, references, and pointers to approved storage locations.

Continuous compliance means:

1. catalog entries stay current as owners, risk, lifecycle, and hosting change;
2. evidence has a review cadence appropriate to risk tier;
3. exceptions have owner, compensating control, review date, and expiration date;
4. drift is remediated or accepted as a documented exception;
5. incidents and exercises feed back into the catalog, policies, specs, and runbooks.

---

## 13. Domain Gap Backlog

This anchor spec intentionally does not solve every domain. The following follow-up specifications or policy updates are required to close known gaps.

| Priority | Domain Gap | Planned Follow-Up |
|---|---|---|
| 1 | Data classification and privacy | Define data classes, retention, deletion, legal hold, lower-environment data, agent data access, and privacy obligations |
| 1 | AI model governance | Define model selection, evaluation, model cards, prompt/tool versioning, data provenance, rollback, and provider-switch evidence |
| 1 | MCP/tool/connector governance | Define MCP server and tool review, allowlists, schema versioning, authorization, audit, community server intake, and connector lifecycle |
| 1 | API lifecycle and API security | Define API cataloging, OpenAPI/AsyncAPI expectations, authn/authz, rate limits, versioning, deprecation, consumer contracts, and OWASP API coverage |
| 1 | Domain/DNS/registrar/email identity lifecycle | Define registrar custody, renewal, DNSSEC, email auth, split-horizon, account recovery, and DNS automation lifecycle |
| 2 | Network/firewall/IPAM | Define network segments, ingress, egress, firewall changes, admin paths, IPAM, and network logging |
| 2 | Vendor/SaaS/third-party risk | Define SaaS inventory, SSO/MFA/logging expectations, third-party OAuth/webhook review, vendor access, contingency plans, and baseline assessments |
| 2 | FinOps and LLM/agent cost controls | Define budgets, cost owners, quota controls, anomaly response, LLM/agent spend controls, and cleanup triggers |
| 2 | Supply-chain provenance/SBOM/signing | Define SBOM expectations, artifact signing, provenance targets, dependency intake, CI runner identity, and release attestations |
| 2 | Endpoint/device posture | Define managed workstation and device posture, MDM/EDR expectations, disk encryption, lost-device process, and physical security baseline |
| 3 | PQC/crypto-agility | Define cryptographic inventory, algorithm agility, certificate/key review, and post-quantum migration planning |
| 3 | Personnel security/acceptable use | Define acceptable use, onboarding/offboarding, confidential handling, and access conduct expectations |
| 3 | Threat-modeling methodology | Define approved methods, misuse case coverage, required diagrams, cadence, and acceptance criteria |
| 3 | Resilience exercises | Define tabletop, GameDay, backup restore, dependency outage, and identity-outage exercise cadence |
| 3 | Program KPIs | Define maturity scoring, design-quality metrics, evidence freshness, exception burn-down, and adoption reporting |

The follow-up list must be maintained in the parent design-quality catalog until each gap is closed by a Covenant specification, a policy update, a Citadel implementation artifact, or a deliberate decision not to govern that domain.

---

## 14. Self-Governance

### 14.1 Spec Owner

This draft is owned by the Covenant governance surface until ratified, replaced, or retired. Human Guardians retain final authority over any change in meaning.

### 14.2 Review Cadence

While in draft, review this specification:

- before ratification;
- after the first parent control-surface catalog entries are created;
- after the first subsidiary restatement is completed;
- whenever a Priority 1 domain gap receives a follow-up specification.

After ratification, review at least semi-annually or when a material domain gap changes.

### 14.3 Activation Criteria

This specification must remain DRAFT until all of the following are true:

1. At least one sample parent control-surface entry exists.
2. At least one subsidiary restatement dry run has been completed.
3. The Council has reviewed whether `ODQ-*` remains catalog-only or becomes a formal Covenant policy family.

### 14.4 Change Process

Changes that alter the quality bar, authority model, risk tiers, minimum failure modes, or restatement model are Covenant-level changes and must follow GOV-002.

Clarifying edits that do not change meaning may be proposed as documentation improvements, but they still require Guardian review before merge.

### 14.5 Versioning Rules

- Patch version: wording clarification, typo fix, or reference update with no meaning change.
- Minor version: new evidence type, object class, artifact expectation, or review gate clarification that does not change the governing thesis.
- Major version: changed authority model, risk-tier semantics, minimum failure mode, or production entry requirement.

### 14.6 Catalog and Schema Updates

Parent catalog and schema artifacts are implementation-adjacent semantic supports, not substitutes for this specification.

- `.org/ontology/design-quality-catalog.yaml` maps `ODQ-*` handles to current coverage, gaps, and planned artifacts.
- `.org/schemas/json-schema/control-surface-catalog-v1.json` defines machine-readable inventory shape.
- Parent schema changes must not store sensitive values in git.
- Catalog gap closure must cite the artifact that closes the gap.
- Subsidiary-specific adoption state belongs in the parent restatement log, not in subsidiary agent-session context.

---

## 15. Subsidiary Restatement

Subsidiaries adopt this quality bar by restating it. They do not inherit it by pointer, and they do not expose this parent document to project agents during normal operation.

### 15.1 Restatement Requirements

A subsidiary restatement must:

1. be written in the subsidiary's own voice;
2. state the subsidiary's own quality bar for systems, integrations, identities, agents, data, vendors, domains, and infrastructure under its authority;
3. define risk tiers and required artifacts in terms the subsidiary can operate;
4. name where the subsidiary keeps its inventory and evidence;
5. keep confidential legal, tax, bank, private account values, credentials, and raw vendor evidence out of git;
6. record adopted scope and deviations through a parent-visible restatement log entry, not by making parent governance runtime context for subsidiary agents.

### 15.2 Parent-to-Subsidiary Flow

The standard flow is:

1. Parent publishes this draft and the restatement template.
2. Parent creates or updates the migration packet.
3. A human opens a subsidiary-scoped session and relays the adoption task.
4. The subsidiary drafts its restatement in its own repository or operating shell.
5. Parent records adoption state, restated-from version, review date, and known gaps in the parent restatement log.

### 15.3 Project L2 Behavior

Project agents follow the subsidiary's restated rules and the project repository contract. They do not need this parent specification in their runtime context.

When a project graduates to a higher risk tier, changes semantic owner, moves operational host, or receives new sensitive data, the subsidiary updates the relevant inventory, evidence, and restatement state before treating the new posture as approved.

---

## Related Documents

- **Source Principles:** [PRINCIPLES.md](../../PRINCIPLES.md)
- **Governance:** [GOVERNANCE.md](../../GOVERNANCE.md), [GOV-002: Covenant Amendment Process](../gov-002-amendment-process.md)
- **Subsidiary Authority:** [ORG-001: Subsidiary Authority and Identity Isolation](../org-001-subsidiary-authority.md), [Subsidiary Authority Specification](./subsidiary-authority.md), [ADR-007: Subsidiary Authority and Identity Isolation](../../docs/architecture/007-subsidiary-authority-and-identity-isolation.md)
- **Security and Identity:** [SEC-001: Zero Trust](../sec-001-zero-trust.md), [SEC-003: Least Privilege](../sec-003-least-privilege.md), [SEC-004: Security Baseline](../sec-004-security-baseline.md), [SEC-005: Machine Identity](../sec-005-machine-identity.md), [GitHub Machine Identity Specification](./github-machine-identity.md)
- **Secrets:** [SEC-002: Secret Scanning](../sec-002-secret-scanning.md), [Secrets Management Specification](./secrets-management.md)
- **Infrastructure:** [INF-001: Infrastructure as Code](../inf-001-infrastructure-as-code.md), [Cloudflare Ownership Transition Specification](./cloudflare-ownership-transition.md)
- **Operations:** [OPS-001: Change Management](../ops-001-change-management.md), [OPS-004: Observability](../ops-004-observability.md), [OPS-005: Runbooks](../ops-005-runbooks.md), [OPS-010: Emergency Response](../ops-010-emergency-response.md)
- **Dependencies:** [DEP-001: Breaking Change Management](../dep-001-breaking-changes.md), [DEP-002: Three Circles of Trust](../dep-002-dependency-circles.md)
- **Documentation:** [DOC-001: Documentation Requirements](../doc-001-documentation.md)

---

## Changelog

| Date | Author | Summary |
|---|---|---|
| 2026-04-29 | Codex | Initial draft anchor specification for organizational design quality; defines authority tiers, risk tiers, maturity levels, review gates, evidence requirements, domain gap backlog, and subsidiary restatement model without creating a new formal policy ID. |
