# ORG-001: Subsidiary Authority and Identity Isolation

**Policy ID:** ORG-001
**Category:** Organizational Structure
**Effective Date:** 2026-04-20
**Last Updated:** 2026-04-20

## Statement

Subsidiaries of The Nash Group operate as their own authority over their own dev agents, repositories, and operational artifacts. Each subsidiary **must** restate functionally equivalent rules from Nash-published specs in its own voice, on its own authority — not by inheritance, pointer, or reference. Nash Group identifiers **must not** appear in any file that a subsidiary-scoped agent reads during normal operation. Session context **must not** flow from parent to subsidiary at runtime: a session started inside a subsidiary traverses only subsidiary-authored files.

## Rationale

The Nash Group→subsidiary relationship is asymmetric by design, but the asymmetry belongs at the spec-publishing layer, not at the dev-agent-session layer. When parent identity leaks into a subsidiary's agent context, three things break:

- **Legal identity separation erodes** — A subsidiary like Happy Patterns LLC is a distinct legal entity. Files that describe it as "a subsidiary of The Nash Group" conflate two entities that have separate tax treatment, separate liability, and separate contractual relationships with the outside world.
- **Dev agents are contaminated** — An agent working on a subsidiary product reads its nearest CLAUDE.md chain by default. If that chain exposes parent archetypes (Covenant, Citadel, Nexus, Guardians), principle numbers, and parent branding, the agent's understanding of authority is incorrect: it treats the parent as a runtime authority when the parent is only a spec publisher.
- **Restatement discipline is lost** — Inheritance-by-pointer is weaker than restatement. Restatement forces each subsidiary to understand and re-author the rule, which exposes drift, missing context, and subsidiary-specific constraints early. Pointer-inheritance defers all of that indefinitely.

Authority restatement is not merely a style preference. It is the correct semantic model for relationships between legally distinct entities that share operational standards.

## Scope

**Applies To:**
- All subsidiary directories under `~/Organizations/` (currently `happy-patterns/`, `jefahnierocks/`, `litecky-editing/`, `seven-springs/`)
- All GitHub organizations corresponding to subsidiary entities (currently `happy-patterns-org`, `jefahnierocks`, `litecky-editing`, `seven-springs`)
- Every file that a subsidiary-scoped agent reads during normal operation — CLAUDE.md, README.md, AGENTS.md, subsidiary metadata files, local environment files, project-level operational docs
- The parent router at `~/Organizations/CLAUDE.md`, which is canonically maintained as a Nash-authored template and deployed to that path

**Exceptions:**
- Parent agents operating from `~/Organizations/the-nash-group/` may read subsidiary repositories for audit and orchestration purposes. Parent write access to subsidiary repositories is not permitted except by explicit cross-entity approval.
- Cross-entity coordination explicitly approved by the Guardian — billing reconciliation, legal compliance audits, security incident response — may reference parent and subsidiary in the same artifact. Such artifacts must live at the parent or under `.claude/orchestration/`, never inside a subsidiary repo.
- The subsidiary registry at `.org/iam/federation/subsidiaries.yaml` holds the parent's view of its subsidiaries. It is Nash-scoped by design and is not read by subsidiary-scoped agents.

**Governed Elsewhere:**
- Session-scoping mechanics and file-traversal rules: `.org/standards/subsidiary-governance.md`
- Agent role contracts and archetypes: `governance/agent-roles.yaml` and AGT-001
- Detailed ownership model, migration guidance, and current-state notes: Subsidiary Authority Specification

## The Three Invariants

### Invariant 1: Identity Isolation

The following identifiers **must not** appear in any subsidiary-scoped artifact:

- The parent entity name, its abbreviations, and its branding
- The three-pillar archetype names (Covenant, Citadel, Nexus, Shield, Tartan) and their derivatives
- Guardian archetype names (Philosopher, Architect, Judge, Gardener, Explorer) when used as governance roles
- The phrase "The Immortals", "The Mentors", "The Watchers" when used as governance tiers
- Covenant principle numbers or direct references to `the-covenant/PRINCIPLES.md`
- ADR numbers or direct paths into `the-covenant/docs/architecture/`
- Any two-letter subsidiary prefix assigned by the parent registry (subsidiaries use their full name instead)
- Nash-specific policy IDs (SEC-xxx, GOV-xxx, etc.) when used as governing rules; subsidiaries cite their own restated policies

A subsidiary may reference the parent entity in *legal* documents (operating agreements, tax filings, contracts) and in artifacts that explicitly live outside the subsidiary's agent-session scope (for example, a README in a `business/` directory for human accounting use). Identity isolation applies to dev-agent-facing artifacts.

### Invariant 2: Authority Restatement

When a Nash-published spec applies to a subsidiary, the subsidiary adopts it by **restating** the rule in its own voice:

- Subsidiary restates the rule as its own policy, in its own document, with its own policy ID (if it uses IDs) or its own natural-language reference.
- The content may be functionally identical to the parent spec. It must not be linguistically identical in ways that expose the Nash origin (for example, copying a Nash table verbatim with Nash footnotes intact).
- The subsidiary may add constraints beyond the parent spec. It may not describe its own rules as Nash-inherited in dev-agent-facing artifacts.
- Parent-published changes to a spec trigger an asynchronous restatement obligation on each subsidiary. The Subsidiary Authority Specification defines the review cadence.

### Invariant 3: Spec Flow, Not Session Flow

The parent→subsidiary relationship is asynchronous spec delivery (pull model):

- Parent publishes specs, standards, and directives in Nash-scoped locations.
- Subsidiaries read parent specs at integration time (when adopting or updating their own governance), not at dev-agent session time.
- A session started inside a subsidiary must not traverse upward into Nash-authored files. The router at `~/Organizations/CLAUDE.md` is the enforcement point: it explicitly instructs subsidiary-scoped sessions to read the subsidiary's own CLAUDE.md and to stop traversing upward.

## Forbidden-Identifier Contamination Check

A subsidiary repository is considered contaminated if a `grep -r` over its dev-agent-facing artifacts finds any identifier in Invariant 1's forbidden list. Contamination detection is a manual process at present (quarterly audit). A Citadel-enforced automated check may be added in a future OPA policy cycle; such a check **must** respect the exception list above (explicitly-authorized cross-entity artifacts).

## Implementation

### Technical Enforcement

Subsidiary isolation is structural, not runtime-enforced. The enforcement surface is the set of files an agent reads, which is determined by where the agent's session starts:

| Session Start Location | Reads From | Must Not Read |
|------------------------|------------|----------------|
| `~/Organizations/the-nash-group/` (parent) | Nash-authored artifacts; may read subsidiary repos for audit | — |
| `~/Organizations/happy-patterns/` (subsidiary shell) | Subsidiary-authored CLAUDE.md, README.md, subsidiary metadata; project-level files | Nash-authored artifacts (including `~/Organizations/CLAUDE.md` default routing) |
| `~/Organizations/happy-patterns/apps/scopecam/` (project) | Project-level files only | Parent router, subsidiary shell files above project, Nash-authored artifacts |

The parent router at `~/Organizations/CLAUDE.md` is the single point where traversal behavior is instructed. Its canonical form is maintained as `.org/templates/organizations-router-claude-md.template` in the Nash repo and deployed to that path.

### Automated Validation

- **Contamination scan** (quarterly, manual for now): grep each subsidiary's dev-agent-facing artifacts for the forbidden identifier list. Any hit is a finding.
- **Restatement drift review** (semi-annually): compare each subsidiary's restated policies against the parent specs they adopt. Flag specs updated in Nash that have not been restated downstream within the review cadence defined in the Subsidiary Authority Specification.
- **Router integrity check** (on every Nash-side template change): diff the deployed `~/Organizations/CLAUDE.md` against the Nash-authored template. Any drift is a finding.

### Human Process

1. **New subsidiary onboarding**: Parent orchestration publishes a subsidiary-authority migration packet (under `.claude/orchestration/subsidiary-authority-migration/`). Subsidiary authors its own CLAUDE.md, README.md, subsidiary metadata using the packet's template skeleton. Parent reviews for isolation compliance only (not for voice or content).
2. **Spec publication**: When Nash publishes or updates a spec that applies to subsidiaries, the parent records the publication date and the expected restatement deadline per subsidiary in the orchestration log. Each subsidiary adopts on its own cadence within that deadline.
3. **Contamination finding**: A finding triggers a PR in the affected subsidiary's repo (not in Nash). Parent may author the PR for review by the subsidiary's owner but must not merge it on the subsidiary's behalf except under an explicit break-glass exception (GOV-003).

## Sensitive Metadata Placement

Subsidiary legal and financial metadata — EIN, entity numbers, formation receipts, bank account details, tax filing deadlines, physical addresses — **must not** be placed in files discoverable through an agent's default context chain. Subsidiaries must:

- Maintain a public operational metadata file (e.g., `.subsidiary.yaml` or equivalent) containing only routing-level fields: display name, parent relationship indicator, governance level (per the subsidiary's own restatement), owned domains, GitHub org reference, billing labels.
- Store legal and financial metadata in the subsidiary's approved secrets authority. On the managed Guardian workstation, local reads use 1Password (`op read`); runtime and CI reads use the repo's approved managed backend (currently Infisical for remote, provider-agnostic per SEC-005 and the Secrets Management Specification).

This rule is enforced by secrets policy, not by repo structure. A subsidiary's public metadata file is subject to isolation review (Invariant 1); a subsidiary's private legal record is governed by the Secrets Management Specification.

## Multi-Organization Strategy

Each subsidiary operates its own GitHub organization (established in ADR-004 and refined here per ADR-007):

- **`happy-patterns-org`** — Happy Patterns LLC; two-seat teams plan with members `verlyn13` and `happy-patterns`
- **`jefahnierocks`** — Personal creative work
- **`litecky-editing`** — Professional editing business
- **`seven-springs`** — Sandbox

Parent seats in subsidiary GitHub orgs are held only where required by shared infrastructure responsibilities (currently: the Citadel automation GitHub App). Human parent seats in subsidiary orgs are not retained by default.

## Compliance Verification

**Automated (future):**
- Contamination scan integrated into the-shield CI (pending; manual until then)
- Router integrity check on Nash-side template PRs

**Manual (current):**
- Quarterly contamination audit across all subsidiaries
- Semi-annual restatement drift review
- Per-PR review on any change to subsidiary-facing files in Nash-authored templates

**Reporting:**
- Audit findings recorded under `.claude/orchestration/subsidiary-authority-migration/` and referenced in STATUS.md
- Restatement status tracked per subsidiary in the subsidiary registry

## Known Exceptions

| Exception | Reason | Review Trigger |
|-----------|--------|----------------|
| Cross-entity audit artifacts | Parent audit of subsidiary compliance requires referencing both entities by name | Quarterly; move any such artifact out of subsidiary-scoped paths |
| Legal documents inside subsidiary directories | Operating agreements, formation receipts, and tax filings legally name both entities | Always; these artifacts must live in paths not traversed by dev-agent sessions |
| `subsidiaries.yaml` registry | Parent's view of its subsidiaries is Nash-scoped by design | N/A — registry is not read by subsidiary agents |
| Guardian-exception approvals | Current single-Guardian approval path (per STATUS.md governance exceptions) may reference both entities in decision records | Restore 2W+2M quorum when synthetic council (FU-1) is operational |

## Related Documents

- **Source Principles:**
  - [Principle 5: Infrastructure as Code](../PRINCIPLES.md) — Subsidiary structure, registry, and router template are versioned artifacts
  - [Principle 9: Zero Trust](../PRINCIPLES.md) — Session context boundaries verified by what an agent can read, not what it is trusted to ignore
  - [Principle 10: Least Privilege](../PRINCIPLES.md) — A subsidiary-scoped agent reads only subsidiary-scoped files
  - [Principle 15: Three Circles of Trust](../PRINCIPLES.md) — Parent specs (authority), subsidiary restatement (adoption), project/dev-agent work (execution)
- **Related Policies:**
  - [AGT-001: Agent Governance](./agt-001-agent-governance.md) — Agent boundary rules, including subsidiary boundary
  - [GOV-003: Break-Glass Procedures](./gov-003-break-glass.md) — Emergency override for cross-entity writes
  - [SEC-005: Machine Identity](./sec-005-machine-identity.md) — Machine identity boundary between parent and subsidiary automation
- **Specifications:**
  - [Subsidiary Authority Specification](./specs/subsidiary-authority.md) — Operational detail, ownership model, migration guidance
  - [Secrets Management Specification](./specs/secrets-management.md) — Storage rules for sensitive subsidiary metadata
- **Architecture:**
  - [ADR-004: Federated Multi-Org Architecture](../docs/architecture/004-federated-multi-org-architecture.md) — Established the multi-org structure; §4 refined by ADR-007
  - [ADR-007: Subsidiary Authority and Identity Isolation](../docs/architecture/007-subsidiary-authority-and-identity-isolation.md) — Decision record establishing this policy
- **Standards:**
  - [Subsidiary Governance Standard](../../.org/standards/subsidiary-governance.md) — Session-scoping mechanics
  - [Agentic Workflow Standard](../../.org/standards/agentic-workflow.md) — Agent orchestration patterns (three-tier model referenced there)
- **Implementation:**
  - `.org/iam/federation/subsidiaries.yaml` — Subsidiary registry (parent-scoped)
  - `.org/templates/organizations-router-claude-md.template` — Router canonical source
  - `.claude/orchestration/subsidiary-authority-migration/` — Migration campaign packet

## Change History

- **2026-04-20** — Initial creation establishing the three invariants (identity isolation, authority restatement, spec flow) per ADR-007; implements Principles 5, 9, 10, 15; pairs with the Subsidiary Authority Specification and the Subsidiary Governance Standard.
