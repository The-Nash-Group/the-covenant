# Google Cloud IAM Quick Start Guide
**Version**: 1.0.0
**Created**: 2025-11-10
**For**: The Nash Group Guardians (Watchers, Mentors, Platform Clan)

> "This guide provides a practical, hands-on quick start for implementing The Nash Group's Google Cloud IAM strategy. For the complete strategy, see `GOOGLE-CLOUD-IAM-STRATEGY.md`."

---

## Overview

This guide walks you through implementing Google Cloud IAM for The Nash Group in **12 weeks**, following our three-pillar architecture and zero-trust principles.

**Core Principles**:
- Zero trust: No long-lived credentials, OIDC federation only
- Least privilege: Minimal permissions by default
- Infrastructure as Code: All IAM policies in Terraform
- Complete audit trail: Cloud Audit Logs exported to Observability Bridge

---

## Prerequisites

**Before You Begin**:
1. ✅ GCP account with billing enabled
2. ✅ Domain ownership verified (nashgroup.example)
3. ✅ Terraform 1.9+ installed
4. ✅ gcloud CLI installed and authenticated
5. ✅ GitHub repository access (`the-citadel`)
6. ✅ HCP Terraform workspace configured

**Required Roles**:
- Organization Administrator (to create Organization)
- Billing Administrator (to link billing account)

---

## Phase 1: Foundation (Weeks 1-2)

### Step 1: Create GCP Organization

```bash
# Verify domain ownership
gcloud organizations list

# Expected output: (empty if no org exists)

# Create organization (requires super admin in Google Workspace)
# This must be done via Google Admin Console:
# https://admin.google.com → Account → Account Settings → Enable Organization

# Verify organization creation
gcloud organizations list
# Expected output:
# DISPLAY_NAME       ID            DIRECTORY_CUSTOMER_ID
# nash-group.example 123456789012  C01234567
```

**Save Organization ID** for later use: `123456789012`

---

### Step 2: Create Google Groups

**Via Google Admin Console** (https://admin.google.com/ac/groups):

| Group Email | Description | Initial Members | Purpose |
|-------------|-------------|-----------------|---------|
| nash-group-owners@nashgroup.example | Break-glass super admins | jeffrey@nashgroup.example | Emergency access |
| nash-group-watchers@nashgroup.example | Security oversight | primary-watcher@nashgroup.example, secondary-watcher@nashgroup.example | Security audits, IAM changes |
| nash-group-mentors@nashgroup.example | Technical leadership | mentor1@nashgroup.example, mentor2@nashgroup.example | Infrastructure management |
| nash-group-platform@nashgroup.example | Service owners | developer1@nashgroup.example, developer2@nashgroup.example | Application deployments |
| nash-group-explorers@nashgroup.example | Experimental access | All Nash Group contributors | Development experimentation |

**Via gcloud CLI** (alternative):

```bash
# Create groups (requires Google Workspace API enabled)
gcloud identity groups create nash-group-owners@nashgroup.example \
  --display-name="Nash Group Owners (Break-Glass)" \
  --description="Emergency super admin access"

gcloud identity groups create nash-group-watchers@nashgroup.example \
  --display-name="Nash Group Watchers" \
  --description="Security oversight and IAM guardians"

gcloud identity groups create nash-group-mentors@nashgroup.example \
  --display-name="Nash Group Mentors" \
  --description="Technical leadership and infrastructure architects"

gcloud identity groups create nash-group-platform@nashgroup.example \
  --display-name="Nash Group Platform Clan" \
  --description="Service owners and application developers"

gcloud identity groups create nash-group-explorers@nashgroup.example \
  --display-name="Nash Group Explorers" \
  --description="Development environment experimentation"

# Add members to groups
gcloud identity groups memberships add \
  --group-email="nash-group-owners@nashgroup.example" \
  --member-email="jeffrey@nashgroup.example"

# Repeat for other groups...
```

---

### Step 3: Assign Organizational Roles

```bash
# Organization ID (from Step 1)
ORG_ID="123456789012"

# Assign nash-group-owners@ as Organization Owner (break-glass only)
gcloud organizations add-iam-policy-binding $ORG_ID \
  --member="group:nash-group-owners@nashgroup.example" \
  --role="roles/owner" \
  --condition=None

# Assign nash-group-watchers@ as Security Admin
gcloud organizations add-iam-policy-binding $ORG_ID \
  --member="group:nash-group-watchers@nashgroup.example" \
  --role="roles/securityadmin"

# Assign nash-group-watchers@ as Security Reviewer
gcloud organizations add-iam-policy-binding $ORG_ID \
  --member="group:nash-group-watchers@nashgroup.example" \
  --role="roles/iam.securityReviewer"

# Assign nash-group-watchers@ as Logging Viewer
gcloud organizations add-iam-policy-binding $ORG_ID \
  --member="group:nash-group-watchers@nashgroup.example" \
  --role="roles/logging.viewer"

# Assign nash-group-mentors@ as Organization Role Viewer
gcloud organizations add-iam-policy-binding $ORG_ID \
  --member="group:nash-group-mentors@nashgroup.example" \
  --role="roles/iam.organizationRoleViewer"

# Verify IAM policy
gcloud organizations get-iam-policy $ORG_ID
```

---

### Step 4: Enable Audit Logging

```bash
# Enable Data Access logs for all services
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="allUsers" \
  --role="roles/logging.viewer"

# Enable Admin Activity Logs (always enabled by default)
# Enable Data Access Logs
gcloud logging sinks create audit-logs-sink \
  storage.googleapis.com/nash-audit-logs-bucket \
  --log-filter='resource.type="audited_resource"'

# Create audit log configuration (via Terraform - see below)
```

**Terraform Configuration** (`the-citadel/terraform/gcp/audit-logs.tf`):

```hcl
resource "google_project_iam_audit_config" "audit_config" {
  project = var.gcp_project_id
  service = "allServices"

  audit_log_config {
    log_type = "ADMIN_READ"
  }

  audit_log_config {
    log_type = "DATA_READ"
    exempted_members = [
      # Exempt high-volume, low-risk reads
      "serviceAccount:observability-bridge@${var.gcp_project_id}.iam.gserviceaccount.com"
    ]
  }

  audit_log_config {
    log_type = "DATA_WRITE"
  }
}
```

---

### Step 5: Terraform Setup

**Create GCP Terraform Configuration**:

```bash
cd the-citadel/terraform
mkdir -p gcp
cd gcp

# Create provider configuration
cat > providers.tf <<'EOF'
terraform {
  required_version = ">= 1.9.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.11.0"  # Exact version pin (Covenant Principle 15)
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "6.11.0"
    }
  }

  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "the-nash-group"

    workspaces {
      name = "nash-gcp-production"
    }
  }
}

provider "google" {
  # Credentials via GOOGLE_CREDENTIALS environment variable in HCP Terraform
  # Or via OIDC Workload Identity (preferred)
}

provider "google-beta" {
  # Same as google provider
}
EOF

# Create variables configuration
cat > variables.tf <<'EOF'
variable "gcp_organization_id" {
  description = "GCP Organization ID"
  type        = string
}

variable "gcp_billing_account_id" {
  description = "GCP Billing Account ID"
  type        = string
}

variable "gcp_region" {
  description = "Default GCP region"
  type        = string
  default     = "us-central1"
}

variable "nash_group_domain" {
  description = "Nash Group domain for Google Groups"
  type        = string
  default     = "nashgroup.example"
}
EOF

# Create main configuration
cat > main.tf <<'EOF'
# Organization resource (data source)
data "google_organization" "nash_group" {
  domain = var.nash_group_domain
}

# Organizational IAM bindings
resource "google_organization_iam_member" "owners" {
  org_id = data.google_organization.nash_group.org_id
  role   = "roles/owner"
  member = "group:nash-group-owners@${var.nash_group_domain}"
}

resource "google_organization_iam_member" "watchers_security_admin" {
  org_id = data.google_organization.nash_group.org_id
  role   = "roles/securityadmin"
  member = "group:nash-group-watchers@${var.nash_group_domain}"
}

resource "google_organization_iam_member" "watchers_security_reviewer" {
  org_id = data.google_organization.nash_group.org_id
  role   = "roles/iam.securityReviewer"
  member = "group:nash-group-watchers@${var.nash_group_domain}"
}

resource "google_organization_iam_member" "watchers_logging_viewer" {
  org_id = data.google_organization.nash_group.org_id
  role   = "roles/logging.viewer"
  member = "group:nash-group-watchers@${var.nash_group_domain}"
}

resource "google_organization_iam_member" "mentors_org_role_viewer" {
  org_id = data.google_organization.nash_group.org_id
  role   = "roles/iam.organizationRoleViewer"
  member = "group:nash-group-mentors@${var.nash_group_domain}"
}
EOF

# Initialize Terraform
terraform init

# Plan changes
terraform plan

# Apply changes (requires HCP Terraform approval)
terraform apply
```

---

### Phase 1 Verification

```bash
# Verify Google Groups exist
gcloud identity groups list

# Verify organizational IAM bindings
gcloud organizations get-iam-policy $ORG_ID

# Verify audit logging enabled
gcloud logging sinks list

# Verify Terraform state
terraform state list
```

**✅ Phase 1 Complete**: Foundation established, Google Groups operational, audit logging enabled

---

## Phase 2: Multi-Tenant Structure (Weeks 3-4)

### Step 1: Create Folders

```bash
ORG_ID="123456789012"

# Create folders for each tenant
gcloud resource-manager folders create \
  --display-name="personal-infra" \
  --organization=$ORG_ID

gcloud resource-manager folders create \
  --display-name="family-infra" \
  --organization=$ORG_ID

gcloud resource-manager folders create \
  --display-name="university-infra" \
  --organization=$ORG_ID

gcloud resource-manager folders create \
  --display-name="ai-lab-infra" \
  --organization=$ORG_ID

# List folders
gcloud resource-manager folders list --organization=$ORG_ID
```

**Save Folder IDs** for later use:
- personal-infra: `111111111111`
- family-infra: `222222222222`
- university-infra: `333333333333`
- ai-lab-infra: `444444444444`

---

### Step 2: Create Projects

```bash
BILLING_ACCOUNT_ID="01234-56789-ABCDE"  # Your billing account ID
PERSONAL_FOLDER_ID="111111111111"
FAMILY_FOLDER_ID="222222222222"
AI_LAB_FOLDER_ID="444444444444"

# Create personal projects
gcloud projects create nash-personal-prod \
  --folder=$PERSONAL_FOLDER_ID \
  --name="Personal Services - Production"

gcloud projects create nash-personal-dev \
  --folder=$PERSONAL_FOLDER_ID \
  --name="Personal Services - Development"

# Create family projects
gcloud projects create nash-family-prod \
  --folder=$FAMILY_FOLDER_ID \
  --name="Family Services - Production"

gcloud projects create nash-family-dev \
  --folder=$FAMILY_FOLDER_ID \
  --name="Family Services - Development"

# Create AI lab projects
gcloud projects create nash-ai-lab-prod \
  --folder=$AI_LAB_FOLDER_ID \
  --name="AI Lab - Production"

gcloud projects create nash-ai-lab-dev \
  --folder=$AI_LAB_FOLDER_ID \
  --name="AI Lab - Development"

# Link billing accounts
gcloud billing projects link nash-personal-prod \
  --billing-account=$BILLING_ACCOUNT_ID

gcloud billing projects link nash-personal-dev \
  --billing-account=$BILLING_ACCOUNT_ID

# Repeat for other projects...

# List projects
gcloud projects list --folder=$PERSONAL_FOLDER_ID
```

---

### Step 3: Assign Folder-Level IAM Policies

```bash
PERSONAL_FOLDER_ID="111111111111"
FAMILY_FOLDER_ID="222222222222"

# Personal folder: personal-admin has editor role
gcloud resource-manager folders add-iam-policy-binding $PERSONAL_FOLDER_ID \
  --member="group:nash-group-personal-admin@nashgroup.example" \
  --role="roles/editor"

# Personal folder: mentors and watchers have viewer role
gcloud resource-manager folders add-iam-policy-binding $PERSONAL_FOLDER_ID \
  --member="group:nash-group-mentors@nashgroup.example" \
  --role="roles/viewer"

gcloud resource-manager folders add-iam-policy-binding $PERSONAL_FOLDER_ID \
  --member="group:nash-group-watchers@nashgroup.example" \
  --role="roles/viewer"

# Family folder: family-admin has editor role
gcloud resource-manager folders add-iam-policy-binding $FAMILY_FOLDER_ID \
  --member="group:nash-group-family-admin@nashgroup.example" \
  --role="roles/editor"

# Family folder: family-member has viewer role (prod only, set at project level)
gcloud projects add-iam-policy-binding nash-family-prod \
  --member="group:nash-group-family-member@nashgroup.example" \
  --role="roles/viewer"

# Verify folder IAM policies
gcloud resource-manager folders get-iam-policy $PERSONAL_FOLDER_ID
gcloud resource-manager folders get-iam-policy $FAMILY_FOLDER_ID
```

---

### Step 4: Configure Network Isolation

```bash
PROJECT_ID="nash-personal-prod"

# Enable Compute Engine API
gcloud services enable compute.googleapis.com --project=$PROJECT_ID

# Create VPC
gcloud compute networks create personal-prod-vpc \
  --project=$PROJECT_ID \
  --subnet-mode=custom \
  --bgp-routing-mode=regional

# Create subnet
gcloud compute networks subnets create personal-prod-subnet \
  --project=$PROJECT_ID \
  --network=personal-prod-vpc \
  --region=us-central1 \
  --range=10.0.0.0/24

# Create firewall rules (deny all ingress by default)
gcloud compute firewall-rules create personal-prod-deny-all-ingress \
  --project=$PROJECT_ID \
  --network=personal-prod-vpc \
  --action=DENY \
  --rules=all \
  --direction=INGRESS \
  --priority=65534

# Create firewall rule (allow internal VPC traffic)
gcloud compute firewall-rules create personal-prod-allow-internal \
  --project=$PROJECT_ID \
  --network=personal-prod-vpc \
  --action=ALLOW \
  --rules=tcp:0-65535,udp:0-65535,icmp \
  --direction=INGRESS \
  --priority=1000 \
  --source-ranges=10.0.0.0/24

# Repeat for other tenants (family, university, ai-lab)
```

---

### Step 5: Apply Resource Labels

```bash
PROJECT_ID="nash-personal-prod"

# Set project labels
gcloud projects update $PROJECT_ID \
  --update-labels=tenant=personal,environment=prod,governance-level=citadel,cost-center=personal-001

# Set labels on compute instances (example)
gcloud compute instances add-labels INSTANCE_NAME \
  --project=$PROJECT_ID \
  --zone=us-central1-a \
  --labels=tenant=personal,environment=prod,owner=jeffrey@nashgroup.example

# Create OPA policy to enforce labels (see Phase 5)
```

---

### Phase 2 Verification

```bash
# Verify folders
gcloud resource-manager folders list --organization=$ORG_ID

# Verify projects
gcloud projects list

# Verify folder IAM policies
gcloud resource-manager folders get-iam-policy $PERSONAL_FOLDER_ID

# Verify VPCs
gcloud compute networks list --project=nash-personal-prod

# Verify labels
gcloud projects describe nash-personal-prod
```

**✅ Phase 2 Complete**: Multi-tenant folder structure established, network isolation configured

---

## Phase 3: Workload Identity Federation (Weeks 5-6)

### Step 1: Create Workload Identity Pool

```bash
PROJECT_ID="nash-personal-prod"

# Enable IAM API
gcloud services enable iam.googleapis.com --project=$PROJECT_ID
gcloud services enable iamcredentials.googleapis.com --project=$PROJECT_ID

# Create Workload Identity Pool
gcloud iam workload-identity-pools create github-actions-pool \
  --project=$PROJECT_ID \
  --location="global" \
  --display-name="GitHub Actions OIDC Pool" \
  --description="Workload Identity Pool for GitHub Actions CI/CD"

# Create Workload Identity Provider (GitHub OIDC)
gcloud iam workload-identity-pools providers create-oidc github-oidc-provider \
  --project=$PROJECT_ID \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --display-name="GitHub OIDC Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.ref=assertion.ref" \
  --issuer-uri="https://token.actions.githubusercontent.com"

# Get Workload Identity Pool Provider resource name
gcloud iam workload-identity-pools providers describe github-oidc-provider \
  --project=$PROJECT_ID \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --format="value(name)"

# Save this value: projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-oidc-provider
```

---

### Step 2: Create Service Accounts

```bash
PROJECT_ID="nash-personal-prod"

# Create citadel-deployer service account (Infrastructure as Code)
gcloud iam service-accounts create citadel-deployer \
  --project=$PROJECT_ID \
  --display-name="The Citadel Infrastructure Deployer" \
  --description="Service account for Terraform infrastructure deployments"

# Create nexus-deployer service account (Service deployments)
gcloud iam service-accounts create nexus-deployer \
  --project=$PROJECT_ID \
  --display-name="The Nexus Service Deployer" \
  --description="Service account for application deployments"

# Create shield-deployer service account (IAM management)
gcloud iam service-accounts create shield-deployer \
  --project=$PROJECT_ID \
  --display-name="The Shield IAM Manager" \
  --description="Service account for IAM management"

# List service accounts
gcloud iam service-accounts list --project=$PROJECT_ID
```

---

### Step 3: Configure IAM Bindings

```bash
PROJECT_ID="nash-personal-prod"
WORKLOAD_IDENTITY_POOL="projects/123456789/locations/global/workloadIdentityPools/github-actions-pool"

# Allow GitHub Actions from the-citadel repo to impersonate citadel-deployer@
gcloud iam service-accounts add-iam-policy-binding citadel-deployer@$PROJECT_ID.iam.gserviceaccount.com \
  --project=$PROJECT_ID \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL}/attribute.repository/the-nash-group/the-citadel"

# Allow GitHub Actions from the-nexus repo to impersonate nexus-deployer@
gcloud iam service-accounts add-iam-policy-binding nexus-deployer@$PROJECT_ID.iam.gserviceaccount.com \
  --project=$PROJECT_ID \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL}/attribute.repository/the-nash-group/the-nexus"

# Allow GitHub Actions from the-shield repo to impersonate shield-deployer@
gcloud iam service-accounts add-iam-policy-binding shield-deployer@$PROJECT_ID.iam.gserviceaccount.com \
  --project=$PROJECT_ID \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL}/attribute.repository/the-nash-group/the-shield"

# Verify bindings
gcloud iam service-accounts get-iam-policy citadel-deployer@$PROJECT_ID.iam.gserviceaccount.com \
  --project=$PROJECT_ID
```

---

### Step 4: Grant Service Account Permissions

```bash
PROJECT_ID="nash-personal-prod"

# Grant citadel-deployer necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:citadel-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/editor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:citadel-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountAdmin"

# Grant nexus-deployer necessary roles (custom role)
# Create custom role: nash.cicd-deployer (see GOOGLE-CLOUD-IAM-STRATEGY.md)
gcloud iam roles create cicd_deployer \
  --project=$PROJECT_ID \
  --title="Nash CI/CD Deployer" \
  --description="Minimal permissions for CI/CD deployments" \
  --permissions="compute.instances.create,compute.instances.update,cloudfunctions.functions.create,cloudfunctions.functions.update,run.services.create,run.services.update,iam.serviceAccounts.actAs" \
  --stage=GA

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:nexus-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="projects/$PROJECT_ID/roles/cicd_deployer"

# Grant shield-deployer necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:shield-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.securityAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:shield-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountAdmin"

# Verify permissions
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:citadel-deployer@*"
```

---

### Step 5: Update GitHub Actions Workflows

**Example Workflow** (`.github/workflows/deploy-to-gcp.yml`):

```yaml
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
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-oidc-provider'
          service_account: 'citadel-deployer@nash-personal-prod.iam.gserviceaccount.com'

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Deploy with Terraform
        run: |
          cd terraform/gcp
          terraform init
          terraform apply -auto-approve

      - name: Verify deployment
        run: |
          gcloud compute instances list --project=nash-personal-prod
```

**Test Workflow**:
```bash
# Trigger workflow
git commit --allow-empty -m "test: trigger GCP deployment"
git push origin main

# Monitor workflow in GitHub Actions UI
# https://github.com/the-nash-group/the-citadel/actions
```

---

### Phase 3 Verification

```bash
# Verify Workload Identity Pool
gcloud iam workload-identity-pools list --location=global

# Verify Service Accounts
gcloud iam service-accounts list --project=$PROJECT_ID

# Verify IAM bindings
gcloud iam service-accounts get-iam-policy citadel-deployer@$PROJECT_ID.iam.gserviceaccount.com

# Verify no service account keys exist
gcloud iam service-accounts keys list \
  --iam-account=citadel-deployer@$PROJECT_ID.iam.gserviceaccount.com

# Test GitHub Actions workflow
# (See GitHub Actions UI for results)
```

**✅ Phase 3 Complete**: Workload Identity Federation operational, zero long-lived credentials

---

## Phase 4-6: Monitoring, OPA Policies, Hardening

For detailed steps on:
- **Phase 4**: Monitoring and Alerting (Cloud Audit Logs, alerting policies, compliance reports)
- **Phase 5**: OPA Policy Enforcement (tenant boundaries, AI agent quotas, family safety)
- **Phase 6**: Integration and Hardening (VPC Service Controls, security review, runbooks)

See the complete strategy document: `GOOGLE-CLOUD-IAM-STRATEGY.md`

---

## Quick Reference Commands

### View IAM Policies

```bash
# Organization-level
gcloud organizations get-iam-policy $ORG_ID

# Folder-level
gcloud resource-manager folders get-iam-policy $FOLDER_ID

# Project-level
gcloud projects get-iam-policy $PROJECT_ID

# Service Account
gcloud iam service-accounts get-iam-policy SA_EMAIL@$PROJECT_ID.iam.gserviceaccount.com
```

---

### Modify IAM Policies

```bash
# Add IAM binding
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="group:nash-group-mentors@nashgroup.example" \
  --role="roles/viewer"

# Remove IAM binding
gcloud projects remove-iam-policy-binding $PROJECT_ID \
  --member="group:nash-group-mentors@nashgroup.example" \
  --role="roles/viewer"

# Replace entire policy (DANGEROUS - use with caution)
gcloud projects set-iam-policy $PROJECT_ID policy.yaml
```

---

### Audit and Troubleshooting

```bash
# View recent audit logs
gcloud logging read "resource.type=audited_resource" \
  --limit=50 \
  --format=json

# View IAM policy changes
gcloud logging read 'protoPayload.methodName="SetIamPolicy"' \
  --limit=50 \
  --format=json

# View service account key creations
gcloud logging read 'protoPayload.methodName="google.iam.admin.v1.CreateServiceAccountKey"' \
  --limit=50 \
  --format=json

# Check who can impersonate service account
gcloud iam service-accounts get-iam-policy SA_EMAIL@$PROJECT_ID.iam.gserviceaccount.com

# Test IAM policy (dry run)
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.role:roles/owner"
```

---

### Break-Glass Access

```bash
# Activate break-glass (emergency only)
gcloud organizations add-iam-policy-binding $ORG_ID \
  --member="user:jeffrey@nashgroup.example" \
  --role="roles/owner"

# Document activation
echo "$(date): Break-glass activated by jeffrey. Reason: [REASON]" >> /var/log/break-glass-events.log

# Perform emergency action...

# Deactivate break-glass
gcloud organizations remove-iam-policy-binding $ORG_ID \
  --member="user:jeffrey@nashgroup.example" \
  --role="roles/owner"

# Verify removal
gcloud organizations get-iam-policy $ORG_ID \
  --flatten="bindings[].members" \
  --filter="bindings.role:roles/owner"
```

---

## Troubleshooting

### Issue: "Permission denied" when creating Organization

**Cause**: Only Google Workspace Super Admins can create Organizations

**Solution**:
1. Log in to Google Admin Console with Super Admin account
2. Enable Organization: https://admin.google.com → Account → Account Settings
3. Retry `gcloud organizations list`

---

### Issue: "Workload Identity Provider not found"

**Cause**: OIDC provider not configured correctly

**Solution**:
```bash
# Verify pool exists
gcloud iam workload-identity-pools list --location=global

# Verify provider exists
gcloud iam workload-identity-pools providers list \
  --workload-identity-pool=github-actions-pool \
  --location=global

# Check attribute mapping
gcloud iam workload-identity-pools providers describe github-oidc-provider \
  --workload-identity-pool=github-actions-pool \
  --location=global
```

---

### Issue: GitHub Actions authentication fails

**Cause**: Missing `id-token: write` permission or incorrect service account

**Solution**:
1. Verify workflow has `permissions: id-token: write`
2. Verify service account email matches exactly
3. Check Workload Identity Pool resource name is correct
4. Test locally:
   ```bash
   gcloud auth application-default login
   gcloud projects list
   ```

---

### Issue: Terraform fails to authenticate

**Cause**: Missing GOOGLE_CREDENTIALS or incorrect Workload Identity setup

**Solution**:
1. For local development:
   ```bash
   gcloud auth application-default login
   export GOOGLE_CREDENTIALS=$(gcloud auth application-default print-access-token)
   ```

2. For HCP Terraform:
   - Add Environment Variable: `GOOGLE_CREDENTIALS` (service account key JSON)
   - Or configure Workload Identity Federation (preferred)

---

## Next Steps

1. **Complete Phase 1-3** using this guide
2. **Review Full Strategy**: Read `GOOGLE-CLOUD-IAM-STRATEGY.md` for Phases 4-6
3. **Create ADR**: Document your GCP IAM decisions in Architecture Decision Record
4. **Iterate**: Adapt strategy based on your specific needs

---

## Additional Resources

- **Complete Strategy**: `GOOGLE-CLOUD-IAM-STRATEGY.md`
- **Nash Group Principles**: `the-covenant/PRINCIPLES.md`
- **IAM Framework**: `.org/IAM-FRAMEWORK.md`
- **Terraform Docs**: https://registry.terraform.io/providers/hashicorp/google/latest/docs
- **Workload Identity Federation**: https://cloud.google.com/iam/docs/workload-identity-federation

---

**Version History**:
- v1.0.0 (2025-11-10): Initial quick start guide

---

*"Identity is the foundation. Build it right, and everything else follows."*
