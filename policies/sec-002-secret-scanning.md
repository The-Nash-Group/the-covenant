# SEC-002: Secret Scanning

**Policy ID:** SEC-002
**Category:** Security
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

No secret, token, password, or key **shall** ever be committed to Git, even in encrypted form within the repository. Push protection **must** be enabled to prevent secret commits.

## Rationale

A secret in Git is compromised forever. We've seen repositories cloned by contractors, forked publicly by accident, and indexed by search engines. Git remembers everything, and what goes in never truly comes out:

- **Permanent Exposure**: Git history preserves secrets even after "removal"
- **Cloning Risk**: Every repository clone spreads the compromise
- **Search Engine Indexing**: Public repositories get scraped and indexed
- **Contractor Access**: Temporary access becomes permanent exposure
- **Fork Proliferation**: Forks may not remove secrets even when original does
- **Backup Exposure**: Repository backups preserve compromised history

Even encrypted secrets in the repository are vulnerable to future cryptographic breaks and key compromise.

## Scope

**Applies To:**
- All repositories under The Nash Group organization
- All commits, branches, and pull requests
- All file types including configuration files, scripts, and documentation
- Infrastructure code, application code, and documentation repositories
- Personal forks and temporary branches

**Exceptions:**
- Test fixtures with clearly fake/example credentials (must be documented as such)
- Public API keys with no security implications (must be verified as safe)

## Implementation

### Technical Enforcement

In `the-citadel/terraform/github/rulesets.tf`:

```hcl
resource "github_repository_ruleset" "secret_scanning" {
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~ALL"]  # Apply to all branches
    }
  }

  rules {
    secret_scanning {
      enable_push_protection = true
    }
  }
}

# Organization-level secret scanning
resource "github_organization_settings" "security" {
  secret_scanning_enabled = true
  secret_scanning_push_protection_enabled = true

  # Custom patterns for Nash Group specific secrets
  secret_scanning_push_protection_custom_link = "https://security.thenash.group/secret-remediation"
}
```

Organization secret scanning configuration:

```hcl
resource "github_organization_secret_scanning_custom_pattern" "nash_group_patterns" {
  pattern = "nash_[a-zA-Z0-9]{32}"
  secret_type = "nash_group_api_key"
}

resource "github_organization_secret_scanning_custom_pattern" "private_keys" {
  pattern = "-----BEGIN [A-Z ]+PRIVATE KEY-----"
  secret_type = "private_key_material"
}
```

### Automated Validation

**GitHub Secret Scanning:**
- Built-in detection for common secret patterns
- Custom patterns for Nash Group specific tokens
- Push protection blocks commits containing secrets
- Historical repository scanning for existing secrets

**CI/CD Integration:**
- Pre-commit hooks scan for secrets locally
- CI pipeline includes additional secret detection tools
- Failed secret scans block PR merging
- Automated secret rotation when possible

**Continuous Monitoring:**
- Regular scans of all repositories for new secret patterns
- Monitoring of public leak databases (GitHub, GitLab, etc.)
- Alert system for discovered secrets requiring immediate action

### Human Process

1. **Developer Education**: Training on secret management best practices
2. **Secret Discovery Response**: Immediate action protocol for found secrets
3. **Secret Rotation**: Automatic or manual rotation of compromised secrets
4. **Access Review**: Regular audit of who has access to secret stores
5. **Incident Response**: Documented procedure for secret exposure incidents

## Secret Management Alternatives

### Approved Secret Storage

**Environment Variables:**
- Runtime injection via CI/CD systems
- Environment-specific configuration
- No secrets in Docker images or config files

**Secret Management Services:**
- HashiCorp Vault for dynamic secrets
- GitHub Secrets for CI/CD workflows
- Cloud provider secret stores (AWS Secrets Manager, etc.)

**Runtime Configuration:**
- Secrets mounted at runtime via orchestration
- Service mesh secret injection
- Init containers for secret retrieval

### Development Practices

**Local Development:**
- `.env` files in `.gitignore`
- Development-specific placeholder values
- Local secret management tools

**Testing:**
- Mock services for external dependencies
- Test-specific non-production credentials
- Synthetic data that doesn't require real secrets

## Compliance Verification

**Automated Checks:**
- GitHub push protection prevents secret commits
- CI/CD pipelines scan for secrets on every build
- Regular historical scans of all repositories
- Integration with external secret leak monitoring

**Manual Audits:**
- Monthly review of secret scanning alerts and resolutions
- Quarterly assessment of secret management practices
- Annual penetration testing including secret exposure vectors

**Reporting:**
- Real-time dashboard of secret scanning status
- Weekly reports on secret scanning alerts and remediation
- Trend analysis of secret exposure patterns and prevention

## Incident Response

### Secret Exposure Response

**Immediate Actions (within 1 hour):**
1. **Revoke/Rotate**: Immediately invalidate the exposed secret
2. **Assess Impact**: Determine what the secret could access
3. **Monitor Usage**: Check logs for unauthorized usage
4. **Communicate**: Alert relevant teams and stakeholders

**Follow-up Actions (within 24 hours):**
1. **Root Cause**: Investigate how secret was committed
2. **Remediation**: Update processes to prevent recurrence
3. **Documentation**: Record incident and lessons learned
4. **Training Update**: Enhance developer education if needed

### Git History Cleaning

**For Confirmed Secret Exposure:**
1. **Never rely on Git history rewriting** as primary remediation
2. **Treat secret as permanently compromised** regardless of history cleaning
3. **Document cleaning attempt** but assume secret is public
4. **Focus on impact mitigation** rather than history sanitization

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 6: Secrets Are Never Committed](../the-covenant/PRINCIPLES.md#principle-6-secrets-are-never-committed)
- **Governance Authority:** [GOVERNANCE.md - Security Authority](../the-covenant/GOVERNANCE.md#the-watchers-administrators)
- **Implementation:** `the-citadel/terraform/github/rulesets.tf`
- **Incident Response:** [OPS-010 Emergency Response Procedures](./ops-010-emergency-response.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 6: Secrets Are Never Committed
