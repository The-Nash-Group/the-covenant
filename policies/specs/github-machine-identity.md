# GitHub Machine Identity Specification

**Version**: 1.0.0
**Created**: 2026-03-02
**Updated**: 2026-03-02
**Policies**: SEC-005 (Machine Identity), SEC-001 (Zero Trust), SEC-003 (Least Privilege), INF-001 (Infrastructure as Code)

---

## Governing Principles

| Principle | Implementation |
|-----------|----------------|
| **SEC-005: Machine Identity** | GitHub Apps as primary machine identity; no Classic PATs |
| **SEC-001: Zero Trust** | Every API call authenticated via Installation Access Token |
| **SEC-003: Least Privilege** | Per-installation permission scoping; minimum required permissions |
| **INF-001: Infrastructure as Code** | App configuration managed via Terraform in the-citadel |
| **GOV-010: Labeling** | All Apps follow `tng-{repo}-{purpose}` naming convention |

---

## 1. GitHub App Architecture

### 1.1 Identity Model

The Nash Group uses a **single GitHub App, multi-installation** model:

```
┌────────────────────────────────────────────────────┐
│  GitHub App: tng-citadel-automation                │
│  Registered in: The-Nash-Group org                 │
│  Owner: @verlyn13                                  │
│                                                     │
│  Private Key (.pem)                                │
│  └── Stored in: gopass (now), Infisical (future)   │
│                                                     │
│  Installations:                                     │
│  ├── The-Nash-Group    (all repos, full perms)     │
│  ├── seven-springs     (all repos, scoped perms)   │
│  ├── jefahnierocks     (all repos, scoped perms)   │
│  ├── happy-patterns    (all repos, scoped perms)   │
│  └── litecky-editing   (all repos, scoped perms)   │
└────────────────────────────────────────────────────┘
```

**Why single App, not one per org?**
- One private key to rotate and protect
- Consistent audit trail ("tng-citadel-automation" in every org's audit log)
- Centralized permission governance (the-citadel manages all installations)
- Simpler Terraform provider configuration

### 1.2 Token Lifecycle

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Private Key │────►│     JWT      │────►│   Install.   │
│  (.pem file) │     │  (10 min)    │     │ Access Token │
│              │     │              │     │   (1 hour)   │
│  Stored in   │     │  Signed by   │     │              │
│  secrets     │     │  private key │     │  Used for    │
│  vault       │     │              │     │  GitHub API  │
└──────────────┘     └──────────────┘     └──────────────┘
     Never               Ephemeral            Ephemeral
     leaves              (generated           (exchanged
     vault               on-demand)           via API)
```

**Step-by-step:**

1. **Sign**: Automation reads private key from secrets vault, signs a JWT with:
   - `iss`: App ID
   - `iat`: Current timestamp
   - `exp`: Current timestamp + 600 (10 minutes max)

2. **Exchange**: POST the JWT to `https://api.github.com/app/installations/{id}/access_tokens`
   - Response: Installation Access Token (IAT) valid for 1 hour
   - Can scope IAT to specific repositories and permissions at exchange time

3. **Use**: All GitHub API calls use the IAT as Bearer token

4. **Expire**: Token automatically expires after 1 hour — no revocation needed

---

## 2. App Registration

### 2.1 Required App Settings

| Setting | Value | Rationale |
|---------|-------|-----------|
| **Name** | `tng-citadel-automation` | Per SEC-005 naming convention |
| **Description** | "The Nash Group infrastructure automation via the-citadel" | Clear purpose |
| **Homepage URL** | `https://github.com/The-Nash-Group/citadel-config` | Points to IaC repo |
| **Webhook** | Disabled (unless needed for events) | Minimize attack surface |
| **Request user auth** | Disabled | Machine-only identity |
| **Expire user auth tokens** | N/A (no user auth) | — |

### 2.2 Permission Matrix

**Repository Permissions:**

| Permission | Access | Rationale |
|------------|--------|-----------|
| `administration` | Read & Write | Create/configure repos, manage settings |
| `contents` | Read & Write | Manage files, branches (for IaC-managed repos) |
| `metadata` | Read | Required (always granted) |
| `pull_requests` | Read & Write | Manage PRs for automated workflows |
| `issues` | Read & Write | Manage issues for tracking |
| `workflows` | Read & Write | Manage GitHub Actions workflows |

**Organization Permissions:**

| Permission | Access | Rationale |
|------------|--------|-----------|
| `members` | Read | Audit team memberships |
| `organization_administration` | Read & Write | Manage org settings via Terraform |
| `organization_custom_roles` | Read | Audit custom roles |

**Not Granted (Least Privilege):**

| Permission | Reason Excluded |
|------------|-----------------|
| `actions` | Not needed for Terraform management |
| `packages` | Not managing GitHub Packages |
| `secrets` | Secrets managed via Infisical/gopass, not GitHub |
| `security_events` | Read-only audit handled separately |
| `single_file` | Not needed — use `contents` with repo scoping |

### 2.3 Per-Installation Permission Scoping

Subsidiary orgs receive **reduced permissions** at installation time:

| Organization | Repository Access | Extra Restrictions |
|-------------|-------------------|--------------------|
| **The-Nash-Group** | All repositories | Full permission set |
| **seven-springs** | All repositories | No `organization_administration` |
| **jefahnierocks** | All repositories | No `organization_administration` |
| **happy-patterns** | All repositories | No `organization_administration` |
| **litecky-editing** | All repositories | No `organization_administration` |

---

## 3. Terraform Integration

### 3.1 Provider Configuration

```hcl
# the-citadel/terraform/providers.tf

# Primary org — uses GitHub App authentication
provider "github" {
  owner = "The-Nash-Group"

  app_auth {
    id              = var.github_app_id
    installation_id = var.github_app_installation_the_nash_group
    pem_file        = var.github_app_pem  # Injected from secrets vault
  }
}

# Subsidiary orgs — aliased providers using same App, different installations
provider "github" {
  alias = "seven_springs"
  owner = "seven-springs"

  app_auth {
    id              = var.github_app_id
    installation_id = var.github_app_installation_seven_springs
    pem_file        = var.github_app_pem  # Same key, different installation
  }
}

provider "github" {
  alias = "jefahnierocks"
  owner = "jefahnierocks"

  app_auth {
    id              = var.github_app_id
    installation_id = var.github_app_installation_jefahnierocks
    pem_file        = var.github_app_pem
  }
}

provider "github" {
  alias = "happy_patterns"
  owner = "happy-patterns"

  app_auth {
    id              = var.github_app_id
    installation_id = var.github_app_installation_happy_patterns
    pem_file        = var.github_app_pem
  }
}

provider "github" {
  alias = "litecky_editing"
  owner = "litecky-editing"

  app_auth {
    id              = var.github_app_id
    installation_id = var.github_app_installation_litecky_editing
    pem_file        = var.github_app_pem
  }
}
```

### 3.2 Variables

```hcl
# the-citadel/terraform/variables.tf (additions)

variable "github_app_id" {
  description = "GitHub App ID for tng-citadel-automation"
  type        = string
  sensitive   = false  # App ID is not secret
}

variable "github_app_pem" {
  description = "Private key (.pem) for the GitHub App — from secrets vault"
  type        = string
  sensitive   = true
}

variable "github_app_installation_the_nash_group" {
  description = "Installation ID for The-Nash-Group org"
  type        = string
  sensitive   = false
}

variable "github_app_installation_seven_springs" {
  description = "Installation ID for seven-springs org"
  type        = string
  sensitive   = false
}

variable "github_app_installation_jefahnierocks" {
  description = "Installation ID for jefahnierocks org"
  type        = string
  sensitive   = false
}

variable "github_app_installation_happy_patterns" {
  description = "Installation ID for happy-patterns org"
  type        = string
  sensitive   = false
}

variable "github_app_installation_litecky_editing" {
  description = "Installation ID for litecky-editing org"
  type        = string
  sensitive   = false
}
```

### 3.3 GitHub Actions and Local OpenTofu Configuration

GitHub App credentials are injected into CI and local runs through approved secret paths, **not** checked-in `.tfvars` files:

| Variable | Category | Sensitive | Source |
|----------|----------|-----------|--------|
| `APP_ID` / `TF_VAR_github_app_id` | GitHub Actions secret / local env | No | GitHub App settings page / gopass |
| `APP_PEM` / `TF_VAR_github_app_pem_file` | GitHub Actions secret / local env | **Yes** | Downloaded `.pem`, stored in gopass as PEM contents |
| `steps.app-token.outputs.installation-id` / `TF_VAR_github_app_installation_id` | Workflow output / local env | No | GitHub App installation page |

---

## 4. Private Key Management

### 4.1 Storage

**Current (Pre-Infisical):**

```bash
# Store in gopass
gopass insert -m infra/github-app/private-key

# Retrieve for local OpenTofu use
export TF_VAR_github_app_pem_file="$(gopass cat infra/github-app/private-key)"
tofu plan
```

**Future (Post-Infisical, after POC 2):**

```bash
# Store in Infisical
infisical secrets set GITHUB_APP_PEM --env=production --project=the-citadel

# Retrieve for local use
eval $(infisical export --format=dotenv --env=production --project=the-citadel)
terraform plan
```

### 4.2 Rotation

Private keys **should** be rotated every 6 months:

1. Generate new private key in GitHub App settings (old key remains valid)
2. Store new key in secrets vault
3. Update GitHub Actions `APP_PEM` secret and local gopass entry
4. Verify OpenTofu can authenticate with new key
5. Delete old key from GitHub App settings
6. Delete old key from secrets vault

### 4.3 Compromise Response

If a private key is suspected compromised:

1. **Immediately** delete all private keys in GitHub App settings (revokes all IATs)
2. Generate a new private key
3. Store in secrets vault
4. Update GitHub Actions `APP_PEM` secret and local gopass entry
5. Audit GitHub audit log for unauthorized actions
6. File incident report per OPS-010

---

## 5. GitHub Actions Integration

### 5.1 Workflow Token Exchange

For workflows that need cross-org access (beyond `GITHUB_TOKEN`):

```yaml
# .github/workflows/cross-org.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Generate Installation Access Token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ vars.TNG_APP_ID }}
          private-key: ${{ secrets.TNG_APP_PEM }}
          owner: seven-springs  # Target org

      - name: Use token for cross-org operations
        env:
          GH_TOKEN: ${{ steps.app-token.outputs.token }}
        run: |
          gh repo list seven-springs --limit 10
```

### 5.2 When to Use Each Token Type

| Scenario | Token | Rationale |
|----------|-------|-----------|
| Same-repo CI/CD | `GITHUB_TOKEN` | Automatic, job-scoped, zero config |
| Cross-repo in same org | GitHub App IAT | Scoped to installation repos |
| Cross-org operations | GitHub App IAT (different installation) | Per-org installation scoping |
| Local developer CLI | Fine-grained PAT | User-attributed, org-approved |
| Emergency access | Fine-grained PAT (break-glass) | Per GOV-003, 24h expiry |

---

## 6. Fine-grained PAT Policy

### 6.1 Organization Settings

Every Nash Group org **must** configure:

| Setting | Value |
|---------|-------|
| Allow Fine-grained PATs | Yes |
| Require admin approval | Yes |
| Allow Classic PATs | **No** (restrict creation) |
| Default token expiry | 90 days maximum |

### 6.2 Developer PAT Standards

| Requirement | Rule |
|-------------|------|
| Expiry | Maximum 90 days |
| Repository scope | "Only select repositories" — never "All" |
| Naming | `{user}-{purpose}-{quarter}` (e.g., `jeffrey-cli-2026Q2`) |
| Permissions | Minimum required for stated purpose |
| Rotation | Re-create before expiry; do not extend |

---

## 7. Audit and Compliance

### 7.1 Audit Log Attribution

| Identity Type | Audit Log Shows | Example |
|--------------|-----------------|---------|
| GitHub App | App name + installation | `tng-citadel-automation[bot]` |
| Fine-grained PAT | User name | `verlyn13` |
| `GITHUB_TOKEN` | `github-actions[bot]` | Workflow run link |

### 7.2 Compliance Checks

```bash
# Quarterly compliance verification

# 1. List all GitHub Apps installed in each org
gh api /orgs/The-Nash-Group/installations | jq '.[].app_slug'
gh api /orgs/seven-springs/installations | jq '.[].app_slug'

# 2. Verify no Classic PATs exist (org admin)
# Settings > Personal access tokens > Active tokens > filter "Classic"

# 3. Verify all Fine-grained PATs have expiry <= 90 days
# Settings > Personal access tokens > Active tokens > check expiry dates

# 4. Verify App permissions match spec
gh api /apps/tng-citadel-automation | jq '.permissions'
```

---

## 8. Implementation Checklist

### Phase 1: App Creation (POC 1 Scope)

- [ ] Register `tng-citadel-automation` GitHub App in The-Nash-Group org
- [ ] Set permissions per Section 2.2
- [ ] Generate private key, store in gopass
- [ ] Install App in seven-springs org (POC target)
- [ ] Configure Terraform provider with App auth
- [ ] Verify: `terraform plan` authenticates via App

### Phase 2: Multi-Org Rollout

- [ ] Install App in jefahnierocks org
- [ ] Install App in happy-patterns org
- [ ] Install App in litecky-editing org
- [ ] Configure all aliased providers in the-citadel
- [ ] Record platform-ready installations in the Citadel workspace registry and CI wiring

### Phase 3: Policy Enforcement

- [ ] Restrict Classic PAT creation in all orgs
- [ ] Enable Fine-grained PAT approval requirement in all orgs
- [ ] Configure Push Protection for private key patterns
- [ ] Set up quarterly compliance check workflow

### Phase 4: Migration to Infisical (Post-POC 2)

- [ ] Migrate private key from gopass to Infisical
- [ ] Update GitHub Actions and local runbooks to source from Infisical
- [ ] Update local development workflow
- [ ] Decommission gopass entry

---

## Related Documents

- **Policy**: [SEC-005: Machine Identity Management](../sec-005-machine-identity.md)
- **IAM Specification**: [IAM Specification](./iam-specification.md) — AWS/GCP identity architecture
- **Zero Trust**: [SEC-001](../sec-001-zero-trust.md)
- **Least Privilege**: [SEC-003](../sec-003-least-privilege.md)
- **Labeling**: [GOV-010](../gov-010-labeling-standard.md)
- **Implementation**: `the-citadel/terraform/github/apps.tf`

---

## Changelog

### v1.0.0 (2026-03-02)
- Initial specification
- GitHub App as primary machine identity
- Single-app multi-installation model for 5 orgs
- Terraform provider integration pattern
- Private key management via gopass (Infisical planned)
- Fine-grained PAT policy for developer CLI use
- Compliance verification procedures

*"One App, five orgs, zero static credentials. Every API call authenticated, scoped, and auditable."*
