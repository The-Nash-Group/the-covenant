# SEC-001: Zero Trust Authentication

**Policy ID:** SEC-001
**Category:** Security
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Zero trust architecture **must** be implemented for all systems. Authenticate every request, authorize every action, audit every access. "Internal only" networks are a myth, and every request must prove its worthiness.

## Rationale

"Internal only" networks are a myth. We've seen internal threats, compromised credentials, and confused deputies. Every request must prove its worthiness:

- **Perimeter Illusion**: Network boundaries provide false security
- **Lateral Movement**: Compromised internal access enables widespread damage
- **Insider Threats**: Malicious or compromised internal users pose significant risk
- **Credential Compromise**: Stolen credentials bypass traditional perimeter defenses
- **Device Compromise**: Infected internal devices can access "trusted" networks
- **Supply Chain Attacks**: Third-party access bypasses perimeter controls

Zero trust assumes breach and requires continuous verification of every access request.

## Scope

**Applies To:**
- All internal services and applications
- All administrative interfaces and dashboards
- All API endpoints and service-to-service communication
- All remote access and VPN connections
- All third-party integrations and contractor access

**Exceptions:**
- Public-facing marketing websites (with appropriate security controls)
- Open source documentation sites (with content-only access)

## Implementation

### Technical Enforcement

Cloudflare Access configuration for internal services:

```hcl
# the-citadel/terraform/cloudflare/access.tf
resource "cloudflare_access_application" "internal_services" {
  zone_id          = data.cloudflare_zone.nash_group.id
  name             = "Internal Services"
  domain           = "*.internal.thenash.group"
  type             = "self_hosted"
  session_duration = "8h"

  # Require authentication for all internal services
  policies = [
    cloudflare_access_policy.internal_policy.id
  ]
}

resource "cloudflare_access_policy" "internal_policy" {
  application_id = cloudflare_access_application.internal_services.id
  name           = "Nash Group Internal Access"
  precedence     = 1
  decision       = "allow"

  include {
    group = [data.cloudflare_access_group.nash_group_employees.id]
  }

  require {
    # Multi-factor authentication required
    common_name = "*.nash.group"

    # Device certificate required
    certificate = true
  }

  session_duration = "8h"
}

# Device certificate requirements
resource "cloudflare_access_ca_certificate" "nash_group_devices" {
  zone_id        = data.cloudflare_zone.nash_group.id
  application_id = cloudflare_access_application.internal_services.id
}
```

Service-to-service authentication:

```hcl
# Service mesh authentication
resource "cloudflare_access_service_token" "service_tokens" {
  for_each = var.internal_services

  name     = "${each.key}-service-token"
  duration = "8760h"  # 1 year, with rotation policy
}

# API Gateway with service authentication
resource "cloudflare_access_application" "api_gateway" {
  zone_id = data.cloudflare_zone.nash_group.id
  name    = "API Gateway"
  domain  = "api.internal.thenash.group"

  policies = [
    cloudflare_access_policy.service_to_service.id,
    cloudflare_access_policy.authenticated_users.id
  ]
}
```

### Automated Validation

**Authentication Verification:**
- All requests require valid authentication tokens
- Token validation at application gateway layer
- Automated token rotation and refresh
- Session management with appropriate timeouts

**Authorization Enforcement:**
- Role-based access control (RBAC) for all resources
- Principle of least privilege automatically enforced
- Dynamic permission evaluation based on context
- Regular access review and permission auditing

**Audit Trail Requirements:**
- All authentication attempts logged and monitored
- Authorization decisions tracked with context
- Access pattern analysis for anomaly detection
- Comprehensive audit trail for compliance

### Human Process

1. **Identity Provisioning**: Secure onboarding with multi-factor authentication
2. **Access Requests**: Formal approval process for resource access
3. **Regular Reviews**: Quarterly access review and cleanup
4. **Incident Response**: Rapid response to authentication anomalies
5. **Training**: Security awareness training on zero trust principles

## Authentication Standards

### Multi-Factor Authentication Requirements

**Required Factors:**
- Something you know (password/passphrase)
- Something you have (device certificate, hardware token, or phone)
- Something you are (biometric where available)

**Implementation:**
```hcl
resource "cloudflare_access_policy" "mfa_required" {
  include {
    group = ["nash-group-employees"]
  }

  require {
    # Device certificate
    certificate = true

    # Additional MFA via identity provider
    login_method = ["saml", "oidc"]
  }

  # Re-authentication required for sensitive operations
  session_duration = "4h"
}
```

### Device Trust Requirements

**Device Registration:**
- All devices must be registered with device certificates
- Corporate-managed devices receive enhanced trust
- Personal devices require additional verification steps
- Compromised devices can be immediately revoked

**Certificate Management:**
- Automated certificate provisioning and renewal
- Certificate revocation for compromised or retired devices
- Regular certificate rotation policy
- Certificate pinning for critical services

## Authorization Framework

### Role-Based Access Control

**Standard Roles:**
- **Reader**: Read-only access to assigned resources
- **Contributor**: Read/write access to specific services
- **Maintainer**: Administrative access to service domains
- **Administrator**: Full access to organizational resources

**Dynamic Authorization:**
```go
// Authorization middleware example
func authorizationMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Extract user identity from authenticated context
        user := getUserFromContext(r.Context())

        // Evaluate permissions dynamically
        if !hasPermission(user, r.Method, r.URL.Path) {
            http.Error(w, "Forbidden", http.StatusForbidden)
            return
        }

        // Log authorization decision
        logAuthzDecision(user, r.Method, r.URL.Path, "allowed")

        next.ServeHTTP(w, r)
    })
}
```

### Resource-Level Permissions

**Granular Access Control:**
- Repository-level access control via GitHub teams
- Service-level access control via Cloudflare Access
- Database-level access control via role-based schemas
- API-level access control via gateway policies

## Compliance Verification

**Automated Checks:**
- Authentication bypass attempt detection
- Unauthorized access pattern monitoring
- Session management and timeout enforcement
- Certificate validity and rotation verification

**Manual Audits:**
- Monthly access review and cleanup
- Quarterly security assessment of authentication systems
- Annual penetration testing of zero trust implementation

**Reporting:**
- Real-time dashboard of authentication and authorization events
- Weekly access pattern analysis and anomaly reports
- Monthly security posture assessment including zero trust maturity

## Emergency Procedures

### Credential Compromise Response

**Immediate Actions (within 15 minutes):**
1. **Revoke Access**: Immediately disable compromised credentials
2. **Assess Impact**: Determine scope of potential unauthorized access
3. **Monitor Activity**: Enhanced monitoring for suspicious activity
4. **Communicate**: Alert security team and relevant stakeholders

**Investigation and Recovery:**
1. **Forensic Analysis**: Detailed investigation of compromise scope
2. **System Hardening**: Additional security controls for affected systems
3. **Credential Rotation**: Force rotation of potentially affected credentials
4. **Process Improvement**: Update procedures to prevent similar incidents

### Zero Trust Bypass Procedures

**Emergency Access:**
- Break-glass procedures for critical system access during authentication failures
- Temporary bypass with enhanced logging and immediate review
- Multi-person authorization for emergency access grants
- Mandatory post-incident review and system restoration

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 9: Trust, but Verify Everything](../the-covenant/PRINCIPLES.md#principle-9-trust-but-verify-everything)
- **Governance Authority:** [GOVERNANCE.md - Security Authority](../the-covenant/GOVERNANCE.md#the-watchers-administrators)
- **Implementation:** `the-citadel/terraform/cloudflare/access.tf`
- **Emergency Procedures:** [GOV-003 Break-Glass Procedures](./gov-003-break-glass.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 9: Trust, but Verify Everything
