# Federated Identity Quick Reference
**Version**: 1.0.0
**Created**: 2025-11-10
**Companion to**: `FEDERATED-IDENTITY-STRATEGY.md`

> "One login, every platform. This is the quick reference for implementing The Nash Group's federated identity system."

---

## TL;DR: The Two-Track Model

| Access Type | Protocol | Use Case | Example |
|------------|----------|----------|---------|
| **Human** | SAML 2.0 | Guardian logs into AWS Console | Jeffrey clicks "AWS" in Google app tray |
| **Machine** | OIDC | GitHub Actions deploys to AWS | Workflow gets temporary AWS credentials |

**Core Principle**: Google Workspace (`thenash.group`) is the Single Source of Truth (SSoT). All other platforms federate to it.

---

## Quick Start Checklist

### Prerequisites (Do Once)
- [x] Google Workspace with `guardian@thenash.group` *(done in Phase 1)*
- [x] Google Groups created (nash-group-owners@, watchers@, mentors@, platform@, explorers@) *(done in Phase 1)*
- [ ] GitHub Enterprise Cloud subscription *(if doing GitHub SAML SSO)*
- [ ] AWS Organization created *(if doing AWS)*
- [ ] Cloudflare Zero Trust enabled *(if doing Cloudflare Access)*

### Implementation Order
1. **Week 3-4**: GitHub Federation (SAML + OIDC)
2. **Week 5-7**: AWS Federation (SAML + OIDC)
3. **Week 8-9**: Cloudflare Federation (SAML + API tokens)
4. **Week 10**: HCP Terraform Federation (SAML)

---

## Visual Architecture

### Current State (Multi-Platform, Siloed Identity)
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   GCP       │  │   GitHub    │  │   AWS       │  │ Cloudflare  │
│             │  │             │  │             │  │             │
│ jeffrey@    │  │ jeffrey-gh  │  │ jeff-aws    │  │ jeff-cf     │
│ thenash.    │  │ (password)  │  │ (password)  │  │ (password)  │
│ group       │  │             │  │             │  │             │
│ (Google)    │  │ + PAT in    │  │ + API key   │  │ + API token │
│             │  │   GitHub    │  │   in GitHub │  │   in GitHub │
│             │  │   Secrets   │  │   Secrets   │  │   Secrets   │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
     ✅               ⚠️              ❌               ⚠️
   Correct       Needs SAML       Not setup      Needs SAML
```

### Target State (Federated Identity)
```
                 ┌──────────────────────────────────┐
                 │   GOOGLE WORKSPACE (SSoT)        │
                 │   thenash.group                  │
                 │                                  │
                 │  jeffrey@thenash.group           │
                 │  ├─ nash-group-mentors@          │
                 │  └─ nash-group-watchers@         │
                 └────────────┬─────────────────────┘
                              │
                ┌─────────────┴─────────────────────┐
                │                                   │
    ┌───────────▼──────────┐          ┌────────────▼────────────┐
    │  SAML 2.0            │          │  OIDC                   │
    │  (Human Guardians)   │          │  (GitHub Actions)       │
    └───────────┬──────────┘          └────────────┬────────────┘
                │                                   │
    ┌───────────┴───────────┐         ┌────────────┴────────────┐
    │                       │         │                         │
┌───▼────┐  ┌───▼─────┐  ┌─▼──────┐ ┌▼────────┐  ┌───▼──────┐  │
│ GitHub │  │ AWS     │  │ Cloud- │ │ GCP WIF │  │ AWS IAM  │  │
│ SAML   │  │ IAM ID  │  │ flare  │ │ Pool    │  │ OIDC     │  │
│ SSO    │  │ Center  │  │ Access │ │         │  │ Provider │  │
└────────┘  └─────────┘  └────────┘ └─────────┘  └──────────┘  │
     ✅          ✅           ✅          ✅           ✅          │
All Platforms Trust Google Workspace - No Platform-Specific     │
Passwords or Long-Lived API Keys                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## SAML 2.0 Setup (Human Access)

### Flow Diagram
```
Guardian                Google Workspace           AWS Console
   │                           │                         │
   │ 1. Click "AWS Console"    │                         │
   ├──────────────────────────>│                         │
   │                           │                         │
   │ 2. Already logged in?     │                         │
   │    (check session)        │                         │
   │<──────────────────────────┤                         │
   │                           │                         │
   │ 3. Generate SAML          │                         │
   │    assertion              │                         │
   │    (signed XML)           │                         │
   │                           ├────────────────────────>│
   │                           │ 4. Here's jeffrey@,     │
   │                           │    he's a Mentor        │
   │                           │                         │
   │                           │ 5. Validate signature,  │
   │                           │    map Mentor → AWS     │
   │                           │    Permission Set       │
   │                           │<────────────────────────┤
   │                           │                         │
   │ 6. Redirect with session  │                         │
   │<──────────────────────────┼─────────────────────────┤
   │                           │                         │
   │ 7. Access AWS Console     │                         │
   ├──────────────────────────────────────────────────>  │
   │                           │                         │
```

### Google Workspace SAML App Setup

**Step 1: Add SAML App in Google Admin Console**
```
Google Admin Console → Apps → Web and mobile apps → Add App → Search for "AWS"

OR for custom apps:
→ Add custom SAML app
   - App name: "AWS IAM Identity Center"
   - ACS URL: https://YOUR-AWS-SSO-URL/saml/assertion
   - Entity ID: https://YOUR-AWS-SSO-URL/saml/metadata
   - Name ID format: EMAIL
   - Name ID: Basic Information > Primary email
```

**Step 2: Configure SAML Attributes**
```
Attribute Mapping:
- email     → Basic Information > Primary email
- groups    → Google Groups > Group membership (full path)
```

**Step 3: Assign to Users/Groups**
```
Turn on for: Everyone (or specific groups like nash-group-mentors@)
```

**Step 4: Download IdP Metadata**
```
Google Admin Console → Apps → Web and mobile apps → [Your SAML App]
→ Download metadata → Save as google-workspace-metadata.xml
```

### AWS IAM Identity Center Setup

**Step 1: Enable IAM Identity Center**
```bash
# Via AWS Console (must be done manually first time)
AWS Console → IAM Identity Center → Enable

# Note the IAM Identity Center URL (e.g., https://d-1234567890.awsapps.com/start)
```

**Step 2: Configure External Identity Provider**
```bash
# Via AWS Console
IAM Identity Center → Settings → Identity source → Actions → Change identity source
→ External identity provider
   - Upload google-workspace-metadata.xml
   - Accept terms
   - Configure

# Via AWS CLI
aws sso-admin create-instance-access-control-attribute-configuration \
  --instance-arn arn:aws:sso:::instance/ssoins-1234567890abcdef \
  --access-control-attributes "Key=email,Value={Source=[{Namespace=urn:ietf:params:scim:schemas:core:2.0:User,AttributePath=email}]}" \
  --access-control-attributes "Key=groups,Value={Source=[{Namespace=urn:ietf:params:scim:schemas:core:2.0:User,AttributePath=groups}]}"
```

**Step 3: Create Permission Sets (via Terraform)**
```hcl
# the-citadel/terraform/aws/sso-permission-sets.tf
resource "aws_ssoadmin_permission_set" "mentor_power_user" {
  name             = "AWS-Mentor-PowerUser"
  description      = "Power user access for Nash Group Mentors"
  instance_arn     = local.sso_instance_arn
  session_duration = "PT8H" # 8 hours

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/PowerUserAccess"
  ]
}

resource "aws_ssoadmin_permission_set" "watcher_security_audit" {
  name             = "AWS-Watcher-SecurityAudit"
  description      = "Security audit access for Nash Group Watchers"
  instance_arn     = local.sso_instance_arn
  session_duration = "PT4H" # 4 hours

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/SecurityAudit",
    "arn:aws:iam::aws:policy/ReadOnlyAccess"
  ]
}
```

**Step 4: Assign Permission Sets to Google Groups**
```hcl
# the-citadel/terraform/aws/sso-assignments.tf
resource "aws_ssoadmin_account_assignment" "mentor_power_user" {
  instance_arn       = local.sso_instance_arn
  permission_set_arn = aws_ssoadmin_permission_set.mentor_power_user.arn

  principal_id   = "nash-group-mentors@thenash.group" # From SAML assertion
  principal_type = "GROUP"

  target_id   = data.aws_caller_identity.current.account_id
  target_type = "AWS_ACCOUNT"
}
```

**Step 5: Test SAML SSO**
```
1. Open Google Workspace app tray
2. Click "AWS IAM Identity Center"
3. Should redirect to AWS Console without password prompt
4. Verify session shows: "Logged in as jeffrey@thenash.group (AWS-Mentor-PowerUser)"
```

---

## OIDC Setup (Machine Access)

### Flow Diagram
```
GitHub Actions          GitHub OIDC Provider       GCP/AWS
Workflow
   │                           │                      │
   │ 1. Workflow starts        │                      │
   │    (on: push)             │                      │
   │                           │                      │
   │ 2. Request OIDC token     │                      │
   ├──────────────────────────>│                      │
   │                           │                      │
   │ 3. Generate JWT           │                      │
   │    (signed by GitHub)     │                      │
   │    Claims:                │                      │
   │    - repo: the-citadel    │                      │
   │    - ref: refs/heads/main │                      │
   │    - exp: 5 minutes       │                      │
   │<──────────────────────────┤                      │
   │                           │                      │
   │ 4. Send JWT to cloud      │                      │
   ├─────────────────────────────────────────────────>│
   │                           │ 5. Validate JWT,     │
   │                           │    check conditions  │
   │                           │    (repo, branch)    │
   │                           │                      │
   │ 6. Temporary credentials  │                      │
   │    (expires in 1 hour)    │                      │
   │<─────────────────────────────────────────────────┤
   │                           │                      │
   │ 7. Use credentials        │                      │
   │    (terraform apply)      │                      │
   ├─────────────────────────────────────────────────>│
   │                           │                      │
   │ 8. Workflow ends,         │                      │
   │    credentials expire     │                      │
   │                           │                      │
```

### GCP Workload Identity Federation Setup

**Step 1: Create Workload Identity Pool (via Terraform)**
```hcl
# the-citadel/terraform/gcp/workload-identity-github.tf
resource "google_iam_workload_identity_pool" "github_actions" {
  workload_identity_pool_id = "github-actions"
  display_name              = "GitHub Actions Pool"
  description               = "Identity pool for GitHub Actions OIDC"
  disabled                  = false
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_actions.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  display_name                       = "GitHub OIDC Provider"

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

**Step 2: Grant Service Account Impersonation (with Conditions)**
```hcl
resource "google_service_account_iam_member" "citadel_deployer_wif" {
  service_account_id = google_service_account.citadel_deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_actions.name}/attribute.repository/The-Nash-Group/the-citadel"

  condition {
    title       = "Only main branch"
    description = "Restrict to main branch deployments"
    expression  = "assertion.ref == 'refs/heads/main'"
  }
}
```

**Step 3: GitHub Actions Workflow**
```yaml
# .github/workflows/deploy-gcp.yml
name: Deploy to GCP

on:
  push:
    branches: [main]

permissions:
  id-token: write # Required for OIDC
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/123456789012/locations/global/workloadIdentityPools/github-actions/providers/github'
          service_account: 'citadel-deployer@nash-personal-prod.iam.gserviceaccount.com'
          # No secrets needed! Token is short-lived and repo-scoped

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Deploy Infrastructure
        run: |
          cd terraform
          terraform init
          terraform plan
          terraform apply -auto-approve
```

### AWS OIDC Setup

**Step 1: Create OIDC Provider (via Terraform)**
```hcl
# the-citadel/terraform/aws/github-oidc-provider.tf
resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]

  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1" # GitHub's OIDC cert thumbprint
  ]

  tags = {
    Name       = "github-actions-oidc"
    Governance = "citadel"
  }
}
```

**Step 2: Create IAM Role with Trust Policy**
```hcl
# the-citadel/terraform/aws/github-oidc-roles.tf
data "aws_iam_policy_document" "citadel_deployer_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github_actions.arn]
    }

    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:The-Nash-Group/the-citadel:*"]
    }
  }
}

resource "aws_iam_role" "citadel_deployer" {
  name               = "citadel-deployer"
  assume_role_policy = data.aws_iam_policy_document.citadel_deployer_assume_role.json

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/PowerUserAccess"
  ]

  tags = {
    Name       = "citadel-deployer"
    Purpose    = "GitHub Actions CI/CD"
    Governance = "citadel"
  }
}
```

**Step 3: GitHub Actions Workflow**
```yaml
# .github/workflows/deploy-aws.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

permissions:
  id-token: write # Required for OIDC
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/citadel-deployer
          aws-region: us-east-1
          # No AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY needed!

      - name: Deploy Infrastructure
        run: |
          cd terraform
          terraform init
          terraform plan
          terraform apply -auto-approve
```

---

## Multi-Cloud Deployment Workflow

### Combined GCP + AWS Deployment

```yaml
# .github/workflows/deploy-multi-cloud.yml
name: Deploy to GCP and AWS

on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  deploy-gcp:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/.../github-actions/providers/github'
          service_account: 'citadel-deployer@nash-personal-prod.iam'

      - name: Deploy GCP Infrastructure
        run: |
          cd terraform/gcp
          terraform init
          terraform apply -auto-approve

  deploy-aws:
    runs-on: ubuntu-latest
    needs: deploy-gcp # Run sequentially or use parallel
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/citadel-deployer
          aws-region: us-east-1

      - name: Deploy AWS Infrastructure
        run: |
          cd terraform/aws
          terraform init
          terraform apply -auto-approve

  deploy-cloudflare:
    runs-on: ubuntu-latest
    needs: [deploy-gcp, deploy-aws]
    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to GCP (to fetch Cloudflare token)
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/.../github-actions/providers/github'
          service_account: 'citadel-deployer@nash-personal-prod.iam'

      - name: Fetch Cloudflare API Token from Secret Manager
        id: secrets
        run: |
          TOKEN=$(gcloud secrets versions access latest --secret="cloudflare-api-token")
          echo "::add-mask::$TOKEN"
          echo "CLOUDFLARE_API_TOKEN=$TOKEN" >> $GITHUB_ENV

      - name: Deploy Cloudflare Configuration
        env:
          CLOUDFLARE_API_TOKEN: ${{ env.CLOUDFLARE_API_TOKEN }}
        run: |
          cd terraform/cloudflare
          terraform init
          terraform apply -auto-approve
```

---

## Troubleshooting Guide

### SAML SSO Errors

#### Error: "Unable to sign in - Invalid SAML response"
**Cause**: Clock skew or expired SAML assertion
**Fix**:
```bash
# Check time sync on Google Workspace
# SAML assertions are only valid for 5 minutes

# Verify AWS IAM Identity Center is using correct IdP metadata
aws sso-admin describe-instance-access-control-attribute-configuration \
  --instance-arn arn:aws:sso:::instance/ssoins-XXXX
```

#### Error: "User is not assigned to a permission set"
**Cause**: Google Group not mapped to AWS Permission Set
**Fix**:
```bash
# Verify user is in correct Google Group
gcloud identity groups memberships list \
  --group-email="nash-group-mentors@thenash.group"

# Verify Permission Set assignment in AWS
aws sso-admin list-account-assignments \
  --instance-arn arn:aws:sso:::instance/ssoins-XXXX \
  --account-id 123456789012 \
  --permission-set-arn arn:aws:sso:::permissionSet/ssoins-XXXX/ps-XXXX
```

### OIDC Errors

#### Error: "OIDC token validation failed"
**Cause**: Incorrect audience or issuer
**Fix**:
```bash
# For GCP: Verify Workload Identity Pool configuration
gcloud iam workload-identity-pools providers describe github \
  --workload-identity-pool=github-actions \
  --location=global

# For AWS: Verify OIDC Provider thumbprint
aws iam get-open-id-connect-provider \
  --open-id-connect-provider-arn arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com
```

#### Error: "Permission denied - repository not authorized"
**Cause**: OIDC condition restricts repo/branch
**Fix**:
```hcl
# Check IAM condition in Terraform
# Ensure assertion.repository matches your repo name
condition {
  title      = "Only the-citadel repo"
  expression = "assertion.repository == 'The-Nash-Group/the-citadel'"
}

# Verify GitHub workflow has correct permissions
permissions:
  id-token: write # Must be present
  contents: read
```

### Break-Glass Access

**If Federation Completely Fails**:

1. **GCP**: Use emergency service account key
   ```bash
   gcloud secrets versions access latest \
     --secret="emergency-citadel-deployer-key" \
     --project=nash-security-vault
   ```

2. **AWS**: Use break-glass IAM user
   ```bash
   # Credentials stored in gopass
   gopass show nash-group/aws/break-glass-admin
   aws configure --profile break-glass
   ```

3. **Cloudflare**: Use emergency API token
   ```bash
   gopass show nash-group/cloudflare/emergency-token
   export CLOUDFLARE_API_TOKEN=$(gopass show -o nash-group/cloudflare/emergency-token)
   ```

---

## Verification Checklist

### After Setting Up SAML SSO

- [ ] Guardian can access platform without platform-specific password
- [ ] Guardian's group membership is visible in platform audit logs
- [ ] Session expires after configured duration (e.g., 8 hours for AWS)
- [ ] Logout from Google Workspace also logs out from platform
- [ ] Access is immediately revoked when removed from Google Group

### After Setting Up OIDC

- [ ] GitHub Actions workflow completes without stored credentials
- [ ] Workflow can only run from authorized repository
- [ ] Workflow can only run from authorized branch (e.g., main)
- [ ] Temporary credentials expire after workflow completes
- [ ] Audit logs show repository context (repo name, branch, commit SHA)

### Security Validation

- [ ] No long-lived credentials in GitHub Secrets
- [ ] No service account keys downloaded locally
- [ ] All Google Workspace users have MFA enabled
- [ ] Break-glass credentials stored securely (gopass, offline)
- [ ] Observability Bridge receives audit logs from all platforms

---

## Next Steps

1. **Review** `FEDERATED-IDENTITY-STRATEGY.md` for complete architecture
2. **Review** `GOOGLE-CLOUD-IAM-STRATEGY.md` for GCP-specific implementation
3. **Start Phase 2**: GitHub Federation (SAML + OIDC) - Week 3-4
4. **Create ADR**: Document federated identity decision in the-covenant
5. **Guardian Training**: Conduct SSO training session for all Guardians

---

**Quick Links**:
- Full Strategy: `FEDERATED-IDENTITY-STRATEGY.md`
- GCP IAM Strategy: `GOOGLE-CLOUD-IAM-STRATEGY.md`
- GCP Quick Start: `GOOGLE-CLOUD-IAM-QUICK-START.md`
- Covenant Principles: `the-covenant/PRINCIPLES.md`

---

*"Identity is simple. Make it so."*

**Last Updated**: 2025-11-10
