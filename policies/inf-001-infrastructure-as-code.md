# INF-001: Infrastructure as Code Only

**Policy ID:** INF-001
**Category:** Infrastructure
**Effective Date:** 2024-09-30
**Last Updated:** 2026-04-07

## Statement

All infrastructure and platform configuration **must** be defined as code. Manual changes in UIs are forbidden sorcery that undermines reproducibility and auditability.

## Rationale

We've lost entire configurations to accidental clicks. We've spent days trying to recreate a manually-configured system. "Documentation" of manual steps is fiction—only code is truth. Manual changes create:

- **Configuration Drift**: Systems diverge from known state
- **Undocumented Changes**: Critical settings lost in the UI wilderness
- **Unreproducible Environments**: "Works in staging" becomes meaningless
- **Audit Trail Gaps**: No record of who changed what when
- **Knowledge Silos**: Infrastructure becomes tribal knowledge
- **Recovery Complications**: Disaster recovery becomes guesswork

Infrastructure as Code ensures every change is tracked, reviewed, and reproducible.

## Scope

**Applies To:**
- All Cloudflare DNS records, zones, and WAF rules
- All GitHub organization settings, repository configurations, and team structures
- All monitoring and alerting configurations
- All service discovery and load balancer configurations
- All security policies and access controls

**Exceptions:**
- Emergency break-glass procedures (with immediate reconciliation required)
- Initial bootstrap configurations for new accounts (must be codified within 24 hours)

## Implementation

### Technical Enforcement

In `the-citadel/terraform/orgs/<workspace>/main.tf`:

```hcl
# Shared module defaults codify Cloudflare baseline
module "zone_standard" {
  source  = "../../modules/cloudflare-zone-standard"
  zone_id = var.cloudflare_zone_id
  domain  = "example.com"
}
```

In `the-citadel/terraform/orgs/the-nash-group/main.tf`:

```hcl
# Team structures and organization defaults are codified in the parent root
module "teams" {
  source = "../../modules/github-team-structure"

  org_owners      = local.parent_roster.org_owners
  team_mentors    = local.parent_roster.team_mentors
  team_watchers   = local.parent_roster.team_watchers
  team_platform   = local.parent_roster.team_platform
  primary_watcher = local.parent_roster.primary_watcher
}
```

### Automated Validation

**Drift Detection:**
- Nightly `tofu plan` runs detect configuration drift
- Automated alerts when manual changes detected
- Weekly drift reports with remediation recommendations

**State Management:**
- OpenTofu state stored in Hetzner Object Storage (S3-compatible)
- State locking prevents concurrent modifications
- State backups independent of primary storage

### Human Process

1. **Change Proposal**: All infrastructure changes start with OpenTofu/IaC code
2. **Review Process**: Infrastructure changes require Mentor + Watcher approval
3. **Plan Validation**: `tofu plan` output reviewed before apply
4. **Apply Execution**: Changes applied via GitHub Actions / approved local operator runbooks with the documented approval gate
5. **Drift Monitoring**: Continuous monitoring for unauthorized changes

## Compliance Verification

**Automated Checks:**
- Nightly drift detection via `tofu plan`
- Resource tagging compliance verification
- Configuration backup and versioning
- Change audit trails in GitHub Actions, git history, and remote state versioning

**Manual Audits:**
- Monthly infrastructure configuration review
- Quarterly compliance assessment against baseline
- Annual disaster recovery testing of IaC procedures

**Reporting:**
- Real-time dashboard showing infrastructure state health
- Weekly drift reports with remediation status
- Monthly change velocity and impact analysis

## Emergency Procedures

### Break-Glass Protocol
For critical incidents requiring immediate manual changes:

1. **Emergency Authorization**: Watcher role documents emergency action
2. **Immediate Change**: Make minimal manual change to restore service
3. **Documentation**: Record all manual changes within 1 hour
4. **Reconciliation**: Create PR to codify changes within 24 hours
5. **Post-Mortem**: Review emergency response and improve procedures

### Drift Remediation

**Automated Drift Response:**
1. **Detection**: Nightly plan detects unauthorized changes
2. **Alert**: Immediate notification to infrastructure team
3. **Assessment**: Determine if change is legitimate or unauthorized
4. **Action**: Either codify change or revert to known state

**Manual Drift Investigation:**
1. **Triage**: Assess scope and impact of configuration drift
2. **Root Cause**: Identify how manual change occurred
3. **Remediation**: Choose between codifying or reverting change
4. **Prevention**: Update processes to prevent similar drift

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 5: The Fortress is Defined by Blueprints](../the-covenant/PRINCIPLES.md#principle-5-the-fortress-is-defined-by-blueprints-not-by-hand)
- **Governance Authority:** [GOVERNANCE.md - Citadel Decisions](../the-covenant/GOVERNANCE.md#citadel-decisions-infrastructure)
- **Implementation:** `the-citadel/terraform/` (all files)
- **Emergency Procedures:** [GOV-003 Break-Glass Procedures](./gov-003-break-glass.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 5: The Fortress is Defined by Blueprints, Not by Hand
