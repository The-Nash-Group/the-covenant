# Google Workspace Architecture: The Nash Group v1.0

**Version**: 1.0.0
**Created**: 2025-11-21
**Status**: TECHNICAL SPECIFICATION
**Authority**: Covenant Level (2 Watchers + 2 Mentors)
**Guardian Roles**: The Architect (Design), The Watcher (Security)
**Supersedes**: High-level policies in FEDERATED-IDENTITY-STRATEGY.md
**Implementation Repository**: the-citadel (Terraform Google Workspace Provider)

> "One identity, everywhere. This is the concrete architectural blueprint for The Nash Group's Google Workspace configuration—from OU topology to DNS records. Security-first, automation-ready, single-player empire architecture."

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Organizational Unit (OU) Topology](#1-organizational-unit-ou-topology)
3. [Context-Aware Access (CAA) Definitions](#2-context-aware-access-caa-definitions)
4. [Federation Attribute Mapping](#3-federation-attribute-mapping)
5. [Application & API Controls](#4-application--api-controls)
6. [Domain & Email Security Hardening](#5-domain--email-security-hardening)
7. [Implementation Roadmap](#implementation-roadmap)
8. [Terraform Configuration Examples](#terraform-configuration-examples)
9. [Governance & Compliance](#governance--compliance)

---

## Executive Summary

### Architecture Principles

The Nash Group's Google Workspace implementation follows these core tenets:

1. **Zero Trust by Default** (SEC-001): Every access request authenticated, authorized, audited
2. **Least Privilege** (SEC-003): Segregated OUs with minimally scoped policies
3. **Federation-First** (FEDERATED-IDENTITY-STRATEGY): Google Workspace as Single Source of Truth
4. **Security Baseline** (SEC-004): MFA, device trust, session management enforced
5. **Organizational Labeling** (GOV-010): Custom attributes encode clan/tier metadata

### Key Design Decisions

| Decision | Rationale | Implementation |
|----------|-----------|----------------|
| **Separate OU for Admins** | Guardian accounts (guardian@) isolated with stricter policies | `/Guardians` OU with mandatory hardware key MFA |
| **Service Account OU** | Bot/machine identities without passwords, OIDC-only | `/Service-Accounts` OU with API-only access |
| **No Guest/External Users** | Single-player empire, no shared collaboration outside org | Disabled in Admin Console |
| **Context-Aware Access** | Device trust + location verification before access | CAA policies bound to Admin Console, GCP, SAML apps |
| **Custom Attributes for SAML** | AWS/GCP role mapping via Google user attributes | Schema extension: `nash_role`, `nash_tier`, `nash_clan` |

### Implementation Status

| Component | Status | Week Target |
|-----------|--------|-------------|
| OU Topology | 🟡 Design Complete | Week 3 |
| Context-Aware Access | 🟡 Design Complete | Week 4 |
| Federation Attributes | 🟡 Design Complete | Week 3 |
| Application Controls | 🟡 Design Complete | Week 4 |
| Domain Security (DNS) | ✅ Partially Complete | Week 3 |

---

## 1. Organizational Unit (OU) Topology

### Design Philosophy

**Requirement**: Strictly segregated OUs to apply differentiated policies based on identity type.

**Why**: Guardians need YubiKeys, Humans use standard MFA, Service Accounts use OIDC, Guests (none allowed).

### OU Hierarchy

```
thenash.group (Root Domain)
│
├── Guardians (Super Admin Accounts)
│   ├── guardian@thenash.group
│   └── [Future emergency admin accounts]
│
├── Humans (Day-to-Day Work Accounts)
│   ├── Mentors
│   │   ├── jeffrey@thenash.group
│   │   └── [Future mentor accounts]
│   ├── Watchers
│   │   └── [Security-focused accounts]
│   ├── Platform-Clan
│   │   └── [Platform engineering accounts]
│   └── Explorers
│       └── [Experimental/learning accounts]
│
├── Service-Accounts (Machine Identities)
│   ├── citadel-deployer@thenash.group (OIDC GitHub Actions)
│   ├── nexus-deployer@thenash.group
│   ├── observability-bridge@thenash.group
│   └── [Future service accounts]
│
└── Suspended (Deactivated Accounts)
    └── [Archived/disabled accounts]
```

### OU-Specific Policies

#### `/Guardians` OU

**Purpose**: Super Admin accounts for Google Workspace and organizational management.

**Policy Settings**:
```yaml
authentication:
  password_policy:
    min_length: 16
    require_special_chars: true
    require_numbers: true
    expiration: 90 days
    history: 24 passwords

  multi_factor_authentication:
    enforcement: MANDATORY
    allowed_methods:
      - Security Key (Hardware - YubiKey, Titan Key)
      - Google Authenticator App (TOTP)
    disallowed_methods:
      - SMS (too weak for admin)
      - Backup codes (only for emergency)

  session_management:
    web_session_duration: 4 hours
    reauth_for_sensitive_actions: true
    concurrent_sessions: 2 maximum

access_controls:
  admin_console: FULL_ACCESS
  google_cloud_console: FULL_ACCESS
  super_admin_privileges: true

context_aware_access:
  required_access_levels:
    - "Admin_Workstation" (see CAA section)
    - "Trusted_Device"

device_management:
  require_device_approval: true
  require_disk_encryption: true
  allow_unmanaged_devices: false

advanced_protection:
  enabled: true  # Google Advanced Protection Program
```

**Terraform Configuration**:
```hcl
# the-citadel/terraform/google-workspace/org-units.tf
resource "googleworkspace_org_unit" "guardians" {
  name        = "Guardians"
  parent_org_unit_path = "/"
  description = "Super Admin accounts - strictest security policies"

  # Will be referenced by user resources
}

# User in Guardians OU
resource "googleworkspace_user" "guardian" {
  primary_email = "guardian@thenash.group"
  name {
    family_name = "Guardian"
    given_name  = "Root"
  }

  org_unit_path = googleworkspace_org_unit.guardians.id

  # Custom attributes for federation (see section 3)
  custom_schemas = [{
    schema_name = "Nash_Group_Federation"
    field_values = {
      "nash_role"     = "org-owner"
      "nash_tier"     = "core"
      "nash_clan"     = "watchers"
      "aws_role_arn"  = "arn:aws:iam::*:role/OrganizationAccountAccessRole"
      "session_duration" = "14400"  # 4 hours in seconds
    }
  }]

  recovery_email = var.guardian_recovery_email  # From secret
  recovery_phone = var.guardian_recovery_phone

  # Force password change on first login
  change_password_at_next_login = false  # Already configured
}
```

#### `/Humans/Mentors` OU

**Purpose**: Day-to-day work accounts for Mentor clan members (infrastructure experts).

**Policy Settings**:
```yaml
authentication:
  password_policy:
    min_length: 14
    require_special_chars: true
    require_numbers: true
    expiration: 180 days
    history: 12 passwords

  multi_factor_authentication:
    enforcement: MANDATORY
    allowed_methods:
      - Security Key (Hardware - recommended)
      - Google Authenticator App (TOTP)
      - Google Prompt (push notification)
    disallowed_methods:
      - SMS (phishing risk)

  session_management:
    web_session_duration: 8 hours
    reauth_for_sensitive_actions: true
    concurrent_sessions: 3 maximum

access_controls:
  admin_console: VIEW_ONLY (audit purposes)
  google_cloud_console: EDITOR_ACCESS (via IAM roles)
  super_admin_privileges: false

context_aware_access:
  required_access_levels:
    - "Trusted_Device"

device_management:
  require_device_approval: true
  require_disk_encryption: true
  allow_unmanaged_devices: false  # Personal devices must be managed
```

**Terraform Configuration**:
```hcl
resource "googleworkspace_org_unit" "mentors" {
  name        = "Mentors"
  parent_org_unit_path = googleworkspace_org_unit.humans.id
  description = "Mentor clan - infrastructure experts with elevated privileges"
}

resource "googleworkspace_user" "jeffrey" {
  primary_email = "jeffrey@thenash.group"
  name {
    family_name = "Johnson"
    given_name  = "Jeffrey"
  }

  org_unit_path = googleworkspace_org_unit.mentors.id

  custom_schemas = [{
    schema_name = "Nash_Group_Federation"
    field_values = {
      "nash_role"     = "mentor"
      "nash_tier"     = "platform"
      "nash_clan"     = "mentors"
      "aws_role_arn"  = "arn:aws:iam::*:role/AWS-Mentor-PowerUser"
      "session_duration" = "28800"  # 8 hours
    }
  }]
}
```

#### `/Service-Accounts` OU

**Purpose**: Machine identities for CI/CD, automation, and service-to-service auth.

**Policy Settings**:
```yaml
authentication:
  password_policy:
    enforcement: NONE  # Service accounts do not use passwords

  multi_factor_authentication:
    enforcement: N/A  # Use Workload Identity Federation (OIDC) instead

  session_management:
    web_session_duration: N/A
    interactive_login: DISABLED

access_controls:
  admin_console: NO_ACCESS
  google_cloud_console: API_ONLY
  super_admin_privileges: false

  api_access:
    allowed_scopes:
      - https://www.googleapis.com/auth/cloud-platform
      - https://www.googleapis.com/auth/iam
      - https://www.googleapis.com/auth/admin.directory.user.readonly

context_aware_access:
  required_access_levels:
    - "Service_Account_OIDC" (validates GitHub Actions token)

device_management:
  require_device_approval: false
  allow_unmanaged_devices: true  # Runs in GitHub Actions runners
```

**Terraform Configuration**:
```hcl
resource "googleworkspace_org_unit" "service_accounts" {
  name        = "Service-Accounts"
  parent_org_unit_path = "/"
  description = "Machine identities - OIDC-only, no passwords"
}

# Note: Service accounts are GCP Service Accounts, not Google Workspace users
# This OU may remain empty for Workspace, but exists for policy segregation
# Actual service accounts are created in GCP:

# In the-citadel/terraform/gcp/service-accounts.tf
resource "google_service_account" "citadel_deployer" {
  account_id   = "citadel-deployer"
  display_name = "Citadel Deployer (GitHub Actions)"
  description  = "Service account for the-citadel Terraform deployments via OIDC"
  project      = var.gcp_project_id
}
```

#### `/Suspended` OU

**Purpose**: Archived/disabled accounts (retention for audit, immediate revocation).

**Policy Settings**:
```yaml
authentication:
  account_status: SUSPENDED
  login_disabled: true

access_controls:
  all_access: REVOKED

retention:
  duration: 365 days  # 1 year retention for audit
  auto_delete_after: true
```

---

## 2. Context-Aware Access (CAA) Definitions

### Overview

Context-Aware Access enforces Zero Trust by evaluating **who**, **what device**, **where**, and **when** before granting access.

**Requirement** (SEC-001): Authenticate every request, authorize every action, audit every access.

### Access Level Architecture

Access Levels are **logical conditions** evaluated at access time. They do not grant permissions—they gate existing permissions.

```
User Permission + Access Level = Actual Access

Example:
  jeffrey@thenash.group HAS Editor role on GCP Project
  + Access Level "Trusted_Device" evaluates TRUE
  = Access GRANTED

  guardian@thenash.group HAS Super Admin on Google Workspace
  + Access Level "Admin_Workstation" evaluates FALSE (untrusted device)
  = Access DENIED (redirect to "Access Blocked" page)
```

### Access Level Definitions

#### Access Level 1: `Trusted_Device`

**Purpose**: Standard access for day-to-day work from managed devices.

**Conditions**:
```yaml
access_level_id: "trusted_device"
description: "Managed device with full disk encryption"

conditions:
  device_policy:
    require_corp_owned: false  # Allow BYOD if managed
    allowed_device_management_levels:
      - "COMPLETE"  # Fully managed by Google Workspace
    require_screen_lock: true

  os_constraints:
    minimum_version:
      - os_type: "DESKTOP_MAC"
        minimum: "14.0"  # macOS Sonoma
      - os_type: "DESKTOP_WINDOWS"
        minimum: "10.0.19041"  # Windows 10 20H1
      - os_type: "DESKTOP_LINUX"
        minimum: "5.4"  # Ubuntu 20.04 LTS kernel
      - os_type: "DESKTOP_CHROME_OS"
        minimum: "latest"

  encryption:
    require_disk_encryption: true

  ip_subnetworks:
    # Allow from any location (remote-first)
    # If restricting, add trusted networks:
    # - "203.0.113.0/24"  # Office network
    # - "198.51.100.0/24"  # Home office
```

**Terraform Configuration**:
```hcl
# the-citadel/terraform/google-workspace/access-levels.tf
resource "google_access_context_manager_access_level" "trusted_device" {
  parent = "accessPolicies/${var.access_policy_id}"
  name   = "accessPolicies/${var.access_policy_id}/accessLevels/trusted_device"
  title  = "Trusted Device"

  basic {
    conditions {
      device_policy {
        require_screen_lock = true

        os_constraints {
          os_type        = "DESKTOP_MAC"
          minimum_version = "14.0"
        }
        os_constraints {
          os_type        = "DESKTOP_WINDOWS"
          minimum_version = "10.0.19041"
        }
        os_constraints {
          os_type        = "DESKTOP_LINUX"
          minimum_version = "5.4"
        }

        require_corp_owned = false  # Allow managed BYOD
      }
    }
  }
}
```

**Application Binding**:
- Google Workspace Apps (Gmail, Drive, Calendar, Docs)
- GCP Console (Editor/Viewer roles)
- SAML Apps (GitHub, AWS via SSO)

#### Access Level 2: `Admin_Workstation`

**Purpose**: Elevated security for Super Admin operations.

**Conditions**:
```yaml
access_level_id: "admin_workstation"
description: "Hardened workstation for Guardian accounts"

conditions:
  device_policy:
    require_corp_owned: true  # Must be organization-managed
    allowed_device_management_levels:
      - "COMPLETE"
    require_screen_lock: true

  os_constraints:
    minimum_version:
      - os_type: "DESKTOP_MAC"
        minimum: "15.0"  # macOS Sequoia (latest)

  encryption:
    require_disk_encryption: true

  ip_subnetworks:
    # Restrict to trusted locations
    - "203.0.113.10/32"  # Guardian workstation static IP
    # OR use VPN IP range:
    # - "198.51.100.0/24"  # VPN subnet

  # Additional: Certificate-based device verification
  device_attributes:
    require_verified_chrome_os: false
    require_admin_approval_apps: true
```

**Terraform Configuration**:
```hcl
resource "google_access_context_manager_access_level" "admin_workstation" {
  parent = "accessPolicies/${var.access_policy_id}"
  name   = "accessPolicies/${var.access_policy_id}/accessLevels/admin_workstation"
  title  = "Admin Workstation"

  basic {
    combining_function = "AND"  # All conditions must be true

    conditions {
      device_policy {
        require_corp_owned  = true
        require_screen_lock = true

        os_constraints {
          os_type        = "DESKTOP_MAC"
          minimum_version = "15.0"
        }
      }

      ip_subnetworks = [
        "203.0.113.10/32"  # Guardian workstation IP
      ]
    }
  }
}
```

**Application Binding**:
- Google Workspace Admin Console
- GCP IAM & Admin (Owner role)
- Emergency break-glass operations

#### Access Level 3: `Emergency_Break_Glass`

**Purpose**: Temporary bypass for critical incidents when normal auth fails.

**Conditions**:
```yaml
access_level_id: "emergency_break_glass"
description: "Temporary bypass for incidents - heavily logged"

conditions:
  # Relaxed conditions, but with enhanced monitoring
  device_policy:
    require_corp_owned: false
    allowed_device_management_levels:
      - "COMPLETE"
      - "BASIC"  # Allow basic managed devices
      - "UNSPECIFIED"  # Allow unmanaged in emergency
    require_screen_lock: false

  ip_subnetworks:
    # Allow from any location

  time_based:
    # Only available during declared incidents
    # Manually activated by Watchers
    # Auto-expires after 4 hours
```

**Activation Process**:
1. **Incident Declaration**: Watcher declares emergency via Admin Console
2. **Manual Activation**: Watcher manually enables `Emergency_Break_Glass` access level
3. **Enhanced Logging**: All actions logged to separate audit sink
4. **Auto-Expiration**: Access level auto-disables after 4 hours
5. **Post-Incident Review**: Mandatory review within 24 hours (GOV-003)

**Terraform Configuration**:
```hcl
resource "google_access_context_manager_access_level" "emergency_break_glass" {
  parent = "accessPolicies/${var.access_policy_id}"
  name   = "accessPolicies/${var.access_policy_id}/accessLevels/emergency_break_glass"
  title  = "Emergency Break-Glass"

  basic {
    conditions {
      # Very permissive - any device, any location
      # Relies on MFA and enhanced logging
      device_policy {
        require_screen_lock = false
      }
    }
  }

  # Lifecycle: Manually managed, not via Terraform for emergency flexibility
  lifecycle {
    prevent_destroy = true
  }
}
```

**Application Binding**:
- Google Workspace Admin Console (read-only during incident)
- GCP Console (emergency IAM access)
- Break-glass service accounts (activated manually)

#### Access Level 4: `Service_Account_OIDC`

**Purpose**: Validate machine identities via OIDC tokens (GitHub Actions).

**Conditions**:
```yaml
access_level_id: "service_account_oidc"
description: "OIDC workload identity for CI/CD pipelines"

conditions:
  # No device policy (runs on GitHub Actions runners)
  # Instead, validate OIDC token claims

  oidc_validation:
    issuer: "https://token.actions.githubusercontent.com"
    audience: "https://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/providers/${PROVIDER_ID}"

    required_claims:
      - claim: "repository"
        values:
          - "The-Nash-Group/the-citadel"
          - "The-Nash-Group/the-nexus"
      - claim: "ref"
        values:
          - "refs/heads/main"  # Only main branch
      - claim: "event_name"
        values:
          - "push"
          - "workflow_dispatch"

  ip_subnetworks:
    # GitHub Actions IP ranges (updated regularly)
    - "140.82.112.0/20"
    - "143.55.64.0/20"
    # See: https://api.github.com/meta
```

**Note**: This is enforced at GCP Workload Identity level, not Google Workspace CAA (different system).

### Access Level Application Matrix

| Access Level | Google Workspace Admin Console | GCP Console | SAML Apps (AWS, GitHub) | API Access |
|--------------|-------------------------------|-------------|------------------------|------------|
| **Trusted_Device** | ✅ Standard users | ✅ Editor/Viewer | ✅ All users | ✅ Standard API |
| **Admin_Workstation** | ✅ Super Admin only | ✅ Owner/Admin | ✅ Admin SAML | ✅ Admin API |
| **Emergency_Break_Glass** | ⚠️ Read-only | ⚠️ Emergency access | ❌ Not bound | ⚠️ Limited API |
| **Service_Account_OIDC** | ❌ Not applicable | ✅ Service Accounts | ❌ Not applicable | ✅ CI/CD API |

---

## 3. Federation Attribute Mapping

### Overview

To support AWS IAM Identity Center (SAML SSO) and GCP Workload Identity (OIDC), we need **custom user attributes** that map to roles/permissions on target platforms.

**Requirement**: Google Groups alone are insufficient—we need per-user attributes for:
- AWS Role ARN assignment
- Session duration control
- Clan/tier metadata (GOV-010)
- Conditional access policies

### Custom User Schema Design

Google Workspace allows custom attributes via **Schema Extensions**. We'll create the `Nash_Group_Federation` schema.

#### Schema Definition: `Nash_Group_Federation`

```yaml
schema_name: "Nash_Group_Federation"
display_name: "Nash Group Federation Attributes"
description: "Custom attributes for SAML/OIDC federation and organizational metadata"

fields:
  - field_name: "nash_role"
    field_type: "STRING"
    display_name: "Nash Role"
    description: "User's primary role (mentor, watcher, platform, explorer)"
    required: true
    indexed: true  # Enable fast queries
    multi_valued: false
    valid_values:
      - "org-owner"
      - "mentor"
      - "watcher"
      - "platform"
      - "explorer"

  - field_name: "nash_tier"
    field_type: "STRING"
    display_name: "Nash Tier"
    description: "Resource access tier (core, platform, application, experimental)"
    required: true
    indexed: true
    multi_valued: false
    valid_values:
      - "core"
      - "platform"
      - "application"
      - "experimental"

  - field_name: "nash_clan"
    field_type: "STRING"
    display_name: "Nash Clan"
    description: "Organizational clan membership"
    required: true
    indexed: true
    multi_valued: false
    valid_values:
      - "watchers"
      - "mentors"
      - "platform-clan"
      - "immortals"

  - field_name: "aws_role_arn"
    field_type: "STRING"
    display_name: "AWS IAM Role ARN"
    description: "AWS IAM role to assume via SAML (supports wildcards)"
    required: false
    multi_valued: true  # Users may have multiple AWS roles
    example: "arn:aws:iam::*:role/AWS-Mentor-PowerUser"

  - field_name: "gcp_service_account"
    field_type: "STRING"
    display_name: "GCP Service Account Email"
    description: "GCP service account for impersonation (Workload Identity)"
    required: false
    multi_valued: false
    example: "citadel-deployer@nash-personal-prod.iam.gserviceaccount.com"

  - field_name: "session_duration"
    field_type: "INT64"
    display_name: "Session Duration (seconds)"
    description: "Maximum session duration for federated access"
    required: false
    default: "28800"  # 8 hours
    min_value: 3600    # 1 hour minimum
    max_value: 43200   # 12 hours maximum

  - field_name: "github_teams"
    field_type: "STRING"
    display_name: "GitHub Teams"
    description: "GitHub team memberships (synced via SAML)"
    required: false
    multi_valued: true
    example: "@the-nash-group/mentors"

  - field_name: "cloudflare_access_groups"
    field_type: "STRING"
    display_name: "Cloudflare Access Groups"
    description: "Cloudflare Access group memberships"
    required: false
    multi_valued: true
    example: "cf-zone-admin"
```

#### Terraform Configuration

```hcl
# the-citadel/terraform/google-workspace/custom-schema.tf
resource "googleworkspace_schema" "nash_group_federation" {
  schema_name  = "Nash_Group_Federation"
  display_name = "Nash Group Federation Attributes"

  fields {
    field_name = "nash_role"
    field_type = "STRING"
    display_name = "Nash Role"
    indexed = true
    multi_valued = false
  }

  fields {
    field_name = "nash_tier"
    field_type = "STRING"
    display_name = "Nash Tier"
    indexed = true
    multi_valued = false
  }

  fields {
    field_name = "nash_clan"
    field_type = "STRING"
    display_name = "Nash Clan"
    indexed = true
    multi_valued = false
  }

  fields {
    field_name = "aws_role_arn"
    field_type = "STRING"
    display_name = "AWS IAM Role ARN"
    multi_valued = true
  }

  fields {
    field_name = "gcp_service_account"
    field_type = "STRING"
    display_name = "GCP Service Account Email"
    multi_valued = false
  }

  fields {
    field_name = "session_duration"
    field_type = "INT64"
    display_name = "Session Duration (seconds)"
    numeric_indexing_spec {
      min_value = 3600
      max_value = 43200
    }
  }

  fields {
    field_name = "github_teams"
    field_type = "STRING"
    display_name = "GitHub Teams"
    multi_valued = true
  }

  fields {
    field_name = "cloudflare_access_groups"
    field_type = "STRING"
    display_name = "Cloudflare Access Groups"
    multi_valued = true
  }
}
```

### SAML Attribute Mapping for AWS IAM Identity Center

When a user logs into AWS via SAML, Google Workspace sends a SAML assertion with these attributes.

#### SAML Assertion Structure

```xml
<saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
  <saml:Subject>
    <saml:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">
      jeffrey@thenash.group
    </saml:NameID>
  </saml:Subject>

  <saml:AttributeStatement>
    <!-- Standard attributes -->
    <saml:Attribute Name="email">
      <saml:AttributeValue>jeffrey@thenash.group</saml:AttributeValue>
    </saml:Attribute>

    <saml:Attribute Name="displayName">
      <saml:AttributeValue>Jeffrey Johnson</saml:AttributeValue>
    </saml:Attribute>

    <!-- Google Groups (for role mapping) -->
    <saml:Attribute Name="groups">
      <saml:AttributeValue>nash-group-mentors@thenash.group</saml:AttributeValue>
      <saml:AttributeValue>nash-group-watchers@thenash.group</saml:AttributeValue>
    </saml:Attribute>

    <!-- Custom attributes from Nash_Group_Federation schema -->
    <saml:Attribute Name="https://aws.amazon.com/SAML/Attributes/Role">
      <saml:AttributeValue>arn:aws:iam::*:role/AWS-Mentor-PowerUser,arn:aws:iam::*:saml-provider/GoogleWorkspace</saml:AttributeValue>
    </saml:Attribute>

    <saml:Attribute Name="https://aws.amazon.com/SAML/Attributes/RoleSessionName">
      <saml:AttributeValue>jeffrey@thenash.group</saml:AttributeValue>
    </saml:Attribute>

    <saml:Attribute Name="https://aws.amazon.com/SAML/Attributes/SessionDuration">
      <saml:AttributeValue>28800</saml:AttributeValue>
    </saml:Attribute>

    <!-- Nash Group custom attributes for audit/governance -->
    <saml:Attribute Name="nash_role">
      <saml:AttributeValue>mentor</saml:AttributeValue>
    </saml:Attribute>

    <saml:Attribute Name="nash_tier">
      <saml:AttributeValue>platform</saml:AttributeValue>
    </saml:Attribute>

    <saml:Attribute Name="nash_clan">
      <saml:AttributeValue>mentors</saml:AttributeValue>
    </saml:Attribute>
  </saml:AttributeStatement>
</saml:Assertion>
```

#### Google Workspace SAML App Configuration

In Google Workspace Admin Console → Apps → SAML Apps → AWS IAM Identity Center:

**Attribute Mapping Table**:

| Application Attribute | Google Directory Attribute | Transform |
|-----------------------|---------------------------|-----------|
| `email` | Primary Email | - |
| `displayName` | Full Name | - |
| `groups` | Group Membership (full path) | - |
| `https://aws.amazon.com/SAML/Attributes/Role` | Custom: `Nash_Group_Federation.aws_role_arn` + `,arn:aws:iam::*:saml-provider/GoogleWorkspace` | Concatenate |
| `https://aws.amazon.com/SAML/Attributes/RoleSessionName` | Primary Email | - |
| `https://aws.amazon.com/SAML/Attributes/SessionDuration` | Custom: `Nash_Group_Federation.session_duration` | - |
| `nash_role` | Custom: `Nash_Group_Federation.nash_role` | - |
| `nash_tier` | Custom: `Nash_Group_Federation.nash_tier` | - |
| `nash_clan` | Custom: `Nash_Group_Federation.nash_clan` | - |

**Note**: The `Role` attribute must be in format: `<RoleARN>,<ProviderARN>`. Google Workspace will concatenate the custom attribute with the provider ARN.

### User Attribute Examples

#### Example 1: guardian@thenash.group

```yaml
user: guardian@thenash.group
org_unit: /Guardians

custom_attributes:
  Nash_Group_Federation:
    nash_role: "org-owner"
    nash_tier: "core"
    nash_clan: "watchers"
    aws_role_arn:
      - "arn:aws:iam::*:role/OrganizationAccountAccessRole"
      - "arn:aws:iam::*:role/AWS-Owner-Admin"
    gcp_service_account: null  # Not applicable for humans
    session_duration: 14400  # 4 hours (shorter for admin)
    github_teams:
      - "@the-nash-group/owners"
    cloudflare_access_groups:
      - "cf-super-admin"
```

#### Example 2: jeffrey@thenash.group

```yaml
user: jeffrey@thenash.group
org_unit: /Humans/Mentors

custom_attributes:
  Nash_Group_Federation:
    nash_role: "mentor"
    nash_tier: "platform"
    nash_clan: "mentors"
    aws_role_arn:
      - "arn:aws:iam::*:role/AWS-Mentor-PowerUser"
    gcp_service_account: null
    session_duration: 28800  # 8 hours
    github_teams:
      - "@the-nash-group/mentors"
      - "@the-nash-group/watchers"
    cloudflare_access_groups:
      - "cf-zone-admin"
```

#### Example 3: Service Account (citadel-deployer)

```yaml
# Note: This is a GCP Service Account, not a Google Workspace user
# Attributes are set via Workload Identity binding, not Workspace schema

gcp_service_account: citadel-deployer@nash-personal-prod.iam.gserviceaccount.com

workload_identity_attributes:
  repository: "The-Nash-Group/the-citadel"
  ref: "refs/heads/main"
  nash_tier: "core"  # Custom claim in OIDC token
  nash_clan: "mentors"
```

---

## 4. Application & API Controls

### Overview

**Requirement**: Control which applications can access Google Workspace data and how users interact with those apps.

**Goals**:
1. Block untrusted third-party apps by default
2. Allowlist specific apps needed for operations
3. Control OAuth scopes granted to apps
4. Enforce session duration for Google Cloud Console specifically

### OAuth Third-Party App Access Policy

#### Default Policy: **Block All Third-Party Apps**

**Rationale** (SEC-003): Least privilege—only explicitly approved apps can access organizational data.

**Configuration**:
```yaml
oauth_policy:
  default_action: DENY
  user_can_authorize_apps: false  # Users cannot consent to apps
  admin_approval_required: true

  # Users cannot install Chrome Web Store apps without approval
  chrome_webstore_policy: WHITELIST_ONLY

  # Users cannot install Google Workspace Marketplace apps
  marketplace_policy: WHITELIST_ONLY
```

**Terraform Configuration**:
```hcl
# the-citadel/terraform/google-workspace/oauth-policy.tf
resource "googleworkspace_api_client_access" "default_deny" {
  # This is managed via Admin Console -> Security -> API Controls -> Manage Third-Party App Access
  # Terraform support limited—use gcloud or Admin Console
}

# Alternative: Use gcloud commands in Terraform null_resource
resource "null_resource" "oauth_default_deny" {
  provisioner "local-exec" {
    command = <<-EOT
      gcloud workspace-admin apps configure \
        --customer-id=${var.customer_id} \
        --allow-user-consent=false \
        --default-action=DENY
    EOT
  }
}
```

#### Allowlisted Third-Party Apps

**Approved Apps**:

| App Name | OAuth Client ID | Scopes Granted | Justification |
|----------|----------------|----------------|---------------|
| **GitHub (SAML SSO)** | (Configured via SAML, not OAuth) | N/A | Source control, CI/CD |
| **Terraform Cloud** | `terraform-cloud-client-id` | `https://www.googleapis.com/auth/admin.directory.user.readonly` | Infrastructure state management |
| **Observability Bridge** | `observability-bridge-client-id` | `https://www.googleapis.com/auth/admin.reports.audit.readonly` | Audit log aggregation |

**Terraform Configuration**:
```hcl
resource "googleworkspace_api_client_access" "terraform_cloud" {
  client_id = var.terraform_cloud_oauth_client_id
  scopes = [
    "https://www.googleapis.com/auth/admin.directory.user.readonly",
    "https://www.googleapis.com/auth/admin.directory.group.readonly"
  ]

  # Apply to entire domain
  domain_wide_delegation = true
}

resource "googleworkspace_api_client_access" "observability_bridge" {
  client_id = var.observability_bridge_oauth_client_id
  scopes = [
    "https://www.googleapis.com/auth/admin.reports.audit.readonly"
  ]

  domain_wide_delegation = true
}
```

### Google Cloud Console Session Control

**Requirement**: Differentiate session durations between Google Workspace (Gmail, Drive) and Google Cloud Console (GCP management).

**Session Duration Policy**:

| User Type | Google Workspace Apps | Google Cloud Console | Re-auth Required |
|-----------|-----------------------|---------------------|------------------|
| **Guardians** | 4 hours | 2 hours | Every sensitive action |
| **Mentors** | 8 hours | 4 hours | IAM changes only |
| **Platform Clan** | 8 hours | 8 hours | IAM changes only |
| **Explorers** | 8 hours | 8 hours | IAM changes only |

**Configuration**:
```yaml
session_management:
  google_workspace_apps:
    web_session_duration:
      guardians: 4 hours
      mentors: 8 hours
      platform_clan: 8 hours
      explorers: 8 hours

  google_cloud_console:
    web_session_duration:
      guardians: 2 hours
      mentors: 4 hours
      platform_clan: 8 hours
      explorers: 8 hours

    re_authentication_required:
      - IAM policy changes
      - Service account key creation
      - Billing account modifications
      - Organization policy changes
```

**Implementation Notes**:
- Google Workspace session duration is per-OU (configured in Admin Console → Security → Session Management)
- Google Cloud Console session duration is controlled via **Context-Aware Access** bindings
- Re-authentication is enforced via GCP IAM Conditions on sensitive operations

**Terraform Configuration**:
```hcl
# Google Workspace session duration (per OU)
# Managed via Admin Console, not Terraform

# GCP IAM Condition for re-auth on sensitive actions
resource "google_organization_iam_binding" "iam_admin_reauth" {
  org_id = var.gcp_organization_id
  role   = "roles/iam.securityAdmin"

  members = [
    "user:guardian@thenash.group",
    "user:jeffrey@thenash.group"
  ]

  condition {
    title       = "Require Re-authentication for IAM Changes"
    description = "Forces re-authentication when modifying IAM policies"
    expression  = <<-EOT
      request.time < timestamp(request.auth.access_token_issued_at) + duration("7200s")
    EOT
    # Token must be less than 2 hours old to modify IAM
  }
}
```

### API Access Controls

**Requirement**: Control which APIs are enabled for the organization.

**Enabled APIs**:
```yaml
enabled_apis:
  # Core Google Workspace APIs
  - admin.googleapis.com  # Admin SDK
  - drive.googleapis.com  # Google Drive
  - gmail.googleapis.com  # Gmail
  - calendar-json.googleapis.com  # Calendar

  # Google Cloud APIs (for GCP integration)
  - cloudresourcemanager.googleapis.com  # Resource Manager
  - iam.googleapis.com  # IAM
  - iamcredentials.googleapis.com  # Workload Identity
  - sts.googleapis.com  # Security Token Service
  - compute.googleapis.com  # Compute Engine
  - storage.googleapis.com  # Cloud Storage
  - logging.googleapis.com  # Cloud Logging
  - monitoring.googleapis.com  # Cloud Monitoring

  # Security & Compliance
  - securitycenter.googleapis.com  # Security Command Center
  - accesscontextmanager.googleapis.com  # Context-Aware Access

disabled_apis:
  # Block unnecessary APIs
  - youtube.googleapis.com  # Not used
  - maps.googleapis.com  # Not used
  - analytics.googleapis.com  # Not used
```

**Terraform Configuration**:
```hcl
# Enable required APIs for GCP project
resource "google_project_service" "required_apis" {
  for_each = toset([
    "admin.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
    "compute.googleapis.com",
    "storage.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "accesscontextmanager.googleapis.com"
  ])

  project = var.gcp_project_id
  service = each.key

  disable_on_destroy = false
}
```

---

## 5. Domain & Email Security Hardening

### Overview

**Requirement**: Harden `thenash.group` domain with industry-standard email security protocols.

**Goals**:
1. **DMARC**: Reject spoofed emails (p=reject)
2. **MTA-STS**: Enforce TLS for email transport
3. **DNSSEC**: Sign DNS records for authenticity
4. **BIMI**: (Optional) Display brand logo in supported mail clients

### DNS Record Strategy

**Domain**: `thenash.group`
**DNS Provider**: Cloudflare
**Integration**: Cloudflare + Google Workspace

#### Current DNS Configuration

```
thenash.group (Root Domain)
├── Cloudflare DNS Management
├── DNSSEC: Enabled (signed by Cloudflare)
└── Google Workspace MX Records: Configured
```

### 5.1 SPF (Sender Policy Framework)

**Purpose**: Specify which mail servers can send email on behalf of `thenash.group`.

**Record Type**: `TXT`
**Record Name**: `@` (root domain)
**Record Value**:
```
v=spf1 include:_spf.google.com ~all
```

**Explanation**:
- `v=spf1`: SPF version 1
- `include:_spf.google.com`: Allow Google Workspace mail servers
- `~all`: Soft fail for other servers (will move to `-all` after testing)

**Terraform Configuration**:
```hcl
# the-citadel/terraform/cloudflare/dns-email-security.tf
resource "cloudflare_record" "spf" {
  zone_id = var.cloudflare_zone_id
  name    = "@"
  type    = "TXT"
  value   = "v=spf1 include:_spf.google.com ~all"
  ttl     = 3600

  comment = "SPF record - Allow Google Workspace mail servers"
}
```

**Testing**:
```bash
dig +short TXT thenash.group | grep spf
# Expected: "v=spf1 include:_spf.google.com ~all"
```

### 5.2 DKIM (DomainKeys Identified Mail)

**Purpose**: Cryptographically sign outgoing emails to prove they came from `thenash.group`.

**Record Type**: `TXT`
**Record Name**: `google._domainkey.thenash.group`
**Record Value**: (Generated by Google Workspace Admin Console)

**Steps to Generate**:
1. Google Workspace Admin Console → Apps → Google Workspace → Gmail → Authenticate email
2. Click "Generate new record"
3. Copy DKIM TXT record value

**Example Record Value**:
```
v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
```

**Terraform Configuration**:
```hcl
resource "cloudflare_record" "dkim_google" {
  zone_id = var.cloudflare_zone_id
  name    = "google._domainkey"
  type    = "TXT"
  value   = var.google_dkim_record_value  # From Google Workspace
  ttl     = 3600

  comment = "DKIM record for Google Workspace email signing"
}
```

**Testing**:
```bash
dig +short TXT google._domainkey.thenash.group
# Should return DKIM public key
```

### 5.3 DMARC (Domain-based Message Authentication)

**Purpose**: Tell receiving mail servers what to do with emails that fail SPF/DKIM checks.

**Record Type**: `TXT`
**Record Name**: `_dmarc.thenash.group`
**Record Value** (Final Production Configuration):
```
v=DMARC1; p=reject; sp=reject; rua=mailto:dmarc-reports@thenash.group; ruf=mailto:dmarc-forensics@thenash.group; fo=1; adkim=s; aspf=s; pct=100
```

**Explanation**:
- `v=DMARC1`: DMARC version 1
- `p=reject`: **Reject** emails that fail authentication (strictest policy)
- `sp=reject`: Same policy for subdomains
- `rua=mailto:dmarc-reports@thenash.group`: Aggregate reports sent to this address
- `ruf=mailto:dmarc-forensics@thenash.group`: Forensic (detailed) reports
- `fo=1`: Send forensic reports if any check fails
- `adkim=s`: **Strict** DKIM alignment (domain must match exactly)
- `aspf=s`: **Strict** SPF alignment
- `pct=100`: Apply policy to 100% of emails

**Phased Rollout** (Recommended):

**Phase 1: Monitoring (Week 1-2)**
```
v=DMARC1; p=none; rua=mailto:dmarc-reports@thenash.group; pct=100
```
- Collect data, no enforcement

**Phase 2: Quarantine (Week 3-4)**
```
v=DMARC1; p=quarantine; sp=quarantine; rua=mailto:dmarc-reports@thenash.group; pct=100
```
- Failed emails go to spam

**Phase 3: Reject (Week 5+)**
```
v=DMARC1; p=reject; sp=reject; rua=mailto:dmarc-reports@thenash.group; ruf=mailto:dmarc-forensics@thenash.group; fo=1; adkim=s; aspf=s; pct=100
```
- Failed emails rejected outright

**Terraform Configuration**:
```hcl
resource "cloudflare_record" "dmarc" {
  zone_id = var.cloudflare_zone_id
  name    = "_dmarc"
  type    = "TXT"
  value   = var.dmarc_policy  # Variable to support phased rollout
  ttl     = 3600

  comment = "DMARC policy - Email authentication enforcement"
}

# Variable definition (the-citadel/terraform/cloudflare/variables.tf)
variable "dmarc_policy" {
  description = "DMARC policy (none/quarantine/reject)"
  type        = string
  default     = "v=DMARC1; p=reject; sp=reject; rua=mailto:dmarc-reports@thenash.group; ruf=mailto:dmarc-forensics@thenash.group; fo=1; adkim=s; aspf=s; pct=100"
}
```

**Testing**:
```bash
dig +short TXT _dmarc.thenash.group
# Expected: "v=DMARC1; p=reject; ..."
```

**DMARC Report Processing**:
- Create `dmarc-reports@thenash.group` mailbox
- Use service like [DMARC Analyzer](https://www.dmarcanalyzer.com/) or [PostmarkApp](https://dmarc.postmarkapp.com/) to parse reports
- Integrate with Observability Bridge for centralized monitoring

### 5.4 MTA-STS (Mail Transfer Agent Strict Transport Security)

**Purpose**: Force mail servers to use TLS when sending email to `thenash.group`.

**Requirements**:
1. DNS TXT record announcing MTA-STS support
2. HTTPS-hosted policy file at `https://mta-sts.thenash.group/.well-known/mta-sts.txt`

#### Step 1: DNS TXT Record

**Record Type**: `TXT`
**Record Name**: `_mta-sts.thenash.group`
**Record Value**:
```
v=STSv1; id=20251121T000000
```

**Explanation**:
- `v=STSv1`: MTA-STS version 1
- `id=20251121T000000`: Policy ID (timestamp of last update)

**Terraform Configuration**:
```hcl
resource "cloudflare_record" "mta_sts_txt" {
  zone_id = var.cloudflare_zone_id
  name    = "_mta-sts"
  type    = "TXT"
  value   = "v=STSv1; id=${var.mta_sts_policy_id}"
  ttl     = 3600

  comment = "MTA-STS DNS record - Enforce TLS for email"
}

variable "mta_sts_policy_id" {
  description = "MTA-STS policy version ID (update when policy changes)"
  type        = string
  default     = "20251121T000000"
}
```

#### Step 2: Host Policy File

**File Location**: `https://mta-sts.thenash.group/.well-known/mta-sts.txt`

**Policy File Content**:
```
version: STSv1
mode: enforce
mx: smtp.google.com
mx: *.smtp.google.com
max_age: 86400
```

**Explanation**:
- `version: STSv1`: Policy version
- `mode: enforce`: **Enforce** TLS (fail delivery if TLS not available)
- `mx: smtp.google.com`: Google Workspace MX servers
- `mx: *.smtp.google.com`: Wildcard for regional MX servers
- `max_age: 86400`: Cache policy for 24 hours (86400 seconds)

**Hosting Options**:

**Option 1: Cloudflare Workers**
```hcl
# the-citadel/terraform/cloudflare/mta-sts-worker.tf
resource "cloudflare_worker_script" "mta_sts" {
  name    = "mta-sts-policy"
  content = file("${path.module}/workers/mta-sts-policy.js")
}

resource "cloudflare_worker_route" "mta_sts" {
  zone_id     = var.cloudflare_zone_id
  pattern     = "mta-sts.thenash.group/.well-known/mta-sts.txt"
  script_name = cloudflare_worker_script.mta_sts.name
}

# File: the-citadel/terraform/cloudflare/workers/mta-sts-policy.js
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const policy = `version: STSv1
mode: enforce
mx: smtp.google.com
mx: *.smtp.google.com
max_age: 86400`

  return new Response(policy, {
    headers: {
      'content-type': 'text/plain',
      'cache-control': 'public, max-age=86400'
    }
  })
}
```

**Option 2: Static Hosting on GCP Cloud Storage**
```hcl
# the-citadel/terraform/gcp/mta-sts-bucket.tf
resource "google_storage_bucket" "mta_sts" {
  name     = "mta-sts-thenash-group"
  location = "US"

  website {
    main_page_suffix = "index.html"
  }

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "mta_sts_policy" {
  name   = ".well-known/mta-sts.txt"
  bucket = google_storage_bucket.mta_sts.name
  content = <<-EOT
    version: STSv1
    mode: enforce
    mx: smtp.google.com
    mx: *.smtp.google.com
    max_age: 86400
  EOT
  content_type = "text/plain"
}

# Cloudflare DNS record pointing to bucket
resource "cloudflare_record" "mta_sts_cname" {
  zone_id = var.cloudflare_zone_id
  name    = "mta-sts"
  type    = "CNAME"
  value   = "c.storage.googleapis.com"
  proxied = true  # Cloudflare proxies for HTTPS

  comment = "MTA-STS policy hosting (GCP Cloud Storage)"
}
```

**Testing**:
```bash
# Check DNS record
dig +short TXT _mta-sts.thenash.group

# Check policy file
curl https://mta-sts.thenash.group/.well-known/mta-sts.txt
# Expected: Policy file content
```

### 5.5 TLS Reporting (SMTP TLS)

**Purpose**: Receive reports about TLS connection failures.

**Record Type**: `TXT`
**Record Name**: `_smtp._tls.thenash.group`
**Record Value**:
```
v=TLSRPTv1; rua=mailto:smtp-tls-reports@thenash.group
```

**Explanation**:
- `v=TLSRPTv1`: TLS Reporting version 1
- `rua=mailto:smtp-tls-reports@thenash.group`: TLS failure reports sent here

**Terraform Configuration**:
```hcl
resource "cloudflare_record" "smtp_tls_reporting" {
  zone_id = var.cloudflare_zone_id
  name    = "_smtp._tls"
  type    = "TXT"
  value   = "v=TLSRPTv1; rua=mailto:smtp-tls-reports@thenash.group"
  ttl     = 3600

  comment = "SMTP TLS reporting - Monitor TLS connection failures"
}
```

### 5.6 BIMI (Brand Indicators for Message Identification)

**Purpose**: Display The Nash Group logo in supported email clients (Gmail, Yahoo, etc.).

**Prerequisites**:
1. **DMARC policy must be `p=quarantine` or `p=reject`** ✅ (we use `p=reject`)
2. **VMC (Verified Mark Certificate)**: Optional but recommended for full BIMI support
3. **Logo Requirements**:
   - SVG format (Tiny PS, no external references)
   - Square aspect ratio (1:1)
   - HTTPS-hosted, publicly accessible

**Record Type**: `TXT`
**Record Name**: `default._bimi.thenash.group`
**Record Value**:
```
v=BIMI1; l=https://assets.thenash.group/logos/nash-group-square.svg; a=https://assets.thenash.group/certs/vmc.pem
```

**Explanation**:
- `v=BIMI1`: BIMI version 1
- `l=https://...`: Logo URL (SVG, square, HTTPS)
- `a=https://...`: VMC (Verified Mark Certificate) URL (optional)

**Terraform Configuration**:
```hcl
resource "cloudflare_record" "bimi" {
  zone_id = var.cloudflare_zone_id
  name    = "default._bimi"
  type    = "TXT"
  value   = "v=BIMI1; l=https://assets.thenash.group/logos/nash-group-square.svg"
  ttl     = 3600

  comment = "BIMI record - Brand logo display in email clients"
}

# Note: VMC (Verified Mark Certificate) is optional but enhances trust
# Obtain VMC from providers like Entrust or DigiCert
```

**Testing**:
```bash
dig +short TXT default._bimi.thenash.group
```

**Note**: BIMI is **optional**. Focus on SPF, DKIM, DMARC, MTA-STS first.

### 5.7 DNSSEC (DNS Security Extensions)

**Purpose**: Cryptographically sign DNS records to prevent DNS spoofing.

**Status**: ✅ **Already enabled** if using Cloudflare (automatic)

**Verification**:
```bash
# Check DNSSEC status
dig +dnssec thenash.group | grep -i rrsig
# Should see RRSIG records (signature records)

# Validate DNSSEC chain
delv @8.8.8.8 thenash.group
# Should see "fully validated"
```

**Cloudflare Configuration**:
- DNSSEC is enabled by default for domains on Cloudflare
- DS records are automatically pushed to registrar (Namecheap, Google Domains, etc.)

**Terraform Configuration**:
```hcl
# DNSSEC is managed automatically by Cloudflare
# Ensure DNSSEC is enabled for the zone
resource "cloudflare_zone_dnssec" "thenash_group" {
  zone_id = var.cloudflare_zone_id
}
```

### Complete DNS Security Record Summary

**Final DNS Configuration for `thenash.group`**:

| Record Type | Record Name | Record Value | Purpose |
|------------|-------------|--------------|---------|
| **TXT** | `@` | `v=spf1 include:_spf.google.com ~all` | SPF - Authorized mail servers |
| **TXT** | `google._domainkey` | `v=DKIM1; k=rsa; p=...` | DKIM - Email signing |
| **TXT** | `_dmarc` | `v=DMARC1; p=reject; ...` | DMARC - Email authentication policy |
| **TXT** | `_mta-sts` | `v=STSv1; id=20251121T000000` | MTA-STS - TLS enforcement announcement |
| **TXT** | `_smtp._tls` | `v=TLSRPTv1; rua=mailto:...` | TLS Reporting |
| **TXT** | `default._bimi` | `v=BIMI1; l=https://...` | BIMI - Brand logo (optional) |
| **CNAME** | `mta-sts` | `c.storage.googleapis.com` | MTA-STS policy file hosting |
| **MX** | `@` | `1 smtp.google.com` | Google Workspace mail servers |
| **MX** | `@` | `5 smtp.google.com` | Google Workspace backup MX |
| **DS** | `@` | (Auto-managed by Cloudflare) | DNSSEC delegation signer |

**Terraform Complete Configuration**:
```hcl
# the-citadel/terraform/cloudflare/dns-email-security-complete.tf

# SPF
resource "cloudflare_record" "spf" {
  zone_id = var.cloudflare_zone_id
  name    = "@"
  type    = "TXT"
  value   = "v=spf1 include:_spf.google.com ~all"
  ttl     = 3600
  comment = "SPF - Authorized mail servers"
}

# DKIM (value from Google Workspace)
resource "cloudflare_record" "dkim_google" {
  zone_id = var.cloudflare_zone_id
  name    = "google._domainkey"
  type    = "TXT"
  value   = var.google_dkim_record_value
  ttl     = 3600
  comment = "DKIM - Email cryptographic signing"
}

# DMARC
resource "cloudflare_record" "dmarc" {
  zone_id = var.cloudflare_zone_id
  name    = "_dmarc"
  type    = "TXT"
  value   = "v=DMARC1; p=reject; sp=reject; rua=mailto:dmarc-reports@thenash.group; ruf=mailto:dmarc-forensics@thenash.group; fo=1; adkim=s; aspf=s; pct=100"
  ttl     = 3600
  comment = "DMARC - Email authentication enforcement (reject policy)"
}

# MTA-STS DNS announcement
resource "cloudflare_record" "mta_sts_txt" {
  zone_id = var.cloudflare_zone_id
  name    = "_mta-sts"
  type    = "TXT"
  value   = "v=STSv1; id=${var.mta_sts_policy_id}"
  ttl     = 3600
  comment = "MTA-STS - TLS enforcement announcement"
}

# MTA-STS policy hosting
resource "cloudflare_record" "mta_sts_cname" {
  zone_id = var.cloudflare_zone_id
  name    = "mta-sts"
  type    = "CNAME"
  value   = "c.storage.googleapis.com"
  proxied = true
  comment = "MTA-STS policy file hosting"
}

# SMTP TLS Reporting
resource "cloudflare_record" "smtp_tls_reporting" {
  zone_id = var.cloudflare_zone_id
  name    = "_smtp._tls"
  type    = "TXT"
  value   = "v=TLSRPTv1; rua=mailto:smtp-tls-reports@thenash.group"
  ttl     = 3600
  comment = "SMTP TLS Reporting - Monitor TLS failures"
}

# BIMI (optional)
resource "cloudflare_record" "bimi" {
  zone_id = var.cloudflare_zone_id
  name    = "default._bimi"
  type    = "TXT"
  value   = "v=BIMI1; l=https://assets.thenash.group/logos/nash-group-square.svg"
  ttl     = 3600
  comment = "BIMI - Brand logo display (optional)"
}

# DNSSEC
resource "cloudflare_zone_dnssec" "thenash_group" {
  zone_id = var.cloudflare_zone_id
}
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 3)

**Goal**: Establish OU structure and custom attributes.

**Tasks**:
- [ ] Create OU hierarchy in Google Workspace Admin Console
- [ ] Create custom schema `Nash_Group_Federation`
- [ ] Configure guardian@ account with hardware key MFA
- [ ] Migrate jeffrey@ to `/Humans/Mentors` OU
- [ ] Configure DNS email security records (SPF, DKIM, DMARC phase 1)

**Terraform Files**:
- `the-citadel/terraform/google-workspace/org-units.tf`
- `the-citadel/terraform/google-workspace/custom-schema.tf`
- `the-citadel/terraform/google-workspace/users.tf`
- `the-citadel/terraform/cloudflare/dns-email-security.tf`

### Phase 2: Context-Aware Access (Week 4)

**Goal**: Enforce device trust and Zero Trust access.

**Tasks**:
- [ ] Enable Context-Aware Access in GCP Organization
- [ ] Create Access Levels: `Trusted_Device`, `Admin_Workstation`, `Emergency_Break_Glass`
- [ ] Bind Access Levels to Google Workspace Admin Console
- [ ] Bind Access Levels to GCP Console (Owner/Admin roles)
- [ ] Test access from trusted and untrusted devices

**Terraform Files**:
- `the-citadel/terraform/google-workspace/access-levels.tf`
- `the-citadel/terraform/google-workspace/access-bindings.tf`

### Phase 3: Application Controls (Week 4)

**Goal**: Lock down third-party app access and OAuth.

**Tasks**:
- [ ] Configure OAuth policy: Block all by default
- [ ] Allowlist approved apps (Terraform Cloud, Observability Bridge)
- [ ] Configure session duration per OU
- [ ] Test third-party app blocking

**Configuration**:
- Via Admin Console (Terraform support limited)
- Document in `GOOGLE-WORKSPACE-ARCHITECTURE.md`

### Phase 4: Email Security Hardening (Week 3-5)

**Goal**: Achieve maximum email security posture.

**Tasks**:
- [ ] Week 3: Deploy SPF, DKIM, DMARC (p=none)
- [ ] Week 4: Monitor DMARC reports, escalate to p=quarantine
- [ ] Week 5: Escalate DMARC to p=reject
- [ ] Week 5: Deploy MTA-STS (DNS + policy file)
- [ ] Week 5: Deploy SMTP TLS Reporting
- [ ] Week 6: (Optional) Deploy BIMI with logo

**Terraform Files**:
- `the-citadel/terraform/cloudflare/dns-email-security-complete.tf`
- `the-citadel/terraform/cloudflare/mta-sts-worker.tf` (or GCP bucket)

### Phase 5: Federation Integration (Week 5-7)

**Goal**: Integrate with AWS, GitHub, Cloudflare via SAML/OIDC.

**Tasks**:
- [ ] Configure SAML app for AWS IAM Identity Center
- [ ] Test SAML SSO: guardian@ → AWS Console
- [ ] Configure SAML app for GitHub Enterprise (if applicable)
- [ ] Configure SAML app for Cloudflare Access
- [ ] Validate custom attributes in SAML assertions

**Terraform Files**:
- `the-citadel/terraform/aws/sso-saml-integration.tf`
- `the-citadel/terraform/google-workspace/saml-apps.tf`

### Phase 6: Monitoring & Compliance (Week 8)

**Goal**: Centralized audit logging and compliance verification.

**Tasks**:
- [ ] Export Google Workspace Admin Logs to GCP Logging
- [ ] Export to Observability Bridge (the-nexus)
- [ ] Create dashboards for:
  - Failed login attempts
  - MFA enrollment status
  - DMARC/MTA-STS compliance
  - Context-Aware Access denials
- [ ] Weekly compliance reports

**Terraform Files**:
- `the-citadel/terraform/gcp/audit-log-export.tf`
- `the-nexus/apps/bridge/config/google-workspace-integration.yaml`

---

## Terraform Configuration Examples

### Complete Terraform Module Structure

```
the-citadel/terraform/google-workspace/
├── main.tf                   # Provider configuration
├── variables.tf              # Input variables
├── outputs.tf                # Output values
├── org-units.tf              # OU hierarchy
├── custom-schema.tf          # Nash_Group_Federation schema
├── users.tf                  # User accounts
├── groups.tf                 # Google Groups
├── access-levels.tf          # Context-Aware Access levels
├── access-bindings.tf        # CAA bindings to apps
├── saml-apps.tf              # SAML app configurations
└── oauth-policy.tf           # Third-party app controls
```

### Provider Configuration

```hcl
# the-citadel/terraform/google-workspace/main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    googleworkspace = {
      source  = "hashicorp/googleworkspace"
      version = "~> 0.7.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "remote" {
    organization = "the-nash-group"
    workspaces {
      name = "google-workspace-prod"
    }
  }
}

provider "googleworkspace" {
  customer_id = var.google_workspace_customer_id

  # Use service account impersonation for admin access
  impersonated_user_email = var.admin_email  # guardian@thenash.group

  # OAuth credentials (service account with domain-wide delegation)
  credentials = var.google_workspace_credentials
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}
```

### Variables

```hcl
# the-citadel/terraform/google-workspace/variables.tf
variable "google_workspace_customer_id" {
  description = "Google Workspace Customer ID (C0xxxxxxx)"
  type        = string
  sensitive   = true
}

variable "admin_email" {
  description = "Super admin email for impersonation"
  type        = string
  default     = "guardian@thenash.group"
}

variable "google_workspace_credentials" {
  description = "Service account credentials JSON (domain-wide delegation)"
  type        = string
  sensitive   = true
}

variable "gcp_project_id" {
  description = "GCP project for Context-Aware Access"
  type        = string
  default     = "nash-personal-prod"
}

variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "access_policy_id" {
  description = "GCP Access Context Manager policy ID"
  type        = string
}

variable "guardian_recovery_email" {
  description = "Recovery email for guardian@"
  type        = string
  sensitive   = true
}

variable "guardian_recovery_phone" {
  description = "Recovery phone for guardian@"
  type        = string
  sensitive   = true
}

variable "google_dkim_record_value" {
  description = "DKIM TXT record value from Google Workspace"
  type        = string
  sensitive   = false
}

variable "mta_sts_policy_id" {
  description = "MTA-STS policy version ID (timestamp)"
  type        = string
  default     = "20251121T000000"
}

variable "cloudflare_zone_id" {
  description = "Cloudflare Zone ID for thenash.group"
  type        = string
}
```

---

## Governance & Compliance

### Alignment with Nash Group Policies

| Configuration Area | Policy Reference | Compliance Requirement |
|--------------------|-----------------|------------------------|
| **OU Segregation** | SEC-003 (Least Privilege) | Different OUs have minimal necessary permissions |
| **MFA Enforcement** | SEC-004 (Security Baseline) | Hardware keys for Guardians, TOTP for others |
| **Context-Aware Access** | SEC-001 (Zero Trust) | Device trust + location verification |
| **Custom Attributes** | GOV-010 (Labeling Standard) | `nash_clan`, `nash_tier`, `nash_role` encoded |
| **OAuth Controls** | SEC-003 (Least Privilege) | Block all, allowlist approved apps |
| **Email Security** | SEC-004 (Security Baseline) | DMARC p=reject, MTA-STS enforced |

### Approval Requirements

**Covenant-Level** (2 Watchers + 2 Mentors):
- OU topology design
- Custom attribute schema
- Email security policy (DMARC p=reject)

**Citadel-Level** (1 Mentor + 1 Watcher):
- Context-Aware Access level definitions
- OAuth allowlist additions
- Session duration changes

**Stronghold-Level** (1 Mentor):
- Individual user attribute updates
- DNS record additions (non-security)

### Audit & Compliance Verification

**Daily Automated Checks**:
- [ ] All Guardians have hardware key MFA enabled
- [ ] No users in wrong OU (drift detection)
- [ ] No unauthorized third-party apps connected
- [ ] DMARC reports show 100% pass rate

**Weekly Manual Reviews**:
- [ ] Review Context-Aware Access denial logs
- [ ] Review failed login attempts
- [ ] Review DMARC/MTA-STS reports
- [ ] Review OAuth app access logs

**Quarterly Audits**:
- [ ] Full OU membership review
- [ ] Custom attribute accuracy verification
- [ ] Access Level effectiveness assessment
- [ ] Email security posture review

---

## Appendix: Quick Reference

### Google Workspace Admin Console URLs

| Function | URL |
|----------|-----|
| **Organizational Units** | `https://admin.google.com/ac/orgunits` |
| **Users** | `https://admin.google.com/ac/users` |
| **Custom Attributes** | `https://admin.google.com/ac/customschema` |
| **Security > 2-Step Verification** | `https://admin.google.com/ac/security/2sv` |
| **Security > Context-Aware Access** | `https://admin.google.com/ac/security/contextawareaccess` |
| **Apps > SAML Apps** | `https://admin.google.com/ac/apps/saml` |
| **Security > API Controls** | `https://admin.google.com/ac/owl` |
| **Apps > Gmail > Authenticate email** | `https://admin.google.com/ac/apps/gmail/authenticateemail` |

### Common gcloud Commands

```bash
# List OUs
gcloud identity groups search --organization="thenash.group"

# List users in OU
gcloud identity users list --organization="thenash.group" \
  --filter="orgUnitPath:/Guardians"

# Check Context-Aware Access policies
gcloud access-context-manager policies list --organization="$ORG_ID"

# List Access Levels
gcloud access-context-manager levels list \
  --policy="$POLICY_ID"
```

### Email Security Testing Tools

| Tool | URL | Purpose |
|------|-----|---------|
| **Google Admin Toolbox** | https://toolbox.googleapps.com/apps/checkmx/ | Check MX, SPF, DKIM, DMARC |
| **MXToolbox** | https://mxtoolbox.com/SuperTool.aspx | Comprehensive DNS/email testing |
| **DMARC Analyzer** | https://www.dmarcanalyzer.com/ | Parse DMARC reports |
| **MTA-STS Validator** | https://www.hardenize.com/ | Verify MTA-STS policy |
| **BIMI Inspector** | https://bimigroup.org/bimi-generator/ | Test BIMI implementation |

---

**Document Status**: TECHNICAL SPECIFICATION - Ready for Implementation
**Next Steps**:
1. Review by nash-group-watchers@ (security validation)
2. Review by nash-group-mentors@ (implementation feasibility)
3. Create ADR in the-covenant documenting this architecture
4. Begin Phase 1 implementation (Week 3)

---

*"From philosophy to configuration. From policy to Terraform. This is how we build civilizations in code."*

**Last Updated**: 2025-11-21
**Document Owner**: guardian@thenash.group
**Implementation Lead**: jeffrey@thenash.group (Mentor, Architect)
