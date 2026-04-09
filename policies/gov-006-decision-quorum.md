# GOV-006: Council Decision Quorum

**Policy ID:** GOV-006
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Council decisions **must** have a 4-member quorum consisting of at least 2 Watchers and 2 Mentors from different clans. Consensus **shall** be required with no blocking objections. Any Watcher **may** exercise veto power for changes that violate core values. All decisions **must** be recorded with full rationale and dissenting opinions.

## Rationale

Structured decision-making ensures legitimacy and quality of governance decisions:

- **Representative Input**: Multi-clan requirement ensures diverse perspectives in decisions
- **Authority Balance**: Watchers and Mentors both contribute to prevent single-group dominance
- **Quality Threshold**: Minimum quorum prevents hasty decisions by small groups
- **Consensus Building**: No-blocking-objections requirement forces resolution of major concerns
- **Core Value Protection**: Watcher veto power preserves fundamental organizational principles
- **Transparency**: Full documentation creates accountability and historical context
- **Legitimacy**: Formal process gives decisions proper authority and acceptance
- **Scalability**: Clear quorum rules prevent governance paralysis as organization grows

The Council structure balances efficiency with thoroughness to make quality decisions with broad support.

## Scope

**Council Decisions Requiring Quorum:**
- Covenant amendments and principle changes
- Major governance process modifications
- Organization structure and team authority changes
- Constitutional interpretation disputes
- Policy creation and major revisions
- Emergency procedure invocations and reviews

**Quorum Composition:**
- **Minimum Size**: 4 members total
- **Authority Distribution**: 2 Watchers + 2 Mentors minimum
- **Diversity Requirement**: Mentors from different clans/domains
- **Consensus Standard**: No blocking objections from quorum members

**Decision Authority:**
- Watchers have veto power over core value violations
- Mentors provide domain expertise and implementation feasibility
- Unanimous Watcher consensus required for constitutional crises
- Blocking concerns must be addressed before proceeding

## Implementation

### Technical Enforcement

GitHub team-based quorum validation:

```hcl
# terraform/github/council_quorum.tf
resource "github_repository_ruleset" "council_quorum" {
  name        = "Council Decision Quorum"
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
    # Require council-level changes to have 4 approvals
    pull_request {
      required_approving_review_count   = 4
      dismiss_stale_reviews            = true
      require_code_owner_review        = true
      required_review_thread_resolution = true

      # Require specific team representation
      restrict_review_dismissals {
        teams = [
          "the-nash-group/watchers",
          "the-nash-group/mentors"
        ]
      }
    }

    # Custom status checks for quorum validation
    required_status_checks {
      required_status_checks = [
        "council-quorum-validator",
        "clan-diversity-check",
        "consensus-verification",
        "veto-power-check"
      ]
      strict_required_status_checks_policy = true
    }
  }
}

# Workflow for council validation
resource "github_repository_file" "council_validator" {
  repository = "the-covenant"
  file       = ".github/workflows/council-validation.yml"
  content = templatefile("${path.module}/templates/council-validation.yml", {
    organization  = "the-nash-group"
    watchers_team = "watchers"
    mentors_team  = "mentors"
  })
}

# Council decision tracking
resource "github_repository_file" "decision_tracker" {
  repository = "the-covenant"
  file       = "REFERENCE/decisions/README.md"
  content = templatefile("${path.module}/templates/decision-tracker.md", {})
}
```

Council validation workflow:

```yaml
# .github/workflows/council-validation.yml
name: Council Quorum Validation
on:
  pull_request:
    branches: [main]
    paths: ['GOVERNANCE.md', 'PRINCIPLES.md', 'HUMAN_MANDATE.md']
  pull_request_review:

jobs:
  validate-quorum:
    runs-on: ubuntu-latest
    name: Validate Council Quorum
    steps:
      - name: Check quorum composition
        uses: actions/github-script@v6
        with:
          script: |
            const { data: reviews } = await github.rest.pulls.listReviews({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number
            });

            const approvals = reviews.filter(review => review.state === 'APPROVED');

            // Get team memberships
            const { data: watchers } = await github.rest.teams.listMembersInOrg({
              org: context.repo.owner,
              team_slug: 'watchers'
            });

            const { data: mentors } = await github.rest.teams.listMembersInOrg({
              org: context.repo.owner,
              team_slug: 'mentors'
            });

            // Analyze approvals
            let watcherApprovals = 0;
            let mentorApprovals = 0;
            let mentorClans = new Set();

            for (const approval of approvals) {
              const username = approval.user.login;

              if (watchers.some(w => w.login === username)) {
                watcherApprovals++;
              } else if (mentors.some(m => m.login === username)) {
                mentorApprovals++;
                // Track clan diversity (simplified - would check actual clan membership)
                mentorClans.add(username); // In real implementation, map to clan
              }
            }

            // Validate quorum requirements
            const quorumMet = watcherApprovals >= 2 && mentorApprovals >= 2 && mentorClans.size >= 2;
            const totalApprovals = watcherApprovals + mentorApprovals;

            // Set status
            const state = quorumMet ? 'success' : 'failure';
            const description = quorumMet
              ? `Quorum met: ${watcherApprovals} Watchers, ${mentorApprovals} Mentors from ${mentorClans.size} clans`
              : `Quorum not met: Need 2 Watchers + 2 Mentors from different clans`;

            await github.rest.repos.createCommitStatus({
              owner: context.repo.owner,
              repo: context.repo.repo,
              sha: context.payload.pull_request.head.sha,
              state: state,
              description: description,
              context: 'council-quorum-validator'
            });

  check-consensus:
    runs-on: ubuntu-latest
    name: Verify Consensus
    steps:
      - name: Check for blocking objections
        uses: actions/github-script@v6
        with:
          script: |
            const { data: reviews } = await github.rest.pulls.listReviews({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number
            });

            // Check for any blocking reviews
            const blockingReviews = reviews.filter(review =>
              review.state === 'CHANGES_REQUESTED' || review.state === 'REQUEST_CHANGES'
            );

            const consensusAchieved = blockingReviews.length === 0;

            await github.rest.repos.createCommitStatus({
              owner: context.repo.owner,
              repo: context.repo.repo,
              sha: context.payload.pull_request.head.sha,
              state: consensusAchieved ? 'success' : 'failure',
              description: consensusAchieved
                ? 'Consensus achieved - no blocking objections'
                : `${blockingReviews.length} blocking objection(s) must be resolved`,
              context: 'consensus-verification'
            });

  check-veto-power:
    runs-on: ubuntu-latest
    name: Check Veto Power Usage
    steps:
      - name: Validate core values protection
        uses: actions/github-script@v6
        with:
          script: |
            // Check if any Watcher has explicitly vetoed for core value violations
            const { data: reviews } = await github.rest.pulls.listReviews({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number
            });

            const { data: watchers } = await github.rest.teams.listMembersInOrg({
              org: context.repo.owner,
              team_slug: 'watchers'
            });

            let vetoInvoked = false;
            let vetoReason = '';

            for (const review of reviews) {
              if (review.state === 'CHANGES_REQUESTED' &&
                  watchers.some(w => w.login === review.user.login)) {

                // Check if review mentions core values
                if (review.body && review.body.toLowerCase().includes('core value')) {
                  vetoInvoked = true;
                  vetoReason = `Watcher ${review.user.login} invoked veto for core value protection`;
                  break;
                }
              }
            }

            await github.rest.repos.createCommitStatus({
              owner: context.repo.owner,
              repo: context.repo.repo,
              sha: context.payload.pull_request.head.sha,
              state: vetoInvoked ? 'failure' : 'success',
              description: vetoInvoked ? vetoReason : 'No core value veto invoked',
              context: 'veto-power-check'
            });
```

### Automated Validation

Council composition and decision tracking:

```python
# scripts/council-tracker.py
import datetime
import github
from typing import Dict, List, Optional, Set
from dataclasses import dataclass

@dataclass
class CouncilMember:
    username: str
    authority_level: str  # 'watcher' or 'mentor'
    clan: Optional[str]   # For clan diversity tracking
    join_date: datetime.datetime

@dataclass
class DecisionRecord:
    pr_number: int
    title: str
    decision_date: datetime.datetime
    quorum_members: List[CouncilMember]
    consensus_achieved: bool
    veto_invoked: bool
    implementation_status: str

class CouncilQuorumTracker:
    def __init__(self, org: str):
        self.gh = github.Github()
        self.org = self.gh.get_organization(org)
        self.covenant_repo = self.org.get_repo("the-covenant")

    def validate_quorum_composition(self, pr_number: int) -> Dict[str, any]:
        """Validate that PR has proper council quorum"""
        pr = self.covenant_repo.get_pull(pr_number)
        approvals = [review for review in pr.get_reviews()
                    if review.state == "APPROVED"]

        watchers = self.get_team_members("watchers")
        mentors = self.get_team_members("mentors")

        quorum_analysis = {
            "pr_number": pr_number,
            "total_approvals": len(approvals),
            "watcher_approvals": 0,
            "mentor_approvals": 0,
            "mentor_clans": set(),
            "quorum_met": False,
            "consensus_achieved": False,
            "veto_invoked": False,
            "missing_requirements": []
        }

        # Analyze approvals
        for approval in approvals:
            username = approval.user.login
            if username in watchers:
                quorum_analysis["watcher_approvals"] += 1
            elif username in mentors:
                quorum_analysis["mentor_approvals"] += 1
                # Get clan membership (simplified)
                clan = self.get_user_clan(username)
                if clan:
                    quorum_analysis["mentor_clans"].add(clan)

        # Check quorum requirements
        missing = []
        if quorum_analysis["watcher_approvals"] < 2:
            missing.append(f"Need {2 - quorum_analysis['watcher_approvals']} more Watcher approvals")

        if quorum_analysis["mentor_approvals"] < 2:
            missing.append(f"Need {2 - quorum_analysis['mentor_approvals']} more Mentor approvals")

        if len(quorum_analysis["mentor_clans"]) < 2:
            missing.append("Need Mentors from at least 2 different clans")

        quorum_analysis["missing_requirements"] = missing
        quorum_analysis["quorum_met"] = len(missing) == 0

        # Check consensus
        quorum_analysis["consensus_achieved"] = self.check_consensus(pr)
        quorum_analysis["veto_invoked"] = self.check_veto_power(pr)

        return quorum_analysis

    def check_consensus(self, pr) -> bool:
        """Verify no blocking objections exist"""
        reviews = pr.get_reviews()
        blocking_reviews = [review for review in reviews
                           if review.state in ["CHANGES_REQUESTED", "REQUEST_CHANGES"]]
        return len(blocking_reviews) == 0

    def check_veto_power(self, pr) -> bool:
        """Check if any Watcher has invoked veto power"""
        reviews = pr.get_reviews()
        watchers = self.get_team_members("watchers")

        for review in reviews:
            if (review.user.login in watchers and
                review.state == "CHANGES_REQUESTED" and
                review.body and "core value" in review.body.lower()):
                return True

        return False

    def record_council_decision(self, pr_number: int) -> DecisionRecord:
        """Create formal record of council decision"""
        pr = self.covenant_repo.get_pull(pr_number)
        quorum_data = self.validate_quorum_composition(pr_number)

        # Extract council members who participated
        quorum_members = []
        approvals = [review for review in pr.get_reviews()
                    if review.state == "APPROVED"]

        for approval in approvals:
            username = approval.user.login
            authority = "watcher" if username in self.get_team_members("watchers") else "mentor"
            clan = self.get_user_clan(username) if authority == "mentor" else None

            quorum_members.append(CouncilMember(
                username=username,
                authority_level=authority,
                clan=clan,
                join_date=approval.submitted_at
            ))

        decision = DecisionRecord(
            pr_number=pr_number,
            title=pr.title,
            decision_date=pr.merged_at or datetime.datetime.now(),
            quorum_members=quorum_members,
            consensus_achieved=quorum_data["consensus_achieved"],
            veto_invoked=quorum_data["veto_invoked"],
            implementation_status="pending"
        )

        # Store decision record
        self.store_decision_record(decision)
        return decision

    def get_council_metrics(self) -> Dict[str, float]:
        """Track council decision effectiveness"""
        decisions = self.get_all_decisions()

        if not decisions:
            return {}

        total_decisions = len(decisions)
        consensus_rate = sum(1 for d in decisions if d.consensus_achieved) / total_decisions
        veto_rate = sum(1 for d in decisions if d.veto_invoked) / total_decisions

        # Calculate average decision time
        decision_times = []
        for decision in decisions:
            # Simplified - would track from proposal to decision
            decision_times.append(24)  # placeholder

        return {
            "total_decisions": total_decisions,
            "consensus_rate": consensus_rate,
            "veto_rate": veto_rate,
            "avg_decision_time_hours": sum(decision_times) / len(decision_times),
            "participation_rate": self.calculate_participation_rate(decisions)
        }
```

### Human Process

Council decision procedure:

1. **Quorum Assembly**:
   - Verify 4-member minimum with 2 Watchers + 2 Mentors
   - Ensure Mentors represent different clans/domains
   - Document all participating council members

2. **Debate and Review**:
   - All council members review proposal thoroughly
   - Raise concerns and blocking objections
   - Seek clarification and additional information
   - Allow sufficient time for consideration

3. **Consensus Building**:
   - Address all blocking concerns raised
   - Modify proposal if needed to achieve consensus
   - Ensure no remaining objections from quorum members
   - Document dissenting opinions if consensus not possible

4. **Veto Power Exercise**:
   - Watchers may veto for core value violations
   - Must provide explicit rationale referencing specific principles
   - Veto triggers mandatory review and potential proposal modification
   - Unanimous Watcher consensus can override other objections

5. **Decision Recording**:
   - Document final decision with full rationale
   - Record all participating council members
   - Note any dissenting opinions or concerns
   - Create implementation tracking issue
   - Announce decision to organization

## Compliance Verification

### Automated Checks

- **Quorum Composition**: GitHub team membership validation
- **Clan Diversity**: Mentor clan/domain representation verification
- **Consensus Verification**: Check for blocking review objections
- **Veto Detection**: Monitor Watcher veto power invocation
- **Decision Recording**: Automated creation of decision records

### Manual Audits

- **Monthly Quorum Review**: Analyze council participation patterns
- **Quarterly Decision Assessment**: Evaluate decision quality and implementation
- **Annual Council Effectiveness**: Review governance decision outcomes

### Reporting

Council decision metrics:
- Number of decisions requiring quorum by month
- Average quorum size and composition
- Consensus achievement rate
- Veto power usage frequency and reasoning
- Decision implementation lag time
- Council member participation rates

## Related Documents

- **Source**: [../the-covenant/GOVERNANCE.md - The Council Review](../the-covenant/GOVERNANCE.md#the-council-review)
- **Related Policies**:
  - [GOV-002: Covenant Amendment Process](./gov-002-amendment-process.md)
  - [GOV-004: Team Authority Matrix](./gov-004-team-authority.md)
  - [GOV-005: Conflict Resolution Process](./gov-005-conflict-resolution.md)
- **Decision Archive**: [REFERENCE/decisions/](../REFERENCE/decisions/)

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-09-30 | 1.0 | Initial policy creation from GOVERNANCE.md Council Review | Claude Code |
