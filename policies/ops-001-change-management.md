# OPS-001: Change Management Process

**Policy ID:** OPS-001
**Category:** Operations
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

All changes to production systems **must** follow a controlled, auditable process that balances velocity with stability. Changes **shall** be categorized by risk and impact, with appropriate approval and validation gates.

## Rationale

Uncontrolled changes are the primary source of production incidents and system instability. A structured change management process prevents incidents while enabling rapid, safe deployment:

- **Incident Prevention**: Most production issues stem from uncontrolled or poorly planned changes
- **Rollback Capability**: Structured changes enable rapid rollback when issues occur
- **Risk Assessment**: Different changes require different levels of validation and approval
- **Audit Compliance**: Regulated environments require documented change processes
- **Learning Integration**: Systematic change process enables continuous improvement
- **Stakeholder Communication**: Changes affect multiple teams and require coordination

Balanced change management enables both innovation velocity and production stability through appropriate risk-based controls.

## Scope

**Applies To:**
- All production infrastructure changes via the-citadel
- All application deployments to production environments
- All database schema changes affecting production data
- All configuration changes that affect user-facing services
- All security-related changes regardless of environment

**Exceptions:**
- Emergency security fixes (expedited process applies)
- Automated dependency updates (pre-approved process)
- Development and testing environment changes (reduced process)

## Implementation

### Technical Enforcement

Change management automation and approval workflows:

```hcl
# terraform/github/change_management.tf
resource "github_repository_ruleset" "change_approval" {
  name        = "Change Management Process"
  repository  = "the-citadel"
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
        { context = "change-management/risk-assessment" },
        { context = "change-management/approval-validation" },
        { context = "change-management/impact-analysis" },
        { context = "terraform/plan-validation" }
      ]
    }

    pull_request {
      required_approving_review_count = 2  # Higher for infrastructure
      dismiss_stale_reviews_on_push  = true
      require_code_owner_review       = true
      require_last_push_approval     = true
    }
  }

  labels = {
    "nash.group/policy"    = "ops-001"
    "nash.group/component" = "change-management"
    "nash.group/criticality" = "high"
  }
}

# Change tracking and metrics
resource "github_repository_file" "change_tracking" {
  repository = "the-citadel"
  file       = ".github/workflows/change-tracking.yml"

  content = templatefile("${path.module}/templates/change-tracking.yml", {
    policy_id = "ops-001"
  })
}
```

Automated change categorization and routing:

```yaml
# .github/workflows/change-management.yml
name: Change Management Process
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, labeled]

jobs:
  assess-change-risk:
    runs-on: ubuntu-latest
    outputs:
      risk-level: ${{ steps.assessment.outputs.risk-level }}
      change-type: ${{ steps.assessment.outputs.change-type }}
      requires-approval: ${{ steps.assessment.outputs.requires-approval }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Analyze Change Impact
        id: assessment
        run: |
          echo "Analyzing change impact and risk level..."

          # Get changed files
          changed_files=$(git diff --name-only origin/main..HEAD)
          echo "Changed files: $changed_files"

          # Initialize risk assessment
          risk_score=0
          change_type="standard"
          requires_approval="true"

          # High-risk patterns
          if echo "$changed_files" | grep -qE "(terraform/.*\.tf|kubernetes/|dns/|security/)"; then
            risk_score=$((risk_score + 3))
            change_type="infrastructure"
          fi

          if echo "$changed_files" | grep -qE "(database/|migration/)"; then
            risk_score=$((risk_score + 2))
            change_type="database"
          fi

          if echo "$changed_files" | grep -qE "(secrets/|auth/|security/)"; then
            risk_score=$((risk_score + 3))
            change_type="security"
          fi

          # Check PR labels for manual override
          pr_labels="${{ toJson(github.event.pull_request.labels.*.name) }}"
          if echo "$pr_labels" | grep -q "emergency"; then
            change_type="emergency"
            requires_approval="false"  # Emergency bypass
          fi

          if echo "$pr_labels" | grep -q "high-risk"; then
            risk_score=$((risk_score + 2))
          fi

          # Determine risk level
          if [ $risk_score -ge 5 ]; then
            risk_level="high"
          elif [ $risk_score -ge 2 ]; then
            risk_level="medium"
          else
            risk_level="low"
          fi

          echo "risk-level=$risk_level" >> $GITHUB_OUTPUT
          echo "change-type=$change_type" >> $GITHUB_OUTPUT
          echo "requires-approval=$requires_approval" >> $GITHUB_OUTPUT

          # Add labels based on assessment
          gh pr edit ${{ github.event.number }} --add-label "risk:$risk_level,type:$change_type"

        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Generate Change Summary
        run: |
          cat > change-summary.md <<EOF
          # Change Management Assessment

          **PR**: #${{ github.event.number }}
          **Risk Level**: ${{ steps.assessment.outputs.risk-level }}
          **Change Type**: ${{ steps.assessment.outputs.change-type }}
          **Approval Required**: ${{ steps.assessment.outputs.requires-approval }}

          ## Risk Assessment
          Based on files changed and impact analysis:
          - Infrastructure changes detected: $(echo "$changed_files" | grep -c terraform || echo 0)
          - Database changes detected: $(echo "$changed_files" | grep -c migration || echo 0)
          - Security changes detected: $(echo "$changed_files" | grep -c security || echo 0)

          ## Next Steps
          1. Review Terraform plan output
          2. Validate against change control process
          3. Obtain required approvals
          4. Execute change with monitoring

          EOF

          gh pr comment ${{ github.event.number }} --body-file change-summary.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  validate-approvals:
    needs: assess-change-risk
    if: needs.assess-change-risk.outputs.requires-approval == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Check Approval Requirements
        run: |
          risk_level="${{ needs.assess-change-risk.outputs.risk-level }}"
          change_type="${{ needs.assess-change-risk.outputs.change-type }}"

          case $risk_level in
            "high")
              required_approvals=2
              required_roles="watcher,mentor"
              ;;
            "medium")
              required_approvals=1
              required_roles="mentor"
              ;;
            "low")
              required_approvals=1
              required_roles="immortal"
              ;;
          esac

          echo "Change requires $required_approvals approvals from: $required_roles"

          # Check current approvals (simplified - would integrate with org structure)
          current_approvals=$(gh pr view ${{ github.event.number }} --json reviews --jq '.reviews | map(select(.state == "APPROVED")) | length')

          if [ "$current_approvals" -lt "$required_approvals" ]; then
            echo "❌ Insufficient approvals: $current_approvals/$required_approvals"
            exit 1
          fi

          echo "✅ Approval requirements met: $current_approvals/$required_approvals"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  terraform-plan:
    if: contains(github.event.pull_request.labels.*.name, 'infrastructure')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: "1.5.0"

      - name: Terraform Plan
        working-directory: terraform
        run: |
          terraform init
          terraform plan -out=tfplan

          # Save plan for review
          terraform show -json tfplan > tfplan.json

          # Generate human-readable summary
          terraform show tfplan > tfplan.txt

      - name: Analyze Terraform Plan
        run: |
          echo "Analyzing Terraform plan for high-risk changes..."

          # Check for destructive operations
          if grep -q "destroy\|delete" terraform/tfplan.txt; then
            echo "⚠️ Destructive operations detected in plan"
            echo "Manual review required before approval"
          fi

          # Check for security-sensitive changes
          if grep -qE "(iam|security|firewall)" terraform/tfplan.txt; then
            echo "🔒 Security-sensitive changes detected"
            echo "Security team review required"
          fi

          # Post plan summary to PR
          gh pr comment ${{ github.event.number }} --body "## Terraform Plan Summary

          \`\`\`
          $(head -20 terraform/tfplan.txt)
          \`\`\`

          Full plan available in workflow artifacts."

        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Upload Plan Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: terraform-plan
          path: |
            terraform/tfplan
            terraform/tfplan.json
            terraform/tfplan.txt
```

### Automated Validation

**Change Risk Categorization:**
```python
#!/usr/bin/env python3
# scripts/assess-change-risk.py
"""
Automated change risk assessment based on files and impact
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List

class ChangeRiskAssessment:
    def __init__(self):
        self.risk_patterns = {
            'infrastructure': {
                'patterns': [r'terraform/.*\.tf$', r'kubernetes/.*\.yaml$', r'helm/'],
                'weight': 3,
                'description': 'Infrastructure configuration changes'
            },
            'database': {
                'patterns': [r'migrations?/', r'schema/', r'db/'],
                'weight': 3,
                'description': 'Database schema or data changes'
            },
            'security': {
                'patterns': [r'security/', r'auth/', r'iam/', r'secrets/'],
                'weight': 4,
                'description': 'Security-related configuration'
            },
            'dns': {
                'patterns': [r'dns/', r'zones/', r'.*\.zone$'],
                'weight': 2,
                'description': 'DNS configuration changes'
            },
            'monitoring': {
                'patterns': [r'monitoring/', r'alerts/', r'dashboards/'],
                'weight': 1,
                'description': 'Monitoring and alerting changes'
            }
        }

        self.approval_matrix = {
            'emergency': {'min_approvals': 0, 'roles': [], 'bypass': True},
            'low': {'min_approvals': 1, 'roles': ['immortal']},
            'medium': {'min_approvals': 1, 'roles': ['mentor']},
            'high': {'min_approvals': 2, 'roles': ['watcher', 'mentor']},
            'critical': {'min_approvals': 3, 'roles': ['watcher', 'watcher', 'mentor']}
        }

    def assess_files(self, changed_files: List[str]) -> Dict:
        """Assess risk level based on changed files"""

        total_risk_score = 0
        matched_categories = []

        for file_path in changed_files:
            for category, config in self.risk_patterns.items():
                for pattern in config['patterns']:
                    if re.search(pattern, file_path):
                        total_risk_score += config['weight']
                        if category not in matched_categories:
                            matched_categories.append(category)
                        break

        # Determine overall risk level
        if total_risk_score >= 8:
            risk_level = 'critical'
        elif total_risk_score >= 5:
            risk_level = 'high'
        elif total_risk_score >= 2:
            risk_level = 'medium'
        else:
            risk_level = 'low'

        return {
            'risk_score': total_risk_score,
            'risk_level': risk_level,
            'categories': matched_categories,
            'approval_requirements': self.approval_matrix[risk_level],
            'files_analyzed': len(changed_files)
        }

    def generate_change_request(self, assessment: Dict, pr_info: Dict) -> Dict:
        """Generate formal change request documentation"""

        return {
            'change_id': f"CHG-{pr_info['number']}-{pr_info['created_at'][:10]}",
            'title': pr_info['title'],
            'description': pr_info['description'],
            'risk_assessment': assessment,
            'approvals_required': assessment['approval_requirements'],
            'implementation_plan': {
                'pre_change_validation': [
                    'Terraform plan reviewed and approved',
                    'Security scan completed',
                    'Backup/rollback plan confirmed'
                ],
                'change_window': 'Standard deployment window',
                'rollback_plan': 'Automated rollback via Terraform',
                'success_criteria': [
                    'All health checks passing',
                    'No alerts triggered',
                    'Functionality verified'
                ]
            },
            'communication': {
                'stakeholders': self._identify_stakeholders(assessment['categories']),
                'notification_channels': ['#engineering', '#ops'],
                'status_updates': 'Real-time via PR comments'
            }
        }

    def _identify_stakeholders(self, categories: List[str]) -> List[str]:
        """Identify stakeholders based on change categories"""

        stakeholder_map = {
            'infrastructure': ['platform-team', 'sre-team'],
            'database': ['data-team', 'backend-team'],
            'security': ['security-team', 'compliance-team'],
            'dns': ['platform-team', 'network-team'],
            'monitoring': ['sre-team', 'platform-team']
        }

        stakeholders = set()
        for category in categories:
            stakeholders.update(stakeholder_map.get(category, []))

        return list(stakeholders)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python assess-change-risk.py <file1> [file2] ...")
        sys.exit(1)

    assessor = ChangeRiskAssessment()
    changed_files = sys.argv[1:]
    assessment = assessor.assess_files(changed_files)

    print(json.dumps(assessment, indent=2))
```

### Human Process

1. **Change Planning**: Document change intent and impact before implementation
2. **Risk Assessment**: Categorize changes by risk level and required approvals
3. **Approval Workflow**: Route changes to appropriate approvers based on risk
4. **Implementation**: Execute changes with monitoring and rollback capability
5. **Post-Change Validation**: Verify change success and document lessons learned

## Change Categories and Processes

### Emergency Changes

**Emergency Criteria:**
- Active security incident requiring immediate response
- Production outage with user impact requiring urgent fix
- Data integrity threat requiring immediate action
- Regulatory compliance issue requiring rapid resolution

**Emergency Process:**
```markdown
# Emergency Change Process

## Immediate Actions (0-15 minutes)
1. **Incident Declaration**: Declare emergency change in #ops-emergency
2. **Change Authorization**: Get verbal approval from on-call Watcher
3. **Documentation**: Create emergency change ticket with basic details
4. **Implementation**: Execute change with enhanced monitoring

## Short-term Follow-up (1-4 hours)
1. **Validation**: Confirm change resolved the emergency
2. **Documentation**: Complete detailed change documentation
3. **Communication**: Notify stakeholders of emergency change
4. **Review**: Schedule emergency change review within 24 hours

## Post-Emergency (24-48 hours)
1. **Post-Mortem**: Conduct change review and incident analysis
2. **Process Improvement**: Identify prevention opportunities
3. **Documentation**: Update procedures based on lessons learned
4. **Compliance**: File regulatory notifications if required
```

### Standard Changes

**Standard Change Categories:**
```yaml
standard_changes:
  application_deployment:
    risk_level: "low"
    approval_required: 1
    approver_roles: ["mentor"]
    automation_level: "high"
    validation: ["automated_tests", "health_checks"]

  infrastructure_config:
    risk_level: "medium"
    approval_required: 2
    approver_roles: ["watcher", "mentor"]
    automation_level: "medium"
    validation: ["terraform_plan", "security_scan"]

  database_schema:
    risk_level: "high"
    approval_required: 2
    approver_roles: ["watcher", "data_owner"]
    automation_level: "low"
    validation: ["migration_test", "rollback_test"]

  security_config:
    risk_level: "high"
    approval_required: 3
    approver_roles: ["security_team", "watcher", "mentor"]
    automation_level: "medium"
    validation: ["security_scan", "compliance_check"]
```

### Pre-approved Changes

**Automated Change Types:**
- Dependency updates (security patches)
- Certificate renewals
- Log rotation and cleanup
- Monitoring configuration updates
- Documentation updates

**Pre-approval Criteria:**
```yaml
pre_approved_changes:
  dependency_updates:
    scope: "security patches only"
    conditions:
      - "no breaking changes detected"
      - "automated tests passing"
      - "rollback plan automated"
    notification: "post-change notification"

  certificate_renewal:
    scope: "TLS certificates with >30 days expiry"
    conditions:
      - "same certificate authority"
      - "same key length and algorithms"
      - "automated validation testing"
    notification: "real-time monitoring alerts"

  configuration_drift:
    scope: "restore to known good configuration"
    conditions:
      - "change matches terraform state"
      - "no manual modifications required"
      - "rollback capability verified"
    notification: "immediate notification to ops team"
```

## Change Implementation Standards

### Change Documentation

**Change Request Template:**
```markdown
# Change Request: [Title]

## Change Information
- **Change ID**: CHG-YYYY-MM-DD-###
- **Type**: [Standard/Emergency/Pre-approved]
- **Risk Level**: [Low/Medium/High/Critical]
- **Requested By**: [Name/Team]
- **Implementation Date**: [Scheduled Date/Time]

## Description
Brief description of what is changing and why.

## Business Justification
- Problem being solved
- Business value delivered
- Impact of not making change

## Technical Details
### Current State
Description of current configuration/state

### Desired State
Description of target configuration/state

### Implementation Steps
1. Step 1: Detailed action
2. Step 2: Detailed action
3. Step 3: Detailed action

## Risk Assessment
### Potential Risks
- Risk 1: Description and mitigation
- Risk 2: Description and mitigation

### Dependencies
- Upstream systems affected
- Downstream systems affected
- Team coordination required

## Testing and Validation
### Pre-Change Testing
- [ ] Test 1: Description
- [ ] Test 2: Description

### Post-Change Validation
- [ ] Validation 1: Success criteria
- [ ] Validation 2: Success criteria

## Rollback Plan
### Rollback Triggers
- Condition 1 that would trigger rollback
- Condition 2 that would trigger rollback

### Rollback Steps
1. Step 1: Detailed rollback action
2. Step 2: Detailed rollback action

### Rollback Testing
- [ ] Rollback procedure tested in staging
- [ ] Rollback time estimate: [X minutes]

## Communication Plan
### Stakeholders
- Team 1: Notification method
- Team 2: Notification method

### Notification Timeline
- T-24h: Advance notification
- T-1h: Implementation starting
- T+1h: Status update
- T+24h: Post-change summary

## Approvals
- [ ] Technical Approval: [Name/Date]
- [ ] Security Approval: [Name/Date] (if required)
- [ ] Business Approval: [Name/Date] (if required)
```

### Implementation Monitoring

**Real-time Change Monitoring:**
```yaml
# Prometheus alerts for change implementation
groups:
  - name: change-management
    rules:
      - alert: ChangeImplementationFailure
        expr: |
          increase(terraform_apply_failures_total[5m]) > 0
        for: 0m
        labels:
          severity: critical
          policy: ops-001
        annotations:
          summary: "Change implementation failure detected"
          description: "Terraform apply failed during change implementation"
          runbook_url: "https://runbooks.nash.group/change-failure"

      - alert: UnexpectedConfigurationDrift
        expr: |
          terraform_drift_detected == 1
        for: 2m
        labels:
          severity: warning
          policy: ops-001
        annotations:
          summary: "Configuration drift detected after change"
          description: "System configuration differs from Terraform state"
          runbook_url: "https://runbooks.nash.group/configuration-drift"

      - alert: ChangeRollbackRequired
        expr: |
          increase(http_requests_total{status_code=~"5.."}[5m]) > 100
        for: 5m
        labels:
          severity: critical
          policy: ops-001
        annotations:
          summary: "High error rate detected - rollback may be required"
          description: "Error rate increased significantly after change"
          runbook_url: "https://runbooks.nash.group/change-rollback"
```

**Change Success Metrics:**
```python
# scripts/measure-change-success.py
class ChangeSuccessMetrics:
    def __init__(self):
        self.metrics = {
            'lead_time': 'Time from change request to implementation',
            'success_rate': 'Percentage of changes implemented without rollback',
            'rollback_time': 'Average time to rollback failed changes',
            'approval_time': 'Time from request to approval',
            'validation_coverage': 'Percentage of changes with complete validation'
        }

    def calculate_change_lead_time(self, change_requests):
        """Calculate average lead time for changes"""
        lead_times = []

        for change in change_requests:
            if change.get('implemented_at') and change.get('requested_at'):
                lead_time = change['implemented_at'] - change['requested_at']
                lead_times.append(lead_time.total_seconds() / 3600)  # hours

        return {
            'average_hours': sum(lead_times) / len(lead_times) if lead_times else 0,
            'median_hours': sorted(lead_times)[len(lead_times)//2] if lead_times else 0,
            'samples': len(lead_times)
        }

    def calculate_success_rate(self, change_requests):
        """Calculate change success rate"""
        total_changes = len(change_requests)
        successful_changes = len([c for c in change_requests if not c.get('rollback_required')])

        return {
            'success_rate': successful_changes / total_changes if total_changes > 0 else 0,
            'total_changes': total_changes,
            'successful_changes': successful_changes,
            'failed_changes': total_changes - successful_changes
        }
```

## Integration with Development Workflow

### CI/CD Integration

**Pipeline Gates:**
```yaml
# .github/workflows/deployment-pipeline.yml
name: Deployment Pipeline
on:
  push:
    branches: [main]

jobs:
  assess-deployment-risk:
    runs-on: ubuntu-latest
    outputs:
      deployment-approved: ${{ steps.approval.outputs.approved }}
    steps:
      - name: Check Change Approval
        id: approval
        run: |
          # Check if this deployment was approved through change management
          commit_msg=$(git log -1 --pretty=%B)

          if echo "$commit_msg" | grep -q "CHANGE-APPROVED:"; then
            change_id=$(echo "$commit_msg" | grep -o "CHANGE-APPROVED: CHG-[0-9-]*")
            echo "approved=true" >> $GITHUB_OUTPUT
            echo "Change approved: $change_id"
          else
            echo "approved=false" >> $GITHUB_OUTPUT
            echo "Deployment requires change management approval"
          fi

  deploy:
    needs: assess-deployment-risk
    if: needs.assess-deployment-risk.outputs.deployment-approved == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy with Monitoring
        run: |
          echo "Deploying with enhanced monitoring..."

          # Deploy application
          ./scripts/deploy.sh

          # Monitor for issues
          ./scripts/monitor-deployment.sh --timeout=300

      - name: Validate Deployment
        run: |
          echo "Validating deployment success..."

          # Health checks
          ./scripts/health-check.sh

          # Smoke tests
          ./scripts/smoke-tests.sh

          # Performance validation
          ./scripts/performance-check.sh

      - name: Update Change Status
        run: |
          echo "Updating change management status..."

          # Extract change ID from commit
          change_id=$(git log -1 --pretty=%B | grep -o "CHG-[0-9-]*")

          # Update change status to completed
          gh issue comment "$change_id" --body "✅ Change implemented successfully at $(date)"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Rollback Automation

**Automated Rollback Triggers:**
```bash
#!/bin/bash
# scripts/automated-rollback.sh
# Monitors deployment and triggers rollback if needed

set -euo pipefail

DEPLOYMENT_ID="${1:-}"
ROLLBACK_THRESHOLD="${2:-5}"  # Error rate percentage
MONITOR_DURATION="${3:-300}"  # 5 minutes

if [ -z "$DEPLOYMENT_ID" ]; then
    echo "Usage: $0 <deployment-id> [error-threshold] [monitor-duration]"
    exit 1
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

check_error_rate() {
    # Query Prometheus for current error rate
    error_rate=$(curl -s "http://prometheus:9090/api/v1/query" \
        --data-urlencode "query=rate(http_requests_total{status_code=~\"5..\"}[2m]) / rate(http_requests_total[2m]) * 100" \
        | jq -r '.data.result[0].value[1] // "0"')

    echo "$error_rate"
}

monitor_deployment() {
    local start_time=$(date +%s)
    local end_time=$((start_time + MONITOR_DURATION))

    log "Starting deployment monitoring for $DEPLOYMENT_ID"
    log "Monitoring duration: ${MONITOR_DURATION}s, Error threshold: ${ROLLBACK_THRESHOLD}%"

    while [ $(date +%s) -lt $end_time ]; do
        current_error_rate=$(check_error_rate)

        log "Current error rate: ${current_error_rate}%"

        if (( $(echo "$current_error_rate > $ROLLBACK_THRESHOLD" | bc -l) )); then
            log "ERROR: Error rate ${current_error_rate}% exceeds threshold ${ROLLBACK_THRESHOLD}%"
            return 1
        fi

        sleep 30
    done

    log "Monitoring completed successfully"
    return 0
}

execute_rollback() {
    log "INITIATING ROLLBACK for deployment $DEPLOYMENT_ID"

    # Get previous successful deployment
    previous_deployment=$(git log --oneline -n 2 --grep="CHANGE-APPROVED" | tail -1 | cut -d' ' -f1)

    if [ -z "$previous_deployment" ]; then
        log "ERROR: Cannot find previous deployment for rollback"
        exit 1
    fi

    log "Rolling back to: $previous_deployment"

    # Execute rollback
    git checkout "$previous_deployment"
    ./scripts/deploy.sh --rollback

    # Verify rollback success
    if ./scripts/health-check.sh; then
        log "✅ Rollback completed successfully"

        # Notify team
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H 'Content-type: application/json' \
            --data "{\"text\":\"🔄 Automated rollback completed for deployment $DEPLOYMENT_ID due to high error rate\"}"
    else
        log "❌ Rollback failed - manual intervention required"
        exit 1
    fi
}

# Main execution
if monitor_deployment; then
    log "✅ Deployment $DEPLOYMENT_ID completed successfully"
else
    execute_rollback
fi
```

## Compliance Verification

**Automated Checks:**
- All production changes require documented change requests
- Change approvals verified before implementation
- Post-change validation confirms success criteria
- Rollback procedures tested regularly

**Manual Audits:**
- Weekly review of change success rates and lead times
- Monthly assessment of change approval compliance
- Quarterly review of emergency change procedures
- Annual evaluation of change management effectiveness

**Reporting:**
- Real-time change management dashboard
- Weekly change velocity and success metrics
- Monthly risk assessment and approval compliance
- Quarterly change management maturity assessment

## Related Documents

- **Governance Authority:** [GOVERNANCE.md - Change Control Process](../the-covenant/GOVERNANCE.md#citadel-decisions-infrastructure)
- **Implementation:** Change tracking automation, approval workflows, rollback procedures
- **Risk Management:** [OPS-003 Fail Fast](./ops-003-fail-fast.md)
- **Infrastructure:** [INF-001 Infrastructure as Code](./inf-001-infrastructure-as-code.md)

## Change History

- **2024-09-30** - Initial creation establishing comprehensive change management process
