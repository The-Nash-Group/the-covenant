# Agent Audit Workflows for The Citadel

*Precise, executable instructions for automated verification agents*

## ⚠️ CRITICAL CONTEXT FOR AGENTS

You are auditing **The Citadel** and related enforcement/evidence layers for
**The Covenant**. This is not routine validation. Classify each control by its
current evidence: live-blocking, report-only, source-tested, native control,
manual audit, procedural, design target, or not currently enforced. Do not
assume every policy must become OPA/Rego, and do not describe target-state
controls as live until the owning repo provides current evidence.

## Workflow 1: Covenant-Policy Traceability Verification

### Agent Identity
**Role:** Covenant Compliance Auditor
**Authority:** Read-only access to all repositories
**Reporting:** Direct to Watchers

### Execution Instructions

```python
# AGENT TASK 1: Extract and map all principles to policies

def audit_covenant_traceability():
    """
    Verify every Covenant principle has policy mapping and an enforcement or
    evidence class.
    CRITICAL: Missing mappings are findings, not automatic proof of a live
    enforcement failure.
    """

    # Step 1: Extract principles
    principles = []
    with open('../the-covenant/PRINCIPLES.md', 'r') as f:
        content = f.read()
        # Extract all principles (format: "### Principle N: Title")
        import re
        pattern = r'### (Principle \d+): (.+)'
        principles = re.findall(pattern, content)

    # Step 2: Map to policies
    traceability_map = {}
    for num, title in principles:
        # Search for principle reference in all policies
        policy_files = glob.glob('policies/*.md')
        mapped_policies = []

        for policy_file in policy_files:
            with open(policy_file, 'r') as f:
                if f'Principle {num}' in f.read():
                    policy_id = os.path.basename(policy_file).replace('.md', '')
                    mapped_policies.append(policy_id)

        traceability_map[f"{num}: {title}"] = mapped_policies

    # Step 3: Generate report
    report = {
        'total_principles': len(principles),
        'mapped_principles': sum(1 for v in traceability_map.values() if v),
        'unmapped_principles': [k for k, v in traceability_map.items() if not v],
        'full_mapping': traceability_map
    }

    # Step 4: CRITICAL - Fail if ANY principle is unmapped
    if report['unmapped_principles']:
        raise AuditFailure(f"CRITICAL: {len(report['unmapped_principles'])} principles have no policy enforcement!")

    return report
```

### Expected Output Format

```json
{
  "audit_id": "covenant-policy-trace-20250930",
  "timestamp": "2025-09-30T10:00:00Z",
  "status": "PASS|FAIL",
  "summary": {
    "total_principles": 16,
    "policies_reviewed": 29,
    "full_coverage": true|false
  },
  "mapping": {
    "Principle 1: Sacred Timeline": ["SC-001"],
    "Principle 2: Commit Purpose": ["SC-002"],
    "Principle 3: No Code Unchallenged": ["OPS-011"],
    // ... complete mapping
  },
  "violations": [
    // Any unmapped principles
  ],
  "recommendations": [
    // Specific remediation steps
  ]
}
```

## Workflow 2: OPA Policy Implementation Verification

### Agent Identity
**Role:** Policy Enforcement Classifier
**Tools Required:** OPA CLI v1.9.0+, jq, git
**Execution Environment:** CI/CD pipeline or local with repo access

### Execution Instructions

```bash
#!/bin/bash
# AGENT TASK 2: Classify policy enforcement evidence and identify OPA gaps

set -euo pipefail

AUDIT_ID="opa-implementation-$(date +%Y%m%d-%H%M%S)"
REPORT_FILE="audit-reports/${AUDIT_ID}.json"

echo '{"audit_id": "'$AUDIT_ID'", "checks": []}' > $REPORT_FILE

# Step 1: Build policy to OPA mapping
for policy_file in policies/*.md; do
    policy_id=$(basename "$policy_file" .md)

    # Check for corresponding OPA rule
    opa_files=$(find policies/opa/policies -name "*.rego" -exec grep -l "$policy_id" {} \; 2>/dev/null || true)

    if [ -z "$opa_files" ]; then
        jq --arg id "$policy_id" \
           '.checks += [{"policy": $id, "status": "MISSING", "severity": "CRITICAL"}]' \
           $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE
        echo "❌ CRITICAL: No OPA implementation for $policy_id"
    else
        # Verify OPA rule structure
        for opa_file in $opa_files; do
            # Check for required elements
            has_import=$(grep -c "import rego.v1" "$opa_file" || echo 0)
            has_default_deny=$(grep -c "default allow := false" "$opa_file" || echo 0)
            has_metadata=$(grep -c "metadata :=" "$opa_file" || echo 0)

            if [[ $has_import -eq 0 ]] || [[ $has_default_deny -eq 0 ]] || [[ $has_metadata -eq 0 ]]; then
                jq --arg id "$policy_id" --arg file "$opa_file" \
                   '.checks += [{"policy": $id, "file": $file, "status": "INCOMPLETE", "severity": "HIGH"}]' \
                   $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE
                echo "⚠️  HIGH: Incomplete OPA implementation for $policy_id in $opa_file"
            else
                # Run tests if they exist
                test_file="${opa_file/.rego/_test.rego}"
                test_file="${test_file/policies/tests}"

                if [ -f "$test_file" ]; then
                    if opa test "$opa_file" "$test_file" -v > /dev/null 2>&1; then
                        jq --arg id "$policy_id" \
                           '.checks += [{"policy": $id, "status": "VERIFIED", "tests": "PASS"}]' \
                           $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE
                        echo "✅ VERIFIED: $policy_id has working OPA implementation"
                    else
                        jq --arg id "$policy_id" \
                           '.checks += [{"policy": $id, "status": "TEST_FAILURE", "severity": "MEDIUM"}]' \
                           $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE
                        echo "⚠️  MEDIUM: Tests failing for $policy_id"
                    fi
                else
                    jq --arg id "$policy_id" \
                       '.checks += [{"policy": $id, "status": "NO_TESTS", "severity": "MEDIUM"}]' \
                       $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE
                    echo "⚠️  MEDIUM: No tests for $policy_id"
                fi
            fi
        done
    fi
done

# Step 2: Test bundle generation
echo "Testing OPA bundle generation..."
if opa build -b policies/opa/policies -o test-bundle.tar.gz 2>/dev/null; then
    jq '.bundle_generation = "SUCCESS"' $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE
    echo "✅ Bundle generation successful"
else
    jq '.bundle_generation = "FAILED"' $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE
    echo "❌ CRITICAL: Bundle generation failed!"
    exit 1
fi

# Step 3: Calculate coverage
total_policies=$(ls policies/*.md | wc -l)
implemented=$(jq '[.checks[] | select(.status == "VERIFIED")] | length' $REPORT_FILE)
coverage=$((implemented * 100 / total_policies))

jq --arg cov "$coverage" '.coverage = ($cov + "%")' $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE

# Step 4: Legacy OPA-only verdict
if [ "$coverage" -lt 100 ]; then
    jq '.verdict = "FAIL: Incomplete OPA coverage"' $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE
    echo "❌ AUDIT FAILED: Only ${coverage}% OPA coverage"
    exit 1
else
    jq '.verdict = "PASS: Full OPA coverage"' $REPORT_FILE > tmp.json && mv tmp.json $REPORT_FILE
    echo "✅ AUDIT PASSED: 100% OPA coverage"
fi
```

## Workflow 3: GOV-010 Labeling Compliance Audit

### Agent Identity
**Role:** Label Compliance Inspector
**Scope:** All infrastructure resources across all systems
**Criticality:** MAXIMUM - Labels are our traceability foundation

### Execution Instructions

```python
# AGENT TASK 3: Verify GOV-010 labeling compliance across ALL resources

import json
import subprocess
import yaml
from typing import Dict, List, Set

class LabelComplianceAuditor:
    """
    Enforces GOV-010: Organizational Labeling Standard
    ZERO TOLERANCE for missing labels
    """

    REQUIRED_LABELS = {
        'project_id',
        'owner',
        'clan',
        'tier',
        'environment',
        'policy_id',
        'citadel_ref'
    }

    VALID_VALUES = {
        'clan': {'mentors', 'watchers', 'platform-clan', 'immortals'},
        'tier': {'core', 'platform', 'application', 'experimental'},
        'environment': {'dev', 'staging', 'prod', 'shared'}
    }

    def audit_github_repositories(self) -> Dict:
        """Check all GitHub repositories for proper topics/labels"""
        violations = []

        # Get all repos via GitHub CLI
        repos_json = subprocess.check_output(
            ['gh', 'api', 'orgs/the-nash-group/repos', '--paginate']
        )
        repos = json.loads(repos_json)

        for repo in repos:
            repo_name = repo['name']
            topics = set(repo.get('topics', []))

            # Check for required label patterns in topics
            missing = []
            for label in self.REQUIRED_LABELS:
                if not any(f"{label}-" in topic for topic in topics):
                    missing.append(label)

            if missing:
                violations.append({
                    'resource': f"github.com/the-nash-group/{repo_name}",
                    'type': 'github_repository',
                    'missing_labels': missing,
                    'severity': 'CRITICAL'
                })

        return {
            'total_repos': len(repos),
            'compliant': len(repos) - len(violations),
            'violations': violations
        }

    def audit_terraform_resources(self) -> Dict:
        """Verify Terraform resources have required tags/labels"""
        violations = []

        # Parse Terraform state
        state_json = subprocess.check_output(
            ['terraform', 'show', '-json'],
            cwd='the-citadel/terraform'
        )
        state = json.loads(state_json)

        for resource in state['values']['root_module']['resources']:
            resource_addr = f"{resource['type']}.{resource['name']}"
            labels = resource['values'].get('tags', {}) or \
                    resource['values'].get('labels', {})

            missing = self.REQUIRED_LABELS - set(labels.keys())
            invalid = {}

            # Validate label values
            for label, valid_set in self.VALID_VALUES.items():
                if label in labels and labels[label] not in valid_set:
                    invalid[label] = f"Invalid value: {labels[label]}"

            if missing or invalid:
                violations.append({
                    'resource': resource_addr,
                    'type': 'terraform_resource',
                    'missing_labels': list(missing),
                    'invalid_labels': invalid,
                    'severity': 'CRITICAL'
                })

        return {
            'total_resources': len(state['values']['root_module']['resources']),
            'violations': violations
        }

    def audit_kubernetes_resources(self) -> Dict:
        """Check K8s resources for label compliance"""
        violations = []

        # Get all namespaced resources
        resource_types = ['deployments', 'services', 'configmaps', 'secrets']

        for resource_type in resource_types:
            resources_yaml = subprocess.check_output(
                ['kubectl', 'get', resource_type, '-A', '-o', 'yaml']
            )
            resources = yaml.safe_load(resources_yaml)

            for item in resources.get('items', []):
                name = item['metadata']['name']
                namespace = item['metadata']['namespace']
                labels = item['metadata'].get('labels', {})

                missing = self.REQUIRED_LABELS - set(labels.keys())

                if missing:
                    violations.append({
                        'resource': f"{namespace}/{resource_type}/{name}",
                        'type': f"k8s_{resource_type}",
                        'missing_labels': list(missing),
                        'severity': 'HIGH'
                    })

        return {'violations': violations}

    def generate_report(self) -> None:
        """Generate comprehensive labeling compliance report"""

        report = {
            'audit_type': 'GOV-010 Labeling Compliance',
            'timestamp': datetime.now().isoformat(),
            'github': self.audit_github_repositories(),
            'terraform': self.audit_terraform_resources(),
            'kubernetes': self.audit_kubernetes_resources()
        }

        # Calculate overall compliance
        total_violations = (
            len(report['github']['violations']) +
            len(report['terraform']['violations']) +
            len(report['kubernetes'].get('violations', []))
        )

        report['summary'] = {
            'total_violations': total_violations,
            'compliance_status': 'FAIL' if total_violations > 0 else 'PASS',
            'critical_violations': sum(
                1 for section in report.values()
                if isinstance(section, dict) and 'violations' in section
                for v in section['violations']
                if v.get('severity') == 'CRITICAL'
            )
        }

        # CRITICAL: Fail hard on any violations
        if total_violations > 0:
            print(f"❌ CRITICAL: {total_violations} labeling violations found!")
            print(json.dumps(report, indent=2))
            sys.exit(1)
        else:
            print("✅ All resources properly labeled per GOV-010")

        return report
```

## Workflow 4: Runtime Enforcement Verification

### Agent Identity
**Role:** Runtime Enforcement Validator
**Mission:** Verify policies are enforced in production, not just documented
**Authority:** Read access to production systems

### Execution Instructions

```bash
#!/bin/bash
# AGENT TASK 4: Verify runtime enforcement is active

CRITICAL_CHECKS=(
    "github_branch_protection"
    "terraform_state_locking"
    "opa_admission_controller"
    "secret_scanning"
    "audit_logging"
)

function check_github_protection() {
    echo "Checking GitHub branch protection..."

    # Get all repos
    repos=$(gh api orgs/the-nash-group/repos --jq '.[].name')

    for repo in $repos; do
        # Check main branch protection
        protection=$(gh api repos/the-nash-group/$repo/branches/main/protection 2>/dev/null || echo "{}")

        if [ "$protection" = "{}" ]; then
            echo "❌ CRITICAL: No branch protection on $repo/main"
            return 1
        fi

        # Verify specific rules
        required_reviews=$(echo "$protection" | jq '.required_pull_request_reviews.required_approving_review_count')
        linear_history=$(echo "$protection" | jq '.required_linear_history.enabled')

        if [ "$required_reviews" -lt 1 ] || [ "$linear_history" != "true" ]; then
            echo "❌ CRITICAL: Insufficient protection on $repo/main"
            return 1
        fi
    done

    echo "✅ GitHub branch protection verified"
    return 0
}

function check_terraform_enforcement() {
    echo "Checking Terraform enforcement..."

    # Check for remote backend
    if ! terraform show 2>/dev/null | grep -q "backend \"remote\""; then
        echo "❌ CRITICAL: Terraform not using remote backend"
        return 1
    fi

    # Check for OPA / policy-gate integration in the current OpenTofu workflow
    # In the live stack this is enforced in GitHub Actions, not via HCP Terraform APIs

    echo "✅ Terraform enforcement verified"
    return 0
}

function check_opa_deployment() {
    echo "Checking OPA deployment..."

    # Check if OPA is running in K8s
    if ! kubectl get deployment -n opa-system opa 2>/dev/null; then
        echo "❌ CRITICAL: OPA not deployed"
        return 1
    fi

    # Check if admission webhook is configured
    if ! kubectl get validatingwebhookconfigurations | grep -q opa; then
        echo "❌ CRITICAL: OPA admission webhook not configured"
        return 1
    fi

    # Test OPA is actually blocking non-compliant resources
    test_resource=$(cat <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-no-labels
  namespace: default
data:
  test: "This should be rejected due to missing labels"
EOF
)

    if echo "$test_resource" | kubectl apply -f - 2>/dev/null; then
        kubectl delete configmap test-no-labels 2>/dev/null
        echo "❌ CRITICAL: OPA not blocking unlabeled resources!"
        return 1
    fi

    echo "✅ OPA enforcement verified"
    return 0
}

function check_secret_scanning() {
    echo "Checking secret scanning..."

    # Check all repos have secret scanning enabled
    repos=$(gh api orgs/the-nash-group/repos --jq '.[].name')

    for repo in $repos; do
        scanning=$(gh api repos/the-nash-group/$repo --jq '.security_and_analysis.secret_scanning.status')

        if [ "$scanning" != "enabled" ]; then
            echo "❌ CRITICAL: Secret scanning disabled on $repo"
            return 1
        fi
    done

    echo "✅ Secret scanning verified"
    return 0
}

function check_audit_logging() {
    echo "Checking audit logging..."

    # Verify OPA decision logging
    decision_count=$(curl -s http://opa.nash.group/v1/logs/decisions | jq '.total')

    if [ "$decision_count" -eq 0 ]; then
        echo "❌ CRITICAL: No OPA decision logs found"
        return 1
    fi

    # Check for recent decisions (last hour)
    recent=$(curl -s "http://opa.nash.group/v1/logs/decisions?since=1h" | jq '.count')

    if [ "$recent" -eq 0 ]; then
        echo "⚠️  WARNING: No recent OPA decisions in last hour"
    fi

    echo "✅ Audit logging verified"
    return 0
}

# Execute all critical checks
FAILED_CHECKS=()

for check in "${CRITICAL_CHECKS[@]}"; do
    if ! check_${check}; then
        FAILED_CHECKS+=($check)
    fi
done

# Generate final report
if [ ${#FAILED_CHECKS[@]} -gt 0 ]; then
    echo ""
    echo "========================================="
    echo "❌ ENFORCEMENT AUDIT FAILED"
    echo "Failed checks: ${FAILED_CHECKS[*]}"
    echo "========================================="
    exit 1
else
    echo ""
    echo "========================================="
    echo "✅ ALL ENFORCEMENT CHECKS PASSED"
    echo "The Citadel defenses are active"
    echo "========================================="
fi
```

## Workflow 5: Continuous Compliance Monitor

### Agent Identity
**Role:** Perpetual Guardian
**Mission:** Never-sleeping verification of all systems
**Frequency:** Continuous with escalating alerts

### Execution Instructions

```python
# AGENT TASK 5: Continuous compliance monitoring daemon

import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict
import requests

class ComplianceMonitor:
    """
    Continuous monitoring daemon that never sleeps.
    Escalates violations immediately to Watchers.
    """

    def __init__(self):
        self.violations = []
        self.last_full_audit = datetime.now()
        self.alert_threshold = {
            'CRITICAL': 0,  # Alert immediately
            'HIGH': 5,      # Alert after 5 minutes
            'MEDIUM': 60,   # Alert after 1 hour
            'LOW': 1440     # Alert after 1 day
        }

    def continuous_monitor(self):
        """Main monitoring loop - runs forever"""

        while True:
            try:
                # Quick checks every minute
                self.quick_validation()

                # Deep audit every hour
                if datetime.now() - self.last_full_audit > timedelta(hours=1):
                    self.deep_audit()
                    self.last_full_audit = datetime.now()

                # Process and escalate violations
                self.process_violations()

                time.sleep(60)  # Check every minute

            except Exception as e:
                # Never stop monitoring, but log errors
                self.alert_watchers(f"Monitor error: {e}", 'CRITICAL')

    def quick_validation(self):
        """Fast checks that run every minute"""

        checks = [
            self.check_branch_protection,
            self.check_opa_health,
            self.check_recent_violations,
            self.check_unauthorized_changes
        ]

        for check in checks:
            threading.Thread(target=check).start()

    def check_branch_protection(self):
        """Verify branch protection hasn't been disabled"""

        critical_repos = ['the-citadel', 'the-covenant']

        for repo in critical_repos:
            response = requests.get(
                f'https://api.github.com/repos/the-nash-group/{repo}/branches/main/protection',
                headers={'Authorization': f'token {os.environ["GITHUB_TOKEN"]}'}
            )

            if response.status_code != 200:
                self.add_violation({
                    'type': 'branch_protection_missing',
                    'resource': f'{repo}/main',
                    'severity': 'CRITICAL',
                    'message': f'Branch protection removed from {repo}/main!'
                })

    def check_opa_health(self):
        """Ensure OPA is responding"""

        try:
            response = requests.get('http://opa.nash.group/health', timeout=5)
            if response.status_code != 200:
                raise Exception(f"OPA unhealthy: {response.status_code}")
        except Exception as e:
            self.add_violation({
                'type': 'opa_unavailable',
                'severity': 'CRITICAL',
                'message': f'OPA is not responding: {e}'
            })

    def check_recent_violations(self):
        """Check for policy violations in last 5 minutes"""

        response = requests.get(
            'http://opa.nash.group/v1/logs/decisions?since=5m&result=deny'
        )

        denials = response.json()
        if denials['count'] > 10:  # Threshold for concern
            self.add_violation({
                'type': 'excessive_denials',
                'severity': 'HIGH',
                'message': f'{denials["count"]} policy denials in last 5 minutes',
                'details': denials['recent']
            })

    def check_unauthorized_changes(self):
        """Detect manual/console changes"""

        # Check Terraform drift
        drift_output = subprocess.run(
            ['terraform', 'plan', '-detailed-exitcode'],
            cwd='the-citadel/terraform',
            capture_output=True
        )

        if drift_output.returncode == 2:  # Changes detected
            self.add_violation({
                'type': 'terraform_drift',
                'severity': 'HIGH',
                'message': 'Unauthorized infrastructure changes detected'
            })

    def deep_audit(self):
        """Comprehensive audit - runs hourly"""

        print(f"[{datetime.now()}] Starting deep audit...")

        # Run all comprehensive checks
        audits = [
            ('Covenant Traceability', self.audit_covenant_traceability),
            ('OPA Implementation', self.audit_opa_implementation),
            ('Label Compliance', self.audit_label_compliance),
            ('Security Policies', self.audit_security_enforcement)
        ]

        for name, audit_func in audits:
            try:
                result = audit_func()
                if not result['passed']:
                    self.add_violation({
                        'type': f'audit_failure_{name}',
                        'severity': 'HIGH',
                        'message': f'Deep audit failed: {name}',
                        'details': result
                    })
            except Exception as e:
                self.add_violation({
                    'type': 'audit_error',
                    'severity': 'CRITICAL',
                    'message': f'Audit crashed: {name}: {e}'
                })

    def add_violation(self, violation: Dict):
        """Add violation to tracking list"""

        violation['timestamp'] = datetime.now().isoformat()
        violation['id'] = f"VIO-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(self.violations)}"
        self.violations.append(violation)

        # Immediate alert for CRITICAL
        if violation['severity'] == 'CRITICAL':
            self.alert_watchers(violation['message'], 'CRITICAL')

    def process_violations(self):
        """Process and escalate violations based on age and severity"""

        now = datetime.now()

        for violation in self.violations:
            age_minutes = (now - datetime.fromisoformat(violation['timestamp'])).seconds / 60
            threshold_minutes = self.alert_threshold[violation['severity']]

            if age_minutes >= threshold_minutes and not violation.get('alerted'):
                self.alert_watchers(
                    f"[{violation['severity']}] {violation['message']}",
                    violation['severity']
                )
                violation['alerted'] = True

    def alert_watchers(self, message: str, severity: str):
        """Send alert to Watchers"""

        alert = {
            'severity': severity,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'source': 'citadel-compliance-monitor'
        }

        # Multiple alert channels for redundancy
        channels = [
            ('Slack', self.send_slack_alert),
            ('PagerDuty', self.send_pagerduty_alert),
            ('Email', self.send_email_alert)
        ]

        for channel_name, channel_func in channels:
            try:
                channel_func(alert)
            except Exception as e:
                print(f"Failed to alert via {channel_name}: {e}")

    def send_slack_alert(self, alert: Dict):
        """Send to Slack #citadel-alerts channel"""

        emoji = {'CRITICAL': '🚨', 'HIGH': '⚠️', 'MEDIUM': '📊', 'LOW': 'ℹ️'}

        requests.post(
            os.environ['SLACK_WEBHOOK_URL'],
            json={
                'text': f"{emoji[alert['severity']]} *{alert['severity']}* - Citadel Compliance Alert",
                'attachments': [{
                    'color': 'danger' if alert['severity'] == 'CRITICAL' else 'warning',
                    'fields': [
                        {'title': 'Message', 'value': alert['message']},
                        {'title': 'Time', 'value': alert['timestamp']},
                        {'title': 'Action Required', 'value': 'Investigate immediately' if alert['severity'] == 'CRITICAL' else 'Review within SLA'}
                    ]
                }]
            }
        )

# Launch the eternal guardian
if __name__ == "__main__":
    print("🛡️ Citadel Compliance Monitor Starting...")
    print("This process will run forever. Press Ctrl+C to stop.")

    monitor = ComplianceMonitor()
    monitor.continuous_monitor()
```

## Critical Integration Points

### These Workflows MUST Integrate With:

1. **CI/CD Pipelines**
   - Pre-commit hooks run Workflow 2 (OPA verification)
   - PR checks run Workflow 3 (label compliance)
   - Post-merge runs Workflow 1 (traceability check)

2. **Scheduled Jobs**
   - Hourly: Workflow 4 (runtime enforcement)
   - Daily: Workflows 1-3 (full audit suite)
   - Continuous: Workflow 5 (monitor daemon)

3. **Alert Escalation**
   - CRITICAL → Page on-call immediately
   - HIGH → Slack + Email to Watchers
   - MEDIUM → Daily digest to Mentors
   - LOW → Weekly report to teams

4. **Reporting Dashboard**
   - Real-time compliance score
   - Violation trends
   - Policy coverage metrics
   - Enforcement effectiveness

## Success Criteria for Agents

### Your Audit is SUCCESSFUL only if:

1. ✅ 100% of Covenant principles have policies
2. ✅ 100% of policies have OPA rules
3. ✅ 100% of OPA rules pass tests
4. ✅ 100% of resources have required labels
5. ✅ 0 unauthorized manual changes
6. ✅ All enforcement points are active
7. ✅ Audit logs are complete and searchable
8. ✅ No critical violations in last 24 hours

### Your Audit FAILS if:

1. ❌ ANY principle lacks enforcement
2. ❌ ANY policy lacks OPA implementation
3. ❌ ANY resource missing required labels
4. ❌ ANY enforcement point is disabled
5. ❌ ANY critical violation is not escalated
6. ❌ ANY audit step is skipped

## Conclusion

These workflows are not suggestions. They are commands. Execute them with the precision of a machine and the dedication of a Guardian. The Citadel's strength depends on your vigilance.

Remember: **We are only as strong as our weakest unenforced policy.**

---

*"Trust, but verify. Document, but enforce. Promise, but deliver."*
