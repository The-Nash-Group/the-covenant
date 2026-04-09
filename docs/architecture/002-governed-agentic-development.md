# ADR-002: Adopt Governed Agentic Development (Constitutional API)

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2025-11-23 |
| **Last Updated** | 2026-03-02 |
| **Author** | Agent (The Architect) |
| **Governance Level** | Covenant (2 Watchers + 2 Mentors, 72h debate) |
| **Status** | Proposed |
| **Related ADRs** | ADR-001, ADR-004 |

## Context

The Nash Group is transitioning to a "Single-Player Empire" model where a lone human Guardian delegates execution to autonomous AI agents. However, the current "Human-in-the-Loop" model is unscalable and prone to "rubber-stamping" complex changes. Furthermore, AI agents are probabilistic and prone to hallucination, sycophancy, and drift. We lack a deterministic mechanism to ensure agent actions are aligned with our Covenant (Constitution) before they reach production.

Research (see `synthetic-governance-research.md`) indicates that:
1. Single-agent reviews suffer from sycophancy and mode collapse.
2. Traditional API keys for agents are a security liability (secrets management).
3. "Consensus" should be the result of adversarial dialectic, not simple voting.

## Decision

We will adopt the **Constitutional API** model for all agentic development, implementing a "Synthetic Council" as the mandatory "Iron Gate" for infrastructure and policy changes.

### 1. The Synthetic Council

We will deploy a multi-agent adversarial consensus engine to validate all Architecture Decision Records (ADRs) and Infrastructure-as-Code (IaC) changes.

* **The Steward (Risk Engine)**: Powered by a high-reasoning model, tasked with finding security and policy violations.
* **The Catalyst (Growth Engine)**: Powered by a high-velocity model, tasked with proposing implementation paths.
* **The Judge (Adjudicator)**: A neutral arbiter that renders a verdict based purely on The Covenant.

**Implementation Status**: The Synthetic Council package (`packages/synthetic-council`) was prototyped but never committed. It must be rebuilt from `governance-config.yaml` and `iron-gate.yml`. See follow-up item FU-1.

### 2. The Iron Gate (Identity-Based Signing)

We will replace static API keys with **identity-based authentication** using the Nash Group's federated identity chain:

* **Identity Provider**: Authentik (self-hosted on Hetzner as the-shield) with Google Workspace as the upstream identity source.
* **Auth Chain**: Google Workspace → Authentik → GitHub OAuth apps (one per org). This is the "Poor Man's Enterprise" pattern — OAuth-based SSO rather than GitHub Enterprise SAML (see ADR-004).
* **Secrets Management**: Infisical (self-hosted at infisical.jefahnierocks.com) manages all secrets and API tokens. gopass serves as the offline mirror for break-glass scenarios.
* **Signing**: Every decision will be cryptographically signed using ephemeral keys (Fulcio/Sigstore).
* **Transparency**: All signatures are logged to a transparency log (Rekor).

This eliminates static API keys and long-lived credentials — the original goal of the Iron Gate design.

### 3. The Signed Decision Record (SDR)

We will standardize on the SDR format (combining ADRs with Sigstore bundles) as the atomic unit of governance. No merge to `main` in protected repositories (`the-covenant`, `the-citadel`) is allowed without a valid, verified SDR.

### 4. Subsidiary Governance Scoping

The Synthetic Council applies to **Covenant and Citadel-level changes** across all Nash Group repositories. However:

* **Stronghold-level changes** in subsidiary orgs (happy-patterns, jefahnierocks, litecky-editing, seven-springs) may bypass the Council per governance level.
* Subsidiaries inherit the 16 Covenant principles but can add their own constraints.
* the-citadel manages subsidiary GitHub orgs via multi-provider Terraform — infrastructure changes always require Citadel governance regardless of which org they affect.

### 5. The Workflow

1. Agent creates a `proposal/*` branch.
2. Agent drafts an ADR.
3. Synthetic Council debates the ADR against `the-covenant/policies`.
4. If approved, the Council signs the decision (SDR).
5. The Iron Gate policy controller verifies the signature.
6. PR is unlocked for human ratification (optional for low-risk, mandatory for high-risk).

## Consequences

### Positive

* **Deterministic Alignment**: Governance becomes code. Policies are enforced mathematically.
* **Security**: Elimination of long-lived agent credentials via Authentik + Infisical.
* **Scalability**: The Guardian is relieved of low-level code review, focusing on intent.
* **Auditability**: Every decision has a cryptographic reasoning trace.
* **Multi-Org Coverage**: Auth chain spans all five GitHub orgs through single identity provider.

### Negative

* **Latency**: The debate process adds time (minutes) to the feedback loop.
* **Cost**: Increased token usage for multi-turn debates.
* **Complexity**: Requires maintenance of Authentik, Infisical, and Sigstore/OIDC infrastructure.
* **Rebuild Required**: Synthetic Council package must be rebuilt from scratch (FU-1).

## Compliance

* **GOV-001**: Supports "Living Principles" by formalizing the amendment process.
* **SEC-001**: Enforces "Zero Trust" by requiring cryptographic proof for every action.
* **INF-001**: Enforces "Infrastructure as Code" by treating governance decisions as code artifacts.
* **Principle #9**: Zero Trust — Authentik enforces identity-based access across all orgs.
* **Principle #10**: Least Privilege — per-org OAuth scoping limits blast radius.

## References

* `the-covenant/history/reports/2025-11/ORGANIZATION-GOVERNANCE-IMPLEMENTATION-REPORT.md`
* `the-covenant/history/research/synthetic-governance-research.md`
* ADR-004: Federated Multi-Org Architecture (identity federation details)
* Follow-up item FU-1: Synthetic Council rebuild

---

> **Living Documents**: ADRs may be updated when facts change, but changes require Guardian approval. Edit in place and add a changelog entry rather than creating a superseding ADR.

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2025-11-23 | Agent (The Architect) | Initial creation — Constitutional API model proposed |
| 2026-03-02 | Agent | Updated auth chain to reflect Authentik + Infisical. Added subsidiary governance scoping, implementation status note, multi-org coverage. Added metadata block per ADR template modernization. |
