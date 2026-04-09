# OPS-007: Daily Stand Protocol

**Policy ID:** OPS-007
**Category:** Operations
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

All Guardians **must** perform daily self-assessment using the three-question protocol: "What hat am I wearing today?", "Does my work align with The Covenant?", and "Am I automating toil or creating it?" This protocol **shall** be integrated into personal workflows and team check-ins to maintain Human/Machine boundary awareness.

## Rationale

From The Human Mandate's Daily Stand: "Each Guardian should ask themselves: 1. What hat am I wearing today? 2. Does my work align with The Covenant? 3. Am I automating toil or creating it?"

The Human/Machine boundary requires continuous conscious maintenance through daily reflection:

- **Role Consciousness**: Without daily role awareness, guardians drift between responsibilities without clear accountability
- **Principle Alignment**: Daily work can gradually deviate from covenant principles without conscious realignment
- **Automation Purpose**: The distinction between value-creating automation and toil-generating work requires daily assessment
- **Cultural Reinforcement**: Daily practices embed organizational values more effectively than periodic training
- **Boundary Maintenance**: The Human/Machine boundary erodes through unconscious habit rather than deliberate violation

This daily protocol ensures that human judgment remains deliberate, principled, and aligned with our automated systems rather than competing with them.

## Scope

**Applies To:**
- All Guardians performing work on behalf of The Nash Group
- All work sessions involving infrastructure, development, or organizational decisions
- All team meetings and collaborative activities
- All significant task transitions and context switches

**Time Boundaries:**
- Individual practices: Personal daily reflection and role declaration
- Team processes: Daily stand-ups and work session kick-offs
- Organizational rituals: Cultural health metrics and alignment tracking

## Implementation

### Technical Enforcement

Daily standup automation with role tracking:

```bash
#!/bin/bash
# ~/.nashgroup/daily-standup.sh
# ROLE: Gardener - Automating daily cultural practices

echo "=== Daily Guardian Protocol ==="
echo "Date: $(date)"
echo

# Question 1: Role consciousness
echo "1. What hat am I wearing today?"
echo "   [ ] Philosopher - Refining principles and values"
echo "   [ ] Architect - Translating philosophy to code"
echo "   [ ] Judge - Reviewing and approving changes"
echo "   [ ] Gardener - Maintaining system health"
echo "   [ ] Explorer - Building new capabilities"
read -p "Primary role: " role

# Question 2: Covenant alignment
echo
echo "2. Does my work align with The Covenant?"
echo "   Which principle guides today's work?"
read -p "Guiding principle: " principle

# Question 3: Automation boundary
echo
echo "3. Am I automating toil or creating it?"
echo "   [ ] Automating - Reducing future manual work"
echo "   [ ] Creating - Building features/capabilities"
echo "   [ ] Warning - May be creating toil"
read -p "Automation status: " automation

# Log to metrics system
curl -X POST "https://metrics.nashgroup.internal/daily-protocol" \
  -H "Content-Type: application/json" \
  -d "{
    \"guardian\": \"$(git config user.name)\",
    \"date\": \"$(date -I)\",
    \"role\": \"$role\",
    \"principle\": \"$principle\",
    \"automation_status\": \"$automation\"
  }"

echo
echo "Protocol complete. Have a purposeful day!"
```

GitHub workflow for PR standup integration:

```yaml
# .github/workflows/pr-daily-check.yml
name: PR Daily Protocol Check
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  daily-protocol:
    runs-on: ubuntu-latest
    steps:
      - name: Check Daily Protocol Completion
        run: |
          # Verify author completed daily protocol today
          AUTHOR="${{ github.event.pull_request.user.login }}"
          TODAY=$(date -I)

          if ! curl -s "https://metrics.nashgroup.internal/daily-protocol/${AUTHOR}/${TODAY}" | grep -q "completed"; then
            echo "WARNING: Daily protocol not completed today"
            echo "Please run daily standup before submitting PRs"
            echo "Command: ~/.nashgroup/daily-standup.sh"
          fi
```

### Automated Validation

Slack integration for daily protocol tracking:

```python
# scripts/daily-protocol-bot.py
# ROLE: Gardener - Maintaining daily cultural practices through automation

import slack_sdk
import json
from datetime import datetime

def send_daily_reminder():
    """Send daily protocol reminder to team channels"""
    client = slack_sdk.WebClient(token=os.environ["SLACK_TOKEN"])

    message = {
        "text": "🌅 Daily Guardian Protocol",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Daily Guardian Protocol*\n\n"
                           "1. 🎭 What hat am I wearing today?\n"
                           "2. 📜 Does my work align with The Covenant?\n"
                           "3. 🤖 Am I automating toil or creating it?"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Complete Protocol"},
                        "value": "complete_protocol",
                        "action_id": "daily_protocol_button"
                    }
                ]
            }
        ]
    }

    # Send to all team channels
    for channel in ["#guardians", "#mentors", "#watchers"]:
        client.chat_postMessage(channel=channel, **message)

def track_completion(user_id, responses):
    """Track daily protocol completion"""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "user": user_id,
        "role_declared": responses.get("role"),
        "principle_identified": responses.get("principle"),
        "automation_assessed": responses.get("automation"),
        "completed": True
    }

    # Store in metrics database
    save_to_metrics_db(metrics)
```

### Human Process

**Personal Daily Practice:**
1. Begin each work session with the three-question protocol
2. Document primary role for the day in personal task management system
3. Identify the covenant principle guiding the day's work
4. Assess whether planned work automates toil or creates new value
5. Adjust workload if answers reveal misalignment

**Team Integration:**
1. Daily stand-ups begin with role declarations from team members
2. Team lead facilitates alignment discussion when role conflicts emerge
3. Weekly retrospectives review daily protocol adherence and effectiveness
4. Team members support each other in maintaining protocol discipline

**Cultural Reinforcement:**
1. New guardian onboarding includes daily protocol training
2. Performance reviews include protocol adherence as cultural competency
3. Team ceremonies celebrate consistent protocol practitioners
4. Leadership modeling through visible protocol adherence

## Compliance Verification

### Automated Checks

**Protocol Completion Tracking:**
```sql
-- Daily protocol completion rate
SELECT
  DATE(timestamp) as protocol_date,
  COUNT(DISTINCT user) as guardians_completed,
  (SELECT COUNT(*) FROM active_guardians) as total_guardians,
  ROUND(COUNT(DISTINCT user) * 100.0 / (SELECT COUNT(*) FROM active_guardians), 2) as completion_rate
FROM daily_protocol_metrics
WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(timestamp)
ORDER BY protocol_date DESC;
```

**Role Distribution Analysis:**
```bash
# Weekly role distribution report
#!/bin/bash
# Check role diversity and balance

echo "=== Weekly Role Distribution ==="
curl -s "https://metrics.nashgroup.internal/weekly-roles" | \
jq -r '.[] | "\(.role): \(.count) guardians (\(.percentage)%)"'

echo
echo "=== Principle Alignment Trends ==="
curl -s "https://metrics.nashgroup.internal/principle-tracking" | \
jq -r '.[] | "\(.principle): \(.mentions) times this week"'
```

### Manual Audits

**Weekly Team Reviews:**
- Team leads review protocol completion rates
- Discussion of role distribution and balance
- Identification of protocol adherence challenges
- Cultural alignment assessment through principle tracking

**Monthly Protocol Evolution:**
- Guardian feedback on protocol effectiveness
- Question refinement based on organizational learning
- Integration improvements with existing workflows
- Cultural impact assessment

### Reporting

**Daily Metrics:**
- Individual protocol completion status
- Team completion rates by organization unit
- Role distribution across active guardians
- Principle alignment patterns

**Weekly Cultural Health:**
- Protocol adherence trends over time
- Role diversity and balance metrics
- Automation vs. toil creation ratios
- Covenant alignment effectiveness

## Related Documents

**Source Material:**
- [../the-covenant/HUMAN_MANDATE.md - The Daily Stand](../the-covenant/HUMAN_MANDATE.md#the-daily-stand)
- [../the-covenant/HUMAN_MANDATE.md - Human/Machine Creed](../the-covenant/HUMAN_MANDATE.md#the-humanmachine-creed)

**Related Policies:**
- [OPS-006: Guardian Role Responsibilities](./ops-006-guardian-roles.md) - Role consciousness framework
- [OPS-008: Weekly Review Process](./ops-008-weekly-review.md) - Team-level boundary assessment
- [GOV-001: Living Principles](./gov-001-living-principles.md) - Covenant principle evolution

**Technical References:**
- [../the-citadel/.github/workflows/daily-protocol.yml](../the-citadel/.github/workflows/daily-protocol.yml) - Automated protocol integration
- [../the-citadel/scripts/daily-standup.sh](../the-citadel/scripts/daily-standup.sh) - Daily protocol automation

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|---------|
| 2024-09-30 | 1.0 | Initial policy creation from Human Mandate daily stand ritual | Claude |
