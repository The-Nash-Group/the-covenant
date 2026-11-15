# AGENT-GOVERNANCE: Synthetic Agent Governance Policy

*Policy ID: AGT-001*
*Status: Active*
*Last Updated: 2026-11-15*
*Covenant Principle: Human Mandate Extension*
*Guardian Ownership: Watchers*
*Related: ORG-001 (Subsidiary Authority and Real Boundaries), Subsidiary Authority Specification*

> "Agents are tools that humans delegate tasks to, not decision-makers."

## Purpose

This policy defines the governance framework for synthetic agents operating within The Nash Group ecosystem. It establishes boundaries, authority levels, and accountability mechanisms to ensure agents serve human purposes while maintaining operational efficiency.

## Scope

This policy applies to:
- All automated agents operating on behalf of The Nash Group (parent-scope / L0 agents)
- AI systems with access to parent organizational resources
- Synthetic Council proceedings
- **Cross-entity parent orchestration** — parent agents that act adjacent to subsidiary operations (e.g., spanning multiple subsidiary repos, reviewing or merging a subsidiary's pull request, running the check of the five real things)

This policy **does not** apply to subsidiary-scope agents (L1 and L2). Per ORG-001, subsidiary agents operate under subsidiary authority — each subsidiary defines its own agent governance, within the minimum contract for product-agents in `governance/agent-roles.yaml`. Parent does not prescribe subsidiary agent behavior beyond that minimum contract.

## Core Principles

### Principle AGT-1: Agents Operate Within Explicit Bounds

**The Law**
No agent shall operate outside its defined authority. Every agent action must trace to an explicit capability grant in `governance/agent-roles.yaml`.

**The Lesson**
Unbounded automation is not helpful—it's dangerous. An agent that "helpfully" exceeds its mandate creates unpredictable system states and erodes human trust.

**Enforcement**
- Agent capabilities are enumerated, not discovered
- Actions outside enumeration are blocked at the API level
- Violations generate CRITICAL alerts to Watchers

### Principle AGT-2: Every Action is Auditable

**The Law**
Every agent action must emit a complete audit trail. The trail must include: timestamp, agent ID, action type, inputs, outputs, authority citation, and outcome.

**The Lesson**
"The agent did it" is not acceptable incident response. Humans must be able to reconstruct any agent action with full fidelity.

**Enforcement**
- All agent actions logged to immutable audit store
- Audit entries include cryptographic proof of sequence
- Logs retained for minimum 365 days
- Missing audit entries are CRITICAL violations

### Principle AGT-3: Escalation is Not Failure

**The Law**
Agents must escalate when encountering situations beyond their authority. Escalation is a success case, not a failure mode.

**The Lesson**
An agent that guesses rather than asks creates worse outcomes than one that admits uncertainty. Human judgment exists precisely for edge cases.

**Enforcement**
- Agent confidence thresholds defined per role
- Below-threshold situations require escalation
- Escalation metrics tracked and reviewed quarterly
- "Always escalates" and "never escalates" patterns investigated

### Principle AGT-4: The Council is Advisory

**The Law**
Synthetic Council verdicts are recommendations, not decisions. Human Guardians retain final authority on all Citadel and Covenant level decisions.

**The Lesson**
Adversarial debate improves decision quality but cannot replace human judgment on matters of governance, security, and strategy.

**Enforcement**
- Council verdicts require human ratification per authority matrix
- Verdicts without human approval cannot proceed
- "Rubber stamp" approval patterns generate warnings

### Principle AGT-5: Agents Respect Entity Boundaries

**The Law**
Parent-scope agents must not author in a subsidiary's repository (except break-glass per GOV-003). They may read a subsidiary's repository, and may review and merge there under the merge rule that ORG-001 cites from the parent's Agentic Workflow Standard, section One-Human Operating Contract. They hand off to a subsidiary's session directly, and a record is kept only across one of the five real boundaries of ORG-001.

None of this applies to Litecky Editing Services. No parent-scope agent reads into, writes to, reviews or merges in Litecky beyond what Litecky's own contract already allows.

**The Lesson**
A boundary is worth an agent's care where it separates something real: another person's interest or a separate legal entity, money, credentials, customers' data and legal-entity records, public identity. Separation of text between one Guardian's own agents protected none of these. Authoring stays with the owning organization's sessions because an organization's record is its own.

**Enforcement**
- Parent agents author only in parent repositories. Nothing mechanical refuses otherwise: the parent's Agentic Workflow Standard records that sessions act through one GitHub login. The readback is the authoring session named on the pull request and the review record on it
- A merge in a subsidiary's repository carries, on the pull request, the record that the merge rule asks for
- Credential values never cross between organizations and agents hold no provider credential (ORG-001 Boundary 3; SEC-005 is unchanged)
- Contamination findings are no longer tracked for any organization. The parent does not read into Litecky to audit it; Litecky's part of the check of the five real things is run from inside Litecky by its own session and reported value-blind
- Break-glass cross-entity writes are logged and reconciled per GOV-003 within 24 hours

## Agent Authority Matrix

### Stronghold Level (Routine)

| Agent | Autonomous | Propose | Escalate |
|-------|------------|---------|----------|
| Gardener | L2 deps, formatting, docs | L1 deps, refactoring | L0 deps, breaking changes |
| Explorer | Sandbox research, PoC | Pattern adoption, tech eval | Paradigm shifts |
| Coordinator | Task routing, status | Workflows, allocation | Conflicts, deadlocks |

### Citadel Level (Infrastructure)

All Citadel decisions require:
1. Synthetic Council debate
2. Council verdict of APPROVED
3. Human approval: 1 Mentor + 1 Watcher
4. 4-hour cool-down before apply

| Agent | Role |
|-------|------|
| Steward | Risk identification, policy citation |
| Catalyst | Implementation proposal, mitigation design |
| Adjudicator | Debate synthesis, verdict generation |

### Covenant Level (Governance)

All Covenant decisions require:
1. Synthetic Council debate
2. Council verdict of APPROVED
3. Human approval: current GOV-006 structural single-Guardian mode; the normal
   2-Watcher + 2-Mentor model remains dormant until separately activated
4. 72-hour debate period

Agent role: Advisory only. Agents may research, summarize, and propose, but all governance decisions are human decisions.

## Synthetic Council Protocol

### Council Composition

A valid council session requires:
- **Steward-Agent**: Takes adversarial (risk) position
- **Catalyst-Agent**: Takes advocacy (velocity) position
- **Adjudicator-Agent**: Synthesizes and renders verdict

### Debate Requirements

1. **Minimum Rounds**: 2 debate rounds minimum
2. **Policy Citations**: Steward objections MUST cite specific policy IDs
3. **Mitigations**: Catalyst MUST propose mitigations for valid objections
4. **Self-Critique**: Adjudicator MUST challenge own conclusions
5. **Instant Consensus**: Triggers Deep Scrutiny Mode (adversarial re-debate)

### Verdict Format

All council verdicts must include:
```yaml
verdict: APPROVED | REJECTED | ESCALATE
rationale: "Clear explanation of decision logic"
policy_citations:
  - policy_id: "SEC-003"
    alignment: "compliant"
self_critique:
  catastrophic_scenario: "Description of worst case"
  risk_probability: 0.05  # Must be < 0.10 to approve
conditions:
  - "Any conditions attached to approval"
reasoning_trace:
  - "Step 1: ..."
  - "Step 2: ..."
```

### Verdict Thresholds

| Verdict | Requirements |
|---------|-------------|
| APPROVED | All policy citations verified, risk < 10%, no unmitigated blocking objections |
| REJECTED | Policy violation unmitigated OR risk >= 10% |
| ESCALATE | Novel situation, policy ambiguity, or council deadlock |

## Cross-Entity Escalation Awareness

> **Scope note**: This section records what *parent* orchestration agents must be aware of when their work touches subsidiary-adjacent concerns. It does not prescribe subsidiary-internal agent governance — per ORG-001, each subsidiary authors its own agent governance on its own authority. The rules below govern parent behavior at the entity boundary.

The subsidiary registry at `.org/iam/federation/subsidiaries.yaml` records each subsidiary's `governance_level` and any `governance_override` the parent has agreed to recognize for cross-entity coordination. When a parent-scope agent acts adjacent to a subsidiary (for example, publishing a standard that a subsidiary may cite, reviewing or merging a subsidiary's pull request, or running the check of the five real things), the agent must:

### Happy Patterns LLC (own GitHub org: `happy-patterns-org`)

- Recognize that cross-entity financial coordination (billing reconciliation, shared infrastructure cost allocation) involves a separate LLC with its own legal and tax treatment
- Leave any change that would affect Happy Patterns' customer-facing artifacts to Happy Patterns' own session: it crosses the public-identity boundary and is recorded in Happy Patterns' own repository
- Treat Happy Patterns' own contract as authoritative within its own GitHub org; keep parent names, role names and policy numbers out of its public and customer-facing material and its legal documents

### Litecky Editing Services

- Litecky is a sole proprietorship that belongs to another person. It is not co-owned. The Guardian is its administrator, and the administrator decides: every Litecky decision comes to him
- Never contact Litecky's owner, ask for her approval, or wait on it. What is hers to decide as the business owner the administrator takes to her himself
- Litecky is a real boundary in both directions: do not read into, write to, review or merge in Litecky beyond what Litecky's own contract already allows
- Treat cross-subsidiary automation as explicitly declined — the registry's `isolation: { cross_subsidiary_access: none }` entry applies to parent orchestration as well
- External integrations touching Litecky Editing require the administrator's decision
- The parent's registry is to keep a place for an owner governance role, unassigned; assume nothing from it

### Seven Springs (sandbox)

- No special rule applies. The pedagogical exception of earlier text excepted Seven Springs from identity isolation in agent-facing files, which ORG-001 version 2.0 retired
- The registry and the Identity and Account Management Specification record Seven Springs' activation state; read them before acting there

### Jefahnierocks (personal/creative)

- Treat as a full subsidiary under ORG-001: the five real boundaries apply equally
- Do not treat `jefahnierocks` as a relaxed extension of parent personal work; it has its own identity layer

**Subsidiary-internal rules** (financial thresholds, council triggers, approval counts within the subsidiary's own governance, legal review requirements, etc.) are authored by each subsidiary in its own artifacts. Parent does not prescribe them. This section is parent-scope awareness of cross-entity boundaries, not subsidiary-scope governance.

## Human Override Mechanisms

### Mandatory Escalation Triggers

Agents MUST escalate to humans when:
1. **Novel Situation**: No precedent in ADRs or policies
2. **Constitutional Conflict**: Two principles in direct conflict
3. **High Financial Impact**: > $1000 USD
4. **Security Critical**: Credentials, PII, access control
5. **Cross-Subsidiary**: Affects multiple subsidiaries

### Break-Glass Override

Per GOV-003, Watchers may invoke break-glass to:
- Bypass council debate requirement
- Override cool-down periods
- Exceed approval count requirements

Break-glass CANNOT override:
- Audit logging requirements
- Principle violations
- Security scanning

### Human Intervention Points

| Decision Level | Agent Authority | Human Authority |
|----------------|-----------------|-----------------|
| Stronghold | Autonomous within bounds | Async audit |
| Citadel | Propose via council | Approve/reject |
| Covenant | Advisory only | Full decision authority |

## Compliance and Monitoring

### Quarterly Agent Assessment

Agents are assessed quarterly on:
- **Uptime/Reliability**: 99.9% target
- **Authority Adherence**: % of actions within bounds
- **Escalation Appropriateness**: Quality of escalation decisions
- **Human Satisfaction**: Guardian feedback score

### Violation Response

| Severity | Response Time | Escalation |
|----------|---------------|------------|
| CRITICAL | Immediate | Page Watchers |
| HIGH | 15 minutes | Slack + Email |
| MEDIUM | 1 hour | Daily digest |
| LOW | 24 hours | Weekly report |

### Audit Requirements

Per Principle AGT-2, all agent actions must:
- Emit structured JSON audit entries
- Include full context (inputs, outputs, authority)
- Be stored in immutable log with retention >= 365 days
- Support replay and forensic analysis

## Configuration Management

### Source Files

- `governance/agent-roles.yaml` — Role definitions (includes product-agent minimum contract for subsidiary-scope)
- `governance/config/governance-config.yaml` — Authority matrix
- `.org/iam/federation/subsidiaries.yaml` — Subsidiary registry with per-subsidiary `governance_level` and any `governance_override` fields (authoritative; supersedes the previously referenced `governance/subsidiary-overrides.yaml` path which was never created)

### Change Authority

Changes to agent governance require:
- **Covenant Level**: GOV-006 structural single-Guardian mode; multi-human
  Council timing and quorum apply only if that mode is separately activated
- **ADR Required**: Document rationale in Architecture Decision Record
- **Phased Rollout**: Test in seven-springs before production

## Related Policies

- **ORG-001**: Subsidiary Authority and Real Boundaries — entity-boundary rules for parent agents
- **GOV-003**: Break-Glass Procedures
- **GOV-004**: Team Authority Matrix
- **SEC-003**: Least Privilege
- **OPS-001**: Change Management
- **HUMAN_MANDATE.md**: Guardian Role Definitions

## Related Specifications

- **Subsidiary Authority Specification** (`policies/specs/subsidiary-authority.md`) — Operational model for the three-tier authority structure; per-subsidiary current-state assessment
- **Subsidiary Governance Standard** (`.org/standards/subsidiary-governance.md`) — Session routing mechanics

---

## Quick Reference

### Agent Can Autonomously:
- L2 dependency updates
- Code formatting
- Documentation sync
- Sandbox experimentation
- Task routing

### Agent Must Propose:
- L1 dependency updates
- Feature implementations
- Infrastructure changes
- Pattern adoptions

### Agent Must Escalate:
- L0 dependencies
- Breaking changes
- Security critical
- Cross-subsidiary
- Novel situations

---

*"The machine executes perfectly. The human decides wisely. Together, they create civilization."*

*Effective Date: 2024-11-24*
*Review Cycle: Quarterly*
*Policy Owner: @the-nash-group/watchers*
