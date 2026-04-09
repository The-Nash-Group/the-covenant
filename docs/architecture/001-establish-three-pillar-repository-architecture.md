# ADR-001: Establish Three-Pillar Repository Architecture

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2025-10-30 |
| **Last Updated** | 2026-03-02 |
| **Author** | The Watchers, The Mentors |
| **Governance Level** | Covenant (2 Watchers + 2 Mentors, 72h debate) |
| **Status** | Accepted |
| **Related ADRs** | ADR-003, ADR-004 |

## Context

The Nash Group initially evolved with multiple repositories whose purposes became unclear over time:

- `the-covenant` - Philosophy and governance (clear purpose)
- `the-citadel` - Contained 41 policy specification markdown files (misleading — name suggested infrastructure)
- `citadel-config` - Terraform infrastructure as code (confusing name alongside "the-citadel")
- `nexus` - Operational tooling monorepo (clear purpose, missing "the-" prefix)

### Problems Identified

1. **Naming Confusion**: "the-citadel" and "citadel-config" sound similar but serve different purposes
2. **Misleading Names**: "the-citadel" suggests infrastructure but contains policy documentation
3. **Duplicated Purpose**: Policy specifications split between the-covenant and the-citadel
4. **Violation of Principles**: Violates "There Can Be Only One" — policy specs exist in two places
5. **ORGANIZATION-SPEC Violations**: the-citadel missing required files (README.md, proper CLAUDE.md)

## Decision

Establish a **Three-Pillar Repository Architecture** with semantic naming, extended by purpose-specific repositories as the organization matures.

### Core Three Pillars

```
┌────────────────────┐
│  THE COVENANT      │ ← Why We Build
│  (Philosophy)      │   • PRINCIPLES.md (16 core principles)
└────────────────────┘   • GOVERNANCE.md (who decides what)
         ↓                • HUMAN_MANDATE.md (5 Guardian roles)
         ↓                • policies/ (policy specifications)
┌────────────────────┐
│  THE CITADEL       │ ← How We Build
│  (Infrastructure)  │   • Terraform IaC (GitHub, Cloudflare, Hetzner)
└────────────────────┘   • Multi-org management via Terraform
         ↓                • OPA policy enforcement
         ↓                • State in Hetzner Object Storage via OpenTofu
┌────────────────────┐
│  THE NEXUS         │ ← What We Build
│  (Operations)      │   • Observability Bridge
└────────────────────┘   • MCP servers
                         • Dashboard and tooling
```

### Extended Pillars

As the architecture matured, two additional repositories emerged to serve specialized functions. These extend the three-pillar model — they do not replace it.

```
┌────────────────────┐
│  THE SHIELD        │ ← How We Secure
│  (Identity / IAM)  │   • Authentik on Hetzner (identity provider)
└────────────────────┘   • IAM framework (Rust/WASM/Rego)
                         • "Poor Man's Enterprise" auth chain
                         • Google Workspace → Authentik → GitHub OAuth

┌────────────────────┐
│  THE TARTAN        │ ← How We Present
│  (Public Identity) │   • Astro site + Rust/WASM components
└────────────────────┘   • Cloudflare Pages deployment
                         • Public-facing brand identity
```

### Repository Purposes (Official)

| Repository | Purpose | Contains | Governance |
|------------|---------|----------|------------|
| **the-covenant** | Philosophy & policy specifications | PRINCIPLES.md, GOVERNANCE.md, policies/ | Covenant (2 Watchers + 2 Mentors, 72h debate) |
| **the-citadel** | Infrastructure as Code | Terraform, GitHub/Cloudflare/Hetzner config | Citadel (1 Mentor + 1 Watcher) |
| **the-nexus** | Operational tooling | Apps, services, MCP servers | Stronghold (1 Mentor) |
| **the-shield** | Identity & Access Management | Authentik config, IAM framework (Rust/WASM/Rego) | Citadel (1 Mentor + 1 Watcher) |
| **the-tartan** | Public website & identity | Astro site, Rust/WASM, Cloudflare Pages | Stronghold (1 Mentor) |

### Multi-Organization Context

The Nash Group is a holding company with subsidiaries that are separate legal and operational entities. The three-pillar architecture serves as the governance backbone for all of them.

**GitHub Organizations** (all on Free tier):

| Organization | Entity | Purpose |
|-------------|--------|---------|
| `the-nash-group` | Parent holding company | Governance, infrastructure, shared tooling |
| `happy-patterns` | Happy Patterns LLC | Production products |
| `jefahnierocks` | Personal/creative | Personal projects |
| `litecky-editing` | Professional editing | Spouse's editing business |
| `seven-springs` | Sandbox | Synthetic sandbox/examples |

**Key architectural points**:

- No GitHub Enterprise — all orgs on Free tier (see ADR-004 for the "Poor Man's Enterprise" pattern)
- Governance inheritance: all subsidiaries inherit the 16 Covenant principles; they can add constraints but never subtract
- the-citadel manages ALL subsidiary GitHub orgs via multi-provider Terraform
- Identity federation via Authentik (the-shield) rather than GitHub Enterprise SAML

### Implementation Plan

1. **Move policy specifications**: the-citadel/policies/*.md → the-covenant/policies/
2. **Archive old the-citadel**: Preserve history, mark as superseded
3. **Rename citadel-config**: citadel-config → the-citadel
4. **Update ORGANIZATION-SPEC.md**: Codify three-pillar architecture

## Implementation Status

All four original phases are complete:

- **Phase 1: Policy Migration** — COMPLETED 2025-10-30. 41 policy specification files moved to the-covenant/policies/.
- **Phase 2: Archive old the-citadel** — COMPLETED 2025-10-30. ARCHIVE-NOTICE.md added, repository preserved for history.
- **Phase 3: Rename citadel-config → the-citadel** — COMPLETED 2025-11-01. GitHub rename executed, local directories updated.
- **Phase 4: Update ORGANIZATION-SPEC.md** — COMPLETED 2025-11-01. Three-pillar architecture codified in organizational standards.

Post-implementation, the Organizational Consistency Audit (2026-03-01) validated all repositories against the three-pillar architecture and extended it with the-shield and the-tartan.

## Consequences

### Positive

1. **Semantic Clarity**: Repository names directly indicate their purpose
2. **Single Source of Truth**: Policy specifications consolidated in one location (the-covenant/policies/)
3. **Eliminates Confusion**: No more "citadel" vs "citadel-config" ambiguity
4. **Aligns with Principles**: Principle 1 ("There Can Be Only One") and Principle 16 ("Living Law")
5. **Scales to Multi-Org**: Three-pillar governance backbone supports subsidiary orgs without duplication
6. **Clean Extension Model**: the-shield and the-tartan extend rather than fragment the architecture

### Negative

1. **Git History Split**: Policy file history split between repositories (old the-citadel archived for reference)
2. **Multi-Org Complexity**: the-citadel now manages 5 GitHub orgs via multi-provider Terraform
3. **No Cross-Org Branch Protection**: GitHub Free tier cannot enforce org-wide rulesets (see ADR-004)

### Neutral

1. **Five Repos, Three Pillars**: the-shield and the-tartan are extensions, not new pillars — the mental model stays simple
2. **Documentation Refresh**: Each architectural evolution requires updating ADRs (hence this living document approach)

## Validation

- [x] All 41 policy files exist in the-covenant/policies/
- [x] Old the-citadel archived with ARCHIVE-NOTICE.md
- [x] Workspace and parent docs distinguish local `the-citadel/` path from the current GitHub repo slug `citadel-config`
- [x] No broken references in any repository
- [x] Compliance audit shows all core repos compliant
- [x] ORGANIZATION-SPEC.md documents three-pillar architecture
- [x] the-shield and the-tartan documented in repo purposes table
- [x] Multi-org context documented with subsidiary mapping

## References

- **Nash Group Principles**: the-covenant/PRINCIPLES.md
- **Governance Requirements**: the-covenant/GOVERNANCE.md
- **Organizational Standards**: .org/ORGANIZATION-SPEC.md
- **Multi-Org Decision**: ADR-004 (Federated Multi-Org Architecture)
- **Cloudflare Baseline**: ADR-003 (Cloudflare Governance Baseline)

---

> **Living Documents**: ADRs may be updated when facts change, but changes require Guardian approval. Edit in place and add a changelog entry rather than creating a superseding ADR.

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2025-10-30 | The Watchers, The Mentors | Initial creation — three-pillar architecture established |
| 2026-03-02 | Agent | Updated to reflect five-repo architecture (added the-shield, the-tartan), multi-org context, subsidiary governance model. Trimmed completed implementation scripts. Added metadata block per ADR template modernization. |
| 2026-04-05 | Agent | Corrected local path vs GitHub slug language for the infrastructure repo and aligned the architecture record with the current parent standards. |
