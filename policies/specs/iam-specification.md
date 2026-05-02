# IAM Specification - The Nash Group
**Version**: 1.1.0 (Agentic Era)
**Status**: PARTIALLY HISTORICAL — REWRITE PENDING
**Created**: 2025-11-20
**Updated**: 2025-11-20 (content); 2026-05-02 (status banner)
**Policies**: SEC-001 (Zero Trust), SEC-003 (Least Privilege), SEC-004 (Security Baseline), GOV-010 (Labeling), OPS-010 (Emergency Response), FIN-001 (Cost Control)

---

> **REWRITE PENDING — DO NOT TREAT AS CURRENT TRUTH** (status updated 2026-05-02). This specification is partly strategic and partly historical. The live Citadel machine-identity path is GitHub App + GitHub Actions + OpenTofu with Hetzner Object Storage state, not HCP Terraform. Multi-org structure follows ADR-004 / ADR-007 (independent subsidiary GitHub orgs under three-tier authority), not the AWS/GCP tenant model described below. SEC-005 (Machine Identity) and the Secrets Management Specification v1.3.0 are the authoritative current parent doctrine for machine credentials and secret storage. Treat AWS, GCP, HCP Terraform, and tenant-isolation sections in this document as decision-time context rather than the current operating model. A full ADR-005/ADR-007-era rewrite is open as remaining roadmap work.

## Governing Principles

This specification implements:

| Principle | Implementation |
|-----------|----------------|
| **SEC-001: Zero Trust** | All access federated via Google Workspace; no static credentials |
| **SEC-003: Least Privilege** | Minimal permissions; time-bounded; role-based |
| **GOV-010: Labeling** | All identities tagged with clan, tier, environment |
| **The Human/Machine Creed** | Clear separation of human judgment vs machine automation |

---

## Identity Hierarchy

```
                    ┌─────────────────────────────────────────┐
                    │   GOOGLE WORKSPACE (SSoT)               │
                    │   thenash.group                         │
                    │                                         │
                    │   Guardian: jeffrey@thenash.group       │
                    │   Groups:                               │
                    │   ├── nash-group-owners@                │
                    │   ├── nash-group-watchers@              │
                    │   ├── nash-group-mentors@               │
                    │   └── nash-group-explorers@             │
                    └────────────────┬────────────────────────┘
                                     │
              ┌──────────────────────┴──────────────────────┐
              │                                             │
    ┌─────────▼─────────┐                     ┌─────────────▼─────────────┐
    │  HUMAN IDENTITIES │                     │  MACHINE IDENTITIES       │
    │  (SAML 2.0)       │                     │                           │
    │                   │                     │  ┌─────────────────────┐  │
    │  ► AWS IAM        │                     │  │ AUTOMATION          │  │
    │    Identity Center│                     │  │ (Deterministic)     │  │
    │  ► GCP Cloud      │                     │  │ ► GitHub Actions    │  │
    │    Identity       │                     │  │ ► HCP Terraform     │  │
    │                   │                     │  │ ► CI/CD Pipelines   │  │
    │  Interactive      │                     │  │ Runs scripts        │  │
    │  Console Access   │                     │  └─────────────────────┘  │
    │  Judgment Calls   │                     │                           │
    └───────────────────┘                     │  ┌─────────────────────┐  │
                                              │  │ SYNTHETIC (v1.1.0)  │  │
                                              │  │ (Probabilistic)     │  │
                                              │  │ ► AI Researcher     │  │
                                              │  │ ► AI Specialist     │  │
                                              │  │ Figures out how     │  │
                                              │  │ Permission Bounded  │  │
                                              │  └─────────────────────┘  │
                                              └───────────────────────────┘
```

### Identity Classification

| Type | Behavior | Permissions Model | Use Case |
|------|----------|-------------------|----------|
| **Human** | Interactive | SAML federated, time-bounded sessions | Console access, judgment calls |
| **Automation** | Deterministic | OIDC, specific permissions | CI/CD pipelines, IaC deployment |
| **Synthetic** | Probabilistic | OIDC + Permission Boundary (cage) | AI agents, autonomous research |

---

## 1. AWS IAM Architecture

### 1.1 Organization Structure

```
AWS Organization (nash-group-root)
├── Management Account (nash-management)
│   ├── AWS Organizations
│   ├── IAM Identity Center
│   ├── Billing & Cost Management
│   └── CloudTrail (Organization Trail)
│
├── Security OU
│   ├── Audit Account (nash-audit)
│   │   └── Central logging, GuardDuty aggregation
│   └── Log Archive Account (nash-logs)
│       └── Immutable log storage
│
├── Infrastructure OU
│   └── Shared Services Account (nash-shared)
│       ├── Transit Gateway
│       ├── DNS (Route 53)
│       └── Shared VPCs
│
└── Workloads OU
    ├── Personal Tenant OU
    │   ├── nash-personal-prod
    │   └── nash-personal-staging
    ├── Family Tenant OU
    │   ├── nash-family-prod
    │   └── nash-family-staging
    ├── University Tenant OU
    │   ├── nash-university-prod
    │   └── nash-university-staging
    └── AI Lab Tenant OU
        ├── nash-ai-lab-prod
        └── nash-ai-lab-staging
```

### 1.2 Permission Sets (IAM Identity Center)

**Human Access via SAML Federation**:

| Permission Set | Google Group | Purpose | Permissions |
|----------------|--------------|---------|-------------|
| `NashAdministrator` | `nash-group-owners@` | Full account access | `AdministratorAccess` |
| `NashWatcher` | `nash-group-watchers@` | Security & infrastructure | `SecurityAudit`, `ViewOnlyAccess`, custom infra |
| `NashMentor` | `nash-group-mentors@` | Development & deployment | `PowerUserAccess` (scoped) |
| `NashExplorer` | `nash-group-explorers@` | Read-only exploration | `ViewOnlyAccess` |
| `NashBreakGlass` | `nash-group-owners@` | Emergency only | `AdministratorAccess` + MFA + Justification |

**Permission Set Definitions**:

```hcl
# terraform/aws/iam-identity-center/permission-sets.tf

resource "aws_ssoadmin_permission_set" "nash_administrator" {
  name             = "NashAdministrator"
  instance_arn     = aws_ssoadmin_instance.main.arn
  session_duration = "PT4H"  # 4 hours max
  description      = "Full administrative access for Nash Group owners"

  tags = {
    "nash:clan"        = "watchers"
    "nash:tier"        = "core"
    "nash:policy_id"   = "SEC-003"
    "nash:guardian_role" = "philosopher"
  }
}

resource "aws_ssoadmin_managed_policy_attachment" "nash_administrator" {
  instance_arn       = aws_ssoadmin_instance.main.arn
  permission_set_arn = aws_ssoadmin_permission_set.nash_administrator.arn
  managed_policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_ssoadmin_permission_set" "nash_watcher" {
  name             = "NashWatcher"
  instance_arn     = aws_ssoadmin_instance.main.arn
  session_duration = "PT8H"  # 8 hours for operational work
  description      = "Security and infrastructure oversight"

  tags = {
    "nash:clan"        = "watchers"
    "nash:tier"        = "core"
    "nash:policy_id"   = "SEC-003"
    "nash:guardian_role" = "judge"
  }
}

resource "aws_ssoadmin_permission_set" "nash_mentor" {
  name             = "NashMentor"
  instance_arn     = aws_ssoadmin_instance.main.arn
  session_duration = "PT8H"
  description      = "Development and deployment capabilities"

  tags = {
    "nash:clan"        = "mentors"
    "nash:tier"        = "platform"
    "nash:policy_id"   = "SEC-003"
    "nash:guardian_role" = "architect"
  }
}

resource "aws_ssoadmin_permission_set" "nash_explorer" {
  name             = "NashExplorer"
  instance_arn     = aws_ssoadmin_instance.main.arn
  session_duration = "PT8H"
  description      = "Read-only access for learning and exploration"

  tags = {
    "nash:clan"        = "immortals"
    "nash:tier"        = "application"
    "nash:policy_id"   = "SEC-003"
    "nash:guardian_role" = "explorer"
  }
}
```

### 1.3 Machine Identities (OIDC Federation)

**No IAM Users. No Access Keys. OIDC Only.**

```hcl
# terraform/aws/iam/oidc-providers.tf

# GitHub Actions OIDC Provider
resource "aws_iam_openid_connect_provider" "github_actions" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["ffffffffffffffffffffffffffffffffffffffff"]

  tags = {
    "nash:project_id"  = "github-federation"
    "nash:owner"       = "@the-nash-group/watchers"
    "nash:clan"        = "watchers"
    "nash:tier"        = "core"
    "nash:environment" = "shared"
    "nash:managed_by"  = "terraform"
  }
}

# HCP Terraform OIDC Provider
resource "aws_iam_openid_connect_provider" "hcp_terraform" {
  url             = "https://app.terraform.io"
  client_id_list  = ["aws.workload.identity"]
  thumbprint_list = ["ffffffffffffffffffffffffffffffffffffffff"]

  tags = {
    "nash:project_id"  = "terraform-federation"
    "nash:owner"       = "@the-nash-group/watchers"
    "nash:clan"        = "watchers"
    "nash:tier"        = "core"
    "nash:environment" = "shared"
    "nash:managed_by"  = "terraform"
  }
}
```

### 1.4 IAM Roles for Machine Access

```hcl
# terraform/aws/iam/roles.tf

# GitHub Actions Deployer Role (Per Tenant)
resource "aws_iam_role" "github_actions_deployer" {
  for_each = toset(["personal", "family", "university", "ai-lab"])

  name = "nash-${each.key}-github-deployer"

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
          # Restrict to specific repos and branches
          "token.actions.githubusercontent.com:sub" = [
            "repo:The-Nash-Group/the-citadel:ref:refs/heads/main",
            "repo:The-Nash-Group/the-citadel:ref:refs/heads/feat/*"
          ]
        }
      }
    }]
  })

  # Permission boundary - cannot exceed these permissions
  permissions_boundary = aws_iam_policy.tenant_boundary[each.key].arn

  tags = {
    "nash:project_id"  = "github-federation"
    "nash:owner"       = "@the-nash-group/mentors"
    "nash:clan"        = "mentors"
    "nash:tier"        = "platform"
    "nash:environment" = "shared"
    "nash:tenant"      = each.key
    "nash:managed_by"  = "terraform"
  }
}

# Terraform Cloud Deployer Role (Per Tenant)
resource "aws_iam_role" "terraform_cloud_deployer" {
  for_each = toset(["personal", "family", "university", "ai-lab"])

  name = "nash-${each.key}-terraform-deployer"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.hcp_terraform.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "app.terraform.io:aud" = "aws.workload.identity"
        }
        StringLike = {
          # Restrict to specific workspace
          "app.terraform.io:sub" = "organization:the-nash-group:project:*:workspace:citadel-${each.key}:run_phase:*"
        }
      }
    }]
  })

  permissions_boundary = aws_iam_policy.tenant_boundary[each.key].arn

  tags = {
    "nash:project_id"  = "terraform-federation"
    "nash:owner"       = "@the-nash-group/mentors"
    "nash:clan"        = "mentors"
    "nash:tier"        = "platform"
    "nash:environment" = "shared"
    "nash:tenant"      = each.key
    "nash:managed_by"  = "terraform"
  }
}
```

### 1.5 Agent Sandbox (Synthetic Users) - v1.1.0

**New in v1.1.0 - The Agentic Era**

AI Agents are not traditional service accounts. They are **Synthetic Users** - probabilistic actors that "figure out" how to solve problems rather than running deterministic scripts. This requires a different security model.

**Implementation**: `terraform/aws/iam/agent-sandbox.tf`

**The Cage Architecture**:
```
┌─────────────────────────────────────────────────────────────────┐
│                    PERMISSION BOUNDARY                          │
│                    (The "Cage")                                 │
│                                                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │ Cost Control  │  │ Region Lock   │  │ Anti-Jailbreak│       │
│  │ (Wallet Guard)│  │ (Geofence)    │  │ (IAM Deny)    │       │
│  └───────────────┘  └───────────────┘  └───────────────┘       │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    AGENT ROLE                          │    │
│  │                    (PowerUserAccess)                   │    │
│  │                                                        │    │
│  │  Can: S3, DynamoDB, Lambda, Bedrock, SageMaker, EC2   │    │
│  │  Cannot: Expensive instances, IAM changes, external S3│    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

**Agent Roles**:

| Role | Purpose | Scope | Session Duration |
|------|---------|-------|------------------|
| `nash-ai-lab-agent-researcher` | Autonomous experimentation | ai-lab tenant | 1 hour |
| `nash-ai-lab-agent-specialist` | Domain-specific tasks | ai-lab tenant | 1 hour |

**Permission Boundary Controls**:

| Control | Effect | Policy Reference |
|---------|--------|------------------|
| **Wallet Guard** | Block instances > t3/t4g/m7g.large | FIN-001 |
| **Cost Commitments** | Deny Savings Plans, Reservations | FIN-001 |
| **Expensive Services** | Deny Redshift, EMR, EKS | FIN-001 |
| **Jailbreak Prevention** | Deny all IAM write operations | SEC-003 |
| **Region Lock** | Restrict to designated region + us-east-1 | SEC-004 |
| **Data Exfiltration** | Deny S3 writes outside ai-lab tenant | SEC-004 |
| **Network Exposure** | Deny public security group rules | SEC-004 |

**Allowed EC2 Instance Types**:
```
t3.micro, t3.small, t3.medium, t3.large
t4g.micro, t4g.small, t4g.medium, t4g.large
m7g.medium, m7g.large
```

**Tags for Synthetic Users**:
```hcl
tags = {
  "nash:identity_type" = "synthetic"
  "nash:tenant"        = "ai-lab"
  "nash:guardian_role" = "explorer"
  "nash:policy_id"     = "SEC-003"
}
```

---

### 1.6 Permission Boundaries (Tenant Isolation)

```hcl
# terraform/aws/iam/permission-boundaries.tf

resource "aws_iam_policy" "tenant_boundary" {
  for_each = toset(["personal", "family", "university", "ai-lab"])

  name        = "nash-${each.key}-boundary"
  description = "Permission boundary for ${each.key} tenant - SEC-003 enforcement"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # Allow actions only on resources with matching tenant tag
      {
        Sid    = "AllowTenantResources"
        Effect = "Allow"
        Action = [
          "ec2:*",
          "s3:*",
          "rds:*",
          "lambda:*",
          "dynamodb:*",
          "sqs:*",
          "sns:*",
          "cloudwatch:*",
          "logs:*"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "aws:ResourceTag/nash:tenant" = each.key
          }
        }
      },
      # Allow creating resources with tenant tag
      {
        Sid    = "AllowCreateWithTag"
        Effect = "Allow"
        Action = [
          "ec2:RunInstances",
          "ec2:CreateVolume",
          "s3:CreateBucket",
          "rds:CreateDBInstance",
          "lambda:CreateFunction"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "aws:RequestTag/nash:tenant" = each.key
          }
        }
      },
      # Explicit deny on other tenants
      {
        Sid    = "DenyOtherTenants"
        Effect = "Deny"
        Action = "*"
        Resource = "*"
        Condition = {
          StringNotEqualsIfExists = {
            "aws:ResourceTag/nash:tenant" = each.key
          }
          "Null" = {
            "aws:ResourceTag/nash:tenant" = "false"
          }
        }
      },
      # Deny IAM modifications (privilege escalation prevention)
      {
        Sid    = "DenyIAMModification"
        Effect = "Deny"
        Action = [
          "iam:CreateUser",
          "iam:CreateAccessKey",
          "iam:AttachUserPolicy",
          "iam:AttachRolePolicy",
          "iam:PutRolePolicy",
          "iam:CreateRole",
          "iam:DeleteRolePolicy",
          "iam:UpdateAssumeRolePolicy"
        ]
        Resource = "*"
      },
      # Deny organization-level actions
      {
        Sid    = "DenyOrganizationActions"
        Effect = "Deny"
        Action = [
          "organizations:*",
          "account:*"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    "nash:project_id"  = "iam-boundaries"
    "nash:owner"       = "@the-nash-group/watchers"
    "nash:clan"        = "watchers"
    "nash:tier"        = "core"
    "nash:environment" = "shared"
    "nash:tenant"      = each.key
    "nash:managed_by"  = "terraform"
  }
}
```

### 1.7 Break-Glass Role & Alerting - v1.1.0

**The "Single-Player Empire" Safety Net**

In a single-player empire, you cannot rely on a 24/7 SOC watching logs. This mechanism makes **your phone the SOC**. If anyone (including you) assumes the break-glass role, you receive an SMS/email immediately.

**Implementation Files**:
- Role: `terraform/aws/iam/break-glass.tf`
- Alerting: `terraform/aws/observability/break-glass-alert.tf`

**Role Definition**:
```hcl
# terraform/aws/iam/break-glass.tf

resource "aws_iam_role" "break_glass" {
  name        = "nash-break-glass-emergency"
  description = "Emergency access - requires justification and audit"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        AWS = "arn:aws:iam::${var.management_account_id}:root"
      }
      Action = "sts:AssumeRole"
      Condition = {
        Bool = {
          "aws:MultiFactorAuthPresent" = "true"
        }
        StringEquals = {
          "sts:RoleSessionName" = "emergency-session"
        }
      }
    }]
  })

  max_session_duration = 3600  # 1 hour max

  tags = {
    "nash:project_id"    = "break-glass"
    "nash:owner"         = "@the-nash-group/watchers"
    "nash:clan"          = "watchers"
    "nash:tier"          = "core"
    "nash:environment"   = "shared"
    "nash:purpose"       = "break-glass"
    "nash:guardian_role" = "philosopher"
    "nash:managed_by"    = "terraform"
  }
}

resource "aws_iam_role_policy_attachment" "break_glass_admin" {
  role       = aws_iam_role.break_glass.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}
```

**Break-Glass Alerting Architecture (v1.1.0)**:
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CloudTrail    │───►│   EventBridge   │───►│    SNS Topic    │
│   AssumeRole    │    │   Rule Match    │    │   Security      │
│   Event         │    │   (nash-*)      │    │   Alerts        │
└─────────────────┘    └─────────────────┘    └────────┬────────┘
                                                       │
                                    ┌──────────────────┼──────────────────┐
                                    │                  │                  │
                              ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
                              │    SMS    │      │   Email   │      │  (Future) │
                              │  +1-xxx   │      │  @nash.   │      │  PagerDuty│
                              └───────────┘      └───────────┘      └───────────┘
```

**Alert Types (v1.1.0)**:

| Event | Alert Level | Message |
|-------|-------------|---------|
| Break-Glass Assumed | 🚨 CRITICAL | "CITADEL ALERT: Break-Glass Protocol Activated!" |
| Agent Boundary Hit | ⚠️ WARNING | "AGENT SANDBOX VIOLATION" |
| IAM Changes | 🔐 INFO | "IAM CHANGE DETECTED" |

**Investigation Checklist** (If alert was NOT you):
1. Revoke the session immediately
2. Check CloudTrail for actions taken
3. Initiate incident response protocol

---

## 2. GCP IAM Architecture

### 2.1 Organization Structure

```
GCP Organization (thenash.group)
├── Folders
│   ├── Infrastructure
│   │   └── nash-shared-services (Project)
│   │       ├── Shared VPC Host
│   │       ├── Cloud DNS
│   │       └── Cloud Interconnect
│   │
│   ├── Security
│   │   ├── nash-audit (Project)
│   │   │   └── Centralized logging
│   │   └── nash-security (Project)
│   │       └── Security Command Center
│   │
│   └── Workloads
│       ├── Personal (Folder)
│       │   ├── nash-personal-prod
│       │   └── nash-personal-staging
│       ├── Family (Folder)
│       │   ├── nash-family-prod
│       │   └── nash-family-staging
│       ├── University (Folder)
│       │   ├── nash-university-prod
│       │   └── nash-university-staging
│       └── AI-Lab (Folder)
│           ├── nash-ai-lab-prod
│           └── nash-ai-lab-staging
│
└── IAM Policy Bindings
    ├── Organization Level (Owner only)
    ├── Folder Level (Per-tenant admins)
    └── Project Level (Workload-specific)
```

### 2.2 Custom IAM Roles

```hcl
# terraform/gcp/iam/custom-roles.tf

# Nash Administrator (Organization Level)
resource "google_organization_iam_custom_role" "nash_administrator" {
  role_id     = "nashAdministrator"
  org_id      = var.gcp_organization_id
  title       = "Nash Administrator"
  description = "Full organizational access for Nash Group owners"

  permissions = [
    "resourcemanager.organizations.get",
    "resourcemanager.organizations.getIamPolicy",
    "resourcemanager.organizations.setIamPolicy",
    "resourcemanager.folders.create",
    "resourcemanager.folders.delete",
    "resourcemanager.folders.get",
    "resourcemanager.folders.list",
    "resourcemanager.folders.update",
    "resourcemanager.projects.create",
    "resourcemanager.projects.delete",
    "resourcemanager.projects.get",
    "resourcemanager.projects.list",
    "resourcemanager.projects.update",
    "billing.accounts.get",
    "billing.accounts.list",
    "billing.accounts.getIamPolicy",
    "billing.accounts.setIamPolicy"
  ]
}

# Nash Watcher (Security Auditor)
resource "google_organization_iam_custom_role" "nash_watcher" {
  role_id     = "nashWatcher"
  org_id      = var.gcp_organization_id
  title       = "Nash Watcher"
  description = "Security and infrastructure oversight"

  permissions = [
    "resourcemanager.organizations.get",
    "resourcemanager.folders.get",
    "resourcemanager.folders.list",
    "resourcemanager.projects.get",
    "resourcemanager.projects.list",
    "iam.roles.get",
    "iam.roles.list",
    "iam.serviceAccounts.get",
    "iam.serviceAccounts.list",
    "logging.logEntries.list",
    "logging.logs.list",
    "monitoring.alertPolicies.list",
    "monitoring.dashboards.list",
    "securitycenter.findings.list",
    "securitycenter.sources.list"
  ]
}

# Nash Mentor (Developer/Deployer)
resource "google_project_iam_custom_role" "nash_mentor" {
  for_each = var.tenant_projects

  role_id     = "nashMentor"
  project     = each.value.project_id
  title       = "Nash Mentor"
  description = "Development and deployment capabilities"

  permissions = [
    "compute.instances.create",
    "compute.instances.delete",
    "compute.instances.get",
    "compute.instances.list",
    "compute.instances.start",
    "compute.instances.stop",
    "storage.buckets.create",
    "storage.buckets.delete",
    "storage.buckets.get",
    "storage.buckets.list",
    "storage.objects.create",
    "storage.objects.delete",
    "storage.objects.get",
    "storage.objects.list",
    "cloudfunctions.functions.create",
    "cloudfunctions.functions.delete",
    "cloudfunctions.functions.get",
    "cloudfunctions.functions.list",
    "cloudfunctions.functions.update",
    "run.services.create",
    "run.services.delete",
    "run.services.get",
    "run.services.list",
    "run.services.update"
  ]
}
```

### 2.3 Workload Identity Federation (Machine Access)

```hcl
# terraform/gcp/iam/workload-identity.tf

# Workload Identity Pool for GitHub Actions
resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-actions-pool"
  display_name              = "GitHub Actions Pool"
  description               = "Workload Identity Pool for GitHub Actions OIDC"
  project                   = var.identity_project_id
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Actions OIDC Provider"
  project                            = var.identity_project_id

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  attribute_condition = "assertion.repository_owner == 'The-Nash-Group'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Workload Identity Pool for HCP Terraform
resource "google_iam_workload_identity_pool" "terraform" {
  workload_identity_pool_id = "terraform-cloud-pool"
  display_name              = "Terraform Cloud Pool"
  description               = "Workload Identity Pool for HCP Terraform OIDC"
  project                   = var.identity_project_id
}

resource "google_iam_workload_identity_pool_provider" "terraform" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.terraform.workload_identity_pool_id
  workload_identity_pool_provider_id = "terraform-provider"
  display_name                       = "HCP Terraform OIDC Provider"
  project                            = var.identity_project_id

  attribute_mapping = {
    "google.subject"             = "assertion.sub"
    "attribute.terraform_org"    = "assertion.terraform_organization_name"
    "attribute.terraform_project" = "assertion.terraform_project_name"
    "attribute.terraform_workspace" = "assertion.terraform_workspace_name"
  }

  attribute_condition = "assertion.terraform_organization_name == 'the-nash-group'"

  oidc {
    issuer_uri = "https://app.terraform.io"
  }
}
```

### 2.4 Service Accounts (Per Tenant)

```hcl
# terraform/gcp/iam/service-accounts.tf

resource "google_service_account" "github_deployer" {
  for_each = var.tenant_projects

  account_id   = "nash-${each.key}-github-deployer"
  display_name = "GitHub Actions Deployer - ${each.key}"
  description  = "Service account for GitHub Actions deployment to ${each.key} tenant"
  project      = each.value.project_id
}

resource "google_service_account" "terraform_deployer" {
  for_each = var.tenant_projects

  account_id   = "nash-${each.key}-tf-deployer"
  display_name = "Terraform Cloud Deployer - ${each.key}"
  description  = "Service account for HCP Terraform deployment to ${each.key} tenant"
  project      = each.value.project_id
}

# Workload Identity Binding - GitHub Actions
resource "google_service_account_iam_binding" "github_workload_identity" {
  for_each = var.tenant_projects

  service_account_id = google_service_account.github_deployer[each.key].name
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/The-Nash-Group/the-citadel"
  ]
}

# Workload Identity Binding - Terraform Cloud
resource "google_service_account_iam_binding" "terraform_workload_identity" {
  for_each = var.tenant_projects

  service_account_id = google_service_account.terraform_deployer[each.key].name
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.terraform.name}/attribute.terraform_workspace/citadel-${each.key}"
  ]
}
```

### 2.5 IAM Policy Bindings (Folder Level)

```hcl
# terraform/gcp/iam/folder-bindings.tf

resource "google_folder_iam_binding" "tenant_admin" {
  for_each = var.tenant_folders

  folder = each.value.folder_id
  role   = "roles/resourcemanager.folderAdmin"

  members = [
    "group:nash-group-${each.key}-admins@thenash.group"
  ]
}

resource "google_folder_iam_binding" "tenant_viewer" {
  for_each = var.tenant_folders

  folder = each.value.folder_id
  role   = "roles/resourcemanager.folderViewer"

  members = [
    "group:nash-group-watchers@thenash.group",
    "group:nash-group-mentors@thenash.group"
  ]
}
```

---

## 3. Identity Matrix

### 3.1 Human Identities

| Role | Google Group | AWS Permission Set | GCP Role | Scope |
|------|--------------|-------------------|----------|-------|
| **Owner** | `nash-group-owners@` | `NashAdministrator` | `roles/owner` | Organization |
| **Watcher** | `nash-group-watchers@` | `NashWatcher` | `nashWatcher` (custom) | Organization |
| **Mentor** | `nash-group-mentors@` | `NashMentor` | `nashMentor` (custom) | Per-Tenant |
| **Explorer** | `nash-group-explorers@` | `NashExplorer` | `roles/viewer` | Per-Project |

### 3.2 Automation Identities (Deterministic)

| Service | Identity Type | AWS Role | GCP Service Account | Scope |
|---------|--------------|----------|---------------------|-------|
| **GitHub Actions** | OIDC | `nash-{tenant}-github-deployer` | `nash-{tenant}-github-deployer@` | Per-Tenant |
| **HCP Terraform** | OIDC | `nash-{tenant}-terraform-deployer` | `nash-{tenant}-tf-deployer@` | Per-Tenant |
| **Break-Glass** | Assumed Role | `nash-break-glass-emergency` | `nash-break-glass@` | Cross-Tenant |

### 3.3 Synthetic Identities (Probabilistic) - v1.1.0

| Agent Type | Identity Tag | AWS Role | Boundary | Scope |
|------------|--------------|----------|----------|-------|
| **AI Researcher** | `synthetic` | `nash-ai-lab-agent-researcher` | `nash-agent-sandbox-boundary` | ai-lab tenant |
| **AI Specialist** | `synthetic` | `nash-ai-lab-agent-specialist` | `nash-agent-sandbox-boundary` | ai-lab tenant |

**Synthetic vs Automation**:
```
Automation (CI/CD):                    Synthetic (Agent):
├── Deterministic behavior             ├── Probabilistic behavior
├── Runs pre-written scripts           ├── "Figures out" how to solve problems
├── Specific, narrow permissions       ├── Broad permissions + strict boundary
├── Predictable resource usage         ├── Variable resource usage
└── No cost risk                       └── Cost controls required (FIN-001)
```

### 3.4 Tenant Isolation Matrix

| Tenant | AWS Account(s) | GCP Project(s) | Permission Boundary |
|--------|---------------|----------------|---------------------|
| **Personal** | `nash-personal-prod`, `nash-personal-staging` | `nash-personal-prod`, `nash-personal-staging` | `nash-personal-boundary` |
| **Family** | `nash-family-prod`, `nash-family-staging` | `nash-family-prod`, `nash-family-staging` | `nash-family-boundary` |
| **University** | `nash-university-prod`, `nash-university-staging` | `nash-university-prod`, `nash-university-staging` | `nash-university-boundary` |
| **AI Lab** | `nash-ai-lab-prod`, `nash-ai-lab-staging` | `nash-ai-lab-prod`, `nash-ai-lab-staging` | `nash-ai-lab-boundary` |

---

## 4. Security Controls

### 4.1 Authentication Requirements

| Identity Type | MFA Required | Session Duration | Credential Type |
|---------------|--------------|------------------|-----------------|
| Human (Console) | ✅ Yes | 4-8 hours | SAML via Google |
| Machine (CI/CD) | N/A | 1 hour max | OIDC token |
| Break-Glass | ✅ Yes | 1 hour max | Assumed Role + MFA |

### 4.2 Prohibited Actions

**These actions are DENIED in all permission boundaries**:

```yaml
# AWS
- iam:CreateUser              # No IAM users
- iam:CreateAccessKey         # No static keys
- iam:AttachUserPolicy        # No user policies
- organizations:LeaveOrganization
- organizations:DeleteOrganization
- account:CloseAccount

# GCP
- iam.serviceAccountKeys.create  # No service account keys
- resourcemanager.organizations.delete
- resourcemanager.folders.delete (without approval)
```

### 4.3 Audit Requirements

| Event | AWS Service | GCP Service | Retention |
|-------|-------------|-------------|-----------|
| IAM Changes | CloudTrail | Cloud Audit Logs | 1 year |
| Console Logins | CloudTrail | Cloud Identity Logs | 90 days |
| API Calls | CloudTrail | Cloud Audit Logs | 90 days |
| Resource Changes | CloudTrail + Config | Cloud Asset Inventory | 1 year |

---

## 5. Implementation Checklist

### Phase 1: Foundation
- [ ] AWS Organization created
- [ ] GCP Organization created
- [ ] Google Groups created
- [ ] IAM Identity Center configured
- [ ] Cloud Identity federation configured

### Phase 2: OIDC Federation
- [ ] GitHub Actions OIDC provider (AWS)
- [ ] GitHub Actions Workload Identity (GCP)
- [ ] HCP Terraform OIDC provider (AWS)
- [ ] HCP Terraform Workload Identity (GCP)

### Phase 3: Roles and Boundaries
- [ ] Permission sets created (AWS)
- [ ] Custom roles created (GCP)
- [ ] Permission boundaries deployed (AWS)
- [ ] Folder IAM bindings configured (GCP)

### Phase 4: Service Accounts
- [ ] Deployer service accounts (per tenant)
- [ ] Workload Identity bindings
- [ ] Break-glass role configured

### Phase 5: Agent Sandbox (v1.1.0)
- [ ] Agent sandbox boundary policy deployed
- [ ] AI Researcher role created
- [ ] AI Specialist role created
- [ ] Cost controls verified (instance type restrictions)
- [ ] Region lock verified
- [ ] Data perimeter tested (S3 tenant isolation)

### Phase 6: Security Alerting (v1.1.0)
- [ ] SNS topic created (`nash-security-alerts-critical`)
- [ ] Guardian phone/email subscriptions confirmed
- [ ] EventBridge rule: Break-glass detection
- [ ] EventBridge rule: Agent boundary violation
- [ ] EventBridge rule: IAM changes
- [ ] Test alert delivery (SMS/email)

### Phase 7: Verification
- [ ] Test human login flow (SAML)
- [ ] Test GitHub Actions deployment (OIDC)
- [ ] Test Terraform Cloud deployment (OIDC)
- [ ] Verify tenant isolation
- [ ] Audit logging confirmed
- [ ] Agent sandbox boundary tested
- [ ] Break-glass alerting tested

---

## Related Documents

- [SEC-001: Zero Trust](../the-covenant/policies/sec-001-zero-trust.md)
- [SEC-003: Least Privilege](../the-covenant/policies/sec-003-least-privilege.md)
- [GOV-010: Labeling Standard](../the-covenant/policies/gov-010-labeling-standard.md)
- [FEDERATED-IDENTITY-STRATEGY.md](../FEDERATED-IDENTITY-STRATEGY.md)
- [AUTHENTICATION-STANDARD-2025.md](./AUTHENTICATION-STANDARD-2025.md)

---

**Last Updated**: 2025-11-20
**Version**: 1.1.0 (Agentic Era)

## Changelog

### v1.1.0 (2025-11-20) - Agentic Era
- **Added**: Identity Classification table (Human/Automation/Synthetic)
- **Added**: Section 1.5 - Agent Sandbox (Synthetic Users)
- **Added**: Section 3.3 - Synthetic Identities matrix
- **Added**: Break-Glass Alerting architecture (EventBridge + SNS)
- **Added**: Three alert types: Break-Glass, Agent Boundary, IAM Changes
- **Updated**: Identity Hierarchy diagram showing Automation vs Synthetic split
- **Added**: Cost controls (FIN-001) in agent permission boundaries
- **Added**: Data perimeter controls for tenant isolation

### v1.0.0 (2025-11-20)
- Initial IAM specification
- AWS and GCP organization structure
- OIDC federation for GitHub Actions and HCP Terraform
- Permission boundaries for tenant isolation
- Break-Glass role definition

*"One identity, every platform. Zero static credentials. Complete tenant isolation. Agents in cages."*
