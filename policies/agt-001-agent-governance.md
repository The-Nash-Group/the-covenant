# AGENT-GOVERNANCE: Synthetic Agent Governance Policy

*Policy ID: AGT-001*
*Status: Active*
*Covenant Principle: Human Mandate Extension*
*Guardian Ownership: Watchers*

> "Agents are tools that humans delegate tasks to, not decision-makers."

## Purpose

This policy defines the governance framework for synthetic agents operating within The Nash Group ecosystem. It establishes boundaries, authority levels, and accountability mechanisms to ensure agents serve human purposes while maintaining operational efficiency.

## Scope

This policy applies to:
- All automated agents operating on behalf of The Nash Group
- AI systems with access to organizational resources
- Synthetic Council proceedings
- Cross-subsidiary agent operations

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
3. Human approval: 2 Watchers + 2 Mentors
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

## Subsidiary-Specific Rules

### Happy Patterns LLC

Stricter governance due to legal entity status:
- Financial threshold: $500 (vs. parent $1000)
- Council required for: billing changes, contract integrations
- Additional reviewer: legal review for customer-facing changes

### Litecky Editing Services

Isolated operations with spouse co-ownership:
- Strict isolation: No cross-subsidiary automation
- Either owner (Jeffrey or spouse) can approve changes
- External integrations require explicit consent

### Seven Springs

Relaxed sandbox environment:
- Elevated autonomous authority
- Council optional for experimental features
- Higher autonomous budget: $200

### Jefahnierocks

Inherits parent defaults without modification.

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

- `governance/agent-roles.yaml` - Role definitions
- `governance/config/governance-config.yaml` - Authority matrix
- `governance/subsidiary-overrides.yaml` - Subsidiary rules

### Change Authority

Changes to agent governance require:
- **Covenant Level**: 2 Watchers + 2 Mentors, 72h debate
- **ADR Required**: Document rationale in Architecture Decision Record
- **Phased Rollout**: Test in seven-springs before production

## Related Policies

- **GOV-003**: Break-Glass Procedures
- **GOV-004**: Team Authority Matrix
- **SEC-003**: Least Privilege
- **OPS-001**: Change Management
- **HUMAN_MANDATE.md**: Guardian Role Definitions

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
