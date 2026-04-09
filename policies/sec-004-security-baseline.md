# SEC-004: Security Baseline Requirements

**Policy ID:** SEC-004
**Category:** Security
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

All systems and applications **must** implement a comprehensive security baseline covering authentication, encryption, vulnerability management, and incident response. Security is not an add-on but a foundational requirement.

## Rationale

Security threats evolve constantly and require proactive, comprehensive defense strategies. A standardized security baseline ensures consistent protection across all systems:

- **Threat Landscape Evolution**: New vulnerabilities and attack vectors emerge continuously
- **Compliance Requirements**: Regulatory and industry standards mandate specific security controls
- **Data Protection**: Customer and business data requires multi-layered protection
- **Business Continuity**: Security incidents can disrupt operations and damage reputation
- **Supply Chain Security**: Dependencies and third-party integrations introduce security risks
- **Insider Threats**: Internal access requires monitoring and controls

Comprehensive security baseline enables proactive threat prevention, rapid incident response, and regulatory compliance across the organization.

## Scope

**Applies To:**
- All applications and services deployed by The Nash Group
- All infrastructure components and network configurations
- All data storage and processing systems
- All third-party integrations and dependencies
- All development and deployment processes
- All user access management and authentication systems

**Exceptions:**
- Development and testing environments (reduced requirements)
- Public documentation and marketing websites (limited baseline)
- Open source projects without sensitive data (basic requirements)

## Implementation

### Technical Enforcement

Security baseline automation and monitoring:

```hcl
# terraform/security/baseline.tf
resource "github_repository_ruleset" "security_baseline" {
  name        = "Security Baseline Requirements"
  repository  = github_repository.service.name
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
  }

  rules {
    required_status_checks {
      strict_required_status_checks_policy = true
      required_status_checks = [
        { context = "security/vulnerability-scan" },
        { context = "security/dependency-audit" },
        { context = "security/secrets-detection" },
        { context = "security/compliance-check" },
        { context = "security/container-scan" }
      ]
    }
  }

  labels = {
    "nash.group/policy"    = "sec-004"
    "nash.group/component" = "security-baseline"
    "nash.group/team"      = var.team_name
  }
}

# Security monitoring and alerting
resource "monitoring_alert" "security_baseline_violation" {
  name        = "Security Baseline Violation"
  description = "Security baseline requirement violated"

  labels = {
    "nash.group/policy"   = "sec-004"
    "nash.group/service"  = var.service_name
    "nash.group/severity" = "high"
  }

  annotations = {
    summary     = "Security baseline violation detected for ${var.service_name}"
    description = "{{ $labels.violation_type }}: {{ $labels.details }}"
    runbook_url = "https://runbooks.nash.group/security-baseline-violation"
  }

  query = <<-EOT
    security_baseline_violations_total > 0
  EOT

  for_duration = "0m"  # Immediate alert
}

# Cloudflare security configuration
resource "cloudflare_zone_settings_override" "security_baseline" {
  zone_id = var.cloudflare_zone_id

  settings {
    # Security level
    security_level = "high"

    # SSL/TLS enforcement
    ssl = "strict"
    min_tls_version = "1.2"
    tls_1_3 = "on"

    # Security headers
    security_header {
      enabled = true
    }

    # Bot management
    bot_management {
      enabled = true
    }

    # Rate limiting
    challenge_ttl = 1800
  }
}
```

Automated security scanning and validation:

```yaml
# .github/workflows/security-baseline.yml
name: Security Baseline Validation
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'  # Daily security scan

jobs:
  vulnerability-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Dependency Vulnerability Scan
        run: |
          echo "Scanning dependencies for vulnerabilities..."

          # Node.js dependencies
          if [ -f package.json ]; then
            npm audit --audit-level moderate
            npx audit-ci --moderate
          fi

          # Python dependencies
          if [ -f requirements.txt ]; then
            pip install safety
            safety check -r requirements.txt
          fi

          # Go dependencies
          if [ -f go.mod ]; then
            go install golang.org/x/vuln/cmd/govulncheck@latest
            govulncheck ./...
          fi

      - name: Container Security Scan
        if: hashFiles('Dockerfile') != ''
        run: |
          echo "Scanning container for vulnerabilities..."

          # Build container
          docker build -t security-scan:latest .

          # Scan with Trivy
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
            aquasec/trivy:latest image --severity HIGH,CRITICAL security-scan:latest

      - name: Static Application Security Testing (SAST)
        run: |
          echo "Running static security analysis..."

          # Semgrep security analysis
          docker run --rm -v "${PWD}:/src" returntocorp/semgrep \
            --config=auto --severity=ERROR /src

          # CodeQL analysis (if supported)
          if [ -f .github/codeql/codeql-config.yml ]; then
            echo "CodeQL analysis configured - will run separately"
          fi

      - name: Secrets Detection
        run: |
          echo "Scanning for exposed secrets..."

          # GitLeaks scan
          docker run --rm -v "${PWD}:/path" zricethezav/gitleaks:latest \
            detect --source="/path" --verbose

          # TruffleHog scan
          docker run --rm -v "${PWD}:/pwd" trufflesecurity/trufflehog:latest \
            filesystem /pwd --only-verified

      - name: Security Configuration Check
        run: |
          echo "Validating security configuration..."

          # Check for security headers in web applications
          if [ -f package.json ] && grep -q "express" package.json; then
            echo "Checking Express.js security configuration..."
            ./scripts/check-express-security.js
          fi

          # Check for secure defaults
          ./scripts/check-security-defaults.sh

      - name: Compliance Check
        run: |
          echo "Running compliance validation..."

          # OWASP security requirements
          ./scripts/owasp-compliance-check.sh

          # Industry-specific compliance
          if [ -f .compliance/requirements.yml ]; then
            ./scripts/compliance-validation.py .compliance/requirements.yml
          fi

  penetration-testing:
    if: github.event_name == 'schedule'  # Only on scheduled runs
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Automated Penetration Testing
        run: |
          echo "Running automated penetration tests..."

          # OWASP ZAP baseline scan
          if [ -f docker-compose.yml ]; then
            docker-compose up -d
            sleep 30  # Wait for services to start

            docker run --rm -v $(pwd):/zap/wrk/:rw \
              owasp/zap2docker-stable zap-baseline.py \
              -t http://host.docker.internal:3000 \
              -J zap-report.json

            docker-compose down
          fi

      - name: Security Metrics Collection
        run: |
          echo "Collecting security metrics..."

          # Generate security scorecard
          python3 scripts/security-scorecard.py > security-metrics.json

          # Upload to monitoring system
          curl -X POST "$METRICS_ENDPOINT/security-baseline" \
            -H "Content-Type: application/json" \
            -d @security-metrics.json
        env:
          METRICS_ENDPOINT: ${{ secrets.METRICS_ENDPOINT }}
```

### Automated Validation

**Security Controls Framework:**
```python
#!/usr/bin/env python3
# scripts/security-baseline-validator.py
"""
Validates security baseline compliance across applications
"""

import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List

class SecurityBaselineValidator:
    def __init__(self):
        self.required_controls = {
            'authentication': {
                'multi_factor_auth': {'required': True, 'weight': 10},
                'session_management': {'required': True, 'weight': 8},
                'password_policy': {'required': True, 'weight': 6}
            },
            'encryption': {
                'data_at_rest': {'required': True, 'weight': 10},
                'data_in_transit': {'required': True, 'weight': 10},
                'key_management': {'required': True, 'weight': 8}
            },
            'access_control': {
                'role_based_access': {'required': True, 'weight': 9},
                'least_privilege': {'required': True, 'weight': 8},
                'access_logging': {'required': True, 'weight': 7}
            },
            'monitoring': {
                'security_logging': {'required': True, 'weight': 9},
                'intrusion_detection': {'required': True, 'weight': 8},
                'vulnerability_monitoring': {'required': True, 'weight': 7}
            },
            'incident_response': {
                'response_plan': {'required': True, 'weight': 8},
                'automated_detection': {'required': True, 'weight': 7},
                'forensic_capability': {'required': True, 'weight': 6}
            }
        }

        self.compliance_frameworks = {
            'owasp_top_10': self._owasp_requirements(),
            'nist_cybersecurity': self._nist_requirements(),
            'iso_27001': self._iso_requirements()
        }

    def validate_application(self, app_path: Path) -> Dict:
        """Validate application against security baseline"""

        results = {
            'application': app_path.name,
            'overall_score': 0,
            'control_results': {},
            'compliance_status': {},
            'recommendations': []
        }

        total_possible_score = 0
        total_actual_score = 0

        # Validate each control category
        for category, controls in self.required_controls.items():
            category_results = self._validate_category(app_path, category, controls)
            results['control_results'][category] = category_results

            # Calculate scores
            category_possible = sum(c['weight'] for c in controls.values())
            category_actual = sum(r['score'] for r in category_results.values())

            total_possible_score += category_possible
            total_actual_score += category_actual

        # Calculate overall score
        results['overall_score'] = (total_actual_score / total_possible_score) * 100

        # Check compliance frameworks
        for framework, requirements in self.compliance_frameworks.items():
            compliance_score = self._check_framework_compliance(results, requirements)
            results['compliance_status'][framework] = compliance_score

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)

        return results

    def _validate_category(self, app_path: Path, category: str, controls: Dict) -> Dict:
        """Validate specific security control category"""

        category_results = {}

        for control_name, control_config in controls.items():
            validation_method = getattr(self, f'_check_{category}_{control_name}', None)

            if validation_method:
                result = validation_method(app_path)
                category_results[control_name] = {
                    'implemented': result['implemented'],
                    'score': result['score'] * control_config['weight'],
                    'details': result['details'],
                    'evidence': result.get('evidence', [])
                }
            else:
                category_results[control_name] = {
                    'implemented': False,
                    'score': 0,
                    'details': f'Validation method not implemented for {control_name}',
                    'evidence': []
                }

        return category_results

    def _check_authentication_multi_factor_auth(self, app_path: Path) -> Dict:
        """Check for multi-factor authentication implementation"""

        evidence = []
        implemented = False

        # Check for MFA libraries
        if (app_path / 'package.json').exists():
            with open(app_path / 'package.json') as f:
                package = json.load(f)
                mfa_libs = ['speakeasy', 'otplib', '@aws-sdk/client-cognito', 'passport-totp']
                found_libs = [lib for lib in mfa_libs if lib in package.get('dependencies', {})]
                if found_libs:
                    implemented = True
                    evidence.extend(found_libs)

        # Check configuration files
        config_files = ['config/auth.yml', 'config/security.yml', '.env.example']
        for config_file in config_files:
            if (app_path / config_file).exists():
                with open(app_path / config_file) as f:
                    content = f.read()
                    if 'mfa' in content.lower() or 'two_factor' in content.lower():
                        implemented = True
                        evidence.append(f'MFA configuration in {config_file}')

        return {
            'implemented': implemented,
            'score': 1.0 if implemented else 0.0,
            'details': 'Multi-factor authentication configured' if implemented else 'MFA not detected',
            'evidence': evidence
        }

    def _check_encryption_data_in_transit(self, app_path: Path) -> Dict:
        """Check for TLS/SSL encryption configuration"""

        evidence = []
        implemented = False

        # Check for HTTPS enforcement
        nginx_configs = list(app_path.glob('**/nginx.conf')) + list(app_path.glob('**/*.nginx'))
        for config in nginx_configs:
            with open(config) as f:
                content = f.read()
                if 'ssl_certificate' in content and 'return 301 https' in content:
                    implemented = True
                    evidence.append(f'HTTPS redirect in {config.name}')

        # Check application configuration
        if (app_path / 'package.json').exists():
            # Check for HTTPS middleware
            tls_libs = ['helmet', 'express-force-ssl', 'koa-force-ssl']
            with open(app_path / 'package.json') as f:
                package = json.load(f)
                found_libs = [lib for lib in tls_libs if lib in package.get('dependencies', {})]
                if found_libs:
                    implemented = True
                    evidence.extend(found_libs)

        return {
            'implemented': implemented,
            'score': 1.0 if implemented else 0.0,
            'details': 'TLS encryption configured' if implemented else 'TLS configuration not detected',
            'evidence': evidence
        }

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate security improvement recommendations"""

        recommendations = []

        # Check overall score
        if results['overall_score'] < 80:
            recommendations.append("Overall security score below 80% - comprehensive security review recommended")

        # Check specific control categories
        for category, controls in results['control_results'].items():
            category_score = sum(c['score'] for c in controls.values())
            max_score = sum(self.required_controls[category][k]['weight'] for k in controls.keys())

            if category_score / max_score < 0.8:
                recommendations.append(f"Improve {category} controls - current implementation insufficient")

        # Check compliance frameworks
        for framework, score in results['compliance_status'].items():
            if score < 0.9:
                recommendations.append(f"Address {framework} compliance gaps - current score: {score:.0%}")

        return recommendations

    def _owasp_requirements(self) -> Dict:
        """OWASP Top 10 security requirements"""
        return {
            'injection_prevention': {'controls': ['input_validation', 'parameterized_queries']},
            'broken_authentication': {'controls': ['multi_factor_auth', 'session_management']},
            'sensitive_data_exposure': {'controls': ['data_encryption', 'secure_storage']},
            'xml_external_entities': {'controls': ['xml_parsing_security', 'input_validation']},
            'broken_access_control': {'controls': ['role_based_access', 'access_logging']},
            'security_misconfiguration': {'controls': ['secure_defaults', 'configuration_management']},
            'cross_site_scripting': {'controls': ['output_encoding', 'content_security_policy']},
            'insecure_deserialization': {'controls': ['input_validation', 'integrity_checks']},
            'vulnerable_components': {'controls': ['dependency_scanning', 'update_management']},
            'logging_monitoring': {'controls': ['security_logging', 'incident_detection']}
        }

    def _nist_requirements(self) -> Dict:
        """NIST Cybersecurity Framework requirements"""
        return {
            'identify': {'controls': ['asset_inventory', 'risk_assessment']},
            'protect': {'controls': ['access_control', 'data_security', 'training']},
            'detect': {'controls': ['monitoring', 'detection_processes']},
            'respond': {'controls': ['response_planning', 'communications']},
            'recover': {'controls': ['recovery_planning', 'improvements']}
        }

    def _iso_requirements(self) -> Dict:
        """ISO 27001 security requirements"""
        return {
            'information_security_policies': {'controls': ['policy_management']},
            'organization_security': {'controls': ['security_organization']},
            'human_resource_security': {'controls': ['security_training']},
            'asset_management': {'controls': ['asset_inventory', 'data_classification']},
            'access_control': {'controls': ['user_access_management', 'privileged_access']},
            'cryptography': {'controls': ['encryption_management', 'key_management']},
            'physical_security': {'controls': ['facility_security', 'equipment_protection']},
            'operations_security': {'controls': ['operational_procedures', 'malware_protection']},
            'communications_security': {'controls': ['network_security', 'information_transfer']},
            'system_development': {'controls': ['secure_development', 'security_testing']},
            'supplier_relationships': {'controls': ['supplier_assessment', 'service_delivery']},
            'incident_management': {'controls': ['incident_response', 'evidence_collection']},
            'business_continuity': {'controls': ['continuity_planning', 'redundancy']},
            'compliance': {'controls': ['compliance_monitoring', 'technical_compliance']}
        }

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python security-baseline-validator.py <application-path>")
        sys.exit(1)

    validator = SecurityBaselineValidator()
    app_path = Path(sys.argv[1])
    results = validator.validate_application(app_path)

    print(json.dumps(results, indent=2))

    # Exit with error code if security score is too low
    if results['overall_score'] < 70:
        print(f"Security baseline validation failed: {results['overall_score']:.1f}% < 70%")
        sys.exit(1)

    print(f"Security baseline validation passed: {results['overall_score']:.1f}%")
```

### Human Process

1. **Security Planning**: Integrate security requirements into project planning phase
2. **Secure Development**: Follow secure coding practices and security testing
3. **Security Reviews**: Regular security assessments and penetration testing
4. **Incident Response**: Rapid response to security incidents and vulnerabilities
5. **Continuous Monitoring**: Ongoing security monitoring and threat intelligence

## Security Control Categories

### Authentication and Identity Management

**Required Controls:**
```yaml
authentication_controls:
  multi_factor_authentication:
    description: "All user accounts must use MFA"
    implementation: "TOTP, SMS, or hardware tokens"
    exceptions: "Service accounts with alternative controls"

  session_management:
    description: "Secure session handling and timeout"
    requirements:
      - "Session tokens must be cryptographically secure"
      - "Sessions must expire after inactivity"
      - "Session fixation protection required"

  password_policy:
    description: "Strong password requirements"
    requirements:
      - "Minimum 12 characters"
      - "Mix of uppercase, lowercase, numbers, symbols"
      - "No common passwords or patterns"
      - "Password history enforcement"

  account_lockout:
    description: "Protection against brute force attacks"
    requirements:
      - "Lock account after 5 failed attempts"
      - "Exponential backoff for unlock attempts"
      - "Notification of lockout events"
```

**Implementation Example:**
```javascript
// Authentication middleware with security baseline
const authMiddleware = {
  // Multi-factor authentication
  requireMFA: (req, res, next) => {
    if (!req.user.mfaVerified) {
      return res.status(401).json({
        error: 'MFA_REQUIRED',
        message: 'Multi-factor authentication required'
      });
    }
    next();
  },

  // Session security
  configureSession: {
    secret: process.env.SESSION_SECRET,
    name: 'sessionId',
    cookie: {
      secure: process.env.NODE_ENV === 'production',
      httpOnly: true,
      maxAge: 30 * 60 * 1000, // 30 minutes
      sameSite: 'strict'
    },
    resave: false,
    saveUninitialized: false
  },

  // Rate limiting for auth endpoints
  authRateLimit: rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 attempts per window
    message: 'Too many authentication attempts',
    standardHeaders: true,
    legacyHeaders: false
  })
};
```

### Encryption and Data Protection

**Encryption Requirements:**
```yaml
encryption_standards:
  data_at_rest:
    algorithm: "AES-256-GCM or ChaCha20-Poly1305"
    key_management: "Hardware Security Module or AWS KMS"
    key_rotation: "Annual rotation minimum"

  data_in_transit:
    protocol: "TLS 1.3 preferred, TLS 1.2 minimum"
    cipher_suites: "AEAD ciphers only"
    certificate_validation: "Full chain validation required"

  application_secrets:
    storage: "Encrypted environment variables or secret manager"
    access_control: "Role-based access to secrets"
    audit_logging: "All secret access logged"

  database_encryption:
    storage: "Transparent Data Encryption (TDE)"
    backups: "Encrypted backup storage"
    connections: "Encrypted client connections"
```

**Implementation Standards:**
```python
# Database encryption configuration
DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
        'OPTIONS': {
            'sslmode': 'require',
            'sslcert': '/path/to/client-cert.pem',
            'sslkey': '/path/to/client-key.pem',
            'sslrootcert': '/path/to/ca-cert.pem',
        }
    }
}

# Application-level encryption
from cryptography.fernet import Fernet
import os

class SecureDataHandler:
    def __init__(self):
        # Key should be stored in secure key management system
        self.key = os.environ['ENCRYPTION_KEY'].encode()
        self.cipher_suite = Fernet(self.key)

    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data before storage"""
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data after retrieval"""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
```

### Vulnerability Management

**Vulnerability Scanning Requirements:**
```yaml
vulnerability_management:
  dependency_scanning:
    frequency: "Daily automated scans"
    tools: ["npm audit", "safety", "govulncheck", "Dependabot"]
    action_required: "High/Critical within 7 days"

  container_scanning:
    frequency: "Every build and weekly"
    tools: ["Trivy", "Clair", "Anchore"]
    base_image_policy: "Official images only, updated monthly"

  static_analysis:
    frequency: "Every commit"
    tools: ["Semgrep", "CodeQL", "SonarQube"]
    coverage: "Security rules and quality gates"

  dynamic_analysis:
    frequency: "Weekly for critical services"
    tools: ["OWASP ZAP", "Burp Suite", "Nessus"]
    scope: "All externally accessible endpoints"

  penetration_testing:
    frequency: "Quarterly for critical systems"
    scope: "External and internal network assessment"
    requirements: "Third-party security assessment"
```

**Automated Vulnerability Response:**
```bash
#!/bin/bash
# scripts/vulnerability-response.sh
# Automated response to vulnerability detection

set -euo pipefail

VULNERABILITY_SEVERITY="${1:-}"
COMPONENT_NAME="${2:-}"
CVE_ID="${3:-}"

if [ -z "$VULNERABILITY_SEVERITY" ] || [ -z "$COMPONENT_NAME" ]; then
    echo "Usage: $0 <severity> <component> [cve-id]"
    echo "Severity: CRITICAL, HIGH, MEDIUM, LOW"
    exit 1
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

create_security_issue() {
    local title="Security Vulnerability: $COMPONENT_NAME ($VULNERABILITY_SEVERITY)"
    local labels="security,vulnerability,$VULNERABILITY_SEVERITY"

    gh issue create \
        --title "$title" \
        --label "$labels" \
        --body "## Vulnerability Details

**Component**: $COMPONENT_NAME
**Severity**: $VULNERABILITY_SEVERITY
**CVE**: ${CVE_ID:-Not specified}

## Response Timeline
- **CRITICAL**: 24 hours
- **HIGH**: 7 days
- **MEDIUM**: 30 days
- **LOW**: Next maintenance window

## Action Required
1. Assess impact on our systems
2. Plan remediation approach
3. Test fixes in staging environment
4. Deploy fix with monitoring
5. Verify vulnerability resolved

See [SEC-004 Security Baseline](policies/sec-004-security-baseline.md) for detailed procedures."

    log "Created security issue for $COMPONENT_NAME vulnerability"
}

notify_security_team() {
    local webhook_url="$SECURITY_ALERTS_WEBHOOK"

    if [ "$VULNERABILITY_SEVERITY" = "CRITICAL" ] || [ "$VULNERABILITY_SEVERITY" = "HIGH" ]; then
        curl -X POST "$webhook_url" \
            -H 'Content-Type: application/json' \
            --data "{
                \"text\": \"🚨 $VULNERABILITY_SEVERITY vulnerability detected in $COMPONENT_NAME\",
                \"attachments\": [{
                    \"color\": \"danger\",
                    \"fields\": [{
                        \"title\": \"Component\",
                        \"value\": \"$COMPONENT_NAME\",
                        \"short\": true
                    }, {
                        \"title\": \"Severity\",
                        \"value\": \"$VULNERABILITY_SEVERITY\",
                        \"short\": true
                    }, {
                        \"title\": \"CVE\",
                        \"value\": \"${CVE_ID:-Not specified}\",
                        \"short\": true
                    }]
                }]
            }"
    fi
}

schedule_remediation() {
    case $VULNERABILITY_SEVERITY in
        "CRITICAL")
            # Immediate response required
            log "CRITICAL vulnerability - immediate response required"
            # Would integrate with on-call system
            ;;
        "HIGH")
            # 7-day response timeline
            log "HIGH severity vulnerability - 7-day response timeline"
            ;;
        "MEDIUM")
            # 30-day response timeline
            log "MEDIUM severity vulnerability - 30-day response timeline"
            ;;
        "LOW")
            # Next maintenance window
            log "LOW severity vulnerability - schedule for next maintenance"
            ;;
    esac
}

# Main execution
log "Processing vulnerability: $COMPONENT_NAME ($VULNERABILITY_SEVERITY)"

create_security_issue
notify_security_team
schedule_remediation

log "Vulnerability response initiated for $COMPONENT_NAME"
```

### Network Security

**Network Security Controls:**
```yaml
network_security:
  firewall_rules:
    default_policy: "DENY"
    allowed_protocols: ["HTTPS (443)", "SSH (22)", "custom ports as needed"]
    monitoring: "All connection attempts logged"

  network_segmentation:
    production_isolation: "Production network isolated from development"
    service_isolation: "Micro-segmentation between services"
    database_access: "Database access restricted to application layer"

  intrusion_detection:
    monitoring: "Real-time network traffic analysis"
    alerting: "Immediate notification of suspicious activity"
    response: "Automated blocking of malicious IPs"

  vpn_requirements:
    protocol: "WireGuard or OpenVPN"
    authentication: "Certificate-based authentication"
    logging: "All VPN connections logged and monitored"
```

**Cloudflare Security Configuration:**
```hcl
# Cloudflare WAF and security rules
resource "cloudflare_ruleset" "security_baseline" {
  zone_id     = var.cloudflare_zone_id
  name        = "Security Baseline Rules"
  description = "Comprehensive security baseline for all services"
  kind        = "zone"
  phase       = "http_request_firewall_custom"

  rules {
    action = "block"
    expression = "(cf.threat_score gt 14)"
    description = "Block high threat score requests"
  }

  rules {
    action = "challenge"
    expression = "(http.request.uri.path contains \"admin\" and cf.threat_score gt 5)"
    description = "Challenge admin access from suspicious IPs"
  }

  rules {
    action = "managed_challenge"
    expression = "(rate(5m) gt 100)"
    description = "Rate limit high-frequency requests"
  }
}

resource "cloudflare_access_application" "admin_access" {
  zone_id                   = var.cloudflare_zone_id
  name                     = "Admin Panel Access"
  domain                   = "admin.${var.domain_name}"
  type                     = "self_hosted"
  session_duration        = "2h"
  auto_redirect_to_identity = false

  policies = [
    cloudflare_access_policy.admin_policy.id
  ]
}

resource "cloudflare_access_policy" "admin_policy" {
  application_id = cloudflare_access_application.admin_access.id
  zone_id        = var.cloudflare_zone_id
  name           = "Admin Access Policy"
  precedence     = 1
  decision       = "allow"

  include {
    group = [var.admin_group_id]
  }

  require {
    any_valid_service_token = true
  }
}
```

## Security Monitoring and Incident Response

### Security Information and Event Management (SIEM)

**Log Collection Standards:**
```yaml
security_logging:
  authentication_events:
    - "All login attempts (success and failure)"
    - "Password changes and resets"
    - "MFA enrollment and verification"
    - "Account lockouts and unlocks"

  authorization_events:
    - "Permission grants and revocations"
    - "Role assignments and changes"
    - "Access to sensitive resources"
    - "Administrative actions"

  system_events:
    - "System start/stop events"
    - "Configuration changes"
    - "Software installations and updates"
    - "Network connection attempts"

  application_events:
    - "Data access and modification"
    - "Error conditions and exceptions"
    - "Performance anomalies"
    - "Security policy violations"
```

**Security Metrics Dashboard:**
```yaml
# Prometheus security metrics
security_metrics:
  authentication_failures:
    query: "increase(auth_failures_total[5m])"
    threshold: "> 10 failures in 5 minutes"

  privilege_escalations:
    query: "increase(privilege_escalation_attempts_total[1h])"
    threshold: "> 1 escalation per hour"

  suspicious_network_activity:
    query: "increase(network_connections_blocked_total[10m])"
    threshold: "> 50 blocked connections in 10 minutes"

  vulnerability_exposure:
    query: "security_vulnerabilities_total by (severity)"
    threshold: "Any CRITICAL vulnerabilities"

  security_baseline_compliance:
    query: "security_baseline_score"
    threshold: "< 80% compliance score"
```

### Incident Response Procedures

**Security Incident Classification:**
```yaml
incident_categories:
  category_1_critical:
    description: "Active security breach with data compromise"
    response_time: "15 minutes"
    escalation: "Security team, executive leadership"
    actions: ["Immediate containment", "Forensic preservation", "External notification"]

  category_2_high:
    description: "Security event with potential for compromise"
    response_time: "1 hour"
    escalation: "Security team, IT operations"
    actions: ["Investigation", "Monitoring enhancement", "Preventive measures"]

  category_3_medium:
    description: "Security policy violation or suspicious activity"
    response_time: "4 hours"
    escalation: "Security team"
    actions: ["Analysis", "Policy enforcement", "User education"]

  category_4_low:
    description: "Security awareness or minor configuration issue"
    response_time: "24 hours"
    escalation: "Local security contact"
    actions: ["Documentation", "Process improvement", "Training"]
```

**Automated Incident Response:**
```python
# Security incident response automation
class SecurityIncidentResponse:
    def __init__(self):
        self.alert_thresholds = {
            'failed_logins': {'threshold': 10, 'window': '5m'},
            'privilege_escalation': {'threshold': 1, 'window': '1h'},
            'data_exfiltration': {'threshold': 1, 'window': '1m'},
            'malware_detection': {'threshold': 1, 'window': '1m'}
        }

    def handle_security_alert(self, alert_type, severity, details):
        """Automated security incident response"""

        incident_id = self.create_incident(alert_type, severity, details)

        # Immediate automated responses
        if severity == 'CRITICAL':
            self.execute_immediate_containment(alert_type, details)
            self.notify_security_team(incident_id, severity)
            self.preserve_forensic_evidence(details)

        elif severity == 'HIGH':
            self.enhance_monitoring(alert_type, details)
            self.notify_security_team(incident_id, severity)

        # Log all incidents
        self.log_security_incident(incident_id, alert_type, severity, details)

        return incident_id

    def execute_immediate_containment(self, alert_type, details):
        """Execute immediate containment measures"""

        if alert_type == 'malware_detection':
            # Isolate affected systems
            self.isolate_system(details['affected_hosts'])

        elif alert_type == 'privilege_escalation':
            # Disable affected user accounts
            self.disable_user_accounts(details['user_accounts'])

        elif alert_type == 'data_exfiltration':
            # Block suspicious network connections
            self.block_network_connections(details['source_ips'])

    def notify_security_team(self, incident_id, severity):
        """Notify security team of incident"""

        if severity in ['CRITICAL', 'HIGH']:
            # Page on-call security team
            self.send_pager_alert(incident_id, severity)

        # Send to security Slack channel
        self.send_slack_notification(incident_id, severity)

        # Create security ticket
        self.create_security_ticket(incident_id, severity)
```

## Compliance and Audit

### Compliance Framework Integration

**Regulatory Compliance Mapping:**
```yaml
compliance_frameworks:
  gdpr:
    requirements:
      - "Data encryption and pseudonymization"
      - "Consent management and tracking"
      - "Data breach notification procedures"
      - "Right to erasure implementation"

  sox:
    requirements:
      - "Financial data access controls"
      - "Change management documentation"
      - "Audit trail completeness"
      - "Segregation of duties"

  pci_dss:
    requirements:
      - "Cardholder data encryption"
      - "Network security monitoring"
      - "Access control implementation"
      - "Regular security testing"

  hipaa:
    requirements:
      - "PHI encryption and access controls"
      - "Audit logging and monitoring"
      - "Risk assessment documentation"
      - "Breach notification procedures"
```

**Automated Compliance Checking:**
```bash
#!/bin/bash
# scripts/compliance-audit.sh
# Automated compliance validation

set -euo pipefail

FRAMEWORK="${1:-owasp}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

check_owasp_compliance() {
    log "Checking OWASP Top 10 compliance..."

    # A01: Injection
    if grep -r "sql.*\+" . --include="*.js" --include="*.py"; then
        echo "⚠️ Potential SQL injection vulnerability detected"
    fi

    # A02: Broken Authentication
    if ! grep -r "bcrypt\|scrypt\|argon2" . --include="*.js" --include="*.py"; then
        echo "⚠️ Secure password hashing not detected"
    fi

    # A03: Sensitive Data Exposure
    if grep -r "password.*=\|secret.*=" . --include="*.js" --include="*.py" | grep -v ".env"; then
        echo "⚠️ Potential hardcoded secrets detected"
    fi

    # Additional OWASP checks...
}

check_pci_compliance() {
    log "Checking PCI DSS compliance..."

    # Requirement 3: Protect stored cardholder data
    if ! find . -name "*.js" -o -name "*.py" | xargs grep -l "encrypt\|cipher"; then
        echo "⚠️ Encryption implementation not detected"
    fi

    # Requirement 8: Assign a unique ID to each person with computer access
    if ! grep -r "unique.*user.*id" . --include="*.yml" --include="*.json"; then
        echo "⚠️ Unique user ID implementation not verified"
    fi

    # Additional PCI DSS checks...
}

generate_compliance_report() {
    local framework="$1"

    cat > "compliance-report-$framework-$(date +%Y%m%d).md" <<EOF
# Compliance Report: $framework

Generated: $(date)

## Summary
Framework: $framework
Assessment Date: $(date +%Y-%m-%d)
Overall Status: $(if [ $compliance_issues -eq 0 ]; then echo "COMPLIANT"; else echo "NON-COMPLIANT"; fi)

## Issues Found
$compliance_issues issues detected

## Recommendations
$(if [ $compliance_issues -gt 0 ]; then echo "Address identified compliance gaps"; else echo "Maintain current compliance posture"; fi)

## Next Assessment
Scheduled: $(date -d "+90 days" +%Y-%m-%d)
EOF
}

# Main execution
compliance_issues=0

case $FRAMEWORK in
    "owasp")
        check_owasp_compliance
        ;;
    "pci")
        check_pci_compliance
        ;;
    *)
        echo "Unsupported framework: $FRAMEWORK"
        exit 1
        ;;
esac

generate_compliance_report "$FRAMEWORK"

if [ $compliance_issues -eq 0 ]; then
    log "✅ Compliance validation passed for $FRAMEWORK"
    exit 0
else
    log "❌ Compliance validation failed: $compliance_issues issues found"
    exit 1
fi
```

## Compliance Verification

**Automated Checks:**
- Daily vulnerability scanning and dependency auditing
- Weekly security configuration validation
- Monthly compliance framework assessment
- Quarterly penetration testing and security review

**Manual Audits:**
- Monthly security control effectiveness review
- Quarterly incident response procedure testing
- Annual third-party security assessment
- Annual compliance framework certification

**Reporting:**
- Real-time security baseline compliance dashboard
- Weekly vulnerability and risk assessment reports
- Monthly security metrics and trend analysis
- Quarterly compliance posture and improvement recommendations

## Related Documents

- **Source Principles:** [PRINCIPLES.md - Security Principles 6, 9, 10](../the-covenant/PRINCIPLES.md)
- **Governance Authority:** [GOVERNANCE.md - Security Standards](../the-covenant/GOVERNANCE.md#stronghold-decisions-individual-repositories)
- **Implementation:** Security tooling, monitoring systems, compliance frameworks
- **Zero Trust:** [SEC-001 Zero Trust Architecture](./sec-001-zero-trust.md)
- **Secrets Management:** [SEC-002 Secret Scanning](./sec-002-secret-scanning.md)
- **Access Control:** [SEC-003 Least Privilege](./sec-003-least-privilege.md)

## Change History

- **2024-09-30** - Initial creation establishing comprehensive security baseline requirements
