# GOV-004: Team Authority Matrix

**Policy ID:** GOV-004
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Team authority **must** be clearly defined and enforced through technical controls. Immortals **shall** propose changes, Mentors **must** approve domain-specific changes, and Watchers **shall** control infrastructure and organization-wide concerns. Authority boundaries **must** be enforced through GitHub teams, CODEOWNERS files, and role-based access controls.

## Rationale

Clear authority delegation prevents conflicts and ensures appropriate expertise reviews changes:

- **Expertise Alignment**: Subject matter experts review changes in their domains
- **Scalable Decision Making**: Distributed authority prevents bottlenecks while maintaining quality
- **Clear Accountability**: Well-defined responsibilities make it clear who is accountable for decisions
- **Conflict Prevention**: Explicit boundaries reduce territorial disputes and unclear responsibilities
- **Quality Assurance**: Domain experts provide better review quality than generalists
- **Efficient Workflows**: Contributors know exactly who to engage for different types of changes
- **Growth Support**: Clear progression path from Immortal → Mentor → Watcher
- **Knowledge Distribution**: Authority structure encourages knowledge sharing across teams

The hierarchy ensures decisions are made by those with appropriate expertise and authority while providing clear escalation paths.

## Scope

**Team Structure:**
- **Immortals**: All Nash Group organization members (contributors)
- **Mentors**: Senior engineers with domain expertise (maintainers/CODEOWNERS)
- **Watchers**: Infrastructure guardians with organization-wide authority (administrators)

**Authority Domains:**
- **Stronghold Decisions**: Individual repository changes
- **Citadel Decisions**: Infrastructure and organization settings
- **Covenant Decisions**: Governance and principle changes

**Technical Enforcement:**
- GitHub team permissions and repository access
- CODEOWNERS file protection and review requirements
- Branch protection rules and required approvals
- Organization settings and billing access

## Implementation

### Technical Enforcement

GitHub team structure and permissions:

```hcl
# terraform/github/teams.tf
resource "github_team" "immortals" {
  name        = "immortals"
  description = "All Nash Group contributors"
  privacy     = "closed"
}

resource "github_team" "mentors" {
  name        = "mentors"
  description = "Domain experts and code owners"
  privacy     = "closed"
  parent_team_id = github_team.immortals.id
}

resource "github_team" "watchers" {
  name        = "watchers"
  description = "Infrastructure guardians and administrators"
  privacy     = "closed"
  parent_team_id = github_team.mentors.id
}

# Platform specialization team
resource "github_team" "platform_clan" {
  name        = "platform-clan"
  description = "Platform services specialists"
  privacy     = "closed"
  parent_team_id = github_team.mentors.id
}

# Team repository permissions
resource "github_team_repository" "mentors_repositories" {
  for_each = var.application_repositories

  team_id    = github_team.mentors.id
  repository = each.value
  permission = "maintain"  # Can manage repo settings, not admin
}

resource "github_team_repository" "watchers_infrastructure" {
  for_each = var.infrastructure_repositories

  team_id    = github_team.watchers.id
  repository = each.value
  permission = "admin"  # Full control of infrastructure repos
}

resource "github_team_repository" "platform_clan_services" {
  for_each = var.platform_service_repositories

  team_id    = github_team.platform_clan.id
  repository = each.value
  permission = "maintain"
}
```

CODEOWNERS enforcement for domain authority:

```hcl
# terraform/github/codeowners.tf
resource "github_repository_file" "application_codeowners" {
  for_each = var.application_repositories

  repository = each.value
  file       = "CODEOWNERS"
  content = templatefile("${path.module}/templates/codeowners/application.txt", {
    mentors_team = "@the-nash-group/mentors"
    domain_leads = lookup(var.domain_leads, each.key, [])
  })

  # Example content:
  # * @the-nash-group/mentors
  # /src/auth/ @the-nash-group/security-mentors
  # /infrastructure/ @the-nash-group/platform-clan
}

resource "github_repository_file" "infrastructure_codeowners" {
  repository = "the-citadel"
  file       = "CODEOWNERS"
  content = templatefile("${path.module}/templates/codeowners/infrastructure.txt", {
    watchers_team = "@the-nash-group/watchers"
    mentors_team  = "@the-nash-group/mentors"
  })

  # Example content:
  # * @the-nash-group/watchers
  # /terraform/github/ @the-nash-group/watchers
  # /terraform/cloudflare/ @the-nash-group/platform-clan @the-nash-group/watchers
}

resource "github_repository_file" "covenant_codeowners" {
  repository = "the-covenant"
  file       = "CODEOWNERS"
  content = templatefile("${path.module}/templates/codeowners/covenant.txt", {
    watchers_team = "@the-nash-group/watchers"
    mentors_team  = "@the-nash-group/mentors"
  })

  # Example content:
  # * @the-nash-group/mentors @the-nash-group/watchers
  # /GOVERNANCE.md @the-nash-group/watchers
  # /PRINCIPLES.md @the-nash-group/mentors
}
```

Authority-based branch protection:

```hcl
# terraform/github/authority_protection.tf
resource "github_repository_ruleset" "stronghold_authority" {
  for_each = var.application_repositories

  name        = "Stronghold Authority - ${each.key}"
  repository  = each.value
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["refs/heads/main"]
      exclude = []
    }
  }

  rules {
    # Mentors can approve domain changes
    pull_request {
      required_approving_review_count   = 1  # 1 Mentor minimum
      dismiss_stale_reviews            = true
      require_code_owner_review        = true
      required_review_thread_resolution = true
    }

    # Critical services need 2 approvals
    dynamic "pull_request" {
      for_each = contains(var.critical_services, each.key) ? [1] : []
      content {
        required_approving_review_count = 2
      }
    }
  }
}

resource "github_repository_ruleset" "citadel_authority" {
  name        = "Citadel Authority"
  repository  = "the-citadel"
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["refs/heads/main"]
      exclude = []
    }
  }

  rules {
    # Infrastructure changes require Mentor + Watcher
    pull_request {
      required_approving_review_count   = 2
      dismiss_stale_reviews            = true
      require_code_owner_review        = true
      required_review_thread_resolution = true
    }

    # Security changes require Watcher approval
    required_status_checks {
      required_status_checks = [
        "security-review-required",
        "terraform-plan-approved"
      ]
      strict_required_status_checks_policy = true
    }
  }
}
```

### Automated Validation

Authority verification and escalation tracking:

```python
# scripts/authority-validator.py
import github
from typing import Dict, List, Optional
from enum import Enum

class AuthorityLevel(Enum):
    IMMORTAL = "immortal"
    MENTOR = "mentor"
    WATCHER = "watcher"

class DecisionScope(Enum):
    STRONGHOLD = "stronghold"  # Repository-level
    CITADEL = "citadel"        # Infrastructure
    COVENANT = "covenant"      # Governance

class AuthorityMatrix:
    def __init__(self, org: str):
        self.gh = github.Github()
        self.org = self.gh.get_organization(org)

    def get_user_authority(self, username: str) -> AuthorityLevel:
        """Determine user's authority level based on team membership"""
        user = self.gh.get_user(username)

        # Check team memberships (highest level wins)
        if self.is_team_member(user, "watchers"):
            return AuthorityLevel.WATCHER
        elif self.is_team_member(user, "mentors"):
            return AuthorityLevel.MENTOR
        elif self.is_team_member(user, "immortals"):
            return AuthorityLevel.IMMORTAL
        else:
            raise ValueError(f"User {username} not found in organization teams")

    def validate_decision_authority(self, pr_number: int,
                                  repository: str) -> Dict[str, bool]:
        """Validate PR has appropriate authority for decision scope"""
        repo = self.org.get_repo(repository)
        pr = repo.get_pull(pr_number)

        scope = self.determine_decision_scope(repository, pr)
        required_authority = self.get_required_authority(scope)

        approvals = [review for review in pr.get_reviews()
                    if review.state == "APPROVED"]

        validation = {
            "scope": scope.value,
            "required_authority": required_authority,
            "has_authority": False,
            "approvers": [],
            "missing_requirements": []
        }

        # Check approval requirements based on scope
        if scope == DecisionScope.STRONGHOLD:
            validation.update(self.validate_stronghold_authority(approvals))
        elif scope == DecisionScope.CITADEL:
            validation.update(self.validate_citadel_authority(approvals))
        elif scope == DecisionScope.COVENANT:
            validation.update(self.validate_covenant_authority(approvals))

        return validation

    def validate_stronghold_authority(self, approvals: List) -> Dict:
        """Validate repository-level change authority"""
        mentor_approvals = [a for a in approvals
                           if self.get_user_authority(a.user.login) in
                           [AuthorityLevel.MENTOR, AuthorityLevel.WATCHER]]

        return {
            "has_authority": len(mentor_approvals) >= 1,
            "mentor_count": len(mentor_approvals),
            "missing_requirements": [] if len(mentor_approvals) >= 1
                                  else ["Requires 1 Mentor approval"]
        }

    def validate_citadel_authority(self, approvals: List) -> Dict:
        """Validate infrastructure change authority"""
        watcher_approvals = [a for a in approvals
                            if self.get_user_authority(a.user.login) == AuthorityLevel.WATCHER]
        mentor_approvals = [a for a in approvals
                           if self.get_user_authority(a.user.login) in
                           [AuthorityLevel.MENTOR, AuthorityLevel.WATCHER]]

        missing = []
        if len(mentor_approvals) < 1:
            missing.append("Requires 1 Mentor approval")
        if len(watcher_approvals) < 1:
            missing.append("Requires 1 Watcher approval")

        return {
            "has_authority": len(missing) == 0,
            "mentor_count": len(mentor_approvals),
            "watcher_count": len(watcher_approvals),
            "missing_requirements": missing
        }

    def validate_covenant_authority(self, approvals: List) -> Dict:
        """Validate governance change authority (Council)"""
        watcher_approvals = [a for a in approvals
                            if self.get_user_authority(a.user.login) == AuthorityLevel.WATCHER]
        mentor_approvals = [a for a in approvals
                           if self.get_user_authority(a.user.login) == AuthorityLevel.MENTOR]

        missing = []
        if len(watcher_approvals) < 2:
            missing.append(f"Requires 2 Watcher approvals (have {len(watcher_approvals)})")
        if len(mentor_approvals) < 2:
            missing.append(f"Requires 2 Mentor approvals (have {len(mentor_approvals)})")

        return {
            "has_authority": len(missing) == 0,
            "mentor_count": len(mentor_approvals),
            "watcher_count": len(watcher_approvals),
            "missing_requirements": missing
        }
```

### Human Process

Authority delegation and team management:

1. **Immortal Onboarding**:
   - Add to @the-nash-group/immortals team
   - Grant repository access based on role
   - Provide authority matrix training
   - Assign mentor for guidance

2. **Mentor Promotion**:
   - Nominated by peers, approved by Watchers
   - Domain expertise demonstrated
   - Add to @the-nash-group/mentors team
   - Update CODEOWNERS for their domains

3. **Watcher Appointment**:
   - Appointed based on demonstrated responsibility
   - Infrastructure and security expertise
   - Add to @the-nash-group/watchers team
   - Grant organization admin privileges

4. **Authority Escalation**:
   - Cross-domain conflicts escalate to Council
   - Technical disagreements resolved by relevant Mentors
   - Governance conflicts arbitrated by Watchers

## Compliance Verification

### Automated Checks

- **Team Membership Validation**: GitHub team membership drives authority
- **CODEOWNERS Enforcement**: Required reviews by domain experts
- **Branch Protection**: Authority requirements enforced before merge
- **Permission Auditing**: Regular checks of repository access levels
- **Authority Tracking**: Logs of who approved what decisions

### Manual Audits

- **Quarterly Team Review**: Validate team membership and permissions
- **Annual Authority Assessment**: Review authority matrix effectiveness
- **CODEOWNERS Audit**: Ensure domain assignments remain current

### Reporting

Authority metrics:
- Decision approval times by authority level
- Authority escalation frequency and resolution
- Team membership growth and role transitions
- Cross-domain collaboration patterns
- Authority delegation effectiveness

## Related Documents

- **Source**: [../the-covenant/GOVERNANCE.md - The Hierarchy of the Realm](../the-covenant/GOVERNANCE.md#the-hierarchy-of-the-realm)
- **Source**: [../the-covenant/GOVERNANCE.md - The Arenas of Decision](../the-covenant/GOVERNANCE.md#the-arenas-of-decision)
- **Related Policies**:
  - [GOV-005: Conflict Resolution Process](./gov-005-conflict-resolution.md)
  - [GOV-006: Council Decision Quorum](./gov-006-decision-quorum.md)
- **Implementation**: [the-citadel terraform/github/teams.tf](../the-citadel/terraform/github/teams.tf)

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-09-30 | 1.0 | Initial policy creation from GOVERNANCE.md Hierarchy and Decision Arenas | Claude Code |
