# GOV-002: Covenant Amendment Process

**Policy ID:** GOV-002
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Changes to the Covenant **must** follow The Ritual of Amendment process. All constitutional changes **shall** require proposal, debate period, council review, and proclamation phases. No principle or governance rule **may** be modified outside this sacred process.

## Rationale

The Covenant represents our organizational constitution and foundational principles. Changing these requires deliberation, consensus, and ceremony to ensure:

- **Deliberate Change**: Major organizational shifts receive appropriate consideration and debate
- **Community Input**: All Immortals can participate in shaping organizational principles
- **Quality Assurance**: Council review prevents hasty or poorly-considered changes
- **Transparency**: Public debate and documentation make the process visible and accountable
- **Legitimacy**: Formal process gives amendments proper authority and acceptance
- **Stability**: Protection against frivolous changes while allowing necessary evolution
- **Implementation Planning**: Changes include consideration of technical implementation requirements

The Ritual of Amendment ensures constitutional changes are made thoughtfully with broad consensus while maintaining organizational stability.

## Scope

**Applies To:**
- All changes to files within the-covenant repository
- All modifications to GOVERNANCE.md, PRINCIPLES.md, and HUMAN_MANDATE.md
- Any proposals affecting organizational structure or decision-making processes
- Changes to team authorities, roles, or responsibilities defined in governance documents
- Modifications to conflict resolution procedures or emergency powers

**Exceptions:**
- Typo corrections and formatting improvements (may use standard PR process)
- Adding clarifying examples that don't change meaning
- Emergency changes during break-glass procedures (must be ratified afterward)

## Implementation

### Technical Enforcement

GitHub repository protection and workflow automation:

```hcl
# terraform/github/covenant_governance.tf
resource "github_repository_ruleset" "covenant_amendment_process" {
  name        = "The Ritual of Amendment"
  repository  = "the-covenant"
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["refs/heads/main"]
      exclude = []
    }
  }

  rules {
    # Require proposal branch naming convention
    creation = false

    # Require 72-hour minimum debate period
    required_status_checks {
      required_status_checks = [
        "amendment-debate-period",
        "council-quorum-check",
        "implementation-plan-review"
      ]
      strict_required_status_checks_policy = true
    }

    # Require council approval (2 Watchers + 2 Mentors)
    pull_request {
      required_approving_review_count   = 4
      dismiss_stale_reviews            = true
      require_code_owner_review        = true
      required_review_thread_resolution = true
    }

    # Block merge until all requirements met
    required_deployments {
      required_deployment_environments = ["council-approval"]
    }
  }
}

# Automated workflow for amendment tracking
resource "github_repository_file" "amendment_workflow" {
  repository = "the-covenant"
  file       = ".github/workflows/amendment-process.yml"
  content = templatefile("${path.module}/templates/amendment-workflow.yml", {
    citadel_repo = "the-citadel"
  })
}
```

Branch naming enforcement for proposals:

```yaml
# .github/workflows/proposal-validation.yml
name: Amendment Proposal Validation
on:
  pull_request:
    branches: [main]
    paths: ['GOVERNANCE.md', 'PRINCIPLES.md', 'HUMAN_MANDATE.md']

jobs:
  validate-proposal:
    runs-on: ubuntu-latest
    steps:
      - name: Check branch naming
        run: |
          if [[ ! "${{ github.head_ref }}" =~ ^proposal/ ]]; then
            echo "Amendment proposals must use branch naming: proposal/[brief-description]"
            exit 1
          fi

      - name: Validate proposal template
        run: |
          # Check PR description contains required sections
          if ! echo "${{ github.event.pull_request.body }}" | grep -q "## The Change"; then
            echo "Missing required section: The Change"
            exit 1
          fi
          # Additional template validation...
```

### Automated Validation

Debate period and quorum tracking:

```python
# scripts/amendment-tracker.py
import datetime
import github
from typing import List, Dict

class AmendmentTracker:
    def __init__(self, repo: str):
        self.repo = github.Github().get_repo(repo)

    def validate_debate_period(self, pr_number: int) -> bool:
        """Ensure minimum 72-hour debate period"""
        pr = self.repo.get_pull(pr_number)
        created = pr.created_at
        now = datetime.datetime.now(created.tzinfo)

        debate_hours = (now - created).total_seconds() / 3600

        # Check if major change (requires 1 week)
        if self.is_major_change(pr):
            return debate_hours >= 168  # 1 week
        return debate_hours >= 72  # 72 hours

    def check_council_quorum(self, pr_number: int) -> Dict[str, bool]:
        """Verify council composition requirements"""
        pr = self.repo.get_pull(pr_number)
        approvals = [review for review in pr.get_reviews()
                    if review.state == "APPROVED"]

        watchers = self.get_team_members("watchers")
        mentors = self.get_team_members("mentors")

        watcher_approvals = sum(1 for approval in approvals
                               if approval.user.login in watchers)
        mentor_approvals = sum(1 for approval in approvals
                              if approval.user.login in mentors)

        return {
            "quorum_met": watcher_approvals >= 2 and mentor_approvals >= 2,
            "watcher_count": watcher_approvals,
            "mentor_count": mentor_approvals,
            "different_clans": self.verify_clan_diversity(approvals)
        }
```

### Human Process

Amendment proposal requirements:

1. **Branch Creation**: `proposal/[brief-description]` naming convention
2. **PR Template**: Must include all required sections:
   - **The Change**: Specific modification being proposed
   - **The Rationale**: Why this change is necessary
   - **The Impact**: Effect on daily operations
   - **The Implementation**: Required the-citadel changes

3. **Debate Period**:
   - 72 hours minimum for minor changes
   - 1 week for major governance changes
   - All Immortals may participate and suggest modifications

4. **Council Review Process**:
   - Quorum: 2 Watchers + 2 Mentors from different clans
   - Consensus required (no blocking objections)
   - Veto power for Watchers on core value violations

5. **Proclamation Phase**:
   - Announcement in #engineering-announcements
   - Auto-creation of implementation issue in the-citadel
   - Co-author attribution to all approvers
   - Decision recording in REFERENCE/decisions/

## Compliance Verification

### Automated Checks

- **Branch Naming**: Workflow validates proposal/ prefix
- **Template Completeness**: PR body validation for required sections
- **Debate Period**: Automated timer prevents premature merge
- **Quorum Verification**: Team membership and approval count validation
- **Implementation Linking**: Automated issue creation in the-citadel

### Manual Audits

- **Monthly Review**: Council reviews amendment process effectiveness
- **Quarterly Assessment**: Measure debate participation and decision quality
- **Annual Governance Review**: Evaluate amendment process itself for improvements

### Reporting

Key metrics tracked:
- Average time from proposal to decision
- Participation rate in amendment debates
- Implementation lag (Covenant to Citadel)
- Amendment frequency and types
- Veto usage and reasoning

## Related Documents

- **Source**: [../the-covenant/GOVERNANCE.md - The Ritual of Amendment](../the-covenant/GOVERNANCE.md#the-ritual-of-amendment)
- **Related Policies**:
  - [GOV-001: Living Principles](./gov-001-living-principles.md)
  - [GOV-006: Council Decision Quorum](./gov-006-decision-quorum.md)
- **Implementation**: [the-citadel terraform/github/](../the-citadel/terraform/github/)

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-09-30 | 1.0 | Initial policy creation from GOVERNANCE.md Ritual of Amendment | Claude Code |
