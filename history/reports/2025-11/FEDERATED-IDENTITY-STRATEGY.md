# Federated Identity Strategy for The Nash Group
**Version**: 1.0.0
**Created**: 2025-11-10
**Status**: PROPOSED
**Authority**: Covenant Level (2 Watchers + 2 Mentors)
**Implementation Repository**: the-citadel (Terraform IaC)

> "One identity, everywhere. The Nash Group's Single Source of Truth extends across every cloud, every platform, every API. Google Workspace is our identity foundation. All other systems bow to it through federation."

---

## Executive Summary

This document extends The Nash Group's identity strategy beyond Google Cloud Platform to create a **unified, federated identity system** across all platforms: GCP, AWS, Cloudflare, GitHub, and any future services.

**Core Principle**: Google Workspace (`thenash.group`) is our **Single Source of Truth (SSoT)** for identity. All other platforms will federate to it via SAML 2.0 (human access) or OIDC (machine access).

**Key Outcomes**:
- **One Login**: Guardians authenticate once to Google Workspace, access all platforms via SSO
- **One Identity Source**: Google Groups define roles; platforms map to these groups
- **Zero Credentials**: No platform-specific passwords or long-lived API keys
- **Unified Audit**: All access traced back to Google Workspace identity
- **Governance Aligned**: Federated access follows Stronghold/Citadel/Covenant decision levels

---

## Table of Contents

1. [Organizational Context](#organizational-context)
2. [Federation Architecture](#federation-architecture)
3. [Human Access: SAML 2.0 SSO](#human-access-saml-20-sso)
4. [Machine Access: OIDC Zero-Trust](#machine-access-oidc-zero-trust)
5. [Platform-Specific Implementation](#platform-specific-implementation)
6. [Google Groups as Identity Backbone](#google-groups-as-identity-backbone)
7. [Permission Matrix: Multi-Cloud](#permission-matrix-multi-cloud)
8. [Audit and Compliance](#audit-and-compliance)
9. [Implementation Roadmap](#implementation-roadmap)
10. [Break-Glass Procedures](#break-glass-procedures)
11. [Migration Strategy](#migration-strategy)

---

## Organizational Context

### The Three-Pillar Mapping

```
┌─────────────────────────────────────────────────────────────┐
│                     THE COVENANT                            │
│                  (Level 1: Philosophy)                      │
│                                                             │
│  SSoT for Identity: Google Workspace (thenash.group)       │
│  SSoT for Roles: Google Groups (nash-group-*)             │
│  SSoT for Audit: Google Workspace Admin Logs               │
│                                                             │
│  Principle #9: Zero Trust → No platform-specific passwords │
│  Principle #10: Least Privilege → Minimal cross-platform   │
└─────────────────────────────────────────────────────────────┘
                            ↓ defines
┌─────────────────────────────────────────────────────────────┐
│                   SPECIFICATIONS                            │
│              (Level 2: Standards & Governance)              │
│                                                             │
│  • SAML 2.0 for Human Access (guardian login to consoles)  │
│  • OIDC for Machine Access (CI/CD pipelines)               │
│  • Group Membership = Authorization                         │
│  • No Long-Lived Credentials (keys expire in minutes)      │
└─────────────────────────────────────────────────────────────┘
                            ↓ implements
┌──────────────────────┐           ┌──────────────────────────┐
│   THE CITADEL        │           │      THE NEXUS           │
│ (Level 3a: IaC)      │           │ (Level 3b: Operations)   │
│                      │           │                          │
│ Terraform creates:   │           │ Services authenticate:   │
│ • AWS IAM Identity   │◄──────────┤ • Via Workload Identity  │
│   Center (SAML)      │           │ • Short-lived tokens     │
│ • GCP Workload       │           │ • No stored credentials  │
│   Identity (OIDC)    │           │                          │
│ • Cloudflare Access  │           │ OPA policies enforce:    │
│ • GitHub Teams sync  │           │ • Cross-platform access  │
└──────────────────────┘           └──────────────────────────┘
```

### Current Platform Inventory

| Platform | Current Usage | Authentication Method (Current) | Federation Strategy |
|----------|---------------|--------------------------------|-------------------|
| **Google Cloud** | Primary cloud, IAM strategy defined | Google Workspace native | Native (already SSoT) |
| **GitHub** | Source control, CI/CD | GitHub accounts | SAML SSO + OIDC for Actions |
| **Cloudflare** | DNS, WAF, CDN | Email/password | SAML SSO via Cloudflare Access |
| **AWS** | Future multi-cloud | Not yet configured | SAML via AWS IAM Identity Center |
| **HCP Terraform** | State management | Email/password | SAML SSO (Terraform Cloud) |

---

## Federation Architecture

### The Two-Track Model

The Nash Group employs a **dual federation strategy**:

#### Track 1: Human Access (SAML 2.0)
**For**: Guardians accessing web consoles (AWS Console, Cloudflare Dashboard, GitHub UI)
**Protocol**: SAML 2.0 (Security Assertion Markup Language)
**Flow**:
1. Guardian clicks "AWS Console" in Google Workspace app tray
2. Google Workspace (IdP) generates signed SAML assertion
3. AWS IAM Identity Center (SP) validates assertion
4. AWS grants temporary session based on Google Group membership
5. Guardian has console access without AWS-specific password

#### Track 2: Machine Access (OIDC)
**For**: CI/CD pipelines (GitHub Actions deploying to GCP/AWS/Cloudflare)
**Protocol**: OIDC (OpenID Connect)
**Flow**:
1. GitHub Action workflow starts
2. GitHub Actions OIDC provider issues short-lived token (seconds)
3. GCP Workload Identity Pool/AWS IAM OIDC Provider validates token
4. Cloud platform grants temporary credentials
5. Workflow deploys infrastructure, credentials expire

### Architecture Diagram

```
                    ┌────────────────────────────────┐
                    │   GOOGLE WORKSPACE (SSoT)      │
                    │   thenash.group                │
                    │                                │
                    │  Users:                        │
                    │   - guardian@                  │
                    │   - jeffrey@                   │
                    │                                │
                    │  Groups:                       │
                    │   - nash-group-owners@         │
                    │   - nash-group-watchers@       │
                    │   - nash-group-mentors@        │
                    │   - nash-group-platform@       │
                    └────────────┬───────────────────┘
                                 │
                    ┌────────────┴───────────────────┐
                    │                                │
         ┌──────────▼─────────┐        ┌────────────▼───────────┐
         │  SAML 2.0 (Human)  │        │  OIDC (Machine)        │
         │  Identity Provider │        │  GitHub Actions OIDC   │
         └──────────┬─────────┘        └────────────┬───────────┘
                    │                                │
      ┌─────────────┼────────────────────────────────┼─────────────┐
      │             │                                │             │
┌─────▼──────┐ ┌───▼────────┐ ┌──────────────┐ ┌───▼─────────┐  │
│ AWS IAM    │ │ Cloudflare │ │ GitHub SSO   │ │ GCP WIF     │  │
│ Identity   │ │ Access     │ │ (Enterprise) │ │ Pool        │  │
│ Center     │ │            │ │              │ │             │  │
│            │ │            │ │              │ │             │  │
│ SP (SAML)  │ │ SP (SAML)  │ │ SP (SAML)    │ │ RP (OIDC)   │  │
└────────────┘ └────────────┘ └──────────────┘ └─────────────┘  │
      │             │                │                 │          │
┌─────▼─────────────▼────────────────▼─────────────────▼──────────┘
│            ALL PLATFORMS TRUST GOOGLE WORKSPACE                 │
│       (No platform-specific passwords or long-lived keys)       │
└─────────────────────────────────────────────────────────────────┘
```

**Legend**:
- **IdP (Identity Provider)**: Google Workspace (the authority that says "this is Jeffrey")
- **SP (Service Provider)**: The platform receiving the authentication (AWS, Cloudflare)
- **RP (Relying Party)**: Similar to SP, for OIDC protocol (GCP Workload Identity)

---

## Human Access: SAML 2.0 SSO

### What is SAML 2.0?

SAML (Security Assertion Markup Language) is the enterprise SSO standard. When a Guardian logs into Google Workspace, they can access all federated platforms without re-authenticating.

**Key Concept**: Google Workspace becomes your "corporate badge" that works everywhere.

### SAML 2.0 Components

1. **Identity Provider (IdP)**: Google Workspace
   - Authenticates users (MFA, WebAuthn, etc.)
   - Issues signed SAML assertions (XML documents)
   - Passes group membership as SAML attributes

2. **Service Provider (SP)**: AWS, Cloudflare, GitHub
   - Receives SAML assertion
   - Validates signature (trusts Google's certificate)
   - Grants access based on group membership

3. **SAML Assertion**: Signed XML document containing:
   - **Subject**: Who is this? (`jeffrey@thenash.group`)
   - **Attributes**: What groups? (`nash-group-mentors@thenash.group`)
   - **Conditions**: When valid? (5 minutes from issuance)

### SAML SSO User Experience

**Before Federation** (current state):
```
Jeffrey needs to fix AWS issue
├── Open AWS Console
├── Remember AWS-specific username/password
├── Enter AWS MFA code
└── Access granted
```

**After Federation** (target state):
```
Jeffrey needs to fix AWS issue
├── Already logged into Google Workspace
├── Click "AWS Console" in Google app tray
└── Access granted (Google asserts: "This is Jeffrey, he's a Mentor")
```

### SAML Attribute Mapping

Google Workspace will pass user attributes to service providers:

| SAML Attribute | Example Value | Used By Service Provider |
|----------------|---------------|-------------------------|
| `Subject` | `jeffrey@thenash.group` | User identification |
| `Groups` | `nash-group-mentors@thenash.group` | Role mapping |
| `DisplayName` | `Jeffrey Johnson` | Audit logs |
| `Email` | `jeffrey@thenash.group` | Notifications |

**Example SAML Assertion** (simplified):
```xml
<saml:Assertion>
  <saml:Subject>
    <saml:NameID>jeffrey@thenash.group</saml:NameID>
  </saml:Subject>
  <saml:AttributeStatement>
    <saml:Attribute Name="Groups">
      <saml:AttributeValue>nash-group-mentors@thenash.group</saml:AttributeValue>
      <saml:AttributeValue>nash-group-watchers@thenash.group</saml:AttributeValue>
    </saml:Attribute>
  </saml:AttributeStatement>
</saml:Assertion>
```

---

## Machine Access: OIDC Zero-Trust

### What is OIDC?

OIDC (OpenID Connect) is a modern authentication protocol built on OAuth 2.0. For CI/CD, it provides **keyless authentication**: GitHub Actions can prove its identity without storing credentials.

**Key Concept**: Short-lived tokens (seconds to minutes) replace long-lived API keys (years).

### OIDC Components

1. **OIDC Provider**: GitHub Actions
   - Issues JWT tokens when workflow runs
   - Token contains claims (repo name, branch, etc.)
   - Token expires in minutes

2. **Relying Party**: GCP Workload Identity, AWS IAM OIDC Provider
   - Receives JWT token
   - Validates signature (trusts GitHub's public key)
   - Grants temporary credentials based on claims

3. **JWT Token**: JSON Web Token containing:
   - **Issuer**: `https://token.actions.githubusercontent.com`
   - **Subject**: `repo:The-Nash-Group/the-citadel:ref:refs/heads/main`
   - **Audience**: Cloud platform identifier
   - **Expiration**: 5 minutes from issuance

### OIDC Workflow Experience

**Before OIDC** (anti-pattern):
```yaml
# GitHub Actions workflow (INSECURE)
- name: Deploy to GCP
  env:
    GCP_SERVICE_ACCOUNT_KEY: ${{ secrets.GCP_SA_KEY }} # Long-lived JSON key
  run: |
    echo "$GCP_SERVICE_ACCOUNT_KEY" > key.json
    gcloud auth activate-service-account --key-file=key.json
    terraform apply
```

**After OIDC** (zero-trust):
```yaml
# GitHub Actions workflow (SECURE)
- name: Authenticate to GCP
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: 'projects/123/locations/global/workloadIdentityPools/github/providers/github'
    service_account: 'citadel-deployer@nash-personal-prod.iam'
    # No secrets stored! Token is short-lived and repo-scoped

- name: Deploy Infrastructure
  run: terraform apply
```

### OIDC Token Claims

GitHub Actions OIDC token includes these claims:

| Claim | Example Value | Used For |
|-------|---------------|----------|
| `iss` | `https://token.actions.githubusercontent.com` | Verify token source |
| `sub` | `repo:The-Nash-Group/the-citadel:ref:refs/heads/main` | Repository identity |
| `aud` | `https://iam.googleapis.com/projects/123/...` | Target platform |
| `repository` | `The-Nash-Group/the-citadel` | Authorization condition |
| `ref` | `refs/heads/main` | Branch restriction |
| `exp` | `1699564800` | Token expiration (5 min) |

**Example OIDC Conditional Policy**:
```hcl
# Terraform: Only allow the-citadel repo on main branch
resource "google_service_account_iam_member" "citadel_deployer" {
  service_account_id = google_service_account.citadel_deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/.../attribute.repository/The-Nash-Group/the-citadel"

  condition {
    title      = "Only main branch"
    expression = "assertion.ref == 'refs/heads/main'"
  }
}
```

---

## Platform-Specific Implementation

### Google Cloud Platform (GCP)

**Status**: ✅ Native integration (Google Workspace is native IdP)

**Human Access**:
- Google Workspace users access GCP Console directly
- Google Groups control GCP IAM roles
- No federation needed (same identity domain)

**Machine Access**:
- Workload Identity Federation for GitHub Actions
- OIDC tokens from GitHub → GCP service account impersonation
- Implemented in `GOOGLE-CLOUD-IAM-STRATEGY.md`

### Amazon Web Services (AWS)

**Status**: 🟡 To be implemented (Phase 2)

#### Human Access: AWS IAM Identity Center (SAML)

**Setup Steps**:
1. **In AWS Console** (as break-glass root user):
   - Enable AWS IAM Identity Center (formerly AWS SSO)
   - Note the Identity Center URL (e.g., `https://d-1234567890.awsapps.com/start`)

2. **In Google Workspace Admin Console**:
   - Add SAML app: "AWS IAM Identity Center"
   - Configure SAML attributes:
     - `email` → User email
     - `groups` → Google Group membership
   - Download IdP metadata XML

3. **In AWS IAM Identity Center**:
   - Create "External Identity Provider"
   - Upload Google Workspace IdP metadata
   - Create Permission Sets (e.g., `AWS-Mentor-Admin`, `AWS-Watcher-ReadOnly`)
   - Assign Permission Sets to Google Groups

**Terraform Configuration**:
```hcl
# the-citadel/terraform/aws/sso.tf
resource "aws_ssoadmin_permission_set" "mentor_admin" {
  name             = "AWS-Mentor-Admin"
  instance_arn     = aws_ssoadmin_instance.main.arn
  description      = "Full admin access for Nash Group Mentors"
  session_duration = "PT8H" # 8 hours
}

resource "aws_ssoadmin_account_assignment" "mentor_admin" {
  instance_arn       = aws_ssoadmin_instance.main.arn
  permission_set_arn = aws_ssoadmin_permission_set.mentor_admin.arn
  principal_type     = "GROUP"
  principal_id       = "nash-group-mentors@thenash.group" # From SAML assertion
  target_type        = "AWS_ACCOUNT"
  target_id          = data.aws_caller_identity.current.account_id
}
```

#### Machine Access: AWS IAM OIDC (GitHub Actions)

**Setup Steps**:
1. **Create OIDC Provider in AWS**:
```hcl
# the-citadel/terraform/aws/github-oidc.tf
resource "aws_iam_openid_connect_provider" "github_actions" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"] # GitHub's cert thumbprint
}
```

2. **Create IAM Role with Trust Policy**:
```hcl
resource "aws_iam_role" "citadel_deployer" {
  name = "citadel-deployer"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.github_actions.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:The-Nash-Group/the-citadel:*"
        }
      }
    }]
  })
}
```

3. **GitHub Actions Workflow**:
```yaml
# .github/workflows/deploy-aws.yml
jobs:
  deploy:
    permissions:
      id-token: write # Required for OIDC
      contents: read

    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/citadel-deployer
          aws-region: us-east-1
          # No AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY needed!

      - name: Deploy Infrastructure
        run: terraform apply -auto-approve
```

### Cloudflare

**Status**: 🟡 To be implemented (Phase 2)

#### Human Access: Cloudflare Access (SAML)

**Setup Steps**:
1. **In Cloudflare Zero Trust Dashboard**:
   - Navigate to Settings → Authentication → Login Methods
   - Add "Google Workspace" as SAML provider
   - Note the SSO URL and Entity ID

2. **In Google Workspace Admin Console**:
   - Add SAML app: "Cloudflare"
   - Configure SSO URL from Cloudflare
   - Map SAML attributes (email, groups)

3. **In Cloudflare Access Policies**:
   - Create policy for Cloudflare Dashboard
   - Rule: "Allow if user is in `nash-group-mentors@thenash.group`"

**Terraform Configuration**:
```hcl
# the-citadel/terraform/cloudflare/access.tf
resource "cloudflare_access_identity_provider" "google_workspace" {
  account_id = var.cloudflare_account_id
  name       = "Google Workspace (thenash.group)"
  type       = "google"

  config {
    client_id     = var.google_oauth_client_id
    client_secret = var.google_oauth_client_secret
  }
}

resource "cloudflare_access_policy" "dashboard_mentors" {
  application_id = cloudflare_access_application.dashboard.id
  name           = "Allow Nash Group Mentors"
  precedence     = 1
  decision       = "allow"

  include {
    group = ["nash-group-mentors@thenash.group"]
  }
}
```

#### Machine Access: Cloudflare API Token (Scoped)

**Note**: Cloudflare does not support OIDC federation yet. Use scoped API tokens stored in Google Secret Manager.

```hcl
# the-citadel/terraform/cloudflare/api-tokens.tf
resource "cloudflare_api_token" "citadel_deployer" {
  name = "citadel-deployer (GitHub Actions)"

  policy {
    permission_groups = [
      data.cloudflare_api_token_permission_groups.all.zone["Zone Read"],
      data.cloudflare_api_token_permission_groups.all.zone["DNS Write"],
    ]
    resources = {
      "com.cloudflare.api.account.zone.*" = "*"
    }
  }

  condition {
    request_ip {
      in = ["0.0.0.0/0"] # GitHub Actions IPs (consider restricting)
    }
  }
}

# Store in Google Secret Manager (not GitHub Secrets)
resource "google_secret_manager_secret_version" "cloudflare_token" {
  secret      = google_secret_manager_secret.cloudflare_token.id
  secret_data = cloudflare_api_token.citadel_deployer.value
}
```

**GitHub Actions Workflow**:
```yaml
- name: Authenticate to GCP (to fetch Cloudflare token)
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: '...'
    service_account: 'citadel-deployer@...'

- name: Fetch Cloudflare Token
  id: secrets
  run: |
    TOKEN=$(gcloud secrets versions access latest --secret="cloudflare-api-token")
    echo "::add-mask::$TOKEN"
    echo "CLOUDFLARE_API_TOKEN=$TOKEN" >> $GITHUB_ENV

- name: Deploy to Cloudflare
  env:
    CLOUDFLARE_API_TOKEN: ${{ env.CLOUDFLARE_API_TOKEN }}
  run: terraform apply
```

### GitHub Enterprise (Organization)

**Status**: 🟢 Partial (can be enhanced)

#### Human Access: GitHub SSO (SAML)

**Requirement**: GitHub Enterprise Cloud (paid plan) or GitHub Enterprise Server

**Setup Steps**:
1. **In GitHub Organization Settings**:
   - Navigate to Settings → Security → Authentication
   - Enable SAML SSO
   - Add Google Workspace as IdP

2. **In Google Workspace Admin Console**:
   - Add SAML app: "GitHub Enterprise Cloud"
   - Configure ACS URL: `https://github.com/orgs/The-Nash-Group/saml/consume`
   - Map attributes (email, groups)

3. **In GitHub Organization**:
   - Require SAML SSO for all members
   - Map Google Groups to GitHub Teams:
     - `nash-group-mentors@` → `@The-Nash-Group/mentors`
     - `nash-group-watchers@` → `@The-Nash-Group/watchers`

**Benefits**:
- Single login to GitHub via Google Workspace
- Automatic team membership sync
- Centralized offboarding (remove from Google Group → loses GitHub access)

#### Machine Access: GitHub Actions (Already OIDC)

GitHub Actions already provides OIDC tokens. This is the **OIDC Provider** for GCP/AWS federation (implemented above).

### HCP Terraform (Terraform Cloud)

**Status**: 🟡 To be implemented (Phase 2)

#### Human Access: Terraform Cloud SAML SSO

**Requirement**: Terraform Cloud Business tier

**Setup Steps**:
1. **In HCP Terraform Organization Settings**:
   - Navigate to Settings → SSO
   - Enable SAML 2.0
   - Add Google Workspace as IdP

2. **In Google Workspace Admin Console**:
   - Add SAML app: "Terraform Cloud"
   - Configure ACS URL from HCP Terraform
   - Map attributes

3. **In HCP Terraform**:
   - Map Google Groups to Terraform Teams:
     - `nash-group-mentors@` → `tfc-citadel-admins` (manage state)
     - `nash-group-platform@` → `tfc-nexus-deployers` (read state)

---

## Google Groups as Identity Backbone

### Group Strategy

Google Groups are the **single source of truth** for all authorization decisions across all platforms.

**Design Principle**: Assign permissions to groups, never to individuals.

### Primary Groups (Cross-Platform)

| Google Group | GitHub Team | GCP IAM Role | AWS Permission Set | Cloudflare Access Group |
|--------------|-------------|--------------|-------------------|------------------------|
| `nash-group-owners@` | `@owners` | `roles/owner` | `AWS-Owner-Admin` | `cf-super-admin` |
| `nash-group-watchers@` | `@watchers` | `roles/iam.securityAdmin` | `AWS-Watcher-SecurityAudit` | `cf-security-viewer` |
| `nash-group-mentors@` | `@mentors` | `roles/editor` | `AWS-Mentor-PowerUser` | `cf-zone-admin` |
| `nash-group-platform@` | `@platform-clan` | `nash.cicd-deployer` | `AWS-Platform-Deployer` | `cf-dns-editor` |
| `nash-group-explorers@` | `@all-members` | `nash.explorer` | `AWS-Explorer-ReadOnly` | `cf-viewer` |

### Tenant-Specific Groups

For multi-tenant isolation, create tenant-scoped groups:

| Google Group | Scope | GCP Folder | AWS Account | Purpose |
|--------------|-------|------------|-------------|---------|
| `nash-group-personal-admin@` | Personal | `personal-infra` | `123456789012` | Jeffrey's full admin |
| `nash-group-family-admin@` | Family | `family-infra` | `234567890123` | Family admin |
| `nash-group-family-member@` | Family | `family-infra` (read-only) | `234567890123` | Family viewer |
| `nash-group-university-admin@` | University | `university-infra` | `345678901234` | Academic research |
| `nash-group-ai-lab-admin@` | AI Lab | `ai-lab-infra` | `456789012345` | AI experiments |

### Group Membership Management

**How to Grant Access** (example):
```bash
# Add new Mentor to all platforms
gcloud identity groups memberships add \
  --group-email="nash-group-mentors@thenash.group" \
  --member-email="new-mentor@thenash.group"

# Result: new-mentor@ immediately has:
# - GCP Editor role on projects
# - AWS Mentor-PowerUser permission set
# - Cloudflare zone admin access
# - GitHub @mentors team membership
```

**How to Revoke Access**:
```bash
# Remove departing Guardian from group
gcloud identity groups memberships delete \
  --group-email="nash-group-mentors@thenash.group" \
  --member-email="departing-mentor@thenash.group"

# Result: departing-mentor@ immediately loses access to ALL platforms
```

---

## Permission Matrix: Multi-Cloud

### Organization-Level Permissions

| Group | GCP | AWS | Cloudflare | GitHub |
|-------|-----|-----|-----------|--------|
| **nash-group-owners@** | Organization Owner | Account Root (via SSO) | Super Admin | Organization Owner |
| **nash-group-watchers@** | Security Admin | SecurityAudit Policy | Audit Logs Read | Security Managers |
| **nash-group-mentors@** | Org Role Viewer | PowerUserAccess | Zone Admin | Maintain |
| **nash-group-platform@** | Project Viewer | ViewOnlyAccess | Analytics Read | Write |
| **nash-group-explorers@** | (none at org level) | (none) | (none) | Read |

### Project/Account-Level Permissions

#### Personal Tenant
| Group | GCP Project: nash-personal-prod | AWS Account: personal | Cloudflare Zone: personal.thenash.group |
|-------|--------------------------------|----------------------|---------------------------------------|
| nash-group-personal-admin@ | Editor | AdministratorAccess | Zone Edit |
| nash-group-mentors@ | Viewer | ViewOnlyAccess | Analytics Read |
| citadel-deployer@ (SA) | nash.cicd-deployer | Deployer Role | DNS Edit (via API token) |

#### Family Tenant
| Group | GCP Project: nash-family-prod | AWS Account: family | Cloudflare Zone: family.thenash.group |
|-------|------------------------------|---------------------|-------------------------------------|
| nash-group-family-admin@ | Editor | AdministratorAccess | Zone Edit |
| nash-group-family-member@ | Viewer (prod only) | ReadOnlyAccess | (none) |
| nash-group-watchers@ | Security Admin | SecurityAudit | Audit Logs |

### Service Account / Role Cross-Reference

| Service Account | GCP | AWS | Purpose |
|----------------|-----|-----|---------|
| **citadel-deployer@** | `nash.cicd-deployer` | `arn:aws:iam::*:role/citadel-deployer` | Deploy infrastructure via GitHub Actions |
| **nexus-deployer@** | `roles/run.admin`, `roles/cloudfunctions.admin` | `arn:aws:iam::*:role/nexus-deployer` | Deploy applications |
| **observability-bridge@** | `roles/logging.logWriter`, `roles/monitoring.metricWriter` | `arn:aws:iam::*:role/observability-bridge` | Write telemetry data |

---

## Audit and Compliance

### Unified Audit Trail

All access across all platforms ultimately traces back to Google Workspace:

```
Google Workspace Admin Logs (SSoT)
├── User Authentication Events
│   ├── jeffrey@thenash.group logged in
│   ├── MFA method: WebAuthn (YubiKey)
│   └── Location: Homer, Alaska (verified)
│
├── Group Membership Changes
│   ├── Added jeffrey@ to nash-group-mentors@
│   └── Changed by: guardian@thenash.group
│
└── SAML Assertions Issued
    ├── Issued assertion to AWS IAM Identity Center
    ├── Subject: jeffrey@thenash.group
    ├── Attributes: nash-group-mentors@thenash.group
    └── Valid for: 8 hours

                    ↓ federated to

Platform-Specific Audit Logs
├── GCP Cloud Audit Logs
│   └── jeffrey@thenash.group created compute instance (via Google Group nash-group-mentors@)
│
├── AWS CloudTrail
│   └── AssumedRoleWithSAML: jeffrey@thenash.group → AWS-Mentor-PowerUser
│
├── Cloudflare Audit Logs
│   └── User jeffrey@thenash.group (via Google SSO) modified DNS record
│
└── GitHub Audit Log
    └── Member jeffrey@thenash.group (via SAML) pushed to the-citadel repository
```

### Audit Log Aggregation

**The Nexus: Observability Bridge** will aggregate logs from all platforms:

```hcl
# the-citadel/terraform/nexus/log-sinks.tf
resource "google_logging_project_sink" "audit_to_pubsub" {
  name        = "audit-to-nexus"
  destination = "pubsub.googleapis.com/projects/nash-nexus-prod/topics/audit-logs"

  filter = <<-EOT
    logName:"cloudaudit.googleapis.com" OR
    logName:"activity"
  EOT
}

# AWS CloudTrail → Observability Bridge
resource "aws_cloudtrail" "organization_trail" {
  name                          = "nash-org-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true
  }
}

# Cloudflare Logpush → Observability Bridge
resource "cloudflare_logpush_job" "audit_logs" {
  enabled          = true
  name             = "nash-audit-logs"
  logpull_options  = "fields=ClientIP,ClientRequestHost,ClientRequestMethod,ClientRequestURI,EdgeStartTimestamp,RayID"
  destination_conf = "https://observability-bridge.thenash.group/ingest/cloudflare"
  dataset          = "http_requests"
  frequency        = "high"
}
```

### Cross-Platform Compliance Queries

**Example: "Who accessed production in the last 24 hours?"**

The Observability Bridge can answer this across all platforms:

```sql
-- Query aggregated audit logs
SELECT
  user_identity,
  platform,
  action,
  resource,
  timestamp
FROM aggregated_audit_logs
WHERE
  environment = 'production'
  AND timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;

-- Result:
-- jeffrey@thenash.group | GCP     | compute.instances.create | nash-personal-prod | 2025-11-10 10:30:00
-- jeffrey@thenash.group | AWS     | ec2:RunInstances         | personal-account   | 2025-11-10 11:45:00
-- guardian@thenash.group | Cloudflare | dns.record.update     | thenash.group      | 2025-11-10 14:20:00
```

### Compliance Reports

**Monthly Report: Federated Access Audit**

| Metric | Value | Compliance Status |
|--------|-------|------------------|
| Total active Guardians | 5 | ✅ All have MFA enabled |
| SAML assertions issued | 127 | ✅ All valid, no expired sessions |
| OIDC tokens issued | 342 | ✅ All repo-scoped, no wildcards |
| Privilege escalations | 2 | ✅ Both break-glass, documented |
| Failed auth attempts | 8 | ⚠️ Investigate 3 from unknown IPs |
| Group membership changes | 3 | ✅ All Citadel-level approved |

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2) ✅ COMPLETED
- Google Workspace setup with `guardian@thenash.group`
- Google Groups created matching GitHub teams
- GCP native integration (already SSoT)

### Phase 2: GitHub Federation (Weeks 3-4)

**Week 3: SAML SSO for GitHub**
- [ ] Upgrade to GitHub Enterprise Cloud (if needed)
- [ ] Configure SAML SSO in GitHub Organization
- [ ] Add GitHub SAML app in Google Workspace
- [ ] Test SSO login for all Guardians
- [ ] Enable "Require SAML SSO" for organization
- [ ] Verify automatic team sync

**Week 4: GitHub OIDC for GCP/AWS** (already partially complete)
- [ ] Configure GCP Workload Identity Federation (done in GOOGLE-CLOUD-IAM-STRATEGY.md)
- [ ] Configure AWS IAM OIDC Provider
- [ ] Update GitHub Actions workflows to use OIDC
- [ ] Remove all long-lived credentials from GitHub Secrets
- [ ] Test deployments to GCP and AWS

### Phase 3: AWS Federation (Weeks 5-7)

**Week 5: AWS Account Setup**
- [ ] Create AWS Organization
- [ ] Create AWS Accounts for each tenant (personal, family, university, ai-lab)
- [ ] Enable AWS IAM Identity Center
- [ ] Configure basic Organization Policies

**Week 6: AWS SAML SSO**
- [ ] Add AWS IAM Identity Center as SAML app in Google Workspace
- [ ] Create AWS Permission Sets (Owner-Admin, Watcher-SecurityAudit, Mentor-PowerUser, Platform-Deployer, Explorer-ReadOnly)
- [ ] Assign Permission Sets to Google Groups
- [ ] Test SSO login for all Guardians

**Week 7: AWS OIDC for GitHub Actions**
- [ ] Create AWS IAM OIDC Provider for GitHub Actions
- [ ] Create IAM Roles with repo-scoped trust policies
- [ ] Update GitHub Actions workflows to assume AWS roles
- [ ] Test deployments to AWS from the-citadel repository

### Phase 4: Cloudflare Federation (Weeks 8-9)

**Week 8: Cloudflare Access Setup**
- [ ] Enable Cloudflare Zero Trust
- [ ] Add Google Workspace as SAML IdP
- [ ] Create Cloudflare Access policies for dashboard
- [ ] Test SSO login to Cloudflare Dashboard

**Week 9: Cloudflare API Token Management**
- [ ] Create scoped Cloudflare API tokens for CI/CD
- [ ] Store tokens in Google Secret Manager
- [ ] Update GitHub Actions workflows to fetch tokens via GCP WIF
- [ ] Test DNS/WAF deployments from the-citadel

### Phase 5: HCP Terraform Federation (Week 10)

**Week 10: Terraform Cloud SSO**
- [ ] Upgrade to HCP Terraform Business tier (if needed)
- [ ] Configure SAML SSO for Terraform Cloud
- [ ] Map Google Groups to Terraform Teams
- [ ] Migrate workspaces to SAML-authenticated organization
- [ ] Test state access and plan/apply operations

### Phase 6: Integration and Hardening (Weeks 11-12)

**Week 11: Observability Bridge Integration**
- [ ] Configure audit log export from all platforms to Observability Bridge
- [ ] Create unified audit dashboard
- [ ] Set up cross-platform alerting
- [ ] Test correlation queries (e.g., "show all jeffrey@ actions today")

**Week 12: Break-Glass Testing and Documentation**
- [ ] Test break-glass procedures for each platform
- [ ] Document emergency access protocols
- [ ] Conduct tabletop exercise (simulate lockout)
- [ ] Create runbooks for common federation issues
- [ ] Final security review with nash-group-watchers@

---

## Break-Glass Procedures

### Scenario 1: Locked Out of Google Workspace (SSoT Failure)

**Symptoms**: Cannot log into Google Workspace, blocking access to ALL platforms.

**Break-Glass Steps**:
1. **Use Google Workspace Super Admin Recovery**:
   - Access Google Admin Console via recovery email
   - Use backup codes (stored in gopass: `nash-group/google/workspace-recovery`)
   - Reset MFA if necessary

2. **If Recovery Fails, Use Platform-Specific Break-Glass**:
   - **GCP**: Use emergency service account key (stored offline, encrypted)
   - **AWS**: Use root account credentials (stored in physical safe)
   - **Cloudflare**: Use emergency API token (stored in gopass)
   - **GitHub**: Use personal access token for organization owner (stored in gopass)

3. **Reconciliation** (within 24 hours):
   - Document all actions taken during break-glass
   - Create PR in the-covenant: `break-glass-YYYY-MM-DD.md`
   - Rotate all emergency credentials used
   - Conduct post-mortem with nash-group-watchers@

### Scenario 2: SAML Federation Failure (Google ↔ AWS)

**Symptoms**: Guardians can log into Google Workspace but cannot access AWS Console.

**Break-Glass Steps**:
1. **Verify Google Workspace is Up**:
   - Check Google Workspace Status Dashboard
   - Test login to GCP Console (native integration)

2. **Use AWS IAM User with MFA**:
   - Emergency IAM user: `break-glass-admin` (created via Terraform)
   - Credentials stored in gopass: `nash-group/aws/break-glass-admin`
   - Log into AWS Console with emergency IAM user

3. **Troubleshoot SAML Configuration**:
   - Check AWS IAM Identity Center → External Identity Provider status
   - Verify SAML metadata URL is accessible
   - Check Google Workspace SAML app configuration
   - Review CloudTrail logs for SAML assertion errors

4. **Reconciliation**:
   - Fix SAML configuration
   - Test SSO for all Guardians
   - Delete break-glass IAM user session
   - Document incident in `the-covenant/incidents/`

### Scenario 3: OIDC Token Failure (GitHub Actions → GCP/AWS)

**Symptoms**: GitHub Actions workflows fail with "OIDC token validation error".

**Break-Glass Steps**:
1. **Use Emergency Service Account Key**:
   - Fetch emergency key from Google Secret Manager
   - Create GitHub Secret: `GCP_EMERGENCY_KEY`
   - Update workflow to use key temporarily

2. **Troubleshoot OIDC Configuration**:
   - Verify Workload Identity Pool is active
   - Check OIDC provider configuration (GitHub URL, audience)
   - Review IAM policy conditions (repo name, branch)
   - Test token generation manually: `gh auth token`

3. **Reconciliation**:
   - Fix OIDC configuration
   - Remove emergency key from GitHub Secrets
   - Rotate emergency service account key
   - Document incident and root cause

### Emergency Contact Tree

If federated identity fails, contact in this order:

1. **nash-group-mentors@** (infrastructure experts)
2. **nash-group-watchers@** (security oversight)
3. **Google Workspace Support** (for SSoT issues)
4. **AWS Premium Support** (for IAM Identity Center issues)

---

## Migration Strategy

### Current State Assessment

| Platform | Current Auth Method | Long-Lived Credentials? | Federation Status |
|----------|-------------------|------------------------|------------------|
| GCP | Google Workspace | ❌ No (native integration) | ✅ Complete |
| GitHub | Email/password | ⚠️ Yes (PATs in GitHub Secrets) | 🟡 Partial (OIDC ready, SAML needed) |
| Cloudflare | Email/password | ⚠️ Yes (API tokens in GitHub Secrets) | ❌ Not started |
| AWS | Not configured | N/A | ❌ Not started |
| HCP Terraform | Email/password | ⚠️ Yes (API token in GitHub Secrets) | ❌ Not started |

### Migration Phases

#### Phase A: Inventory (Week 1)
- [ ] Audit all GitHub Secrets containing long-lived credentials
- [ ] List all service account keys in GCP (should be zero)
- [ ] Document all platform-specific passwords in use
- [ ] Identify all integrations requiring credentials

#### Phase B: Parallel Run (Weeks 2-10)
- [ ] Set up federation for each platform (per roadmap)
- [ ] Keep old credentials active during testing
- [ ] Run federated and legacy auth side-by-side
- [ ] Monitor for issues, iterate on configuration

#### Phase C: Cutover (Week 11)
- [ ] Announce cutover date to all Guardians
- [ ] Switch primary authentication to federated
- [ ] Keep legacy credentials as break-glass for 1 week
- [ ] Monitor audit logs for failed auth attempts

#### Phase D: Decommission (Week 12)
- [ ] Delete all platform-specific passwords
- [ ] Revoke all long-lived API tokens
- [ ] Remove credentials from GitHub Secrets
- [ ] Rotate all emergency break-glass credentials
- [ ] Document final state in the-covenant

### Rollback Plan

If federation fails during migration:

1. **Immediate Rollback** (within 1 hour):
   - Re-enable legacy authentication methods
   - Notify all Guardians via Slack/email
   - Use break-glass credentials to restore access

2. **Root Cause Analysis** (within 24 hours):
   - Review audit logs for errors
   - Identify configuration issue
   - Document lessons learned

3. **Retry** (within 1 week):
   - Fix configuration based on RCA
   - Test in isolated tenant (e.g., ai-lab-infra)
   - Attempt cutover again with improved monitoring

---

## Appendix: Glossary

| Term | Definition |
|------|------------|
| **IdP (Identity Provider)** | System that authenticates users (Google Workspace) |
| **SP (Service Provider)** | System that relies on IdP for authentication (AWS, Cloudflare) |
| **RP (Relying Party)** | Similar to SP, for OIDC protocol (GCP Workload Identity) |
| **SAML 2.0** | XML-based protocol for enterprise SSO (human access) |
| **OIDC (OpenID Connect)** | JSON-based protocol for modern SSO (machine access) |
| **SSO (Single Sign-On)** | Login once, access multiple systems |
| **SSoT (Single Source of Truth)** | Authoritative source for identity (Google Workspace) |
| **JWT (JSON Web Token)** | Compact, URL-safe token format used by OIDC |
| **Workload Identity** | GCP's implementation of OIDC federation |
| **IAM Identity Center** | AWS's SAML SSO service (formerly AWS SSO) |
| **Federated Identity** | Identity managed externally but trusted by platform |

---

## Appendix: Reference Links

### Google Workspace SAML Configuration
- [Google Workspace SAML Setup Guide](https://support.google.com/a/answer/6087519)
- [SAML Attribute Mapping](https://support.google.com/a/answer/6194963)

### AWS IAM Identity Center
- [AWS IAM Identity Center Documentation](https://docs.aws.amazon.com/singlesignon/)
- [Enabling External Identity Provider](https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html)

### GCP Workload Identity Federation
- [Workload Identity Federation Overview](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Configuring GitHub Actions OIDC](https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions)

### GitHub SAML SSO
- [GitHub Enterprise SAML SSO](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

### Cloudflare Access
- [Cloudflare Zero Trust Documentation](https://developers.cloudflare.com/cloudflare-one/)
- [Configuring Google Workspace as IdP](https://developers.cloudflare.com/cloudflare-one/identity/idp-integration/google/)

---

**Document Status**: PROPOSED - Awaiting Covenant-level approval (2 Watchers + 2 Mentors)

**Next Steps**:
1. Review by nash-group-watchers@ (security implications)
2. Review by nash-group-mentors@ (implementation feasibility)
3. Create ADR in the-covenant documenting this decision
4. Begin Phase 2 implementation (GitHub Federation)

---

*"From many platforms, one identity. From one identity, zero trust. From zero trust, complete observability. This is The Nash Group way."*

**Last Updated**: 2025-11-10
**Document Owner**: guardian@thenash.group
**Implementation Lead**: TBD (Citadel-level decision)
