# ADR-008: Policy Authority Topology — Identity, Resource, Permission-Binding, Runtime Enforcement

## Status

**Proposed** (pending Covenant-tier ratification under the single-Guardian quorum exception per `STATUS.md §Governance Exceptions` and `ADR-007 §Current-state note`; full 2 Watchers + 2 Mentors quorum restored when the synthetic council per FU-1 is operational).

## Date

2026-05-17

## Context

Every permission system — across every provider, every layer, every era — composes the same shape: a policy binds an **actor** to a **scope** with a **permission**. The system stores those bindings; the runtime evaluates them. This shape is invariant across cloud providers, identity-and-access frameworks, file-system ACLs, network policies, and our own internal governance.

Our existing principles — Principles 5 (Infrastructure as Code), 9 (Zero Trust), 10 (Least Privilege), 11 (Observability), and 15 (Three Circles of Trust) — touch every part of this shape, but they do not articulate the **authority topology** that underlies it: which pillar of our architecture owns which dimension. As a result, three operational pressures have surfaced over the last quarter:

1. **Pillar scope-creep.** Projects intended for one authority domain have absorbed concerns belonging to another, because the boundary was implicit rather than explicit. The most visible example: an operator-personal project managing identity-scoped resources on a shared parent account, with no clear seam between the identity dimension (which is parent-scoped) and the resource dimension (which can be project-scoped within the parent account).
2. **Ambiguous Shield activation contour.** The Shield is planned for Q2 2026 but its scope statement defers to *"contracts, registry schema, and authority metadata; not the runtime owner by default."* That framing is correct as far as it goes, but it does not say which authority domain Shield owns and which it does not. Without an explicit topology, Shield's design phase risks under-scoping (omitting work that must land somewhere) or over-scoping (absorbing runtime ownership it should not).
3. **Inconsistent decomposition for new providers.** As we onboard new providers or revisit existing ones, the placement question recurs ("does this go in Citadel? Shield? a subsidiary? a personal project?"). Each time, the answer is re-derived. A canonical topology reduces this to lookup.

ADR-001 established the three-pillar architecture (Covenant / Citadel / Nexus, with Shield as the planned cross-cutting identity layer). ADR-007 established the three-tier authority model (parent_l0 / subsidiary_l1 / project_l2). Neither addresses **policy authority composition** — the question of which domain inside a policy belongs to which pillar.

The gap surfaced concretely while planning a round of cross-organization infrastructure work whose provider permission model expressed the three-part composition (`policy = actor + scope + permission`) as a first-class concept. That provider is one instance of a near-universal pattern: the same three-part decomposition appears in cloud IAM systems (principal + resource + action; member + resource + role), file-system ACLs, capability systems, and our own subsidiary-authority model (entity + sovereignty + authority-tier). The topology articulated by this ADR is therefore **provider-agnostic** — though specific providers, transitional specs, and parent-standard documents at lower layers translate this topology into provider-specific implementation guidance.

## Decision

This ADR establishes the **Policy Authority Topology**: a four-domain decomposition of every policy system, with each domain mapped to a single owning pillar (or runtime layer). The topology is constitutional — it constrains how new providers are integrated, how Shield's scope is articulated, how Citadel's IaC is bounded, and how subsidiaries restate parent specs.

### The Four Authority Domains

Every policy system — regardless of provider, era, or technology — admits this decomposition:

1. **Identity Domain.** Who acts. The registry of actors (humans, machines, services, agents, break-glass identities), their lifecycle, their authentication credentials' shape, their authority-tier metadata (parent_l0 / subsidiary_l1 / project_l2), and the audit contracts that govern their use.
2. **Resource Domain.** What is acted upon. The definitions of resources that exist in a given system, their scopes (account-level, zone-level, project-level, resource-level), and the IaC that provisions them.
3. **Permission-Binding Domain.** What is allowed. The permission/role taxonomy, the decision-input and decision-output contracts, and the policy artifacts that bind an actor to a scope with a permission. This is the layer where the three-part policy object is composed.
4. **Runtime Enforcement Domain.** What actually happens at request time. The evaluator that, on each access, fetches the relevant policy, examines actor + scope + permission against the request, and renders an allow/deny decision. This is fundamentally a runtime concern, distinct from the contract and registry layers above.

These four domains are **independent authority surfaces**. Each can evolve at its own cadence. Each has distinct evidence shapes, distinct review processes, and distinct failure modes. Conflating them — for example, treating runtime enforcement as part of identity registration — has produced concrete misalignments in our recent operational history.

### Pillar Mapping

| Domain | Owning authority | Notes |
|---|---|---|
| **Identity Domain** | **The Shield** (when active); the Citadel transitionally until Shield activates | Identity registry schema, identity classes, authority-tier metadata, audit contracts. Per Shield's stated framing, Shield "owns the decision contract, registry schema, and authority metadata; it does not become the runtime owner by default." This ADR ratifies that framing as the canonical Identity Domain ownership. |
| **Resource Domain** | **The Citadel** | Resource definitions, scope provisioning, IaC. The Citadel is the single source of truth for resources that exist in any provider; the resource ID becomes the scope identifier consumed by the Permission-Binding Domain. |
| **Permission-Binding Domain** | **The Shield** (contracts, role taxonomy, policy-binding schemas) consumed by **the Citadel** (which implements per Shield's contracts via IaC) | The contract layer is identity-side authority (Shield owns the "what permissions exist and what decisions consume them"). The implementation layer is resource-side authority (Citadel provisions tokens / policies / bindings via IaC). These two layers are tightly coupled but distinct: Shield publishes the contract; Citadel consumes it. |
| **Runtime Enforcement Domain** | **The runtime layer itself** — typically the provider's own evaluator; **the Nexus** when wired to enforce our own request-path admission | We do not own provider-runtime enforcement. We define contracts that the runtime consumes; we audit decisions; we do not replace the runtime evaluator. Nexus owns request-path admission for surfaces where we operate the runtime ourselves. |

### Composition Rule

For any policy in any system, the following must be true:

- The **actor** identifier and its authority-tier metadata are governed by the Identity Domain.
- The **scope** identifier is exported by the Resource Domain.
- The **permission** taxonomy and the **binding** that composes (actor + scope + permission) into a policy artifact are governed by the Permission-Binding Domain.
- The **enforcement** of that policy at request time is the responsibility of the Runtime Enforcement Domain.

The Permission-Binding Domain depends on outputs from both Identity (actors are referenced by identifier) and Resource (scopes are referenced by identifier). Identity and Resource Domains are mutually independent — neither depends on the other directly, except that the Identity Domain may reference Resource Domain outputs when expressing authority-tier metadata in resource terms (for example, "this identity is the parent_l0 owner of the resource at <scope-id>").

### Transitional Posture (Shield Activation Lag)

Shield is planned but not yet active. Until Shield activates, **the Citadel temporarily holds the Identity Domain and the Permission-Binding Domain contract layer in addition to the Resource Domain**. This is acceptable because:

- The Citadel is the only currently-active pillar capable of writing IaC, and identity + permission-binding artifacts are currently IaC-shaped (API tokens provisioned via OpenTofu; access policies provisioned via OpenTofu).
- The contract layer for identity and permission-binding can be authored anywhere during the transition; what matters is that on Shield activation, the contract authorship migrates to Shield without changing the resource implementations.
- Identifiers are preserved across the migration: the Eight Principles' Principle 7 (`provider_token_id` recorded as a durable identity) ensures that when a token's contract authorship moves from Citadel to Shield, the token's identifier — and thus its audit lineage — survives.

On Shield activation:

- Identity registry schemas, authentication contracts, authority-tier metadata, and audit contracts move under Shield authorship.
- Permission-binding contracts (role taxonomy, decision-input/output shapes, policy-object schemas) move under Shield authorship.
- The Citadel retains Resource Domain ownership and continues to implement Permission-Binding artifacts via IaC, now consuming Shield's contracts rather than authoring them.
- Runtime Enforcement remains where it was: provider-runtime for provider resources; Nexus for request-path admission on our own surfaces.

This is a one-way migration; once contract authorship lands in Shield, it does not return to Citadel except by amendment to this ADR.

### Constraint on Lower-Layer Documents

This ADR is principle-language. It does not name providers, technologies, or specific implementation patterns. The translation of this topology to specific providers belongs in lower layers:

- **Transitional specs** at `the-covenant/policies/specs/` (provider-bridging; may name providers; lives in Covenant for governance reach but is allowed to be provider-specific). Examples already in use: `cloudflare-ownership-transition.md`, `github-machine-identity.md`. New specs may be added or existing ones amended to reflect this topology.
- **Parent standards** at `.org/standards/` (provider-specific implementation patterns; how a given provider's permission model maps to the four domains; placement rules for resources, tokens, policies; how Shield contracts are consumed by Citadel IaC for a given provider).
- **Pillar contracts** at `the-citadel/CLAUDE.md`, `the-shield/CLAUDE.md`, `the-nexus/CLAUDE.md` (pillar-internal restatement of how each pillar implements its domain ownership; provider-specific where the pillar is the implementation layer).
- **Subsidiary restatement** per ORG-001 (subsidiaries restate this topology in their own voice when relevant to their scope).

### What This ADR Does Not Decide

- Specific provider implementations. Provider-specific decomposition and placement belongs in transitional specs at `policies/specs/` (provider-named files allowed at that layer) and parent standards at `.org/standards/`.
- Specific identifiers, paths, names, or formats. These are implementation details.
- Specific runtime-enforcement technology choices (OPA sidecar, library, Cedar service, WASM, hybrid). The Runtime Enforcement Domain is acknowledged as distinct; the technology selection remains an open ADR-gated question per Shield's framing.
- Activation timing for Shield. This is operational sequencing, not authority topology.
- Migration timing or sequence for any specific identity or resource. Each migration is its own work item under the topology's contract.

## Consequences

### What becomes easier

- **Placement decisions are deterministic.** For any new resource, identity, policy, or runtime concern, the topology yields the owning pillar without re-derivation. This applies to new providers we adopt as well as existing providers we revisit.
- **Shield's design phase has clear contour.** Shield owns the Identity Domain and the Permission-Binding Domain's contract layer. Shield does not own resource provisioning, IaC, or runtime enforcement. This bounds Shield's scope without under- or over-reaching.
- **Citadel's scope is preserved against creep.** Citadel owns the Resource Domain and implements Permission-Binding artifacts. The contract layer for identity and permission-binding is Shield-authored (or transitionally Citadel-held until Shield activates).
- **Subsidiary boundaries are clearer.** When a subsidiary project manages resources scoped to a parent provider account, the topology says: the project may own resource implementations within its scope, but the identity contracts, authority-tier metadata, and policy bindings remain at parent authority (Identity Domain ownership doesn't transfer downstream).
- **Audit accountability is clearer.** Each domain's evidence has a single owning authority. Cross-domain audit (e.g., "who acted on what with which permission at what time") composes from per-domain evidence with no overlap.

### What becomes harder

- **Pillar coordination requirements increase during transition.** Until Shield activates, Citadel must hold two domains' worth of authoring; coordination cost is non-zero. The transitional posture is explicit about this and includes a one-way migration contract.
- **Provider-specific patterns become more disciplined.** Where a provider's permission model doesn't cleanly map to the four domains, we must articulate the translation explicitly in a transitional spec or parent standard. This is more work than ad-hoc placement but reduces ongoing drift.
- **Subsidiary restatement obligation expands slightly.** Subsidiaries that touch policy systems may need to restate the topology in their own voice per ORG-001. The current restatement cadence already accommodates this; the obligation does not create new structural pressure beyond what ORG-001 already imposes.

### Risks

- **Shield activation slip.** If Shield's Q2 2026 target slips significantly, Citadel carries the Identity and Permission-Binding Domain authoring longer than intended. Mitigation: the transitional posture is explicit; Citadel has been holding these domains de facto already. Drift between intended Shield authorship and de facto Citadel authorship is bounded by the contract (Citadel's holdings migrate one-way when Shield activates).
- **Runtime Enforcement Domain ambiguity.** The current state is that we rely on provider-runtime enforcement for provider resources and have not wired Nexus to our own request-path admission. This is unchanged by the ADR — the ADR acknowledges the domain as distinct without committing to a specific technology. Selection of runtime-enforcement topology (sidecar, library, etc.) remains an open ADR-gated question per Shield's framing.
- **Composition rule edge cases.** Some policy artifacts (e.g., shared rulesets, account-wide WAF, organization-level cross-account policies) span domains in non-obvious ways. The transitional specs and parent standards layer absorb the translation; this ADR articulates the principle but does not pre-decide every edge case.

### Mitigations

- The transitional posture is contractual: Shield activation is the single migration event; the migration is one-way; identifiers are preserved per Principle 7.
- The composition rule is testable: for any policy, the four-domain decomposition can be applied and any domain owner can be checked against the pillar mapping. Misalignment surfaces as a finding in the contamination-scan tradition established by ORG-001.
- Edge cases get explicit treatment at the transitional-spec layer, where provider names are allowed and concrete decomposition can be authored.

## References

### Principles this ADR implements

- **Principle 5: Infrastructure as Code** — Resource Domain is IaC-shaped; Citadel implements Permission-Binding via IaC consuming Shield contracts.
- **Principle 9: Zero Trust** — Identity Domain registry plus Permission-Binding contracts plus Runtime Enforcement implements zero-trust authority separation. Authority topology extends Zero Trust from request-time verification to authoring-time domain separation.
- **Principle 10: Least Privilege** — Permission-Binding Domain operates at exact-minimum scope; the topology makes the granularity of "minimum" explicit (per-actor + per-scope + per-permission).
- **Principle 11: Observability** — Identity Domain owns audit contracts; per-domain evidence composes into cross-domain audit without overlap.
- **Principle 15: Three Circles of Trust** — Parent-published topology (Covenant layer); subsidiary-restated topology (subsidiary layer); project/dev-agent execution within those circles.

### Related governance artifacts

- **ADR-001: Three-Pillar Repository Architecture** — Establishes the pillars this topology maps to.
- **ADR-005: Adopt OpenTofu as IaC Engine** — Establishes the IaC engine that implements Resource and Permission-Binding Domain artifacts.
- **ADR-007: Subsidiary Authority and Identity Isolation** — Establishes the parent_l0 / subsidiary_l1 / project_l2 authority tiers that the Identity Domain consumes as metadata.
- **ORG-001: Subsidiary Authority and Identity Isolation** — Governs how the topology is restated by subsidiaries.
- **SEC-005: Machine Identity** — Defines machine identity types; the Identity Domain extends SEC-005 across the four-domain decomposition without superseding it.
- **GOV-003: Break-Glass Procedures** — Provides emergency override across all four domains; not domain-specific.

### Specifications this ADR shapes

- **Identity and Account Management Specification** (currently `policies/specs/identity-and-account-management.md`) — v0.2.0 amendment adds §7 "Authority Topology for Identity, Resource, and Policy-Binding" articulating this topology as the framework underlying §1–6.
- **Cloudflare Ownership Transition Specification** (`policies/specs/cloudflare-ownership-transition.md`) — Anticipated amendment to align with the topology; provider-specific translation lives in this transitional spec.
- **`iam-specification.md` REWRITE PENDING** — When that rewrite proceeds, it inherits this topology as foundational.

### Implementation layers

- **Shield's design baseline** (`the-shield/docs/identity-foundation-plan-2026-05-11.md`, `iam-architectural-posture-2026-05-11.md`, `pac-alignment-2026-05-11.md`) absorbs this topology as primary design input.
- **Citadel's structure** (`the-citadel/terraform/`) implements the Resource Domain and Permission-Binding Domain artifacts; consumes Shield contracts.
- **Nexus's runtime admission** (`the-nexus/policy/`) implements Runtime Enforcement Domain for surfaces where we operate the runtime.
- **Parent standards** (`.org/standards/`) translate the topology to provider-specific implementation patterns.

## Ratification

This ADR proposes a Covenant-tier change. Per `GOVERNANCE.md §Covenant Decisions`, the default ratification path requires 2 Watchers + 2 Mentors and a 72-hour debate period minimum.

Per `STATUS.md §Governance Exceptions row 4` and `ADR-007 §Current-state note`, the standing single-Guardian quorum exception applies until the synthetic council per FU-1 is operational. The Guardian ratifies under that exception with the following acknowledgments:

- The full 2W+2M quorum is restored when the synthetic council per FU-1 is operational.
- Each Covenant-tier change under the exception is recorded with date and authority basis in the document's changelog.
- Changes ratified under the exception are eligible for re-ratification through the council when the council operates per the FU-1 operational definition (Synthetic Council restoration trigger).

Ratification of this ADR carries the corresponding `identity-and-account-management.md` v0.2.0 amendment as a paired Covenant-tier change. The amendment makes the topology concrete in spec form; the ADR makes the decision discoverable in the architecture record.

### Guardian Sign-Off Template

When the Guardian ratifies this ADR (and the paired IAM Spec amendment), record under the changelog table below:

```
| 2026-MM-DD | Guardian (jeffrey) | **Proposed → Accepted.** Ratified under the Covenant-tier single-Guardian quorum exception (STATUS.md §Governance Exceptions row 4 + ADR-007 §Current-state note). Full 2W+2M quorum restored when FU-1 synthetic council is operational. Paired ratification: identity-and-account-management.md v0.1.0 → v0.2.0 (§7 Authority Topology added). |
```

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2026-05-17 | Agent | Initial DRAFT of ADR-008 — Policy Authority Topology. Articulates the four-domain decomposition (Identity, Resource, Permission-Binding, Runtime Enforcement) and maps each to an owning pillar (Shield, Citadel, Shield contracts consumed by Citadel implementations, runtime). Provider-agnostic; transitional and provider-specific content explicitly delegated to lower layers. Paired with identity-and-account-management.md v0.2.0 amendment for ratification. Awaiting Guardian sign-off under the single-Guardian quorum exception. |
