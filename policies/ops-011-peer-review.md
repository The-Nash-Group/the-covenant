# OPS-011: Peer Review Requirements

**Policy ID:** OPS-011
**Category:** Operations
**Effective Date:** 2024-08-01
**Last Updated:** 2024-09-30

## Statement

Every change to protected branches **must** require peer review. No exceptions, no "quick fixes," no "just this once." The wisdom of the clan is always greater than any individual warrior, regardless of seniority or expertise.

## Rationale

Unreviewed code is a Trojan horse. We've seen single-line changes take down production, and "obvious" fixes introduce subtle bugs. The four eyes principle has saved us from:

- **Logic Errors**: Fresh eyes catch what familiarity misses
- **Security Vulnerabilities**: Reviewers spot injection points and access issues
- **Performance Regressions**: Second opinions identify efficiency problems
- **Architectural Violations**: Peers enforce consistency and standards
- **Knowledge Silos**: Code review spreads understanding across the team

Even the most senior engineer benefits from the perspective of a junior developer who asks "why does this work this way?"

## Scope

**Applies To:**
- All pull requests targeting `main` or protected branches
- All repositories under The Nash Group organization
- Changes to infrastructure code in `the-citadel`
- Emergency hotfixes (with expedited but still required review)

**Exceptions:**
- Automated dependency updates from Renovate (pre-configured rules)
- Documentation-only changes to non-critical repositories (single approver)

## Implementation

### Technical Enforcement

In `the-citadel/terraform/github/rulesets.tf`:

```hcl
resource "github_repository_ruleset" "peer_review" {
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
  }

  rules {
    pull_request {
      required_approving_review_count   = 1
      dismiss_stale_reviews_on_push    = true
      require_code_owner_review        = true
      require_last_push_approval      = false
      required_review_thread_resolution = true
    }
  }
}

# Enhanced requirements for critical infrastructure
resource "github_repository_ruleset" "citadel_enhanced_review" {
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
    repository_name {
      include = ["the-citadel"]
    }
  }

  rules {
    pull_request {
      required_approving_review_count = 2  # Higher bar for infrastructure
      require_code_owner_review      = true
      dismiss_stale_reviews_on_push  = true
    }
  }
}
```

### Automated Validation

- **Branch Protection**: GitHub prevents merging without required approvals
- **CODEOWNERS Integration**: Automatically requests reviews from domain experts
- **Stale Review Dismissal**: New pushes invalidate previous approvals

### Human Process

1. **PR Creation**: Author provides clear description and context
2. **Reviewer Assignment**: Automatic via CODEOWNERS or manual selection
3. **Review Standards**: Reviewers must verify both correctness and compliance
4. **Approval Process**: Explicit approval required, not just lack of objection
5. **Merge Authorization**: Final merge only after all requirements met

## Review Standards

### What Reviewers Must Check

**Correctness:**
- Logic is sound and handles edge cases
- Code does what the PR description claims
- No obvious bugs or race conditions

**Security:**
- No secrets or credentials in code
- Proper input validation and sanitization
- Access controls and permissions correct

**Standards Compliance:**
- Follows coding conventions and style
- Adheres to architectural patterns
- Includes appropriate tests and documentation

**Quality:**
- Code is readable and maintainable
- Performance considerations addressed
- Error handling is comprehensive

### Review Response Time

- **Standard PRs**: 24 hours during business days
- **Critical Fixes**: 4 hours maximum
- **Infrastructure Changes**: 48 hours (requires deeper analysis)

## Review Roles and Responsibilities

### Code Author
- **Provide Context**: Clear PR description with "why" not just "what"
- **Respond Promptly**: Address reviewer feedback within 24 hours
- **Test Thoroughly**: Include test results and manual validation
- **Be Receptive**: Accept feedback gracefully and improve

### Code Reviewer (Judge Role)
- **Review Thoroughly**: Don't rubber-stamp based on author reputation
- **Ask Questions**: If unclear, ask for clarification
- **Suggest Improvements**: Offer specific, actionable feedback
- **Block if Necessary**: Use blocking reviews for serious issues
- **Follow Up**: Verify fixes address the original concerns

### Code Owner (Mentor Role)
- **Domain Expertise**: Provide specialized knowledge for their area
- **Architectural Guidance**: Ensure changes align with system design
- **Mentoring**: Help authors understand better approaches
- **Final Arbiter**: Make decisions on conflicting reviewer opinions

## Compliance Verification

**Automated Checks:**
- GitHub branch protection prevents unreviewed merges
- Audit logs track all review bypass attempts
- Weekly reports on review compliance rates

**Manual Audits:**
- Monthly assessment of review quality and thoroughness
- Quarterly analysis of bugs that escaped review process

**Reporting:**
- Review metrics dashboard showing approval times and patterns
- Post-incident analysis when unreviewed changes cause issues

## Emergency Procedures

### Break-Glass Process
For critical production outages where review delay risks further damage:

1. **Emergency Authorization**: Watcher role can temporarily disable protection
2. **Immediate Fix**: Deploy minimal change to restore service
3. **Post-Incident Review**: Emergency change reviewed within 4 hours
4. **Documentation**: Full incident report including review bypass justification
5. **Process Improvement**: Update procedures to prevent similar bypasses

### Expedited Review
For urgent but non-emergency changes:

1. **Priority Labeling**: Mark PR as `urgent` with justification
2. **Reviewer Notification**: Direct message to available reviewers
3. **Reduced SLA**: 4-hour maximum response time
4. **Same Standards**: Quality requirements unchanged despite urgency

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 3: No Code Enters the Timeline Unchallenged](../PRINCIPLES.md#principle-3-no-code-enters-the-timeline-unchallenged)
- **Governance Authority:** [GOVERNANCE.md - Mentors & Watchers Review Authority](../GOVERNANCE.md#the-mentors-maintainerscodeowners)
- **Implementation:** `the-citadel/terraform/github/rulesets.tf`
- **Emergency Procedures:** [GOV-003 Break-Glass Procedures](./gov-003-break-glass.md)

## Change History

- **2024-08-01** - Initial creation based on Principle 3
- **2024-09-30** - Added emergency procedures and enhanced review standards for infrastructure
