# SEC-005: Machine Identity Management

**Policy ID:** SEC-005
**Category:** Security
**Effective Date:** 2026-03-02
**Last Updated:** 2026-03-02

## Statement

All machine-to-platform authentication **must** use short-lived, scoped credentials issued by a registered identity (GitHub App, OIDC provider, or platform-native token). Static, long-lived credentials (Classic PATs, service account passwords, manually-created API keys) are **prohibited** for automation. Every machine identity **must** be registered in the organization's identity registry, scoped to the minimum permissions required, and auditable by name.

## Rationale

Machine identities now outnumber human identities in modern organizations. Unmanaged machine credentials are the most common vector for lateral movement, privilege escalation, and persistent access after compromise:

- **Static Credentials Rot**: Long-lived tokens accumulate privileges and are forgotten until breached
- **Attribution Gap**: Shared service accounts and Classic PATs obscure who did what
- **Blast Radius**: Broadly-scoped tokens amplify the impact of a single compromise
- **Seat Cost**: Service accounts tied to human users consume paid seat licenses unnecessarily
- **Rotation Burden**: Manual rotation of long-lived credentials is error-prone and routinely skipped
- **Audit Blindness**: Generic "bot" or "ci-user" identities defeat forensic investigation

Short-lived, scoped machine identities eliminate these risks by design.

## Scope

**Applies To:**
- All GitHub API automation (CI/CD, Terraform, bots, integrations)
- All cloud provider service-to-service authentication (AWS, GCP, Cloudflare)
- All CLI tooling that authenticates to external platforms
- All cross-organization automation

**Exceptions:**
- `GITHUB_TOKEN` within GitHub Actions workflows (platform-managed, job-scoped, automatic)
- Developer Fine-grained PATs for local CLI use (subject to org approval policy and 90-day max expiry)
- Break-glass credentials stored in gopass (subject to GOV-003 emergency procedures)

## Identity Hierarchy for Machines

```
┌─────────────────────────────────────────────────────────────┐
│                    MACHINE IDENTITIES                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  TIER 1: PLATFORM-NATIVE (Preferred)                  │  │
│  │  ► GITHUB_TOKEN (job-scoped, automatic)               │  │
│  │  ► OIDC Workload Identity (AWS, GCP, Cloudflare)      │  │
│  │  Lifespan: Minutes to 1 hour                          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  TIER 2: GITHUB APPS (Primary for GitHub API)         │  │
│  │  ► Installation Access Token (1-hour lifespan)        │  │
│  │  ► Private key signs JWT → exchanges for IAT          │  │
│  │  ► No seat cost, org-level audit attribution          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  TIER 3: FINE-GRAINED PATs (Developer CLI only)       │  │
│  │  ► 90-day maximum expiry                              │  │
│  │  ► Org approval required                              │  │
│  │  ► Repository-scoped, not "All repositories"          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  PROHIBITED                                            │  │
│  │  ✗ Classic PATs                                        │  │
│  │  ✗ Service account users (human accounts used by bots)│  │
│  │  ✗ Manually-created API keys without expiry            │  │
│  │  ✗ Shared credentials across organizations             │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Implementation

### Technical Enforcement

**GitHub App as Primary Machine Identity:**

```hcl
# the-citadel/terraform/github/apps.tf (conceptual)
#
# Each GitHub organization gets its own GitHub App.
# The App's private key is stored in the secrets vault.
# Automation exchanges the key for a 1-hour Installation Access Token.

# Provider configuration using GitHub App authentication
provider "github" {
  alias = "seven-springs"
  owner = "seven-springs"

  app_auth {
    id              = var.github_app_id_seven_springs
    installation_id = var.github_app_installation_id_seven_springs
    pem_file        = var.github_app_pem_seven_springs  # From secrets vault
  }
}
```

**Organization Token Policy:**

```hcl
# Enforce Fine-grained PAT requirements at the org level
# (Conceptual - managed via GitHub org settings)
#
# Settings > Personal access tokens > Settings:
#   - Require approval for Fine-grained PATs: ENABLED
#   - Restrict Classic PATs: ENABLED (block creation)
#   - Default expiry: 90 days maximum
```

**OIDC Federation (Cloud Providers):**

```hcl
# GitHub Actions → AWS (no stored credentials)
resource "aws_iam_openid_connect_provider" "github_actions" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["ffffffffffffffffffffffffffffffffffffffff"]
}

# GitHub Actions → GCP (no stored credentials)
resource "google_iam_workload_identity_pool_provider" "github" {
  # See IAM Specification for full configuration
}
```

### Automated Validation

**Identity Registry Audit:**
- All GitHub Apps registered in `the-citadel/terraform/github/apps.tf` (IaC-managed)
- Monthly automated scan for Classic PATs across all orgs
- Push Protection blocks committed private keys and tokens
- Expiry warnings for Fine-grained PATs via GitHub webhook

**Permission Drift Detection:**
- Weekly scan comparing App permissions against the spec
- Alert on any permission added outside of Terraform
- Quarterly review of Installation Access Token usage patterns

### Human Process

1. **App Registration**: New GitHub Apps proposed via PR to the-citadel, reviewed per Citadel governance (1 Mentor + 1 Watcher)
2. **Private Key Custody**: Private keys stored in secrets vault (gopass now, Infisical after POC 2)
3. **Permission Review**: Quarterly review of all App permissions against actual usage
4. **Decommissioning**: Unused Apps removed via PR, private keys destroyed

## Naming Convention

| Component | Pattern | Example |
|-----------|---------|---------|
| GitHub App | `tng-{repo}-{purpose}` | `tng-citadel-automation` |
| IAM Role (AWS) | `nash-{tenant}-{service}-deployer` | `nash-personal-github-deployer` |
| Service Account (GCP) | `nash-{tenant}-{service}-deployer` | `nash-personal-tf-deployer` |
| Fine-grained PAT | `{user}-{purpose}-{expiry}` | `jeffrey-cli-2026Q2` |

## Multi-Organization Strategy

Each GitHub organization **must** have its own GitHub App installation:

| Organization | App Name | Purpose | Permissions |
|-------------|----------|---------|-------------|
| The-Nash-Group | `tng-citadel-automation` | Terraform IaC management | `administration:write`, `contents:write`, `members:read` |
| seven-springs | `tng-citadel-automation` | Terraform IaC management | `administration:write`, `contents:write` |
| jefahnierocks | `tng-citadel-automation` | Terraform IaC management | `administration:write`, `contents:write` |
| happy-patterns | `tng-citadel-automation` | Terraform IaC management | `administration:write`, `contents:write` |
| litecky-editing | `tng-citadel-automation` | Terraform IaC management | `administration:write`, `contents:write` |

**Strategy**: One App registered in The-Nash-Group, installed across all subsidiary orgs. This provides:
- Single private key to manage
- Consistent audit attribution ("tng-citadel-automation" in all org logs)
- Per-installation permission scoping (subsidiaries can have fewer permissions)

## Compliance Verification

**Automated Checks:**
- No Classic PATs detected across any organization (monthly scan)
- All GitHub Apps registered in Terraform (drift detection)
- All Fine-grained PATs have expiry <= 90 days
- Push Protection enabled on all repositories (SEC-002 cross-reference)

**Manual Audits:**
- Quarterly review of GitHub App permissions vs. actual usage
- Quarterly review of Fine-grained PAT approvals
- Annual review of OIDC trust relationships

**Reporting:**
- Dashboard showing active machine identities per org
- Token expiry calendar with 14-day advance warnings
- Audit log of all Installation Access Token issuances

## Related Documents

- **Source Principles:**
  - [Principle 5: Infrastructure as Code](../PRINCIPLES.md) — Machine identities managed as code
  - [Principle 6: Secrets Never Committed](../PRINCIPLES.md) — Private keys never in git
  - [Principle 9: Zero Trust](../PRINCIPLES.md) — Every machine request authenticated
  - [Principle 10: Least Privilege](../PRINCIPLES.md) — Minimum permissions per identity
- **Related Policies:**
  - [SEC-001: Zero Trust Authentication](./sec-001-zero-trust.md)
  - [SEC-002: Secret Scanning](./sec-002-secret-scanning.md)
  - [SEC-003: Least Privilege Access](./sec-003-least-privilege.md)
  - [GOV-003: Break-Glass Procedures](./gov-003-break-glass.md)
  - [GOV-010: Organizational Labeling](./gov-010-labeling-standard.md)
- **Specifications:**
  - [IAM Specification](./specs/iam-specification.md) — AWS/GCP identity architecture
  - [GitHub Machine Identity Specification](./specs/github-machine-identity.md) — GitHub App implementation details
- **Implementation:** `the-citadel/terraform/github/apps.tf`

## Change History

- **2026-03-02** - Initial creation implementing Principles 5, 6, 9, 10 for GitHub and cross-platform machine identities
