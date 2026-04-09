# GOV-010: Organizational Labeling Standard

**Policy ID:** GOV-010
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

All resources managed under Policy-as-Code (PaC) and Infrastructure-as-Code (IaC) **must** include a standard set of organizational labels. These labels **shall** ensure traceability from Covenant principles through Human Mandate roles to Citadel enforcement. No resource **may** be deployed or managed without the required core label set.

## Rationale

Consistent labeling encodes organizational culture into infrastructure. Labels transform abstract governance into actionable metadata that machines can enforce and humans can understand. This creates:

- **Traceability**: Direct lineage from Covenant → Policy → Citadel implementation
- **Accountability**: Clear ownership by clans and Guardian roles
- **Automation**: Reliable metadata for enforcement via OPA, Terraform, CI/CD
- **Knowledge Management**: Documentation embedded into resources themselves
- **Audit Capability**: Machine-readable compliance and governance tracking

Without systematic labeling, our infrastructure becomes anonymous and ungovernable—a collection of resources without culture or accountability.

## Scope

**Applies To:**
- All GitHub repositories under The Nash Group organization
- All Cloudflare DNS records, WAF rules, and access policies
- All Terraform resources in `the-citadel`
- All monitoring alerts, dashboards, and SLOs
- All CI/CD pipelines and automation workflows

**Exceptions:**
- Temporary development resources (lifespan < 7 days)
- Third-party managed services where labeling is not supported

## Label Hierarchy

### Core Labels (Required for All Resources)

These form the minimal metadata set that guarantees universal traceability:

| Label | Purpose | Example Values | Enforcement |
|-------|---------|----------------|-------------|
| `project_id` | Unique project identifier | `system-dashboard`, `the-citadel` | Required |
| `owner` | Primary responsible team/Guardian | `@the-nash-group/mentors`, `platform-clan` | Required |
| `clan` | Organizational group | `mentors`, `watchers`, `platform-clan`, `immortals` | Required |
| `tier` | Resource criticality level | `core`, `platform`, `application`, `experimental` | Required |
| `environment` | Deployment environment | `dev`, `staging`, `prod`, `shared` | Required |
| `policy_id` | Governing formal policy | `SC-003`, `SEC-001`, `INF-001` | Required |
| `citadel_ref` | Terraform resource path | `github.tf:ruleset.peer_review` | Required |

### Contextual Labels (Applied When Relevant)

#### Governance Set
| Label | Purpose | Example Values |
|-------|---------|----------------|
| `covenant_ref` | Source principle link | `principles.md#principle-3` |
| `approval_required` | Required approver level | `mentor`, `watcher`, `council` |
| `review_cycle` | Governance review frequency | `quarterly`, `annual`, `continuous` |

#### Observability Set
| Label | Purpose | Example Values |
|-------|---------|----------------|
| `slo_id` | Service Level Objective ID | `svc-dashboard-latency-p99` |
| `monitoring` | Associated runbook/alert | `high-error-rate`, `cert-expiry` |
| `drift_policy` | Drift handling strategy | `alert-only`, `auto-reconcile`, `manual-review` |

#### Lifecycle Set
| Label | Purpose | Example Values |
|-------|---------|----------------|
| `status` | Current resource state | `active`, `deprecated`, `experimental`, `sunset` |
| `deprecation_date` | Planned retirement | `2025-03-15` (ISO8601) |
| `migration_path` | Replacement guidance | `/docs/migrations/v2-upgrade.md` |

#### Knowledge Set
| Label | Purpose | Example Values |
|-------|---------|----------------|
| `adr_ref` | Architecture Decision Record | `ADR-001`, `decisions/auth-strategy.md` |
| `doc_ref` | Primary documentation | `/docs/observability.md`, `README.md` |

### Guardian Role Attribution

The label `guardian_role` **may** be applied when a resource embodies a Human Mandate role:

| Guardian Role | Applied When | Example Resource |
|---------------|--------------|------------------|
| `judge` | Resource enforces compliance | GitHub ruleset requiring peer review |
| `architect` | Resource translates principles | Terraform module implementing zero-trust |
| `gardener` | Resource maintains health | Automated dependency update workflow |
| `philosopher` | Resource embodies principles | Repository containing governance docs |
| `explorer` | Resource enables innovation | Development sandbox environment |

**Important**: This is metaphorical attribution—the resource acts in that role. Actual ownership is encoded in the `owner` label.

## Implementation

### Technical Enforcement

In `the-citadel/terraform/labels.tf`:

```hcl
# Standard label validation
locals {
  required_core_labels = [
    "project_id",
    "owner",
    "clan",
    "tier",
    "environment",
    "policy_id",
    "citadel_ref"
  ]

  valid_clans = ["mentors", "watchers", "platform-clan", "immortals"]
  valid_tiers = ["core", "platform", "application", "experimental"]
  valid_environments = ["dev", "staging", "prod", "shared"]
}

# GitHub repository labeling
resource "github_repository" "labeled_repo" {
  for_each = var.repositories

  name = each.key

  # Core labels enforced via topics (GitHub's label mechanism)
  topics = [
    "project-${each.value.project_id}",
    "owner-${replace(each.value.owner, "/", "-")}",
    "clan-${each.value.clan}",
    "tier-${each.value.tier}",
    "env-${each.value.environment}",
    "policy-${each.value.policy_id}",
    "citadel-${replace(each.value.citadel_ref, "/", "-")}"
  ]

  lifecycle {
    precondition {
      condition = contains(local.valid_clans, each.value.clan)
      error_message = "Invalid clan: must be one of ${join(", ", local.valid_clans)}"
    }
  }
}
```

### Automated Validation

- **Terraform Plan Phase**: Label schema validation via preconditions
- **CI/CD Pipeline**: OPA/Rego policies reject unlabeled resources
- **GitHub Actions**: Automated label compliance checking
- **Weekly Audits**: Scan for missing or invalid labels

### Human Process

1. **Resource Creation**: Author must include all core labels
2. **Review Process**: Judges verify label accuracy and completeness
3. **Audit Process**: Gardeners maintain label consistency over time

## Resource Class Examples

### GitHub Repository
```yaml
# Core Labels (Required)
project_id: "system-dashboard"
owner: "@the-nash-group/platform-clan"
clan: "platform-clan"
tier: "application"
environment: "prod"
policy_id: "SC-001,SC-002,OPS-011"
citadel_ref: "github.tf:repository.system_dashboard"

# Contextual Labels
covenant_ref: "principles.md#principle-13"
status: "active"
doc_ref: "README.md"
guardian_role: "explorer"
```

### Cloudflare DNS Record
```yaml
# Core Labels (Required)
project_id: "thenash-group-dns"
owner: "@the-nash-group/watchers"
clan: "watchers"
tier: "core"
environment: "prod"
policy_id: "INF-001,SEC-002"
citadel_ref: "cloudflare.tf:dns_record.main_site"

# Contextual Labels
slo_id: "dns-resolution-latency"
monitoring: "dns-health-check"
drift_policy: "auto-reconcile"
```

### GitHub Ruleset
```yaml
# Core Labels (Required)
project_id: "github-governance"
owner: "@the-nash-group/mentors"
clan: "mentors"
tier: "core"
environment: "shared"
policy_id: "SC-001,SC-002,OPS-011"
citadel_ref: "github.tf:ruleset.peer_review"

# Contextual Labels
covenant_ref: "principles.md#principle-3"
approval_required: "mentor"
guardian_role: "judge"
```

### Terraform Module
```yaml
# Core Labels (Required)
project_id: "infrastructure-modules"
owner: "@the-nash-group/mentors"
clan: "mentors"
tier: "platform"
environment: "shared"
policy_id: "INF-001"
citadel_ref: "modules/github-repo/main.tf"

# Contextual Labels
adr_ref: "ADR-003-module-standards"
doc_ref: "modules/github-repo/README.md"
guardian_role: "architect"
status: "active"
```

## Compliance Verification

**Automated Checks:**
- Terraform validation fails on missing core labels
- CI pipelines scan for label compliance weekly
- OPA policies prevent deployment of unlabeled resources
- GitHub Actions validate repository topic compliance

**Manual Audits:**
- Monthly label consistency review by Gardener role
- Quarterly assessment of contextual label usage
- Annual review of label schema effectiveness

**Reporting:**
- Dashboard showing label compliance rates by resource type
- Alerts for resources missing core labels
- Metrics on label usage patterns and evolution

## Violation Response

**Prevention:**
- Terraform preconditions block creation of unlabeled resources
- CI/CD pipeline fails on label validation errors
- Clear error messages guide correct labeling

**Detection:**
- Automated scanning identifies existing unlabeled resources
- Drift detection catches label modifications
- Audit reports highlight systematic labeling gaps

**Remediation:**
- Grace period for existing resources to be labeled (90 days)
- Automated label suggestion based on resource patterns
- Escalation process for persistent violations

## Benefits

- **Governance Automation**: Labels enable policy enforcement at scale
- **Cost Attribution**: Clear ownership and project attribution
- **Security Compliance**: Automated validation of security policies
- **Operational Excellence**: Consistent metadata for monitoring and alerting
- **Knowledge Preservation**: Embedded documentation and decision tracing

## Related Documents

- **Source Principles:** [PRINCIPLES.md - Principle 13: Code Without Docs is Incomplete](../PRINCIPLES.md#principle-13-code-without-docs-is-incomplete), [Principle 16: Living Law](../PRINCIPLES.md#principle-16-these-principles-are-living-law)
- **Governance Authority:** [GOVERNANCE.md - Traceability Requirements](../GOVERNANCE.md)
- **Human Mandate:** [HUMAN_MANDATE.md - Guardian Role Metaphors](../HUMAN_MANDATE.md)
- **Implementation:** `the-citadel/terraform/labels.tf`, `the-citadel/terraform/validation.tf`

## Change History

- **2024-09-30** - Initial creation with core/contextual label hierarchy and resource class examples
