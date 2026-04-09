# DOC-001: Documentation Requirements

**Policy ID:** DOC-001
**Category:** Documentation
**Effective Date:** 2024-09-30
**Last Updated:** 2024-09-30

## Statement

Every repository **must** have a README. Every API **must** have schemas. Every decision **must** have an ADR (Architecture Decision Record). "The code is self-documenting" is a lie told by those who remember what they wrote.

## Rationale

"The code is self-documenting" is a lie told by those who remember what they wrote. Six months later, even the author needs documentation:

- **Knowledge Loss**: Tribal knowledge disappears when team members leave
- **Onboarding Friction**: New team members spend weeks understanding undocumented systems
- **Decision Context**: Why decisions were made is lost without documentation
- **API Integration**: External teams cannot integrate without clear API documentation
- **Maintenance Burden**: Undocumented code is harder to modify and debug
- **Compliance Requirements**: Regulatory and audit requirements need documented processes

Comprehensive documentation enables knowledge transfer, reduces onboarding time, and preserves decision context for future team members.

## Scope

**Applies To:**
- All repositories owned by The Nash Group organization
- All APIs (REST, GraphQL, gRPC) exposed internally or externally
- All significant technical decisions affecting architecture or implementation
- All operational procedures and deployment processes
- All database schemas and data models

**Exceptions:**
- Temporary experimental repositories (marked with `experimental` topic)
- Forked repositories where we don't control the documentation standards

## Implementation

### Technical Enforcement

Repository template enforcement through GitHub:

```hcl
# terraform/github/repository_templates.tf
resource "github_repository" "template_service" {
  name         = "template-service"
  description  = "Standard service template with required documentation"
  is_template  = true

  # Required files enforced by template
  template {
    owner      = "the-nash-group"
    repository = "template-service"
  }

  # Branch protection requires documentation updates
  # Defined in rulesets.tf
}

resource "github_repository_ruleset" "documentation_requirements" {
  name        = "Documentation Standards"
  repository  = github_repository.service.name
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
  }

  rules {
    # Require README.md updates for significant changes
    required_status_checks {
      strict_required_status_checks_policy = true
      required_status_checks = [
        { context = "docs/readme-validation" },
        { context = "docs/api-documentation" },
        { context = "docs/changelog-updated" }
      ]
    }
  }

  labels = {
    "nash.group/policy"    = "doc-001"
    "nash.group/component" = "documentation"
    "nash.group/team"      = var.team_name
  }
}
```

Repository structure validation:

```yaml
# .github/workflows/documentation-validation.yml
name: Documentation Validation
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Repository Structure
        run: |
          # Required files
          test -f README.md || { echo "README.md is required"; exit 1; }
          test -f CHANGELOG.md || { echo "CHANGELOG.md is required"; exit 1; }
          test -d docs/ || { echo "docs/ directory is required"; exit 1; }

          # README.md content requirements
          grep -q "# " README.md || { echo "README.md missing main heading"; exit 1; }
          grep -q "## Getting Started" README.md || { echo "README.md missing Getting Started section"; exit 1; }
          grep -q "## API Documentation" README.md || echo "Warning: API services should have API Documentation section"

          # Architecture Decision Records
          if [ -d "docs/decisions" ]; then
            for adr in docs/decisions/*.md; do
              if [ -f "$adr" ]; then
                grep -q "# ADR" "$adr" || { echo "$adr is not a valid ADR format"; exit 1; }
                grep -q "## Status" "$adr" || { echo "$adr missing Status section"; exit 1; }
                grep -q "## Context" "$adr" || { echo "$adr missing Context section"; exit 1; }
                grep -q "## Decision" "$adr" || { echo "$adr missing Decision section"; exit 1; }
              fi
            done
          fi

      - name: Validate API Documentation
        run: |
          # Check for OpenAPI specs if this is an API service
          if grep -q "api" README.md || [ -f "api/" ] || [ -f "openapi.yaml" ] || [ -f "swagger.yaml" ]; then
            # Look for API documentation
            test -f openapi.yaml || test -f swagger.yaml || test -f docs/api.md || {
              echo "API service missing documentation (openapi.yaml, swagger.yaml, or docs/api.md)"
              exit 1
            }

            # Validate OpenAPI spec if present
            if [ -f "openapi.yaml" ]; then
              npx @apidevtools/swagger-parser validate openapi.yaml || exit 1
            fi
            if [ -f "swagger.yaml" ]; then
              npx @apidevtools/swagger-parser validate swagger.yaml || exit 1
            fi
          fi

      - name: Check Documentation Links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: 'yes'
          use-verbose-mode: 'yes'
          config-file: '.github/workflows/markdown-link-check-config.json'

      - name: Validate CHANGELOG
        run: |
          # CHANGELOG.md format validation
          if [ -f "CHANGELOG.md" ]; then
            grep -q "# Changelog" CHANGELOG.md || { echo "CHANGELOG.md missing main heading"; exit 1; }
            grep -q "## \[" CHANGELOG.md || { echo "CHANGELOG.md missing version entries"; exit 1; }
          fi
```

### Automated Validation

**README.md Standards:**
- Must include service description and purpose
- Must include getting started/installation instructions
- Must include API documentation links for services
- Must include contribution guidelines
- Must include license information

**API Documentation Standards:**
- OpenAPI 3.0+ specification for REST APIs
- Schema definitions for all request/response objects
- Example requests and responses
- Error code documentation
- Authentication and authorization requirements

**Architecture Decision Records (ADRs):**
```markdown
# ADR-001: Service Architecture Pattern

## Status
Accepted

## Context
We need to establish a consistent pattern for microservice architecture that balances independence with operational simplicity.

## Decision
We will use the hexagonal architecture pattern with clearly defined ports and adapters, enabling clean separation between business logic and external dependencies.

## Consequences
### Positive
- Clear separation of concerns
- Easier to test business logic in isolation
- Reduced coupling to external systems
- Consistent structure across services

### Negative
- Initial development overhead
- Learning curve for team members
- More complex project structure

## Implementation
- All new services must follow hexagonal architecture
- Existing services will be refactored during major updates
- Template repository will include example implementation

## Related Documents
- [Service Template Repository](https://github.com/the-nash-group/template-service)
- [Architecture Guidelines](../architecture-guidelines.md)
```

### Human Process

1. **Documentation-First Development**: Documentation written before or alongside code, not after
2. **Documentation Reviews**: All documentation changes require peer review
3. **ADR Process**: Significant technical decisions documented within 48 hours of decision
4. **API-First Design**: APIs designed and documented before implementation
5. **Quarterly Documentation Audits**: Regular review of documentation completeness and accuracy

## Documentation Categories

### Repository Documentation

**README.md Template:**
```markdown
# Service Name

Brief description of what this service does and why it exists.

## Getting Started

### Prerequisites
- Node.js 18+
- Docker and Docker Compose
- Access to development environment

### Installation
```bash
git clone https://github.com/the-nash-group/service-name
cd service-name
npm install
```

### Running Locally
```bash
# Start dependencies
docker-compose up -d postgres redis

# Start the service
npm run dev
```

### Running Tests
```bash
npm test
npm run test:integration
```

## Architecture

High-level architecture overview with diagrams where appropriate.

### Key Components
- **API Layer**: REST endpoints and request/response handling
- **Business Logic**: Core service functionality and rules
- **Data Layer**: Database access and data modeling
- **External Integrations**: Third-party service connections

## API Documentation

- **OpenAPI Spec**: [openapi.yaml](./openapi.yaml)
- **Interactive Docs**: [API Explorer](http://localhost:3000/docs)
- **Postman Collection**: [service-name.postman_collection.json](./docs/service-name.postman_collection.json)

## Configuration

### Environment Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Service port | `3000` | No |
| `DATABASE_URL` | PostgreSQL connection | - | Yes |
| `REDIS_URL` | Redis connection | - | Yes |

### Feature Flags
- `FEATURE_NEW_ENDPOINT`: Enable experimental API endpoint

## Deployment

### Production Deployment
Deployed automatically via GitHub Actions on merge to `main`.

### Manual Deployment
```bash
kubectl apply -f k8s/
```

## Monitoring and Observability

- **Metrics**: Prometheus metrics at `/metrics`
- **Health Check**: `/health` and `/ready` endpoints
- **Logging**: Structured JSON logs
- **Tracing**: OpenTelemetry instrumentation

## Development

### Code Standards
- ESLint configuration in `.eslintrc.js`
- Prettier formatting enforced
- Husky pre-commit hooks

### Architecture Decision Records
See [docs/decisions/](./docs/decisions/) for architectural decisions.

## Security

### Authentication
Service uses OAuth 2.0 with JWT tokens.

### Authorization
Role-based access control (RBAC) with the following roles:
- `admin`: Full access
- `user`: Read/write access
- `readonly`: Read-only access

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Update documentation
5. Submit a pull request

## License

MIT License - see [LICENSE](./LICENSE) file.

## Support

- **Documentation**: [Full documentation](./docs/)
- **Issues**: [GitHub Issues](https://github.com/the-nash-group/service-name/issues)
- **Team Contact**: [team-email@nash.group](mailto:team-email@nash.group)
```

### API Documentation Standards

**OpenAPI Specification Example:**
```yaml
openapi: 3.0.3
info:
  title: Service Name API
  description: |
    API for managing service-name resources.

    ## Authentication
    All endpoints require a valid JWT token in the Authorization header:
    ```
    Authorization: Bearer <jwt-token>
    ```

    ## Rate Limiting
    API calls are limited to 1000 requests per hour per authenticated user.

  version: 1.0.0
  contact:
    name: The Nash Group
    email: api-support@nash.group
    url: https://nash.group
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.nash.group/v1
    description: Production server
  - url: https://staging-api.nash.group/v1
    description: Staging server

paths:
  /users:
    get:
      summary: List users
      description: |
        Retrieve a paginated list of users.

        ### Authorization
        Requires `user:read` permission.

        ### Rate Limiting
        This endpoint is limited to 100 requests per minute.

      parameters:
        - name: page
          in: query
          description: Page number (1-based)
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: Number of items per page
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
              examples:
                success:
                  summary: Successful user list
                  value:
                    data:
                      - id: "user_123"
                        email: "user@example.com"
                        name: "John Doe"
                        created_at: "2024-01-15T10:30:00Z"
                    pagination:
                      page: 1
                      limit: 20
                      total: 150
                      has_more: true
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
        - created_at
      properties:
        id:
          type: string
          description: Unique user identifier
          example: "user_123"
        email:
          type: string
          format: email
          description: User's email address
          example: "user@example.com"
        name:
          type: string
          description: User's full name
          example: "John Doe"
        created_at:
          type: string
          format: date-time
          description: User creation timestamp
          example: "2024-01-15T10:30:00Z"

    UserListResponse:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "UNAUTHORIZED"
              message: "Valid authentication required"

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

### Database Documentation

**Schema Documentation Example:**
```sql
-- docs/schema.sql
-- Database schema for service-name
-- Last updated: 2024-09-30

-- Users table
-- Stores user account information
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Indexes
    CONSTRAINT users_email_check CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Add indexes
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_created_at ON users (created_at);

-- Audit table for user changes
CREATE TABLE user_audit (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    action VARCHAR(50) NOT NULL, -- INSERT, UPDATE, DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by UUID REFERENCES users(id),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Documentation Quality Standards

### Content Requirements

**Completeness Checklist:**
- [ ] Clear purpose and scope description
- [ ] Step-by-step setup instructions
- [ ] Complete API reference with examples
- [ ] Configuration options documented
- [ ] Error handling and troubleshooting guide
- [ ] Security considerations covered
- [ ] Performance characteristics documented

**Accuracy Standards:**
- All code examples must be tested and working
- Screenshots and diagrams must be current (updated within 6 months)
- Links must be validated and working
- Version compatibility clearly stated

**Accessibility Requirements:**
- Clear headings and document structure
- Alt text for images and diagrams
- Simple language avoiding unnecessary jargon
- Code examples with explanatory comments

### Maintenance Procedures

**Regular Updates:**
- Documentation reviewed during quarterly team retrospectives
- ADRs updated when decisions are superseded
- API documentation automatically generated from code annotations
- README files updated with each significant feature release

**Quality Assurance:**
- Peer review required for all documentation changes
- Link checking automated in CI/CD pipeline
- Style guide adherence validated automatically
- User feedback collection and response process

## Compliance Verification

**Automated Checks:**
- Weekly validation of all repository README files
- Monthly API documentation completeness audit
- Quarterly link validation across all documentation
- Annual review of ADR currency and relevance

**Manual Audits:**
- Quarterly documentation walk-through with new team members
- Annual documentation effectiveness survey
- Post-incident review of documentation gaps

**Reporting:**
- Monthly documentation compliance dashboard
- Quarterly documentation quality metrics
- Annual documentation ROI analysis (time saved vs. maintenance cost)

## Documentation Tools and Standards

### Approved Tools

**Documentation Platforms:**
- GitHub-flavored Markdown for repository documentation
- OpenAPI 3.0+ for API specifications
- Mermaid diagrams for architecture visualization
- Draw.io for complex system diagrams

**Validation Tools:**
- `markdownlint` for Markdown formatting
- `swagger-codegen` for API documentation validation
- `alex` for inclusive language checking
- `textlint` for writing style consistency

**Integration Requirements:**
- Documentation must render correctly in GitHub
- API documentation must be accessible via service endpoints
- Diagrams must be version-controlled and editable
- Search functionality required for large documentation sets

## Related Documents

- **Source Principle:** [PRINCIPLES.md - Principle 13: Code Without Docs is Incomplete](../the-covenant/PRINCIPLES.md#principle-13-code-without-docs-is-incomplete)
- **Governance Authority:** [GOVERNANCE.md - Development Standards](../the-covenant/GOVERNANCE.md#stronghold-decisions-individual-repositories)
- **Implementation:** Repository templates, documentation tooling, CI/CD validation
- **Development Standards:** [SC-003 Trunk-Based Development](./sc-003-trunk-based-development.md)

## Change History

- **2024-09-30** - Initial creation based on Principle 13: Code Without Docs is Incomplete
