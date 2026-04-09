# GOV-001: Living Principles

**Policy ID:** GOV-001
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

These principles **must** evolve through experience. They are not carved in stone but written in a living repository. Dogma without reflection becomes ritual without purpose.

## Rationale

Dogma without reflection becomes ritual without purpose. We must learn, adapt, and improve our principles as we learn new lessons:

- **Context Evolution**: Technology and organizational needs change over time
- **Learning Integration**: New experiences should refine our understanding
- **Principle Obsolescence**: Some principles may become outdated or counterproductive
- **Implementation Gaps**: Real-world application reveals flaws in theoretical principles
- **Cultural Adaptation**: Principles must adapt to team growth and cultural evolution
- **Continuous Improvement**: Static principles prevent organizational learning and growth

Living principles enable adaptive governance that improves through experience while maintaining consistency and predictability.

## Scope

**Applies To:**
- All principles documented in PRINCIPLES.md within the-covenant repository
- All governance procedures and policies derived from these principles
- All technical implementations in the-citadel that enforce principles
- All decision-making processes that reference organizational principles
- All onboarding and training materials that communicate principles

**Exceptions:**
- Fundamental ethical principles (those are truly immutable)
- Legally required compliance principles (cannot be changed without legal review)

## Implementation

### Technical Enforcement

Principle evolution tracking and governance:

```hcl
# terraform/github/principle_governance.tf
resource "github_repository_ruleset" "principle_changes" {
  name        = "Living Principles Governance"
  repository  = "the-covenant"  # Principle repository
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
  }

  rules {
    required_status_checks {
      strict_required_status_checks_policy = true
      required_status_checks = [
        { context = "governance/principle-impact-analysis" },
        { context = "governance/implementation-validation" },
        { context = "governance/consultation-period" }
      ]
    }

    pull_request {
      required_approving_review_count = 3  # Higher bar for principle changes
      dismiss_stale_reviews_on_push  = true
      require_code_owner_review       = true
      require_last_push_approval     = true
    }

    # Require specific labels for principle changes
    required_conversations_resolution = true
  }

  labels = {
    "nash.group/policy"    = "gov-001"
    "nash.group/component" = "governance"
    "nash.group/criticality" = "high"
  }
}

# Issue templates for principle evolution
resource "github_repository_file" "principle_proposal_template" {
  repository = "the-covenant"
  file       = ".github/ISSUE_TEMPLATE/principle-proposal.yml"

  content = yamlencode({
    name        = "Principle Proposal"
    description = "Propose a new principle or modification to existing principles"
    title       = "[PRINCIPLE] "
    labels      = ["principle-proposal", "governance"]

    body = [
      {
        type = "markdown"
        attributes = {
          value = "## Principle Evolution Process\n\nThis template helps ensure principle changes follow the Living Principles policy (GOV-001)."
        }
      },
      {
        type        = "dropdown"
        id          = "change-type"
        attributes = {
          label = "Type of Change"
          options = [
            "New Principle",
            "Modify Existing Principle",
            "Remove Obsolete Principle",
            "Clarify Implementation"
          ]
        }
        validations = { required = true }
      },
      {
        type        = "textarea"
        id          = "current-state"
        attributes = {
          label       = "Current State"
          description = "What is the current principle or lack thereof?"
          placeholder = "Describe the existing principle or the gap that needs addressing"
        }
        validations = { required = true }
      },
      {
        type        = "textarea"
        id          = "proposed-change"
        attributes = {
          label       = "Proposed Change"
          description = "What specific change are you proposing?"
          placeholder = "Be specific about the new or modified principle"
        }
        validations = { required = true }
      },
      {
        type        = "textarea"
        id          = "rationale"
        attributes = {
          label       = "Rationale"
          description = "Why is this change necessary?"
          placeholder = "What experience or learning drives this proposal?"
        }
        validations = { required = true }
      }
    ]
  })
}
```

Automated principle evolution tracking:

```yaml
# .github/workflows/principle-evolution.yml
name: Principle Evolution Tracking
on:
  pull_request:
    paths: ['PRINCIPLES.md', 'GOVERNANCE.md']
  issues:
    types: [opened, labeled]

jobs:
  track-principle-changes:
    if: contains(github.event.pull_request.labels.*.name, 'principle-change') || contains(github.event.issue.labels.*.name, 'principle-proposal')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Analyze Principle Impact
        if: github.event_name == 'pull_request'
        run: |
          echo "Analyzing principle changes for implementation impact..."

          # Get changed lines in PRINCIPLES.md
          git diff origin/main HEAD -- PRINCIPLES.md > principle-changes.diff

          # Extract changed principles
          python3 - <<'EOF'
          import re
          import sys

          # Read the diff
          with open('principle-changes.diff', 'r') as f:
              diff_content = f.read()

          # Find principle sections that changed
          principle_pattern = r'^[+-].*?##\s+Principle\s+(\d+):\s+(.+)$'
          changes = re.findall(principle_pattern, diff_content, re.MULTILINE)

          if changes:
              print("Principle changes detected:")
              for action, principle_num, title in [(line[0], *line[1:]) for line in changes]:
                  action_type = "Added" if action == '+' else "Modified/Removed"
                  print(f"- {action_type}: Principle {principle_num}: {title}")

              # Check for implementation impact
              print("\nChecking the-citadel for implementation impact...")
              # This would integrate with the the-citadel repository
              # to find references to changed principles
          else:
              print("No principle-level changes detected")
          EOF

      - name: Validate Implementation Consistency
        if: github.event_name == 'pull_request'
        run: |
          echo "Validating that principle changes have corresponding implementation updates..."

          # Check if the-citadel needs updates
          # This would be a more sophisticated check in practice
          if git diff --name-only origin/main HEAD | grep -q "PRINCIPLES.md"; then
              echo "Principle changes detected - checking for the-citadel updates"

              # Create an issue or PR in the-citadel if needed
              echo "Implementation validation required"
          fi

      - name: Generate Evolution Report
        run: |
          echo "Generating principle evolution report..."

          cat > principle-evolution-report.md <<EOF
          # Principle Evolution Report

          Generated: $(date)
          PR/Issue: #${{ github.event.number }}

          ## Changes Summary
          $(if [ -f principle-changes.diff ]; then echo "Changes detected in PRINCIPLES.md"; else echo "No principle changes"; fi)

          ## Implementation Impact
          - Citadel-config updates: $(if git diff --name-only origin/main HEAD | grep -q citadel; then echo "Required"; else echo "Not required"; fi)
          - Policy updates: TBD
          - Training updates: TBD

          ## Next Steps
          1. Complete impact analysis
          2. Update implementation as needed
          3. Communicate changes to organization
          4. Update training materials
          EOF

          echo "Report generated:"
          cat principle-evolution-report.md

          # Add report as PR comment
          if [ "${{ github.event_name }}" = "pull_request" ]; then
              gh pr comment ${{ github.event.number }} --body-file principle-evolution-report.md
          fi
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  consultation-period:
    if: contains(github.event.issue.labels.*.name, 'principle-proposal')
    runs-on: ubuntu-latest
    steps:
      - name: Start Consultation Period
        run: |
          echo "Starting consultation period for principle proposal..."

          # Calculate consultation end date (minimum 7 days)
          end_date=$(date -d '+7 days' +%Y-%m-%d)

          # Add comment to issue
          gh issue comment ${{ github.event.issue.number }} --body "## Consultation Period Started

          This principle proposal is now in consultation period until **$end_date**.

          ### Participation Guidelines
          - All team members are encouraged to provide feedback
          - Consider implementation challenges and organizational impact
          - Share experiences that support or challenge the proposal
          - Suggest improvements or alternatives

          ### Next Steps
          After consultation period:
          1. Proposal will be reviewed by governance team
          2. If approved, implementation plan will be created
          3. Changes will be made to PRINCIPLES.md and related systems

          See [GOV-001 Living Principles](policies/gov-001-living-principles.md) for full process."

          # Set reminder for consultation end
          gh issue edit ${{ github.event.issue.number }} --add-label "consultation-active"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Automated Validation

**Principle Consistency Checking:**
```python
#!/usr/bin/env python3
# scripts/validate-principle-consistency.py
"""
Validates consistency between PRINCIPLES.md and implementation
"""

import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple

class PrincipleConsistencyValidator:
    def __init__(self):
        self.principles_file = Path("../the-covenant/PRINCIPLES.md")
        self.policies_dir = Path("policies/")
        self.citadel_dir = Path("../the-citadel/terraform/")

    def extract_principles(self) -> Dict[int, Dict]:
        """Extract all principles from PRINCIPLES.md"""
        if not self.principles_file.exists():
            raise FileNotFoundError("PRINCIPLES.md not found")

        with open(self.principles_file, 'r') as f:
            content = f.read()

        principles = {}
        principle_pattern = r'### Principle (\d+): (.+?)\n\n\*\*The Law\*\*\s*\n(.+?)\n\n\*\*The Lesson\*\*\s*\n(.+?)\n\n\*\*The Implementation\*\*\s*\n(.+?)(?=\n###|\n---|\Z)'

        matches = re.findall(principle_pattern, content, re.DOTALL)

        for match in matches:
            num, title, law, lesson, implementation = match
            principles[int(num)] = {
                'title': title.strip(),
                'law': law.strip(),
                'lesson': lesson.strip(),
                'implementation': implementation.strip()
            }

        return principles

    def find_principle_references(self) -> Dict[int, List[str]]:
        """Find references to principles in policies and implementation"""
        references = {}

        # Check policy files
        for policy_file in self.policies_dir.glob("*.md"):
            with open(policy_file, 'r') as f:
                content = f.read()

            # Look for principle references
            principle_refs = re.findall(r'Principle (\d+):', content)
            for ref in principle_refs:
                principle_num = int(ref)
                if principle_num not in references:
                    references[principle_num] = []
                references[principle_num].append(f"policy:{policy_file.name}")

        # Check Terraform files
        for tf_file in self.citadel_dir.rglob("*.tf"):
            with open(tf_file, 'r') as f:
                content = f.read()

            # Look for principle comments
            principle_refs = re.findall(r'# Principle (\d+):|nash\.group/principle.*?(\d+)', content)
            for ref in principle_refs:
                if isinstance(ref, tuple):
                    principle_num = int(ref[1]) if ref[1] else int(ref[0])
                else:
                    principle_num = int(ref)

                if principle_num not in references:
                    references[principle_num] = []
                references[principle_num].append(f"terraform:{tf_file.name}")

        return references

    def validate_consistency(self) -> List[Dict]:
        """Validate consistency between principles and implementation"""
        issues = []

        principles = self.extract_principles()
        references = self.find_principle_references()

        # Check for principles without implementation
        for num, principle in principles.items():
            if num not in references:
                issues.append({
                    'type': 'missing_implementation',
                    'principle': num,
                    'title': principle['title'],
                    'message': f"Principle {num} has no implementation references"
                })

        # Check for orphaned references
        all_principle_nums = set(principles.keys())
        referenced_nums = set(references.keys())

        for num in referenced_nums - all_principle_nums:
            issues.append({
                'type': 'orphaned_reference',
                'principle': num,
                'references': references[num],
                'message': f"References found to non-existent Principle {num}"
            })

        return issues

    def generate_report(self) -> str:
        """Generate a consistency report"""
        principles = self.extract_principles()
        references = self.find_principle_references()
        issues = self.validate_consistency()

        report = ["# Principle Consistency Report\n"]
        report.append(f"Generated: {datetime.now().isoformat()}\n")

        report.append("## Summary")
        report.append(f"- Total principles: {len(principles)}")
        report.append(f"- Principles with implementation: {len(references)}")
        report.append(f"- Consistency issues: {len(issues)}\n")

        if issues:
            report.append("## Issues Found")
            for issue in issues:
                report.append(f"- **{issue['type']}**: {issue['message']}")

        report.append("\n## Implementation Coverage")
        for num, principle in principles.items():
            refs = references.get(num, [])
            report.append(f"- Principle {num}: {principle['title']}")
            if refs:
                for ref in refs:
                    report.append(f"  - {ref}")
            else:
                report.append("  - ⚠️ No implementation found")

        return "\n".join(report)

if __name__ == "__main__":
    import datetime

    validator = PrincipleConsistencyValidator()
    issues = validator.validate_consistency()

    if issues:
        print("❌ Principle consistency issues found:")
        for issue in issues:
            print(f"  - {issue['message']}")
        exit(1)
    else:
        print("✅ All principles are consistently implemented")

    # Generate full report
    report = validator.generate_report()
    with open("principle-consistency-report.md", "w") as f:
        f.write(report)
    print("📄 Full report saved to principle-consistency-report.md")
```

### Human Process

1. **Quarterly Principle Review**: Regular assessment of principle effectiveness and relevance
2. **Experience Integration**: Process for incorporating lessons learned into principle updates
3. **Consultation Process**: Minimum 7-day consultation period for all principle changes
4. **Implementation Alignment**: Ensure the-citadel updates accompany principle changes
5. **Communication Strategy**: Clear communication of principle changes to all team members

## Principle Evolution Process

### Proposal Phase

**Principle Change Proposal Template:**
```markdown
# Principle Change Proposal

## Type of Change
- [ ] New Principle
- [ ] Modify Existing Principle
- [ ] Remove Obsolete Principle
- [ ] Clarify Implementation

## Current State
Describe the current principle or the gap that needs addressing.

## Proposed Change
Specific text of the new or modified principle.

### The Law
What is the rule we should follow?

### The Lesson
What experience or wisdom led to this principle?

### The Implementation
How will this be enforced in the-citadel?

### The Guardian
Which role from the Human Mandate owns this principle?

## Rationale
Why is this change necessary? What triggered this proposal?

### Experience That Led to This
- Incident or learning that prompted the change
- Specific examples of current principle inadequacy
- Evidence of need for change

### Expected Benefits
- How this will improve our operations
- Risks mitigated by this change
- Value delivered to the organization

## Impact Analysis

### Implementation Impact
- [ ] Requires the-citadel changes
- [ ] Requires policy updates
- [ ] Requires training updates
- [ ] Requires tooling changes

### Affected Systems
List systems, processes, or teams affected by this change.

### Migration Plan
If this is a breaking change to existing practices:
1. Current state assessment
2. Migration timeline
3. Support during transition
4. Success criteria

## Consultation

### Stakeholders to Consult
- [ ] Engineering teams
- [ ] Security team
- [ ] Operations team
- [ ] External partners (if applicable)

### Consultation Period
Minimum 7 days, extended for complex changes.

### Decision Criteria
What will determine if this proposal is accepted?
```

### Review and Approval Process

**Governance Review Stages:**
1. **Initial Screening**: Proposal completeness and basic feasibility
2. **Consultation Period**: Organization-wide feedback collection
3. **Impact Analysis**: Technical and operational impact assessment
4. **Implementation Planning**: Detailed plan for principle adoption
5. **Approval Decision**: Final approval by governance team
6. **Implementation**: Coordinated rollout across systems and processes

**Approval Criteria:**
```yaml
approval_requirements:
  min_consultation_days: 7
  required_approvals:
    - watchers: 2
    - mentors: 2
    - affected_teams: 1 (if applicable)

  blocking_criteria:
    - unresolved_major_concerns: true
    - implementation_infeasible: true
    - conflicts_with_existing: true

  expedited_process:
    security_critical: true
    incident_response: true
    min_consultation_days: 2
```

### Implementation and Communication

**Change Implementation Checklist:**
```markdown
## Principle Change Implementation

### Pre-Implementation
- [ ] Governance approval received
- [ ] Implementation plan approved
- [ ] Communication plan prepared
- [ ] Training materials updated

### Implementation
- [ ] PRINCIPLES.md updated
- [ ] Related policies updated
- [ ] Citadel-config updated
- [ ] Automation updated
- [ ] Documentation updated

### Post-Implementation
- [ ] Change communicated to organization
- [ ] Training delivered
- [ ] Feedback collection started
- [ ] Success metrics established

### Follow-up
- [ ] 30-day effectiveness review
- [ ] 90-day impact assessment
- [ ] Annual principle review inclusion
```

**Communication Strategy:**
```markdown
# Principle Change Communication Plan

## Announcement Channels
1. **Email**: All-hands notification
2. **Slack**: #announcements and relevant team channels
3. **Documentation**: Updated principle documentation
4. **Training**: Integration into onboarding materials

## Message Template
Subject: [PRINCIPLE UPDATE] New/Modified Principle: [Title]

Team,

We've updated our organizational principles based on recent experience and learning.

**What Changed**: Brief description of the change
**Why**: Rationale for the change
**Impact**: How this affects daily work
**Action Required**: What team members need to do
**Questions**: How to get help or clarification

See full details: [link to updated PRINCIPLES.md]

## Feedback Collection
- Open feedback period: 30 days
- Feedback channels: GitHub issues, Slack, email
- Feedback review: Weekly during feedback period
```

## Principle Lifecycle Management

### Principle Health Monitoring

**Effectiveness Metrics:**
```yaml
principle_health_metrics:
  implementation_coverage:
    measurement: "% of applicable systems implementing principle"
    target: ">95%"
    frequency: "monthly"

  violation_rate:
    measurement: "incidents caused by principle violations"
    target: "<1 per quarter"
    frequency: "quarterly"

  team_understanding:
    measurement: "% of team members who can explain principle"
    target: ">90%"
    frequency: "annually"

  relevance_score:
    measurement: "team assessment of principle relevance"
    target: ">4.0/5.0"
    frequency: "annually"
```

**Principle Retirement Process:**
```markdown
# Principle Retirement Checklist

## Trigger Conditions
- [ ] Principle no longer relevant to current operations
- [ ] Principle conflicts with newer, better principle
- [ ] Principle implementation consistently problematic
- [ ] Technology/practice evolution makes principle obsolete

## Retirement Process
1. **Obsolescence Assessment**: Confirm principle is truly obsolete
2. **Impact Analysis**: Identify systems and processes using this principle
3. **Migration Plan**: Plan for removing principle and updating systems
4. **Consultation**: Get organization feedback on retirement
5. **Implementation**: Remove principle and update all references
6. **Communication**: Announce retirement and provide transition guidance

## Post-Retirement
- [ ] All implementation references removed
- [ ] Historical context preserved in decisions/ directory
- [ ] Lessons learned integrated into remaining principles
```

### Continuous Improvement

**Annual Principle Review Process:**
```markdown
# Annual Principle Review

## Preparation (Month 1)
- Collect principle effectiveness data
- Survey team on principle relevance and clarity
- Analyze incidents related to principle violations
- Review implementation consistency

## Review Process (Month 2)
- Team workshops on principle effectiveness
- Cross-functional review of principle implementation
- Identify improvement opportunities
- Propose principle changes

## Implementation (Month 3)
- Process approved principle changes
- Update implementation and documentation
- Communicate changes to organization
- Update training materials

## Success Criteria
- All principles reviewed for relevance
- Implementation consistency >95%
- Team understanding >90%
- Improvement proposals addressed
```

**Learning Integration:**
```python
# scripts/extract-learning.py
"""
Extract learning from incidents and experiences for principle evolution
"""

def analyze_incident_patterns():
    """Analyze patterns in incidents that might indicate principle gaps"""

    incident_patterns = {
        'recurring_issues': [],
        'principle_violations': [],
        'implementation_gaps': [],
        'new_principle_needs': []
    }

    # Analyze incident reports for patterns
    # This would integrate with incident management systems

    return incident_patterns

def suggest_principle_updates(patterns):
    """Suggest principle updates based on incident patterns"""

    suggestions = []

    for pattern in patterns['recurring_issues']:
        suggestion = {
            'type': 'strengthen_existing',
            'principle': pattern['related_principle'],
            'reasoning': pattern['failure_mode'],
            'proposed_change': pattern['suggested_improvement']
        }
        suggestions.append(suggestion)

    for gap in patterns['new_principle_needs']:
        suggestion = {
            'type': 'new_principle',
            'area': gap['domain'],
            'reasoning': gap['incidents'],
            'proposed_principle': gap['draft']
        }
        suggestions.append(suggestion)

    return suggestions
```

## Compliance Verification

**Automated Checks:**
- Daily validation of principle-implementation consistency
- Weekly monitoring of principle evolution process compliance
- Monthly assessment of principle effectiveness metrics
- Quarterly review of principle change impact

**Manual Audits:**
- Monthly review of principle consultation processes
- Quarterly assessment of principle implementation coverage
- Annual comprehensive principle effectiveness review

**Reporting:**
- Real-time principle evolution dashboard
- Monthly principle health metrics
- Quarterly principle change impact reports
- Annual organizational principle maturity assessment

## Integration with Organizational Learning

### Learning Capture Process

**Post-Incident Principle Review:**
```markdown
# Post-Incident Principle Review

## Incident Information
- **Incident ID**: INC-2024-001
- **Date**: 2024-09-30
- **Severity**: High
- **Root Cause**: Configuration drift

## Principle Analysis
### Related Principles
- Principle 5: Infrastructure as Code Only
- Principle 8: Fail Fast, Recover Faster

### Principle Effectiveness
- Did existing principles prevent this incident? No
- Were principles followed correctly? Partially
- Are principles clear enough? Needs improvement

### Proposed Changes
1. **Strengthen Principle 5**: Add automated drift detection requirement
2. **Implementation Update**: Enhance the-citadel drift monitoring
3. **New Principle**: Consider "Configuration Immutability" principle

## Next Steps
- [ ] Create principle change proposal
- [ ] Update implementation plan
- [ ] Schedule team discussion
```

**Quarterly Learning Integration:**
```bash
#!/bin/bash
# scripts/quarterly-learning-integration.sh
# Integrates lessons learned into principle evolution

set -euo pipefail

echo "Starting quarterly learning integration..."

# Collect incident data
echo "Analyzing incidents from last quarter..."
python3 scripts/analyze-incident-patterns.py --period="last-quarter" > incident-analysis.json

# Review principle effectiveness
echo "Reviewing principle effectiveness..."
python3 scripts/principle-effectiveness.py --metrics=quarterly > effectiveness-report.md

# Generate improvement suggestions
echo "Generating improvement suggestions..."
python3 scripts/suggest-principle-updates.py \
    --incidents=incident-analysis.json \
    --effectiveness=effectiveness-report.md \
    > principle-suggestions.md

# Create GitHub issues for significant suggestions
echo "Creating improvement proposals..."
while read -r suggestion; do
    if [[ $suggestion =~ "HIGH_PRIORITY" ]]; then
        gh issue create \
            --title="[PRINCIPLE] $suggestion" \
            --label="principle-proposal,high-priority" \
            --body-file=principle-suggestions.md
    fi
done < principle-suggestions.md

echo "Quarterly learning integration completed"
```

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 16: These Principles Are Living Law](../the-covenant/PRINCIPLES.md#principle-16-these-principles-are-living-law)
- **Governance Authority:** [GOVERNANCE.md - Covenant Decisions](../the-covenant/GOVERNANCE.md#covenant-decisions-constitutional-changes)
- **Implementation:** Principle evolution tracking, governance automation, consultation processes
- **Change Management:** [DEP-001 Breaking Change Management](./dep-001-breaking-changes.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 16: These Principles Are Living Law
