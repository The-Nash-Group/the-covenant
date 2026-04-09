# OPS-003: Fail Fast Architecture

**Policy ID:** OPS-003
**Category:** Operations
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Systems **must** fail quickly and obviously when something is wrong. Silent failures and degraded states are the enemy. A system that limps along with partial failures is harder to debug than one that fails completely.

## Rationale

A system that limps along with partial failures is harder to debug than one that fails completely. We've lost more data to silent corruption than to hard crashes:

- **Silent Corruption**: Gradual degradation goes unnoticed until catastrophic
- **Debugging Difficulty**: Intermittent issues are exponentially harder to diagnose
- **Data Integrity**: Partial failures can corrupt state while appearing functional
- **Cascading Failures**: Limping services become bottlenecks for dependent systems
- **False Confidence**: Degraded performance masks underlying issues
- **Resource Waste**: Failing services consume resources without providing value

Fast failure enables quick detection, immediate response, and clean recovery paths.

## Scope

**Applies To:**
- All services and applications deployed by The Nash Group
- All health monitoring and observability systems
- All external dependencies and integration points
- All batch processing and background job systems
- All data processing and storage systems

**Exceptions:**
- Graceful degradation scenarios with explicit monitoring and alerting
- Planned maintenance modes with clear status communication

## Implementation

### Technical Enforcement

Health check endpoint requirements:

```go
// Standard health check implementation
func healthHandler(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
    defer cancel()

    // Check critical dependencies with fail-fast semantics
    checks := []HealthCheck{
        {Name: "database", Check: checkDatabase(ctx)},
        {Name: "redis", Check: checkRedis(ctx)},
        {Name: "external-api", Check: checkExternalAPI(ctx)},
    }

    allHealthy := true
    for _, check := range checks {
        if err := check.Check; err != nil {
            log.Error("Health check failed", "service", check.Name, "error", err)
            allHealthy = false
        }
    }

    if !allHealthy {
        w.WriteHeader(http.StatusServiceUnavailable)
        json.NewEncoder(w).Encode(map[string]string{
            "status": "unhealthy",
            "timestamp": time.Now().UTC().Format(time.RFC3339),
        })
        return
    }

    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{
        "status": "healthy",
        "timestamp": time.Now().UTC().Format(time.RFC3339),
    })
}
```

Cloudflare health check configuration:

```hcl
# the-citadel/terraform/cloudflare/health_checks.tf
resource "cloudflare_healthcheck" "service_health" {
  for_each = var.services

  zone_id     = data.cloudflare_zone.nash_group.id
  name        = "${each.key}-health"
  address     = each.value.health_endpoint
  type        = "HTTPS"
  port        = 443
  path        = "/health"

  # Fail fast configuration
  interval          = 30    # Check every 30 seconds
  retries          = 2     # Fail after 2 consecutive failures
  timeout          = 10    # 10 second timeout per check
  consecutive_up   = 2     # Require 2 successes to mark healthy

  # Expected response
  expected_codes = ["200"]
  method         = "GET"
  follow_redirects = false

  # Immediate alerting on failure
  notification_email_addresses = [
    "alerts@thenash.group"
  ]
}
```

### Automated Validation

**Service Health Monitoring:**
- Standard `/health` and `/ready` endpoints for all services
- Cloudflare health checks with fail-fast thresholds
- Immediate alerts on health check failures
- Automated traffic shifting away from unhealthy instances

**Circuit Breaker Implementation:**
- Automatic circuit breaking for external dependencies
- Fail-fast behavior when circuit is open
- Exponential backoff for recovery attempts
- Metrics and alerting on circuit breaker state changes

**Timeout Configuration:**
- Aggressive timeouts for all external calls
- Request timeout enforcement at multiple layers
- Database query timeout limits
- HTTP client timeout configuration

### Human Process

1. **Service Design**: Build services with explicit failure modes
2. **Health Endpoint Development**: Implement comprehensive health checks
3. **Monitoring Setup**: Configure alerts for all failure scenarios
4. **Incident Response**: Rapid response to service failures
5. **Post-Incident Analysis**: Learn from failures to improve detection

## Failure Detection Standards

### Health Check Requirements

**Critical Health Indicators:**
- Database connectivity and basic query execution
- External service reachability and response time
- Memory and disk space availability
- Critical configuration validity

**Health Check Response Times:**
- Health endpoint response under 5 seconds
- Database health check under 2 seconds
- External service health check under 3 seconds
- Overall health evaluation under 10 seconds

### Alerting Thresholds

**Immediate Alerts:**
- Any health check failure (within 1 minute)
- Response time exceeding SLA thresholds
- Error rate above 1% for more than 2 minutes
- Any service becoming unreachable

**Escalation Triggers:**
- Health check failures lasting more than 5 minutes
- Multiple service failures indicating systemic issues
- Customer-facing error rates above 0.1%

## Circuit Breaker Configuration

### Implementation Standards

```go
// Circuit breaker for external dependencies
type CircuitBreaker struct {
    failureThreshold int           // Fail after 5 consecutive failures
    timeout         time.Duration  // Open circuit for 60 seconds
    maxRequests     int           // Allow 3 requests in half-open state
}

func (cb *CircuitBreaker) Call(fn func() error) error {
    if cb.State() == Open {
        return ErrCircuitOpen
    }

    err := fn()
    if err != nil {
        cb.recordFailure()
        return err
    }

    cb.recordSuccess()
    return nil
}
```

### Circuit Breaker Policies

**External Services:**
- Fail after 5 consecutive failures
- Open circuit for 60 seconds
- Half-open state allows 3 test requests
- Immediate failure response when circuit is open

**Database Connections:**
- Fail after 3 consecutive connection failures
- Open circuit for 30 seconds
- Health check required before closing circuit

## Compliance Verification

**Automated Checks:**
- Health endpoint availability monitoring
- Response time threshold enforcement
- Circuit breaker state tracking
- Alert generation and delivery verification

**Manual Audits:**
- Monthly review of failure detection effectiveness
- Quarterly assessment of incident response times
- Annual disaster recovery testing with forced failures

**Reporting:**
- Real-time dashboard of service health status
- Weekly failure detection and response metrics
- Monthly analysis of mean time to detection (MTTD) trends

## Emergency Procedures

### Service Failure Response

**Immediate Actions (within 5 minutes):**
1. **Automatic Response**: Health checks trigger traffic rerouting
2. **Alert Triage**: On-call engineer assesses failure scope
3. **Communication**: Status page update for customer-facing impacts
4. **Isolation**: Failing services isolated from healthy ones

**Investigation and Recovery:**
1. **Root Cause**: Rapid diagnosis of failure root cause
2. **Remediation**: Fix underlying issue or implement workaround
3. **Verification**: Confirm health checks pass before restoring traffic
4. **Documentation**: Record incident details and response actions

### False Positive Handling

**Health Check Validation:**
1. **Correlation**: Verify multiple health indicators before acting
2. **Manual Override**: Emergency procedures for health check failures
3. **Escalation**: Human verification for ambiguous health states
4. **Tuning**: Adjust health check sensitivity based on false positives

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 8: Fail Fast, Recover Faster](../the-covenant/PRINCIPLES.md#principle-8-fail-fast-recover-faster)
- **Governance Authority:** [GOVERNANCE.md - Operations Standards](../the-covenant/GOVERNANCE.md#stronghold-decisions-individual-repositories)
- **Implementation:** `the-citadel/terraform/cloudflare/health_checks.tf`
- **Monitoring:** [OPS-004 Observability Requirements](./ops-004-observability.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 8: Fail Fast, Recover Faster
