# COM-001: Git Workflow Standards

**Policy ID:** COM-001
**Category:** Source Control
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

The `main` branch **must** represent production truth with linear, readable, and meaningful history. Every commit **must** follow Conventional Commits format and speak its purpose clearly.

## Rationale

We learned from the chaos of tangled merge commits, where debugging became archaeology and rollbacks became gambling. A messy Git history is a confused chronicle that obscures the true story of our code's evolution:

- **Debugging Difficulty**: Tangled history makes finding the source of issues nearly impossible
- **Rollback Risk**: Complex merge history makes safe rollbacks dangerous
- **Code Archeology**: Understanding change context requires detective work instead of clear history
- **Commit Message Chaos**: "Fix stuff" and "Update code" provide no useful information during incidents
- **Integration Conflicts**: Non-linear history creates complex merge conflicts and integration issues
- **Audit Compliance**: Unclear change history complicates compliance and security auditing

Linear, well-documented Git history enables rapid debugging, safe rollbacks, and clear understanding of code evolution.

## Scope

**Applies To:**
- All Git repositories owned by The Nash Group organization
- All branches that will eventually merge to main/master
- All commit messages in production branches
- All pull request titles and descriptions
- All release tagging and versioning

**Exceptions:**
- Personal development branches (before PR creation)
- Experimental repositories marked with `experimental` topic
- Forked repositories where we don't control the workflow

## Implementation

### Technical Enforcement

GitHub rulesets enforcing Git workflow standards:

```hcl
# terraform/github/git_workflow.tf
resource "github_repository_ruleset" "sacred_timeline" {
  name        = "The Great Charter - Sacred Timeline"
  repository  = github_repository.service.name
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
  }

  rules {
    # Linear history requirement
    required_linear_history = true

    # Branch protection
    deletion                = false
    force_push              = false
    non_fast_forward        = false

    # Require squash merges to maintain linearity
    pull_request {
      required_approving_review_count = 1
      dismiss_stale_reviews_on_push  = true
      require_code_owner_review       = true
    }
  }

  labels = {
    "nash.group/policy"    = "com-001"
    "nash.group/component" = "git-workflow"
    "nash.group/team"      = var.team_name
  }
}

resource "github_repository_ruleset" "covenant_of_commits" {
  name        = "Covenant of Commits - Message Standards"
  repository  = github_repository.service.name
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
  }

  rules {
    # Conventional commits enforcement
    commit_message_pattern {
      operator = "starts_with"
      pattern  = "^(feat|fix|docs|chore|refactor|perf|test|build|ci|revert)(\\(.+\\))?: .+"
      name     = "Conventional Commits Format"
      negate   = false
    }

    # Minimum commit message length
    commit_message_pattern {
      operator = "regex"
      pattern  = "^.{10,}$"
      name     = "Minimum Message Length"
      negate   = false
    }
  }

  labels = {
    "nash.group/policy"    = "com-001"
    "nash.group/component" = "commit-standards"
    "nash.group/team"      = var.team_name
  }
}
```

Automated commit message and PR validation:

```yaml
# .github/workflows/git-workflow-validation.yml
name: Git Workflow Validation
on:
  pull_request:
    branches: [main, master]

jobs:
  validate-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Validate Commit Messages
        run: |
          echo "Validating commit messages for conventional commits format..."

          # Get commits in this PR
          commits=$(git rev-list --reverse origin/main..HEAD)

          for commit in $commits; do
            message=$(git log --format=%s -n 1 $commit)
            echo "Checking commit: $commit"
            echo "Message: $message"

            # Check conventional commits format
            if ! echo "$message" | grep -qE "^(feat|fix|docs|chore|refactor|perf|test|build|ci|revert)(\(.+\))?: .+"; then
              echo "❌ Commit $commit does not follow conventional commits format"
              echo "Expected: type(scope): description"
              echo "Examples:"
              echo "  feat(api): add user authentication endpoint"
              echo "  fix(db): resolve connection timeout issue"
              echo "  docs(readme): update installation instructions"
              exit 1
            fi

            # Check minimum length
            if [ ${#message} -lt 10 ]; then
              echo "❌ Commit message too short: $message"
              echo "Minimum 10 characters required"
              exit 1
            fi

            # Check for banned phrases
            if echo "$message" | grep -qiE "(fix stuff|update code|misc|wip|tmp|temporary)"; then
              echo "❌ Commit message too vague: $message"
              echo "Please provide specific description of changes"
              exit 1
            fi

            echo "✅ Commit $commit format valid"
          done

      - name: Validate PR Title
        run: |
          echo "Validating PR title format..."
          pr_title="${{ github.event.pull_request.title }}"

          # PR title should also follow conventional commits
          if ! echo "$pr_title" | grep -qE "^(feat|fix|docs|chore|refactor|perf|test|build|ci|revert)(\(.+\))?: .+"; then
            echo "❌ PR title does not follow conventional commits format"
            echo "Current title: $pr_title"
            echo "Expected format: type(scope): description"
            exit 1
          fi

          echo "✅ PR title format valid: $pr_title"

      - name: Check Branch Naming
        run: |
          echo "Validating branch naming convention..."
          branch_name="${{ github.head_ref }}"

          # Valid branch patterns
          if echo "$branch_name" | grep -qE "^(feature|feat|fix|hotfix|docs|chore|refactor|perf|test)\/[a-z0-9-]+$"; then
            echo "✅ Branch name follows convention: $branch_name"
          else
            echo "❌ Branch name does not follow convention: $branch_name"
            echo "Expected patterns:"
            echo "  feature/user-authentication"
            echo "  fix/database-connection"
            echo "  docs/api-documentation"
            echo "  chore/update-dependencies"
            exit 1
          fi

      - name: Validate Linear History
        run: |
          echo "Validating linear history..."

          # Check for merge commits in the PR
          merge_commits=$(git rev-list --merges origin/main..HEAD)

          if [ -n "$merge_commits" ]; then
            echo "❌ Merge commits found in PR history"
            echo "Please rebase your branch to maintain linear history"
            echo "Merge commits found:"
            for commit in $merge_commits; do
              echo "  - $commit: $(git log --format=%s -n 1 $commit)"
            done
            exit 1
          fi

          echo "✅ Linear history maintained"

      - name: Generate Commit Summary
        run: |
          echo "## Git Workflow Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "**Branch**: ${{ github.head_ref }}" >> $GITHUB_STEP_SUMMARY
          echo "**Commits**: $(git rev-list --count origin/main..HEAD)" >> $GITHUB_STEP_SUMMARY
          echo "**Linear History**: ✅ Maintained" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### Commits in this PR" >> $GITHUB_STEP_SUMMARY

          git log --oneline --reverse origin/main..HEAD | while read line; do
            echo "- $line" >> $GITHUB_STEP_SUMMARY
          done
```

### Automated Validation

**Commit Message Standards:**
- Must follow Conventional Commits specification
- Minimum 10 characters in length
- Must not contain vague terms like "fix stuff" or "update code"
- Must provide meaningful description of changes

**Branch Naming Conventions:**
```bash
# Valid branch patterns
feature/user-authentication
fix/database-connection-timeout
docs/api-documentation-update
chore/dependency-updates
refactor/user-service-cleanup
perf/database-query-optimization
test/integration-test-coverage
hotfix/security-vulnerability-patch
```

**Git Workflow Automation:**
```bash
#!/bin/bash
# scripts/setup-git-hooks.sh
# Sets up local git hooks for workflow enforcement

set -euo pipefail

HOOKS_DIR=".git/hooks"

# Create commit-msg hook for conventional commits
cat > "$HOOKS_DIR/commit-msg" <<'EOF'
#!/bin/bash
# Validate commit message format

commit_regex='^(feat|fix|docs|chore|refactor|perf|test|build|ci|revert)(\(.+\))?: .+'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Invalid commit message format"
    echo "Expected: type(scope): description"
    echo "Examples:"
    echo "  feat(api): add user authentication"
    echo "  fix(db): resolve timeout issue"
    echo "  docs: update README"
    exit 1
fi

# Check minimum length
if [ $(wc -c < "$1") -lt 10 ]; then
    echo "❌ Commit message too short (minimum 10 characters)"
    exit 1
fi

echo "✅ Commit message format valid"
EOF

# Create pre-push hook for branch validation
cat > "$HOOKS_DIR/pre-push" <<'EOF'
#!/bin/bash
# Validate branch and commits before push

current_branch=$(git symbolic-ref --short HEAD)

# Skip validation for main/master
if [[ "$current_branch" =~ ^(main|master)$ ]]; then
    exit 0
fi

# Validate branch naming
if ! echo "$current_branch" | grep -qE "^(feature|feat|fix|hotfix|docs|chore|refactor|perf|test)\/[a-z0-9-]+$"; then
    echo "❌ Branch name doesn't follow convention: $current_branch"
    echo "Expected: type/description-with-dashes"
    exit 1
fi

# Check for merge commits
if git rev-list --merges HEAD ^origin/main | head -1 | grep -q .; then
    echo "❌ Merge commits detected. Please rebase to maintain linear history"
    exit 1
fi

echo "✅ Pre-push validation passed"
EOF

# Make hooks executable
chmod +x "$HOOKS_DIR/commit-msg"
chmod +x "$HOOKS_DIR/pre-push"

echo "Git hooks installed successfully"
echo "Hooks will enforce:"
echo "  - Conventional commit messages"
echo "  - Branch naming conventions"
echo "  - Linear history requirements"
```

### Human Process

1. **Branch Creation**: Create feature branches with conventional naming
2. **Commit Discipline**: Write clear, conventional commit messages as work progresses
3. **Rebase Workflow**: Use rebase to maintain linear history before merging
4. **PR Review**: Ensure PR titles follow conventional commits format
5. **Squash Merging**: Use squash merges to maintain clean main branch history

## Git Workflow Standards

### Conventional Commits Specification

**Commit Message Format:**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Required Types:**
- **feat**: A new feature for the user
- **fix**: A bug fix for the user
- **docs**: Documentation changes
- **chore**: Maintenance tasks, dependency updates
- **refactor**: Code changes that neither fix bugs nor add features
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Changes to build system or external dependencies
- **ci**: Changes to CI/CD configuration files and scripts
- **revert**: Reverts a previous commit

**Scope Examples:**
```bash
feat(api): add user authentication endpoint
fix(db): resolve connection pool timeout
docs(readme): add installation instructions
chore(deps): update lodash to v4.17.21
refactor(auth): simplify token validation logic
perf(query): optimize user lookup query
test(api): add integration tests for auth flow
build(docker): update base image to node:18
ci(github): add security scanning workflow
revert: feat(api): add user authentication endpoint
```

### Branch Management

**Branch Naming Convention:**
```bash
# Feature development
feature/user-profile-management
feat/oauth-integration

# Bug fixes
fix/memory-leak-user-service
hotfix/security-vulnerability

# Documentation
docs/api-reference-update
docs/deployment-guide

# Maintenance
chore/dependency-updates
chore/cleanup-unused-files

# Performance improvements
perf/database-indexing
perf/api-response-caching

# Testing
test/unit-test-coverage
test/integration-test-suite
```

**Branch Lifecycle:**
1. **Creation**: Branch from latest `main`
2. **Development**: Regular commits with conventional messages
3. **Sync**: Regular rebase with `main` to stay current
4. **Review**: Create PR when feature is complete
5. **Merge**: Squash merge to maintain linear history
6. **Cleanup**: Delete feature branch after merge

### Pull Request Standards

**PR Title Format:**
```bash
# Must follow conventional commits format
feat(auth): implement OAuth2 integration
fix(api): resolve timeout in user endpoint
docs(readme): update deployment instructions
```

**PR Description Template:**
```markdown
## Type of Change
- [ ] 🚀 New feature
- [ ] 🐛 Bug fix
- [ ] 📚 Documentation update
- [ ] 🔧 Maintenance/chore
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test updates

## Description
Brief description of what this PR accomplishes.

## Changes Made
- Specific change 1
- Specific change 2
- Specific change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Documentation
- [ ] Code comments added/updated
- [ ] README updated
- [ ] API documentation updated
- [ ] Changelog updated

## Breaking Changes
- [ ] This PR introduces breaking changes
- [ ] Migration guide created (if applicable)

## Related Issues
Closes #123
Related to #456
```

### Release Management

**Semantic Versioning:**
```bash
# Version format: MAJOR.MINOR.PATCH
# Example: 2.1.3

# MAJOR: Breaking changes
feat!: implement new authentication system
BREAKING CHANGE: old auth tokens no longer valid

# MINOR: New features (backward compatible)
feat(api): add user preferences endpoint

# PATCH: Bug fixes
fix(auth): resolve token expiration bug
```

**Release Tagging:**
```bash
# Create annotated tags for releases
git tag -a v2.1.3 -m "Release v2.1.3

feat(api): add user preferences endpoint
fix(auth): resolve token expiration bug
perf(db): optimize user queries"

# Tag format follows semantic versioning
# Tag message includes conventional commit summary
```

### Repository History Standards

**Linear History Enforcement:**
```bash
# Prohibited: Merge commits in main branch
git merge feature/user-auth  # ❌ Creates merge commit

# Required: Squash merge or rebase
git rebase main  # ✅ Maintains linear history
git merge --squash feature/user-auth  # ✅ Single commit per feature
```

**Commit Granularity:**
- Each commit should represent a single logical change
- Commits should be atomic and revertible independently
- Work-in-progress commits should be squashed before merge
- Each commit should pass tests and maintain working state

**History Cleanup:**
```bash
# Interactive rebase to clean up history before PR
git rebase -i main

# Squash related commits
pick a1b2c3d feat(auth): add user model
squash d4e5f6g feat(auth): add validation
squash g7h8i9j feat(auth): add tests

# Result: Single clean commit
# feat(auth): implement user authentication with validation and tests
```

## Git Workflow Tools

### Developer Tools

**Git Configuration:**
```bash
# Set up Git for conventional commits
git config --global user.name "Your Name"
git config --global user.email "your.email@nash.group"

# Set up helpful aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# Conventional commit template
git config --global commit.template ~/.gitmessage
```

**Commit Message Template:**
```bash
# ~/.gitmessage
# <type>[optional scope]: <description>
#
# [optional body]
#
# [optional footer(s)]
#
# Types: feat, fix, docs, chore, refactor, perf, test, build, ci, revert
# Examples:
#   feat(api): add user authentication
#   fix(db): resolve timeout issue
#   docs: update README
```

**IDE Integration:**
```json
// VS Code settings.json
{
  "git.inputValidation": "always",
  "git.inputValidationLength": 72,
  "git.inputValidationSubjectLength": 50,
  "conventionalCommits.scopes": [
    "api", "auth", "db", "ui", "docs", "test", "ci", "build"
  ]
}
```

### Repository Templates

**Repository Setup Automation:**
```bash
#!/bin/bash
# scripts/setup-repository-standards.sh
# Sets up Git workflow standards for new repository

set -euo pipefail

echo "Setting up Git workflow standards..."

# Install git hooks
./scripts/setup-git-hooks.sh

# Create PR template
mkdir -p .github/pull_request_template
cp templates/pull_request_template.md .github/pull_request_template/

# Create issue templates
mkdir -p .github/ISSUE_TEMPLATE
cp templates/issue_templates/* .github/ISSUE_TEMPLATE/

# Set up GitHub Actions workflows
mkdir -p .github/workflows
cp templates/workflows/git-workflow-validation.yml .github/workflows/

# Configure branch protection (requires admin access)
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["git-workflow-validation"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null

echo "Git workflow standards setup complete"
```

## Compliance Verification

**Automated Checks:**
- Pre-commit hooks validate commit message format
- CI/CD validates linear history and conventional commits
- Branch protection enforces review requirements
- Automated commit message analysis in pull requests

**Manual Audits:**
- Weekly review of commit message quality across repositories
- Monthly assessment of linear history compliance
- Quarterly evaluation of Git workflow effectiveness

**Reporting:**
- Real-time Git workflow compliance dashboard
- Weekly commit quality metrics
- Monthly branch management efficiency reports
- Quarterly developer workflow satisfaction surveys

## Integration with Development Process

### IDE and Tool Integration

**Recommended Tools:**
- **Commitizen**: Interactive commit message creation
- **Husky**: Git hooks management
- **Conventional Changelog**: Automated changelog generation
- **Semantic Release**: Automated version management

**Setup Example:**
```json
// package.json
{
  "devDependencies": {
    "@commitlint/cli": "^17.0.0",
    "@commitlint/config-conventional": "^17.0.0",
    "husky": "^8.0.0",
    "lint-staged": "^13.0.0"
  },
  "husky": {
    "hooks": {
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS",
      "pre-commit": "lint-staged"
    }
  },
  "commitlint": {
    "extends": ["@commitlint/config-conventional"]
  }
}
```

### Training and Onboarding

**New Developer Checklist:**
```markdown
## Git Workflow Onboarding

### Setup
- [ ] Configure Git with name and email
- [ ] Install recommended Git tools (commitizen, husky)
- [ ] Set up commit message template
- [ ] Configure IDE for conventional commits

### Knowledge Check
- [ ] Understand conventional commits format
- [ ] Know branch naming conventions
- [ ] Understand linear history importance
- [ ] Practice rebase workflow

### First Contribution
- [ ] Create properly named branch
- [ ] Make commits with conventional messages
- [ ] Create PR with proper title and description
- [ ] Successfully merge with squash commit
```

## Related Documents

- **Source Principles:** [PRINCIPLES.md - Principle 1: The Sacred Timeline is Linear and Clean](../the-covenant/PRINCIPLES.md#principle-1-the-sacred-timeline-is-linear-and-clean), [Principle 2: Every Commit Shall Speak Its Purpose](../the-covenant/PRINCIPLES.md#principle-2-every-commit-shall-speak-its-purpose)
- **Governance Authority:** [GOVERNANCE.md - Development Standards](../the-covenant/GOVERNANCE.md#stronghold-decisions-individual-repositories)
- **Implementation:** GitHub rulesets, Git hooks, CI/CD workflows
- **Development Process:** [SC-003 Trunk-Based Development](./sc-003-trunk-based-development.md)

## Change History

- **2024-09-30** - Initial creation based on Principles 1 & 2: Sacred Timeline and Commit Purpose
