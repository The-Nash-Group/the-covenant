# Policy Enforcement Guide - The Shield
**Version**: 1.0.1
**Created**: 2025-11-20
**Purpose**: Covenant policy context for OPA enforcement of IaC plans (SEC-003)

> **Ownership boundary:** This document is retained as Covenant policy context and historical implementation shape. Exact commands, Make targets, workflow files, tool versions, and runnable enforcement code are owned by `the-citadel`. Do not treat command snippets in this guide as the current Citadel runbook unless Citadel's repo contract confirms them.

---

## Table of Contents

1. [Overview](#overview)
2. [The Iron Gate Architecture](#the-iron-gate-architecture)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Policy Rules](#policy-rules)
7. [Testing](#testing)
8. [CI/CD Integration](#cicd-integration)
9. [Troubleshooting](#troubleshooting)

---

## Overview

**The Shield** enforces SEC-003 (Least Privilege Access) policy through **OPA (Open Policy Agent)** using the `conftest` CLI. This creates an "Iron Gate" that prevents policy violations from ever leaving your local machine.

### Key Principle

> "The System Will Enforce Invariantly. The Guardians Will Exercise Judgment."

**Machine enforces**: No wildcard IAM, no admin roles for services, strict tenant isolation
**Human reviews**: IaC plans, approves changes, exercises break-glass when needed

---

## The Iron Gate Architecture

```
┌────────────────────────────────────────────────────┐
│  1. Guardian writes OpenTofu code                  │
│     (the-citadel/terraform/*)                      │
└────────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────────┐
│  2. Guardian runs: make plan                       │
│     tofu plan -out=tfplan                          │
└────────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────────┐
│  3. THE IRON GATE (automatic)                      │
│     conftest test tfplan.json                      │
│     ├── SEC-003-RULE-1: No wildcard IAM            │
│     ├── SEC-003-RULE-2: No admin for machines      │
│     ├── SEC-003-RULE-3: Tenant isolation           │
│     ├── SEC-003-RULE-4: Zero trust network         │
│     ├── SEC-003-RULE-5: Key rotation               │
│     ├── SEC-003-RULE-6: No public buckets          │
│     ├── SEC-003-RULE-7: Prevent destroy            │
│     └── SEC-003-RULE-8: Team permissions           │
└────────────────────────────────────────────────────┘
                    ↓
          ┌─────────┴─────────┐
          │                   │
      ✅ PASS              ❌ FAIL
          │                   │
          ↓                   ↓
 ┌─────────────────┐   ┌──────────────────┐
 │  git commit     │   │  Fix violations  │
 │  git push       │   │  Re-run plan     │
 └─────────────────┘   └──────────────────┘
```

---

## Prerequisites

### Required Tools

- **OpenTofu** 1.11+
- **conftest** (OPA policy enforcer)
- **make** (GNU Make)
- **jq** (JSON processor, for debugging)

### Environment

- macOS, Linux, or WSL2
- Access to the-citadel workspace and remote state backend
- GitHub App or approved local machine-auth path for organization access

---

## Installation

### 1. Install conftest

**macOS**:
```bash
brew install conftest
```

**Linux**:
```bash
# Download latest release
wget https://github.com/open-policy-agent/conftest/releases/download/v0.47.0/conftest_0.47.0_Linux_x86_64.tar.gz
tar xzf conftest_0.47.0_Linux_x86_64.tar.gz
sudo mv conftest /usr/local/bin/
```

**Verify installation**:
```bash
conftest --version
# Expected: Conftest: 0.47.0+
```

### 2. Verify Policy Files

Check that policy files exist:
```bash
cd /Users/verlyn13/Development/the-nash-group

# Main policy file
ls the-citadel/policies/opa/sec-003-least-privilege.rego

# Test cases
ls the-citadel/policies/opa/tests/sec-003-*.tf
```

### 3. Test Policy Engine

Run a quick test:
```bash
cd the-citadel

# Test with violations (should fail)
make plan WORKSPACE_DIR=../the-citadel/policies/opa/tests
```

---

## Usage

### Standard Workflow

**1. Plan with Policy Enforcement**:
```bash
cd the-citadel

# Plan for organization workspace
make plan WORKSPACE_DIR=terraform/organization

# Plan for specific tenant
make plan WORKSPACE_DIR=terraform/projects/personal
```

**2. Review Output**:

**✅ Success**:
```
🛡️  Engaging The Shield (SEC-003: Least Privilege)...
✓ The Shield: Integrity Verified
```

**❌ Failure**:
```
🛡️  Engaging The Shield (SEC-003: Least Privilege)...
FAIL - SEC-003 Violation (The Shield): IAM Policy 'aws_iam_policy.wildcard_actions' grants wildcard '*' Action.

✗ The Shield: Policy violations detected
```

**3. Apply Changes** (if passed):
```bash
make apply WORKSPACE_DIR=terraform/organization
```

### Policy-Only Check

Run policy checks without planning:
```bash
# Generate plan first
cd terraform/organization
terraform plan -out=tfplan

# Then run policy check
cd ../..
make audit-shield WORKSPACE_DIR=terraform/organization
```

### Test Policy Changes

When modifying the policy itself:
```bash
cd the-citadel/policies/opa/tests

# Test violations (should fail)
terraform init
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json
conftest test tfplan.json -p ../sec-003-least-privilege.rego

# Test compliant code (should pass)
# Rename sec-003-compliant.tf to main.tf
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json
conftest test tfplan.json -p ../sec-003-least-privilege.rego
```

---

## Policy Rules

### RULE 1: No Wildcard IAM Actions

**What it checks**: IAM policies with `Action: "*"` or `Resource: "*"`

**Why**: Wildcards violate least privilege principle

**Violation example**:
```hcl
resource "aws_iam_policy" "bad" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = "*"  # ❌ DENIED
      Resource = "*"
    }]
  })
}
```

**Compliant example**:
```hcl
resource "aws_iam_policy" "good" {
  policy = jsonencode({
    Statement = [{
      Effect = "Allow"
      Action = ["s3:GetObject", "s3:ListBucket"]  # ✅ SPECIFIC
      Resource = "arn:aws:s3:::nash-personal-*"
    }]
  })
}
```

**Exception**: Break-glass accounts tagged with `Purpose = "break-glass"`

---

### RULE 2: No Admin Roles for Machines

**What it checks**: Service accounts/roles with Owner, Editor, or AdministratorAccess

**Why**: Machines should have minimal, specific permissions

**Violation example**:
```hcl
resource "google_project_iam_binding" "bad" {
  role = "roles/owner"  # ❌ DENIED
  members = ["serviceAccount:bot@project.iam.gserviceaccount.com"]
}
```

**Compliant example**:
```hcl
resource "google_project_iam_binding" "good" {
  role = "roles/compute.instanceAdmin.v1"  # ✅ SPECIFIC
  members = ["serviceAccount:deployer@project.iam.gserviceaccount.com"]
}
```

**Exception**: `human:owner` (e.g., `user:jeffrey@thenash.group`)

---

### RULE 3: Strict Tenant Isolation

**What it checks**: Resource names follow `nash-{tenant}-*` pattern

**Why**: Prevents cross-tenant resource access

**Violation example**:
```hcl
resource "google_service_account" "bad" {
  account_id = "generic-deployer"  # ❌ DENIED
}
```

**Compliant examples**:
```hcl
resource "google_service_account" "good" {
  account_id = "nash-personal-deployer"  # ✅ PASSES
}

resource "google_project" "good" {
  project_id = "nash-family-prod"  # ✅ PASSES
}
```

**Valid prefixes**: `nash-personal`, `nash-family`, `nash-university`, `nash-ai-lab`, `citadel`, `nexus`, `shield`

---

### RULE 4: Zero Trust Network

**What it checks**: Security groups allowing `0.0.0.0/0` on sensitive ports

**Why**: Implements Covenant Principle 9 (Zero Trust)

**Violation example**:
```hcl
resource "aws_security_group_rule" "bad" {
  type        = "ingress"
  from_port   = 22  # SSH
  cidr_blocks = ["0.0.0.0/0"]  # ❌ DENIED
}
```

**Compliant example**:
```hcl
resource "aws_security_group_rule" "good" {
  type        = "ingress"
  from_port   = 22
  cidr_blocks = ["10.0.0.0/8"]  # ✅ VPN only
}
```

**Sensitive ports**: 22 (SSH), 3389 (RDP), 27017 (MongoDB), 5432 (PostgreSQL), 3306 (MySQL), 6379 (Redis), 5601 (Kibana), 9200 (Elasticsearch)

---

### RULE 5: Service Account Key Rotation

**What it checks**: Service account keys without rotation policy

**Why**: Long-lived credentials are security liabilities

**Severity**: Warning (not blocking)

**Violation example**:
```hcl
resource "google_service_account_key" "bad" {
  service_account_id = google_service_account.deployer.name
  # ⚠️ WARNING: No rotation policy
}
```

**Best practice**: Use Workload Identity (OIDC) instead of service account keys

---

### RULE 6: No Public Storage Buckets

**What it checks**: S3/GCS buckets with public access

**Why**: Data leaks through misconfigured storage

**Violation example**:
```hcl
resource "aws_s3_bucket_public_access_block" "bad" {
  block_public_acls = false  # ❌ DENIED
}

resource "google_storage_bucket_iam_binding" "bad" {
  members = ["allUsers"]  # ❌ DENIED
}
```

**Compliant example**:
```hcl
resource "aws_s3_bucket_public_access_block" "good" {
  block_public_acls       = true   # ✅ PASSES
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

---

### RULE 7: Prevent Destroy on Critical Resources

**What it checks**: AWS accounts, GCP projects, KMS keys without `prevent_destroy`

**Why**: Accidental deletion is catastrophic

**Violation example**:
```hcl
resource "google_project" "bad" {
  project_id = "nash-personal-prod"
  # ❌ DENIED: Missing prevent_destroy
}
```

**Compliant example**:
```hcl
resource "google_project" "good" {
  project_id = "nash-personal-prod"

  lifecycle {
    prevent_destroy = true  # ✅ PASSES
  }
}
```

---

### RULE 8: GitHub Team Permissions

**What it checks**: Non-Watchers teams with `admin` permission

**Why**: Implements GOV-004 (Team Authority Matrix)

**Violation example**:
```hcl
resource "github_team_repository" "bad" {
  team_id    = github_team.mentors.id  # Not watchers
  permission = "admin"  # ❌ DENIED
}
```

**Compliant example**:
```hcl
resource "github_team_repository" "good" {
  team_id    = github_team.mentors.id
  permission = "maintain"  # ✅ PASSES
}

resource "github_team_repository" "watchers_ok" {
  team_id    = github_team.watchers.id
  permission = "admin"  # ✅ PASSES (watchers can have admin)
}
```

---

## Testing

### Test the Policy Engine

```bash
cd the-citadel/policies/opa/tests

# Test violations (should report 8+ failures)
terraform init
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json
conftest test tfplan.json -p ../sec-003-least-privilege.rego

# Expected output:
# FAIL - SEC-003 Violation (The Shield): IAM Policy 'aws_iam_policy.wildcard_actions_violation' grants wildcard '*' Action.
# FAIL - SEC-003 Violation (The Shield): Resource 'google_project_iam_binding.admin_role_violation' assigns prohibited role 'roles/owner'.
# ... (8+ failures)
```

### Test Compliant Code

```bash
# Swap to compliant examples
mv sec-003-violations.tf sec-003-violations.tf.bak
mv sec-003-compliant.tf main.tf

terraform init
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json
conftest test tfplan.json -p ../sec-003-least-privilege.rego

# Expected output:
# (no failures - only warnings for key rotation)
```

---

## CI/CD Integration

### GitHub Actions Workflow

> **Citadel-owned:** The runnable workflow belongs in `the-citadel`. The example below is historical context for the intended enforcement gate, not a current Covenant instruction to create workflow files here.

Create `.github/workflows/terraform-shield.yml`:

```yaml
name: The Shield - Policy Enforcement

on:
  pull_request:
    paths:
      - 'the-citadel/terraform/**'
      - 'the-covenant/policies/**'

jobs:
  shield-enforcement:
    name: SEC-003 Policy Check
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.12.2
          cli_config_credentials_token: ${{ secrets.TFC_TOKEN }}

      - name: Install conftest
        run: |
          wget https://github.com/open-policy-agent/conftest/releases/download/v0.47.0/conftest_0.47.0_Linux_x86_64.tar.gz
          tar xzf conftest_0.47.0_Linux_x86_64.tar.gz
          sudo mv conftest /usr/local/bin/

      - name: Terraform Init
        working-directory: the-citadel/terraform/organization
        run: terraform init

      - name: Terraform Plan
        working-directory: the-citadel/terraform/organization
        run: terraform plan -out=tfplan

      - name: The Iron Gate (Policy Enforcement)
        working-directory: the-citadel/terraform/organization
        run: |
          terraform show -json tfplan > tfplan.json
          conftest test tfplan.json -p ../../../the-citadel/policies/opa/sec-003-least-privilege.rego

      - name: Post Policy Results
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ **The Shield**: SEC-003 policy violations detected. Review the workflow logs for details.'
            })
```

---

## Troubleshooting

### conftest not found

```bash
# Verify installation
which conftest
conftest --version

# If not found, reinstall
brew install conftest  # macOS
```

### Policy file not found

```bash
# Verify path
ls ../the-citadel/policies/opa/sec-003-least-privilege.rego

# If running from wrong directory
cd the-citadel
make plan WORKSPACE_DIR=terraform/organization
```

### False positive: Break-glass account denied

**Solution**: Tag the resource with `Purpose = "break-glass"`:

```hcl
resource "aws_iam_role" "emergency" {
  name = "nash-break-glass-emergency"

  tags = {
    Purpose = "break-glass"  # ✅ Exempts from admin role check
  }
}
```

### Human owner denied

**Solution**: Ensure email contains owner's name:

```hcl
members = [
  "user:jeffrey@thenash.group"  # ✅ Detected as human owner
]
```

### Plan succeeds but policy fails

This means your Terraform code is valid but violates security policies. **This is expected behavior** - The Iron Gate is working correctly. Fix the violation and re-plan.

---

## Emergency Procedures

### Bypass The Shield (Break-Glass)

**⚠️ USE ONLY IN GENUINE EMERGENCIES**

```bash
cd the-citadel

# Bypass policy checks (EMERGENCY ONLY)
make emergency-bypass WORKSPACE_DIR=terraform/organization
# Will prompt for justification (logged to BREAK_GLASS_LOG.md)
```

**Post-Emergency**:
1. Create reconciliation PR within 24 hours
2. Update policies if legitimate gap discovered
3. Document in incident post-mortem

---

## Related Documents

- [SEC-003 Policy Specification](../sec-003-least-privilege.md)
- [ADR-005: Adopt OpenTofu as IaC Engine](../../docs/architecture/005-adopt-opentofu-as-iac-engine.md)
- [ROLES-AND-POLICIES-ANALYSIS.md](../../the-shield/docs/ROLES-AND-POLICIES-ANALYSIS.md)

---

**Last Updated**: 2026-04-26
**Version**: 1.0.1

---

*"The Iron Gate stands. No violation shall pass. This is The Nash Group way."*
