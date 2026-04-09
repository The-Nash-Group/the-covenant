# SC-002: Conventional Commits

**Policy ID:** SC-002
**Category:** Source Control
**Effective Date:** 2024-08-01
**Last Updated:** 2024-09-30

## Statement

All commits to protected branches **must** follow Conventional Commits format. Pull request titles **shall** be meaningful and become the squash commit message. Commit messages like "Fix stuff" or "Update code" **are forbidden**.

## Rationale

"Fix stuff" and "Update code" are not messages—they are admissions of defeat. When debugging production at 3 AM, clear commit messages are the difference between quick resolution and despair. Our Git history is not just a record; it's a diagnostic tool that must tell the story of every change and its purpose.

A well-crafted commit message answers three questions:
1. **What** changed?
2. **Why** did it change?
3. **How** does it impact the system?

## Scope

**Applies To:**
- All commits that will be merged to `main` or protected branches
- Pull request titles (which become squash commit messages)
- All repositories under The Nash Group organization

**Exceptions:**
- Work-in-progress commits on feature branches (before squashing)
- Automated commits from dependency updates (handled by Renovate)

## Implementation

### Technical Enforcement

In `the-citadel/terraform/github/rulesets.tf`:

```hcl
resource "github_repository_ruleset" "conventional_commits" {
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
  }

  rules {
    commit_message_pattern {
      operator = "starts_with"
      pattern  = "^(feat|fix|docs|chore|refactor|perf|test|build|ci|revert)(\\(.+\\))?: .+"
      name     = "Conventional Commits"
      negate   = false
    }
  }
}
```

### Automated Validation

- **Commit Message Linting**: CI pipeline validates all PR titles
- **Pre-merge Hook**: GitHub ruleset blocks non-conforming commits
- **Template Enforcement**: PR templates guide proper title format

### Human Process

1. **PR Creation**: Author must write clear, conventional title
2. **Review Process**: Judge role verifies commit message clarity
3. **Merge Process**: Squash-and-merge preserves conventional format

## Required Format

### Standard Pattern
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Allowed Types
- **feat**: New feature for the user
- **fix**: Bug fix for the user
- **docs**: Documentation changes
- **style**: Formatting, missing semicolons, etc.
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding missing tests or correcting existing ones
- **build**: Changes affecting build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Regular maintenance tasks
- **revert**: Reverting a previous commit

### Examples

**Good:**
- `feat(auth): add OAuth2 integration for GitHub login`
- `fix(api): resolve race condition in user session handling`
- `docs(readme): update installation instructions for Docker setup`

**Bad:**
- `fix stuff`
- `update`
- `changes`
- `WIP`
- `asdf`

## Compliance Verification

**Automated Checks:**
- GitHub ruleset enforcement prevents invalid commits
- CI pipeline validates PR titles against conventional format
- Repository audit scans commit history weekly

**Manual Audits:**
- Quarterly review of commit message quality
- Mentors assess clarity and usefulness during reviews

**Reporting:**
- Violations blocked and logged in audit trail
- Monthly metrics on commit message compliance

## Violation Response

**Prevention:**
- GitHub ruleset blocks non-conforming commits automatically
- PR template guides authors to correct format
- Clear error messages explain expected format

**Correction:**
- Non-conforming PR titles must be updated before merge
- Feature branch commits can be messy (cleaned up during squash)

## Benefits

- **Debugging Efficiency**: Clear history accelerates problem diagnosis
- **Automated Tooling**: Enables semantic versioning and changelog generation
- **Code Archaeology**: Future developers understand the "why" behind changes
- **Release Management**: Automated identification of breaking changes vs. patches

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 2: Every Commit Shall Speak Its Purpose](../PRINCIPLES.md#principle-2-every-commit-shall-speak-its-purpose)
- **Governance Authority:** [GOVERNANCE.md - Mentors (Code Review)](../GOVERNANCE.md#the-mentors-maintainerscodeowners)
- **Implementation:** `the-citadel/terraform/github/rulesets.tf`
- **Complementary Policies:** [SC-001 Linear History](./sc-001-linear-history.md), [COM-001 Git Workflow Standards](./com-001-git-workflow.md)

## Change History

- **2024-08-01** - Initial creation based on Principle 2
- **2024-09-30** - Added detailed examples and compliance verification procedures
