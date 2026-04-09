# Google Cloud IAM Strategy for The Nash Group
**Version**: 1.0.0
**Created**: 2025-11-10
**Status**: PROPOSED
**Authority**: Covenant Level (2 Watchers + 2 Mentors)
**Implementation Repository**: the-citadel (Terraform IaC)

> "Identity is the new perimeter. In Google Cloud, we extend The Nash Group's zero-trust philosophy to every resource, service, and API call."

---

## Executive Summary

This document defines The Nash Group's comprehensive Google Cloud Platform (GCP) Identity and Access Management (IAM) strategy. It aligns GCP's IAM primitives with The Nash Group's three-pillar architecture, Five Guardian governance model, and zero-trust security principles.

**Key Outcomes**:
- Google Groups mirror Nash Group governance structure
- GCP IAM roles map to Guardian responsibilities
- Multi-tenant isolation extends to GCP Projects
- Zero-trust OIDC workload identity for CI/CD
- Complete audit trail via Cloud Logging and Cloud Audit Logs
- OPA policies enforce organizational standards

---

## Table of Contents

1. [Organizational Context](#organizational-context)
2. [Google Cloud IAM Foundations](#google-cloud-iam-foundations)
3. [Google Groups Strategy](#google-groups-strategy)
4. [GCP IAM Role Mapping](#gcp-iam-role-mapping)
5. [Multi-Tenant Architecture](#multi-tenant-architecture)
6. [Workload Identity Federation](#workload-identity-federation)
7. [Service Accounts Strategy](#service-accounts-strategy)
8. [Permission Matrix](#permission-matrix)
9. [Audit and Monitoring](#audit-and-monitoring)
10. [Implementation Roadmap](#implementation-roadmap)
11. [Ongoing Management](#ongoing-management)
12. [Break-Glass Procedures](#break-glass-procedures)
13. [Compliance and Governance](#compliance-and-governance)

---

## Organizational Context

### The Three-Pillar Architecture

```
┌─────────────────┐
│  THE COVENANT   │ ← Level 1: Why We Build (Philosophy)
│  (Philosophy)   │   • 16 Core Principles (esp. #9: Zero Trust, #10: Least Privilege)
└─────────────────┘   • GOVERNANCE.md (decision authority)
         ↓             • HUMAN_MANDATE.md (5 Guardian roles)
┌─────────────────┐
│ SPECIFICATIONS  │ ← Level 2: Standards & Governance
│ (.org/specs/)   │   • IAM Standards (WebAuthn, mTLS, OIDC)
└─────────────────┘   • Service Standards (health checks, metrics)
         ↓
┌─────────────────┐
│  THE CITADEL    │ ← Level 3a: How We Build (Infrastructure)
│  (IaC)          │   • Terraform for GCP IAM configuration
└─────────────────┘   • Workload Identity Federation setup
         ↓             • GCP resource provisioning
┌─────────────────┐
│  THE NEXUS      │ ← Level 3b: What We Build (Operations)
│  (Operations)   │   • Services authenticate via Workload Identity
└─────────────────┘   • OPA policies enforce runtime authorization
```

### The Five Guardian Roles

The Nash Group defines five archetypal roles (not job titles, but "hats" Guardians wear):

1. **The Philosopher** - Debates and refines principles
2. **The Architect** - Transforms philosophy into infrastructure code
3. **The Judge** - Ensures changes align with principles
4. **The Gardener** - Maintains system health (dependencies, drift)
5. **The Explorer** - Builds new capabilities within boundaries

### Organizational Teams

| Team | Primary Guardian Hats | Decision Authority | GitHub Team |
|------|----------------------|-------------------|-------------|
| **The Watchers** | Judge (Security), Philosopher (Security), Emergency Responder | Citadel + Covenant decisions | `@the-nash-group/watchers` |
| **The Mentors** | Judge, Architect, Gardener | Citadel decisions | `@the-nash-group/mentors` |
| **Platform Clan** | Explorer, Architect | Stronghold decisions | `@the-nash-group/platform-clan` |
| **All Guardians** | Explorer, Philosopher (Participant) | Propose changes | All org members |

### Decision Authority Matrix

| Decision Type | Scope | Required Approvals | Example |
|---------------|-------|-------------------|---------|
| **Stronghold** | Single repository | 1 Mentor | Add feature to service |
| **Citadel** | Infrastructure | 1 Mentor + 1 Watcher | Create GCP project |
| **Covenant** | Principles/Governance | 2 Watchers + 2 Mentors | Change IAM policy |

---

## Google Cloud IAM Foundations

### GCP IAM Hierarchy

```
Organization (nash-group.example)
├── Folder: personal-infra
│   ├── Project: personal-services-prod
│   └── Project: personal-services-dev
├── Folder: family-infra
│   ├── Project: family-services-prod
│   └── Project: family-services-dev
├── Folder: university-infra
│   └── Project: university-research
└── Folder: ai-lab-infra
    ├── Project: ai-lab-prod
    └── Project: ai-lab-dev
```

### IAM Primitives Mapping

| GCP Primitive | Nash Group Concept | Purpose |
|---------------|-------------------|---------|
| **Organization** | The Nash Group | Root of all resources |
| **Folder** | Tenant Boundary | Isolates personal/family/university/ai-lab |
| **Project** | Service Environment | Isolates prod/dev/staging |
| **Google Group** | Guardian Team | Mirrors GitHub team structure |
| **Service Account** | Service Identity | Represents applications, CI/CD, automation |
| **Workload Identity Pool** | OIDC Federation | Zero-trust authentication for GitHub Actions |
| **IAM Role** | Permission Set | Predefined or custom role bundles |
| **IAM Policy** | Authorization Rule | Who can do what on which resource |

### Core GCP IAM Principles

**Alignment with Nash Group Principles**:

1. **Principle 9: Zero Trust** → No ambient credentials, OIDC federation only
2. **Principle 10: Least Privilege** → Predefined roles preferred, custom roles minimal
3. **Immutable Infrastructure** → IAM policies managed via Terraform
4. **Audit Everything** → Cloud Audit Logs + Export to Observability Bridge

---

## Google Groups Strategy

### Primary Groups (Mirror GitHub Teams)

Google Groups serve as the identity backbone, enabling centralized membership management and cross-platform consistency.

#### 1. nash-group-owners@nashgroup.example
- **Purpose**: Break-glass super admins (emergency access only)
- **GCP Role**: `roles/owner` at Organization level
- **GitHub Equivalent**: `@the-nash-group/break-glass`
- **Members**: Jeffrey (Owner), designated emergency contacts
- **Usage**: Emergency response, disaster recovery, break-glass scenarios
- **Access Review**: Weekly (logged and alerted)

#### 2. nash-group-watchers@nashgroup.example
- **Purpose**: Security oversight, infrastructure guardians
- **GCP Roles**:
  - `roles/securityadmin` (Organization)
  - `roles/iam.securityReviewer` (Organization)
  - `roles/logging.viewer` (Organization)
  - `roles/cloudasset.viewer` (Organization)
- **GitHub Equivalent**: `@the-nash-group/watchers`
- **Members**: Primary Watcher, Secondary Watcher, Security Specialists
- **Usage**: Security audits, IAM changes, incident response
- **Access Review**: Bi-weekly

#### 3. nash-group-mentors@nashgroup.example
- **Purpose**: Technical leadership, infrastructure management
- **GCP Roles**:
  - `roles/editor` (Project-level, per environment)
  - `roles/iam.roleAdmin` (Folder-level)
  - `roles/resourcemanager.folderAdmin` (Folder-level)
- **GitHub Equivalent**: `@the-nash-group/mentors`
- **Members**: Senior engineers, architects, platform engineers
- **Usage**: Infrastructure changes, service deployments, architecture decisions
- **Access Review**: Bi-weekly

#### 4. nash-group-platform@nashgroup.example
- **Purpose**: Service owners, application developers
- **GCP Roles**:
  - `roles/viewer` (Project-level)
  - `roles/compute.instanceAdmin.v1` (Project-level)
  - `roles/container.developer` (Project-level)
  - `roles/cloudfunctions.developer` (Project-level)
- **GitHub Equivalent**: `@the-nash-group/platform-clan`
- **Members**: Service owners, application developers
- **Usage**: Deploy services, manage applications, view logs
- **Access Review**: Monthly

#### 5. nash-group-explorers@nashgroup.example
- **Purpose**: Experimental access to development environments
- **GCP Roles**:
  - `roles/viewer` (Dev projects only)
  - Custom role: `nash.explorer` (limited create/modify in dev)
- **GitHub Equivalent**: All org members
- **Members**: All Nash Group contributors
- **Usage**: Explore, learn, experiment in dev environments
- **Access Review**: Quarterly

### Tenant-Specific Groups

Each tenant (personal, family, university, ai-lab) has dedicated groups for granular isolation:

#### Personal Tenant
- `nash-group-personal-admin@nashgroup.example`
  - Role: `roles/editor` on `personal-*` projects
  - Members: Jeffrey (Owner)

#### Family Tenant
- `nash-group-family-admin@nashgroup.example`
  - Role: `roles/editor` on `family-*` projects
  - Members: Jeffrey, Spouse (Family Admin)
- `nash-group-family-member@nashgroup.example`
  - Role: `roles/viewer` on `family-*` projects
  - Members: Family members, children (read-only)

#### University Tenant
- `nash-group-university-admin@nashgroup.example`
  - Role: `roles/editor` on `university-*` projects
  - Members: Jeffrey, Academic collaborators

#### AI Lab Tenant
- `nash-group-ai-lab-admin@nashgroup.example`
  - Role: `roles/editor` on `ai-lab-*` projects
  - Members: Jeffrey, AI researchers

### Service Groups (Future)

As services mature, create service-specific groups:

- `nash-service-observability-bridge@nashgroup.example`
- `nash-service-devops-mcp@nashgroup.example`
- `nash-service-dashboard@nashgroup.example`

---

## GCP IAM Role Mapping

### Guardian Role to GCP Role Mapping

| Guardian Hat | GCP Role(s) | Scope | Use Case |
|--------------|------------|-------|----------|
| **Super Admin (Break-Glass)** | `roles/owner` | Organization | Emergency full control |
| **Watcher (Security)** | `roles/securityadmin`, `roles/iam.securityReviewer` | Organization | Security audits, IAM oversight |
| **Watcher (Emergency)** | `roles/compute.instanceAdmin.v1`, `roles/container.admin` | All projects | Incident response, restart services |
| **Mentor (Architect)** | `roles/editor`, `roles/iam.roleAdmin` | Folder | Design and implement infrastructure |
| **Mentor (Judge)** | `roles/iam.securityReviewer`, `roles/logging.viewer` | Organization | Review IAM changes, audit logs |
| **Mentor (Gardener)** | `roles/editor`, `roles/monitoring.admin` | Project | Maintain services, update dependencies |
| **Platform Clan (Explorer)** | `roles/compute.instanceAdmin.v1`, `roles/cloudfunctions.developer` | Project (dev) | Deploy services, manage applications |
| **Explorer (All Guardians)** | `roles/viewer`, Custom: `nash.explorer` | Project (dev) | Read-only, limited experimentation |

### Custom Roles

Create minimal custom roles where predefined roles are too permissive:

#### nash.explorer (Development Experimentation)
```yaml
title: "Nash Explorer - Development Access"
description: "Limited experimentation in development environments"
stage: GA
includedPermissions:
  - compute.instances.create
  - compute.instances.start
  - compute.instances.stop
  - cloudfunctions.functions.create
  - cloudfunctions.functions.update
  - storage.buckets.list
  - storage.objects.create
  - storage.objects.get
```

#### nash.cicd-deployer (CI/CD Pipeline)
```yaml
title: "Nash CI/CD Deployer"
description: "Minimal permissions for GitHub Actions deployments"
stage: GA
includedPermissions:
  - compute.instances.create
  - compute.instances.update
  - cloudfunctions.functions.create
  - cloudfunctions.functions.update
  - run.services.create
  - run.services.update
  - iam.serviceAccounts.actAs
```

#### nash.tenant-boundary-enforcer (OPA Policy Engine)
```yaml
title: "Nash Tenant Boundary Enforcer"
description: "Read-only access for OPA policy validation"
stage: GA
includedPermissions:
  - resourcemanager.projects.get
  - resourcemanager.folders.get
  - iam.serviceAccounts.list
  - iam.roles.list
  - compute.instances.list
```

---

## Multi-Tenant Architecture

### Tenant Isolation Strategy

**Principle**: Strong boundaries via Folders, Projects, and IAM policies.

```
Organization: nash-group.example
│
├── Folder: personal-infra (Tenant: personal)
│   ├── IAM Policy: nash-group-personal-admin@nashgroup.example = roles/editor
│   ├── Project: personal-services-prod
│   │   ├── VPC: personal-prod-vpc
│   │   └── IAM Policy: Inherit from folder + service-specific
│   └── Project: personal-services-dev
│       ├── VPC: personal-dev-vpc
│       └── IAM Policy: nash-group-explorers = nash.explorer
│
├── Folder: family-infra (Tenant: family)
│   ├── IAM Policy: nash-group-family-admin@nashgroup.example = roles/editor
│   ├── IAM Policy: nash-group-family-member@nashgroup.example = roles/viewer
│   ├── Project: family-services-prod
│   │   ├── VPC: family-prod-vpc (Shared Services VPC for parental controls)
│   │   └── IAM Policy: Inherit from folder
│   └── Project: family-services-dev
│       └── IAM Policy: nash-group-family-admin = roles/editor
│
├── Folder: university-infra (Tenant: university)
│   ├── IAM Policy: nash-group-university-admin@nashgroup.example = roles/editor
│   ├── Project: university-research
│   │   ├── VPC: university-vpc
│   │   └── IAM Policy: Academic collaborators = roles/viewer
│   └── Data Classification: Academic compliance labels
│
└── Folder: ai-lab-infra (Tenant: ai-lab)
    ├── IAM Policy: nash-group-ai-lab-admin@nashgroup.example = roles/editor
    ├── Project: ai-lab-prod
    │   ├── VPC: ai-lab-prod-vpc
    │   ├── Quotas: GPU quotas enforced
    │   └── IAM Policy: AI agents via service accounts (OPA-enforced)
    └── Project: ai-lab-dev
        └── IAM Policy: nash-group-explorers = nash.explorer
```

### Network Isolation

**VPC Per Tenant**:
- Each tenant has dedicated VPCs (personal-prod-vpc, family-prod-vpc, etc.)
- VPC Peering for controlled cross-tenant communication (e.g., family → personal for shared services)
- VPC Service Controls for data exfiltration prevention

**Shared Services VPC (Family)**:
- Parental control proxy
- Content filtering gateway
- Activity monitoring service

### Resource Tagging and Labels

**Required Labels on All Resources**:
```yaml
tenant: personal | family | university | ai-lab
environment: prod | dev | staging
owner: guardian-email
governance-level: stronghold | citadel | covenant
cost-center: budget-allocation-id
compliance: academic | family-safety | ai-governance
```

---

## Workload Identity Federation

### Zero-Trust CI/CD Authentication

**Principle**: No long-lived service account keys. GitHub Actions authenticates via OIDC tokens.

#### Workload Identity Pool Configuration

```hcl
# the-citadel/terraform/gcp/workload-identity.tf

resource "google_iam_workload_identity_pool" "github_actions" {
  workload_identity_pool_id = "github-actions-pool"
  display_name              = "GitHub Actions OIDC Pool"
  description               = "Workload Identity Pool for GitHub Actions CI/CD"
  disabled                  = false
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_actions.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-oidc-provider"
  display_name                       = "GitHub OIDC Provider"
  description                        = "OIDC provider for GitHub Actions"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}
```

#### Service Account Bindings

```hcl
# Service Account for the-citadel (Infrastructure Deployment)
resource "google_service_account" "citadel_deployer" {
  account_id   = "citadel-deployer"
  display_name = "The Citadel Infrastructure Deployer"
  description  = "Service account for Terraform infrastructure deployments"
}

# Allow GitHub Actions from the-citadel repo to impersonate this SA
resource "google_service_account_iam_member" "citadel_workload_identity" {
  service_account_id = google_service_account.citadel_deployer.name
  role               = "roles/iam.workloadIdentityUser"

  member = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_actions.name}/attribute.repository/the-nash-group/the-citadel"
}

# Grant necessary permissions to the service account
resource "google_project_iam_member" "citadel_deployer_permissions" {
  for_each = toset([
    "roles/compute.admin",
    "roles/container.admin",
    "roles/iam.serviceAccountAdmin",
    "roles/resourcemanager.projectIamAdmin",
  ])

  project = var.gcp_project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.citadel_deployer.email}"
}
```

#### GitHub Actions Workflow Example

```yaml
# .github/workflows/deploy-to-gcp.yml
name: Deploy to GCP

on:
  push:
    branches: [main]

permissions:
  id-token: write  # Required for OIDC token
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-oidc-provider'
          service_account: 'citadel-deployer@nash-group.iam.gserviceaccount.com'

      - name: Deploy with Terraform
        run: |
          terraform init
          terraform apply -auto-approve
```

### Repository-Specific Service Accounts

Each pillar repository gets dedicated service accounts:

| Repository | Service Account | Purpose | GCP Roles |
|------------|----------------|---------|-----------|
| **the-citadel** | `citadel-deployer@` | Infrastructure as Code | `roles/editor`, `roles/iam.serviceAccountAdmin` |
| **the-nexus** | `nexus-deployer@` | Service deployments | `nash.cicd-deployer` |
| **the-shield** | `shield-deployer@` | IAM management | `roles/iam.securityAdmin`, `roles/iam.serviceAccountAdmin` |

---

## Service Accounts Strategy

### Human vs. Service Identity

**Nash Group Identity Types** → **GCP Service Accounts**:

| Nash Identity Type | GCP Implementation | Authentication | Example |
|-------------------|-------------------|----------------|---------|
| **Human: Owner** | Google Group membership | WebAuthn + TOTP | jeffrey@nashgroup.example |
| **Human: Family Admin** | Google Group membership | WebAuthn + TOTP | spouse@nashgroup.example |
| **AI Agent: Orchestrator** | Service Account + OPA policy | API Key + JWT | `ai-research-coordinator@nash-group.iam.gserviceaccount.com` |
| **Service: Nexus App** | Service Account + Workload Identity | mTLS cert (15 min) | `nexus-observability-bridge@nash-group.iam.gserviceaccount.com` |
| **CI/CD: GitHub Actions** | Workload Identity Federation | OIDC token (short-lived) | `citadel-deployer@nash-group.iam.gserviceaccount.com` |

### Service Account Naming Convention

**Format**: `{component}-{purpose}@{project}.iam.gserviceaccount.com`

Examples:
- `citadel-deployer@nash-personal-prod.iam.gserviceaccount.com`
- `nexus-bridge@nash-personal-prod.iam.gserviceaccount.com`
- `ai-research-coordinator@nash-ai-lab-prod.iam.gserviceaccount.com`

### Service Account Lifecycle

**Creation**: Via Terraform in the-citadel
**Rotation**: Keys rotated automatically every 90 days (enforced via OPA policy)
**Decommissioning**: Terraform destroy, keys revoked, audit log retention

### Key Management

**Principle**: Avoid service account keys. Use Workload Identity where possible.

**When Keys Are Required** (legacy integrations):
1. Store keys in Google Secret Manager (not git, not local)
2. Rotate every 90 days (automated via Cloud Scheduler + Cloud Functions)
3. Audit key usage via Cloud Audit Logs
4. Alert on key creation/download events

---

## Permission Matrix

### Organization-Level Permissions

| Group | Role | Justification | Principle |
|-------|------|--------------|-----------|
| nash-group-owners@ | `roles/owner` | Break-glass super admin | Emergency response only |
| nash-group-watchers@ | `roles/securityadmin` | Security oversight | Covenant Principle 9: Zero Trust |
| nash-group-watchers@ | `roles/iam.securityReviewer` | IAM audit capability | Covenant Principle 10: Least Privilege |
| nash-group-watchers@ | `roles/logging.viewer` | Audit log access | Observability for all actions |
| nash-group-mentors@ | `roles/iam.organizationRoleViewer` | Understand role structure | Transparency for architects |

### Folder-Level Permissions (Per Tenant)

#### Personal Tenant (personal-infra folder)
| Group | Role | Scope | Justification |
|-------|------|-------|--------------|
| nash-group-personal-admin@ | `roles/editor` | All projects in folder | Full control for owner |
| nash-group-mentors@ | `roles/viewer` | All projects | Infrastructure visibility |
| nash-group-watchers@ | `roles/viewer` | All projects | Security oversight |

#### Family Tenant (family-infra folder)
| Group | Role | Scope | Justification |
|-------|------|-------|--------------|
| nash-group-family-admin@ | `roles/editor` | All projects in folder | Family admin control |
| nash-group-family-member@ | `roles/viewer` | Production project only | Read-only access to shared resources |
| nash-group-watchers@ | `roles/securityadmin` | All projects | Enforce parental controls |

#### University Tenant (university-infra folder)
| Group | Role | Scope | Justification |
|-------|------|-------|--------------|
| nash-group-university-admin@ | `roles/editor` | All projects | Academic research control |
| nash-group-mentors@ | `roles/viewer` | All projects | Support research infrastructure |

#### AI Lab Tenant (ai-lab-infra folder)
| Group | Role | Scope | Justification |
|-------|------|-------|--------------|
| nash-group-ai-lab-admin@ | `roles/editor` | All projects | AI experimentation control |
| AI Agent Service Accounts | Custom: `nash.ai-agent-runner` | Production project | Limited AI agent execution |
| nash-group-explorers@ | `roles/viewer` | Development project | Learn AI/ML workflows |

### Project-Level Permissions (Example: personal-services-prod)

| Identity | Role | Justification | Principle |
|----------|------|--------------|-----------|
| nash-group-personal-admin@ | `roles/editor` | Full project control | Owner authority |
| citadel-deployer@...iam.gserviceaccount.com | `nash.cicd-deployer` | Deploy infrastructure | Least privilege for CI/CD |
| nexus-bridge@...iam.gserviceaccount.com | `roles/monitoring.metricWriter`, `roles/logging.logWriter` | Write metrics and logs | Service observability |
| nash-group-mentors@ | `roles/viewer` | Read infrastructure state | Debugging and support |
| nash-group-watchers@ | `roles/viewer` | Security audits | Continuous compliance |

---

## Audit and Monitoring

### Cloud Audit Logs Configuration

**Enable All Audit Log Types**:
1. **Admin Activity Logs** (always on, no config needed)
   - IAM policy changes
   - Service account key creation
   - Resource creation/deletion

2. **Data Access Logs** (requires explicit enablement)
   - Read operations on resources
   - List operations on resources
   - **Exclude**: High-volume low-risk reads (e.g., GCS object reads for logs)

3. **System Event Logs** (always on)
   - Automated GCP system actions
   - Maintenance events

**Terraform Configuration**:
```hcl
# Enable Data Access logs for IAM and Compute Engine
resource "google_project_iam_audit_config" "audit_config" {
  project = var.gcp_project_id
  service = "allServices"

  audit_log_config {
    log_type = "ADMIN_READ"
  }

  audit_log_config {
    log_type = "DATA_READ"
  }

  audit_log_config {
    log_type = "DATA_WRITE"
  }
}
```

### Log Export to Observability Bridge

**Export Cloud Audit Logs to the-nexus Observability Bridge**:

```hcl
# Create log sink
resource "google_logging_project_sink" "observability_bridge_sink" {
  name        = "observability-bridge-audit-logs"
  destination = "pubsub.googleapis.com/projects/${var.gcp_project_id}/topics/audit-logs"

  filter = <<-EOT
    resource.type="audited_resource"
    AND (
      protoPayload.methodName="google.iam.admin.v1.CreateServiceAccountKey"
      OR protoPayload.methodName="SetIamPolicy"
      OR protoPayload.authorizationInfo.granted=true
    )
  EOT

  unique_writer_identity = true
}

# Grant sink permission to publish to Pub/Sub
resource "google_pubsub_topic_iam_member" "sink_publisher" {
  topic  = google_pubsub_topic.audit_logs.name
  role   = "roles/pubsub.publisher"
  member = google_logging_project_sink.observability_bridge_sink.writer_identity
}

# Observability Bridge subscribes to this topic
resource "google_pubsub_subscription" "observability_bridge_sub" {
  name  = "observability-bridge-audit-subscription"
  topic = google_pubsub_topic.audit_logs.name

  push_config {
    push_endpoint = "https://observability-bridge.thenash.group/ingest/gcp-audit-logs"

    oidc_token {
      service_account_email = google_service_account.observability_bridge.email
    }
  }
}
```

### Alerting Rules

**Immediate Alerts** (sent to nash-group-watchers@):

1. **Break-Glass Access Used**
   - Condition: `nash-group-owners@` member performs ANY action
   - Severity: CRITICAL
   - Response: Immediate investigation, log review

2. **IAM Policy Change**
   - Condition: `SetIamPolicy` method called on Organization/Folder/Project
   - Severity: HIGH
   - Response: Review change in audit logs, verify authorization

3. **Service Account Key Created**
   - Condition: `CreateServiceAccountKey` method called
   - Severity: MEDIUM
   - Response: Verify requester, check if Workload Identity alternative exists

4. **Privilege Escalation Attempt**
   - Condition: User granted `roles/owner` or `roles/editor` at Organization level
   - Severity: CRITICAL
   - Response: Immediate revocation, incident investigation

5. **Tenant Boundary Violation**
   - Condition: Service account from tenant A accesses resources in tenant B
   - Severity: HIGH
   - Response: OPA policy review, access revocation

**Terraform Alerting Policy**:
```hcl
resource "google_monitoring_alert_policy" "iam_policy_change" {
  display_name = "IAM Policy Change Alert"
  combiner     = "OR"

  conditions {
    display_name = "IAM policy modification detected"

    condition_matched_log {
      filter = <<-EOT
        resource.type="audited_resource"
        AND protoPayload.methodName="SetIamPolicy"
      EOT
    }
  }

  notification_channels = [google_monitoring_notification_channel.watchers_email.id]

  alert_strategy {
    auto_close = "1800s"  # 30 minutes
  }
}
```

### Compliance Reports

**Weekly Reports** (automated via Cloud Scheduler + Cloud Functions):
1. **Access Review**: Who has access to what resources
2. **Unused Service Accounts**: Accounts with no activity in 30 days
3. **Over-Privileged Accounts**: Accounts with `roles/owner` or `roles/editor`
4. **Key Age Report**: Service account keys older than 60 days

**Monthly Reports**:
1. **Policy Violation Summary**: Attempted unauthorized access
2. **Tenant Boundary Audit**: Cross-tenant access attempts
3. **AI Agent Activity**: Resource usage by AI agents
4. **Cost by Tenant**: GCP spending per tenant

**Quarterly Reports**:
1. **Complete Access Audit**: Full IAM policy review
2. **Compliance Validation**: SOC 2, GDPR, NIST 800-63 alignment
3. **Security Posture Assessment**: Vulnerabilities, misconfigurations

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)

**Goal**: Establish GCP Organization and foundational IAM structure

**Tasks**:
1. **Create GCP Organization** (nash-group.example)
   - Domain verification
   - Organization resource creation
   - Billing account setup

2. **Create Google Groups**
   - nash-group-owners@
   - nash-group-watchers@
   - nash-group-mentors@
   - nash-group-platform@
   - nash-group-explorers@

3. **Assign Organizational Roles**
   - Bind nash-group-owners@ to `roles/owner`
   - Bind nash-group-watchers@ to `roles/securityadmin`, `roles/iam.securityReviewer`
   - Bind nash-group-mentors@ to `roles/iam.organizationRoleViewer`

4. **Enable Audit Logging**
   - Enable Admin Activity Logs
   - Enable Data Access Logs (IAM, Compute)
   - Configure log retention (1 year minimum)

5. **Terraform Setup**
   - Create `the-citadel/terraform/gcp/` directory
   - Define GCP provider configuration
   - Implement IAM resources in Terraform
   - Store state in HCP Terraform workspace: `nash-gcp-production`

**Deliverables**:
- GCP Organization operational
- Google Groups synced with GitHub teams
- Audit logging enabled
- Terraform IaC for GCP IAM

**Decision Authority**: Citadel (1 Mentor + 1 Watcher approval)

---

### Phase 2: Multi-Tenant Structure (Weeks 3-4)

**Goal**: Create folder and project hierarchy for tenant isolation

**Tasks**:
1. **Create Folders**
   - personal-infra
   - family-infra
   - university-infra
   - ai-lab-infra

2. **Create Initial Projects**
   - personal-services-prod
   - personal-services-dev
   - family-services-prod
   - ai-lab-dev

3. **Assign Folder-Level IAM Policies**
   - personal-infra → nash-group-personal-admin@
   - family-infra → nash-group-family-admin@, nash-group-family-member@
   - university-infra → nash-group-university-admin@
   - ai-lab-infra → nash-group-ai-lab-admin@

4. **Configure Network Isolation**
   - Create VPCs per tenant
   - Configure VPC Service Controls
   - Set up VPC peering (family ↔ personal for shared services)

5. **Apply Resource Labels**
   - Implement mandatory label schema (tenant, environment, owner, governance-level)
   - Create OPA policy to enforce label presence

**Deliverables**:
- Multi-tenant folder structure
- Projects with network isolation
- IAM policies enforcing tenant boundaries
- Resource labeling standards

**Decision Authority**: Citadel (1 Mentor + 1 Watcher approval)

---

### Phase 3: Workload Identity Federation (Weeks 5-6)

**Goal**: Zero-trust authentication for CI/CD pipelines

**Tasks**:
1. **Create Workload Identity Pool**
   - Pool ID: `github-actions-pool`
   - Provider: GitHub OIDC (`https://token.actions.githubusercontent.com`)

2. **Create Service Accounts**
   - citadel-deployer@ (Infrastructure as Code)
   - nexus-deployer@ (Service deployments)
   - shield-deployer@ (IAM management)

3. **Configure IAM Bindings**
   - Allow GitHub Actions from `the-citadel` repo to impersonate `citadel-deployer@`
   - Allow GitHub Actions from `the-nexus` to impersonate `nexus-deployer@`
   - Allow GitHub Actions from `the-shield` to impersonate `shield-deployer@`

4. **Grant Service Account Permissions**
   - citadel-deployer@ → `roles/editor`, `roles/iam.serviceAccountAdmin`
   - nexus-deployer@ → Custom role: `nash.cicd-deployer`
   - shield-deployer@ → `roles/iam.securityAdmin`

5. **Update GitHub Actions Workflows**
   - Replace long-lived keys with OIDC authentication
   - Test deployments from CI/CD
   - Revoke all existing service account keys

**Deliverables**:
- Workload Identity Pool operational
- CI/CD pipelines using OIDC tokens
- Zero long-lived service account keys
- GitHub Actions workflows updated

**Decision Authority**: Citadel (1 Mentor + 1 Watcher approval)

---

### Phase 4: Monitoring and Alerting (Weeks 7-8)

**Goal**: Complete visibility and alerting for IAM events

**Tasks**:
1. **Configure Log Sinks**
   - Export Cloud Audit Logs to Pub/Sub
   - Configure subscription for Observability Bridge
   - Test log ingestion pipeline

2. **Create Alerting Policies**
   - Break-glass access alert
   - IAM policy change alert
   - Service account key creation alert
   - Privilege escalation attempt alert
   - Tenant boundary violation alert

3. **Implement Compliance Reports**
   - Weekly: Access review, unused accounts, over-privileged accounts, key age
   - Monthly: Policy violations, tenant boundary audit, AI agent activity, cost by tenant
   - Quarterly: Complete access audit, compliance validation, security posture

4. **Integrate with Observability Bridge**
   - Stream GCP audit logs to Bridge
   - Correlate GCP events with GitHub/Cloudflare events
   - Build unified dashboard in the-nexus

5. **Test Incident Response**
   - Simulate break-glass event
   - Simulate IAM policy change
   - Verify alerts are sent
   - Validate runbook execution

**Deliverables**:
- Audit logs exported to Observability Bridge
- Alerting policies operational
- Compliance reports automated
- Incident response tested

**Decision Authority**: Citadel (1 Mentor + 1 Watcher approval)

---

### Phase 5: OPA Policy Enforcement (Weeks 9-10)

**Goal**: Runtime policy enforcement for authorization and tenant boundaries

**Tasks**:
1. **Deploy OPA to GCP**
   - Deploy OPA as Cloud Run service
   - Configure OPA to fetch policies from `.org/iam/policies/`
   - Secure OPA endpoint with IAM

2. **Implement OPA Policies**
   - `tenant-isolation.rego` (enforce tenant boundaries)
   - `ai-agent-quotas.rego` (enforce AI agent resource limits)
   - `family-safety.rego` (parental control policies)
   - `service-account-rotation.rego` (enforce 90-day key rotation)

3. **Integrate OPA with GCP**
   - Cloud Functions to validate actions before execution
   - Cloud Scheduler to run periodic compliance checks
   - Deny actions that violate OPA policies

4. **Test OPA Policies**
   - Test tenant boundary enforcement (family → personal access denied)
   - Test AI agent quota limits
   - Test service account key age policy
   - Test policy override scenarios

5. **Document OPA Integration**
   - ADR for OPA architecture
   - Runbooks for policy updates
   - Troubleshooting guide

**Deliverables**:
- OPA deployed and operational
- Policies enforcing tenant boundaries
- AI agent quotas enforced
- Policy testing complete

**Decision Authority**: Citadel (1 Mentor + 1 Watcher approval)

---

### Phase 6: Integration and Hardening (Weeks 11-12)

**Goal**: Final integration, security hardening, and documentation

**Tasks**:
1. **Harden Service Accounts**
   - Review all service account permissions (principle of least privilege)
   - Remove unused service accounts
   - Audit key age (rotate keys > 60 days old)
   - Enforce OPA policy for key rotation

2. **Implement VPC Service Controls**
   - Create service perimeters for each tenant
   - Restrict data exfiltration
   - Allow controlled cross-tenant communication

3. **Review IAM Policies**
   - Audit organization-level bindings (remove unnecessary `roles/owner`)
   - Audit folder-level bindings (ensure least privilege)
   - Audit project-level bindings (remove over-privileged accounts)

4. **Create Runbooks**
   - Break-glass access procedures
   - Incident response for IAM compromise
   - Service account key rotation
   - Adding/removing Google Group members
   - Onboarding new Guardians

5. **Document Architecture**
   - ADR-XXX: GCP IAM Strategy
   - ADR-XXX: Workload Identity Federation
   - ADR-XXX: Multi-Tenant Isolation
   - Update `ORGANIZATION-SPEC.md` with GCP IAM standards
   - Update `the-citadel/CLAUDE.md` with GCP workflows

6. **Conduct Security Review**
   - External audit of IAM policies
   - Penetration testing of tenant boundaries
   - Review compliance with SOC 2, GDPR, NIST 800-63

**Deliverables**:
- Hardened service accounts
- VPC Service Controls operational
- IAM policies reviewed and optimized
- Runbooks complete
- Architecture documentation updated
- Security review completed

**Decision Authority**: Covenant (2 Watchers + 2 Mentors approval for governance updates)

---

## Ongoing Management

### Daily Operations

**Automated Tasks**:
- Drift detection: Compare Terraform state with actual GCP IAM policies
- Log export: Stream audit logs to Observability Bridge
- Alerting: Monitor for IAM policy changes, privilege escalation

**Manual Tasks** (Watchers):
- Review overnight alerts
- Investigate IAM policy changes
- Approve/deny pending access requests

---

### Weekly Tasks

**Automated Reports**:
- Access review (who has access to what)
- Unused service accounts (no activity in 7+ days)
- Over-privileged accounts (`roles/owner`, `roles/editor`)
- Service account key age (keys > 60 days old)

**Manual Tasks** (Watchers + Mentors):
- Review access report, revoke unnecessary permissions
- Review break-glass access logs (should be empty)
- Plan upcoming IAM changes

---

### Monthly Tasks

**Automated Reports**:
- Policy violation summary (unauthorized access attempts)
- Tenant boundary audit (cross-tenant access attempts)
- AI agent activity (resource usage, quota compliance)
- Cost by tenant (GCP spending per tenant)

**Manual Tasks** (Watchers + Mentors):
- Conduct access review meeting
- Update IAM policies based on new services
- Review AI agent quotas and adjust
- Cost optimization analysis

---

### Quarterly Tasks

**Automated Reports**:
- Complete access audit (all IAM bindings)
- Compliance validation (SOC 2, GDPR, NIST 800-63)
- Security posture assessment (misconfigurations, vulnerabilities)

**Manual Tasks** (Full Council):
- Governance review (do roles and permissions align with reality?)
- Update Google Group memberships
- Review and update custom IAM roles
- Security audit with external auditor
- Update IAM policies for lessons learned

---

### Service Account Key Rotation

**Automated** (Cloud Scheduler + Cloud Function):
- Trigger: Weekly check for keys > 60 days old
- Action: Create new key, update Secret Manager, revoke old key
- Notification: Alert owner of key rotation

**Manual** (when automated rotation fails):
1. Generate new key: `gcloud iam service-accounts keys create new-key.json --iam-account=SERVICE_ACCOUNT_EMAIL`
2. Update Secret Manager: `gcloud secrets versions add SECRET_NAME --data-file=new-key.json`
3. Test new key: Deploy and verify service functionality
4. Revoke old key: `gcloud iam service-accounts keys delete OLD_KEY_ID --iam-account=SERVICE_ACCOUNT_EMAIL`
5. Log rotation: Document in audit log

---

### Adding New Guardians

**Process**:
1. **Proposal**: Guardian proposes new member (via GitHub issue)
2. **Debate**: 72-hour minimum discussion period
3. **Approval**: Requires 1 Watcher + 1 Mentor
4. **Onboarding**:
   - Add to Google Group (nash-group-mentors@ or nash-group-platform@)
   - Add to GitHub Team (@the-nash-group/mentors or @the-nash-group/platform-clan)
   - Grant GCP access via group membership (automatic)
   - Conduct IAM training session
   - Assign mentor for first 30 days

**Governance**: Citadel Level (1 Mentor + 1 Watcher approval)

---

### Removing Guardians

**Process**:
1. **Initiation**: Guardian departure or access revocation required
2. **Immediate Revocation**:
   - Remove from Google Group (IAM access revoked automatically)
   - Remove from GitHub Team
   - Revoke any personally-assigned IAM bindings
   - Rotate any service account keys they had access to
3. **Audit**:
   - Review all actions taken by departing Guardian (last 90 days)
   - Verify no unauthorized changes
   - Document findings
4. **Knowledge Transfer**:
   - Transfer ownership of services/projects
   - Update CODEOWNERS files
   - Update documentation

**Governance**: Citadel Level (1 Mentor + 1 Watcher approval)

---

## Break-Glass Procedures

### When to Use Break-Glass

**Legitimate Use Cases**:
1. **Automated system failure**: Terraform state corrupted, CI/CD broken
2. **Security incident**: Active attack, compromise detected
3. **Service outage**: Production down, immediate intervention required
4. **Lost credentials**: All Watchers/Mentors unavailable, emergency access needed

**NOT Legitimate**:
- Convenience (bypassing approval process)
- Impatience (change can't wait for review)
- Debugging (use `roles/viewer` instead)

---

### Break-Glass Access Protocol

**Step 1: Activate Break-Glass**
```bash
# Add yourself to nash-group-owners@ (Organization owner role)
gcloud organizations add-iam-policy-binding ORGANIZATION_ID \
  --member="user:jeffrey@nashgroup.example" \
  --role="roles/owner"
```

**Step 2: Document Activation**
```bash
# Log to incident response system
echo "$(date): Break-glass activated by jeffrey. Reason: [REASON]" >> /var/log/break-glass-events.log

# Alert Watchers (automated)
# Email sent to nash-group-watchers@ with details
```

**Step 3: Perform Emergency Action**
```bash
# Example: Restart compromised compute instance
gcloud compute instances stop INSTANCE_NAME --zone=ZONE
gcloud compute instances start INSTANCE_NAME --zone=ZONE

# Document every action
echo "$(date): Restarted instance INSTANCE_NAME" >> /var/log/break-glass-events.log
```

**Step 4: Deactivate Break-Glass**
```bash
# Remove yourself from nash-group-owners@
gcloud organizations remove-iam-policy-binding ORGANIZATION_ID \
  --member="user:jeffrey@nashgroup.example" \
  --role="roles/owner"

# Verify removal
gcloud organizations get-iam-policy ORGANIZATION_ID \
  --flatten="bindings[].members" \
  --filter="bindings.role:roles/owner"
```

**Step 5: Reconciliation (within 24 hours)**
1. Create Terraform PR to codify manual changes
2. Document actions in ADR (Architecture Decision Record)
3. Update runbooks if new pattern discovered
4. Conduct post-mortem (within 48 hours)

**Step 6: Post-Mortem (within 48 hours)**
- What happened?
- Why was break-glass necessary?
- What manual actions were taken?
- How can we prevent this in the future?
- What Covenant principles need updating?

---

### Break-Glass Audit

**Immediate Alerts** (sent to nash-group-watchers@):
- ANY action by nash-group-owners@ member triggers alert
- Email subject: "[CRITICAL] Break-Glass Access Used by [USER]"
- Email body: Timestamp, user, action, resource

**Weekly Review**:
- Watchers review all break-glass events
- Verify legitimacy of each use
- Follow up on outstanding reconciliation PRs

**Quarterly Review**:
- Full Council reviews break-glass usage patterns
- Update break-glass policies if needed
- Conduct break-glass drill (test procedures)

---

## Compliance and Governance

### Alignment with Covenant Principles

| Covenant Principle | GCP IAM Implementation | Verification |
|--------------------|----------------------|--------------|
| **#5: Infrastructure as Code** | All IAM policies in Terraform | Drift detection nightly |
| **#6: No Committed Secrets** | OIDC Workload Identity, no keys in git | Secret scanning in CI |
| **#9: Zero Trust** | OIDC for CI/CD, mTLS for services | Audit logs for all access |
| **#10: Least Privilege** | Predefined roles, minimal custom roles | Quarterly access audit |
| **#11: Measure Everything** | Cloud Audit Logs, Cloud Monitoring | Observability Bridge integration |
| **#12: Executable Runbooks** | Automated alerting with runbook URLs | Alert policy definitions |

---

### SOC 2 Type II Compliance

**Access Controls**:
- ✅ Principle of least privilege enforced (Principle #10)
- ✅ Access requests documented and approved (Citadel governance)
- ✅ Periodic access reviews (weekly/monthly/quarterly)
- ✅ Break-glass access logged and audited

**Audit Trails**:
- ✅ Complete audit logs (Cloud Audit Logs)
- ✅ Immutable log storage (1-year retention minimum)
- ✅ Tamper-proof logging (Google-managed, append-only)
- ✅ Log analysis and alerting (Observability Bridge)

**Change Management**:
- ✅ All changes via Terraform (Infrastructure as Code)
- ✅ Peer review required (GitHub PR process)
- ✅ Manual approval gate (HCP Terraform)
- ✅ Rollback capability (Terraform state history)

---

### GDPR Compliance

**Data Subject Rights**:
- Right to access: Cloud Audit Logs provide access trail
- Right to erasure: Service accounts deleted via Terraform destroy
- Right to portability: Audit logs exportable to JSON

**Data Protection**:
- Encryption at rest: Google-managed encryption
- Encryption in transit: TLS 1.3 for all API calls
- Access controls: Least privilege IAM policies
- Data residency: Configurable via GCP region selection

---

### NIST 800-63 Digital Identity Guidelines

**Identity Assurance Level (IAL)**:
- IAL2: WebAuthn (passkeys) for humans
- IAL3: WebAuthn + TOTP (multi-factor authentication)

**Authenticator Assurance Level (AAL)**:
- AAL2: OIDC tokens for CI/CD (short-lived)
- AAL3: mTLS certificates for services (15-minute lifetime)

**Federation Assurance Level (FAL)**:
- FAL2: Workload Identity Federation (OIDC)
- FAL3: Assertion encryption via TLS 1.3

---

### CIS Google Cloud Platform Foundation Benchmark

**IAM Recommendations**:
- ✅ 1.1: Ensure that corporate login credentials are used (Google Groups)
- ✅ 1.2: Ensure that multi-factor authentication is enabled (WebAuthn + TOTP)
- ✅ 1.4: Ensure that there are only GCP-managed service account keys for service accounts
- ✅ 1.5: Ensure that Service Account has no Admin privileges
- ✅ 1.6: Ensure that IAM users are not assigned the Service Account User role
- ✅ 1.7: Ensure user-managed/external keys for service accounts are rotated every 90 days

**Logging and Monitoring**:
- ✅ 2.1: Ensure that Cloud Audit Logging is configured properly
- ✅ 2.2: Ensure that sinks are configured for all log entries
- ✅ 2.3: Ensure that retention policies on log buckets are configured
- ✅ 2.5: Ensure that Cloud Asset Inventory is enabled

---

## Summary

This Google Cloud IAM strategy provides The Nash Group with:

1. **Organizational Alignment**: Google Groups mirror GitHub teams, ensuring consistency
2. **Zero-Trust Authentication**: Workload Identity Federation eliminates long-lived credentials
3. **Multi-Tenant Isolation**: Folders and projects enforce strong tenant boundaries
4. **Least Privilege Access**: Predefined roles and minimal custom roles
5. **Complete Audit Trail**: Cloud Audit Logs exported to Observability Bridge
6. **Policy Enforcement**: OPA policies validate authorization at runtime
7. **Automated Compliance**: Weekly/monthly/quarterly reports ensure ongoing compliance
8. **Break-Glass Procedures**: Documented emergency access with reconciliation requirements
9. **Governance Integration**: IAM decisions follow Covenant principles and governance levels

**Implementation Timeline**: 12 weeks (3 months)
**Governance Level**: Citadel (1 Mentor + 1 Watcher approval per phase)
**Post-Implementation**: Quarterly reviews to adapt to changing needs

---

## Next Steps

1. **Review and Approve**: Present this strategy to 1 Mentor + 1 Watcher for Citadel-level approval
2. **Create ADR**: Document decision in Architecture Decision Record
3. **Begin Phase 1**: Establish GCP Organization and foundational IAM structure
4. **Iterate**: Adapt strategy based on lessons learned during implementation

---

**Version History**:
- v1.0.0 (2025-11-10): Initial comprehensive GCP IAM strategy

**Next Review**: 2026-02-10 (Quarterly)

---

*"In Google Cloud, as in all realms of The Nash Group, identity is the foundation. Zero trust, least privilege, and complete audit trails ensure our infrastructure remains secure, compliant, and aligned with our principles."*

**The Shield protects all pillars. There can be only one identity source of truth.**
