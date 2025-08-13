# The Archivist's Guide
*REFERENCE/index.md*

> "Those who cannot remember the past are condemned to repeat it. Those who document the past empower the future."

## Purpose of the Archives

This directory is not a graveyard but a museum. Here lie the artifacts of our journey—the configurations we've outgrown, the patterns we've abandoned, and the decisions that shaped our current form. Each document tells a story of evolution.

## The Great Migration: From Safe-Settings to Terraform

**Date of Transition**: August 2025  
**Rationale**: Architecture Decision Record [`001-terraform-migration.md`](./decisions/001-terraform-migration.md)

We began with Safe-Settings, a YAML-based GitHub configuration system. It served us well, teaching us the value of configuration as code. But as our needs grew, we required something more powerful—a true infrastructure as code solution that could manage not just GitHub, but our entire platform.

## Directory Structure

```
REFERENCE/
├── index.md                          # You are here
├── legacy-safe-settings/              # The Old Ways
│   ├── README.md                      # Original Safe-Settings documentation
│   ├── org-settings.yml               # Organization-wide settings (archived 2025-08-13)
│   ├── suborg-platform-clan.yml      # Platform team configuration (archived 2025-08-13)
│   ├── repo-citadel-config.yml       # Citadel repository settings (archived 2025-08-13)
│   └── migration-notes.md            # Lessons from the transition
├── decisions/                         # Architecture Decision Records
│   ├── 000-template.md               # ADR template
│   ├── 001-terraform-migration.md    # Why we moved to Terraform
│   ├── 002-covenant-citadel-split.md # Separating philosophy from implementation
│   └── 003-trunk-based-development.md # Adopting TBD
└── deprecated/                        # Retired patterns and practices
    ├── branch-protection-rules.md    # Replaced by Repository Rulesets
    └── manual-runbooks.md            # Superseded by automation

```

## The Legacy Safe-Settings Files

### `legacy-safe-settings/org-settings.yml`
**Original Purpose**: Defined organization-wide GitHub settings including rulesets, labels, and default behaviors.  
**Superseded By**: `citadel-config/github.tf` - Terraform GitHub provider resources  
**Key Learning**: YAML was readable but lacked the power of a true programming language. We needed conditionals, loops, and modules.

### `legacy-safe-settings/suborg-platform-clan.yml` 
**Original Purpose**: Configured settings for all `service-*` repositories under the platform team's domain.  
**Superseded By**: `citadel-config/modules/github-stronghold/` - Reusable Terraform module  
**Key Learning**: The suborg pattern was powerful but inflexible. Terraform modules provide better composition and reusability.

### `legacy-safe-settings/repo-citadel-config.yml`
**Original Purpose**: Specific configuration for the citadel-config repository itself.  
**Superseded By**: Self-referential Terraform configuration in `citadel-config`  
**Key Learning**: Having the configuration repository configure itself created elegant self-hosting.

## Architecture Decision Records

Our most important documents. Each ADR captures:
- **Context**: What situation prompted this decision?
- **Decision**: What did we decide to do?
- **Consequences**: What were the results?
- **Status**: Is this still our approach?

### Featured Decisions

#### ADR-001: Terraform Migration
**Status**: Implemented  
**Summary**: Moved from Safe-Settings YAML to Terraform for infrastructure management  
**Key Outcomes**: 
- Unified management of GitHub and Cloudflare
- State management and drift detection
- Modular, reusable configurations

#### ADR-002: Covenant-Citadel Split
**Status**: Implemented  
**Summary**: Separated philosophical governance (Covenant) from technical implementation (Citadel)  
**Key Outcomes**:
- Clear separation of concerns
- Governance changes don't trigger infrastructure changes
- Philosophy documented separately from implementation

#### ADR-003: Trunk-Based Development
**Status**: Active  
**Summary**: Adopted TBD with short-lived feature branches  
**Key Outcomes**:
- Reduced integration pain
- Faster feedback cycles
- Simplified Git history

## Deprecated Patterns

### Branch Protection Rules → Repository Rulesets
**Deprecated**: 2024-06  
**Reason**: GitHub's Repository Rulesets provide more power and flexibility  
**Migration Path**: All branch protection converted to rulesets with enhanced conditions

### Manual Runbooks → Automated Responses
**Deprecated**: 2024-09  
**Reason**: Manual steps at 3 AM are error-prone  
**Migration Path**: All critical runbooks converted to automated workflows or scripts

## The Wisdom of the Archives

Each archived file contains a header comment block:

```yaml
# ARCHIVED: 2025-08-13
# REASON: Migrated to Terraform (citadel-config/github.tf)
# ORIGINAL PURPOSE: Organization-wide GitHub settings
# NOTABLE FEATURES: First implementation of Conventional Commits enforcement
# LESSONS LEARNED: YAML insufficient for complex conditional logic
```

## How to Use the Archives

### For Learning
Read the progression from simple YAML to complex Terraform. See how our needs evolved and how our tools evolved to meet them.

### For Debugging
When something breaks, check if we've solved this problem before. The archives often contain the "why" behind current decisions.

### For Proposals
Before proposing a "new" idea, check if we've tried it before. If we have, understand why we moved away from it.

## Contributing to the Archives

When deprecating a pattern or configuration:

1. **Document the transition**: Create an ADR explaining the change
2. **Archive with context**: Add header comments explaining the what, when, why
3. **Preserve the knowledge**: Include lessons learned and migration notes
4. **Update this index**: Keep the guide current for future archaeologists

## The Living Memory

These archives are not static. They grow with every major decision, every migration, every lesson learned. They are our institutional memory, preserved for those who come after.

### Recent Additions
- **2025-08**: The Great Migration from Safe-Settings to Terraform
- **2025-07**: Adoption of Repository Rulesets over Branch Protection
- **2025-06**: Implementation of Conventional Commits

### Upcoming Additions
- Implementation of Policy as Code for Cloudflare
- Migration to OpenTelemetry for observability
- Adoption of SLSA for supply chain security

## The Archivist's Wisdom

> "In our old configurations, we see our younger selves—eager, learning, sometimes naive. We keep these records not to mock our past, but to measure our growth. Every deprecated pattern was once our best idea. Every archived configuration once solved real problems. They deserve respect, even in retirement."

## Quick Reference: What Replaced What

| Old System | New System | Migration Date | ADR |
|------------|------------|----------------|-----|
| Safe-Settings YAML | Terraform IaC | 2025-08 | [001](./decisions/001-terraform-migration.md) |
| Branch Protection | Repository Rulesets | 2024-06 | [004](./decisions/004-repository-rulesets.md) |
| Manual Runbooks | Automated Workflows | 2024-09 | [005](./decisions/005-automated-operations.md) |
| Click-Ops | GitOps | 2025-01 | [006](./decisions/006-gitops-everything.md) |

---

*"The Archives are not about the past. They are about not repeating it unnecessarily."*

**Return to**: [`README.md`](../README.md) - The Covenant  
**See Also**: [`citadel-config`](https://github.com/the-nash-group/citadel-config) - Current implementation  
**Questions?**: Open an issue labeled `archaeology`
