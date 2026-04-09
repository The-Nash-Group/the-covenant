# ADR-003: Establish Cloudflare Governance Baseline (Greenfield)

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2025-11-21 |
| **Last Updated** | 2026-04-08 |
| **Author** | Agent |
| **Governance Level** | Citadel (1 Mentor + 1 Watcher) |
| **Status** | Accepted |
| **Related ADRs** | ADR-001, ADR-004, ADR-005 |

> **Current-state note (2026-04-08)**: The active Cloudflare implementation no longer uses the pre-ADR-005 monolithic path shown in older examples below. Current Citadel Cloudflare management lives in `the-citadel/terraform/modules/cloudflare-zone-standard/` plus per-workspace roots under `the-citadel/terraform/orgs/<workspace>/`. The baseline zone-settings layer is converged for `thenash.group` and `jefahnierocks.com`, and new Cloudflare delivery resources now follow the transitional ownership rule captured in `the-covenant/policies/specs/cloudflare-ownership-transition.md`.

## Context

### Problem

The Nash Group is initializing its edge security and Zero Trust networking layer via Cloudflare. We are in a **greenfield state** with no legacy technical debt or binding configurations.

Traditionally, cloud infrastructure follows this anti-pattern:
1. Resources are created manually via web console ("ClickOps")
2. Configuration drift accumulates over time
3. Infrastructure is later "discovered" and retrofitted into Terraform
4. Documentation lags reality by weeks or months
5. Security misconfigurations persist undetected

This approach violates:
- **Covenant Principle #5** (Infrastructure as Code)
- **Covenant Principle #9** (Zero Trust)
- **Covenant Principle #13** (Code Without Docs is Incomplete)
- **Covenant Principle #14** (Progress Without Breakage)

### Constraints

1. **Greenfield advantage**: No existing infrastructure to import or reconcile
2. **Multi-organizational future**: Must support multiple distinct domains/organizations under single Cloudflare account
3. **Zero Trust mandate**: All access must be identity-based from day zero
4. **Professional operations**: Must operate at enterprise standards despite single-operator reality
5. **Agent collaboration**: Must support both human Guardians and autonomous agents

### Assumptions

1. Cloudflare will be the primary edge security and CDN provider
2. Multiple distinct organizations will be managed (personal, family, business, etc.)
3. Human operators will resist "ClickOps" temptation if tooling is excellent
4. Automated policy enforcement can prevent 90%+ of security misconfigurations
5. cf-terraforming tool is available for future reconciliation if needed

### Alternatives Considered

#### Alternative 1: Traditional "Import Later" Approach
**Rejected**: Would allow drift from day one, violate IaC principle, require reconciliation effort later

**Reasoning**: Greenfield state is rare gift - squandering it with manual configuration would be architectural malpractice

#### Alternative 2: Monolithic Single-Tenant Structure
**Rejected**: Would require restructuring when adding second organization, violates future-proofing

**Reasoning**: Professional multi-tenant architecture costs ~10% more upfront effort, saves 300%+ on second deployment

#### Alternative 3: Per-Zone Repositories
**Rejected**: Would fragment governance, create approval bottlenecks, violate single source of truth

**Reasoning**: Centralized governance with modular implementation provides best balance

## Decision

### Summary

We will adopt a **"Code-First, Validate-Always"** Iron Gate architecture for Cloudflare, establishing multi-tenant professional infrastructure patterns from day zero with automated policy enforcement.

### Rationale

**Greenfield deployment allows us to**:
1. Define the *ideal* state in code, then create reality to match
2. Enforce security policies *before* vulnerable configurations exist
3. Establish patterns that scale to N organizations with zero refactoring
4. Create executable documentation that cannot drift from reality
5. Demonstrate agent-capable infrastructure from inception

**This decision implements**:
- Covenant Principle #5: Infrastructure as Code (all config in git)
- Covenant Principle #9: Zero Trust (identity-based access only)
- Covenant Principle #10: Least Privilege (module-enforced defaults)
- Covenant Principle #13: Code Without Docs is Incomplete (Terraform is documentation)

### Implementation

#### Component 1: Iron Gate Architecture

All Cloudflare configurations must pass through validation pipeline before deployment.

**Pipeline stages**:
1. **Terraform Format** - Enforce HCL style consistency
2. **Terraform Validate** - Catch syntax errors and invalid references
3. **OPA Policy Check** - Enforce security policies (SEC-003, SEC-004)
4. **OpenTofu Plan** - Generate speculative plan in GitHub Actions or approved local workflow
5. **Human Review** - Guardian approves or rejects
6. **Terraform Apply** - Deploy to Cloudflare (auto or manual trigger)
7. **Drift Detection** - Nightly verification of state integrity

**Source of Truth**: `the-citadel/terraform/providers/cloudflare/`

#### Component 2: Multi-Tenant Directory Structure

Professional-grade organization supporting multiple distinct entities:

```
the-citadel/terraform/providers/cloudflare/
├── modules/
│   ├── standard_zone/          # Baseline security + performance for ANY zone
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── zero_trust_app/         # Standard Access Application pattern
│   └── workers_app/            # Standard Workers deployment
├── global/
│   ├── account.tf              # Cloudflare account settings
│   ├── teams.tf                # Zero Trust "Team" (homezerotrust)
│   ├── gateway.tf              # Global DNS/HTTP filtering rules
│   └── access_groups.tf        # Reusable Access Groups
└── zones/
    ├── thenash-group/          # Parent organization (thenash.group)
    │   ├── main.tf
    │   ├── dns.tf
    │   ├── workers.tf
    │   └── terraform.tfvars
    ├── happy-patterns-co/      # Happy Patterns LLC (happy-patterns.co; .com redirects)
    │   └── main.tf
    ├── jefahnierocks-com/      # Personal/creative (jefahnierocks.com)
    │   └── main.tf
    ├── litecky-editing/        # Professional editing
    │   └── main.tf
    └── README.md
```

**Rationale**:
- `modules/` - Reusable security patterns (DRY principle)
- `global/` - Account-level configuration (applied once)
- `zones/` - Per-domain configuration (scales to N organizations)

#### Component 3: Security Policies (OPA)

Automated policy enforcement via Open Policy Agent:

**Policy SEC-004: Cloudflare Security Baseline**
```rego
# Located: the-citadel/policies/opa/sec-004-cloudflare-baseline.rego

# DENY: Unproxied DNS records (exposes origin IP)
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "cloudflare_record"
    resource.change.after.type == "A"
    resource.change.after.proxied == false
    not resource.change.after.comment contains "EXEMPTION"
    msg := sprintf("DNS record %s must be proxied (Orange Cloud)", [resource.change.after.name])
}

# DENY: Non-strict SSL mode
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "cloudflare_zone_settings_override"
    resource.change.after.settings[0].ssl != "strict"
    msg := "Zone SSL mode must be 'strict'"
}

# DENY: Access policies without IdP group selector
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "cloudflare_access_policy"
    not has_idp_group(resource.change.after.include)
    msg := "Access policies must include IdP group selector (no Everyone/IP-only)"
}
```

**Policy SEC-003: Least Privilege** (existing, applies to all Terraform)

#### Component 4: Standard Zone Module

Baseline security configuration applied to all zones:

```hcl
# modules/standard_zone/main.tf
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

variable "zone_id" {
  type        = string
  description = "Cloudflare Zone ID"
}

variable "domain" {
  type        = string
  description = "Domain name for this zone"
}

# Enforce Strict SSL (SEC-004)
resource "cloudflare_zone_settings_override" "security_baseline" {
  zone_id = var.zone_id

  settings {
    # SSL/TLS Configuration
    ssl                      = "strict"
    always_use_https         = "on"
    automatic_https_rewrites = "on"
    tls_1_3                  = "on"
    min_tls_version          = "1.2"

    # Security Headers (Covenant Principle #9: Zero Trust)
    security_header {
      enabled            = true
      include_subdomains = true
      max_age            = 31536000
      nosniff            = true
      preload            = true
    }

    # Performance Optimization
    brotli               = "on"
    minify {
      css  = "on"
      js   = "on"
      html = "on"
    }

    # Caching Strategy
    browser_cache_ttl = 14400
    cache_level       = "aggressive"

    # Bot Protection
    browser_check    = "on"
    challenge_ttl    = 1800
    security_level   = "medium"
  }
}

# Baseline WAF Protection (SEC-004)
resource "cloudflare_ruleset" "managed_waf" {
  zone_id     = var.zone_id
  name        = "Managed WAF - ${var.domain}"
  description = "Cloudflare Managed Ruleset for baseline protection"
  kind        = "zone"
  phase       = "http_request_firewall_managed"

  rules {
    action = "execute"
    action_parameters {
      id      = "efb7b8c949ac4650a09736fc376e9aee" # Cloudflare Managed Ruleset
      version = "latest"
    }
    expression = "true"
    enabled    = true
  }
}

# OWASP Core Ruleset (SEC-004)
resource "cloudflare_ruleset" "owasp_core" {
  zone_id     = var.zone_id
  name        = "OWASP Core Ruleset - ${var.domain}"
  description = "OWASP Top 10 protection"
  kind        = "zone"
  phase       = "http_request_firewall_managed"

  rules {
    action = "execute"
    action_parameters {
      id      = "4814384a9e5d4991b9815dcfc25d2f1f" # OWASP Core Ruleset
      version = "latest"
    }
    expression = "true"
    enabled    = true
  }
}

output "zone_id" {
  value       = var.zone_id
  description = "Zone ID for reference by other resources"
}
```

#### Component 5: Instantiation Pattern

Each organization's zone follows this pattern:

```hcl
# zones/thenash-group/main.tf
module "security_baseline" {
  source  = "../../modules/standard_zone"
  zone_id = var.cloudflare_zone_id
  domain  = "thenash.group"
}

# DNS Records (all proxied per SEC-004)
resource "cloudflare_record" "www" {
  zone_id = var.cloudflare_zone_id
  name    = "www"
  value   = "origin.example.com"
  type    = "CNAME"
  proxied = true
  comment = "Main website"
}

resource "cloudflare_record" "api" {
  zone_id = var.cloudflare_zone_id
  name    = "api"
  value   = "192.0.2.1"
  type    = "A"
  proxied = true
  comment = "API endpoint"
}

# EXEMPTION example (requires justification)
resource "cloudflare_record" "mail" {
  zone_id = var.cloudflare_zone_id
  name    = "mail"
  value   = "192.0.2.10"
  type    = "A"
  proxied = false
  comment = "EXEMPTION: Mail server cannot be proxied (SMTP/IMAP protocols)"
}
```

## Consequences

### Positive

1. **Auditability**: Every DNS record, WAF rule, and security setting is git-tracked with full history
2. **Security**: Misconfigurations (e.g., exposing origin IPs) blocked by OPA *before* they exist in production
3. **Scalability**: Onboarding a new subsidiary zone requires ~20 lines of code (module instantiation)
4. **Documentation**: Terraform configuration IS the documentation (cannot drift)
5. **Agent-Ready**: Autonomous agents can propose infrastructure changes via PRs
6. **Professional Standards**: Enterprise-grade patterns despite single-operator reality
7. **Zero Reconciliation**: No "import existing state" technical debt to pay down
8. **Velocity**: After initial setup, new zones deploy in < 5 minutes

### Negative

1. **Initial Velocity**: First zone takes 2-4 hours vs. 15 minutes of ClickOps
2. **Quick Fixes Slower**: "Just add a DNS record" now requires PR + pipeline (adds 5-10 minutes)
3. **Module Maintenance**: standard_zone module becomes critical path, must be maintained carefully
4. **Policy Complexity**: OPA policies add cognitive overhead for new contributors
5. **Exemption Process**: Legitimate edge cases (e.g., mail servers) require code comments and documentation

### Neutral

1. **Cloudflare Dashboard**: Becomes read-only for operations (write-only during break-glass)
2. **Learning Curve**: Guardians must learn Terraform + OPA (but this knowledge compounds)
3. **Tooling Dependency**: Relies on cf-terraforming for emergency reconciliation

### Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Module bug affects all zones** | High | Comprehensive testing, staging environment, gradual rollout |
| **OPA policy too strict, blocks legitimate changes** | Medium | Exemption mechanism via code comments, policy can be updated |
| **Guardian bypasses IaC during incident** | Low | Break-glass protocol requires 24h reconciliation, documented in BREAK_GLASS.md |
| **Single point of failure (the-citadel repo)** | Medium | Nightly backups, local working copies, Hetzner Object Storage versioning |

## Compliance

### Covenant Principles Implemented

- **Principle #5**: Infrastructure as Code - All Cloudflare config lives in Terraform
- **Principle #9**: Zero Trust - Identity-based access enforced by policy
- **Principle #10**: Least Privilege - Module defaults to minimal exposure
- **Principle #13**: Code Without Docs is Incomplete - Terraform IS the docs
- **Principle #14**: Progress Without Breakage - Staging validation before production

### Policies Created/Modified

- **SEC-004-cloudflare-baseline.rego** (NEW) - Cloudflare-specific security checks
  - Enforce proxied DNS records
  - Enforce strict SSL mode
  - Enforce identity-based Access policies
  - Validate WAF rulesets enabled

- **SEC-003-least-privilege.rego** (EXISTING) - General least privilege checks
  - Applies to all Terraform resources including Cloudflare

### Per-Subsidiary Governance

Not all Cloudflare zones require the same governance level:

| Zone | Governance | Rationale |
|------|-----------|-----------|
| `thenash.group` | Citadel | Parent org, infrastructure backbone |
| `happy-patterns.co` | Citadel | Production LLC, customer-facing |
| `jefahnierocks.com` | Stronghold | Personal, lower blast radius |
| `litecky-editing` domains | Stronghold | Small business, lower blast radius |

All zones still use the `standard_zone` module and pass OPA policy checks — governance level affects approval requirements, not security baselines.

## Implementation Plan

### Phase 1: Foundation (Week 1)

**Tasks**:
1. Create directory structure: `providers/cloudflare/modules/`, `global/`, `zones/`
2. Implement `standard_zone` module with security baselines
3. Create OPA policy: `sec-004-cloudflare-baseline.rego`
4. Document module usage in README.md

**Deliverables**:
- `terraform/providers/cloudflare/` structure
- Reusable security module
- Automated policy enforcement
- Complete documentation

### Phase 2: First Zone (Week 1)

**Tasks**:
1. Instantiate `standard_zone` for first organization
2. Add DNS records following proxy-by-default pattern
3. Validate with `terraform plan`
4. Run OPA policy checks
5. Apply to production

**Deliverables**:
- First zone deployed via IaC
- All security policies passing
- Zero manual console configuration

### Phase 3: CI/CD Integration (Week 2)

**Tasks**:
1. Update `.github/workflows/terraform.yml` for Cloudflare provider
2. Add OPA validation step to pipeline
3. Configure the-citadel OpenTofu workspace and CI for the Cloudflare provider
4. Test end-to-end PR → Apply workflow

**Deliverables**:
- Automated pipeline with policy gates
- Documented approval workflow
- Guardian training on new process

### Phase 4: Documentation & Training (Week 2)

**Tasks**:
1. Update `the-citadel/CLAUDE.md` with Cloudflare structure
2. Create `docs/CLOUDFLARE-ARCHITECTURE.md`
3. Document exemption process for unproxied records
4. Create runbook for adding new zones

**Deliverables**:
- Complete Cloudflare documentation
- Agent-readable context files
- Human-readable procedures

## Validation Criteria

**This ADR is successfully implemented when**:

1. ✅ Directory structure exists: `providers/cloudflare/modules/`, `global/`, `zones/`
2. ✅ `standard_zone` module deploys successfully to test zone
3. ✅ OPA policy `sec-004-cloudflare-baseline.rego` passes for compliant config
4. ✅ OPA policy DENIES unproxied A records without EXEMPTION comment
5. ✅ OPA policy DENIES non-strict SSL mode
6. ✅ First production zone deployed entirely via Terraform
7. ✅ Zero manual console changes made
8. ✅ CI/CD pipeline enforces policies before apply
9. ✅ Documentation complete and agent-readable

## References

- [Covenant Principle #5: Infrastructure as Code](../../PRINCIPLES.md#principle-5-infrastructure-as-code)
- [Covenant Principle #9: Zero Trust](../../PRINCIPLES.md#principle-9-zero-trust)
- [ADR-001: Three-Pillar Repository Architecture](./001-establish-three-pillar-repository-architecture.md)
- [BREAK_GLASS.md](../../../the-citadel/BREAK_GLASS.md) - Emergency procedures
- [cf-terraforming Integration](../../../the-citadel/docs/CLOUDFLARE-TERRAFORMING.md)
- [Terraform Cloudflare Provider](https://registry.terraform.io/providers/cloudflare/cloudflare/latest/docs)

---

> **Living Documents**: ADRs may be updated when facts change, but changes require Guardian approval. Edit in place and add a changelog entry rather than creating a superseding ADR.

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2025-11-21 | Agent | Initial creation — Cloudflare governance baseline proposed |
| 2026-03-02 | Agent | Replaced placeholder domains with real subsidiary names (thenash-group, happy-patterns-co, jefahnierocks-com, litecky-editing). Added per-subsidiary governance table. Updated metadata to match new template format. Confirmed OPA policy path at the-citadel/policies/opa/. |
| 2026-04-05 | Agent | Recorded current implementation state: Cloudflare v5.18.0 migration delivered, SEC-004 enforced from the-citadel CI, and the baseline now expressed through individual `cloudflare_zone_setting` resources. |
| 2026-04-08 | Agent | Marked the ADR accepted and added a current-state note for the delivered OpenTofu multi-workspace architecture and Cloudflare ownership transition rule. |
