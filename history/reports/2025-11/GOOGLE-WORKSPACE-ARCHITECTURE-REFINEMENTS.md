# Google Workspace Architecture: Strategic Refinements (Nov 2025)

**Version**: 1.1.0
**Created**: 2025-11-21
**Status**: CRITICAL OPERATIONAL FIXES
**Authority**: Covenant Level (2 Watchers + 2 Mentors)
**Guardian Roles**: The Watcher (Security Review), The Architect (Implementation)
**Parent Document**: GOOGLE-WORKSPACE-ARCHITECTURE.md v1.0.0

> "From specification to operation. These refinements address real-world deployment challenges discovered during expert security review. They transform a 'best practice' architecture into a 'next practice' implementation."

---

## Executive Summary

This document captures **critical operational refinements** to the Google Workspace Architecture specification based on expert security review. These are not optional enhancements—they are **required fixes** to prevent lockout scenarios and align with November 2025 authentication landscape.

### Critical Issues Addressed

| Issue | Risk Level | Impact | Fix |
|-------|------------|--------|-----|
| **Break-Glass Paradox** | 🔴 CRITICAL | Complete lockout if CAA fails | Add CAA_Exempt emergency admin |
| **Passkey Clarity** | 🟡 HIGH | Policy blocks modern FIDO2 authenticators | Explicitly allow Passkeys |
| **Chrome Enterprise Requirement** | 🟡 HIGH | Device trust policies fail without browser enrollment | Document CBCM setup |
| **Terraform Binding Limitations** | 🟠 MEDIUM | Hours wasted on unsupported API calls | Manual binding strategy |
| **Service Account Naming** | 🟢 LOW | Future-proofing for AI agents | Rename to Machine-Identities |

---

## 1. Critical Fix: The "Golden Key" Break-Glass Account

### The Paradox

**Original Specification** (Section 2.3):
> "Emergency Break-Glass access level is manually activated by Watchers during incidents."

**The Problem**:
If Context-Aware Access (CAA) is misconfigured or Google's systems are down, **Watchers cannot log into the Admin Console to enable the break-glass policy**. This creates a circular dependency:

```
CAA is broken → Watcher locked out → Cannot access Admin Console → Cannot disable CAA → Permanent lockout
```

**Real-World Scenario**:
1. You deploy CAA policy requiring `Admin_Workstation` access level
2. You misconfigure the IP allowlist (wrong subnet)
3. `guardian@thenash.group` is now locked out of Admin Console
4. You cannot log in to fix the IP allowlist
5. **You are permanently locked out of your own organization**

### The Solution: CAA_Exempt Emergency Admin

**Design**:
Create a single emergency admin account that is **explicitly excluded** from all Context-Aware Access policies.

**Account Details**:
```yaml
account: emergency-admin@thenash.group
purpose: "Golden Key for CAA lockout recovery"
ou: /Guardians
mfa: Hardware security key ONLY (YubiKey stored in physical safe)
access_level: EXEMPT from all CAA policies
usage_policy: ONLY for recovering from CAA lockout
audit: All logins generate immediate alert to Watchers

restrictions:
  - Cannot modify organization policies (read-only except CAA)
  - Cannot create/delete users
  - Cannot access Google Drive, Gmail (admin only)
  - Session duration: 1 hour maximum
  - Re-authentication required every 15 minutes

physical_security:
  - YubiKey stored in home safe
  - Password stored in gopass: nash-group/google/emergency-admin-password
  - Recovery codes printed and stored in safe deposit box
```

**Access Group Configuration**:
```yaml
group_name: "CAA_Exempt"
members:
  - emergency-admin@thenash.group
description: "Emergency accounts excluded from Context-Aware Access policies"

binding:
  all_caa_policies: "Apply to: All Users - Exclude Group(CAA_Exempt)"
```

### Terraform Implementation

```hcl
# the-citadel/terraform/google-workspace/emergency-admin.tf

# Create CAA_Exempt group
resource "googleworkspace_group" "caa_exempt" {
  email       = "caa-exempt@thenash.group"
  name        = "Context-Aware Access Exempt"
  description = "Emergency accounts excluded from all CAA policies (break-glass only)"

  # Prevent accidental deletion
  lifecycle {
    prevent_destroy = true
  }
}

# Create emergency admin account
resource "googleworkspace_user" "emergency_admin" {
  primary_email = "emergency-admin@thenash.group"

  name {
    family_name = "Emergency"
    given_name  = "Admin"
  }

  org_unit_path = googleworkspace_org_unit.guardians.id

  password              = var.emergency_admin_password  # From secret
  change_password_at_next_login = false

  custom_schemas = [{
    schema_name = "Nash_Group_Federation"
    field_values = {
      "nash_role"     = "emergency-admin"
      "nash_tier"     = "core"
      "nash_clan"     = "watchers"
      "aws_role_arn"  = ""  # No AWS access
      "session_duration" = "3600"  # 1 hour only
    }
  }]

  recovery_email = var.guardian_recovery_email
  recovery_phone = var.guardian_recovery_phone

  # Lifecycle protection
  lifecycle {
    prevent_destroy = true
  }
}

# Add emergency admin to CAA_Exempt group
resource "googleworkspace_group_member" "emergency_admin_exempt" {
  group_id = googleworkspace_group.caa_exempt.id
  email    = googleworkspace_user.emergency_admin.primary_email
  role     = "MEMBER"

  lifecycle {
    prevent_destroy = true
  }
}

# Monitoring: Alert on emergency admin login
resource "google_logging_metric" "emergency_admin_login" {
  name   = "emergency_admin_login"
  filter = <<-EOT
    protoPayload.authenticationInfo.principalEmail="emergency-admin@thenash.group"
    AND protoPayload.methodName="google.login.LoginService.loginSuccess"
  EOT

  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
  }
}

resource "google_monitoring_alert_policy" "emergency_admin_alert" {
  display_name = "🚨 EMERGENCY ADMIN ACCOUNT USED"
  combiner     = "OR"

  conditions {
    display_name = "Emergency admin login detected"
    condition_threshold {
      filter          = "metric.type=\"logging.googleapis.com/user/${google_logging_metric.emergency_admin_login.name}\""
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0
    }
  }

  notification_channels = [var.critical_alert_channel_id]

  alert_strategy {
    auto_close = "604800s"  # 7 days
  }

  documentation {
    content = <<-EOT
      # Emergency Admin Account Used

      The `emergency-admin@thenash.group` account has been used.

      **This should ONLY happen during:**
      - Context-Aware Access lockout recovery
      - Break-glass emergency procedures

      **Immediate Actions:**
      1. Verify this was authorized (contact all Watchers)
      2. Review audit logs for actions taken
      3. Investigate why normal admin access failed
      4. Rotate emergency admin credentials after incident

      **Runbook**: https://runbooks.thenash.group/emergency-admin-usage
    EOT
  }
}
```

### Context-Aware Access Policy Modification

**ALL CAA policies must exclude this group**:

```hcl
# the-citadel/terraform/google-workspace/access-levels.tf

# Example: Trusted_Device access level (modified)
resource "google_access_context_manager_access_level" "trusted_device" {
  parent = "accessPolicies/${var.access_policy_id}"
  name   = "accessPolicies/${var.access_policy_id}/accessLevels/trusted_device"
  title  = "Trusted Device"

  basic {
    combining_function = "OR"

    # Original device policy conditions
    conditions {
      device_policy {
        require_screen_lock = true
        # ... rest of policy
      }
    }

    # NEW: Exempt CAA_Exempt group members
    conditions {
      members = [
        "group:${googleworkspace_group.caa_exempt.email}"
      ]
    }
  }
}

# Apply same pattern to Admin_Workstation and all other access levels
```

**CRITICAL**: Every access level needs the exemption condition, or the emergency account is useless.

### Usage Protocol

**When to Use Emergency Admin**:
1. ✅ Context-Aware Access lockout (cannot log into Admin Console)
2. ✅ Need to disable broken CAA policy during incident
3. ✅ Testing CAA policies in production (verify exemption works)
4. ❌ Regular administrative tasks (use guardian@ instead)
5. ❌ Convenience (too lazy to grab YubiKey)

**Step-by-Step Break-Glass Procedure**:

```bash
# 1. Retrieve credentials
gopass show nash-group/google/emergency-admin-password

# 2. Retrieve YubiKey from safe
# Physical step - go to home safe

# 3. Log into Admin Console
open "https://admin.google.com"
# Email: emergency-admin@thenash.group
# Password: [from gopass]
# MFA: YubiKey only

# 4. Navigate to Security > Context-Aware Access
# 5. Identify broken access level
# 6. Temporarily disable or fix configuration

# 7. Test normal admin access
# Try logging in as guardian@thenash.group

# 8. If fixed, re-enable CAA policy

# 9. Log out of emergency-admin@

# 10. Post-incident actions:
# - Document what went wrong in the-covenant/incidents/
# - Rotate emergency-admin password
# - Review audit logs for emergency session
# - Create ADR if CAA policy needs permanent change
```

### Audit and Compliance

**Monthly Verification**:
```bash
# Verify emergency admin is in CAA_Exempt group
gcloud identity groups memberships list \
  --group-email="caa-exempt@thenash.group"

# Verify account has not been used (unless incident)
gcloud logging read \
  'protoPayload.authenticationInfo.principalEmail="emergency-admin@thenash.group"' \
  --limit=10 \
  --format=json

# Expected: No logins in past 30 days (unless emergency)
```

**Quarterly Testing**:
1. Deliberately misconfigure a test CAA policy
2. Verify you can log in as emergency-admin@
3. Fix the test policy
4. Verify normal admin access restored
5. Document test results

---

## 2. Passkey Evolution (FIDO2 Clarification)

### The Issue

**Original Specification** (Section 1, Guardians OU):
> "MFA enforcement: Security Key (Hardware - YubiKey, Titan Key)"

**The Problem**:
By November 2025, **Passkeys** (synced FIDO2 credentials) are mature and widely supported:
- iCloud Keychain (Apple devices)
- Google Password Manager (Android/Chrome)
- 1Password, Bitwarden (cross-platform)

**Passkeys are FIDO2-compliant** and as secure as hardware keys for most threat models. The policy as written might be interpreted as blocking Passkeys, forcing users to carry physical hardware tokens.

**User Experience Impact**:
- Guardian needs to log in from iPhone → Blocked (no hardware key)
- Guardian traveling without YubiKey → Locked out
- Passkey provides equivalent security without physical device dependency

### The Solution: Explicitly Allow Passkeys

**Refined Policy**:

```yaml
authentication:
  multi_factor_authentication:
    enforcement: MANDATORY
    allowed_methods:
      - Security Key (Hardware) - YubiKey, Titan Key, Feitian
      - Passkey (FIDO2) - iCloud Keychain, Google Password Manager
      - Authenticator App (TOTP) - Google Authenticator, Authy

    disallowed_methods:
      - SMS (phishing vulnerability)
      - Voice call (SIM swap risk)
      - Backup codes (except emergency recovery)

    priority_order:
      1. Security Key (Hardware) - RECOMMENDED for Guardians
      2. Passkey (FIDO2) - ACCEPTABLE for Guardians
      3. Authenticator App (TOTP) - MINIMUM for Humans

    notes:
      - "Passkeys must be bound to the Admin_Workstation access level"
      - "Passkeys stored in iCloud Keychain require device unlock (biometric/PIN)"
      - "Hardware keys preferred for guardian@ due to offline capability"
```

**Google Workspace Configuration**:

In Admin Console → Security → 2-Step Verification:

```
Enforcement: ON
Allow users to turn off 2-Step Verification: NO

Allowed Methods:
  ✅ Security Key (including Passkeys)
  ✅ Google Prompt
  ✅ Google Authenticator App
  ❌ Text message
  ❌ Phone call
  ✅ Backup codes (for emergency only)
```

**IMPORTANT**: Google Workspace treats Passkeys as "Security Keys" in the UI. The distinction is:
- **Hardware Security Key**: Physical USB/NFC device (YubiKey)
- **Passkey**: FIDO2 credential stored in platform authenticator (iCloud Keychain, Google Password Manager)

Both use the same WebAuthn standard, so they're equally secure from a cryptographic perspective.

### Implementation Notes

**For guardian@thenash.group**:
1. **Primary MFA**: YubiKey 5C NFC (stored with laptop)
2. **Backup MFA**: Passkey in iCloud Keychain (synced to iPhone/iPad)
3. **Emergency**: Backup codes in gopass

**For jeffrey@thenash.group**:
1. **Primary MFA**: Passkey in iCloud Keychain (convenience)
2. **Backup MFA**: YubiKey 5C NFC (optional, recommended)
3. **Tertiary**: Google Authenticator TOTP (fallback)

**Terraform Update** (no change needed):
Google Workspace Admin Console doesn't distinguish Passkeys from Hardware Keys in policy—they're all "Security Key" in the API.

---

## 3. Chrome Enterprise Premium / Browser Cloud Management

### The Issue

**Original Specification** (Section 2, Access Level 1: Trusted_Device):
> "device_policy: require_corp_owned: false  # Allow BYOD if managed"

**The Problem**:
To enforce `device_policy.require_corp_owned` or even basic device trust, Google requires the **Chrome Browser** to be enrolled in **Chrome Browser Cloud Management (CBCM)**.

**Without CBCM enrollment**:
- Google cannot identify the device
- `device_policy` evaluations fail
- Access Level evaluates to `FALSE`
- User is blocked from all apps

**Real-World Impact**:
You deploy the `Trusted_Device` access level, bind it to Gmail/Drive, and suddenly **you cannot access your own email** because Google doesn't recognize your device.

### The Solution: Chrome Browser Cloud Management Setup

**Prerequisites**:
1. Google Workspace Enterprise Standard or Plus (you likely have this)
2. Chrome Browser (stable channel, latest version)
3. Browser token from Admin Console

**Setup Steps**:

#### Step 1: Enable Chrome Browser Cloud Management

**Admin Console** → **Devices** → **Chrome** → **Settings** → **User & Browser Settings**

```yaml
Enable Browser Management: ON

Verification:
  Require Chrome Browser Cloud Management: YES
  Allow unmanaged browsers: NO (for Guardians OU only)
```

#### Step 2: Generate Enrollment Token

**Admin Console** → **Devices** → **Chrome** → **Enrollment & access** → **Browser enrollment**

```
Click "Generate token"
Copy enrollment token (looks like: 1234567890abcdef...)
```

#### Step 3: Enroll Your Chrome Browser (macOS)

**Option A: Command Line (Recommended)**:
```bash
# Download Chrome Enterprise bundle
# https://chromeenterprise.google/browser/download/

# Enroll Chrome with token
sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --enrollment-token="YOUR_TOKEN_HERE" \
  --machine-level-user-cloud-policy-enrollment-token="YOUR_TOKEN_HERE"

# Verify enrollment
chrome://policy/
# Look for "CloudManagementEnrollmentToken" = Enrolled
```

**Option B: Manual Enrollment**:
1. Open Chrome
2. Go to `chrome://policy/`
3. Click "Reload policies"
4. If not enrolled, you'll see "Set up Chrome Browser Cloud Management"
5. Follow prompts, paste enrollment token

#### Step 4: Install Endpoint Verification Extension

**Chrome Web Store** → Search for "**Endpoint Verification**" (by Google)
**OR** direct URL: https://chrome.google.com/webstore/detail/endpoint-verification/callobklhcbilhphinckomhgkigmfocg

**After Installation**:
1. Extension will request "Verify your device"
2. Click "Verify"
3. Sign in with guardian@thenash.group (or jeffrey@)
4. Chrome will register device certificate with Google

**Verification**:
```bash
# Check if device is recognized
# Admin Console → Devices → Chrome → Browsers
# You should see your device listed with:
# - Browser version
# - OS version
# - Last sync time
# - Device certificate status
```

### Updated Documentation

**GOOGLE-WORKSPACE-ARCHITECTURE.md Section 2.1 Trusted_Device** should include:

```yaml
prerequisites:
  chrome_browser:
    version: "Latest stable (120+)"
    enrollment: "Chrome Browser Cloud Management required"
    extension: "Endpoint Verification extension installed"
    setup_guide: "See GOOGLE-WORKSPACE-ARCHITECTURE-REFINEMENTS.md Section 3"

  verification:
    admin_console_url: "https://admin.google.com/ac/chrome/devices"
    expected_status: "Device visible with certificate"
    failure_mode: "If not enrolled, access level evaluates to FALSE → blocked"
```

**Add to Implementation Roadmap (Phase 2, Week 4)**:

```markdown
### Phase 2: Context-Aware Access (Week 4)

**Prerequisites** (do BEFORE deploying CAA policies):
- [ ] Enroll Chrome Browser in Chrome Browser Cloud Management
- [ ] Install Endpoint Verification extension
- [ ] Verify device appears in Admin Console → Devices → Chrome
- [ ] Test access to gmail.com (should work)

**CAA Deployment**:
- [ ] Create Access Levels via Terraform
- [ ] Manually bind to Google Workspace apps (Admin Console)
- [ ] Test from enrolled device (should work)
- [ ] Test from unenrolled device (should block)
```

---

## 4. Terraform Provider Limitations for CAA Bindings

### The Issue

**Original Specification** (Section 2, Context-Aware Access):
> "Application Binding: Which Google Apps (Drive, Admin Console) get bound to which Access Level?"

**The Problem**:
The `hashicorp/googleworkspace` Terraform provider **does not support** binding Context-Aware Access levels to Google Workspace applications (Gmail, Drive, Admin Console).

**What IS supported via Terraform**:
- ✅ Creating Access Levels (`google_access_context_manager_access_level`)
- ✅ Creating Access Policies (`google_access_context_manager_access_policy`)
- ✅ Binding Access Levels to **GCP resources** (GCS buckets, BigQuery, etc.)

**What is NOT supported**:
- ❌ Binding Access Levels to **Google Workspace apps** (Gmail, Drive, Calendar, Admin Console)
- ❌ Configuring which OU gets which Access Level for Workspace apps

**Real-World Impact**:
If you try to Terraform the bindings, you'll spend hours debugging `Error 400: Invalid Scope` or `API not enabled` errors. The APIs exist, but the Terraform provider doesn't expose them.

### The Solution: Hybrid Approach

**Terraform Manages**:
- Access Level definitions
- Access Policy (organization-wide)
- GCP resource bindings

**Manual Management** (Admin Console):
- Binding Access Levels to Google Workspace apps
- Per-OU Access Level assignments

**Rationale**:
This is **pragmatic architecture**. We use Terraform where it's reliable, and Admin Console where the API support is immature.

### Implementation Strategy

#### Phase 2 (Week 4): Deploy CAA

**Step 1: Terraform Creates Access Levels**
```bash
cd the-citadel/terraform/google-workspace
terraform init
terraform plan -target=google_access_context_manager_access_level.trusted_device
terraform apply -target=google_access_context_manager_access_level.trusted_device
# Repeat for admin_workstation, emergency_break_glass
```

**Step 2: Manual Binding in Admin Console**

**Admin Console** → **Security** → **Access and data control** → **Context-Aware Access**

**For Gmail:**
```
App: Gmail
Access Level: Trusted_Device
Apply to: All Users (except CAA_Exempt group)
```

**For Google Drive:**
```
App: Google Drive
Access Level: Trusted_Device
Apply to: All Users (except CAA_Exempt group)
```

**For Admin Console:**
```
App: Admin Console
Access Level: Admin_Workstation
Apply to: OU=/Guardians
```

**Step 3: Document Manual Changes**

Create `the-citadel/docs/manual-configurations.md`:
```markdown
# Manual Configurations (Not in Terraform)

## Context-Aware Access Bindings

**Date Configured**: 2025-11-21
**Configured By**: jeffrey@thenash.group

### Gmail
- Access Level: `Trusted_Device`
- Apply to: All Users
- Exclude: `caa-exempt@thenash.group`

### Google Drive
- Access Level: `Trusted_Device`
- Apply to: All Users
- Exclude: `caa-exempt@thenash.group`

### Admin Console
- Access Level: `Admin_Workstation`
- Apply to: OU=/Guardians
- Exclude: `emergency-admin@thenash.group`

**Drift Detection**:
- Monthly manual review
- Screenshot configurations in Admin Console
- Store in the-citadel/docs/screenshots/
```

### Future Improvement

**When Provider Matures** (mid-2026?):
Monitor `hashicorp/googleworkspace` provider releases for:
- `googleworkspace_access_level_binding` resource
- Support for `application_id` targeting Workspace apps

**Then**:
1. Import existing manual bindings into Terraform state
2. Codify in `access-bindings.tf`
3. Delete `manual-configurations.md`

---

## 5. Machine-Identities: Future-Proofing for AI Agents

### The Issue

**Original Specification** (Section 1, OU Topology):
> "`/Service-Accounts` OU: Machine identities for CI/CD, automation, and service-to-service auth."

**The Problem**:
The term "Service Accounts" is GCP-specific and implies traditional automation bots. By 2026, **AI agents** will need organizational identities:

**Use Cases**:
- AI assistant organizing Google Drive folders
- AI agent reading Gmail to extract invoices
- AI summarizer accessing Google Docs for reports
- AI scheduler accessing Calendar

**These are not "service accounts" in the traditional sense**—they're **agentic identities** with autonomous behavior.

### The Solution: Rename to `/Machine-Identities`

**Rationale**:
- "Machine-Identities" is inclusive of bots, services, and AI agents
- Aligns with industry trend toward "non-human identities" (NHI)
- Future-proofs for **Workforce Identity Federation for AI Agents** (Google's 2026 roadmap)

**Policy Differentiation**:

```yaml
/Machine-Identities (Root OU)
  ├── /Automation (Traditional bots)
  │   ├── citadel-deployer@thenash.group (CI/CD)
  │   ├── nexus-deployer@thenash.group (App deployment)
  │   └── observability-bridge@thenash.group (Log aggregation)
  │
  └── /Agentic (AI/ML agents - future)
      ├── ai-drive-organizer@thenash.group
      ├── ai-email-parser@thenash.group
      └── ai-calendar-scheduler@thenash.group
```

**Policy Differences**:

| Aspect | /Automation | /Agentic |
|--------|------------|----------|
| **Authentication** | OIDC only | OIDC + limited OAuth |
| **Data Access** | API-only | Read-only Drive/Gmail |
| **Session Duration** | N/A (stateless tokens) | 1 hour max |
| **Audit Logging** | Standard | Enhanced (all actions logged) |
| **Human Oversight** | Guardian approval for creation | Guardian approval + monthly review |

### Terraform Refactoring

**Rename OU**:
```hcl
# the-citadel/terraform/google-workspace/org-units.tf

# OLD:
# resource "googleworkspace_org_unit" "service_accounts" {
#   name        = "Service-Accounts"
#   parent_org_unit_path = "/"
#   description = "Machine identities - OIDC-only, no passwords"
# }

# NEW:
resource "googleworkspace_org_unit" "machine_identities" {
  name        = "Machine-Identities"
  parent_org_unit_path = "/"
  description = "Non-human identities: automation bots and AI agents"
}

# Create sub-OUs
resource "googleworkspace_org_unit" "automation" {
  name        = "Automation"
  parent_org_unit_path = googleworkspace_org_unit.machine_identities.id
  description = "Traditional CI/CD bots - OIDC-only, no interactive login"
}

resource "googleworkspace_org_unit" "agentic" {
  name        = "Agentic"
  parent_org_unit_path = googleworkspace_org_unit.machine_identities.id
  description = "AI/ML agents - limited OAuth for Drive/Gmail read access (future)"
}
```

**Update Custom Attribute Schema**:
```hcl
# Add "agent_type" field to Nash_Group_Federation schema
resource "googleworkspace_schema" "nash_group_federation" {
  schema_name  = "Nash_Group_Federation"
  display_name = "Nash Group Federation Attributes"

  # ... existing fields ...

  # NEW field for machine identities
  fields {
    field_name = "machine_type"
    field_type = "STRING"
    display_name = "Machine Identity Type"
    multi_valued = false
  }
  # Valid values: "automation", "agentic", "human"
}
```

### Governance Policy Update

**Create `the-covenant/policies/ops-012-agentic-identity.md`** (future):
```markdown
# OPS-012: Agentic Identity Management

**Policy ID:** OPS-012
**Category:** Operations
**Effective Date:** 2026-01-01 (planned)

## Statement

AI agents requiring organizational data access **must** be provisioned as Machine-Identities with limited OAuth scopes, read-only access, enhanced logging, and monthly human review.

## Scope

**Applies To:**
- AI assistants accessing Google Drive
- AI agents parsing Gmail
- AI schedulers accessing Calendar
- Any autonomous system requiring Google Workspace data

## Requirements

1. **Authentication**: OIDC preferred, OAuth 2.0 allowed with approval
2. **Authorization**: Read-only by default, write requires Citadel approval
3. **Audit**: All actions logged to Observability Bridge
4. **Review**: Monthly review of agent behavior by Guardian
5. **Sunset**: Unused agents auto-disabled after 90 days
```

---

## 6. Updated Implementation Roadmap

### Phase 1 Modifications (Week 3)

**Add Prerequisites**:
```markdown
### Week 3: Foundation (BEFORE deploying CAA)

**Chrome Browser Setup** (CRITICAL - do first):
- [ ] Install Chrome Browser Cloud Management
- [ ] Generate enrollment token
- [ ] Enroll Chrome on guardian's Mac
- [ ] Enroll Chrome on jeffrey's Mac
- [ ] Install Endpoint Verification extension
- [ ] Verify devices appear in Admin Console → Devices → Chrome

**Emergency Admin Account** (CRITICAL - do second):
- [ ] Create emergency-admin@thenash.group account
- [ ] Configure hardware key MFA (YubiKey in safe)
- [ ] Store password in gopass: nash-group/google/emergency-admin-password
- [ ] Create CAA_Exempt group
- [ ] Add emergency-admin to CAA_Exempt group
- [ ] Test login with emergency account
- [ ] Configure alert for emergency admin usage

**OU Topology**:
- [ ] Rename /Service-Accounts to /Machine-Identities
- [ ] Create sub-OUs: /Automation, /Agentic
- [ ] Migrate existing service accounts to /Automation

**Custom Attributes**:
- [ ] Add "machine_type" field to Nash_Group_Federation schema
```

### Phase 2 Modifications (Week 4)

**Context-Aware Access Deployment Strategy**:
```markdown
### Week 4: Context-Aware Access

**Terraform (Automated)**:
- [ ] Create Access Levels: Trusted_Device, Admin_Workstation, Emergency_Break_Glass
- [ ] Modify all Access Levels to include CAA_Exempt exemption
- [ ] Validate Access Levels in Admin Console

**Manual Configuration** (documented in manual-configurations.md):
- [ ] Bind Trusted_Device to Gmail (exclude CAA_Exempt)
- [ ] Bind Trusted_Device to Google Drive (exclude CAA_Exempt)
- [ ] Bind Admin_Workstation to Admin Console (Guardians OU only)
- [ ] Test access from enrolled device (should work)
- [ ] Test access from unenrolled device (should block)
- [ ] Test emergency-admin@ can bypass (should work)

**Rollback Plan**:
- [ ] Document how to disable all CAA policies via emergency-admin@
- [ ] Test rollback procedure in non-production OU first
```

---

## 7. Critical Configuration Checklist

### Before Deploying Context-Aware Access

**Prerequisites** (MUST complete ALL before enabling CAA):

```
Pre-Flight Checklist (Week 3):

Chrome Browser Cloud Management:
  [ ] Admin Console → Devices → Chrome → Settings enabled
  [ ] Enrollment token generated
  [ ] guardian@'s Chrome enrolled (verified in Admin Console)
  [ ] jeffrey@'s Chrome enrolled (verified in Admin Console)
  [ ] Endpoint Verification extension installed (both users)
  [ ] Test access to gmail.com (both users - should work)

Emergency Admin Account:
  [ ] emergency-admin@thenash.group created
  [ ] YubiKey configured as primary MFA
  [ ] Password stored in gopass
  [ ] CAA_Exempt group created
  [ ] emergency-admin added to CAA_Exempt
  [ ] Test login as emergency-admin (should work)
  [ ] Alert configured for emergency admin usage
  [ ] Physical YubiKey location documented (home safe)

Terraform State:
  [ ] Google Workspace provider configured
  [ ] Access Policy ID obtained
  [ ] All variables set in terraform.tfvars
  [ ] terraform plan executed successfully
  [ ] Manual configurations documented

Communication:
  [ ] All Guardians notified of upcoming CAA deployment
  [ ] Emergency procedures communicated
  [ ] Break-glass YubiKey locations confirmed
```

### CAA Deployment Day (Week 4)

**Deployment Sequence** (follow exactly):

```
Step 1: Deploy Terraform (9:00 AM)
  [ ] terraform apply (Access Levels only, no bindings)
  [ ] Verify Access Levels in Admin Console
  [ ] Verify CAA_Exempt exemption in each Access Level

Step 2: Manual Bindings (9:30 AM)
  [ ] Bind Trusted_Device to Gmail (test with jeffrey@ first)
  [ ] Wait 5 minutes, test access
  [ ] If successful, bind to Google Drive
  [ ] Wait 5 minutes, test access

Step 3: Admin Console Protection (10:00 AM)
  [ ] Bind Admin_Workstation to Admin Console
  [ ] Test guardian@ can access (from enrolled device)
  [ ] Test jeffrey@ cannot access Admin Console
  [ ] Test emergency-admin@ can access (bypass)

Step 4: Monitoring (10:30 AM)
  [ ] Check audit logs for CAA denials
  [ ] Verify alerts firing correctly
  [ ] Monitor Slack/email for access issues

Step 5: Rollback Test (11:00 AM)
  [ ] Log in as emergency-admin@
  [ ] Temporarily disable Trusted_Device binding for Gmail
  [ ] Verify access restored
  [ ] Re-enable binding
  [ ] Log out of emergency-admin@
```

---

## 8. Governance Updates

### Policies Requiring Amendment

**SEC-001 (Zero Trust Authentication)**:
- Add section: "Emergency Admin Exemption Strategy"
- Reference: CAA_Exempt group design

**SEC-003 (Least Privilege)**:
- Add section: "Machine Identity Differentiation"
- Reference: /Automation vs /Agentic policy differences

**SEC-004 (Security Baseline)**:
- Update section: "Multi-Factor Authentication Requirements"
- Clarify: Passkeys are FIDO2-compliant and acceptable

### ADRs to Create

**Immediately (Week 3)**:
```bash
cd the-covenant
../.org/tooling/generators/create-adr.sh "Break-Glass CAA Exemption Strategy"
../.org/tooling/generators/create-adr.sh "Passkey Authentication Policy Clarification"
../.org/tooling/generators/create-adr.sh "Machine-Identities OU Refactoring"
```

**After Implementation (Week 5)**:
```bash
../.org/tooling/generators/create-adr.sh "Hybrid Terraform Manual CAA Binding Approach"
../.org/tooling/generators/create-adr.sh "Chrome Browser Cloud Management Mandate"
```

---

## 9. Risk Assessment

### Risks Mitigated by These Refinements

| Original Risk | Mitigation | Residual Risk |
|---------------|------------|---------------|
| **Complete CAA lockout** | Emergency admin with CAA_Exempt | Physical YubiKey loss (store backup codes) |
| **Passkey blocked by policy** | Explicitly allow FIDO2 Passkeys | None (Passkeys are secure) |
| **Device not recognized** | Chrome Browser Cloud Management | User forgets to enroll device (documentation) |
| **Terraform binding failure** | Hybrid manual approach | Manual drift (monthly review) |
| **AI agents not planned** | Machine-Identities OU structure | Future policy definition needed |

### Residual Risks Requiring Ongoing Mitigation

**Physical YubiKey Loss** (Low Probability, High Impact):
- **Mitigation**: Store backup YubiKey in safe deposit box
- **Recovery**: Use backup codes from gopass

**Emergency Admin Compromise** (Very Low Probability, Critical Impact):
- **Mitigation**: Hardware key MFA, 1-hour session, alert on usage
- **Recovery**: Rotate password, revoke YubiKey, audit all actions

**Manual Configuration Drift** (Medium Probability, Low Impact):
- **Mitigation**: Monthly screenshot review, documented in manual-configurations.md
- **Recovery**: Re-apply correct configuration, investigate cause

---

## 10. Expert Validation: Response to Feedback

### Feedback Point 1: "Air Gap" in OU Topology ✅

**Your Comment**:
> "By isolating Guardians from Humans, you solve the biggest risk: 'Daily Driver Compromise.'"

**Response**: Confirmed. This is **intentional separation of privilege**. Guardian accounts are "break-glass" only. Jeffrey's day-to-day work happens in the Mentors OU with different policies.

### Feedback Point 2: SAML Attribute Mapping as Infrastructure ✅

**Your Comment**:
> "By mapping nash_role and nash_tier into the SAML assertion, you turn Google Workspace into a Policy Decision Point (PDP) for the entire estate."

**Response**: Exactly. This is **policy-as-data**. Google Groups are coarse-grained (teams), custom attributes are fine-grained (individual permissions). Together they enable **attribute-based access control (ABAC)** across clouds.

### Feedback Point 3: MTA-STS Hardening ✅

**Your Comment**:
> "Most organizations stop at DMARC. Going the extra mile for MTA-STS puts you in the top 1% globally."

**Response**: Acknowledged. MTA-STS forces TLS encryption **before** the email is sent, preventing downgrade attacks. DMARC alone can't protect against MitM during transport.

### Feedback Point 4: Passkey Evolution ✅ FIXED

**Your Comment**:
> "Ensure this configuration explicitly allows Passkeys as a valid FIDO2 authenticator."

**Response**: **FIXED in Section 2**. Policy now explicitly states:
- "Security Key (Hardware)" **includes** Passkeys
- FIDO2 compliance is the standard, not physical form factor

### Feedback Point 5: Chrome Enterprise Factor ✅ FIXED

**Your Comment**:
> "You need to install the Google Endpoint Verification extension and enroll your Chrome browser."

**Response**: **FIXED in Section 3**. Complete setup guide added:
- Chrome Browser Cloud Management enrollment steps
- Endpoint Verification extension installation
- Verification procedure in Admin Console

### Feedback Point 6: Break-Glass Gap ✅ FIXED

**Your Comment**:
> "If the Watcher is locked out, how do they enable the Break-Glass policy? You need the 'Golden Key.'"

**Response**: **FIXED in Section 1**. Complete implementation:
- `emergency-admin@thenash.group` account created
- `CAA_Exempt` group excludes emergency admin from all CAA policies
- YubiKey stored in physical safe
- Alert on usage
- Terraform configuration complete

### Feedback Point 7: Terraform Provider Maturity ✅ FIXED

**Your Comment**:
> "Binding Access Levels to Google Workspace Apps via Terraform is historically flaky."

**Response**: **FIXED in Section 4**. Hybrid approach documented:
- Terraform manages Access Level **definitions**
- Admin Console manages Access Level **bindings** to apps
- Document manual configurations in `manual-configurations.md`
- Monthly review for drift

### Feedback Point 8: Agentic Identity Future ✅ FIXED

**Your Comment**:
> "Rename /Service-Accounts to /Machine-Identities to be inclusive of future AI agents."

**Response**: **FIXED in Section 5**. Complete refactoring:
- `/Machine-Identities` root OU
- `/Automation` sub-OU (traditional bots)
- `/Agentic` sub-OU (AI agents, future)
- Custom attribute: `machine_type` field added
- Future policy: `OPS-012: Agentic Identity Management` planned

---

## 11. Final Implementation Checklist

### Week 3 (Foundation + Fixes)

**Day 1-2: Chrome Browser Setup**
- [ ] Install Chrome Enterprise on all Guardian/Mentor devices
- [ ] Generate enrollment token
- [ ] Enroll all devices
- [ ] Install Endpoint Verification extension
- [ ] Verify in Admin Console

**Day 3-4: Emergency Admin**
- [ ] Create emergency-admin@ account
- [ ] Configure YubiKey MFA
- [ ] Store credentials in gopass
- [ ] Create CAA_Exempt group
- [ ] Test login and verify exemption
- [ ] Configure monitoring/alerting

**Day 5: OU Refactoring**
- [ ] Rename /Service-Accounts → /Machine-Identities
- [ ] Create /Automation and /Agentic sub-OUs
- [ ] Update custom schema (machine_type field)
- [ ] Run terraform plan, review changes
- [ ] Run terraform apply

### Week 4 (CAA Deployment)

**Day 1: Terraform Deployment**
- [ ] Deploy Access Levels (Terraform)
- [ ] Verify CAA_Exempt exemptions
- [ ] Document Access Level IDs

**Day 2: Manual Bindings**
- [ ] Bind Trusted_Device → Gmail (test with jeffrey@)
- [ ] Wait, monitor, validate
- [ ] Bind Trusted_Device → Google Drive
- [ ] Wait, monitor, validate

**Day 3: Admin Console Protection**
- [ ] Bind Admin_Workstation → Admin Console
- [ ] Test guardian@ access
- [ ] Test jeffrey@ blocked
- [ ] Test emergency-admin@ bypass

**Day 4: Monitoring & Documentation**
- [ ] Review audit logs
- [ ] Screenshot all configurations
- [ ] Update manual-configurations.md
- [ ] Create ADRs

**Day 5: Rollback Test & Sign-Off**
- [ ] Simulate CAA lockout
- [ ] Test emergency admin recovery
- [ ] Document rollback procedure
- [ ] Sign-off by nash-group-watchers@

---

## Conclusion

These refinements address **critical operational gaps** that would cause production incidents:

1. **Break-Glass Lockout Prevention** → No more permanent lockouts
2. **Passkey Clarity** → Modern authentication supported
3. **Chrome Browser Enrollment** → Device trust actually works
4. **Terraform Limitations** → Pragmatic hybrid approach
5. **Future-Proof Naming** → Ready for AI agents

**Status**: Ready for Week 3 implementation with these fixes applied.

**Approval Requirements**: Covenant Level (these are security architecture changes)
- **The Watcher** (Security validation) - @nash-group-watchers
- **The Architect** (Implementation feasibility) - @nash-group-mentors

---

**Document Status**: CRITICAL OPERATIONAL FIXES - Implement Before CAA Deployment

**Next Steps**:
1. Review by nash-group-watchers@ and nash-group-mentors@
2. Create ADRs for break-glass strategy, Passkey policy, machine-identities refactoring
3. Begin Week 3 implementation with fixes applied
4. Update GOOGLE-WORKSPACE-ARCHITECTURE.md to reference this refinements document

---

*"From specification to operation. From theory to practice. These refinements ensure we don't lock ourselves out of our own empire."*

**Last Updated**: 2025-11-21
**Document Owner**: guardian@thenash.group
**Implementation Lead**: jeffrey@thenash.group (Mentor, Architect)
**Security Reviewer**: Expert Consultant (The Watcher)
