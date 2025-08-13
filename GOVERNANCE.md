# GOVERNANCE.md
*The Laws of the Clans*

> "Power shared wisely is power multiplied. Power hoarded foolishly is power lost."

## The Foundation: The Human Mandate

This governance structure operates within the framework of [The Human Mandate](./HUMAN_MANDATE.md), which defines the five archetypal roles that Guardians fulfill: The Philosopher, The Architect, The Judge, The Gardener, and The Explorer. While the roles below define formal authority, the Mandate defines functional responsibility.

## The Hierarchy of the Realm

### The Clans and Their Powers

#### The Immortals (Contributors)
- **Who They Are**: All members of The Nash Group organization
- **Their Power**: 
  - Propose changes (Pull Requests) to any repository they have access to
  - Participate in debates on proposed changes
  - Raise issues and concerns
  - Share knowledge and experience
- **Their Responsibility**: 
  - Uphold the principles of the Covenant
  - Review and provide feedback on proposals
  - Share knowledge freely with fellow Immortals

#### The Mentors (Maintainers/CODEOWNERS)
- **Who They Are**: Senior engineers designated as code owners for specific domains
- **Primary Mandate Roles**: The Judge, The Architect, The Gardener (see [Human Mandate](./HUMAN_MANDATE.md#from-mandate-to-mission-how-roles-map-to-teams))
- **Their Power**:
  - Approve changes within their designated territories (as defined in CODEOWNERS)
  - Block merges that violate our principles
  - Guide Immortals in their growth
  - Translate principles into technical implementation
- **Their Responsibility**:
  - Maintain quality and consistency
  - Review proposals thoroughly and promptly
  - Document decisions and share knowledge
  - Ensure principles are properly implemented in `citadel-config`

#### The Watchers (Administrators)
- **Who They Are**: The guardians of infrastructure and organization-wide concerns
- **Primary Mandate Roles**: The Judge (Security), The Philosopher (Security), Emergency Responder (see [Human Mandate](./HUMAN_MANDATE.md#from-mandate-to-mission-how-roles-map-to-teams))
- **Their Power**:
  - Modify organization settings and team structures
  - Access billing and security configurations
  - Emergency override capabilities (break-glass procedures)
  - Final arbitration on governance disputes
- **Their Responsibility**:
  - Protect the infrastructure
  - Ensure compliance and security
  - Maintain the bridge between Covenant and Citadel
  - Act as stewards, not tyrants

## The Arenas of Decision

Different decisions require different levels of authority and consensus:

### Stronghold Decisions (Individual Repositories)
- **Scope**: Changes affecting a single service or repository
- **Authority**: The repository's designated Mentors
- **Process**: Standard PR review and approval
- **Required Approvals**: 1 Mentor minimum (2 for critical services)

### Citadel Decisions (Infrastructure)
- **Scope**: Changes to `citadel-config` affecting Cloudflare, GitHub settings, or other infrastructure
- **Authority**: Joint between Mentors and Watchers
- **Process**: 
  1. Proposal must reference a principle from the Covenant
  2. Terraform plan must be reviewed
  3. Changes affecting security require Watcher approval
- **Required Approvals**: 1 Mentor + 1 Watcher for infrastructure changes

### Covenant Decisions (Constitutional Changes)
- **Scope**: Changes to this repository - our principles, governance, or standards
- **Authority**: The Council (collective of senior Mentors and Watchers)
- **Process**: The Ritual of Amendment (see below)
- **Required Approvals**: 2 Watchers + 2 Mentors from different clans

## The Ritual of Amendment

Changing the Covenant is a sacred act. It requires deliberation, consensus, and ceremony.

### 1. The Proposal
- Fork the repository and create a branch named `proposal/[brief-description]`
- Make your changes with clear commits
- Write a comprehensive PR description using the template
- Your proposal must include:
  - **The Change**: What principle or governance rule is being modified?
  - **The Rationale**: Why is this change necessary?
  - **The Impact**: How will this affect our daily operations?
  - **The Implementation**: What changes will be needed in `citadel-config`?

### 2. The Debate Period
- **Minimum Duration**: 72 hours for minor changes, 1 week for major changes
- **Participation**: All Immortals may comment and suggest modifications
- **Revisions**: The proposer may amend their proposal based on feedback
- **Blocking Concerns**: Any Mentor or Watcher may raise a blocking concern that must be addressed

### 3. The Council Review
- **Quorum**: At least 4 members (2 Watchers + 2 Mentors)
- **Voting**: Approval requires consensus (no blocking objections)
- **Veto Power**: Any Watcher may veto changes that violate core values
- **Documentation**: All decisions must be recorded in the PR discussion

### 4. The Proclamation
Upon approval and merge:
- The change is announced in `#engineering-announcements`
- A corresponding issue is automatically created in `citadel-config` for implementation
- The merge commit includes all approvers as co-authors
- The decision is recorded in `REFERENCE/decisions/`

## Emergency Powers

In times of crisis, normal governance may be suspended:

### Break-Glass Procedures
- **When**: Critical security issues, production outages, or compliance emergencies
- **Who**: Any Watcher may invoke emergency powers
- **What**: Direct changes to infrastructure without prior Covenant approval
- **After**: 
  - Emergency changes must be documented within 24 hours
  - A post-mortem must be conducted within 1 week
  - Covenant updates must be proposed to codify lessons learned

### The Right of Challenge
- Any Immortal may challenge an emergency action after the crisis
- Challenges are reviewed by the full Council
- Unjustified emergency actions may result in power restrictions

## The Teams

Current team structures and their territorial authority:

### `@the-nash-group/mentors`
- **Territory**: All application code and service repositories
- **Members**: [Maintained in GitHub Teams]
- **Selection**: Nominated by peers, approved by Watchers

### `@the-nash-group/watchers`
- **Territory**: Organization settings, infrastructure, security
- **Members**: [Maintained in GitHub Teams]
- **Selection**: Appointed based on demonstrated responsibility

### `@the-nash-group/platform-clan`
- **Territory**: Platform services (`service-*` repositories)
- **Members**: Specialists in platform and infrastructure
- **Selection**: Self-organized with Mentor approval

## Conflict Resolution

When the clans disagree:

### The Escalation Path
1. **Technical Disagreement**: Resolved by the relevant Mentors
2. **Cross-Clan Dispute**: Escalated to a Council of Mentors
3. **Governance Conflict**: Arbitrated by the Watchers
4. **Constitutional Crisis**: Resolved by unanimous Watcher consensus

### The Principles of Resolution
- **Data Over Opinion**: Decisions should be backed by evidence
- **User Over Developer**: What serves our users best?
- **Simple Over Complex**: The boring solution often wins
- **Covenant Over Convention**: Our principles guide us

## Evolution and Adaptation

This governance model is designed to evolve:

### Regular Reviews
- **Quarterly**: Team membership and permissions review
- **Bi-Annually**: Governance effectiveness assessment
- **Annually**: Complete Covenant review and refresh

### Metrics of Health
- Time from proposal to decision
- Participation rate in governance decisions
- Implementation lag (Covenant to Citadel)
- Emergency override frequency

## The Binding Oath

All who join The Nash Group implicitly accept this governance model. By contributing to our repositories, you agree to:

1. Respect the decision-making process
2. Participate constructively in debates
3. Accept the will of the Council
4. Put the collective good above individual preference
5. Share knowledge freely and openly

---

*"In unity, strength. In debate, wisdom. In code, immortality."*

**Next Document**: [`PRINCIPLES.md`](./PRINCIPLES.md) - Our technical standards  
**Implementation**: [`citadel-config`](https://github.com/the-nash-group/citadel-config) - Where philosophy becomes reality
