# GOV-005: Conflict Resolution Process

**Policy ID:** GOV-005
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Conflicts **must** follow the established escalation path. Technical disagreements **shall** be resolved by relevant Mentors, cross-clan disputes **must** escalate to the Council of Mentors, and governance conflicts **shall** be arbitrated by Watchers. All decisions **must** be backed by data over opinion and prioritize user benefit over developer preference.

## Rationale

Structured conflict resolution prevents disputes from blocking progress and ensures appropriate expertise resolves different types of conflicts:

- **Clear Escalation Path**: Eliminates confusion about who resolves which types of conflicts
- **Expertise Matching**: Technical experts resolve technical issues, governance experts handle governance
- **Prevent Gridlock**: Conflicts don't indefinitely block progress or team effectiveness
- **Fair Process**: Systematic approach ensures all perspectives are heard and considered
- **Data-Driven Decisions**: Objective criteria prevent personality-based or political resolutions
- **User Focus**: Ultimate arbitration principle keeps user needs as primary consideration
- **Relationship Preservation**: Structured process maintains team cohesion through disagreements
- **Learning Integration**: Conflict patterns inform improvements to processes and communication

The escalation path ensures conflicts are resolved by appropriate authority with clear principles guiding resolution.

## Scope

**Conflict Types:**
- **Technical Disagreements**: Architecture, implementation approaches, code quality standards
- **Cross-Clan Disputes**: Territory boundaries, resource allocation, priority conflicts
- **Governance Conflicts**: Process interpretation, authority boundaries, policy violations
- **Constitutional Crises**: Fundamental disagreements about organizational principles

**Resolution Authority:**
- **Technical**: Relevant domain Mentors
- **Cross-Clan**: Council of Mentors (multi-domain)
- **Governance**: Watchers arbitration
- **Constitutional**: Unanimous Watcher consensus

**Escalation Triggers:**
- Initial resolution attempt fails
- Conflict involves multiple domains
- Authority boundary disputes
- Process violation allegations

## Implementation

### Technical Enforcement

GitHub issue tracking and escalation automation:

```hcl
# terraform/github/conflict_resolution.tf
resource "github_repository_file" "conflict_templates" {
  repository = "the-covenant"
  file       = ".github/ISSUE_TEMPLATE/conflict-resolution.yml"
  content = templatefile("${path.module}/templates/conflict-template.yml", {
    mentors_team  = "the-nash-group/mentors"
    watchers_team = "the-nash-group/watchers"
  })
}

# Automated escalation workflow
resource "github_repository_file" "escalation_workflow" {
  repository = "the-covenant"
  file       = ".github/workflows/conflict-escalation.yml"
  content = templatefile("${path.module}/templates/escalation-workflow.yml", {
    organization = "the-nash-group"
  })
}

# Conflict tracking labels
resource "github_issue_label" "conflict_labels" {
  for_each = {
    "conflict/technical"      = { color = "FF6B6B", description = "Technical disagreement requiring Mentor resolution" }
    "conflict/cross-clan"     = { color = "FFA500", description = "Multi-domain dispute requiring Council" }
    "conflict/governance"     = { color = "FF0000", description = "Governance issue requiring Watcher arbitration" }
    "conflict/constitutional" = { color = "8B0000", description = "Constitutional crisis requiring unanimous Watchers" }
    "escalation/level-1"      = { color = "FFFF00", description = "First level escalation" }
    "escalation/level-2"      = { color = "FF8C00", description = "Council escalation" }
    "escalation/level-3"      = { color = "DC143C", description = "Watcher arbitration" }
    "resolution/pending"      = { color = "87CEEB", description = "Awaiting resolution decision" }
    "resolution/complete"     = { color = "90EE90", description = "Conflict resolved" }
  }

  repository = "the-covenant"
  name       = each.key
  color      = each.value.color
  description = each.value.description
}
```

Escalation workflow automation:

```yaml
# .github/workflows/conflict-escalation.yml
name: Conflict Escalation Management
on:
  issues:
    types: [opened, labeled, commented]
  schedule:
    - cron: '0 9 * * *'  # Daily escalation check

jobs:
  classify-conflict:
    if: github.event.action == 'opened' && contains(github.event.issue.title, '[CONFLICT]')
    runs-on: ubuntu-latest
    steps:
      - name: Auto-classify conflict type
        uses: actions/github-script@v6
        with:
          script: |
            const title = context.payload.issue.title.toLowerCase();
            const body = context.payload.issue.body.toLowerCase();

            let conflictType = 'conflict/technical';  // default
            let assignees = ['@the-nash-group/mentors'];

            if (body.includes('governance') || body.includes('process')) {
              conflictType = 'conflict/governance';
              assignees = ['@the-nash-group/watchers'];
            } else if (body.includes('cross-clan') || body.includes('territory')) {
              conflictType = 'conflict/cross-clan';
              assignees = ['@the-nash-group/mentors'];
            } else if (body.includes('constitutional') || body.includes('principles')) {
              conflictType = 'conflict/constitutional';
              assignees = ['@the-nash-group/watchers'];
            }

            // Add appropriate labels
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: [conflictType, 'resolution/pending']
            });

  check-escalation-timers:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - name: Check for stale conflicts needing escalation
        uses: actions/github-script@v6
        with:
          script: |
            const issues = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              labels: 'resolution/pending',
              state: 'open'
            });

            const now = new Date();

            for (const issue of issues.data) {
              const created = new Date(issue.created_at);
              const ageHours = (now - created) / (1000 * 60 * 60);

              // Escalate if unresolved after 72 hours
              if (ageHours > 72) {
                await escalateConflict(issue);
              }
            }

  track-resolution:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - name: Record resolution metrics
        run: |
          # Log resolution time and method
          echo "Conflict resolved: ${{ github.event.issue.number }}"
          # Add to resolution metrics dashboard
```

### Automated Validation

Conflict tracking and resolution monitoring:

```python
# scripts/conflict-tracker.py
import datetime
import github
from typing import Dict, List, Optional
from enum import Enum

class ConflictType(Enum):
    TECHNICAL = "technical"
    CROSS_CLAN = "cross_clan"
    GOVERNANCE = "governance"
    CONSTITUTIONAL = "constitutional"

class EscalationLevel(Enum):
    LEVEL_1 = 1  # Initial domain resolution
    LEVEL_2 = 2  # Council escalation
    LEVEL_3 = 3  # Watcher arbitration

class ConflictResolver:
    def __init__(self, org: str):
        self.gh = github.Github()
        self.org = self.gh.get_organization(org)
        self.covenant_repo = self.org.get_repo("the-covenant")

    def classify_conflict(self, issue_body: str, participants: List[str]) -> ConflictType:
        """Automatically classify conflict type based on content and participants"""
        body_lower = issue_body.lower()

        # Check for governance keywords
        if any(word in body_lower for word in ['governance', 'process', 'authority', 'policy']):
            return ConflictType.GOVERNANCE

        # Check for constitutional keywords
        if any(word in body_lower for word in ['principles', 'constitutional', 'fundamental']):
            return ConflictType.CONSTITUTIONAL

        # Check for cross-clan indicators
        participant_teams = [self.get_user_primary_team(user) for user in participants]
        if len(set(participant_teams)) > 1:
            return ConflictType.CROSS_CLAN

        return ConflictType.TECHNICAL

    def determine_resolution_authority(self, conflict_type: ConflictType,
                                     escalation_level: EscalationLevel) -> List[str]:
        """Determine who has authority to resolve this conflict"""
        if conflict_type == ConflictType.TECHNICAL:
            if escalation_level == EscalationLevel.LEVEL_1:
                return ["mentors"]  # Domain mentors
            else:
                return ["mentors"]  # Mentor council

        elif conflict_type == ConflictType.CROSS_CLAN:
            return ["mentors"]  # Council of Mentors

        elif conflict_type == ConflictType.GOVERNANCE:
            return ["watchers"]  # Watcher arbitration

        elif conflict_type == ConflictType.CONSTITUTIONAL:
            return ["watchers"]  # Unanimous Watcher consensus

        return []

    def track_resolution_metrics(self) -> Dict[str, float]:
        """Track conflict resolution effectiveness"""
        conflicts = self.covenant_repo.get_issues(labels=["conflict"])

        metrics = {
            "total_conflicts": len(list(conflicts)),
            "avg_resolution_time": 0,
            "escalation_rate": 0,
            "resolution_rate": 0
        }

        resolved_conflicts = [issue for issue in conflicts if issue.state == "closed"]

        if resolved_conflicts:
            resolution_times = []
            escalations = 0

            for issue in resolved_conflicts:
                # Calculate resolution time
                created = issue.created_at
                closed = issue.closed_at
                if closed:
                    hours = (closed - created).total_seconds() / 3600
                    resolution_times.append(hours)

                # Check if escalated
                labels = [label.name for label in issue.labels]
                if any(label.startswith("escalation/") for label in labels):
                    escalations += 1

            metrics.update({
                "avg_resolution_time": sum(resolution_times) / len(resolution_times),
                "escalation_rate": escalations / len(resolved_conflicts),
                "resolution_rate": len(resolved_conflicts) / len(list(conflicts))
            })

        return metrics

    def apply_resolution_principles(self, conflict_data: Dict) -> Dict[str, str]:
        """Apply the four principles of resolution to conflict data"""
        principles = {
            "data_over_opinion": "Evaluate based on metrics, user feedback, and evidence",
            "user_over_developer": "Prioritize user experience and business value",
            "simple_over_complex": "Choose the solution with lower complexity and maintenance",
            "covenant_over_convention": "Follow established principles and governance"
        }

        recommendations = {}
        for principle, description in principles.items():
            recommendations[principle] = self.evaluate_principle(conflict_data, principle)

        return recommendations
```

### Human Process

Conflict resolution procedure:

1. **Conflict Identification**:
   - Create issue with `[CONFLICT]` prefix in the-covenant repository
   - Use conflict resolution template to document:
     - Parties involved
     - Nature of disagreement
     - Attempted resolutions
     - Requested arbitration

2. **Initial Resolution (Level 1)**:
   - **Technical Conflicts**: Assigned to relevant domain Mentors
   - **Cross-Clan Issues**: Assigned to Council of Mentors
   - **Governance Issues**: Assigned to Watchers
   - 72-hour resolution target

3. **Escalation (Level 2)**:
   - Triggered if initial resolution fails or is disputed
   - Technical → Council of Mentors
   - Cross-Clan → Full Council review
   - Governance → Watcher panel

4. **Final Arbitration (Level 3)**:
   - Constitutional issues → Unanimous Watcher consensus
   - Apply resolution principles in order:
     - Data over opinion
     - User over developer
     - Simple over complex
     - Covenant over convention

5. **Resolution Documentation**:
   - Record final decision with rationale
   - Update relevant documentation or processes
   - Communicate decision to all affected parties
   - Add to decision log for future reference

## Compliance Verification

### Automated Checks

- **Conflict Classification**: Auto-tagging based on issue content and participants
- **Escalation Timers**: Automatic escalation after 72-hour resolution window
- **Authority Validation**: Verify resolvers have appropriate team membership
- **Resolution Tracking**: Metrics on resolution time and escalation frequency
- **Documentation Requirements**: Ensure resolution rationale is recorded

### Manual Audits

- **Monthly Conflict Review**: Analyze conflict patterns and resolution effectiveness
- **Quarterly Process Assessment**: Evaluate escalation path efficiency
- **Annual Resolution Training**: Ensure team understands conflict resolution procedures

### Reporting

Conflict resolution metrics:
- Number of conflicts by type and month
- Average resolution time by escalation level
- Escalation rate and patterns
- Resolution satisfaction surveys
- Repeat conflict analysis
- Authority boundary clarification needs

## Related Documents

- **Source**: [../the-covenant/GOVERNANCE.md - Conflict Resolution](../the-covenant/GOVERNANCE.md#conflict-resolution)
- **Related Policies**:
  - [GOV-004: Team Authority Matrix](./gov-004-team-authority.md)
  - [GOV-006: Council Decision Quorum](./gov-006-decision-quorum.md)
- **Templates**: [.github/ISSUE_TEMPLATE/conflict-resolution.yml](../.github/ISSUE_TEMPLATE/conflict-resolution.yml)

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-09-30 | 1.0 | Initial policy creation from GOVERNANCE.md Conflict Resolution | Claude Code |
