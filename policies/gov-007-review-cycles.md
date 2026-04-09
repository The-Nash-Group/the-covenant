# GOV-007: Governance Review Cycles

**Policy ID:** GOV-007
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Governance effectiveness **must** be regularly assessed through structured review cycles. Team membership and permissions **shall** be reviewed quarterly, governance process effectiveness **must** be assessed bi-annually, and the complete Covenant **shall** undergo annual review and refresh. All reviews **must** include metrics tracking and improvement recommendations.

## Rationale

Regular governance review ensures continuous improvement and adaptation to organizational needs:

- **Process Evolution**: Regular assessment identifies inefficiencies and improvement opportunities
- **Team Alignment**: Quarterly reviews ensure team membership matches current roles and responsibilities
- **Permission Hygiene**: Regular access reviews prevent permission creep and security risks
- **Effectiveness Measurement**: Metrics tracking reveals governance bottlenecks and successes
- **Stakeholder Feedback**: Structured reviews capture input from all organizational levels
- **Adaptation Capability**: Bi-annual assessments allow governance to evolve with organizational growth
- **Constitutional Maintenance**: Annual Covenant review ensures principles remain relevant and effective
- **Continuous Learning**: Review cycles institutionalize organizational learning and improvement

Structured review cycles prevent governance stagnation and ensure processes serve the organization effectively.

## Scope

**Review Cycles:**
- **Quarterly**: Team membership, permissions, immediate process issues
- **Bi-Annual**: Governance effectiveness, decision metrics, process improvements
- **Annual**: Complete Covenant review, principle relevance, major governance updates

**Review Coverage:**
- Team composition and role alignment
- Permission and access level appropriateness
- Decision-making process efficiency
- Conflict resolution effectiveness
- Emergency procedure usage and outcomes
- Governance participation rates and satisfaction

**Stakeholder Participation:**
- All team members provide input on governance effectiveness
- Council members assess decision quality and process efficiency
- Watchers evaluate overall organizational governance health

## Implementation

### Technical Enforcement

Automated review scheduling and tracking:

```hcl
# terraform/github/review_cycles.tf
resource "github_repository_file" "review_automation" {
  repository = "the-covenant"
  file       = ".github/workflows/governance-reviews.yml"
  content = templatefile("${path.module}/templates/review-automation.yml", {
    organization = "the-nash-group"
  })
}

# Review issue templates
resource "github_repository_file" "quarterly_review_template" {
  repository = "the-covenant"
  file       = ".github/ISSUE_TEMPLATE/quarterly-review.yml"
  content = templatefile("${path.module}/templates/quarterly-review.yml", {})
}

resource "github_repository_file" "biannual_review_template" {
  repository = "the-covenant"
  file       = ".github/ISSUE_TEMPLATE/biannual-review.yml"
  content = templatefile("${path.module}/templates/biannual-review.yml", {})
}

resource "github_repository_file" "annual_review_template" {
  repository = "the-covenant"
  file       = ".github/ISSUE_TEMPLATE/annual-review.yml"
  content = templatefile("${path.module}/templates/annual-review.yml", {})
}

# Review metrics dashboard
resource "github_repository_file" "review_dashboard" {
  repository = "the-covenant"
  file       = "REFERENCE/governance-metrics/README.md"
  content = templatefile("${path.module}/templates/governance-dashboard.md", {})
}
```

Automated review scheduling workflow:

```yaml
# .github/workflows/governance-reviews.yml
name: Governance Review Cycles
on:
  schedule:
    # Quarterly reviews (every 3 months on 1st)
    - cron: '0 9 1 */3 *'
    # Bi-annual assessment (January 1st and July 1st)
    - cron: '0 9 1 1,7 *'
    # Annual review (January 1st)
    - cron: '0 9 1 1 *'
  workflow_dispatch:
    inputs:
      review_type:
        description: 'Type of review to create'
        required: true
        type: choice
        options:
          - quarterly
          - biannual
          - annual

jobs:
  create-quarterly-review:
    if: contains(github.event.schedule, '*/3') || github.event.inputs.review_type == 'quarterly'
    runs-on: ubuntu-latest
    steps:
      - name: Create quarterly review issue
        uses: actions/github-script@v6
        with:
          script: |
            const now = new Date();
            const quarter = Math.floor((now.getMonth() + 3) / 3);
            const year = now.getFullYear();

            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `Q${quarter} ${year} Governance Review - Team & Permissions`,
              body: `# Quarterly Governance Review

              **Review Period**: Q${quarter} ${year}
              **Due Date**: ${new Date(now.getTime() + 14*24*60*60*1000).toISOString().split('T')[0]}

              ## Team Membership Review
              - [ ] Review @the-nash-group/immortals membership
              - [ ] Review @the-nash-group/mentors assignments
              - [ ] Review @the-nash-group/watchers composition
              - [ ] Review @the-nash-group/platform-clan alignment

              ## Permission Audit
              - [ ] Validate repository access levels
              - [ ] Check CODEOWNERS file accuracy
              - [ ] Review organization admin privileges
              - [ ] Audit third-party integrations

              ## Process Health Check
              - [ ] Review recent conflict resolutions
              - [ ] Analyze decision times and bottlenecks
              - [ ] Check emergency procedure usage
              - [ ] Evaluate participation rates

              ## Action Items
              <!-- To be filled during review -->

              **Assigned to**: @the-nash-group/watchers
              `,
              labels: ['governance', 'quarterly-review', 'high-priority'],
              assignees: ['@the-nash-group/watchers']
            });

  create-biannual-assessment:
    if: contains(github.event.schedule, '1,7') || github.event.inputs.review_type == 'biannual'
    runs-on: ubuntu-latest
    steps:
      - name: Generate governance metrics
        run: |
          # Collect metrics from the past 6 months
          python scripts/governance-metrics.py --period=6months > /tmp/metrics.json

      - name: Create biannual assessment issue
        uses: actions/github-script@v6
        with:
          script: |
            const now = new Date();
            const period = now.getMonth() < 6 ? 'H1' : 'H2';
            const year = now.getFullYear();

            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `${period} ${year} Governance Effectiveness Assessment`,
              body: `# Bi-Annual Governance Assessment

              **Assessment Period**: ${period} ${year}
              **Review Deadline**: ${new Date(now.getTime() + 21*24*60*60*1000).toISOString().split('T')[0]}

              ## Governance Metrics Review
              - [ ] Decision time analysis
              - [ ] Participation rate assessment
              - [ ] Conflict resolution effectiveness
              - [ ] Emergency procedure review
              - [ ] Amendment process evaluation

              ## Process Effectiveness
              - [ ] Team authority matrix functioning
              - [ ] Council quorum operations
              - [ ] Escalation path efficiency
              - [ ] Documentation quality

              ## Stakeholder Feedback
              - [ ] Survey all Immortals on governance satisfaction
              - [ ] Collect Mentor feedback on decision processes
              - [ ] Gather Watcher input on organizational health

              ## Improvement Recommendations
              <!-- To be filled during assessment -->

              **Assigned to**: @the-nash-group/watchers @the-nash-group/mentors
              `,
              labels: ['governance', 'biannual-assessment', 'critical'],
              assignees: ['@the-nash-group/watchers']
            });

  create-annual-review:
    if: contains(github.event.schedule, '1 1') || github.event.inputs.review_type == 'annual'
    runs-on: ubuntu-latest
    steps:
      - name: Create annual Covenant review
        uses: actions/github-script@v6
        with:
          script: |
            const year = new Date().getFullYear();

            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `${year} Annual Covenant Review & Refresh`,
              body: `# Annual Covenant Review

              **Review Year**: ${year}
              **Completion Deadline**: ${new Date().getFullYear()}-02-28

              ## Principle Relevance Assessment
              - [ ] Review all principles in PRINCIPLES.md
              - [ ] Assess current relevance and effectiveness
              - [ ] Identify outdated or ineffective principles
              - [ ] Propose new principles based on learning

              ## Governance Structure Evaluation
              - [ ] Review team hierarchy effectiveness
              - [ ] Assess authority distribution
              - [ ] Evaluate decision-making processes
              - [ ] Review conflict resolution mechanisms

              ## Cultural Alignment Check
              - [ ] Survey organization on values alignment
              - [ ] Assess principle implementation in daily work
              - [ ] Review onboarding effectiveness
              - [ ] Evaluate cultural evolution needs

              ## Major Governance Updates
              - [ ] Propose structural improvements
              - [ ] Update role definitions if needed
              - [ ] Revise process documentation
              - [ ] Plan implementation of changes

              ## Implementation Planning
              <!-- Major changes requiring implementation -->

              **Assigned to**: @the-nash-group/watchers
              **Stakeholders**: All organization members
              `,
              labels: ['governance', 'annual-review', 'strategic'],
              assignees: ['@the-nash-group/watchers']
            });
```

### Automated Validation

Governance metrics collection and analysis:

```python
# scripts/governance-metrics.py
import datetime
import github
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class GovernanceMetrics:
    period: str
    team_metrics: Dict[str, Any]
    decision_metrics: Dict[str, Any]
    conflict_metrics: Dict[str, Any]
    participation_metrics: Dict[str, Any]
    emergency_metrics: Dict[str, Any]

class GovernanceReviewTracker:
    def __init__(self, org: str):
        self.gh = github.Github()
        self.org = self.gh.get_organization(org)
        self.covenant_repo = self.org.get_repo("the-covenant")

    def collect_quarterly_metrics(self) -> GovernanceMetrics:
        """Collect metrics for quarterly review"""
        now = datetime.datetime.now()
        three_months_ago = now - datetime.timedelta(days=90)

        return GovernanceMetrics(
            period=f"Q{(now.month-1)//3 + 1} {now.year}",
            team_metrics=self.get_team_metrics(),
            decision_metrics=self.get_decision_metrics(three_months_ago),
            conflict_metrics=self.get_conflict_metrics(three_months_ago),
            participation_metrics=self.get_participation_metrics(three_months_ago),
            emergency_metrics=self.get_emergency_metrics(three_months_ago)
        )

    def get_team_metrics(self) -> Dict[str, Any]:
        """Analyze team composition and changes"""
        teams = ['immortals', 'mentors', 'watchers', 'platform-clan']
        metrics = {}

        for team_name in teams:
            try:
                team = self.org.get_team_by_slug(team_name)
                members = list(team.get_members())

                metrics[team_name] = {
                    "member_count": len(members),
                    "recent_additions": self.get_recent_team_additions(team),
                    "recent_removals": self.get_recent_team_removals(team),
                    "inactive_members": self.identify_inactive_members(members)
                }
            except github.UnknownObjectException:
                metrics[team_name] = {"error": "Team not found"}

        return metrics

    def get_decision_metrics(self, since: datetime.datetime) -> Dict[str, Any]:
        """Track decision-making effectiveness"""
        # Get all PRs merged since the date
        prs = self.covenant_repo.get_pulls(
            state='closed',
            sort='updated',
            direction='desc'
        )

        recent_prs = [pr for pr in prs if pr.merged_at and pr.merged_at >= since]

        decision_times = []
        approval_counts = []
        consensus_failures = 0

        for pr in recent_prs:
            if pr.created_at and pr.merged_at:
                decision_time = (pr.merged_at - pr.created_at).total_seconds() / 3600
                decision_times.append(decision_time)

            # Count approvals
            reviews = pr.get_reviews()
            approvals = [r for r in reviews if r.state == "APPROVED"]
            approval_counts.append(len(approvals))

            # Check for consensus issues
            blocking_reviews = [r for r in reviews if r.state == "CHANGES_REQUESTED"]
            if blocking_reviews:
                consensus_failures += 1

        return {
            "total_decisions": len(recent_prs),
            "avg_decision_time_hours": sum(decision_times) / len(decision_times) if decision_times else 0,
            "avg_approvals_per_decision": sum(approval_counts) / len(approval_counts) if approval_counts else 0,
            "consensus_failure_rate": consensus_failures / len(recent_prs) if recent_prs else 0,
            "decisions_per_month": len(recent_prs) / 3  # 3 month period
        }

    def get_conflict_metrics(self, since: datetime.datetime) -> Dict[str, Any]:
        """Track conflict resolution effectiveness"""
        conflicts = self.covenant_repo.get_issues(
            labels=['conflict'],
            since=since,
            state='all'
        )

        conflict_list = list(conflicts)
        resolved_conflicts = [c for c in conflict_list if c.state == 'closed']

        if not conflict_list:
            return {"total_conflicts": 0}

        resolution_times = []
        escalation_count = 0

        for conflict in resolved_conflicts:
            if conflict.closed_at and conflict.created_at:
                resolution_time = (conflict.closed_at - conflict.created_at).total_seconds() / 3600
                resolution_times.append(resolution_time)

            # Check for escalations
            labels = [label.name for label in conflict.labels]
            if any(label.startswith('escalation/') for label in labels):
                escalation_count += 1

        return {
            "total_conflicts": len(conflict_list),
            "resolved_conflicts": len(resolved_conflicts),
            "resolution_rate": len(resolved_conflicts) / len(conflict_list),
            "avg_resolution_time_hours": sum(resolution_times) / len(resolution_times) if resolution_times else 0,
            "escalation_rate": escalation_count / len(conflict_list) if conflict_list else 0
        }

    def get_participation_metrics(self, since: datetime.datetime) -> Dict[str, Any]:
        """Measure governance participation"""
        # Simplified participation tracking
        # In practice, would track PR reviews, issue comments, team discussions

        recent_issues = self.covenant_repo.get_issues(
            since=since,
            state='all'
        )

        participants = set()
        total_comments = 0

        for issue in recent_issues:
            participants.add(issue.user.login)
            comments = issue.get_comments()
            for comment in comments:
                participants.add(comment.user.login)
                total_comments += 1

        return {
            "unique_participants": len(participants),
            "total_governance_comments": total_comments,
            "avg_comments_per_participant": total_comments / len(participants) if participants else 0,
            "governance_engagement_rate": len(participants) / self.get_total_org_members()
        }

    def get_emergency_metrics(self, since: datetime.datetime) -> Dict[str, Any]:
        """Track emergency procedure usage"""
        emergency_issues = self.covenant_repo.get_issues(
            labels=['emergency'],
            since=since,
            state='all'
        )

        emergency_list = list(emergency_issues)
        documentation_complete = 0
        postmortems_complete = 0

        for emergency in emergency_list:
            # Check if documentation was completed within 24 hours
            # Simplified check - would verify actual documentation
            labels = [label.name for label in emergency.labels]
            if 'documentation-complete' in labels:
                documentation_complete += 1
            if 'postmortem-complete' in labels:
                postmortems_complete += 1

        return {
            "total_emergencies": len(emergency_list),
            "documentation_compliance_rate": documentation_complete / len(emergency_list) if emergency_list else 1,
            "postmortem_completion_rate": postmortems_complete / len(emergency_list) if emergency_list else 1,
            "emergency_frequency_per_month": len(emergency_list) / 3
        }

    def generate_review_recommendations(self, metrics: GovernanceMetrics) -> List[str]:
        """Generate improvement recommendations based on metrics"""
        recommendations = []

        # Decision time recommendations
        if metrics.decision_metrics.get("avg_decision_time_hours", 0) > 168:  # 1 week
            recommendations.append("Consider streamlining decision process - average decision time exceeds 1 week")

        # Participation recommendations
        if metrics.participation_metrics.get("governance_engagement_rate", 0) < 0.5:
            recommendations.append("Low governance engagement - consider improving communication and participation incentives")

        # Conflict resolution recommendations
        if metrics.conflict_metrics.get("escalation_rate", 0) > 0.3:
            recommendations.append("High conflict escalation rate - review initial resolution processes")

        # Emergency procedure recommendations
        if metrics.emergency_metrics.get("documentation_compliance_rate", 1) < 0.8:
            recommendations.append("Emergency documentation compliance below 80% - strengthen documentation requirements")

        return recommendations

    def export_metrics_report(self, metrics: GovernanceMetrics, recommendations: List[str]) -> str:
        """Export metrics as formatted report"""
        report = f"""# Governance Review Report - {metrics.period}

## Executive Summary

This report covers governance effectiveness for {metrics.period}.

## Team Metrics
{json.dumps(metrics.team_metrics, indent=2)}

## Decision Making Effectiveness
{json.dumps(metrics.decision_metrics, indent=2)}

## Conflict Resolution
{json.dumps(metrics.conflict_metrics, indent=2)}

## Participation Analysis
{json.dumps(metrics.participation_metrics, indent=2)}

## Emergency Procedures
{json.dumps(metrics.emergency_metrics, indent=2)}

## Recommendations

{chr(10).join(f"- {rec}" for rec in recommendations)}

## Next Steps

Based on this analysis, the following actions are recommended:
1. Address high-priority recommendations above
2. Plan implementation for next quarter
3. Schedule follow-up review to track improvements
"""
        return report
```

### Human Process

Review cycle execution:

1. **Quarterly Review Process**:
   - Automated issue creation with checklist
   - Watchers lead team membership and permission review
   - 2-week completion timeline
   - Focus on operational governance issues

2. **Bi-Annual Assessment**:
   - Comprehensive metrics analysis
   - Stakeholder survey and feedback collection
   - Process effectiveness evaluation
   - 3-week completion timeline
   - Council-level review and approval

3. **Annual Covenant Review**:
   - Strategic governance assessment
   - Complete principle relevance review
   - Cultural alignment evaluation
   - Major governance structure updates
   - 8-week completion timeline
   - Organization-wide participation

4. **Review Documentation**:
   - All findings documented in governance repository
   - Action items tracked with deadlines
   - Improvement recommendations prioritized
   - Implementation plans created for major changes

## Compliance Verification

### Automated Checks

- **Review Scheduling**: Calendar-based issue creation for all review cycles
- **Metrics Collection**: Automated governance metrics gathering and analysis
- **Completion Tracking**: Monitor review issue status and deadlines
- **Participation Monitoring**: Track stakeholder engagement in reviews
- **Action Item Follow-up**: Automated reminders for improvement implementations

### Manual Audits

- **Review Quality Assessment**: Evaluate thoroughness and usefulness of reviews
- **Implementation Verification**: Confirm approved improvements are implemented
- **Stakeholder Satisfaction**: Survey participants on review process effectiveness

### Reporting

Review cycle metrics:
- Review completion rates and timeliness
- Participation levels across different cycles
- Implementation rate of review recommendations
- Governance health trends over time
- Stakeholder satisfaction with review process

## Related Documents

- **Source**: [../the-covenant/GOVERNANCE.md - Evolution and Adaptation](../the-covenant/GOVERNANCE.md#evolution-and-adaptation)
- **Related Policies**:
  - [GOV-001: Living Principles](./gov-001-living-principles.md)
  - [GOV-002: Covenant Amendment Process](./gov-002-amendment-process.md)
- **Metrics Dashboard**: [REFERENCE/governance-metrics/](../REFERENCE/governance-metrics/)

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-09-30 | 1.0 | Initial policy creation from GOVERNANCE.md Evolution and Adaptation | Claude Code |
