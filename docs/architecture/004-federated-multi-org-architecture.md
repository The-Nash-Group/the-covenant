# ADR-004: Federated Multi-Org Architecture

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2026-03-02 |
| **Last Updated** | 2026-04-26 |
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

GitHub Enterprise Cloud with SAML SSO costs $21/user/org/month. For 5 organizations, even with a single user, this represents a significant recurring cost for a small holding company. More critically:

- Enterprise SAML requires each org to be on Enterprise plan separately
- The Nash Group is a "Single-Player Empire" — one human Guardian with AI agents
- The cost-to-value ratio is poor for a solo operator managing subsidiary orgs

We need identity federation *without* Enterprise pricing.

### Alternatives Considered

**Alternative 1: Stay Single-Org** — Rejected. Conflates governance with product, makes subsidiary autonomy impossible, and violates the principle that legal entities should have clear technical boundaries.

**Alternative 2: GitHub Enterprise Cloud** — Rejected. Cost-prohibitive at $21/user/org/month per org. Designed for large teams, not single-operator holding companies.

**Alternative 3: Multi-Org Without Federation** — Rejected. Separate orgs with no identity link means managing credentials per-org manually — the worst of both worlds.

## Decision

We adopt a **federated multi-org architecture** using Authentik as a self-hosted identity provider to bridge the gap between GitHub Free tier and Enterprise-grade identity management.

### 1. Multi-Org GitHub Structure

Each legal/operational entity gets its own GitHub organization, all on Free tier:

| Organization | Entity | Legal Structure | Primary Domain |
|-------------|--------|----------------|----------------|
| `the-nash-group` | Parent holding company | Sole proprietorship | thenash.group |
| `happy-patterns-org` | Happy Patterns LLC | LLC | happy-patterns.com (also owns happy-patterns.co) |
| `jefahnierocks` | Personal/creative | Personal | jefahnierocks.com |
| `litecky-editing` | Professional editing | Sole proprietorship | litecky-editing (TBD) |
| `seven-springs` | Sandbox/examples | None (synthetic) | None |

### 2. Authentik IS the-shield

Authentik, self-hosted on Hetzner, serves as the Nash Group's identity provider. It is the instantiation of the-shield repository's IAM architecture.

**The "Poor Man's Enterprise" auth chain**:

```
Google Workspace (SSoT for identity)
        ↓ OIDC/SAML
    Authentik (the-shield, Hetzner)
        ↓ OAuth Apps (one per GitHub org)
    GitHub Org 1 ─── GitHub Org 2 ─── GitHub Org 3 ...
```

- **Google Workspace** is the single source of truth for human identity
- **Authentik** federates that identity to all downstream services via OAuth/OIDC
- Each **GitHub org** has its own Authentik OAuth app, providing SSO-like experience without SAML
- This is OAuth-based, not SAML — GitHub Free tier supports OAuth apps but not SAML enforcement

**Tradeoff**: Users are not *forced* to authenticate via Authentik (no SAML enforcement). The Guardian must maintain discipline. For a single-operator setup, this is acceptable.

### 3. Infisical for Secrets Management

Infisical, self-hosted at infisical.jefahnierocks.com, replaces ad-hoc secrets management:

- **Primary secrets store**: All API tokens, service credentials, and configuration secrets
- **Local vs runtime boundary**: Managed workstations use env vars and/or `op read` for local bootstrap. Runtime and CI continue to use each repo's approved managed backend. Any remaining legacy archive material is non-default.
- **Eliminates**: Static tokens in `.envrc` files, manually-rotated API keys, secrets scattered across services
- **Per-org scoping**: Infisical projects map to GitHub orgs, enabling least-privilege secret access
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
| `jefahnierocks.com` | Personal | Personal/creative projects | Hosts Infisical, Authentik |
| Future subsidiary domains | Per entity | As needed | Follow Cloudflare governance (ADR-003) |

## Consequences

### Positive

1. **Clean entity separation**: Each legal entity has its own GitHub org, billing, and membership
2. **Governance scales**: Parent governance inherited automatically; subsidiaries add, never subtract
3. **No Enterprise tax**: All orgs on Free tier; Authentik provides federation for free (self-hosted)
4. **Identity federation**: Single login experience across all orgs via Authentik OAuth
5. **Secrets centralized**: Infisical eliminates secrets sprawl across `.envrc` files and manual rotation
6. **IaC coverage**: the-citadel manages all orgs via multi-provider OpenTofu/IaC — no ClickOps anywhere

### Negative

1. **No cross-org branch protection**: GitHub Free tier cannot enforce rulesets across orgs; each org configures independently via OpenTofu/IaC
2. **Authentik maintenance**: Self-hosted identity provider requires uptime monitoring, updates, and backup
3. **No SAML-enforced login**: OAuth apps are voluntary — a user *could* bypass Authentik and log in directly to GitHub (mitigated by single-operator discipline)
4. **Multi-provider OpenTofu/IaC complexity**: the-citadel requires one GitHub provider block per org, increasing configuration surface

### Neutral

1. **Per-org billing**: Each org manages its own billing relationship (appropriate for separate legal entities)
2. **OpenTofu multi-provider**: Adds ~20 lines of provider config per org, manageable for 5 orgs
3. **Authentik learning curve**: One-time setup cost; Authentik has good documentation and active community

## Compliance

- **Principle #1** (Sacred Timeline / SSoT): Google Workspace is the single source of truth for identity
- **Principle #5** (Infrastructure as Code): All org configurations managed via OpenTofu/IaC in the-citadel
- **Principle #9** (Zero Trust): Authentik enforces identity-based access; no shared credentials
- **Principle #10** (Least Privilege): Per-org OAuth scoping limits blast radius; Infisical projects scope secrets per-org
- **Principle #16** (Living Law): This architecture evolved from experience — single-org was tried, found wanting, and replaced

## References

- [ADR-001: Three-Pillar Repository Architecture](./001-establish-three-pillar-repository-architecture.md)
- [ADR-002: Governed Agentic Development](./002-governed-agentic-development.md)
- [ADR-003: Cloudflare Governance Baseline](./003-establish-cloudflare-governance-baseline.md)
- [ADR-007: Subsidiary Authority and Identity Isolation](./007-subsidiary-authority-and-identity-isolation.md) — refines §4 (restatement model)
- [PRINCIPLES.md](../../PRINCIPLES.md) — 16 core principles
- [GOVERNANCE.md](../../GOVERNANCE.md) — Decision authority matrix

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
