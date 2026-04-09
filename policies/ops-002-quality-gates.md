# OPS-002: Automated Quality Gates

**Policy ID:** OPS-002
**Category:** Operations
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

All code **must** pass automated quality gates (CI, linting, tests, security scanning) before merge. The machines are impartial judges that enforce standards without favoritism or exception.

## Rationale

"It works on my machine" is not a deployment strategy. Consistent, automated validation catches issues that human eyes miss and enforces standards without favoritism. We've learned that:

- **Inconsistent Environments**: Manual testing creates false confidence
- **Human Bias**: Developers skip steps under pressure or overconfidence
- **Standard Drift**: Without automation, coding standards slowly degrade
- **Regression Introduction**: Manual validation misses edge cases that automated tests catch
- **Security Gaps**: Humans forget security checks; automation never does

Automated checks provide objective, repeatable validation that scales across all contributors and repositories.

## Scope

**Applies To:**
- All pull requests targeting protected branches
- All repositories under The Nash Group organization
- Infrastructure code changes in `the-citadel`
- Third-party dependency updates and security patches

**Exceptions:**
- Documentation-only changes (reduced gate requirements)
- Emergency hotfixes (may bypass non-critical gates with post-merge remediation)

## Implementation

### Technical Enforcement

In `the-citadel/terraform/github/rulesets.tf`:

```hcl
resource "github_repository_ruleset" "automated_gates" {
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
        { context = "ci/build" },
        { context = "ci/test" },
        { context = "ci/lint" },
        { context = "security/dependency-scan" },
        { context = "security/secret-scan" },
        { context = "security/vulnerability-scan" }
      ]
    }
  }
}

# Enhanced gates for infrastructure repositories
resource "github_repository_ruleset" "infrastructure_enhanced_gates" {
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
    repository_name {
      include = ["the-citadel", "*-infrastructure"]
    }
  }

  rules {
    required_status_checks {
      strict_required_status_checks_policy = true
      required_status_checks = [
        { context = "terraform/validate" },
        { context = "terraform/plan" },
        { context = "terraform/security-scan" },
        { context = "terraform/cost-estimation" },
        { context = "ci/lint" }
      ]
    }
  }
}
```

### Automated Validation

**Standard Quality Gates:**
- **Build Verification**: Code compiles without errors
- **Test Execution**: Unit tests pass with minimum coverage thresholds
- **Code Linting**: Style and convention compliance via automated tools
- **Security Scanning**: Dependency vulnerabilities and secret detection
- **Type Checking**: Static analysis for type safety (where applicable)

**Infrastructure-Specific Gates:**
- **Terraform Validation**: `terraform validate` and `terraform fmt` checks
- **Plan Generation**: Successful `terraform plan` without errors
- **Security Policy**: Infrastructure security scanning via tools like tfsec
- **Cost Analysis**: Automated cost estimation for resource changes

### Human Process

1. **Pre-Submission**: Developer runs gates locally before pushing
2. **Automated Execution**: CI system executes all required gates on push
3. **Gate Monitoring**: Real-time status visible in PR interface
4. **Failure Response**: Clear error messages guide remediation
5. **Approval Workflow**: Human review only after gates pass

## Compliance Verification

**Automated Checks:**
- GitHub branch protection enforces gate completion
- Gate bypass attempts logged and alerted
- Weekly reports on gate success rates by repository
- Automated remediation for common gate failures

**Manual Audits:**
- Monthly review of gate effectiveness and coverage
- Quarterly assessment of gate execution performance
- Post-incident analysis when issues escape gate validation

**Reporting:**
- Real-time dashboard showing gate health across repositories
- Trend analysis of gate failures and remediation times
- Cost/benefit analysis of gate investments

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 4: The Machines Must Bless the Code](../the-covenant/PRINCIPLES.md#principle-4-the-machines-must-bless-the-code)
- **Governance Authority:** [GOVERNANCE.md - Review Standards](../the-covenant/GOVERNANCE.md#citadel-decisions-infrastructure)
- **Implementation:** `the-citadel/terraform/github/rulesets.tf`
- **Emergency Procedures:** [GOV-003 Break-Glass Procedures](./gov-003-break-glass.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 4: The Machines Must Bless the Code
