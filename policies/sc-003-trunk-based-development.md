# SC-003: Trunk-Based Development

**Policy ID:** SC-003
**Category:** Source Control
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

We practice Trunk-Based Development. Feature branches **must** live for days, not months. The `main` branch is the single source of truth, and long-lived branches are parallel universes that diverge from reality.

## Rationale

Long-lived branches are parallel universes that diverge from reality. The pain of merging grows exponentially with time. Small, frequent integrations reduce risk and increase velocity:

- **Integration Hell**: Large merges become archaeological expeditions
- **Merge Conflicts**: Complexity increases exponentially with branch age
- **Stale Context**: Long branches lose sight of evolving requirements
- **Feature Isolation**: Features developed in isolation miss integration issues
- **Delayed Feedback**: Late integration discovery of conflicts and issues
- **Deployment Risk**: Big merges create big deployment risks

Small PR metrics tracked and celebrated, feature flags preferred over feature branches.

## Scope

**Applies To:**
- All development workflows across The Nash Group
- All feature branches in application and infrastructure repositories
- All pull requests and merge strategies
- All team collaboration and integration practices

**Exceptions:**
- Release branches (short-lived, specific versioning purpose)
- Hotfix branches (immediate production issue resolution)
- Experimental spike branches (clearly labeled, time-boxed)

## Implementation

### Technical Enforcement

In `the-citadel/terraform/github/rulesets.tf`:

```hcl
# Branch lifecycle management
resource "github_repository_ruleset" "trunk_based_development" {
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      exclude = ["~DEFAULT_BRANCH", "release/*", "hotfix/*"]
    }
  }

  rules {
    creation_allowed = true
    deletion_allowed = true

    # Encourage small, fast-moving branches
    pull_request {
      required_approving_review_count = 1
      dismiss_stale_reviews_on_push  = false  # Allow fast iteration
    }
  }
}
```

GitHub Actions workflow for branch hygiene:

```yaml
# .github/workflows/branch-hygiene.yml
name: Branch Hygiene
on:
  schedule:
    - cron: '0 9 * * MON'  # Weekly Monday check

jobs:
  stale-branch-cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Identify stale branches
        run: |
          # Find branches older than 14 days
          git for-each-ref --format='%(refname:short) %(committerdate)' refs/remotes/origin/ | \
          awk '$2 <= "'$(date -d '14 days ago' --iso-8601)'"' > stale-branches.txt

      - name: Notify owners of stale branches
        run: |
          # Create issues for stale branches
          while read branch date; do
            if [[ $branch != "main" && $branch != "release/*" ]]; then
              gh issue create --title "Stale branch: $branch" \
                --body "Branch $branch is over 14 days old. Please merge or close."
            fi
          done < stale-branches.txt
```

### Automated Validation

**Branch Age Monitoring:**
- Daily reports on branch age and activity
- Automated notifications for branches older than 7 days
- Weekly cleanup suggestions for stale branches

**Small PR Encouragement:**
- PR size metrics tracking (lines changed, files modified)
- Automated suggestions for PR splitting when size thresholds exceeded
- Recognition and metrics for small, focused PRs

**Integration Frequency:**
- Metrics on time between branch creation and merge
- Team dashboards showing integration velocity
- Alerts when integration frequency drops below targets

### Human Process

1. **Feature Planning**: Break large features into small, incremental changes
2. **Branch Creation**: Create branches from latest main, keep scope minimal
3. **Regular Integration**: Merge to main frequently, rebase to stay current
4. **Feature Flags**: Use feature toggles instead of long-lived feature branches
5. **Continuous Deployment**: Enable frequent, low-risk deployments

## Development Practices

### Feature Flag Strategy

**Instead of Long Branches:**
```javascript
// Use feature flags for incomplete features
if (featureFlags.isEnabled('new-user-dashboard')) {
  return <NewUserDashboard />;
}
return <LegacyUserDashboard />;
```

**Progressive Rollout:**
- Deploy code to main with features disabled
- Enable features gradually via configuration
- Monitor and rollback via flags, not code changes

### Branch Naming Conventions

**Approved Patterns:**
- `feat/user-authentication` (feature development)
- `fix/login-timeout-issue` (bug fixes)
- `chore/update-dependencies` (maintenance)
- `docs/api-documentation` (documentation)

**Lifecycle Indicators:**
- `spike/performance-investigation` (experimental, time-boxed)
- `hotfix/critical-security-patch` (production emergency)

### Integration Strategies

**Preferred Approach:**
1. **Small, Focused Changes**: Single responsibility per PR
2. **Frequent Rebasing**: Keep branches current with main
3. **Fast Review Cycles**: Prioritize quick feedback over perfect code
4. **Incremental Delivery**: Ship working increments regularly

## Compliance Verification

**Automated Checks:**
- Branch age monitoring and alerting
- PR size metrics and recommendations
- Integration frequency tracking
- Stale branch cleanup automation

**Manual Audits:**
- Weekly review of branch hygiene and integration practices
- Monthly assessment of feature flag usage and effectiveness
- Quarterly analysis of integration velocity and quality metrics

**Reporting:**
- Real-time dashboard of branch health and integration metrics
- Weekly team reports on integration velocity and branch hygiene
- Monthly trend analysis of development flow and efficiency

## Team Culture and Incentives

### Metrics That Matter

**Positive Indicators:**
- Average branch lifespan under 3 days
- PR size under 200 lines of code
- Integration frequency over 2 merges per developer per week
- Feature flag adoption rate

**Anti-Patterns to Avoid:**
- Branches older than 14 days (automatic flagging)
- PRs larger than 500 lines (require justification)
- Integration gaps longer than 1 week
- Feature development without flags

### Recognition Programs

**Small PR Champions:**
- Monthly recognition for consistently small, focused PRs
- Metrics dashboard highlighting efficient integration practices
- Team retrospectives celebrating integration success stories

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 7: The Trunk is Sacred](../the-covenant/PRINCIPLES.md#principle-7-the-trunk-is-sacred)
- **Governance Authority:** [GOVERNANCE.md - Development Standards](../the-covenant/GOVERNANCE.md#stronghold-decisions-individual-repositories)
- **Implementation:** `the-citadel/terraform/github/rulesets.tf`, `.github/workflows/`
- **Feature Management:** [DEP-001 Breaking Change Management](./dep-001-breaking-changes.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 7: The Trunk is Sacred
