# OPS-005: Runbook Standards

**Policy ID:** OPS-005
**Category:** Operations
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Every alert **must** have a runbook. Every runbook **must** be automated or have clear, tested manual steps. A 3 AM page is not the time to figure out what to do.

## Rationale

A 3 AM page is not the time to figure out what to do. We've lost hours to incomplete runbooks and outdated procedures. The response must be mechanical, not creative:

- **Incident Confusion**: Unclear procedures during critical outages waste precious time
- **Stress-Induced Errors**: Sleep-deprived engineers make mistakes with incomplete guidance
- **Knowledge Gaps**: Critical procedures trapped in individual team members' heads
- **Inconsistent Response**: Different engineers taking different approaches to the same problem
- **Training Delays**: New team members can't respond effectively without documented procedures
- **Post-Incident Analysis**: Poor documentation hinders learning from incidents

Clear, tested runbooks enable rapid incident response, consistent procedures, and effective knowledge transfer across the organization.

## Scope

**Applies To:**
- All monitoring alerts and notifications across The Nash Group systems
- All operational procedures for critical services and infrastructure
- All incident response procedures and escalation paths
- All maintenance and deployment procedures
- All emergency break-glass procedures

**Exceptions:**
- Informational alerts that require no action (logging only)
- Alerts for deprecated systems during sunset periods

## Implementation

### Technical Enforcement

Alert definitions must include runbook URLs:

```hcl
# terraform/monitoring/alerts.tf
resource "monitoring_alert" "high_error_rate" {
  name        = "High Error Rate"
  description = "Error rate exceeds 1% for service ${var.service_name}"

  labels = {
    "nash.group/policy"       = "ops-005"
    "nash.group/service"      = var.service_name
    "nash.group/severity"     = "warning"
    "nash.group/team"         = var.team_name
  }

  annotations = {
    summary     = "High error rate detected for ${var.service_name}"
    description = "Error rate is {{ $value | humanizePercentage }} for service {{ $labels.service }}"
    runbook_url = "https://runbooks.nash.group/alerts/high-error-rate"
  }

  query = <<-EOT
    (
      rate(http_requests_total{status_code=~"5.."}[5m]) /
      rate(http_requests_total[5m])
    ) > 0.01
  EOT

  for_duration = "2m"
}

# Validate runbook URL accessibility
resource "monitoring_alert" "latency_p99_high" {
  name        = "High P99 Latency"
  description = "P99 latency exceeds 500ms for service ${var.service_name}"

  labels = {
    "nash.group/policy"       = "ops-005"
    "nash.group/service"      = var.service_name
    "nash.group/severity"     = "critical"
    "nash.group/team"         = var.team_name
  }

  annotations = {
    summary     = "High latency detected for ${var.service_name}"
    description = "P99 latency is {{ $value }}s for service {{ $labels.service }}"
    runbook_url = "https://runbooks.nash.group/alerts/high-latency"
  }

  query = <<-EOT
    histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.5
  EOT

  for_duration = "5m"
}
```

Runbook repository structure and automation:

```yaml
# .github/workflows/runbook-validation.yml
name: Runbook Validation
on:
  push:
    paths: ['runbooks/**']
  pull_request:
    paths: ['runbooks/**']

jobs:
  validate-runbooks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Runbook Structure
        run: |
          # Check required sections in each runbook
          for runbook in runbooks/**/*.md; do
            echo "Validating $runbook"

            # Required sections
            grep -q "# Overview" "$runbook" || { echo "Missing Overview section in $runbook"; exit 1; }
            grep -q "# Symptoms" "$runbook" || { echo "Missing Symptoms section in $runbook"; exit 1; }
            grep -q "# Investigation" "$runbook" || { echo "Missing Investigation section in $runbook"; exit 1; }
            grep -q "# Resolution" "$runbook" || { echo "Missing Resolution section in $runbook"; exit 1; }
            grep -q "# Prevention" "$runbook" || { echo "Missing Prevention section in $runbook"; exit 1; }

            # Check for automation scripts
            if grep -q "## Automated Resolution" "$runbook"; then
              script_path=$(grep -A 1 "## Automated Resolution" "$runbook" | grep -o '\./scripts/[^"]*\.sh' || true)
              if [ -n "$script_path" ] && [ ! -f "$script_path" ]; then
                echo "Automated script $script_path referenced but not found for $runbook"
                exit 1
              fi
            fi
          done

      - name: Test Automated Scripts
        run: |
          # Test all automation scripts with dry-run
          for script in scripts/**/*.sh; do
            if [ -f "$script" ]; then
              echo "Testing $script"
              chmod +x "$script"
              "$script" --dry-run || { echo "Script $script failed dry-run test"; exit 1; }
            fi
          done

      - name: Validate Alert Runbook Links
        run: |
          # Extract runbook URLs from alert definitions
          grep -r "runbook_url" terraform/ | grep -o 'https://runbooks.nash.group/[^"]*' | sort -u > alert_runbooks.txt

          # Check each runbook URL has corresponding file
          while read -r url; do
            path=$(echo "$url" | sed 's|https://runbooks.nash.group/||')
            if [ ! -f "runbooks/${path}.md" ]; then
              echo "Alert references runbook at $url but runbooks/${path}.md not found"
              exit 1
            fi
          done < alert_runbooks.txt
```

### Automated Validation

**Runbook Standards:**
- Every runbook must include standard sections: Overview, Symptoms, Investigation, Resolution, Prevention
- Runbooks must be tested and updated quarterly
- All manual steps must be validated within 30 days of creation
- Automation scripts must include dry-run modes for testing

**Alert Integration:**
- All alerts must include `runbook_url` annotation
- Runbook URLs must be accessible and return HTTP 200
- Alert descriptions must clearly state the problem and urgency
- Escalation paths must be documented for alerts requiring human intervention

**Documentation Format:**
```markdown
# Alert Name: High Error Rate

## Overview
Brief description of what this alert means and why it matters.

## Symptoms
- What users experience when this alert fires
- Observable system behavior indicating the problem

## Investigation
### Immediate Checks
1. Check service health dashboard
2. Review recent deployments
3. Examine error logs for patterns

### Diagnostic Commands
```bash
# Check current error rate
prometheus_query 'rate(http_requests_total{status_code=~"5.."}[5m])'

# Check recent deployment events
kubectl get events --sort-by='.lastTimestamp' | head -20
```

### Automated Resolution
Available automation: `./scripts/restart-unhealthy-pods.sh`

## Resolution
### Automated Response
If automation is available and safe to run:
```bash
./scripts/restart-unhealthy-pods.sh --service=api --confirm
```

### Manual Steps
1. Identify failing service instances
2. Check resource utilization and limits
3. Review application logs for exceptions
4. Restart problematic instances
5. Monitor error rate recovery

## Prevention
- Regular load testing to identify capacity limits
- Proper resource limits and health checks
- Gradual deployment strategies with automatic rollback

## Escalation
- **Level 1**: Service Team (immediate response expected)
- **Level 2**: Platform Team (if service team unavailable)
- **Level 3**: On-call Engineer (for infrastructure issues)

## Related Documentation
- [Service Architecture](../docs/service-architecture.md)
- [Deployment Procedures](../docs/deployment.md)
- [Incident Response Guide](../docs/incident-response.md)
```

### Human Process

1. **Runbook Creation**: Every new alert requires corresponding runbook before deployment
2. **Quarterly Testing**: All runbooks must be tested with recent team members every quarter
3. **Incident Updates**: Runbooks must be updated within 48 hours after any incident where they were used
4. **Automation Development**: Manual procedures used more than 3 times per month must be automated
5. **Cross-Training**: Each critical runbook must be executable by at least 3 team members

## Runbook Categories and Standards

### Alert Response Runbooks

**Critical Service Alerts:**
- Must include automated remediation where safe
- Maximum response time: 15 minutes to initial action
- Escalation path clearly defined
- Recovery validation steps included

**Infrastructure Alerts:**
- Focus on immediate stability restoration
- Include capacity planning considerations
- Link to relevant infrastructure documentation
- Specify when to engage external vendors

**Security Alerts:**
- Immediate containment procedures
- Evidence preservation requirements
- Communication protocols
- Regulatory compliance considerations

### Operational Procedure Runbooks

**Deployment Procedures:**
```markdown
# Service Deployment Runbook

## Pre-Deployment Checklist
- [ ] All tests passing in CI/CD pipeline
- [ ] Security scan completed successfully
- [ ] Infrastructure capacity verified
- [ ] Rollback plan prepared
- [ ] Monitoring dashboards ready

## Deployment Steps
1. **Staging Deployment**
   ```bash
   kubectl apply -f manifests/ --context=staging
   ```

2. **Smoke Tests**
   ```bash
   ./scripts/smoke-test.sh --environment=staging
   ```

3. **Production Deployment**
   ```bash
   kubectl apply -f manifests/ --context=production --timeout=300s
   ```

## Post-Deployment Validation
- [ ] Health checks passing
- [ ] Key metrics within normal ranges
- [ ] Error rates below baseline
- [ ] User-facing functionality verified

## Rollback Procedure
If any validation fails:
```bash
kubectl rollout undo deployment/service-name --context=production
```
```

**Maintenance Procedures:**
- Scheduled maintenance windows
- System backup and restoration
- Database migration procedures
- Certificate renewal processes

### Emergency Response Runbooks

**Break-Glass Procedures:**
```markdown
# Emergency Database Access

## When to Use
- Database is unresponsive
- All automated recovery has failed
- Data integrity at risk

## Authorization Required
- Two Watchers must approve
- Incident commander must be notified
- Security team must be informed

## Access Steps
1. **Emergency Authentication**
   ```bash
   aws sts assume-role --role-arn arn:aws:iam::account:role/emergency-db-access
   ```

2. **Direct Database Connection**
   ```bash
   mysql -h prod-db-cluster.amazonaws.com -u emergency_user
   ```

3. **Immediate Actions**
   - Assess database state
   - Identify blocking queries
   - Review replication status
   - Document all actions taken

## Post-Emergency Actions
- [ ] Document all changes made
- [ ] File incident report
- [ ] Schedule post-mortem
- [ ] Revoke emergency access
- [ ] Update automation based on findings
```

## Automation Standards

### Script Requirements

**Automation Script Template:**
```bash
#!/bin/bash
# Runbook automation: High Error Rate Response
# Policy: OPS-005
# Last Updated: 2024-09-30

set -euo pipefail

# Configuration
SERVICE_NAME="${1:-}"
DRY_RUN="${2:-false}"
CONFIRM="${3:-false}"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

# Validation
if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: $0 <service-name> [--dry-run] [--confirm]"
    exit 1
fi

# Dry-run mode
if [ "$DRY_RUN" = "true" ] || [ "$2" = "--dry-run" ]; then
    log "DRY RUN MODE: No changes will be made"
    KUBECTL_ARGS="--dry-run=client"
else
    KUBECTL_ARGS=""
fi

# Confirmation required for production actions
if [ "$DRY_RUN" != "true" ] && [ "$CONFIRM" != "true" ] && [ "$3" != "--confirm" ]; then
    echo "Production changes require --confirm flag"
    exit 1
fi

# Main automation logic
main() {
    log "Starting automated response for service: $SERVICE_NAME"

    # Check current service status
    log "Checking service health..."
    kubectl get pods -l app="$SERVICE_NAME" $KUBECTL_ARGS

    # Restart unhealthy pods
    log "Restarting unhealthy pods..."
    kubectl delete pods -l app="$SERVICE_NAME" --field-selector=status.phase!=Running $KUBECTL_ARGS

    # Wait for recovery
    if [ "$DRY_RUN" != "true" ]; then
        log "Waiting for pods to restart..."
        kubectl wait --for=condition=Ready pods -l app="$SERVICE_NAME" --timeout=300s
    fi

    log "Automated response completed"
}

# Execute main function
main "$@"
```

**Testing Requirements:**
- All scripts must support `--dry-run` mode
- Scripts must be idempotent (safe to run multiple times)
- Scripts must include comprehensive logging
- Scripts must validate prerequisites before execution
- Scripts must include rollback procedures where applicable

## Compliance Verification

**Automated Checks:**
- Weekly validation of all runbook URLs referenced in alerts
- Monthly testing of automation scripts in staging environments
- Quarterly validation that all alerts have corresponding runbooks
- Annual audit of runbook completeness and accuracy

**Manual Audits:**
- Quarterly runbook walk-throughs with team members
- Post-incident review of runbook effectiveness
- Annual review of automation coverage and manual procedure optimization

**Reporting:**
- Monthly runbook compliance dashboard
- Quarterly automation effectiveness metrics
- Annual incident response time analysis and improvement recommendations

## Quality Standards

### Runbook Effectiveness Metrics

**Response Time Metrics:**
- Time from alert to first action (target: <15 minutes)
- Time from investigation start to problem identification (target: <30 minutes)
- Time from problem identification to resolution (target: <60 minutes)

**Accuracy Metrics:**
- Percentage of incidents resolved using documented procedures
- Rate of runbook updates following incidents
- Automation success rate (target: >95%)

**Coverage Metrics:**
- Percentage of alerts with corresponding runbooks (target: 100%)
- Percentage of manual procedures that have been automated (target: >80%)
- Number of team members trained on critical runbooks (target: >3 per runbook)

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 12: Runbooks Are Executable Documentation](../the-covenant/PRINCIPLES.md#principle-12-runbooks-are-executable-documentation)
- **Governance Authority:** [GOVERNANCE.md - Operations Standards](../the-covenant/GOVERNANCE.md#stronghold-decisions-individual-repositories)
- **Implementation:** Runbook repository, monitoring infrastructure, automation scripts
- **Observability:** [OPS-004 Observability Requirements](./ops-004-observability.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 12: Runbooks Are Executable Documentation
