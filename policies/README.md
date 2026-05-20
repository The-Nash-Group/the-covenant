# The Nash Group Policies

*Constitutional policy framework implementing The Nash Group's governance principles*

## Overview

This directory contains the constitutional policy framework for The Nash Group,
transforming philosophical principles into durable invariants, governance
constraints, status semantics, and policy intent that lower layers can enforce.
It is not the long-term home for changing provider bindings, workflow paths,
credential names, or repo-local implementation procedures.

Operational examples and provider-specific specifications may remain here as
transitional buildout material until the policy-home correction work classifies
and moves or restates them into the proper layer: parent `.org` standards,
Shield identity contracts, Citadel infrastructure enforcement, Nexus runtime
admission, or subsidiary/project-local restatements.

> **Current-state note:** ADR-005 makes OpenTofu the active IaC engine in
> `the-citadel`. Some older policy examples still use historical Terraform
> wording or `terraform/` path names. Treat implementation snippets as
> illustrative translation targets unless current Citadel, Shield, Nexus, or
> subsidiary evidence proves they are live.

## Policy Categories

### Source Control (SC)
- **[SC-001: Linear Git History](./sc-001-linear-history.md)** - Main branch must maintain linear, clean history
- **[SC-002: Conventional Commits](./sc-002-conventional-commits.md)** - All commits follow conventional format, clear PR titles
- **[SC-003: Trunk-Based Development](./sc-003-trunk-based-development.md)** - Feature branches live days not months, main is single source of truth

### Security (SEC)
- **[SEC-001: Zero Trust Authentication](./sec-001-zero-trust.md)** - Authenticate every request, authorize every action, audit every access
- **[SEC-002: Secret Scanning](./sec-002-secret-scanning.md)** - No secrets in Git, push protection enabled
- **[SEC-003: Least Privilege Access](./sec-003-least-privilege.md)** - Exact permissions needed, no more, with expiration and renewal
- **[SEC-004: Security Baseline Requirements](./sec-004-security-baseline.md)** - Foundational security controls across all categories
- **[SEC-005: Machine Identity Management](./sec-005-machine-identity.md)** - GitHub Apps, OIDC, and scoped credentials for all machine-to-platform authentication

### Infrastructure (INF)
- **[INF-001: Infrastructure as Code](./inf-001-infrastructure-as-code.md)** - All infrastructure defined as code, manual UI changes forbidden

### Operations (OPS)
- **[OPS-001: Change Management Process](./ops-001-change-management.md)** - Comprehensive change control for all production systems
- **[OPS-002: Automated Quality Gates](./ops-002-quality-gates.md)** - All code must pass automated gates before merge
- **[OPS-003: Fail Fast Architecture](./ops-003-fail-fast.md)** - Systems must fail quickly and obviously when wrong
- **[OPS-004: Observability Requirements](./ops-004-observability.md)** - Every service must emit metrics, logs, and traces
- **[OPS-005: Runbook Standards](./ops-005-runbooks.md)** - Every alert has runbook, every runbook has tested manual steps
- **[OPS-006: Guardian Role Responsibilities](./ops-006-guardian-roles.md)** - All Guardians wear specific hats: Philosopher, Architect, Judge, Gardener, Explorer
- **[OPS-007: Daily Stand Protocol](./ops-007-daily-stand.md)** - Daily self-assessment: What hat? Covenant alignment? Automating or creating toil?
- **[OPS-008: Weekly Review Process](./ops-008-weekly-review.md)** - Teams assess Human/Machine boundary, identify automation opportunities
- **[OPS-009: Quarterly Reflection Ritual](./ops-009-quarterly-reflection.md)** - Organization evaluates role clarity, team authority, Human Mandate effectiveness
- **[OPS-010: Emergency Response Procedures](./ops-010-emergency-response.md)** - Watchers assume command, Mentors diagnose, all follow incident response
- **[OPS-011: Peer Review Requirements](./ops-011-peer-review.md)** - Every change to protected branches requires peer review

### Documentation (DOC)
- **[DOC-001: Documentation Requirements](./doc-001-documentation.md)** - Every repo has README, every API has schemas, every decision has ADR

### Dependencies (DEP)
- **[DEP-001: Breaking Change Management](./dep-001-breaking-changes.md)** - Breaking changes require migration paths, deprecation needs notice periods
- **[DEP-002: Three Circles of Trust](./dep-002-dependency-circles.md)** - L0 (Frontier), L1 (Vanguard), L2 (Supporting Cast) dependency management

### Governance (GOV)
- **[GOV-001: Living Principles](./gov-001-living-principles.md)** - Principles evolve through experience, not carved in stone
- **[GOV-002: Covenant Amendment Process](./gov-002-amendment-process.md)** - Covenant changes require proposal, debate, council review, proclamation
- **[GOV-003: Emergency Break-Glass Procedures](./gov-003-break-glass.md)** - Watchers can bypass normal process during critical emergencies
- **[GOV-004: Team Authority Matrix](./gov-004-team-authority.md)** - Immortals propose, Mentors approve domains, Watchers control infrastructure
- **[GOV-005: Conflict Resolution Process](./gov-005-conflict-resolution.md)** - Technical → Mentors, Cross-clan → Council, Governance → Watchers
- **[GOV-006: Council Decision Quorum](./gov-006-decision-quorum.md)** - 4-member quorum (2 Watchers + 2 Mentors), consensus required
- **[GOV-007: Governance Review Cycles](./gov-007-review-cycles.md)** - Quarterly team review, bi-annual governance assessment, annual Covenant refresh
- **[GOV-008: The Binding Oath](./gov-008-binding-oath.md)** - All contributors accept governance model, participate constructively
- **[GOV-010: Organizational Labeling Standard](./gov-010-labeling-standard.md)** - All resources require standard organizational labels for traceability

### Communication (COM)
- **[COM-001: Git Workflow Standards](./com-001-git-workflow.md)** - Linear history, conventional commits, and meaningful PR titles

### Agent Governance (AGT)
- **[AGT-001: Synthetic Agent Governance](./agt-001-agent-governance.md)** - Governance policy for AI/synthetic agents operating within the organization
- **[AGT-002: Agent Audit Workflows](./agt-002-audit-workflows.md)** - Executable audit instructions for automated verification agents
- **[AGT-003: Citadel Audit Framework](./agt-003-citadel-audit-framework.md)** - Systematic verification that Covenant principles are enforced
- **[AGT-004: Enforcement Checklist](./agt-004-enforcement-checklist.md)** - Master verification checklist for Citadel enforcement

### Organizational Authority (ORG)
- **[ORG-001: Subsidiary Authority and Identity Isolation](./org-001-subsidiary-authority.md)** - Three-tier authority model invariants (identity isolation, authority restatement, spec flow); operational rule for the boundary between parent and subsidiary

### Specifications
- **[Cloudflare Ownership Transition](./specs/cloudflare-ownership-transition.md)** (ACCEPTED v1.1.0) - Transitional stewardship and placement rules for Cloudflare resources; provider-specific sections should be classified for parent-standard or Citadel home.
- **[GitHub Machine Identity](./specs/github-machine-identity.md)** - GitHub App architecture and credential lifecycle for machine identities; provider-specific sections should be classified for Shield/Citadel home.
- **[Identity and Account Management](./specs/identity-and-account-management.md)** (v0.2.0; §§1-6 DRAFT — Accepted for Validation since 2026-05-03; §7 ratified 2026-05-17 via ADR-008) - Multi-entity identity contract plus the accepted policy authority topology; durable invariants remain here while identity-contract detail moves to Shield or parent standards.
- **[IAM Specification](./specs/iam-specification.md)** (PARTIALLY HISTORICAL — REWRITE PENDING) - Pre-ADR-005 IAM architecture reference.
- **[Secrets Management](./specs/secrets-management.md)** (ACTIVE v1.3.0) - Secret classification, lifecycle, ownership, distribution, and rotation model; provider-neutral invariants remain here while backend-specific bindings belong to owning implementation layers.
- **[Subsidiary Authority](./specs/subsidiary-authority.md)** (ACTIVE v1.0.3) - Operational model for parent, subsidiary, and project authority boundaries.
- **[Organizational Design Quality](./specs/organizational-design-quality.md)** (DRAFT v0.1.0) - Anchor quality bar for control-surface classification, ownership, review, evidence, and subsidiary restatement; not active policy.

> **Note**: GOV-009 was intentionally reserved for future use. The policy ID gap between GOV-008 and GOV-010 is deliberate.

## Source Document Mapping

These policies implement principles and procedures from The Nash Group's foundational documents:

### From PRINCIPLES.md
| Principle | Policy | Description |
|-----------|---------|-------------|
| 1-2: Sacred Timeline & Commit Purpose | COM-001 | Git workflow standards |
| 3: No Code Unchallenged | OPS-002 | Peer review requirements |
| 4: Machines Must Bless | OPS-002 | Automated quality gates |
| 5: Fortress Defined by Blueprints | INF-001 | Infrastructure as Code |
| 6: Secrets Never Committed | SEC-002 | Secret scanning |
| 7: Trunk is Sacred | SC-003 | Trunk-based development |
| 8: Fail Fast, Recover Faster | OPS-003 | Fail fast architecture |
| 9: Trust, but Verify Everything | SEC-001, SEC-005 | Zero trust authentication, machine identity |
| 10: Least Privilege | SEC-003, SEC-005 | Least privilege access, scoped machine credentials |
| 11: If Not Measured, Doesn't Exist | OPS-004 | Observability requirements |
| 12: Runbooks Are Executable | OPS-005 | Runbook standards |
| 13: Code Without Docs Incomplete | DOC-001 | Documentation requirements |
| 14: Progress Without Breakage | DEP-001 | Breaking change management |
| 15: Three Circles of Trust | DEP-002 | Dependency management |
| 16: Living Law | GOV-001 | Living principles |

### From GOVERNANCE.md
| Section | Policy | Description |
|---------|---------|-------------|
| Ritual of Amendment | GOV-002 | Covenant amendment process |
| Break-Glass Procedures | GOV-003 | Emergency procedures |
| Hierarchy of the Realm | GOV-004 | Team authority matrix |
| Conflict Resolution | GOV-005 | Conflict resolution process |
| Council Review | GOV-006 | Decision quorum requirements |
| Evolution and Adaptation | GOV-007 | Governance review cycles |
| Binding Oath | GOV-008 | Contributor commitments |

### From HUMAN_MANDATE.md
| Section | Policy | Description |
|---------|---------|-------------|
| Five Archetypes | OPS-006 | Guardian role responsibilities |
| Daily Stand | OPS-007 | Daily protocol |
| Weekly Review | OPS-008 | Weekly team process |
| Quarterly Reflection | OPS-009 | Quarterly assessment |
| Emergency Protocols | OPS-010 | Emergency response |

## Policy Template Structure

Each policy follows a standardized template:

```markdown
# [ID]: [Name]

**Policy ID:** [ID]
**Category:** [Category]
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement
[Clear imperative using must/shall/will]

## Rationale
[Why this policy exists, lessons learned]

## Scope
**Applies To:** [Specific resources/processes]
**Exceptions:** [Documented exceptions]

## Implementation Impact
### Enforcement Home
[Citadel, Shield, Nexus, parent standard, subsidiary restatement, or project-local]
### Validation or Evidence
[CI/CD, monitoring, audit evidence, native control, manual review, or advisory status]
### Human Process
[Procedures, workflows, approvals]

## Compliance Verification
**Automated Checks:** [System validation]
**Manual Audits:** [Human verification]
**Reporting:** [Metrics and dashboards]

## Related Documents
- **Source Principle:** [Link to source]
- **Governance Authority:** [Link to authority]
- **Implementation:** [Link to code]

## Change History
- **2024-09-30** - Initial creation
```

## Implementation Status

### Translation and Enforcement
- **Covenant invariants**: Policies define durable rules and status semantics.
- **Implementation examples**: Older policies may contain OpenTofu, GitHub,
  Cloudflare, CI/CD, or workflow examples. These are translation targets or
  historical references unless backed by current evidence in the owning layer.
- **Citadel enforcement**: Provider bindings, OpenTofu/IaC, CI gates, and native
  controls are owned by Citadel.
- **Shield contracts**: IAM, identity registry, authorization-decision, and
  secret-authority metadata contracts are Shield/parent-standard work until
  implementation is authorized.
- **Nexus runtime admission**: Runtime policy loading and service-facing
  operational checks belong to Nexus once wired.
- **Subsidiary/project execution**: Local restatement and project-specific
  implementation belong to the owning entity or project.

### Human Processes
- ✅ **Role Definitions**: Clear responsibilities for Immortals, Mentors, Watchers
- ✅ **Approval Workflows**: Structured decision-making processes
- ✅ **Escalation Paths**: Clear conflict resolution procedures
- ✅ **Cultural Practices**: Daily, weekly, and quarterly rituals

### Compliance and Auditing Intent
- **Automated monitoring target**: Real-time compliance checking belongs in the
  owning enforcement layer when evidence proves the check is live.
- **Manual audit procedures**: Human verification processes remain valid even
  where automated controls are advisory, report-only, or source-tested only.
- **Reporting requirements**: Metrics, dashboards, and trends are expected
  evidence surfaces; current availability is determined by the owning repo.
- **Violation response**: Remediation procedures are defined here at the policy
  level and executed by the owning operational layer.

## Usage Guidelines

### For Policy Updates
1. Follow [GOV-002 Covenant Amendment Process](./gov-002-amendment-process.md)
2. Reference source principle being modified
3. Include implementation impact assessment
4. Maintain cross-reference integrity

### For Implementation
1. Review [GOV-004 Team Authority Matrix](./gov-004-team-authority.md) for approval requirements
2. Follow [OPS-001 Change Management Process](./ops-001-change-management.md) for production changes
3. Use [GOV-003 Emergency Break-Glass Procedures](./gov-003-break-glass.md) only for genuine emergencies

### For Compliance
1. Regular review per [GOV-007 Governance Review Cycles](./gov-007-review-cycles.md)
2. Incident response via [OPS-010 Emergency Response Procedures](./ops-010-emergency-response.md)
3. Conflict resolution using [GOV-005 Conflict Resolution Process](./gov-005-conflict-resolution.md)

## Success Metrics

- **Coverage**: 100% of PRINCIPLES.md, GOVERNANCE.md, and HUMAN_MANDATE.md formalized
- **Traceability**: Every policy traces to source documents with specific sections
- **Enforceability**: Every policy maps to an intended enforcement or evidence
  home; not every Covenant policy should embed implementation detail.
- **Completeness**: 38 numbered policies (SC, SEC, INF, OPS, DOC, DEP, GOV, COM, AGT, ORG) plus 6 specifications under `specs/`
- **Consistency**: Standardized template and cross-referencing throughout

> **Frontmatter currency note (2026-05-02)**: Most policies still carry their original `Last Updated: 2024-09-30` stamp because they have not been substantively revised since. Files with newer stamps (SEC-005, AGT-001, ORG-001, COM-001, INF-001, SEC-004) reflect intentional revisions. The original stamp is therefore truthful — not bulk-refreshed dishonestly — but readers should consult the linked Covenant ADRs (especially ADR-005 OpenTofu, ADR-007 Subsidiary Authority) and the active specifications for current enforcement detail.

---

*"These policies preserve The Nash Group's philosophical foundation as durable organizational reality; lower layers turn that foundation into evidence, automation, and operation."*

**Source Documents**: PRINCIPLES.md, GOVERNANCE.md, HUMAN_MANDATE.md
**Implementation**: [The Citadel](https://github.com/The-Nash-Group/citadel-config) - OpenTofu/IaC and Policy as Code enforcement where current Citadel evidence proves the control is live
**Change Process**: [GOV-002 Amendment Process](./gov-002-amendment-process.md)
