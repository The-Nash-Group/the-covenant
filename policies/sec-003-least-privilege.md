# SEC-003: Least Privilege Access

**Policy ID:** SEC-003
**Category:** Security
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Every identity (human or machine) **must** get exactly the permissions they need, no more, no less. Permissions **must** expire and require renewal. Over-privileged accounts are ticking time bombs.

## Rationale

Over-privileged accounts are ticking time bombs. We've seen admin credentials used for daily work, service accounts with org-wide access, and forgotten bot tokens with write permissions:

- **Blast Radius**: Excessive permissions amplify the impact of compromise
- **Privilege Creep**: Permissions accumulate over time without review
- **Stale Access**: Former employees and obsolete services retain access
- **Lateral Movement**: Over-privileged accounts enable broader compromise
- **Compliance Risk**: Excessive permissions violate regulatory requirements
- **Insider Risk**: Too much access tempts abuse and creates opportunity

Minimal permissions reduce risk, improve auditability, and force intentional access design.

## Scope

**Applies To:**
- All human user accounts and service accounts
- All GitHub team memberships and repository permissions
- All cloud provider IAM roles and policies
- All database access and application permissions
- All API keys, tokens, and automated access credentials

**Exceptions:**
- Emergency break-glass accounts (with enhanced monitoring and time limits)
- Initial bootstrap accounts (must be reduced to minimal permissions within 24 hours)

## Implementation

### Technical Enforcement

GitHub team repository access with minimal permissions:

```hcl
# the-citadel/terraform/github/teams.tf
resource "github_team_repository" "least_privilege" {
  for_each = var.team_repository_access

  team_id    = github_team.teams[each.value.team].id
  repository = github_repository.repositories[each.value.repository].name

  # Minimal permission - push not admin, not maintain
  permission = each.value.permission  # "pull", "triage", "push", "maintain", "admin"
}

# Service teams get only push access to their services
resource "github_team_repository" "service_teams" {
  for_each = var.service_repositories

  team_id    = github_team.teams["${each.key}-team"].id
  repository = each.key
  permission = "push"  # Cannot modify repository settings or manage access
}

# Platform team gets maintain access to platform repos
resource "github_team_repository" "platform_access" {
  for_each = var.platform_repositories

  team_id    = github_team.teams["platform-team"].id
  repository = each.key
  permission = "maintain"  # Can manage issues, PRs, settings but not repository security
}
```

Cloudflare access with role-based permissions:

```hcl
# the-citadel/terraform/cloudflare/access_policies.tf
resource "cloudflare_access_policy" "developer_access" {
  application_id = cloudflare_access_application.internal_services.id
  name           = "Developer Access"
  precedence     = 1
  decision       = "allow"

  include {
    group = [cloudflare_access_group.developers.id]
  }

  # Developers can only access development and staging environments
  require {
    any_valid_service_token = false
    common_name            = "*.dev.nash.group"
  }
}

resource "cloudflare_access_policy" "production_access" {
  application_id = cloudflare_access_application.production_services.id
  name           = "Production Access"
  precedence     = 1
  decision       = "allow"

  include {
    group = [cloudflare_access_group.platform_team.id]
  }

  # Production access requires additional verification
  require {
    certificate = true
    mfa         = true
  }

  # Shorter session duration for production access
  session_duration = "2h"
}
```

### Automated Validation

**Permission Auditing:**
- Monthly automated review of all user and service permissions
- Identification of unused or excessive permissions
- Automated alerts for permission changes and escalations
- Regular attestation requirements for privileged access

**Access Expiration:**
- Automatic expiration of temporary access grants
- Regular re-certification of ongoing access needs
- Automated removal of access for inactive accounts
- Time-boxed access for contractor and vendor accounts

**Privilege Monitoring:**
- Real-time monitoring of privileged actions and access
- Anomaly detection for unusual permission usage
- Automated alerts for permission escalation attempts
- Regular reports on privilege distribution and usage

### Human Process

1. **Access Requests**: Formal justification required for all permission grants
2. **Approval Workflow**: Manager and security team approval for privileged access
3. **Regular Reviews**: Quarterly access certification and cleanup
4. **Termination Process**: Immediate access revocation upon role changes
5. **Escalation Procedures**: Temporary privilege escalation with approval and logging

## Permission Framework

### Role Definition Standards

**Standard Permission Levels:**
```hcl
variable "permission_levels" {
  description = "Standard permission levels across all systems"
  type = map(object({
    github_permission      = string
    cloudflare_access     = list(string)
    database_roles        = list(string)
    monitoring_access     = string
  }))

  default = {
    "developer" = {
      github_permission   = "push"
      cloudflare_access  = ["dev", "staging"]
      database_roles     = ["readonly"]
      monitoring_access  = "read"
    }
    "maintainer" = {
      github_permission   = "maintain"
      cloudflare_access  = ["dev", "staging", "production"]
      database_roles     = ["readonly", "app_user"]
      monitoring_access  = "write"
    }
    "administrator" = {
      github_permission   = "admin"
      cloudflare_access  = ["all"]
      database_roles     = ["admin"]
      monitoring_access  = "admin"
    }
  }
}
```

### Service Account Management

**Service Account Standards:**
- One service account per service or application
- Minimal permissions for specific service functions
- Regular rotation of service account credentials
- Monitoring and alerting for service account usage

**Implementation Example:**
```hcl
# Service-specific access tokens
resource "github_repository_deploy_key" "service_deploy" {
  for_each = var.services

  title      = "${each.key}-deploy-key"
  repository = each.key
  key        = each.value.deploy_public_key
  read_only  = false  # Only if write access needed for deployment
}

# Cloudflare service tokens with minimal scope
resource "cloudflare_access_service_token" "service_access" {
  for_each = var.services

  name     = "${each.key}-service"
  duration = "8760h"  # 1 year with automatic rotation

  # Restrict to specific application
  scopes = [cloudflare_access_application.services[each.key].id]
}
```

## Access Review and Certification

### Automated Access Review

**Monthly Automated Review:**
```yaml
# .github/workflows/access-review.yml
name: Monthly Access Review
on:
  schedule:
    - cron: '0 0 1 * *'  # First day of each month

jobs:
  generate-access-report:
    runs-on: ubuntu-latest
    steps:
      - name: Generate Team Access Report
        run: |
          # Generate report of all team memberships and permissions
          gh api orgs/the-nash-group/teams --paginate | \
            jq -r '.[] | .slug' | \
            xargs -I {} gh api orgs/the-nash-group/teams/{}/members > team-access.json

      - name: Identify Stale Access
        run: |
          # Find accounts with no activity in 90+ days
          # Find over-privileged accounts
          # Generate recommendations for access cleanup

      - name: Create Access Review Issue
        run: |
          gh issue create --title "Monthly Access Review - $(date +%Y-%m)" \
            --body-file access-review-report.md \
            --assignee @the-nash-group/watchers
```

### Human Certification Process

**Quarterly Manager Attestation:**
1. **Manager Review**: Direct managers certify team member access needs
2. **Security Review**: Security team reviews privileged access grants
3. **Cleanup Actions**: Remove unnecessary or excessive permissions
4. **Documentation**: Record access decisions and justifications

**Annual Comprehensive Review:**
1. **Role Analysis**: Review all roles and their permission requirements
2. **Permission Optimization**: Identify opportunities to reduce default permissions
3. **Process Improvement**: Update access request and review procedures
4. **Compliance Audit**: Verify adherence to least privilege principles

## Compliance Verification

**Automated Checks:**
- Permission drift detection and alerting
- Unused permission identification and cleanup recommendations
- Access pattern analysis for privilege abuse detection
- Automated compliance reporting for regulatory requirements

**Manual Audits:**
- Monthly spot checks of high-privilege accounts
- Quarterly comprehensive access review and certification
- Annual third-party security assessment of access controls

**Reporting:**
- Real-time dashboard of permission distribution and usage
- Weekly reports on access changes and privilege escalations
- Monthly trend analysis of permission grants and revocations

## Emergency Procedures

### Emergency Access Escalation

**Break-Glass Access:**
```hcl
# Emergency access for critical incidents
resource "github_team" "emergency_access" {
  name        = "emergency-responders"
  description = "Temporary emergency access team"
  privacy     = "secret"

  # Automatically expire membership after 24 hours
  lifecycle {
    prevent_destroy = false
  }
}
```

**Emergency Process:**
1. **Incident Declaration**: On-call engineer declares emergency requiring elevated access
2. **Temporary Grant**: Automated system grants emergency permissions for 4 hours
3. **Monitoring**: Enhanced logging and monitoring of emergency access usage
4. **Review**: Post-incident review of emergency access usage and justification
5. **Cleanup**: Automatic revocation of emergency permissions after time limit

### Compromised Account Response

**Immediate Actions:**
1. **Account Lockout**: Immediately disable all access for compromised account
2. **Permission Audit**: Review all permissions and recent activities
3. **Lateral Impact**: Assess potential compromise of connected systems
4. **Credential Rotation**: Force rotation of shared or service credentials

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 10: The Principle of Least Privilege](../the-covenant/PRINCIPLES.md#principle-10-the-principle-of-least-privilege)
- **Governance Authority:** [GOVERNANCE.md - Team Authority Matrix](../the-covenant/GOVERNANCE.md#the-hierarchy-of-the-realm)
- **Implementation:** `the-citadel/terraform/github/teams.tf`, `the-citadel/terraform/cloudflare/access_policies.tf`
- **Emergency Procedures:** [GOV-003 Break-Glass Procedures](./gov-003-break-glass.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 10: The Principle of Least Privilege
