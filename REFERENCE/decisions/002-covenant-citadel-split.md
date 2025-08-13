# ADR-002: Separation of Philosophy and Implementation

**Date**: 2025-08-13  
**Status**: Accepted  
**Deciders**: @the-nash-group/watchers, @the-nash-group/mentors  

## Context

As we migrated to Terraform, we initially considered keeping everything in one repository - principles, governance, and Terraform code together. This would have been simpler but raised concerns about clarity of purpose and separation of concerns.

## Problem

1. **Mixed Audiences**: Philosophy interests all stakeholders; Terraform interests engineers
2. **Different Change Velocities**: Principles evolve slowly; implementation changes frequently
3. **Approval Confusion**: Who approves what? Philosophy vs. technical implementation
4. **Testing Challenges**: Can't easily test philosophical documents
5. **Access Control**: Different security requirements for docs vs. infrastructure code

## Decision

Separate governance and principles (`the-covenant`) from technical implementation (`citadel-config`).

## Consequences

### Positive
- **Clear Separation**: Philosophy (why) vs. implementation (how)
- **Appropriate Workflows**: Deliberation for principles, CI/CD for infrastructure
- **Focused Repositories**: Each repo has one clear purpose
- **Better Security**: Infrastructure secrets isolated from documentation
- **Cleaner History**: Philosophical debates separate from technical commits

### Negative
- **Synchronization**: Must ensure principles and implementation stay aligned
- **Two PRs**: Some changes require PRs in both repositories
- **Cross-Reference**: Need to maintain links between principles and implementation
- **Onboarding**: New contributors must understand both repositories

## Implementation

### The Covenant (Philosophy)
- Contains PRINCIPLES.md, GOVERNANCE.md, and other documentation
- No automation, no technical enforcement
- Changes require broad consensus and debate period
- Public repository for transparency

### Citadel-Config (Implementation)
- Contains Terraform code that implements the principles
- Full CI/CD automation with plan/apply
- Changes require technical review and testing
- Private repository for security

### Workflow
1. Principle changes proposed and debated in `the-covenant`
2. Once ratified, implementation PR opened in `citadel-config`
3. Terraform plan shows exact infrastructure changes
4. Apply on merge enforces the new principle

## Lessons Learned

- Document the relationship clearly in both READMEs
- Every Terraform resource should reference its governing principle
- Regular audits ensure alignment between repositories
- Consider a tool to validate implementation matches principles

## References

- [Conway's Law](https://en.wikipedia.org/wiki/Conway%27s_law)
- [Separation of Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns)
- Original discussion: Issue #48 (archived)