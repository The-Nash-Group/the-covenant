# AI Assistant Context - The Covenant
*The Philosophical Heart of The Nash Group*

> **IMPORTANT**: This repository has no technical enforcement power. It defines philosophy and governance. Implementation happens in `the-citadel`.

## Repository Purpose

**The Covenant** is the constitutional foundation of The Nash Group infrastructure. It contains:
- **GOVERNANCE.md** - The Laws of the Clans (who decides what)
- **PRINCIPLES.md** - 16 core principles (our engineering philosophy)
- **HUMAN_MANDATE.md** - The five archetypal Guardian roles
- **policies/** - constitutional invariants, policy-status semantics, and transitional specifications pending layer classification
- **REFERENCE/** - Historical decisions and migration artifacts

**Critical Principle**: Changes to philosophy and durable invariants PRECEDE changes to implementation. Do not implement in `the-citadel`, `the-shield`, `the-nexus`, or subsidiary/project repos before the owning authority layer is clear.

## The Three-Pillar Architecture

```
┌──────────────────┐
│  THE COVENANT    │ ← Philosophy & Governance (this repo) - The "Why"
│  (Philosophy)    │   Moral authority, no technical power
└──────────────────┘
         ↓ defines
┌──────────────────┐
│  THE CITADEL     │ ← Infrastructure as Code - The "How"
│  (Enforcement)   │   OpenTofu IaC, CI/CD, provider configs
└──────────────────┘
         ↓ enables
┌──────────────────┐
│  THE NEXUS       │ ← Operations & Services - The "What"
│  (Operations)    │   Apps, services, runtime policies
└──────────────────┘
```

## Key Concepts for AI Assistants

### The Human/Machine Boundary

**YOU MUST understand this sacred separation**:

**The System Will**:
- Enforce invariantly (apply rules exactly as written)
- Report deviations (detect drift without exception)
- Execute flawlessly (no opinions in automation)
- Automate toil (handle repetitive tasks)

**The Guardians Will**:
- Provide intent (define principles)
- Exercise judgment (review plans, triage alerts)
- Assume command (manual control in emergencies)
- Evolve the system (improve automation)

### Governance Hierarchy

1. **The Immortals** (All contributors)
   - Propose changes via Pull Requests
   - Participate in debates
   - Share knowledge

2. **The Mentors** (@the-nash-group/mentors)
   - Code owners for specific domains
   - Approve changes within their territories
   - Translate principles to technical implementation
   - **Primary roles**: The Judge, The Architect, The Gardener

3. **The Watchers** (@the-nash-group/watchers)
   - Infrastructure guardians
   - Emergency override capabilities
   - Final arbitration on governance disputes
   - **Primary roles**: The Judge (Security), The Philosopher (Security)

### The Five Guardian Archetypes

**These are "hats" Guardians wear, not job titles**:

1. **The Philosopher** - Debates and refines principles in this repo
2. **The Architect** - Transforms philosophy into OpenTofu/IaC and policy code
3. **The Judge** - Ensures changes align with principles
4. **The Gardener** - Maintains system health (dependencies, refactoring, drift)
5. **The Explorer** - Builds new capabilities within established boundaries

## Critical Governance Rules

**IMPORTANT: Decision Authority Matrix**:

| Decision Type | Required Approvals | Debate Period |
|---------------|-------------------|---------------|
| **Stronghold** (Single repo) | 1 Mentor | None |
| **Citadel** (Infrastructure) | 1 Mentor + 1 Watcher | None |
| **Covenant** (Principles/Governance) | 2 Watchers + 2 Mentors | 72 hours minimum |

**YOU MUST** ensure Covenant changes follow "The Ritual of Amendment":
1. The Proposal - Create branch, document change, reference rationale
2. The Debate Period - Minimum 72 hours, all Immortals may comment
3. The Council Review - Quorum of 4 members, consensus required
4. The Proclamation - Announcement and implementation issue creation

## The 16 Core Principles (Abbreviated)

1. **Sacred Timeline** - Linear history, no merge commits
2. **Conventional Commits** - `feat|fix|docs|chore(scope): description`
3. **Required Reviews** - No code enters main unchallenged
4. **CI/CD Gates** - Machines must bless the code
5. **Infrastructure as Code** - No manual changes, ever
6. **No Committed Secrets** - Zero tolerance
7. **Trunk-Based Development** - Short-lived feature branches
8. **Fail Fast, Recover Faster** - Embrace failures as learning
9. **Zero Trust** - Trust but verify everything
10. **Least Privilege** - Minimal necessary permissions
11. **Measure Everything** - If not measured, doesn't exist
12. **Executable Runbooks** - Documentation that runs
13. **Code Without Docs is Incomplete** - READMEs, ADRs, schemas
14. **Progress Without Breakage** - Backward compatibility always
15. **Three Circles of Trust** - L0 (Frontier), L1 (Vanguard), L2 (Supporting)
16. **Living Law** - Principles evolve through experience

**Full details**: See [PRINCIPLES.md](./PRINCIPLES.md)

## Common Workflows

### Proposing a Principle Change

```bash
# 1. Create proposal branch
git checkout -b proposal/my-principle-change

# 2. Edit PRINCIPLES.md or GOVERNANCE.md
vim PRINCIPLES.md

# 3. Create ADR documenting the change
../.org/tooling/generators/create-adr.sh "Adopt New Pattern"

# 4. Edit ADR with full context
vim docs/architecture/NNN-adopt-new-pattern.md

# 5. Submit PR with template
git add .
git commit -m "docs: propose principle change for [reason]"
git push origin proposal/my-principle-change

# 6. In PR: Reference existing principles, provide rationale
# 7. Wait minimum 72 hours for debate
# 8. Requires 2 Watchers + 2 Mentors approval
```

### Creating an Architecture Decision Record

```bash
# Use the generator
../.org/tooling/generators/create-adr.sh "Decision Title"

# Template structure (IMPORTANT - fill all sections):
# - Status: Proposed | Accepted | Deprecated | Superseded
# - Context: What issue motivates this?
# - Decision: What are we proposing/doing?
# - Consequences: What becomes easier or harder?
# - References: Link to discussions, documents
```

### Maintaining Architecture Decision Records

ADRs are **living documents** — they should reflect current architectural truth rather than accumulate stale information. However, ADRs are still governance documents and changes require Guardian (human) approval.

1. **Propose updates to the Guardian** — agents must not unilaterally modify ADRs; get human sign-off first
2. **Edit in place rather than supersede** — unless the original decision is being genuinely reversed
3. **Add a row to the Changelog table** at the bottom of the ADR with the date, author, and summary of the change
4. **Preserve the original Date** in the metadata — use the "Last Updated" field for the most recent edit
5. **Keep the ADR self-contained** — an agent reading the ADR for the first time should get an accurate picture of today's architecture
6. **Only create a superseding ADR** (status: "Superseded by ADR-XXX") for genuine decision reversals where the original rationale no longer applies

### Reviewing a Covenant Change

**YOU MUST check**:
1. **Does it reference existing principles?** - Changes build on foundations
2. **Is rationale clear?** - Why is this necessary?
3. **Is implementation path defined?** - How will this be enforced?
4. **Are consequences documented?** - What becomes easier/harder?
5. **Is it actionable?** - Can the owning lower layer translate this to OpenTofu/IaC, Policy as Code, Shield/Nexus contracts, subsidiary restatements, or another evidence-backed enforcement artifact?

### Validation Commands

```bash
# Validate repository structure
../.org/tooling/validators/validate-repo-structure.sh .

# Validate naming conventions
../.org/tooling/validators/validate-naming.sh .

# Check for secrets
../.org/tooling/validators/check-secrets.sh .

# Run compliance audit (from parent)
../.org/tooling/auditors/audit-compliance.sh
```

## Important Files & Their Purposes

- **GOVERNANCE.md** - Complete governance rules and decision authority
- **PRINCIPLES.md** - All 16 principles with philosophy and implementation-impact notes
- **HUMAN_MANDATE.md** - The five Guardian roles and Human/Machine Creed
- **CONTRIBUTING.md** - How to propose changes
- **REFERENCE/** - Historical context and legacy configurations
- **docs/architecture/** - Architecture Decision Records (ADRs); ADR-007 (2026-04-20) defines the three-tier authority model that refines ADR-004 §4; ADR-008 (2026-05-17) defines the policy authority topology for Identity, Resource, Permission-Binding, and Runtime Enforcement domains.
- **policies/org-001-subsidiary-authority.md** - Subsidiary authority and identity isolation policy (the three invariants: identity isolation, authority restatement, spec flow)
- **policies/specs/** - Constitutional and transitional specifications (subsidiary-authority, secrets-management, github-machine-identity, cloudflare-ownership-transition, identity-and-account-management (v0.2.1 — the LIVE IAM contract), iam-specification (v1.1.0 PARTIALLY HISTORICAL — do not treat as current), organizational-design-quality). Provider-specific and workflow-specific sections are candidates for parent-standard, Shield, Citadel, Nexus, or subsidiary restatement homes.

## Constraints & Guidelines

**YOU MUST adhere to these rules**:

1. **This repo has NO automation** - No GitHub Actions, no CI/CD by design
2. **Changes here are CONSTITUTIONAL** - They become standards, contracts, automation, or restatements in the owning lower layer
3. **Every principle must be ACTIONABLE** - The Architect, Shield, Citadel, Nexus, or a subsidiary must be able to translate it without changing its meaning
4. **Documentation is PROPHECY** - What we write shapes what we build
5. **Conventional Commits REQUIRED** - `docs|feat|chore(scope): description`
6. **ADRs are LIVING DOCUMENTS** - May be updated when facts change, but changes require Guardian approval

## Anti-Patterns to Avoid

**NEVER**:
- Add GitHub Actions workflows to this repo (philosophy, not automation)
- Merge PRs without proper debate period (72h minimum for Covenant changes)
- Let ADRs become stale (propose updates to the Guardian when facts change)
- Modify ADRs without Guardian approval (these are governance documents)
- Propose principles that can't be enforced in code
- Skip the Ritual of Amendment for governance changes
- Implement in `the-citadel`, `the-shield`, `the-nexus`, or a subsidiary/project repo before the owning authority layer is clear

## Integration with Other Repositories

### From Covenant → Owning Lower Layer

**Standard workflow**:
1. Principle proposed and ratified in `the-covenant`
2. Implementation PR created in the owning lower-layer repository referencing the principle
3. Evidence-backed contracts, OpenTofu/IaC, policy code, runtime admission, or restatements translate philosophy into enforcement
4. Example reference: "Implements Covenant Principle 5: Infrastructure as Code"

## Working with Pre-commit Hooks

```bash
# Install (once)
pip3 install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files

# Skip for emergencies (RARE - document why)
git commit --no-verify -m "emergency: [reason]"
```

## Emergency Procedures

**If automation fails** (see HUMAN_MANDATE.md):
1. Humans assume command immediately
2. Take manual action to resolve incident
3. Document all manual changes
4. Create reconciliation PR within 24 hours
5. Update principles if pattern discovered

## Mission, Vision, Values

**Mission**: Build a single, unified platform that is timeless, secure, and self-aware.

**Vision**: A future where development is focused, creative, unburdened by toil, anchored by single source of truth.

**Values**:
- **Immortality through Code** - Software that outlives its creators
- **There Can Be Only One** - Single source of truth for everything
- **The Quickening is Knowledge** - Learn from every event, especially failures

## Quick Reference for Common Tasks

| Task | Command | Notes |
|------|---------|-------|
| Create ADR | `../.org/tooling/generators/create-adr.sh "Title"` | Edit to fill all sections |
| Validate structure | `../.org/tooling/validators/validate-repo-structure.sh .` | Must pass before commit |
| Check naming | `../.org/tooling/validators/validate-naming.sh .` | Enforce kebab-case |
| Scan secrets | `../.org/tooling/validators/check-secrets.sh .` | Zero tolerance |
| View memory | `/memory` | Shows loaded AGENTS.md files |

## Org-Wide Standards

**IMPORTANT - Apply to all Nash Group repos**:
- **Naming**: kebab-case for files/repos/dirs (except Python: snake_case.py)
- **Commits**: Conventional Commits format required
- **PRs**: Reference Covenant principles being implemented
- **Documentation**: UPPERCASE.md for special files (README.md, AGENTS.md, etc.)
- **History**: Linear only, squash and merge
- **Reviews**: Required for all changes

## For Codex

This repository is **The Covenant** — philosophy and governance.
See `../AGENTS.md` for full organizational context and the three-pillar architecture.

---

**Remember**: The Covenant without the Citadel is mere words. The Citadel without the Covenant is mere machinery. Together, they are civilization.

*Last Updated: 2026-06-28*
