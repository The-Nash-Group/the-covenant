# SC-001: Linear Git History

**Policy ID:** SC-001
**Category:** Source Control
**Effective Date:** 2024-08-01
**Last Updated:** 2024-09-30

## Statement

The `main` branch **must** maintain a linear, clean history. All commits to `main` **shall** be meaningful and tell the story of our code's evolution. Merge commits, force pushes, and branch deletions **are forbidden** on protected branches.

## Rationale

We learned from the chaos of tangled merge commits, where debugging became archaeology and rollbacks became gambling. A messy Git history is a confused chronicle that obscures the true story of our code's evolution. When production breaks at 3 AM, a linear history is the difference between quick diagnosis and prolonged outage.

The sacred timeline represents our production truth and must be treated with reverence.

## Scope

**Applies To:**
- All repositories under The Nash Group organization
- The `main` branch and any other protected branches (e.g., `release/*`)
- All commits that will become part of the permanent history

**Exceptions:**
- Feature branches may have non-linear history during development
- Emergency hotfix branches (with mandatory post-incident cleanup)

## Implementation

### Technical Enforcement

In `the-citadel/terraform/github/rulesets.tf`:

```hcl
resource "github_repository_ruleset" "sacred_timeline" {
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH", "release/*"]
      exclude = []
    }
  }

  rules {
    required_linear_history = true
    deletion                = false
    force_push              = false
    creation                = true
  }
}
```

### Automated Validation

- **Pre-merge Validation**: GitHub branch protection prevents non-linear merges
- **CI Integration**: Squash-and-merge enforced for all pull requests
- **History Auditing**: Weekly automated scan for history anomalies

### Human Process

1. **Pull Request Strategy**: All changes must use "Squash and merge"
2. **Commit Message**: PR title becomes the squash commit message (must follow SC-002)
3. **Review Requirement**: Judge role must verify PR follows linear history principles

## Compliance Verification

**Automated Checks:**
- GitHub ruleset enforcement prevents violations in real-time
- `git log --graph --oneline` auditing via CI weekly
- Alert on any non-fast-forward pushes attempted

**Manual Audits:**
- Monthly review of commit graph topology
- Quarterly assessment of merge strategy effectiveness

**Reporting:**
- Violations logged in organization audit trail
- Branch protection bypass attempts tracked and reported

## Violation Response

**Immediate:**
- Attempted violations are automatically blocked by GitHub
- Repository push rejected with clear error message

**Corrective Action:**
- If somehow bypassed, immediate force-push to restore linear history
- Post-incident review of how protection was circumvented
- Strengthening of technical controls

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 1: The Sacred Timeline is Linear and Clean](../PRINCIPLES.md#principle-1-the-sacred-timeline-is-linear-and-clean)
- **Governance Authority:** [GOVERNANCE.md - Mentors (Code Quality)](../GOVERNANCE.md#the-mentors-maintainerscodeowners)
- **Implementation:** `the-citadel/terraform/github/rulesets.tf`
- **Complementary Policies:** [SC-002 Conventional Commits](./sc-002-conventional-commits.md)

## Change History

- **2024-08-01** - Initial creation based on Principle 1
- **2024-09-30** - Added violation response procedures and compliance verification details
