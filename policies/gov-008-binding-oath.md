# GOV-008: The Binding Oath

**Policy ID:** GOV-008
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

All contributors **must** accept the governance model upon joining The Nash Group. By contributing to repositories, contributors **shall** implicitly agree to respect the decision-making process, participate constructively in debates, accept Council decisions, prioritize collective good over individual preference, and share knowledge freely and openly.

## Rationale

A shared commitment to governance principles ensures organizational cohesion and effective collaboration:

- **Governance Legitimacy**: Universal acceptance gives governance decisions proper authority and compliance
- **Process Respect**: Commitment to follow established procedures prevents governance circumvention
- **Constructive Participation**: Agreement to engage positively improves decision quality and team dynamics
- **Collective Priority**: Putting group needs first enables effective organizational decision-making
- **Knowledge Sharing**: Open knowledge exchange accelerates learning and prevents silos
- **Cultural Foundation**: Shared values create the basis for effective teamwork and conflict resolution
- **Onboarding Clarity**: Clear expectations help new contributors understand organizational culture
- **Accountability Framework**: Explicit agreement enables addressing non-compliance constructively

The Binding Oath creates the social contract necessary for effective governance and collaborative success.

## Scope

**Who Must Accept:**
- All Nash Group organization members
- All repository contributors (internal and external)
- All participants in governance processes
- All users of organizational resources and infrastructure

**Oath Components:**
1. **Respect Decision Process**: Follow established governance procedures and authority
2. **Constructive Participation**: Engage positively in debates and decision-making
3. **Accept Council Decisions**: Respect outcomes even when personally disagreeing
4. **Collective Good Priority**: Put organizational needs above individual preferences
5. **Open Knowledge Sharing**: Share information and expertise freely with teammates

**Enforcement Scope:**
- Contribution to any Nash Group repository
- Participation in governance discussions
- Use of organization infrastructure and resources
- Membership in teams and access to privileged information

## Implementation

### Technical Enforcement

Onboarding automation and oath acceptance tracking:

```hcl
# terraform/github/binding_oath.tf
resource "github_repository_file" "contributor_agreement" {
  repository = "the-covenant"
  file       = "CONTRIBUTOR_AGREEMENT.md"
  content = templatefile("${path.module}/templates/contributor-agreement.md", {
    organization = "the-nash-group"
  })
}

# Onboarding workflow
resource "github_repository_file" "onboarding_workflow" {
  repository = ".github"  # Organization-level repository
  file       = ".github/workflows/new-member-onboarding.yml"
  content = templatefile("${path.module}/templates/onboarding-workflow.yml", {
    covenant_repo = "the-covenant"
  })
}

# Organization profile with governance links
resource "github_repository_file" "org_profile" {
  repository = ".github"
  file       = "profile/README.md"
  content = templatefile("${path.module}/templates/org-profile.md", {
    governance_link = "https://github.com/the-nash-group/the-covenant/blob/main/GOVERNANCE.md"
    principles_link = "https://github.com/the-nash-group/the-covenant/blob/main/PRINCIPLES.md"
  })
}

# Repository template with governance reminder
resource "github_repository_file" "repo_template" {
  for_each = var.template_repositories

  repository = each.value
  file       = "GOVERNANCE_NOTICE.md"
  content = templatefile("${path.module}/templates/governance-notice.md", {
    covenant_repo = "the-covenant"
  })
}
```

New member onboarding automation:

```yaml
# .github/workflows/new-member-onboarding.yml
name: New Member Onboarding
on:
  member:
    types: [added]
  membership:
    types: [added]

jobs:
  welcome-new-member:
    runs-on: ubuntu-latest
    steps:
      - name: Create onboarding issue
        uses: actions/github-script@v6
        with:
          script: |
            const newMember = context.payload.member.login;

            await github.rest.issues.create({
              owner: 'the-nash-group',
              repo: 'the-covenant',
              title: `Welcome to The Nash Group - ${newMember}`,
              body: `# Welcome to The Nash Group! 🎉

              Hi @${newMember}! Welcome to our organization. This issue will guide you through our governance and culture.

              ## The Binding Oath

              By joining The Nash Group and contributing to our repositories, you implicitly accept our governance model and agree to:

              - [ ] **Respect the Decision Process**: Follow our established governance procedures and authority structure
              - [ ] **Participate Constructively**: Engage positively in debates and decision-making processes
              - [ ] **Accept Council Decisions**: Respect outcomes of our governance processes, even when personally disagreeing
              - [ ] **Prioritize Collective Good**: Put organizational needs above individual preferences
              - [ ] **Share Knowledge Freely**: Share information and expertise openly with teammates

              ## Required Reading

              Please read and acknowledge understanding of these foundational documents:

              - [ ] [The Covenant - GOVERNANCE.md](./GOVERNANCE.md) - Our governance structure and processes
              - [ ] [The Covenant - PRINCIPLES.md](./PRINCIPLES.md) - Our technical and cultural principles
              - [ ] [The Covenant - HUMAN_MANDATE.md](./HUMAN_MANDATE.md) - The archetypal roles that guide our work

              ## Team Assignment

              - [ ] Add to @the-nash-group/immortals team (all contributors)
              - [ ] Determine appropriate domain/clan assignment if applicable
              - [ ] Grant repository access based on role and responsibilities

              ## Getting Started

              - [ ] Set up development environment following our standards
              - [ ] Join relevant communication channels
              - [ ] Introduce yourself to the team
              - [ ] Find a mentor for guidance and questions

              ## Governance Acknowledgment

              Please comment below with: "I acknowledge and accept The Binding Oath and governance model of The Nash Group."

              Once you've completed the checklist above, this issue will be closed.

              Welcome aboard! 🚀

              /cc @the-nash-group/watchers @the-nash-group/mentors
              `,
              labels: ['onboarding', 'governance', 'new-member'],
              assignees: [newMember, '@the-nash-group/watchers']
            });

      - name: Add to immortals team
        uses: actions/github-script@v6
        with:
          script: |
            const newMember = context.payload.member.login;

            try {
              await github.rest.teams.addOrUpdateMembershipForUserInOrg({
                org: 'the-nash-group',
                team_slug: 'immortals',
                username: newMember,
                role: 'member'
              });

              console.log(`Added ${newMember} to immortals team`);
            } catch (error) {
              console.error(`Failed to add ${newMember} to immortals team:`, error);
            }

  track-oath-acceptance:
    runs-on: ubuntu-latest
    needs: welcome-new-member
    steps:
      - name: Monitor for oath acceptance
        uses: actions/github-script@v6
        with:
          script: |
            // This would be triggered by issue comments
            // Monitor for the acknowledgment phrase in comments
            // Track completion in a governance metrics system
```

### Automated Validation

Oath compliance and participation monitoring:

```python
# scripts/oath-compliance.py
import datetime
import github
from typing import Dict, List, Optional, Set
from dataclasses import dataclass

@dataclass
class MemberOnboarding:
    username: str
    join_date: datetime.datetime
    oath_acknowledged: bool
    onboarding_complete: bool
    mentor_assigned: Optional[str]
    team_assignments: List[str]

@dataclass
class GovernanceParticipation:
    username: str
    pr_reviews_count: int
    governance_comments: int
    conflict_participation: int
    knowledge_sharing_score: float
    compliance_score: float

class BindingOathTracker:
    def __init__(self, org: str):
        self.gh = github.Github()
        self.org = self.gh.get_organization(org)
        self.covenant_repo = self.org.get_repo("the-covenant")

    def track_new_member_onboarding(self, username: str) -> MemberOnboarding:
        """Track new member onboarding progress"""
        # Find onboarding issue for user
        onboarding_issues = self.covenant_repo.get_issues(
            labels=['onboarding', 'new-member'],
            state='all'
        )

        user_onboarding = None
        for issue in onboarding_issues:
            if username in issue.title:
                user_onboarding = issue
                break

        if not user_onboarding:
            return MemberOnboarding(
                username=username,
                join_date=datetime.datetime.now(),
                oath_acknowledged=False,
                onboarding_complete=False,
                mentor_assigned=None,
                team_assignments=[]
            )

        # Check for oath acknowledgment in comments
        oath_acknowledged = False
        comments = user_onboarding.get_comments()
        for comment in comments:
            if (comment.user.login == username and
                "acknowledge and accept The Binding Oath" in comment.body):
                oath_acknowledged = True
                break

        # Check team assignments
        team_assignments = self.get_user_teams(username)

        return MemberOnboarding(
            username=username,
            join_date=user_onboarding.created_at,
            oath_acknowledged=oath_acknowledged,
            onboarding_complete=user_onboarding.state == 'closed',
            mentor_assigned=self.get_assigned_mentor(user_onboarding),
            team_assignments=team_assignments
        )

    def assess_governance_participation(self, username: str,
                                      period_days: int = 90) -> GovernanceParticipation:
        """Assess member's adherence to oath principles"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=period_days)

        # Count PR reviews (constructive participation)
        pr_reviews = self.count_user_pr_reviews(username, cutoff_date)

        # Count governance-related comments
        governance_comments = self.count_governance_comments(username, cutoff_date)

        # Check conflict resolution participation
        conflict_participation = self.count_conflict_participation(username, cutoff_date)

        # Assess knowledge sharing (simplified metric)
        knowledge_sharing_score = self.calculate_knowledge_sharing_score(username, cutoff_date)

        # Calculate overall compliance score
        compliance_score = self.calculate_compliance_score(
            pr_reviews, governance_comments, conflict_participation, knowledge_sharing_score
        )

        return GovernanceParticipation(
            username=username,
            pr_reviews_count=pr_reviews,
            governance_comments=governance_comments,
            conflict_participation=conflict_participation,
            knowledge_sharing_score=knowledge_sharing_score,
            compliance_score=compliance_score
        )

    def calculate_compliance_score(self, pr_reviews: int, governance_comments: int,
                                 conflict_participation: int, knowledge_sharing: float) -> float:
        """Calculate overall oath compliance score (0-100)"""
        # Weighted scoring based on oath components
        weights = {
            'participation': 0.3,  # Constructive participation
            'governance': 0.2,     # Governance engagement
            'conflict': 0.2,       # Conflict resolution participation
            'knowledge': 0.3       # Knowledge sharing
        }

        # Normalize values to 0-100 scale
        participation_score = min(100, pr_reviews * 10)  # 10 reviews = 100 points
        governance_score = min(100, governance_comments * 20)  # 5 comments = 100 points
        conflict_score = min(100, conflict_participation * 50)  # 2 participations = 100 points
        knowledge_score = knowledge_sharing  # Already 0-100

        total_score = (
            participation_score * weights['participation'] +
            governance_score * weights['governance'] +
            conflict_score * weights['conflict'] +
            knowledge_score * weights['knowledge']
        )

        return round(total_score, 2)

    def identify_oath_violations(self) -> List[Dict[str, any]]:
        """Identify potential violations of oath principles"""
        violations = []

        # Check all organization members
        members = self.org.get_members()

        for member in members:
            username = member.login

            # Skip service accounts and bots
            if member.type == 'Bot':
                continue

            participation = self.assess_governance_participation(username)

            # Flag low participation (potential oath violation)
            if participation.compliance_score < 30:
                violations.append({
                    'username': username,
                    'violation_type': 'low_participation',
                    'compliance_score': participation.compliance_score,
                    'details': {
                        'pr_reviews': participation.pr_reviews_count,
                        'governance_comments': participation.governance_comments,
                        'knowledge_sharing': participation.knowledge_sharing_score
                    },
                    'recommendation': 'Reach out for coaching on governance participation'
                })

            # Check for destructive behavior patterns
            destructive_behavior = self.check_destructive_patterns(username)
            if destructive_behavior:
                violations.append({
                    'username': username,
                    'violation_type': 'destructive_behavior',
                    'details': destructive_behavior,
                    'recommendation': 'Council review for oath compliance'
                })

        return violations

    def check_destructive_patterns(self, username: str) -> Optional[Dict[str, any]]:
        """Check for patterns that violate oath principles"""
        # Simplified check - would include:
        # - Consistently blocking without constructive alternatives
        # - Personal attacks or unconstructive criticism
        # - Refusing to accept council decisions
        # - Hoarding knowledge or refusing to help teammates

        # This would analyze comment sentiment, review patterns, etc.
        # For now, return None (no violations detected)
        return None

    def generate_oath_compliance_report(self) -> str:
        """Generate organization-wide oath compliance report"""
        members = list(self.org.get_members())
        total_members = len([m for m in members if m.type != 'Bot'])

        # Assess all members
        compliance_scores = []
        violations = self.identify_oath_violations()

        for member in members:
            if member.type == 'Bot':
                continue

            participation = self.assess_governance_participation(member.login)
            compliance_scores.append(participation.compliance_score)

        avg_compliance = sum(compliance_scores) / len(compliance_scores) if compliance_scores else 0

        report = f"""# Binding Oath Compliance Report

## Organization Overview
- **Total Members**: {total_members}
- **Average Compliance Score**: {avg_compliance:.1f}/100
- **Members with Violations**: {len(violations)}

## Compliance Distribution
- **High Compliance (80-100)**: {sum(1 for s in compliance_scores if s >= 80)}
- **Medium Compliance (50-79)**: {sum(1 for s in compliance_scores if 50 <= s < 80)}
- **Low Compliance (<50)**: {sum(1 for s in compliance_scores if s < 50)}

## Identified Violations
{self.format_violations(violations)}

## Recommendations
- Follow up with low-compliance members for coaching
- Review onboarding process effectiveness
- Consider recognition for high-participation members
- Investigate patterns in violations

## Next Steps
1. Address violations through mentoring
2. Improve governance participation incentives
3. Enhanced onboarding for oath understanding
"""
        return report

    def format_violations(self, violations: List[Dict]) -> str:
        """Format violations for report"""
        if not violations:
            return "No significant violations identified."

        formatted = []
        for violation in violations[:5]:  # Show top 5
            formatted.append(f"- **{violation['username']}**: {violation['violation_type']} (Score: {violation.get('compliance_score', 'N/A')})")

        return "\n".join(formatted)
```

### Human Process

Oath implementation and enforcement:

1. **New Member Onboarding**:
   - Automatic onboarding issue creation upon organization invitation
   - Required reading of governance documents
   - Explicit oath acknowledgment in onboarding issue
   - Mentor assignment for guidance and support

2. **Ongoing Compliance Monitoring**:
   - Quarterly assessment of governance participation
   - Tracking of oath principle adherence through behavior
   - Early intervention for declining participation
   - Recognition for exemplary governance participation

3. **Violation Response Process**:
   - Coaching and mentoring for low participation
   - Council review for serious oath violations
   - Progressive response: guidance → formal discussion → team review
   - Focus on improvement rather than punishment

4. **Cultural Reinforcement**:
   - Regular communication about governance values
   - Recognition of positive governance participation
   - Integration of oath principles into performance discussions
   - Community building around shared governance values

## Compliance Verification

### Automated Checks

- **Onboarding Tracking**: Monitor completion of new member onboarding process
- **Oath Acknowledgment**: Track explicit acceptance in onboarding issues
- **Participation Metrics**: Measure governance engagement and contribution quality
- **Violation Detection**: Automated identification of concerning participation patterns
- **Compliance Scoring**: Regular assessment of oath adherence across organization

### Manual Audits

- **Quarterly Oath Review**: Council assessment of organization-wide compliance
- **Individual Coaching**: One-on-one discussions with low-participation members
- **Cultural Assessment**: Survey organization on governance culture and oath effectiveness

### Reporting

Oath compliance metrics:
- Organization-wide compliance score trends
- New member onboarding completion rates
- Participation levels across different governance activities
- Violation frequency and response effectiveness
- Cultural alignment survey results

## Related Documents

- **Source**: [../the-covenant/GOVERNANCE.md - The Binding Oath](../the-covenant/GOVERNANCE.md#the-binding-oath)
- **Supporting Documents**:
  - [../the-covenant/GOVERNANCE.md](../the-covenant/GOVERNANCE.md) - Complete governance structure
  - [../the-covenant/PRINCIPLES.md](../the-covenant/PRINCIPLES.md) - Organizational principles
  - [../the-covenant/HUMAN_MANDATE.md](../the-covenant/HUMAN_MANDATE.md) - Role archetypes
- **Related Policies**:
  - [GOV-001: Living Principles](./gov-001-living-principles.md)
  - [GOV-007: Governance Review Cycles](./gov-007-review-cycles.md)

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-09-30 | 1.0 | Initial policy creation from GOVERNANCE.md The Binding Oath | Claude Code |
