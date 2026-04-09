# OPS-006: Guardian Role Responsibilities

**Policy ID:** OPS-006
**Category:** Operations
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

All Guardians **must** wear specific archetypal hats during their work: Philosopher, Architect, Judge, Gardener, or Explorer. Each role **shall** have clearly defined responsibilities, performance expectations, and decision-making authority. Role clarity **must** be maintained through explicit hat declaration in all significant actions.

## Rationale

From The Human Mandate's Five Archetypes of Guardianship: "These are not job titles but 'hats' that Guardians wear depending on the task at hand. A single person may wear multiple hats throughout their day."

The Human/Machine boundary requires deliberate human judgment channeled through specific archetypal roles:

- **Context Switching Clarity**: Without explicit role declaration, guardians operate in ambiguous capacity leading to conflicting expectations
- **Responsibility Accountability**: Clear role definitions enable proper performance evaluation and knowledge transfer
- **Decision Authority**: Different roles carry different levels of authority and responsibility for various types of decisions
- **Cultural Preservation**: Archetypal roles embody organizational values and ensure cultural continuity across team changes
- **Human Judgment Focus**: Each role channels human wisdom and context in specific ways that complement machine execution

These archetypal roles ensure that human responsibilities remain distinct from machine automation while providing clear frameworks for exercising judgment, creativity, and leadership within our technical systems.

## Scope

**Applies To:**
- All Guardians when making decisions affecting infrastructure, processes, or governance
- All significant actions including PRs, reviews, incident response, and architectural decisions
- All team interactions requiring clear authority and responsibility delineation
- All documentation and communication requiring role-based context
- All performance evaluations and career development activities

**Role Boundaries:**
- Individual practices: Personal role awareness and conscious hat-wearing
- Team processes: Role-based task assignment and responsibility matrices
- Organizational rituals: Role effectiveness assessment and cultural reinforcement

## Implementation

### Technical Enforcement

GitHub PR templates must include role declaration:

```markdown
# Pull Request Template
## Guardian Role Declaration
**Hat being worn:** [ ] Philosopher | [ ] Architect | [ ] Judge | [ ] Gardener | [ ] Explorer

**Role Context:**
<!-- Explain why this role is appropriate for this change -->

## Change Alignment
**Covenant Principle:** <!-- Which principle from the-covenant guides this work -->
**Human/Machine Boundary:** <!-- How does this respect the boundary -->
```

Terraform code comments must include role attribution:

```hcl
# terraform/github/repositories.tf
# ROLE: Architect - Translating covenant principles into technical implementation
# PRINCIPLE: Infrastructure as Code - All changes through version control
resource "github_repository" "service_template" {
  name        = var.repository_name
  description = "Service following Nash Group patterns"

  # Hat: Architect - Designing reusable organizational patterns
  template {
    owner      = "the-nash-group"
    repository = "service-template"
  }
}
```

### Automated Validation

CI pipeline role validation:

```yaml
# .github/workflows/guardian-role-check.yml
name: Guardian Role Validation
on: [pull_request]
jobs:
  validate-role:
    runs-on: ubuntu-latest
    steps:
      - name: Check Role Declaration
        run: |
          if ! grep -q "Hat being worn:" PR_BODY; then
            echo "ERROR: PR must declare Guardian role"
            exit 1
          fi
      - name: Validate Role Context
        run: |
          if ! grep -q "Role Context:" PR_BODY; then
            echo "ERROR: Must explain role appropriateness"
            exit 1
          fi
```

Bot automation for role tracking:

```hcl
# terraform/github/apps.tf
# ROLE: Gardener - Maintaining organizational health through automation
resource "github_app_installation" "role_tracker" {
  app_id          = var.role_tracker_app_id
  installation_id = var.installation_id

  # Tracks role declarations across all repositories
  # Reports role distribution and effectiveness metrics
}
```

### Human Process

**Daily Role Declaration:**
1. Guardians must consciously choose their primary hat for each work session
2. Role context must be documented in commit messages and PR descriptions
3. Role transitions must be explicit when switching between different types of work
4. Cross-functional work requires role clarification to avoid responsibility conflicts

**Performance Management:**
1. Performance reviews must evaluate effectiveness in each role worn
2. Career development plans must identify role strengths and growth areas
3. Team role distribution must be balanced across all five archetypes
4. Role mentorship programs must pair experienced guardians with developing ones

**Cultural Reinforcement:**
1. Team meetings begin with role check-ins
2. Incident response assigns roles based on situation requirements
3. Architecture decisions require explicit Architect hat declaration
4. Policy changes require explicit Philosopher hat declaration

## Compliance Verification

### Automated Checks

**Code Analysis:**
```bash
# Daily role attribution audit
#!/bin/bash
# Check for role declarations in recent commits
git log --since="1 day ago" --grep="ROLE:" --oneline || {
  echo "WARNING: Commits without role attribution detected"
}

# Verify PR template compliance
for pr in $(gh pr list --json number -q '.[].number'); do
  if ! gh pr view $pr --json body -q '.body' | grep -q "Hat being worn:"; then
    echo "VIOLATION: PR #$pr missing role declaration"
  fi
done
```

**Metrics Collection:**
```sql
-- Role distribution analysis
SELECT
  guardian_name,
  role_type,
  COUNT(*) as actions_count,
  AVG(effectiveness_score) as avg_effectiveness
FROM guardian_actions
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY guardian_name, role_type
ORDER BY guardian_name, actions_count DESC;
```

### Manual Audits

**Quarterly Role Reviews:**
- Team role distribution assessment
- Individual role effectiveness evaluation
- Role conflict identification and resolution
- Cultural alignment verification with Human Mandate principles

**Annual Role Evolution:**
- Role definition updates based on organizational learning
- New role archetype consideration
- Role authority boundary adjustments
- Performance criteria refinement

### Reporting

**Weekly Role Metrics:**
- Role declaration compliance rate per team
- Role distribution balance across guardians
- Role effectiveness scores by archetype
- Role conflict incidents and resolutions

**Monthly Cultural Health:**
- Guardian satisfaction with role clarity
- Role-based decision quality assessment
- Human/Machine boundary respect metrics
- Archetypal role evolution tracking

## Related Documents

**Source Material:**
- [../the-covenant/HUMAN_MANDATE.md - The Five Archetypes of Guardianship](../the-covenant/HUMAN_MANDATE.md#the-five-archetypes-of-guardianship)
- [../the-covenant/HUMAN_MANDATE.md - From Mandate to Mission](../the-covenant/HUMAN_MANDATE.md#from-mandate-to-mission-how-roles-map-to-teams)

**Related Policies:**
- [OPS-007: Daily Stand Protocol](./ops-007-daily-stand.md) - Daily role consciousness
- [OPS-008: Weekly Review Process](./ops-008-weekly-review.md) - Team role assessment
- [GOV-004: Team Authority](./gov-004-team-authority.md) - Role-based authorities
- [GOV-008: Binding Oath](./gov-008-binding-oath.md) - Guardian oath including role responsibilities

**Technical References:**
- [../the-citadel/terraform/github/teams.tf](../the-citadel/terraform/github/teams.tf) - Team role implementations
- [../the-citadel/.github/PULL_REQUEST_TEMPLATE.md](../the-citadel/.github/PULL_REQUEST_TEMPLATE.md) - Role declaration template

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|---------|
| 2024-09-30 | 1.0 | Initial policy creation from Human Mandate archetypal roles | Claude |
