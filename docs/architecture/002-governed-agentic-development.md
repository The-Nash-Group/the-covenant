# ADR-002: Adopt Governed Agentic Development (Constitutional API)

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2025-11-23 |
| **Last Updated** | 2026-05-13 |
| **Author** | Agent (The Architect) |
| **Governance Level** | Covenant (2 Watchers + 2 Mentors, 72h debate) |
| **Status** | Proposed |
| **Related ADRs** | ADR-001, ADR-004, ADR-005, ADR-007 |

> **Current-state note (2026-05-13):** This ADR remains **Proposed**. The
> Synthetic Council, SDR requirement, and Iron Gate workflow below are target
> governance mechanics, not current live merge gates. Current agent authority is
> manifest/provenance-bound and human-approved where implemented; no automated
> quorum restoration or SDR-required merge gate is live from this ADR alone.

## Context

The Nash Group is transitioning to a "Single-Player Empire" model where a lone human Guardian delegates execution to autonomous AI agents. However, the current "Human-in-the-Loop" model is unscalable and prone to "rubber-stamping" complex changes. Furthermore, AI agents are probabilistic and prone to hallucination, sycophancy, and drift. We lack a deterministic mechanism to ensure agent actions are aligned with our Covenant (Constitution) before they reach production.

Research (see `synthetic-governance-research.md`) indicates that:
1. Single-agent reviews suffer from sycophancy and mode collapse.
2. Traditional API keys for agents are a security liability (secrets management).
3. "Consensus" should be the result of adversarial dialectic, not simple voting.

## Decision

We will adopt the **Constitutional API** model for all agentic development,
targeting a "Synthetic Council" as the mandatory "Iron Gate" for infrastructure
and policy changes once FU-1 and SDR verification are implemented.

### 1. The Synthetic Council

We will deploy a multi-agent adversarial consensus engine to validate all Architecture Decision Records (ADRs) and Infrastructure-as-Code (IaC) changes.

* **The Steward (Risk Engine)**: Powered by a high-reasoning model, tasked with finding security and policy violations.
* **The Catalyst (Growth Engine)**: Powered by a high-velocity model, tasked with proposing implementation paths.
* **The Judge (Adjudicator)**: A neutral arbiter that renders a verdict based purely on The Covenant.

**Implementation Status**: The Synthetic Council package (`packages/synthetic-council`) was prototyped but never committed. It must be rebuilt from `governance-config.yaml` and `iron-gate.yml`. See follow-up item FU-1.

### 2. The Iron Gate (Identity-Based Signing)

We will replace static API keys with **identity-based authentication** using the Nash Group's Shield identity-contract lane:

* **Identity authority today**: Google Workspace for humans; SEC-005 machine identity for GitHub App, OIDC, and scoped provider-token automation.
* **Shield contract lane**: agent identity is manifest/provenance-bound first. Runtime-issued credentials require a real client, explicit contract, and Guardian-approved registration.
* **Secrets Management**: Runtime and automation use the repo's approved managed backend. On the managed workstation, local developer and agent reads use env vars and/or `op read`. Any remaining legacy archive material is migration-only residue, not current behavior.
* **Signing target**: Decisions would be cryptographically signed using ephemeral keys (Fulcio/Sigstore) once the SDR lane is implemented.
* **Transparency target**: Signatures would be logged to a transparency log (Rekor) once the SDR lane is implemented.

This targets elimination of static API keys and long-lived credentials — the
original goal of the Iron Gate design — but does not prove that every current
automation path has already migrated.

### 3. The Signed Decision Record (SDR)

We will standardize on the SDR format (combining ADRs with Sigstore bundles) as
the target atomic unit of governance. Once implemented and approved, protected
repositories can require a valid, verified SDR before merge; this ADR does not
claim that gate is live today.

### 4. Subsidiary Governance Scoping

The target Synthetic Council applies to **Covenant and Citadel-level changes**
across all Nash Group repositories. However:

* **Stronghold-level changes** in subsidiary orgs (`happy-patterns-org`, `jefahnierocks`, `litecky-editing`, `seven-springs`) may bypass the Council per governance level.
* Subsidiaries restate adopted parent specs on their own authority and can add their own constraints.
* the-citadel manages active subsidiary GitHub and Cloudflare controls through OpenTofu/IaC per readiness and placement rules — infrastructure changes always require Citadel governance regardless of which org they affect.

### 5. The Workflow

This is the target workflow, not the current live merge gate:

1. Agent creates a `proposal/*` branch.
2. Agent drafts an ADR.
3. Synthetic Council debates the ADR against `the-covenant/policies`.
4. If approved, the Council signs the decision (SDR).
5. The Iron Gate policy controller verifies the signature.
6. PR is unlocked for human ratification (optional for low-risk, mandatory for high-risk).

## Consequences

### Positive

* **Deterministic Alignment**: Governance can become code where the council and SDR lanes are implemented.
* **Security**: Targeted reduction of long-lived agent credentials through Shield contracts, SEC-005 machine identity, and the repo's approved managed backend.
* **Scalability**: The Guardian is relieved of low-level code review, focusing on intent.
* **Auditability**: Decisions gain a cryptographic reasoning trace once the SDR lane is wired.
* **Multi-Org Coverage**: Target-state auth chain can span all GitHub orgs once identity federation is implemented and evidenced.

### Negative

* **Latency**: The debate process adds time (minutes) to the feedback loop.
* **Cost**: Increased token usage for multi-turn debates.
* **Complexity**: Requires maintenance of identity contracts, secret-authority metadata, and Sigstore/OIDC infrastructure; Authentik remains lab-only unless a future trigger justifies production adoption.
* **Rebuild Required**: Synthetic Council package must be rebuilt from scratch (FU-1).

## Compliance

* **GOV-001**: Supports "Living Principles" by formalizing the amendment process.
* **SEC-001**: Targets "Zero Trust" by requiring cryptographic proof for governed actions once SDR verification is wired.
* **INF-001**: Targets "Infrastructure as Code" by treating governance decisions as code artifacts once the workflow is implemented.
* **Principle #9**: Zero Trust — identity-based access requires explicit authentication, authorization, provenance, and evidence; Authentik is not production enforcement today.
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
| 2026-04-26 | Codex | Aligned subsidiary scoping with ADR-005 and ADR-007: restatement replaces inheritance language, `happy-patterns-org` is the active Happy Patterns org, and OpenTofu/IaC replaces current Terraform wording. |
| 2026-05-12 | Codex | Reframed identity-based signing around Shield contracts, Google Workspace current human authority, SEC-005 machine identity, and manifest/provenance-bound agent identity; Authentik remains lab-only unless future triggers justify production adoption. |
| 2026-05-13 | Codex | Added policy-status qualifiers so the proposed Synthetic Council, SDR, Sigstore/Rekor, and merge-gate language reads as target governance mechanics rather than current live enforcement. |
