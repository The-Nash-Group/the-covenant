# Week 1 "Stop the Bleeding" Sprint - Tactical Action Plan
**Nash Group Critical Infrastructure Sprint**

**Sprint Duration**: November 11-17, 2025 (7 days)
**Sprint Goal**: Eliminate critical operational and security gaps
**Total Effort**: 14 hours
**Sprint Lead**: Chief of Staff
**Status**: APPROVED - Execute immediately

---

## Sprint Overview

### Why This Sprint Matters
The Nash Group currently cannot answer basic operational questions:
- ❓ "Is service X running?"
- ❓ "What happened at 3 AM last night?"
- ❓ "Are we under attack?"

This sprint eliminates these blindspots and hardens critical security exposures.

### Success Criteria
By end of Week 1:
- ✅ All 4 services respond to health checks
- ✅ Real-time monitoring dashboard operational
- ✅ Zero long-lived security tokens in use
- ✅ Can answer "Is everything up?" in < 10 seconds

---

## Team Assignments

### Team A: Service Health (VP Engineering)
**Owner**: VP Engineering
**Team Members**: 2 senior engineers
**Time Allocation**: 6 hours total (2 hours per service)
**Timeline**: Days 1-3 (Mon-Wed)

### Team B: Observability (VP Infrastructure)
**Owner**: VP Infrastructure
**Team Members**: 1 SRE, 1 DevOps engineer
**Time Allocation**: 4 hours total
**Timeline**: Days 3-4 (Wed-Thu)

### Team C: Security Hardening (CISO)
**Owner**: Chief Information Security Officer
**Team Members**: 1 security engineer
**Time Allocation**: 4 hours total
**Timeline**: Days 5-7 (Fri-Sun)

---

## Daily Schedule

### Monday, November 11
**Focus**: Service health implementation kickoff

**8:00 AM**: Sprint kickoff meeting (30 min)
- Review sprint goals
- Confirm team assignments
- Set up communication channels (#infrastructure-sprint)

**9:00 AM - 5:00 PM**: Team A works on service health
- Target: bridge service health endpoints (2 hours)
- Reference implementation: ds service (already complete)

**5:00 PM**: Daily standup (15 min)
- Progress: bridge service complete
- Blockers: None expected
- Tomorrow: mcp + dashboard services

---

### Tuesday, November 12
**Focus**: Complete remaining service health endpoints

**9:00 AM - 5:00 PM**: Team A continues
- Morning: mcp service health endpoints (2 hours)
- Afternoon: dashboard service health endpoints (2 hours)

**5:00 PM**: Daily standup (15 min)
- Progress: All 4 services have health endpoints
- Blockers: Escalate any issues to Chief of Staff
- Tomorrow: Monitoring deployment

**Gate Check**: All 4 services must have health endpoints before proceeding

---

### Wednesday, November 13
**Focus**: Deploy monitoring infrastructure

**9:00 AM - 12:00 PM**: Team B deploys Grafana Cloud
- Sign up for Grafana Cloud free tier
- Configure agent on each service
- Verify metrics flowing

**1:00 PM - 3:00 PM**: Team B creates "Is Everything Up?" dashboard
- Show health status of all 4 services
- Display uptime percentage
- Show last successful health check time

**3:00 PM - 5:00 PM**: Team B configures alerting
- Email/Slack alerts for service down
- Test alerting by stopping one service

**5:00 PM**: Daily standup (15 min)
- Progress: Monitoring operational
- Blockers: Escalate immediately
- Tomorrow: Security hardening begins

**Gate Check**: Dashboard must show all 4 services before proceeding

---

### Thursday, November 14
**Focus**: Validate monitoring, prep security work

**9:00 AM - 12:00 PM**: Team A + Team B validation
- Verify all health endpoints working
- Confirm dashboard updates in real-time
- Test alerting (stop a service, verify alert fires)

**1:00 PM - 5:00 PM**: Team C security assessment
- Audit current OIDC configuration
- Identify all uses of TF_CLOUD_TOKEN
- Plan OIDC implementation approach

**5:00 PM**: Daily standup (15 min)
- Progress: Monitoring validated, security plan ready
- Blockers: Escalate immediately
- Tomorrow: OIDC implementation

---

### Friday, November 15
**Focus**: Implement OIDC security hardening

**9:00 AM - 1:00 PM**: Team C OIDC implementation (4 hours)
- Update the-citadel Terraform workflows
- Configure OIDC trust relationship with GitHub
- Test token exchange works end-to-end
- Remove TF_CLOUD_TOKEN from GitHub secrets

**1:00 PM - 3:00 PM**: Team C validation
- Run terraform plan via OIDC
- Verify no fallback to long-lived token
- Document OIDC troubleshooting in runbook

**3:00 PM - 5:00 PM**: Sprint review prep
- Gather metrics
- Prepare demo
- Document lessons learned

**5:00 PM**: Daily standup (15 min)
- Progress: OIDC complete
- Blockers: Resolve before Monday
- Tomorrow: Weekend monitoring

**Gate Check**: Must successfully apply Terraform via OIDC before completing sprint

---

### Saturday-Sunday, November 16-17
**Focus**: Monitoring, catch-up if needed

**Passive monitoring**: Verify services stay healthy over weekend
**On-call**: Team lead available for critical issues
**Catch-up time**: If any work slipped, complete by Sunday EOD

---

## Task Breakdown by Team

### Team A: Service Health Implementation

#### Task 1: bridge Service Health Endpoints (2 hours)
**Location**: `/Users/verlyn13/Development/the-nash-group/the-nexus/apps/bridge/`

**Steps**:
1. Review existing ds health implementation for reference
2. Create `/health/live` endpoint (simple, always returns 200 OK)
3. Create `/health/ready` endpoint (checks dependencies)
4. Test locally: `curl http://localhost:7171/health/live`
5. Update bridge README with health endpoint documentation
6. Create PR, get review, merge

**Reference Implementation** (Node.js):
```javascript
// Add to apps/bridge/src/server.ts

app.get('/health/live', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    service: 'bridge'
  });
});

app.get('/health/ready', async (req, res) => {
  try {
    // Check database connection
    const dbCheck = await checkDatabase();

    // Check external dependencies
    const externalChecks = await Promise.all([
      checkDsService(),
      // Add other dependencies
    ]);

    const allHealthy = dbCheck.healthy &&
                       externalChecks.every(c => c.healthy);

    res.status(allHealthy ? 200 : 503).json({
      status: allHealthy ? 'ready' : 'not_ready',
      timestamp: new Date().toISOString(),
      service: 'bridge',
      checks: {
        database: dbCheck,
        ds_service: externalChecks[0],
      }
    });
  } catch (error) {
    res.status(503).json({
      status: 'not_ready',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});
```

**Acceptance Criteria**:
- ✅ `/health/live` returns 200 with JSON payload
- ✅ `/health/ready` checks actual dependencies
- ✅ Tests pass locally
- ✅ Documentation updated
- ✅ PR merged

---

#### Task 2: mcp Service Health Endpoints (2 hours)
**Location**: `/Users/verlyn13/Development/the-nash-group/the-nexus/apps/mcp/`

**Note**: MCP uses stdio (no HTTP), so health check is simulated via ds

**Alternative Approach**:
```javascript
// Add health check via MCP protocol
export const healthTools = {
  health_check: {
    name: 'health_check',
    description: 'Check MCP server health',
    inputSchema: {
      type: 'object',
      properties: {}
    },
    handler: async () => {
      return {
        status: 'ok',
        timestamp: new Date().toISOString(),
        service: 'mcp',
        dependencies: {
          ds_service: await checkDsHealth()
        }
      };
    }
  }
};
```

**Acceptance Criteria**:
- ✅ Health check tool available via MCP protocol
- ✅ Tests pass locally
- ✅ Documentation updated
- ✅ PR merged

---

#### Task 3: dashboard Service Health Endpoints (2 hours)
**Location**: `/Users/verlyn13/Development/the-nash-group/the-nexus/apps/dashboard/`

**Steps**:
1. Add health endpoints to Express backend
2. Create `/health/live` endpoint
3. Create `/health/ready` endpoint (check backend dependencies)
4. Test locally: `curl http://localhost:3001/health/live`
5. Update dashboard README
6. Create PR, merge

**Reference Implementation** (Express):
```javascript
// Add to apps/dashboard/server/index.ts

app.get('/health/live', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    service: 'dashboard'
  });
});

app.get('/health/ready', async (req, res) => {
  try {
    const checks = {
      ds_service: await fetch('http://localhost:7777/v1/health')
        .then(r => ({ healthy: r.ok }))
        .catch(() => ({ healthy: false })),
      bridge_service: await fetch('http://localhost:7171/health/live')
        .then(r => ({ healthy: r.ok }))
        .catch(() => ({ healthy: false }))
    };

    const allHealthy = Object.values(checks).every(c => c.healthy);

    res.status(allHealthy ? 200 : 503).json({
      status: allHealthy ? 'ready' : 'not_ready',
      timestamp: new Date().toISOString(),
      service: 'dashboard',
      checks
    });
  } catch (error) {
    res.status(503).json({
      status: 'not_ready',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});
```

**Acceptance Criteria**:
- ✅ `/health/live` returns 200 with JSON payload
- ✅ `/health/ready` checks ds and bridge services
- ✅ Tests pass locally
- ✅ Documentation updated
- ✅ PR merged

---

### Team B: Observability Foundation

#### Task 1: Deploy Grafana Cloud (1 hour)

**Steps**:
1. Sign up for Grafana Cloud free tier: https://grafana.com/auth/sign-up/create-user
2. Create organization: "The Nash Group"
3. Note API key and endpoints
4. Install Grafana Agent on each service host

**Configuration**:
```yaml
# grafana-agent.yaml
server:
  log_level: info

metrics:
  global:
    scrape_interval: 15s
  configs:
    - name: nash-services
      scrape_configs:
        - job_name: 'bridge'
          static_configs:
            - targets: ['localhost:7171']
        - job_name: 'ds'
          static_configs:
            - targets: ['localhost:7777']
        - job_name: 'dashboard'
          static_configs:
            - targets: ['localhost:3001']
      remote_write:
        - url: ${GRAFANA_CLOUD_ENDPOINT}
          basic_auth:
            username: ${GRAFANA_CLOUD_USER}
            password: ${GRAFANA_CLOUD_API_KEY}
```

**Acceptance Criteria**:
- ✅ Grafana Cloud account created
- ✅ Agent installed on each host
- ✅ Metrics flowing to Grafana Cloud
- ✅ Can query metrics in Grafana UI

---

#### Task 2: Create "Is Everything Up?" Dashboard (2 hours)

**Dashboard Panels**:
1. **Service Status Grid** - Green/red for each service
2. **Uptime Percentage** - 24-hour rolling average
3. **Last Health Check** - Timestamp for each service
4. **Request Rate** - Requests per second
5. **Error Rate** - Percentage of 5xx responses

**Grafana Dashboard JSON**:
```json
{
  "dashboard": {
    "title": "Is Everything Up?",
    "panels": [
      {
        "title": "Service Health Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job='bridge'}",
            "legendFormat": "bridge"
          },
          {
            "expr": "up{job='ds'}",
            "legendFormat": "ds"
          },
          {
            "expr": "up{job='dashboard'}",
            "legendFormat": "dashboard"
          }
        ],
        "thresholds": [
          { "value": 0, "color": "red" },
          { "value": 1, "color": "green" }
        ]
      }
    ]
  }
}
```

**Acceptance Criteria**:
- ✅ Dashboard shows all 4 services
- ✅ Green/red status clearly visible
- ✅ Updates in real-time
- ✅ Accessible via URL (bookmark in team Slack)

---

#### Task 3: Configure Alerting (1 hour)

**Alert Rules**:
1. **Service Down** - Fire if service unreachable for 1 minute
2. **Service Unhealthy** - Fire if `/health/ready` returns 503 for 5 minutes
3. **High Error Rate** - Fire if 5xx > 5% for 10 minutes

**Alert Configuration**:
```yaml
# alerts.yaml
groups:
  - name: service_health
    interval: 1m
    rules:
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"

      - alert: ServiceUnhealthy
        expr: http_health_ready_status != 200
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Service {{ $labels.job }} is unhealthy"
```

**Notification Channels**:
- Email: infrastructure-team@thenash.group
- Slack: #infrastructure-alerts

**Acceptance Criteria**:
- ✅ Alert rules configured in Grafana
- ✅ Test alerts fire when simulated
- ✅ Notifications delivered to email + Slack
- ✅ Alert runbook URL included in notification

---

### Team C: OIDC Security Hardening

#### Task 1: Complete OIDC Implementation (4 hours)

**Current State**:
- OIDC permissions configured (`id-token: write`)
- Fallback to `TF_CLOUD_TOKEN` still exists

**Target State**:
- OIDC exclusively, no token fallback
- `TF_CLOUD_TOKEN` secret deleted

**Steps**:

**Step 1: Verify OIDC Trust (30 min)**
```bash
# In HCP Terraform workspace settings
# Verify OIDC provider configured:
# - Provider: token.actions.githubusercontent.com
# - Audience: https://app.terraform.io
# - Organization: the-nash-group
```

**Step 2: Update Terraform Workflows (1 hour)**
```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
  push:
    branches: [main]

permissions:
  id-token: write  # Required for OIDC
  contents: read
  pull-requests: write

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          cli_config_credentials_token: "" # Don't use token!

      - name: Configure OIDC
        run: |
          # OIDC happens automatically via GitHub Actions OIDC provider
          echo "Using OIDC authentication"

      - name: Terraform Init
        run: terraform init
        env:
          TF_CLOUD_ORGANIZATION: the-nash-group
          TF_WORKSPACE: citadel-production
          # NO TF_CLOUD_TOKEN!

      - name: Terraform Plan
        run: terraform plan -no-color

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve
```

**Step 3: Test OIDC Authentication (1 hour)**
```bash
# Create test branch
git checkout -b test/oidc-validation

# Make trivial change
echo "# OIDC Test" >> terraform/test.txt

# Commit and push
git add terraform/test.txt
git commit -m "test: validate OIDC authentication"
git push origin test/oidc-validation

# Create PR and verify workflow runs with OIDC
# Watch GitHub Actions logs for:
# ✅ "Using OIDC authentication"
# ✅ Terraform init succeeds
# ✅ No mention of TF_CLOUD_TOKEN
```

**Step 4: Remove Token Fallback (30 min)**
```bash
# In GitHub repository settings
# Navigate to: Settings > Secrets and variables > Actions
# Delete: TF_CLOUD_TOKEN

# Verify no other workflows use TF_CLOUD_TOKEN:
grep -r "TF_CLOUD_TOKEN" .github/workflows/
# Should return: (no matches)
```

**Step 5: Document OIDC Flow (1 hour)**
Create `the-citadel/docs/OIDC-AUTHENTICATION.md`:

```markdown
# OIDC Authentication for Terraform

## Overview
The Citadel uses OIDC (OpenID Connect) for zero-trust authentication with HCP Terraform.

## How It Works
1. GitHub Actions generates OIDC token
2. Token includes claims: repo, ref, workflow
3. HCP Terraform validates token against trust policy
4. Short-lived credentials granted (1 hour)
5. Terraform operations execute
6. Credentials expire automatically

## Troubleshooting
See: the-citadel/docs/OIDC-TROUBLESHOOTING.md
```

**Acceptance Criteria**:
- ✅ OIDC trust configured in HCP Terraform
- ✅ Workflows use OIDC exclusively
- ✅ TF_CLOUD_TOKEN deleted from GitHub
- ✅ Test terraform apply succeeds via OIDC
- ✅ Documentation complete
- ✅ Audit log shows OIDC usage (not token)

---

## Sprint Ceremonies

### Daily Standup (15 minutes, 5:00 PM)
**Format**:
- What did you complete today?
- What will you work on tomorrow?
- Any blockers?

**Attendance**: All team members + Chief of Staff
**Location**: Slack #infrastructure-sprint (async) or Zoom (if needed)

---

### Sprint Review (Friday, 3:00 PM, 1 hour)
**Agenda**:
1. Demo: Health endpoints working (10 min)
2. Demo: "Is Everything Up?" dashboard (10 min)
3. Demo: OIDC authentication (10 min)
4. Metrics review (10 min)
5. Lessons learned (10 min)
6. Next sprint planning (10 min)

**Attendees**:
- All sprint team members
- Chief of Staff
- CTO (optional)
- VP Engineering
- VP Infrastructure
- CISO

**Deliverables**:
- Working demo recorded
- Sprint metrics documented
- Lessons learned captured
- Next sprint backlog prioritized

---

## Success Metrics

### Implementation Score
**Baseline**: 45/100
**Target**: 60/100
**Actual**: ___/100 (measure at sprint end)

### Component Completion
- [ ] bridge health endpoints (2 hours)
- [ ] mcp health endpoints (2 hours)
- [ ] dashboard health endpoints (2 hours)
- [ ] Grafana Cloud deployed (1 hour)
- [ ] "Is Everything Up?" dashboard (2 hours)
- [ ] Alerting configured (1 hour)
- [ ] OIDC implementation (4 hours)

**Total**: 14 hours
**Completed**: ___/14 hours

### Business Value Delivered
- ✅ Can answer "Is service X up?" (Yes/No)
- ✅ Monitoring dashboard operational (Yes/No)
- ✅ Alerts fire when service down (Yes/No)
- ✅ Zero long-lived tokens (Yes/No)

### Risk Reduction
- **Before**: Cannot detect outages (Risk: 9/10)
- **After**: Real-time monitoring (Risk: 3/10)
- **Risk Reduction**: 67%

- **Before**: Long-lived tokens (Risk: 8/10)
- **After**: OIDC only (Risk: 2/10)
- **Risk Reduction**: 75%

---

## Blockers & Escalation

### Known Risks
1. **Team availability** - Holiday schedules, PTO
2. **Grafana Cloud signup** - Credit card required for free tier
3. **OIDC trust** - May need HCP Terraform support ticket
4. **Service restarts** - May impact users

### Escalation Path
**Level 1 (Minor blocker, <1 hour delay)**:
- Raise in daily standup
- Team lead resolves

**Level 2 (Moderate blocker, 1-4 hour delay)**:
- Tag Chief of Staff in Slack
- Response within 1 hour

**Level 3 (Critical blocker, >4 hour delay)**:
- Emergency call with Chief of Staff + CTO
- Immediate resource reallocation

**Level 4 (Sprint-breaking blocker)**:
- Executive decision required
- May pause sprint, reassess approach

---

## Post-Sprint Actions

### Immediate (Monday, November 18)
1. Sprint retrospective (1 hour)
2. Deploy to production (if in staging)
3. Monitor for 24 hours
4. Document final metrics

### Week 2 Actions
1. Begin Month 1 standardization sprint
2. Address any technical debt from Week 1
3. Share success with broader organization
4. Recognize team contributions

---

## Communication Plan

### Internal Communication
**Slack #infrastructure-sprint**:
- Daily progress updates
- Blocker discussions
- Demo recordings

**Email to Leadership**:
- Friday EOD sprint summary
- Key metrics and achievements
- Photos/screenshots of dashboard

### External Communication
**Engineering All-Hands**:
- Share dashboard in next meeting
- Recognize team contributions
- Inspire others with operational excellence

---

## Resources & References

### Documentation
- [Nash Group Organization Spec](../ORGANIZATION-SPEC.md)
- [Implementation Gap Report](../.org/audits/IMPLEMENTATION-GAP-REPORT-2025-10-31.md)
- [Technical Principles](../the-covenant/PRINCIPLES.md)

### Tools
- Grafana Cloud: https://grafana.com/auth/sign-up/create-user
- HCP Terraform: https://app.terraform.io/
- GitHub Actions OIDC: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect

### Reference Implementations
- ds service health: `/Users/verlyn13/Development/the-nash-group/the-nexus/apps/ds/internal/server/`
- Prometheus client (Node): https://github.com/siimon/prom-client
- OpenTelemetry (Node): https://opentelemetry.io/docs/languages/js/

---

## Contact Information

**Sprint Lead**: Chief of Staff
**Email**: chief-of-staff@thenash.group
**Slack**: @chief-of-staff
**Emergency**: [Phone number]

**VP Engineering**: [Name]
**VP Infrastructure**: [Name]
**CISO**: [Name]

---

**Sprint Start**: Monday, November 11, 2025, 9:00 AM
**Sprint End**: Sunday, November 17, 2025, 11:59 PM
**Sprint Review**: Friday, November 15, 2025, 3:00 PM

**Let's make The Nash Group operationally excellent!** 🚀

---

*"Stop the bleeding first, then build. This sprint saves lives (and uptime)."*
