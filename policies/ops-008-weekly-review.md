# OPS-008: Weekly Review Process

**Policy ID:** OPS-008
**Category:** Operations
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Teams **must** conduct weekly reviews to assess Human/Machine boundary maintenance, identify automation opportunities, and prioritize manual work elimination. These reviews **shall** follow the three-question assessment: "Are we maintaining the Human/Machine boundary?", "What manual work should be automated?", and "What automated processes need human oversight?" The review **must** produce actionable automation backlog items.

## Rationale

From The Human Mandate's Weekly Review: "Teams should collectively assess: 1. Are we maintaining the Human/Machine boundary? 2. What manual work should be automated? 3. What automated processes need human oversight?"

The Human/Machine boundary requires continuous team-level evaluation and adjustment:

- **Boundary Drift**: Without regular assessment, teams gradually drift toward either over-automation or under-automation
- **Toil Accumulation**: Manual processes compound weekly without systematic identification and elimination
- **Automation Gaps**: New manual work emerges faster than ad-hoc automation efforts can address
- **Oversight Requirements**: Automated systems require evolving human oversight as they mature and change
- **Team Learning**: Collective boundary assessment builds shared understanding better than individual reflection
- **Cultural Reinforcement**: Weekly rituals embed Human/Machine consciousness into team operations

This weekly process ensures teams systematically evolve their Human/Machine boundary rather than allowing it to drift through inattention.

## Scope

**Applies To:**
- All teams with infrastructure, development, or operational responsibilities
- All automated processes requiring human oversight or judgment
- All manual processes potentially suitable for automation
- All team workflows and operational procedures

**Review Boundaries:**
- Team processes: Collective boundary assessment and automation planning
- Individual workflows: Personal automation opportunities and toil identification
- Organizational systems: Cross-team automation coordination and oversight requirements

## Implementation

### Technical Enforcement

Weekly review automation with metrics collection:

```bash
#!/bin/bash
# scripts/weekly-boundary-review.sh
# ROLE: Gardener - Systematizing weekly cultural practices

TEAM_NAME=${1:-$(git config nash.team)}
REVIEW_DATE=$(date -I)

echo "=== Weekly Human/Machine Boundary Review ==="
echo "Team: $TEAM_NAME"
echo "Date: $REVIEW_DATE"
echo

# Question 1: Boundary maintenance
echo "1. Are we maintaining the Human/Machine boundary?"
echo "   Review this week's work distribution:"

# Analyze recent commits for automation vs manual work indicators
git log --since="1 week ago" --oneline --grep="ROLE:" | \
awk '{
  if ($0 ~ /automate|automation|bot|script/) automation++
  if ($0 ~ /manual|fix|hotfix|emergency/) manual++
}
END {
  total = automation + manual
  if (total > 0) {
    printf "   Automation work: %d commits (%.1f%%)\n", automation, automation*100/total
    printf "   Manual work: %d commits (%.1f%%)\n", manual, manual*100/total
  }
}'

# Question 2: Automation opportunities
echo
echo "2. What manual work should be automated?"
echo "   Scanning for toil indicators..."

# Check for repeated manual patterns
grep -r "TODO.*automate\|FIXME.*manual\|NOTE.*repetitive" . 2>/dev/null | \
head -5 | sed 's/^/   Found: /'

# Question 3: Oversight requirements
echo
echo "3. What automated processes need human oversight?"
echo "   Checking automation health..."

# Check for automation failures or warnings
if command -v terraform >/dev/null; then
  echo "   Terraform state health: $(terraform show -json 2>/dev/null | jq -r '.values.root_module.resources | length') resources managed"
fi

if command -v gh >/dev/null; then
  echo "   GitHub automation status: $(gh api /repos/:owner/:repo/actions/runs --jq '[.workflow_runs[0:5] | .[] | select(.conclusion != "success")] | length') recent failures"
fi

echo
echo "=== Action Items ==="
echo "Enter automation backlog items (one per line, empty line to finish):"

# Collect action items
action_items=()
while read -r line; do
  [[ -z "$line" ]] && break
  action_items+=("$line")
done

# Save review results
review_data=$(jq -n \
  --arg team "$TEAM_NAME" \
  --arg date "$REVIEW_DATE" \
  --argjson items "$(printf '%s\n' "${action_items[@]}" | jq -R . | jq -s .)" \
  '{
    team: $team,
    date: $date,
    action_items: $items,
    completed: true
  }')

# Submit to metrics system
curl -X POST "https://metrics.nashgroup.internal/weekly-reviews" \
  -H "Content-Type: application/json" \
  -d "$review_data"

echo "Review completed and logged. Action items added to automation backlog."
```

GitHub Issues automation for backlog management:

```yaml
# .github/workflows/weekly-review-automation.yml
name: Weekly Review Automation
on:
  schedule:
    - cron: '0 9 * * 1'  # Mondays at 9 AM
  workflow_dispatch:

jobs:
  create-review-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Create Weekly Review Issue
        run: |
          ISSUE_BODY=$(cat <<EOF
          # Weekly Human/Machine Boundary Review

          **Review Date:** $(date -I)
          **Team:** @the-nash-group/$(echo $GITHUB_REPOSITORY | cut -d'/' -f2)

          ## Assessment Questions

          ### 1. Are we maintaining the Human/Machine boundary?
          - [ ] Review work distribution from past week
          - [ ] Identify boundary violations or drift
          - [ ] Assess role clarity in recent decisions

          ### 2. What manual work should be automated?
          - [ ] Scan for repeated manual tasks
          - [ ] Identify toil-generating processes
          - [ ] Prioritize automation opportunities

          ### 3. What automated processes need human oversight?
          - [ ] Review automation failures and alerts
          - [ ] Assess oversight adequacy
          - [ ] Update human checkpoints as needed

          ## Action Items
          <!-- Add automation backlog items here -->

          ## Metrics
          - Automation work: _% of commits
          - Manual work: _% of commits
          - New toil identified: _ items
          - Automation candidates: _ items

          /label weekly-review automation boundary
          EOF
          )

          gh issue create \
            --title "Weekly Review: $(date -I)" \
            --body "$ISSUE_BODY" \
            --label "weekly-review,automation,boundary"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Automated Validation

Automation backlog tracking:

```python
# scripts/automation-backlog-tracker.py
# ROLE: Gardener - Tracking automation opportunities and progress

import json
import requests
from datetime import datetime, timedelta

class AutomationBacklogTracker:
    def __init__(self, metrics_url):
        self.metrics_url = metrics_url

    def analyze_weekly_trends(self):
        """Analyze automation trends from weekly reviews"""
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=12)

        response = requests.get(
            f"{self.metrics_url}/weekly-reviews",
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        )

        reviews = response.json()

        # Calculate trends
        trends = {
            "total_reviews": len(reviews),
            "avg_action_items": sum(len(r["action_items"]) for r in reviews) / len(reviews),
            "automation_completion_rate": self.calculate_completion_rate(reviews),
            "recurring_toil": self.identify_recurring_patterns(reviews)
        }

        return trends

    def identify_recurring_patterns(self, reviews):
        """Identify frequently mentioned manual tasks"""
        all_items = []
        for review in reviews:
            all_items.extend(review["action_items"])

        # Simple keyword frequency analysis
        keywords = {}
        for item in all_items:
            words = item.lower().split()
            for word in words:
                if len(word) > 4:  # Skip short words
                    keywords[word] = keywords.get(word, 0) + 1

        # Return top recurring patterns
        return sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]

    def generate_team_report(self, team_name):
        """Generate weekly review effectiveness report for team"""
        trends = self.analyze_weekly_trends()

        report = f"""
        # Weekly Review Effectiveness Report
        Team: {team_name}
        Generated: {datetime.now().isoformat()}

        ## Summary
        - Total reviews conducted: {trends['total_reviews']}
        - Average action items per review: {trends['avg_action_items']:.1f}
        - Automation completion rate: {trends['automation_completion_rate']:.1%}

        ## Recurring Toil Patterns
        """

        for pattern, count in trends["recurring_toil"]:
            report += f"- {pattern}: mentioned {count} times\n"

        return report
```

### Human Process

**Team Review Facilitation:**
1. Designated facilitator rotates weekly among team members
2. Review begins with previous week's automation backlog status update
3. Team collectively answers the three assessment questions
4. Discussion prioritizes automation opportunities by impact and effort
5. Action items are assigned owners and target completion dates
6. Review concludes with boundary health assessment and cultural check-in

**Cross-Team Coordination:**
1. Monthly integration meetings share automation patterns across teams
2. Shared automation backlog for organization-wide opportunities
3. Resource allocation discussions for high-impact automation projects
4. Cultural consistency review across team boundary practices

**Continuous Improvement:**
1. Quarterly meta-reviews assess weekly review process effectiveness
2. Team feedback drives review format and tooling improvements
3. Success stories and lessons learned shared across organization
4. Review metrics inform cultural health and boundary maintenance trends

## Compliance Verification

### Automated Checks

**Review Completion Tracking:**
```sql
-- Weekly review compliance monitoring
SELECT
  team_name,
  DATE(review_date) as week_of,
  COUNT(*) as reviews_completed,
  AVG(JSON_LENGTH(action_items)) as avg_action_items,
  SUM(CASE WHEN JSON_LENGTH(action_items) = 0 THEN 1 ELSE 0 END) as empty_reviews
FROM weekly_boundary_reviews
WHERE review_date >= DATE_SUB(NOW(), INTERVAL 8 WEEK)
GROUP BY team_name, YEARWEEK(review_date)
ORDER BY team_name, week_of DESC;
```

**Automation Progress Tracking:**
```bash
# Weekly automation backlog health check
#!/bin/bash

echo "=== Automation Backlog Health ==="

# Check completion rates
curl -s "https://metrics.nashgroup.internal/automation-backlog/stats" | \
jq -r '
  "Total items: \(.total_items)",
  "Completed: \(.completed_items) (\(.completion_rate)%)",
  "In progress: \(.in_progress_items)",
  "Overdue: \(.overdue_items)"
'

# Identify stale items
echo
echo "=== Stale Backlog Items (>30 days) ==="
curl -s "https://metrics.nashgroup.internal/automation-backlog/stale" | \
jq -r '.[] | "- \(.title) (created: \(.created_date), team: \(.team))"'
```

### Manual Audits

**Monthly Review Quality Assessment:**
- Team lead evaluation of review depth and actionability
- Cross-team comparison of automation progress and patterns
- Cultural alignment assessment with Human/Machine boundary principles
- Process effectiveness measurement and improvement identification

**Quarterly Boundary Evolution:**
- Organization-wide boundary health assessment
- Team-specific boundary practice evaluation
- Automation strategy alignment with organizational goals
- Cultural consistency measurement across teams

### Reporting

**Weekly Team Metrics:**
- Review completion rate by team
- Average action items generated per review
- Automation backlog completion velocity
- Boundary health indicators by team

**Monthly Organizational Health:**
- Cross-team automation pattern analysis
- Boundary drift identification and correction
- Cultural consistency metrics
- Resource allocation effectiveness for automation initiatives

## Related Documents

**Source Material:**
- [../the-covenant/HUMAN_MANDATE.md - The Weekly Review](../the-covenant/HUMAN_MANDATE.md#the-weekly-review)
- [../the-covenant/HUMAN_MANDATE.md - Human/Machine Creed](../the-covenant/HUMAN_MANDATE.md#the-humanmachine-creed)

**Related Policies:**
- [OPS-006: Guardian Role Responsibilities](./ops-006-guardian-roles.md) - Role-based automation decisions
- [OPS-007: Daily Stand Protocol](./ops-007-daily-stand.md) - Individual boundary consciousness
- [OPS-009: Quarterly Reflection Ritual](./ops-009-quarterly-reflection.md) - Organizational boundary assessment
- [OPS-005: Runbooks](./ops-005-runbooks.md) - Automation vs manual procedure decisions

**Technical References:**
- [../the-citadel/scripts/weekly-boundary-review.sh](../the-citadel/scripts/weekly-boundary-review.sh) - Review automation
- [../the-citadel/.github/workflows/weekly-review.yml](../the-citadel/.github/workflows/weekly-review.yml) - Automated review facilitation

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|---------|
| 2024-09-30 | 1.0 | Initial policy creation from Human Mandate weekly review ritual | Claude |
