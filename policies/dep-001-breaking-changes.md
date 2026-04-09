# DEP-001: Breaking Change Management

**Policy ID:** DEP-001
**Category:** Deployment
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Breaking changes **must** require migration paths. Deprecation **must** require notice periods. Evolution **must** require backward compatibility. Moving fast and breaking things breaks trust.

## Rationale

Moving fast and breaking things breaks trust. We've seen services abandoned because upgrades were too painful. Smooth migrations build confidence:

- **User Trust Erosion**: Breaking changes without migration paths frustrate users and partners
- **Integration Fragility**: Downstream systems break when APIs change without notice
- **Adoption Resistance**: Teams avoid updating dependencies that frequently break compatibility
- **Support Burden**: Breaking changes create support tickets and emergency fixes
- **Technical Debt**: Rushed breaking changes often require follow-up fixes
- **Ecosystem Fragmentation**: Incompatible versions create maintenance nightmares

Careful change management enables continuous evolution while maintaining system stability and user confidence.

## Scope

**Applies To:**
- All public APIs (REST, GraphQL, gRPC) exposed to external teams
- All internal APIs consumed by multiple services
- All libraries and packages published to internal or external registries
- All configuration schemas and data formats
- All database schemas affecting multiple applications

**Exceptions:**
- Internal implementation details not exposed through APIs
- Experimental features clearly marked as unstable
- Emergency security fixes (with expedited communication process)

## Implementation

### Technical Enforcement

API versioning and deprecation management:

```hcl
# terraform/github/breaking_change_detection.tf
resource "github_repository_ruleset" "breaking_change_validation" {
  name        = "Breaking Change Protection"
  repository  = github_repository.api_service.name
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
        { context = "api/breaking-change-detection" },
        { context = "api/backward-compatibility" },
        { context = "api/deprecation-notice" }
      ]
    }

    # Require specific PR labels for breaking changes
    required_linear_history = true
  }

  labels = {
    "nash.group/policy"    = "dep-001"
    "nash.group/component" = "api-management"
    "nash.group/team"      = var.team_name
  }
}

# Monitoring for deprecated API usage
resource "monitoring_alert" "deprecated_api_usage" {
  name        = "Deprecated API Usage"
  description = "Deprecated API endpoints are still being used"

  labels = {
    "nash.group/policy"   = "dep-001"
    "nash.group/service"  = var.service_name
    "nash.group/severity" = "warning"
  }

  annotations = {
    summary     = "Deprecated API usage detected for ${var.service_name}"
    description = "{{ $value }} requests to deprecated endpoints in the last hour"
    runbook_url = "https://runbooks.nash.group/deprecated-api-usage"
  }

  query = <<-EOT
    sum(rate(http_requests_total{deprecated="true"}[1h])) > 0
  EOT

  for_duration = "5m"
}
```

Automated breaking change detection:

```yaml
# .github/workflows/breaking-change-detection.yml
name: Breaking Change Detection
on:
  pull_request:
    branches: [main]
    paths: ['api/**', 'schema/**', 'openapi.yaml']

jobs:
  detect-breaking-changes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Tools
        run: |
          npm install -g @apidevtools/swagger-diff
          npm install -g oasdiff

      - name: Check OpenAPI Breaking Changes
        if: hashFiles('openapi.yaml') != ''
        run: |
          # Get the OpenAPI spec from main branch
          git show main:openapi.yaml > openapi-main.yaml || exit 0

          # Compare current spec with main
          if [ -f openapi-main.yaml ]; then
            echo "Checking for breaking changes..."
            oasdiff breaking openapi-main.yaml openapi.yaml --format json > breaking-changes.json

            # Check if breaking changes found
            if [ -s breaking-changes.json ] && [ "$(cat breaking-changes.json)" != "[]" ]; then
              echo "Breaking changes detected:"
              cat breaking-changes.json | jq '.'

              # Check if PR has breaking-change label
              gh pr view ${{ github.event.number }} --json labels --jq '.labels[].name' | grep -q "breaking-change" || {
                echo "Breaking changes detected but PR not labeled as 'breaking-change'"
                echo "Please add the 'breaking-change' label and ensure proper deprecation process"
                exit 1
              }

              # Validate deprecation notice
              echo "Validating deprecation notice..."
              ./scripts/validate-deprecation-notice.sh
            fi
          fi
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Validate Migration Guide
        if: contains(github.event.pull_request.labels.*.name, 'breaking-change')
        run: |
          # Check for migration guide
          test -f "docs/migrations/$(date +%Y-%m-%d)-migration.md" || {
            echo "Breaking change PR must include migration guide"
            echo "Create docs/migrations/$(date +%Y-%m-%d)-migration.md"
            exit 1
          }

          # Validate migration guide format
          ./scripts/validate-migration-guide.sh "docs/migrations/$(date +%Y-%m-%d)-migration.md"

      - name: Check Backward Compatibility
        run: |
          # Run backward compatibility tests if they exist
          if [ -f "test/backward-compatibility.test.js" ]; then
            npm test -- test/backward-compatibility.test.js
          fi

          # Check for deprecated endpoint monitoring
          if grep -q "deprecated.*true" api/ || grep -q "deprecated.*true" openapi.yaml; then
            echo "Validating deprecated endpoint monitoring..."
            grep -q "deprecated.*true" monitoring/alerts.yaml || {
              echo "Deprecated endpoints must have monitoring alerts"
              exit 1
            }
          fi
```

### Automated Validation

**Breaking Change Detection:**
- Automated OpenAPI schema comparison for REST APIs
- GraphQL schema evolution validation
- Database schema migration analysis
- Contract testing for backward compatibility

**Deprecation Process Automation:**
```bash
#!/bin/bash
# scripts/deprecate-endpoint.sh
# Automates the endpoint deprecation process

set -euo pipefail

ENDPOINT_PATH="${1:-}"
DEPRECATION_DATE="${2:-$(date +%Y-%m-%d)}"
REMOVAL_DATE="${3:-$(date -d '+6 months' +%Y-%m-%d)}"

if [ -z "$ENDPOINT_PATH" ]; then
    echo "Usage: $0 <endpoint-path> [deprecation-date] [removal-date]"
    echo "Example: $0 /api/v1/users 2024-09-30 2025-03-30"
    exit 1
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

# Update OpenAPI specification
update_openapi_spec() {
    log "Updating OpenAPI specification for $ENDPOINT_PATH"

    # Add deprecation markers to OpenAPI spec
    python3 - <<EOF
import yaml
import sys

with open('openapi.yaml', 'r') as f:
    spec = yaml.safe_load(f)

# Add deprecation information
for path, methods in spec.get('paths', {}).items():
    if path == '$ENDPOINT_PATH':
        for method, definition in methods.items():
            if isinstance(definition, dict):
                definition['deprecated'] = True
                definition['description'] = f"{definition.get('description', '')}\\n\\n**DEPRECATED**: This endpoint is deprecated as of $DEPRECATION_DATE and will be removed on $REMOVAL_DATE. See migration guide."

                # Add deprecation headers
                if 'responses' in definition:
                    for response in definition['responses'].values():
                        if 'headers' not in response:
                            response['headers'] = {}
                        response['headers']['X-API-Deprecation'] = {
                            'description': 'Deprecation notice',
                            'schema': {'type': 'string'},
                            'example': 'Deprecated as of $DEPRECATION_DATE, removal on $REMOVAL_DATE'
                        }

with open('openapi.yaml', 'w') as f:
    yaml.dump(spec, f, default_flow_style=False)
EOF
}

# Add monitoring for deprecated endpoint
add_monitoring() {
    log "Adding monitoring for deprecated endpoint usage"

    cat >> monitoring/deprecated-endpoints.yaml <<EOF
- alert: DeprecatedEndpointUsage_$(echo $ENDPOINT_PATH | tr '/' '_')
  expr: |
    sum(rate(http_requests_total{path="$ENDPOINT_PATH"}[1h])) > 0
  for: 1h
  labels:
    severity: warning
    deprecated_endpoint: "$ENDPOINT_PATH"
    deprecation_date: "$DEPRECATION_DATE"
    removal_date: "$REMOVAL_DATE"
  annotations:
    summary: "Usage detected for deprecated endpoint $ENDPOINT_PATH"
    description: "{{ \$value }} requests to deprecated endpoint $ENDPOINT_PATH in the last hour"
    migration_guide: "https://docs.nash.group/migrations/$DEPRECATION_DATE"
EOF
}

# Create migration guide template
create_migration_guide() {
    log "Creating migration guide template"

    mkdir -p docs/migrations
    cat > "docs/migrations/$DEPRECATION_DATE-migration.md" <<EOF
# Migration Guide: $ENDPOINT_PATH Deprecation

**Deprecation Date:** $DEPRECATION_DATE
**Removal Date:** $REMOVAL_DATE
**Affected Endpoint:** \`$ENDPOINT_PATH\`

## Overview

This endpoint is being deprecated and will be removed on $REMOVAL_DATE.

## Migration Path

### Recommended Approach
[Describe the recommended replacement endpoint or approach]

### Example Migration
\`\`\`javascript
// Old approach (deprecated)
const response = await fetch('$ENDPOINT_PATH');

// New approach
const response = await fetch('/api/v2/new-endpoint');
\`\`\`

## Breaking Changes
- [List specific breaking changes]
- [Include impact analysis]

## Timeline
- **$DEPRECATION_DATE**: Endpoint marked as deprecated
- **$(date -d "$DEPRECATION_DATE + 3 months" +%Y-%m-%d)**: Support notifications begin
- **$REMOVAL_DATE**: Endpoint removed

## Support
For questions or assistance with migration:
- **Documentation**: [API Documentation](../api-reference.md)
- **Team Contact**: [team-email@nash.group](mailto:team-email@nash.group)
- **GitHub Issues**: [Create an issue](https://github.com/the-nash-group/service-name/issues/new)
EOF
}

# Add deprecation headers to application code
add_deprecation_headers() {
    log "Adding deprecation headers to application response"

    cat >> src/middleware/deprecation.js <<EOF
// Deprecation middleware for $ENDPOINT_PATH
app.use('$ENDPOINT_PATH', (req, res, next) => {
    res.set({
        'X-API-Deprecation': 'Deprecated as of $DEPRECATION_DATE, removal on $REMOVAL_DATE',
        'X-API-Migration-Guide': 'https://docs.nash.group/migrations/$DEPRECATION_DATE',
        'X-API-Sunset': '$REMOVAL_DATE'
    });

    // Log usage for monitoring
    console.log({
        message: 'Deprecated endpoint accessed',
        endpoint: '$ENDPOINT_PATH',
        user_agent: req.get('User-Agent'),
        ip: req.ip,
        timestamp: new Date().toISOString(),
        deprecation_date: '$DEPRECATION_DATE',
        removal_date: '$REMOVAL_DATE'
    });

    next();
});
EOF
}

# Main execution
main() {
    log "Starting deprecation process for $ENDPOINT_PATH"

    update_openapi_spec
    add_monitoring
    create_migration_guide
    add_deprecation_headers

    log "Deprecation process completed"
    log "Next steps:"
    log "1. Review and customize the migration guide in docs/migrations/$DEPRECATION_DATE-migration.md"
    log "2. Test the deprecation headers and monitoring"
    log "3. Communicate the deprecation to affected teams"
    log "4. Create calendar reminders for removal date"
}

main "$@"
```

### Human Process

1. **Breaking Change Review**: All breaking changes require architecture review before implementation
2. **Deprecation Planning**: 6-month minimum notice period for public APIs, 3-month for internal APIs
3. **Migration Support**: Dedicated support during migration period with office hours
4. **Communication Strategy**: Multi-channel announcement including email, Slack, and documentation
5. **Removal Verification**: Confirmation that no active usage remains before final removal

## Breaking Change Categories

### API Changes

**High-Impact Breaking Changes:**
- Removing endpoints or operations
- Changing required parameters or response schemas
- Modifying authentication or authorization requirements
- Altering error response formats

**Medium-Impact Breaking Changes:**
- Adding required fields to request bodies
- Changing default values for optional parameters
- Modifying HTTP status codes for specific scenarios
- Updating rate limiting policies

**Low-Impact Breaking Changes:**
- Adding optional parameters
- Adding new response fields
- Introducing new optional headers
- Expanding enum values

### Database Schema Changes

**Schema Migration Template:**
```sql
-- Migration: Add user preferences column
-- Date: 2024-09-30
-- Breaking Change: Yes (requires application update)
-- Rollback: migration_20240930_rollback.sql

BEGIN;

-- Step 1: Add new column as nullable (backward compatible)
ALTER TABLE users
ADD COLUMN preferences JSONB DEFAULT '{}';

-- Step 2: Populate default values for existing users
UPDATE users
SET preferences = '{"theme": "light", "notifications": true}'
WHERE preferences IS NULL;

-- Step 3: Add not-null constraint (breaking change point)
-- This step will be executed in a separate migration
-- after application code is updated to handle the new column

COMMIT;
```

**Rollback Procedure:**
```sql
-- Rollback migration: Remove user preferences column
-- Date: 2024-09-30

BEGIN;

-- Remove the column (this will lose data)
ALTER TABLE users DROP COLUMN IF EXISTS preferences;

COMMIT;
```

### Configuration Changes

**Configuration Evolution Example:**
```yaml
# config/v1/service.yaml (deprecated)
database:
  host: localhost
  port: 5432
  username: service_user
  password: secret

# config/v2/service.yaml (current)
database:
  connection_string: postgresql://service_user:secret@localhost:5432/service_db
  pool_size: 10
  timeout: 30s

# Migration support: Accept both formats during transition
migration:
  accept_legacy_config: true
  legacy_deprecation_date: "2024-12-31"
```

## Deprecation and Migration Standards

### Communication Timeline

**6 Months Before Removal:**
- Initial deprecation announcement
- Migration guide published
- Deprecated endpoints marked in documentation
- Monitoring for usage patterns established

**3 Months Before Removal:**
- Direct outreach to teams with high usage
- Office hours scheduled for migration support
- Automated notifications to API consumers

**1 Month Before Removal:**
- Final migration reminder
- Escalation to team leads for remaining usage
- Preparation for removal deployment

**Removal Day:**
- Staged removal with monitoring
- Immediate rollback capability maintained
- Post-removal validation and cleanup

### Migration Guide Standards

**Required Sections:**
```markdown
# Migration Guide: [Change Description]

## Overview
Brief description of what's changing and why.

## Timeline
- **Deprecation Date**: When the change was announced
- **Migration Period**: Time available for migration
- **Removal Date**: When the old functionality will be removed

## What's Changing
Detailed breakdown of specific changes.

## Migration Steps
Step-by-step instructions for updating to new approach.

### Code Examples
Before and after code examples showing the migration.

## Compatibility Notes
Information about backward compatibility during transition.

## Testing
How to test the migration in development and staging.

## Rollback Plan
How to revert if issues are discovered.

## Support
Contact information and resources for help.
```

### Semantic Versioning

**Version Number Strategy:**
- **Major Version**: Breaking changes requiring user action
- **Minor Version**: New features with backward compatibility
- **Patch Version**: Bug fixes and internal improvements

**Pre-release Versioning:**
```json
{
  "version": "2.0.0-beta.1",
  "deprecation_notice": "v1.x will be supported until 2025-03-30",
  "migration_guide": "https://docs.nash.group/migrations/v2.0.0"
}
```

## Backward Compatibility Testing

### Automated Testing Strategy

**Contract Testing:**
```javascript
// test/backward-compatibility.test.js
const { matchers } = require('@pact-foundation/pact');

describe('Backward Compatibility', () => {
  test('v1 API contracts still valid', async () => {
    const response = await request(app)
      .get('/api/v1/users')
      .set('Accept', 'application/json');

    expect(response.status).toBe(200);
    expect(response.body).toMatchObject({
      data: expect.arrayContaining([
        expect.objectContaining({
          id: expect.any(String),
          email: expect.any(String),
          name: expect.any(String)
        })
      ])
    });
  });

  test('deprecated endpoints return proper headers', async () => {
    const response = await request(app)
      .get('/api/v1/deprecated-endpoint');

    expect(response.headers).toHaveProperty('x-api-deprecation');
    expect(response.headers).toHaveProperty('x-api-sunset');
    expect(response.headers).toHaveProperty('x-api-migration-guide');
  });
});
```

**Integration Testing:**
```yaml
# test/compatibility/docker-compose.yml
version: '3.8'
services:
  api-v1:
    build:
      context: .
      dockerfile: Dockerfile.v1
    ports:
      - "3001:3000"

  api-v2:
    build:
      context: .
      dockerfile: Dockerfile.v2
    ports:
      - "3002:3000"

  compatibility-tests:
    build:
      context: .
      dockerfile: Dockerfile.test
    depends_on:
      - api-v1
      - api-v2
    command: npm run test:compatibility
```

## Compliance Verification

**Automated Checks:**
- Daily scan for deprecated API usage patterns
- Weekly validation of migration guide completeness
- Monthly review of breaking change implementation status
- Quarterly assessment of deprecation timeline adherence

**Manual Audits:**
- Monthly review of pending breaking changes and migration progress
- Quarterly evaluation of breaking change impact on downstream systems
- Annual assessment of breaking change policy effectiveness

**Reporting:**
- Real-time dashboard of deprecated API usage
- Weekly breaking change implementation status reports
- Monthly migration progress tracking
- Quarterly breaking change policy compliance metrics

## Emergency Breaking Changes

### Security-Related Breaking Changes

**Expedited Process:**
1. **Immediate Assessment**: Security team evaluates severity and scope
2. **Risk vs. Impact**: Balance security risk against breaking change impact
3. **Accelerated Timeline**: Reduced notice period with intensive communication
4. **Emergency Support**: Dedicated support team during emergency migration

**Example Security Breaking Change:**
```markdown
# SECURITY ADVISORY: Emergency API Key Format Change

**Severity**: Critical
**Timeline**: 72-hour migration window
**Reason**: Active exploitation of predictable API key format

## Immediate Actions Required
1. Generate new API keys using updated format
2. Update applications to use new keys
3. Revoke old API keys by 2024-10-03 23:59 UTC

## Emergency Support
- **Slack**: #security-emergency-support
- **Email**: security-emergency@nash.group
- **Phone**: +1-555-EMERGENCY (24/7)
```

### Rollback Procedures

**Breaking Change Rollback Plan:**
```yaml
# rollback-plan.yml
rollback_triggers:
  - error_rate_increase: ">5%"
  - customer_complaints: ">10 in 1 hour"
  - critical_system_failure: true

rollback_steps:
  1. immediate_stop: "Stop deployment of breaking change"
  2. restore_previous: "Restore previous API version"
  3. communicate: "Notify affected teams of rollback"
  4. investigate: "Root cause analysis of failure"
  5. reschedule: "Plan revised breaking change approach"

rollback_automation:
  enabled: true
  auto_rollback_conditions:
    - "error_rate > 10% for 5 minutes"
    - "availability < 99% for 10 minutes"
```

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 14: Progress Without Breakage](../the-covenant/PRINCIPLES.md#principle-14-progress-without-breakage)
- **Governance Authority:** [GOVERNANCE.md - API Evolution Standards](../the-covenant/GOVERNANCE.md#stronghold-decisions-individual-repositories)
- **Implementation:** API versioning, deprecation automation, migration tooling
- **Development Standards:** [SC-003 Trunk-Based Development](./sc-003-trunk-based-development.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 14: Progress Without Breakage
