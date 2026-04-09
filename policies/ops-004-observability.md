# OPS-004: Observability Requirements

**Policy ID:** OPS-004
**Category:** Operations
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Every service **must** emit metrics, logs, and traces. Observability is not optional—it's fundamental. "It seems slow" is not actionable; "The P99 latency increased from 200ms to 800ms starting at 14:23 UTC" is.

## Rationale

"It seems slow" is not actionable. "The P99 latency increased from 200ms to 800ms starting at 14:23 UTC" is. We cannot fix what we cannot see:

- **Invisible Problems**: Issues that can't be measured can't be resolved
- **Reactive Debugging**: Without observability, debugging becomes archaeology
- **Performance Guesswork**: Optimization without metrics is gambling
- **Incident Blindness**: Can't respond effectively to issues you can't see
- **Capacity Planning**: Growth planning requires historical data and trends
- **User Impact**: Customer experience problems hide in unmeasured systems

Comprehensive observability enables proactive problem detection, effective debugging, and data-driven optimization.

## Scope

**Applies To:**
- All services and applications deployed by The Nash Group
- All microservices and background job processors
- All external integrations and API endpoints
- All database operations and data processing pipelines
- All infrastructure components and supporting systems

**Exceptions:**
- Static websites and content delivery (basic access logging sufficient)
- One-time scripts and utilities (logging only, no metrics required)

## Implementation

### Technical Enforcement

Standard observability implementation requirements:

```go
// Standard structured logging
import (
    "github.com/sirupsen/logrus"
    "github.com/opentelemetry/opentelemetry-go/trace"
    "github.com/prometheus/client_golang/prometheus"
)

// Required log fields for all services
type LogFields struct {
    Service     string    `json:"service"`
    Version     string    `json:"version"`
    Environment string    `json:"environment"`
    TraceID     string    `json:"trace_id"`
    SpanID      string    `json:"span_id"`
    UserID      string    `json:"user_id,omitempty"`
    RequestID   string    `json:"request_id"`
    Timestamp   time.Time `json:"timestamp"`
    Level       string    `json:"level"`
    Message     string    `json:"message"`
}

// Standard metrics for all HTTP services
var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status_code"},
    )

    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )

    httpActiveConnections = prometheus.NewGauge(
        prometheus.GaugeOpts{
            Name: "http_active_connections",
            Help: "Current number of active HTTP connections",
        },
    )
)
```

OpenTelemetry tracing configuration:

```go
// Standard tracing setup for all services
func initTracing(serviceName string) {
    exporter, err := jaeger.New(
        jaeger.WithCollectorEndpoint(jaeger.WithEndpoint("http://jaeger:14268/api/traces")),
    )
    if err != nil {
        log.Fatal("Failed to initialize Jaeger exporter:", err)
    }

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String(serviceName),
            semconv.ServiceVersionKey.String(os.Getenv("SERVICE_VERSION")),
            semconv.DeploymentEnvironmentKey.String(os.Getenv("ENVIRONMENT")),
        )),
    )

    otel.SetTracerProvider(tp)
}
```

### Automated Validation

**Metrics Collection Standards:**
- Prometheus metrics exposition on `/metrics` endpoint
- Standard RED metrics (Rate, Errors, Duration) for all services
- Custom business metrics relevant to service function
- Resource utilization metrics (CPU, memory, disk, network)

**Logging Standards:**
- Structured JSON logging to stdout/stderr
- Consistent log levels: DEBUG, INFO, WARN, ERROR, FATAL
- Correlation IDs for request tracing across services
- No sensitive data (PII, credentials) in logs

**Distributed Tracing:**
- OpenTelemetry instrumentation for all external calls
- Trace propagation across service boundaries
- Custom spans for important business operations
- Error and exception tracking in traces

### Human Process

1. **Service Development**: Build observability into service from day one
2. **Monitoring Setup**: Configure alerts and dashboards during deployment
3. **SLI/SLO Definition**: Define Service Level Indicators and Objectives
4. **Incident Response**: Use observability data for rapid issue resolution
5. **Performance Optimization**: Regular review of metrics for optimization opportunities

## Observability Standards

### Required Metrics by Service Type

**Web Services:**
```prometheus
# Essential HTTP service metrics
http_requests_total{method, endpoint, status_code}
http_request_duration_seconds{method, endpoint}
http_active_connections
http_request_size_bytes{method, endpoint}
http_response_size_bytes{method, endpoint}
```

**Background Services:**
```prometheus
# Job processing metrics
jobs_processed_total{queue, status}
job_duration_seconds{queue}
jobs_in_queue{queue}
job_failures_total{queue, error_type}
job_retries_total{queue}
```

**Database Services:**
```prometheus
# Database connection and query metrics
db_connections_active{database}
db_connections_idle{database}
db_query_duration_seconds{database, operation}
db_queries_total{database, operation, status}
db_connection_errors_total{database}
```

### Service Level Indicators (SLIs)

**Availability SLIs:**
- Percentage of successful HTTP requests (non-5xx responses)
- Percentage of successful health check responses
- Uptime percentage based on external monitoring

**Latency SLIs:**
- P50, P95, P99 response time for critical endpoints
- Time to first byte for content delivery
- End-to-end transaction completion time

**Error Rate SLIs:**
- Percentage of requests resulting in errors
- Business logic error rates
- External dependency failure rates

### Service Level Objectives (SLOs)

**Standard SLO Targets:**
```yaml
# Example SLO definitions
slos:
  availability:
    target: 99.9%
    measurement_window: 30d
    error_budget: 43m  # 0.1% of 30 days

  latency:
    p99_target: 500ms
    p95_target: 200ms
    measurement_window: 7d

  error_rate:
    target: 0.1%
    measurement_window: 24h
```

## Monitoring and Alerting

### Alert Configuration Standards

```yaml
# Prometheus alerting rules template
groups:
  - name: service.rules
    rules:
      - alert: HighErrorRate
        expr: |
          (
            rate(http_requests_total{status_code=~"5.."}[5m]) /
            rate(http_requests_total[5m])
          ) > 0.01
        for: 2m
        labels:
          severity: warning
          service: "{{ $labels.service }}"
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} for service {{ $labels.service }}"
          runbook_url: "https://runbooks.nash.group/high-error-rate"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
          service: "{{ $labels.service }}"
        annotations:
          summary: "High latency detected"
          description: "P99 latency is {{ $value }}s for service {{ $labels.service }}"
          runbook_url: "https://runbooks.nash.group/high-latency"
```

### Dashboard Requirements

**Standard Dashboard Sections:**
1. **Service Overview**: Health, request rate, error rate, latency
2. **Resource Utilization**: CPU, memory, disk, network usage
3. **Business Metrics**: Service-specific KPIs and business logic metrics
4. **External Dependencies**: Status and performance of upstream services
5. **Alerting Status**: Current alerts and their severity levels

## Compliance Verification

**Automated Checks:**
- Metrics endpoint availability and response validation
- Log format compliance and structured data verification
- Trace propagation testing across service boundaries
- Alert rule syntax validation and testing

**Manual Audits:**
- Monthly review of observability coverage and effectiveness
- Quarterly assessment of SLI/SLO performance and targets
- Annual review of monitoring costs and optimization opportunities

**Reporting:**
- Real-time service health dashboard across all services
- Weekly observability compliance reports
- Monthly SLO performance and error budget consumption reports

## Incident Response Integration

### Observability During Incidents

**Immediate Data Access:**
- Pre-built dashboards for rapid incident assessment
- Automated correlation of metrics, logs, and traces
- Historical comparison views for anomaly identification
- Real-time alerting integration with incident management

**Post-Incident Analysis:**
- Historical data retention for thorough post-mortems
- Correlation analysis between observability signals and incidents
- Root cause analysis using distributed tracing data
- Documentation of observability gaps discovered during incidents

### Continuous Improvement

**Observability Retrospectives:**
1. **Monthly**: Review observability effectiveness during recent incidents
2. **Quarterly**: Assess gaps in monitoring coverage and alerting quality
3. **Annually**: Evaluate observability tooling and process improvements

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 11: If It's Not Measured, It Doesn't Exist](../the-covenant/PRINCIPLES.md#principle-11-if-its-not-measured-it-doesnt-exist)
- **Governance Authority:** [GOVERNANCE.md - Operations Standards](../the-covenant/GOVERNANCE.md#stronghold-decisions-individual-repositories)
- **Implementation:** Service templates, monitoring infrastructure
- **Runbooks:** [OPS-005 Runbook Standards](./ops-005-runbooks.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 11: If It's Not Measured, It Doesn't Exist
