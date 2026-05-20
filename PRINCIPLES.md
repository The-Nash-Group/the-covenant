# PRINCIPLES.md
*The Art of the Duel - Technical Standards of The Nash Group*

> "Excellence is not an act, but a habit. Our code is not a project, but a practice."

## The Human Element

These principles are not self-enforcing. They require human judgment, as defined in [The Human Mandate](./HUMAN_MANDATE.md). The Architect translates these principles into code, the Judge ensures compliance, and the Gardener maintains their health over time.

## Core Technical Principles

Each principle follows the sacred format:
- **The Law**: The rule we follow
- **The Lesson**: The hard-fought wisdom behind it
- **The Implementation**: How it's enforced in `the-citadel`
- **The Guardian**: Which role from the Human Mandate owns this principle

> **Layering note (2026-05-12):** The Law and Lesson are the durable Covenant
> content. Implementation blocks are illustrative translation targets or
> historical examples unless current Citadel, Shield, Nexus, or subsidiary
> evidence proves the specific control is live. Future amendments should keep
> provider-specific and workflow-specific detail in the owning implementation
> layer.

---

## Source Control & Git Workflow

### Principle 1: The Sacred Timeline is Linear and Clean

**The Law**
The `main` branch represents our production truth. Its history must be linear, readable, and meaningful. Every commit tells a story.

**The Lesson**
We learned from the chaos of tangled merge commits, where debugging became archaeology and rollbacks became gambling. A messy Git history is a confused chronicle that obscures the true story of our code's evolution.

**The Implementation**
In `the-citadel/github.tf`:
```hcl
resource "github_repository_ruleset" "sacred_timeline" {
  enforcement = "active"
  target      = "branch"
  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
    }
  }
  rules {
    required_linear_history = true
    deletion                = false
    force_push              = false
  }
}
```

### Principle 2: Every Commit Shall Speak Its Purpose

**The Law**
All commits to `main` must follow Conventional Commits format. PR titles become squash commit messages and must be meaningful.

**The Lesson**
"Fix stuff" and "Update code" are not messages—they are admissions of defeat. When debugging production at 3 AM, clear commit messages are the difference between quick resolution and despair.

**The Implementation**
In `the-citadel/github.tf`:
```hcl
resource "github_repository_ruleset" "conventional_commits" {
  rules {
    commit_message_pattern {
      operator = "starts_with"
      pattern  = "^(feat|fix|docs|chore|refactor|perf|test|build|ci|revert)(\\(.+\\))?: .+"
      name     = "Conventional Commits"
    }
  }
}
```

---

## Code Review & Quality Gates

### Principle 3: No Code Enters the Timeline Unchallenged

**The Law**
Every change to `main` requires peer review. No exceptions, no "quick fixes," no "just this once."

**The Lesson**
Unreviewed code is a Trojan horse. We've seen single-line changes take down production, and "obvious" fixes introduce subtle bugs. The wisdom of the clan is always greater than any individual warrior.

**The Implementation**
In `the-citadel/github.tf`:
```hcl
resource "github_repository_ruleset" "peer_review" {
  rules {
    pull_request {
      required_approving_review_count = 1
      dismiss_stale_reviews_on_push  = true
      require_code_owner_review       = true
      require_last_push_approval     = false
    }
  }
}
```

### Principle 4: The Machines Must Bless the Code

**The Law**
Automated checks (CI, linting, tests) must pass before merge. The machines are impartial judges.

**The Lesson**
"It works on my machine" is not a deployment strategy. Consistent, automated validation catches issues that human eyes miss and enforces standards without favoritism.

**The Implementation**
In `the-citadel/github.tf`:
```hcl
resource "github_repository_ruleset" "automated_gates" {
  rules {
    required_status_checks {
      strict_required_status_checks_policy = true
      required_status_checks = [
        { context = "ci" },
        { context = "lint" },
        { context = "security-scan" }
      ]
    }
  }
}
```

---

## Infrastructure & Configuration

### Principle 5: The Fortress is Defined by Blueprints, Not by Hand

**The Law**
All infrastructure and platform configuration must be defined as code. Manual changes in UIs are forbidden sorcery.

**The Lesson**
We've lost entire configurations to accidental clicks. We've spent days trying to recreate a manually-configured system. "Documentation" of manual steps is fiction—only code is truth.

**The Implementation**
In the relevant `the-citadel` OpenTofu/IaC workspaces:
- All DNS records defined in OpenTofu/IaC
- All WAF rules codified
- All repository settings declared
- Drift detection via scheduled `tofu plan` runs

### Principle 6: Secrets Are Never Committed

**The Law**
No secret, token, password, or key shall ever be committed to Git, even in encrypted form within the repository.

**The Lesson**
A secret in Git is compromised forever. We've seen repositories cloned by contractors, forked publicly by accident, and indexed by search engines. Git remembers everything.

**The Implementation**
In `the-citadel/github.tf`:
```hcl
resource "github_repository_ruleset" "secret_scanning" {
  rules {
    secret_scanning {
      enable_push_protection = true
    }
  }
}
```

---

## Development Practices

### Principle 7: The Trunk is Sacred

**The Law**
We practice Trunk-Based Development. Feature branches live for days, not months. The `main` branch is the single source of truth.

**The Lesson**
Long-lived branches are parallel universes that diverge from reality. The pain of merging grows exponentially with time. Small, frequent integrations reduce risk and increase velocity.

**The Implementation**
Enforcement through culture and tooling:
- PR automation closes branches older than 14 days
- Small PR metrics tracked and celebrated
- Feature flags over feature branches

### Principle 8: Fail Fast, Recover Faster

**The Law**
Systems must fail quickly and obviously when something is wrong. Silent failures and degraded states are the enemy.

**The Lesson**
A system that limps along with partial failures is harder to debug than one that fails completely. We've lost more data to silent corruption than to hard crashes.

**The Implementation**
Standard health check endpoints and monitoring:
- All services implement `/health` and `/ready`
- Cloudflare health checks configured for all origins
- Immediate alerts on check failures

---

## Security & Access

### Principle 9: Trust, but Verify Everything

**The Law**
Zero trust architecture. Authenticate every request, authorize every action, audit every access.

**The Lesson**
"Internal only" networks are a myth. We've seen internal threats, compromised credentials, and confused deputies. Every request must prove its worthiness.

**The Implementation**
In `the-citadel/cloudflare.tf`:
```hcl
resource "cloudflare_access_application" "internal_services" {
  name             = "Internal Services"
  domain           = "*.internal.thenash.group"
  session_duration = "8h"
}
```

### Principle 10: The Principle of Least Privilege

**The Law**
Every identity (human or machine) gets exactly the permissions they need, no more, no less. Permissions expire and must be renewed.

**The Lesson**
Over-privileged accounts are ticking time bombs. We've seen admin credentials used for daily work, service accounts with org-wide access, and forgotten bot tokens with write permissions.

**The Implementation**
In `the-citadel/github.tf`:
```hcl
resource "github_team_repository" "least_privilege" {
  team_id    = github_team.service_team.id
  repository = github_repository.service.name
  permission = "push"  # Not admin, not maintain, just push
}
```

---

## Observability & Operations

### Principle 11: If It's Not Measured, It Doesn't Exist

**The Law**
Every service must emit metrics, logs, and traces. Observability is not optional—it's fundamental.

**The Lesson**
"It seems slow" is not actionable. "The P99 latency increased from 200ms to 800ms starting at 14:23 UTC" is. We cannot fix what we cannot see.

**The Implementation**
Standard observability requirements:
- Structured JSON logging
- OpenTelemetry tracing
- Prometheus metrics exposition
- Defined SLIs and SLOs

### Principle 12: Runbooks Are Executable Documentation

**The Law**
Every alert must have a runbook. Every runbook must be automated or have clear, tested manual steps.

**The Lesson**
A 3 AM page is not the time to figure out what to do. We've lost hours to incomplete runbooks and outdated procedures. The response must be mechanical, not creative.

**The Implementation**
Alert definitions include runbook URLs:
```hcl
resource "monitoring_alert" "high_error_rate" {
  name        = "High Error Rate"
  description = "Error rate exceeds 1%"
  runbook_url = "https://runbooks.thenash.group/high-error-rate"
}
```

---

## Documentation & Knowledge

### Principle 13: Code Without Docs is Incomplete

**The Law**
Every repository must have a README. Every API must have schemas. Every decision must have an ADR (Architecture Decision Record).

**The Lesson**
"The code is self-documenting" is a lie told by those who remember what they wrote. Six months later, even the author needs documentation.

**The Implementation**
Repository templates enforce documentation:
- README.md required
- `/docs` directory structure
- OpenAPI specs for all APIs
- ADRs for significant changes

---

## Evolution & Deprecation

### Principle 14: Progress Without Breakage

**The Law**
Breaking changes require migration paths. Deprecation requires notice periods. Evolution requires backward compatibility.

**The Lesson**
Moving fast and breaking things breaks trust. We've seen services abandoned because upgrades were too painful. Smooth migrations build confidence.

**The Implementation**
Deprecation policy enforcement:
- Deprecated features marked but not removed for 2 quarters
- Migration guides required
- Automated compatibility testing

---

## Dependency Management

### Principle 15: The Three Circles of Trust

**The Law**
Dependencies shall be managed in three concentric circles: L0 (Frontier - bleeding edge exploration), L1 (Vanguard - pinned direct dependencies), L2 (Supporting Cast - transitive dependencies). Each circle has distinct update velocities and risk tolerances.

**The Lesson**
We lost weeks to cascading transitive breaks. We lost innovation to over-conservative pinning. The middle path: explore fearlessly at the core, ship on stable foundations, ignore the noise at the edges.

**The Implementation**
In `the-citadel/github.tf`:
- Repository templates enforce layer structure
- Renovate organization config enforces update streams
- CI workflows validate layer integrity

---

## The Meta-Principle

### Principle 16: These Principles Are Living Law

**The Law**
These principles evolve through experience. They are not carved in stone but written in a living repository.

**The Lesson**
Dogma without reflection becomes ritual without purpose. We must learn, adapt, and improve our principles as we learn new lessons.

**The Implementation**
This document itself is under version control, with a clear change process defined in `GOVERNANCE.md`. Every principle can be challenged, debated, and evolved.

---

## Quick Reference: Principle to Implementation Map

| Principle | Citadel Config File | Resource Type |
|-----------|-------------------|---------------|
| Linear History | `github.tf` | `github_repository_ruleset` |
| Conventional Commits | `github.tf` | `github_repository_ruleset` |
| Required Reviews | `github.tf` | `github_repository_ruleset` |
| CI Gates | `github.tf` | `github_repository_ruleset` |
| IaC Only | `terraform.tf` | OpenTofu backend configuration |
| Secret Scanning | `github.tf` | `github_repository_ruleset` |
| Zero Trust | `cloudflare.tf` | `cloudflare_access_*` |
| Least Privilege | `github.tf` | `github_team_repository` |
| Three Circles of Trust | `github.tf` | Repository templates, Renovate config |

---

*"These are not rules imposed upon us, but wisdom earned through trial. Each principle is a scar that taught us to be better."*

**Previous**: [`GOVERNANCE.md`](./GOVERNANCE.md) - How we make decisions
**Implementation**: [`the-citadel`](https://github.com/The-Nash-Group/citadel-config) - Where these principles become code
**History**: [`REFERENCE/decisions/`](./REFERENCE/decisions/) - Why we chose these principles
