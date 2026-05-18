# ADR-004: Federated Multi-Org Architecture

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2026-03-02 |
| **Last Updated** | 2026-05-13 |
| **Author** | Agent |
| **Governance Level** | Covenant (2 Watchers + 2 Mentors, 72h debate) |
| **Status** | Accepted |
| **Related ADRs** | ADR-001, ADR-002, ADR-003, ADR-007 (refines §4) |

## Context

The Nash Group started as a single GitHub organization (`the-nash-group`) housing all repositories. As subsidiaries matured into distinct legal and operational entities — Happy Patterns LLC, JefahnieRocks, Litecky Editing Services, Seven Springs — the single-org model created problems:

1. **Governance conflation**: Product repositories (Happy Patterns) mixed with governance infrastructure (the-covenant, the-citadel) under one org, making permissions coarse-grained.
2. **Identity confusion**: Contributors to a personal creative project (JefahnieRocks) appeared in the same org as production LLC work (Happy Patterns).
3. **Billing entanglement**: A single org billing relationship for entities with different legal and tax structures.
4. **No entity separation**: GitHub org membership implies trust across all repositories — inappropriate when entities have different risk profiles.

### Why Not GitHub Enterprise?

GitHub Enterprise Cloud is designed around centralized enterprise account management, advanced security controls, compliance features, and billing across multiple organizations. Those capabilities are directionally relevant, but current operating scale does not justify making Enterprise the default boundary for every subsidiary. More critically:

- GitHub Team already covers the active small-team collaboration need where it exists
- Enterprise account administration is heavier than the current single-Guardian, small-subsidiary operating model requires
- The Nash Group is a "Single-Player Empire" — one human Guardian with AI agents
- The cost-to-value ratio is poor for dormant, personal, or low-collaboration subsidiaries

We need identity federation and entity separation with staged platform spend.

### Alternatives Considered

**Alternative 1: Stay Single-Org** — Rejected. Conflates governance with product, makes subsidiary autonomy impossible, and violates the principle that legal entities should have clear technical boundaries.

**Alternative 2: GitHub Enterprise Cloud** — Deferred. Revisit when the number of paid seats, regulated collaboration requirements, audit requirements, or centralized multi-org administration needs justify the enterprise control plane.

**Alternative 3: Multi-Org Without Federation** — Rejected. Separate orgs with no identity link means managing credentials per-org manually — the worst of both worlds.

## Decision

We adopt a **federated multi-org architecture** with staged identity controls to bridge the gap between low-cost GitHub organization boundaries and enterprise-grade identity management. Authentik remains a possible future broker, but current production identity formation is Shield-contract-first and evidence-gated.

### 1. Multi-Org GitHub Structure

Each legal/operational entity gets its own semantic authority boundary. GitHub paid-plan adoption is staged according to actual collaboration, compliance, billing, and automation needs:

| Organization / Boundary | Entity | Legal Structure | Current Hosting Posture | Primary Domain |
|-------------|--------|----------------|-------------------------|----------------|
| `the-nash-group` | Parent holding company | Sole proprietorship | Parent GitHub org; shared controls only | thenash.group |
| `happy-patterns-org` | Happy Patterns LLC | LLC | GitHub Team, two members; owns `scopecam` | happy-patterns.com (also owns happy-patterns.co) |
| `jefahnierocks` | Personal/creative | Personal | Semantic owner for personal projects; paid org features deferred until justified | jefahnierocks.com |
| `litecky-editing` | Professional editing | Sole proprietorship | Subsidiary boundary; activation follows co-owner governance | liteckyediting.com |
| `seven-springs` | Sandbox/examples | None (synthetic) | Sandbox boundary with relaxed isolation | sevensprings.dev |

### 1.1 Semantic Ownership vs Operational Hosting

Semantic ownership and operational hosting are related but not identical.

- **Semantic owner** determines the legal/entity authority, governance tier, billing label, future OpenTofu workspace, secrets authority, agent context, and long-term repository home.
- **Operational host** is where the repository, GitHub features, or infrastructure currently run.
- A temporary mismatch is allowed only when the parent registry or orchestration record names the semantic owner, current host, intended long-term home, and trigger for migration.

This rule matters most for the current subsidiary mix:

- **Happy Patterns LLC** is active enough to justify paid GitHub Team collaboration. It owns `scopecam`, and active LLC product work should live under Happy Patterns authority.
- **Jefahnierocks** remains the semantic owner for personal projects even when it is not yet practical to pay for every GitHub org feature. Personal projects may remain in lower-cost or existing hosting while the parent records them as Jefahnierocks-owned and tracks move triggers.

Parent or global infrastructure roots must not become shortcuts for subsidiary ownership. If a project is semantically Jefahnierocks-owned or Happy Patterns-owned, its future IaC workspace, GitHub controls, secret boundaries, and audit evidence must converge on that subsidiary boundary when the trigger is met.

### 2. Shield Identity Foundation

Shield is the identity and authorization contract home. It defines identity
classes, registry shape, authorization-decision contracts, secret-authority
metadata contracts, and restatement packet shape before any identity runtime is
implemented.

Current state as of 2026-05-12:

- **Google Workspace** is the current human identity authority.
- **GitHub** is the current operating substrate, not the permanent identity
  control plane.
- **SEC-005 machine identity** governs GitHub App, OIDC, and scoped provider
  token use.
- **Authentik** is lab-only. It is not production identity, not repo-owned
  runtime, and not the default answer for human SSO at the current two-human
  operating scale.
- **GitHub Enterprise SAML** remains unavailable and must not be assumed.

Authentik may become a future broker only after evidence exists for host
placement, ownership, backup/restore, Docker/socket policy, Cloudflare/Tunnel or
Access design, break-glass recovery, secret custody, and an actual user,
contractor, or compliance trigger.

### 3. Infisical for Secrets Management

Infisical is a hosted secret-management service candidate and implementation
binding. It does not replace every repo's approved backend by Covenant claim
alone:

- **Target primary secrets store**: API tokens, service credentials, and
  configuration secrets migrate only after the owning repo or entity adopts the
  backend and records evidence
- **Local vs runtime boundary**: Managed workstations use env vars and/or `op read` for local bootstrap. Runtime and CI continue to use each repo's approved managed backend. Any remaining legacy archive material is non-default.
- **Target reduction**: Static tokens in `.envrc` files, manually rotated API
  keys, and secrets scattered across services are retired per owning-repo
  migration evidence
- **Per-org scoping target**: Infisical projects may map to GitHub orgs,
  enabling least-privilege secret access where adopted
- **IaC planning path**: OpenTofu may manage Infisical declaratively through the Infisical provider for projects, identities, approvals, dynamic secrets, rotations, syncs, certificate management, and secret objects; the detailed planning inventory lives in the Secrets Management Specification

### 4. Subsidiary Governance Model

> **Refined by ADR-007 (2026-04-20):** The original formulation below described governance as inheritance. ADR-007 refines this to a restatement model: subsidiaries do not inherit parent rules by pointer; they restate functionally equivalent rules on their own authority, in their own voice, in their own artifacts. A subsidiary may add constraints beyond what the parent specifies, but must not describe its own dev-agent-facing rules as Nash-derived. See ADR-007 for the three invariants (identity isolation, authority restatement, spec flow).

| Governance Aspect | Parent (the-nash-group) | Subsidiaries |
|-------------------|------------------------|--------------|
| **Principles** | Defines all 16 | Restates equivalent rules on own authority; may add more |
| **Default governance** | Covenant (highest) | Stronghold (lowest) |
| **Infrastructure changes** | Citadel level | Citadel level (the-citadel manages all orgs) |
| **Product changes** | N/A | Stronghold (1 Mentor) |
| **Security-critical changes** | Covenant level | Citadel level minimum |

### 5. Domain Architecture

| Domain | Owner | Purpose | Notes |
|--------|-------|---------|-------|
| `thenash.group` | Parent | Organizational identity | Cloudflare-managed |
| `happy-patterns.com` | Happy Patterns LLC | Primary product domain | Landing page pending; `happy-patterns.co` also owned as secondary |
| `jefahnierocks.com` | Personal | Personal/creative projects | Hosts Infisical service evidence; Authentik remains lab-only, not production identity |
| Future subsidiary domains | Per entity | As needed | Follow Cloudflare governance (ADR-003) |

## Consequences

### Positive

1. **Clean entity separation**: Each legal entity has a named authority boundary, with paid hosting adopted where it creates operational value
2. **Governance scales**: Parent publishes specs; subsidiaries restate equivalent rules on their own authority
3. **Staged platform spend**: Happy Patterns can use GitHub Team now while dormant or personal boundaries defer paid features until justified
4. **Identity federation path**: A single-login experience across orgs remains a target once an evidence-backed broker is justified
5. **Secrets centralization path**: Infisical or another approved backend can reduce secrets sprawl after repo/entity adoption evidence
6. **IaC coverage path**: the-citadel manages the OpenTofu/IaC control plane where resources are codified; live-provider claims still require current evidence

### Negative

1. **Uneven GitHub capabilities during bootstrap**: Subsidiaries on different plans have different collaboration, policy, and audit surfaces until paid features are justified
2. **Future broker maintenance**: Any self-hosted identity provider would require uptime monitoring, updates, backup, and break-glass recovery before production adoption
3. **No SAML-enforced login**: GitHub Enterprise SAML is unavailable under current plan posture; future OAuth broker designs would remain voluntary unless a stronger control plane is adopted
4. **Multi-provider OpenTofu/IaC complexity**: the-citadel requires one GitHub provider block per org, increasing configuration surface
5. **Temporary ownership/hosting split**: Some personal projects may be semantically owned by Jefahnierocks while operationally hosted elsewhere until a migration trigger is met

### Neutral

1. **Per-org billing**: Each org manages its own billing relationship (appropriate for separate legal entities)
2. **OpenTofu multi-provider**: Adds ~20 lines of provider config per org, manageable for 5 orgs
3. **Identity-broker learning curve**: One-time setup cost if a future broker such as Authentik becomes justified
4. **Plan upgrades are operational decisions**: Upgrading a subsidiary's GitHub plan is a governance and budget decision, not a change to semantic ownership

## Compliance

- **Principle #1** (Sacred Timeline / SSoT): Google Workspace is the single source of truth for identity
- **Principle #5** (Infrastructure as Code): Org configurations in Citadel scope are managed via OpenTofu/IaC in the-citadel
- **Principle #9** (Zero Trust): identity controls require explicit authentication, authorization, and audit evidence; Authentik is not production enforcement today
- **Principle #10** (Least Privilege): Per-org OAuth and per-backend scoping are target mechanisms for limiting blast radius where adopted and evidenced
- **Principle #16** (Living Law): This architecture evolved from experience — single-org was tried, found wanting, and replaced

## References

- [ADR-001: Three-Pillar Repository Architecture](./001-establish-three-pillar-repository-architecture.md)
- [ADR-002: Governed Agentic Development](./002-governed-agentic-development.md)
- [ADR-003: Cloudflare Governance Baseline](./003-establish-cloudflare-governance-baseline.md)
- [ADR-007: Subsidiary Authority and Identity Isolation](./007-subsidiary-authority-and-identity-isolation.md) — refines §4 (restatement model)
- [PRINCIPLES.md](../../PRINCIPLES.md) — 16 core principles
- [GOVERNANCE.md](../../GOVERNANCE.md) — Decision authority matrix
- [GitHub Docs: Getting started with GitHub Team](https://docs.github.com/en/get-started/onboarding/getting-started-with-github-team)
- [GitHub Docs: Upgrading your account's plan](https://docs.github.com/billing/managing-billing-for-your-github-account/upgrading-your-github-subscription)
- [GitHub Docs: Enterprise accounts](https://docs.github.com/github/setting-up-and-managing-your-enterprise/about-enterprise-accounts)

---

> **Living Documents**: ADRs may be updated when facts change, but changes require Guardian approval. Edit in place and add a changelog entry rather than creating a superseding ADR.

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2026-03-02 | Agent | Initial creation — documents multi-org GitHub, Authentik federation, Infisical secrets, subsidiary governance, domain architecture |
| 2026-04-05 | Agent | Added current-state note: ADR-005 migration converged for the parent org on 2026-04-04, Phase 4 now focuses on onboarding `jefahnierocks`, and OPA enforcement is partially delivered rather than merely planned. |
| 2026-04-15 | Agent | Clarified the Infisical planning path: OpenTofu may manage Infisical projects, identities, approvals, dynamic secrets, syncs, rotations, certificates, and secret objects as code; detailed capability inventory moved to the active Secrets Management Specification. |
| 2026-04-20 | Agent | Refined §4 Subsidiary Governance Model in place per ADR-007: replaced inheritance language ("inherits all 16") with restatement model ("restates equivalent rules on own authority"); updated §5 Domain Architecture entry for Happy Patterns LLC (primary domain is happy-patterns.com, happy-patterns.co also owned as secondary); corrected §1 GitHub Organization table to reference happy-patterns-org (the actual GitHub org slug, now on a two-seat teams plan); added ADR-007 to Related ADRs and References. Original decision preserved; refinement scope limited to authority-layer semantics and factual corrections. |
| 2026-04-26 | Agent | Aligned current-state IaC wording with ADR-005: replaced active Terraform implementation language with OpenTofu/IaC terminology without changing the multi-org architecture decision. |
| 2026-04-26 | Codex | Clarified staged GitHub plan adoption: Happy Patterns LLC is active on GitHub Team and owns `scopecam`; Jefahnierocks remains the semantic owner for personal projects while paid org hosting is deferred until justified. |
| 2026-05-12 | Codex | Clarified Shield identity foundation: Authentik is lab-only, Shield is the identity-contract home, Google Workspace remains current human authority, GitHub is current substrate, and SEC-005 governs machine identity. |
| 2026-05-13 | Codex | Qualified Infisical, Authentik, identity federation, secret centralization, and IaC coverage language so ADR-004 does not read as proof of current live enforcement beyond owning-repo evidence. |
