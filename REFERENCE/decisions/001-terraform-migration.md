> **ARCHIVED**: This is a legacy decision record. Current ADRs live in `docs/architecture/`.

# ADR-001: Migration from Safe-Settings to Terraform

**Date**: 2025-08-13
**Status**: Accepted
**Deciders**: @the-nash-group/watchers, @the-nash-group/mentors

## Context

We initially adopted Safe-Settings as our GitHub configuration management tool. It served us well for basic repository settings, branch protection, and team permissions. However, as our infrastructure needs grew beyond GitHub to include Cloudflare, monitoring, and other platforms, we found ourselves managing configuration across multiple tools and interfaces.

## Problem

1. **Limited Scope**: Safe-Settings only manages GitHub, not our entire infrastructure
2. **YAML Limitations**: No real programming constructs (loops, conditionals, functions)
3. **Weak Validation**: Errors only discovered at runtime
4. **No State Management**: Difficult to track drift or rollback changes
5. **Poor Modularity**: Copy-paste patterns instead of reusable modules

## Decision

Migrate from Safe-Settings to Terraform for all infrastructure configuration management.

## Consequences

### Positive
- **Unified Tool**: Single tool for GitHub, Cloudflare, AWS, etc.
- **True IaC**: Full programming language with modules, conditionals, and functions
- **State Management**: Terraform state tracks all resources and detects drift
- **Plan/Apply Workflow**: See exactly what will change before applying
- **Ecosystem**: Vast provider ecosystem and community modules
- **Testing**: Can write actual tests for infrastructure code

### Negative
- **Learning Curve**: Team must learn HCL and Terraform concepts
- **State Complexity**: State file management requires discipline
- **Longer Feedback Loop**: Plan/apply cycle vs. immediate YAML updates
- **Migration Effort**: Must translate all YAML to Terraform resources

## Implementation

1. Create `citadel-config` repository for Terraform code
2. Archive Safe-Settings configuration in `the-covenant/REFERENCE/legacy-safe-settings/`
3. Translate YAML resources to Terraform GitHub provider resources
4. Use Terraform Cloud for state management (free tier)
5. Implement GitHub Actions workflow for plan/apply automation

## Lessons Learned

- Start with remote state from day one
- Modularize early - refactoring later is painful
- Document the mapping between old and new resources
- Run both systems in parallel during transition
- Keep the old configuration as reference

## References

- [Terraform GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest)
- [Safe-Settings Repository](https://github.com/github/safe-settings)
- Original discussion: Issue #42 (archived)
