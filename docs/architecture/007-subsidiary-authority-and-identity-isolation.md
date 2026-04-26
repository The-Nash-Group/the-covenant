# ADR-007: Subsidiary Authority and Identity Isolation

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2026-04-20 |
| **Last Updated** | 2026-04-20 |
| **Author** | Agent |
| **Governance Level** | Covenant (2 Watchers + 2 Mentors, 72h debate) |
| **Status** | Accepted |
| **Related ADRs** | ADR-001, ADR-002, ADR-004 (amended in place) |
| **Supersedes** | Inheritance-by-pointer language in ADR-004 §4 |

> **Current-state note (2026-04-20):** Approval is proceeding under the documented Guardian-exception path tracked in STATUS.md (single-Guardian quorum while the synthetic council per FU-1 is not yet operational). This ADR restates the approval basis explicitly rather than silently relaxing the Covenant-level rule.

## Context

ADR-004 established a federated multi-org architecture with each legal entity as its own GitHub organization. At the time, subsidiaries existed primarily as on-disk directories with lightweight metadata; governance was described as inheritance — subsidiaries "inherit all 16 Covenant principles" and "can add constraints but never subtract."

That inheritance-by-pointer model predated real subsidiary operation. Three changes in 2026 Q2 exposed its limits:

1. **Happy Patterns LLC became an independent GitHub organization** (`happy-patterns-org`, two-seat teams plan with members `verlyn13` and `happy-patterns`). Its repositories are no longer team resources inside `the-nash-group`; they are assets of a separate legal entity with its own governance surface.
2. **Product development began inside a subsidiary.** A working product repository (scopecam, under Happy Patterns) now has its own CLAUDE.md, AGENTS.md, operational contract, and dev-agent workflow. These files — correctly — make zero reference to Nash Group, Covenant, Citadel, Nexus, or any parent archetype.
3. **The subsidiary shell leaks parent identity.** The directory layer between the product and the parent (for example, `~/Organizations/happy-patterns/CLAUDE.md`) is currently written in Nash-facing voice ("this subsidiary inherits…", "subsidiary of The Nash Group") and pulls Nash governance terminology into any session started at the subsidiary root. The parent router at `~/Organizations/CLAUDE.md` compounds this by listing subsidiaries as rows in the Nash matrix.

The inheritance model is also factually imprecise. Happy Patterns LLC is a distinct legal entity. It does not "inherit" Nash Group rules the way a child inherits from a parent class; it adopts equivalent rules on its own authority because it chooses to, because the rules are sound, and because the parent relationship requires it as a condition of structural coherence. The two framings are operationally similar and legally very different.

### Why this matters for agents

An AI agent working on a Happy Patterns product reads the nearest CLAUDE.md chain by default. Under the current structure, that chain is contaminated:

```
Current (leaky)                               Target (isolated)
───────────────                               ─────────────────
~/Organizations/CLAUDE.md (Nash router)       Subsidiary router, neutral voice
 ↓ read during dir traversal                   ↓
~/Organizations/happy-patterns/CLAUDE.md      Happy Patterns' own authority doc
 (Nash-facing, "subsidiary of…")              (Happy Patterns' own voice)
 ↓                                             ↓
apps/scopecam/CLAUDE.md (clean — OK)          apps/scopecam/CLAUDE.md (clean — OK)
```

The leakage is entirely at the middle tier. The fix is entirely at the middle tier.

### Alternatives Considered

**Alternative 1: Extend the current two-tier model with a subsidiary-isolation flag.** Rejected. Adds configuration without correcting the underlying authority framing. The problem is not that dev agents read parent files; it is that the parent framing presumes authority it should not exercise over subsidiary dev agents.

**Alternative 2: Prohibit subsidiary directories from holding CLAUDE.md files.** Rejected. Leaves dev agents with no context at the subsidiary-shell level and forces every project to re-derive subsidiary identity. Also conflicts with the fact that subsidiaries are genuine authorities with their own operational detail to communicate.

**Alternative 3: Treat Nash and subsidiaries as equal peers.** Rejected. Nash Group holds the parent relationship, publishes shared specs, and manages cross-entity concerns (billing labels, infrastructure defaults, dependency governance tiers). The relationship is asymmetric by design. The correction is to make the asymmetry live only at the spec-publishing layer, not in agent session context.

## Decision

We adopt a **three-tier authority model** with strict identity isolation at the subsidiary boundary.

### 1. Three Tiers

| Tier | Authority | Publishes | Agent context |
|------|-----------|-----------|---------------|
| **Parent** (The Nash Group) | Specs, standards, principles | Spec documents, standards, templates, directives | Used by parent orchestration agents only |
| **Subsidiary Authority** (e.g., Happy Patterns LLC) | Its own governance, voice, branding, CI, seats | Its own CLAUDE.md, README.md, operational docs, team structure | Used by subsidiary-scoped sessions and their dev agents |
| **Project / Dev Agent** (e.g., scopecam) | Its own code, tests, PR process | Code, project docs, AGENTS.md as needed | Sees only subsidiary identity |

### 2. Three Invariants

These are enforceable rules that subordinate specs and standards must implement:

1. **Identity isolation.** Nash Group identifiers — including the entity name, the three-pillar archetype names (Covenant, Citadel, Nexus, Shield, Tartan), Guardian archetype names, principle numbers, ADR references, and any prefix that binds a subsidiary to Nash's namespace — **must not** appear in any file that a subsidiary-scoped agent reads during normal operation. A dev agent working on a Happy Patterns product must not discover the Nash Group exists by reading its own project's context chain.

2. **Authority restatement, not inheritance.** Subsidiaries do not inherit parent principles by pointer. Each subsidiary restates the equivalent rules in its own voice, on its own authority, in its own documents. The content may be functionally identical; the author-of-record is the subsidiary. A subsidiary may add constraints beyond what the parent specifies, but must not describe its own rules as Nash-derived in dev-agent-facing artifacts.

3. **Spec flow, not session flow.** The Nash→subsidiary relationship is asynchronous spec delivery (pull model). Parent publishes; subsidiary adopts at its own cadence, in its own repositories, with its own review process. No runtime context sharing: a session started inside a subsidiary must not traverse upward into Nash-authored files. Parent-authored content reaches the subsidiary only through specs the subsidiary chose to adopt and restated in its own voice.

### 3. What Each Tier Owns

**Parent (The Nash Group) owns:**
- Specs under `the-covenant/policies/specs/`
- Principles, governance policies, and ADRs under `the-covenant/`
- Cross-cutting standards under `.org/standards/`
- Templates under `.org/templates/`
- Shared infrastructure and IaC under `the-citadel/`
- Parent orchestration under `.claude/orchestration/`
- The subsidiary registry under `.org/iam/federation/subsidiaries.yaml` (the parent's view of its subsidiaries)
- Cross-entity concerns: billing labels, dependency governance tiers, audit requirements, break-glass procedures

**Subsidiary Authority owns:**
- Its own CLAUDE.md, README.md, CONTRIBUTING.md at the subsidiary root
- Its own subsidiary metadata file (with sensitive fields extracted to secure storage — see §5)
- Its own operational standards, restated from parent specs where adopted
- Its own team structure, branch protection, CI/CD workflows within its GitHub org
- Its own brand and voice
- Its own relationship with its dev agents and contributors

**Project (e.g., scopecam) owns:**
- All code, tests, and project-scoped documentation
- Its own CLAUDE.md and optionally AGENTS.md
- Its build, test, and deployment commands
- Its contribution workflow

### 4. The Boundary

The boundary between parent and subsidiary is enforced by three mechanisms:

| Mechanism | Location | Purpose |
|-----------|----------|---------|
| **Policy** | `the-covenant/policies/org-001-subsidiary-authority.md` | The rule itself, implementing the three invariants |
| **Spec** | `the-covenant/policies/specs/subsidiary-authority.md` | Operational detail: ownership model, what must not cross, migration guidance |
| **Standard** | `.org/standards/subsidiary-governance.md` | Agent session scoping: what files a subsidiary-scoped agent may read, how to detect contamination |

A directive (`DIRECTIVE-2026-04-20-subsidiary-authority.md`) binds the parent orchestration agents operationally while the specs and standards land.

### 5. Sensitive Metadata Placement

Subsidiary legal and financial metadata — EIN, entity numbers, formation receipts, bank account details, physical addresses — **must not** be placed in files discoverable through an agent's default context chain. The spec requires:

- A public operational metadata file (for example, `.subsidiary.yaml`) containing only routing information: display name, parent relationship, governance level, owned domains, GitHub org reference, billing labels.
- A private tax and legal record stored in the subsidiary's approved secrets authority. On the managed Guardian workstation, local reads may use 1Password (`op read`); runtime and CI reads use the repo's approved managed backend (currently Infisical for remote, provider-agnostic per SEC-005 and the Secrets Management Specification).
- Sensitive fields **must not** appear in git-tracked metadata files.

### 6. Relationship to ADR-004

ADR-004 §4 ("Subsidiary Governance Model") described inheritance. That framing is amended in place (see ADR-004 Changelog 2026-04-20) to match the restatement model. ADR-004 remains the authority for the federated multi-org decision; ADR-007 refines the authority-layer semantics that ADR-004 introduced.

## Consequences

### Positive

1. **Dev agents are uncontaminated.** A session working on a Happy Patterns product sees Happy Patterns identity only. No Nash archetypes, no principle numbers, no ADR references leak into the session.
2. **Subsidiary authority becomes real.** Each subsidiary's governance surface is first-class rather than a pass-through of parent rules. Subsidiaries develop their own operational voice.
3. **LLC identity independence is enforceable.** The legal separation between Happy Patterns LLC and The Nash Group has a structural correlate in the technical and governance layers.
4. **The parent's role becomes cleaner.** The Nash Group governs by spec publication and exception; it does not operate as runtime authority over subsidiary dev work.
5. **The structure generalizes.** The same pattern applies to future subsidiaries without requiring parent-level intervention in their dev agent contexts.

### Negative

1. **More artifacts to keep synchronized.** Each subsidiary now maintains its own CLAUDE.md, README.md, and subsidiary metadata rather than inheriting by pointer. A parent spec change produces an asynchronous migration obligation for each subsidiary.
2. **Restatement can drift.** If a subsidiary restates a parent spec in its own voice and the parent spec later changes, the subsidiary's restatement may fall behind. The Subsidiary Authority Spec addresses this with a review cadence, but drift risk is real.
3. **Sensitive metadata extraction is work.** Existing subsidiaries have tax and legal metadata in git-tracked files. Moving those fields to secure storage is one-time migration work that must land before the isolation rule can be fully enforced.
4. **Scaffolding cost per subsidiary.** Adding a new subsidiary now requires a richer set of artifacts at inception, not just a `.subsidiary.yaml`.

### Neutral

1. **Authority restatement is functionally close to inheritance** for most operational purposes. The difference matters at the edges — legal framing, agent context scoping, subsidiary autonomy — which are exactly the edges this ADR is about.
2. **Parent agents can still audit subsidiary repositories.** Isolation is about what a subsidiary-scoped agent reads, not about whether a parent-scoped agent may read subsidiary files. Parent read access for audit is preserved; parent write access to subsidiary repos is not permitted except by explicit cross-entity approval.
3. **The router at `~/Organizations/CLAUDE.md`** is outside the Nash repo on disk but implements Nash routing logic. Its canonical version will be tracked as a template under `.org/templates/` and deployed as a config artifact. Versioning the router this way is a side effect of the boundary decision, not a core architectural choice.

## Compliance

- **Principle #5** (Infrastructure as Code): Subsidiary structure, registry, and the router template are all versioned artifacts, not runtime configuration.
- **Principle #9** (Zero Trust): Session context boundaries are verified by what an agent can read, not by what the agent is trusted to ignore.
- **Principle #10** (Least Privilege): A subsidiary-scoped agent reads only subsidiary-scoped files. Parent content is invisible to it by construction.
- **Principle #15** (Three Circles of Trust): The three tiers map naturally — parent specs are L0 (authority), subsidiary restatement is L1 (adoption), project/dev-agent work is L2 (execution).
- **Principle #16** (Living Law): The inheritance model came from an earlier architectural moment; this ADR refines it based on operational experience.

## Implementation Path

This ADR is realized in four phases, tracked in `.claude/orchestration/subsidiary-authority-migration/`:

1. **Doctrine** — This ADR, ORG-001 policy, Subsidiary Authority Spec, ADR-004 in-place update.
2. **Codification** — Subsidiary Governance Standard, updates to agentic-workflow.md, agent-roles.yaml (product-agent archetype), AGT-001 subsidiary-boundary clause, subsidiaries.yaml registry fix.
3. **Binding** — Parent operational directive, parent CLAUDE.md / STATUS.md / ROADMAP.md updates.
4. **Migration** — Campaign packet with migration guide (one worked example), router template, handoff to each subsidiary for its own rewrites.

Phases 1–3 are parent-repo work. Phase 4 is the parent's handoff to subsidiaries; execution within each subsidiary is out of scope for this ADR.

## References

- [ADR-001: Three-Pillar Repository Architecture](./001-establish-three-pillar-repository-architecture.md)
- [ADR-002: Governed Agentic Development](./002-governed-agentic-development.md)
- [ADR-004: Federated Multi-Org Architecture](./004-federated-multi-org-architecture.md) — amended in place 2026-04-20
- [PRINCIPLES.md](../../PRINCIPLES.md) — 16 core principles
- [GOVERNANCE.md](../../GOVERNANCE.md) — Decision authority matrix
- [ORG-001: Subsidiary Authority and Identity Isolation](../../policies/org-001-subsidiary-authority.md) *(to be created in Phase 1)*
- [Subsidiary Authority Specification](../../policies/specs/subsidiary-authority.md) *(to be created in Phase 1)*

---

> **Living Documents**: ADRs may be updated when facts change, but changes require Guardian approval. Edit in place and add a changelog entry rather than creating a superseding ADR.

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2026-04-20 | Agent | Initial creation — establishes three-tier authority model, three invariants (identity isolation, authority restatement, spec flow), sensitive metadata placement rule; supersedes inheritance-by-pointer language in ADR-004 §4 (amended in place same date) |
