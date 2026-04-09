# The Nash Group - Organizational Specification
*Version 1.0.0 - The Meta-Infrastructure*

> "Before we build the eternal, we must define what eternal means."

## Purpose

This document defines the **formal organizational structure** of The Nash Group. It establishes:
- Directory structures and file organization
- Naming conventions for repositories, files, and directories
- Schema standards and validation requirements
- Template systems and repository patterns
- Lifecycle management and governance

This is the **meta-layer** that enables consistent, scalable infrastructure across all Nash Group repositories.

## Core Principles

1. **Consistency Over Creativity** - Every repository follows the same structure
2. **Validation Over Trust** - All conventions are automatically enforced
3. **Templates Over Memory** - New repositories start from blessed patterns
4. **Schemas Over Documentation** - Formal validation trumps written rules
5. **Evolution Through Process** - Changes require deliberation and approval

## The Four-Pillar Architecture

**Established**: 2025-10-30 per ADR-001
**Updated**: 2025-10-30 (Specification Governance added)
**Status**: Official organizational architecture

The Nash Group follows a four-layer architecture with three repository pillars and one cross-cutting governance layer:

```
┌────────────────────┐
│  THE COVENANT      │ ← Level 1: Why We Build (Philosophy)
│  (Philosophy)      │   • PRINCIPLES.md (16 core principles)
└────────────────────┘   • GOVERNANCE.md (decision authority)
         ↓                • HUMAN_MANDATE.md (5 Guardian roles)
         ↓                • policies/ (policy specifications)
┌────────────────────┐
│  SPECIFICATIONS    │ ← Level 2: Standards & Governance (Cross-cutting)
│  (.org/specs/)     │   • API Standards (OpenAPI 3.1.0)
└────────────────────┘   • Service Standards (health checks, metrics)
         ↓                • Data Standards (JSON Schema 2020-12)
         ↓                • Enforcement Policies (OPA)
┌────────────────────┐
│  THE CITADEL       │ ← Level 3a: How We Build (Infrastructure)
│  (Infrastructure)  │   • Terraform IaC
└────────────────────┘   • GitHub/Cloudflare management
         ↓                • Zero-trust OIDC
         ↓                • State in HCP Terraform
┌────────────────────┐
│  THE NEXUS         │ ← Level 3b: What We Build (Operations)
│  (Operations)      │   • Observability Bridge
└────────────────────┘   • MCP servers
                         • Runtime policies (the-nexus/policy/*.rego)
                         • Dashboard and tooling
```

### Core Repository Purposes

| Repository | Purpose | Governance Level | Contains |
|------------|---------|------------------|----------|
| **the-covenant** | Philosophy & policy specifications | Covenant (2 Watchers + 2 Mentors, 72h debate) | PRINCIPLES.md, GOVERNANCE.md, policies/ |
| **the-citadel** | Infrastructure as Code | Citadel (1 Mentor + 1 Watcher) | Terraform, GitHub/Cloudflare config |
| **the-nexus** | Operational tooling | Stronghold (1 Mentor) | Apps, services, runtime policies |
| **the-shield** | Identity & Access Management | Citadel (1 Mentor + 1 Watcher) | IAM system, identities, OPA policies (planned) |

### Semantic Meaning

- **the-covenant** = "Why we build" (Level 1) - Establishes principles and governance
- **specifications** = "Standards & governance" (Level 2) - Bridges philosophy and implementation
- **the-citadel** = "How we build" (Level 3a) - Enforces principles through infrastructure
- **the-shield** = "Security foundation" (Cross-cutting) - Identity, authentication, authorization, audit
- **the-nexus** = "What we build" (Level 3b) - Operational tools and services

All other repositories follow standard naming conventions (see below).

### Specification Governance

**Location**: `.org/specs/` (cross-cutting layer)
**Status**: MANDATORY as of 2025-10-30
**Governance**: Covenant Level (2 Watchers + 2 Mentors)

Specifications provide the **fourth conceptual pillar** that bridges philosophy and implementation:

**Core Specifications**:
1. **API Standards** - All APIs must have OpenAPI 3.1.0 specifications
2. **Service Standards** - All services must implement health checks and metrics
3. **Data Standards** - All data models must have JSON Schema 2020-12
4. **Event Standards** - All events should follow CloudEvents 1.0

**See**: `.org/SPECIFICATIONS.md` for complete governance framework

### Identity & Access Management (IAM)

**Location**: `.org/iam/` (cross-cutting security layer)
**Status**: MANDATORY as of 2025-10-30
**Governance**: Covenant Level (2 Watchers + 2 Mentors)
**Implementation Repository**: `the-shield` (planned)

IAM provides the **security foundation** across all pillars, managing identities, authentication, authorization, and audit for:

**Identity Types**:
1. **Human Identities** - Family members, collaborators (WebAuthn + TOTP)
2. **AI Agent Identities** - Orchestrators, specialists (API keys + JWT, 90-day rotation)
3. **Service Identities** - Infrastructure, applications (mTLS certificates, OIDC)
4. **Device Identities** - Workstations, mobile, IoT (device certificates)

**Multi-Tenant Architecture**:
- **personal** - Personal infrastructure and projects
- **family** - Shared family resources with parental controls
- **university** - Academic research with compliance
- **ai-lab** - AI agent playground with governance

**Authorization Model**: RBAC + ABAC Hybrid with OPA policy-as-code

**Five Layers**:
1. Identity (who/what is requesting?)
2. Authentication (prove your identity)
3. Authorization (what are you allowed?)
4. Enforcement (apply at every access point)
5. Audit (complete immutable trail)

**See**: `.org/IAM-FRAMEWORK.md` for complete IAM governance framework

## Repository Naming Standards

### Repository Names

All repositories **MUST** follow kebab-case naming:

```
✅ VALID                    ❌ INVALID
the-covenant               TheCovenent
citadel-config            CitadelConfig
service-user-auth         service_user_auth
holy-ground               Holy-Ground
the-chronicles            the_chronicles
```

### Repository Prefixes

Repositories **SHOULD** use semantic prefixes:

| Prefix | Purpose | Example |
|--------|---------|---------|
| `service-` | Microservices | `service-user-auth` |
| `lib-` | Libraries | `lib-common-utils` |
| `app-` | Applications | `app-dashboard` |
| `infra-` | Infrastructure | `infra-terraform-modules` |
| `docs-` | Documentation | `docs-api-reference` |
| `tool-` | Tooling | `tool-deployment-cli` |

Special repositories may omit prefixes (the three pillars):
- `the-covenant` (philosophy & governance)
- `the-citadel` (infrastructure as code)
- `nexus` (operational tooling)

Planned special repositories:
- `the-chronicles` (service catalog - future)
- `holy-ground` (secrets management - if needed)

## Directory Structure Standards

### Required Root Files

Every repository **MUST** contain:

```
repository/
├── README.md              # Required: Repository overview
├── CONTRIBUTING.md        # Required: Contribution guidelines
├── LICENSE                # Required: License file
├── CHANGELOG.md           # Required: Change history
├── .gitignore            # Required: Git ignore rules
├── .editorconfig         # Required: Editor configuration
└── CLAUDE.md             # Required: AI assistant context
```

### Standard Directory Structure

```
repository/
├── src/                  # Source code (if applicable)
├── docs/                 # Documentation
│   ├── architecture/    # Architecture Decision Records
│   ├── api/             # API documentation
│   └── guides/          # User guides
├── tests/               # Test files
├── scripts/             # Build and utility scripts
├── config/              # Configuration files
├── .github/             # GitHub configuration
│   ├── workflows/       # GitHub Actions
│   ├── ISSUE_TEMPLATE/  # Issue templates
│   └── pull_request_template.md
└── .devcontainer/       # Development container config
```

### Language-Specific Conventions

**TypeScript/JavaScript:**
```
src/
├── index.ts
├── types/
├── utils/
├── services/
└── components/
```

**Python:**
```
src/
├── __init__.py
├── core/
├── models/
├── services/
└── utils/
```

**Go:**
```
cmd/
├── api/
└── cli/
pkg/
├── models/
└── services/
```

## File Naming Standards

### General Rules

1. **Use kebab-case** for all files except where language conventions dictate otherwise
2. **Be descriptive** - `user-authentication-service.ts` not `auth.ts`
3. **Include file purpose** - `deploy-production.sh` not `deploy.sh`

### Naming by File Type

| Type | Convention | Example |
|------|------------|---------|
| Documentation | UPPERCASE.md | `README.md`, `CONTRIBUTING.md` |
| Config | kebab-case.{ext} | `docker-compose.yml` |
| Scripts | kebab-case.sh | `run-tests.sh` |
| Source (TS/JS) | kebab-case.ts | `user-service.ts` |
| Source (Python) | snake_case.py | `user_service.py` |
| Source (Go) | snake_case.go | `user_service.go` |
| Tests | {name}.test.{ext} | `user-service.test.ts` |

### Special Files

These files **MUST** use exact names:

```
README.md              # Not readme.md or Readme.md
CHANGELOG.md          # Not CHANGES.md
LICENSE               # Not LICENSE.md or LICENSE.txt
Dockerfile            # Not dockerfile
Makefile             # Not makefile
.gitignore           # Not gitignore
.env.example         # Not .env.sample
CLAUDE.md            # Not AI.md or ASSISTANT.md
```

## Schema Standards

### Adopted Standards

The Nash Group adopts these schema standards:

1. **JSON Schema Draft 2020-12** for configuration validation
2. **OpenAPI 3.1.0** for API specifications
3. **CUE v0.10.0** for complex configuration schemas
4. **AsyncAPI 2.6.0** for event-driven architectures

### Schema Organization

```
schemas/
├── json-schema/
│   ├── service-config-v1.json
│   └── deployment-v1.json
├── openapi/
│   ├── user-api-v1.yaml
│   └── admin-api-v1.yaml
├── cue/
│   ├── tenant.cue
│   └── service.cue
└── asyncapi/
    └── events-v1.yaml
```

### Version Strategy

- **Major versions** in filename: `user-api-v1.yaml`, `user-api-v2.yaml`
- **Minor versions** in schema: `version: "1.2.3"`
- **Breaking changes** require new major version file

## Template System

### Repository Templates

Located in `.org/templates/repositories/`:

```
templates/repositories/
├── typescript-service/
│   ├── template.yaml      # Template metadata
│   ├── cookiecutter.json  # Variable definitions
│   └── {{cookiecutter.repo_name}}/
│       ├── README.md
│       ├── package.json
│       └── src/
├── python-service/
├── go-service/
└── infrastructure/
```

### File Templates

Located in `.org/templates/files/`:

```
templates/files/
├── README.md.tmpl
├── CONTRIBUTING.md.tmpl
├── CHANGELOG.md.tmpl
├── CLAUDE.md.tmpl
├── Dockerfile.tmpl
└── docker-compose.yml.tmpl
```

### Template Variables

Standard variables available in all templates:

```yaml
organization:
  name: "The Nash Group"
  github: "the-nash-group"
  domain: "thenash.group"

repository:
  name: "{{cookiecutter.repo_name}}"
  description: "{{cookiecutter.description}}"
  owner: "{{cookiecutter.team}}"

author:
  name: "{{cookiecutter.author_name}}"
  email: "{{cookiecutter.author_email}}"

dates:
  created: "{{cookiecutter.created_date}}"
  modified: "{{cookiecutter.modified_date}}"
```

## Architecture Decision Records

### ADR Format

All ADRs **MUST** follow this structure:

```markdown
# ADR-NNN: Title

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
What is the issue we're seeing that motivates this decision?

## Decision
What is the change that we're proposing/doing?

## Consequences
What becomes easier or harder because of this decision?

## References
- Link to relevant documents
- Link to discussions
```

### ADR Naming

- Format: `NNN-descriptive-name.md`
- Example: `001-adopt-terraform.md`
- Always use 3-digit numbers with leading zeros

### ADR Location

```
docs/architecture/
├── 001-adopt-terraform.md
├── 002-multi-tenant-architecture.md
├── 003-event-driven-design.md
└── template.md
```

## Validation Framework

### Pre-commit Hooks

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-naming
        name: Validate naming conventions
        entry: .org/tooling/validators/validate-naming.sh
        language: script
        pass_filenames: true

      - id: validate-structure
        name: Validate repository structure
        entry: .org/tooling/validators/validate-repo-structure.sh
        language: script
        pass_filenames: false
```

### CI/CD Validation

GitHub Actions workflow:

```yaml
name: Validate Organization Standards

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Naming
        run: .org/tooling/validators/validate-naming.sh

      - name: Validate Structure
        run: .org/tooling/validators/validate-repo-structure.sh

      - name: Validate Schemas
        run: .org/tooling/validators/validate-schemas.sh
```

### Validation Scripts

Located in `.org/tooling/validators/`:

```
validators/
├── validate-naming.sh          # Check file/directory names
├── validate-repo-structure.sh  # Check required files/dirs
├── validate-schemas.sh         # Validate against schemas
├── validate-dependencies.sh    # Check dependency rules
└── check-secrets.sh           # Scan for secrets
```

## Repository Lifecycle

### Creation

1. Use template: `trinity create repo --template [type] --name [name]`
2. Template generates compliant structure
3. Pre-commit hooks installed automatically
4. CI/CD workflows configured
5. Initial ADR created (`001-repository-creation.md`)

### Evolution

1. Changes follow The Covenant governance process
2. ADRs document significant decisions
3. CHANGELOG.md updated with each release
4. Schemas versioned appropriately

### Deprecation

1. ADR documents deprecation decision
2. README updated with deprecation notice
3. Repository archived after grace period
4. References updated in dependent repos

### Deletion

1. Requires two-key approval (two Watchers)
2. Final backup created
3. Repository deleted
4. Deletion logged in organization audit

## The .org Directory

The `.org/` directory is the organizational control center:

```
.org/
├── SPECIFICATIONS.md         # Specification governance entry point (Level 2)
├── ORGANIZATION-SPEC.md      # This document (organizational standards)
├── specs/                    # Specification governance framework
│   ├── active/              # Current enforced specifications
│   │   ├── specification-governance-framework.md
│   │   └── specification-quick-start.md
│   ├── draft/               # Proposed specifications
│   └── archived/            # Historical specifications
├── contracts/                # Specification implementations
│   ├── api/                 # OpenAPI specifications
│   ├── event/               # AsyncAPI specifications
│   └── data/                # JSON Schema definitions
├── policies/                 # OPA enforcement policies
│   ├── governance/          # Specification compliance policies
│   ├── security/            # Security validation policies
│   └── operational/         # Runtime enforcement policies
├── schemas/                  # Legacy validation schemas (deprecated)
│   ├── json-schema/         # Migrate to .org/contracts/data/
│   ├── openapi/             # Migrate to .org/contracts/api/
│   └── cue/
├── templates/                # Repository and file templates
│   ├── repositories/
│   └── files/
├── tooling/                  # Automation and validation
│   ├── validators/
│   ├── generators/
│   └── auditors/
└── docs/                     # Meta-documentation
    ├── guides/
    └── decisions/
```

**Note**: The `schemas/` directory is deprecated in favor of the new `contracts/` structure. Migrate existing schemas during the next quarterly review.

## Compliance and Auditing

### Automated Compliance Checks

Run nightly via GitHub Actions:

1. Repository structure validation
2. Naming convention checks
3. Required file presence
4. Schema compliance
5. Security scanning

### Quarterly Audits

Manual review every quarter:

1. ADR completeness
2. Documentation currency
3. Dependency updates
4. Security posture
5. Organizational drift

### Non-Compliance Protocol

1. **Warning** - Automated notification to repository owner
2. **Grace Period** - 30 days to remediate
3. **Escalation** - Issue raised to Watchers
4. **Enforcement** - Repository marked non-compliant
5. **Remediation** - Assisted migration to compliance

## Migration Strategy

### For Existing Repositories

1. Run audit: `.org/tooling/auditors/audit-repo.sh [repo-name]`
2. Generate report of non-compliance
3. Create migration plan
4. Apply fixes incrementally
5. Add validation hooks
6. Mark as compliant

### Migration Tools

```bash
# Audit existing repository
.org/tooling/auditors/audit-repo.sh [repo]

# Generate migration plan
.org/tooling/generators/create-migration-plan.sh [repo]

# Apply automated fixes
.org/tooling/migrators/auto-fix.sh [repo]

# Validate compliance
.org/tooling/validators/validate-compliance.sh [repo]
```

## Evolution of This Specification

This specification evolves through:

1. **Proposal** - Issue or PR in the-covenant
2. **Discussion** - Community feedback period (minimum 1 week)
3. **Approval** - Requires 2 Watchers + 2 Mentors
4. **Implementation** - Update tooling and templates
5. **Migration** - Gradual rollout with grace period

Version history maintained in `CHANGELOG-SPEC.md`.

## Quick Reference

### Essential Commands

```bash
# Create new repository from template
trinity create repo --template typescript-service --name my-service

# Validate current repository
.org/tooling/validators/validate-repo.sh .

# Generate migration plan
.org/tooling/generators/create-migration-plan.sh .

# Create new ADR
.org/tooling/generators/create-adr.sh "Adopt New Pattern"

# Audit all repositories
.org/tooling/auditors/audit-all.sh
```

### File Naming Cheat Sheet

```
✅ user-service.ts          ❌ userService.ts
✅ deploy-production.sh     ❌ deployProd.sh
✅ docker-compose.yml       ❌ docker_compose.yaml
✅ README.md               ❌ readme.md
✅ user_service.py         ❌ user-service.py (Python)
```

### Required Files Checklist

- [ ] README.md
- [ ] CONTRIBUTING.md
- [ ] LICENSE
- [ ] CHANGELOG.md
- [ ] .gitignore
- [ ] .editorconfig
- [ ] CLAUDE.md
- [ ] docs/architecture/

---

*"Standards are not limitations - they are the foundation of infinite creativity within defined boundaries."*

**Implementation**: [`.org/`](./.org/) - Tooling and templates
**Philosophy**: [`the-covenant`](./the-covenant/) - Why these standards exist
**Enforcement**: [`citadel-config`](./citadel-config/) - Technical implementation
