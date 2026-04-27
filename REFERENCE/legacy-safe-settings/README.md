# Legacy Safe-Settings Configuration

**Archived**: 2025-08-13
**Replaced By**: Terraform configuration in `citadel-config`
**Migration ADR**: [001-terraform-migration.md](../decisions/001-terraform-migration.md)

## Overview

This directory contains the archived Safe-Settings configuration that previously managed our GitHub organization settings. These YAML files were the law of the land before The Great Migration to Terraform.

## Files

### `org-settings.yml`
- **Purpose**: Organization-wide GitHub settings and rulesets
- **Replaced by**: `citadel-config/github.tf` - `github_organization_settings` and `github_repository_ruleset` resources
- **Key Features**: Branch protection, commit message patterns, required status checks

### `suborg-platform-clan.yml`
- **Purpose**: Settings for all `service-*` repositories under the platform team
- **Replaced by**: `citadel-config/modules/github-stronghold/` Terraform module
- **Key Features**: Team permissions, branch protection, review requirements

### `repo-citadel-config.yml`
- **Purpose**: Specific settings for the citadel-config repository
- **Replaced by**: `citadel-config/repositories.tf` - individual repository configurations
- **Key Features**: Repository metadata, merge strategies, topics

## Why We Migrated

1. **Scope Limitations**: Safe-Settings only managed GitHub; we needed Cloudflare, monitoring, etc.
2. **Language Limitations**: YAML lacked loops, conditionals, and functions
3. **No State Management**: Couldn't track drift or plan changes
4. **Poor Modularity**: Too much copy-paste, no reusable components

## Migration Mapping

| Safe-Settings Feature | Terraform Equivalent |
|----------------------|---------------------|
| `rulesets:` | `github_repository_ruleset` resource |
| `branch_protection:` | `github_branch_protection` resource |
| `teams:` | `github_team_repository` resource |
| `labels:` | `github_issue_label` resource |
| `repository:` settings | `github_repository` resource |

## Lessons for the Future

1. **Start with State**: We learned the hard way that state management is crucial
2. **Modularize Early**: Refactoring YAML into Terraform modules was painful
3. **Document Everything**: This mapping saved us during migration
4. **Parallel Run**: We ran both systems for 2 weeks to ensure parity

## Note on the Arbiter Workflow

The `enforce-covenant.yml` workflow that previously lived in `.github/workflows/` attempted to run Safe-Settings via GitHub Actions. This has been completely replaced by Terraform Cloud's plan/apply workflow in `citadel-config`.

Key differences:
- Safe-Settings ran on schedule and push
- Terraform runs on PR (plan) and merge (apply)
- Safe-Settings was eventually consistent
- Terraform is immediately consistent

## For Historical Reference Only

These files are preserved for:
- Understanding our infrastructure history
- Reference during troubleshooting
- Learning from past patterns
- Audit and compliance requirements

**DO NOT** attempt to use these configurations. All infrastructure is now managed through Terraform in the `citadel-config` repository.
