# ADR-005: Adopt OpenTofu as IaC Engine

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2026-03-16 |
| **Last Updated** | 2026-05-02 |
| **Author** | Agent |
| **Governance Level** | Citadel (1 Mentor + 1 Watcher) |
| **Status** | Accepted |
| **Related ADRs** | ADR-001, ADR-003, ADR-004 |

> **Current-state note (2026-04-08)**: This decision is no longer speculative. OpenTofu is the live IaC engine in `the-citadel`, Hetzner Object Storage is the active remote state backend, and the multi-org migration delivered through Phase 4 on 2026-04-08 with the parent Forge witness gap closed. Treat HCP Terraform references below as decision-time context rather than the current operating model.

## Context

The Nash Group's infrastructure is managed as code through Terraform, executed via HCP Terraform (Terraform Cloud) as the state backend and approval gate. This has worked well technically — the HCL code, provider ecosystem, and workflow patterns are sound.

However, HashiCorp's trajectory toward a business-first (paid) model changes the economics and long-term viability of this dependency:

1. **BSL licensing**: HashiCorp relicensed Terraform under the Business Source License (BSL 1.1) in August 2023, restricting competitive use. While the current Nash Group usage is not directly affected, this signals a strategic direction toward paid tiers for features that were previously open.
2. **HCP Terraform cost trajectory**: HCP Terraform (formerly Terraform Cloud) is a SaaS dependency with pricing that scales with usage. For a single-operator holding company managing 5 GitHub orgs, the cost-to-value ratio degrades over time.
3. **Vendor concentration risk**: Backend (HCP), binary (terraform), provider registry, and state management are all controlled by a single vendor post-IBM acquisition. This violates the spirit of Principle #9 (Zero Trust) applied to toolchain dependencies.
4. **OpenTofu maturity**: OpenTofu, the Linux Foundation fork of Terraform, reached stable 1.x compatibility. As of March 2026, it offers native S3 locking (`use_lockfile = true`), state encryption at rest, `tofu test` for infrastructure testing, LSP support, and an MCP server for AI-assisted development — features that match or exceed HashiCorp Terraform.

### Alternatives Considered

**Alternative 1: Stay on Terraform + HCP** — Rejected. Increasing vendor lock-in, paid-model trajectory, single-vendor risk for the entire IaC stack.

**Alternative 2: Terraform binary + self-hosted backend** — Rejected. Still depends on BSL-licensed binary. If self-hosting the backend anyway, the marginal effort to switch to OpenTofu is near-zero and eliminates the licensing concern entirely.

**Alternative 3: Pulumi or CDK** — Rejected. Would require rewriting all existing HCL, losing the investment in current infrastructure code. The issue is the vendor, not the language.

**Alternative 4: OpenTofu + SaaS control plane (Spacelift, Scalr)** — Rejected. Introduces a new SaaS dependency; the goal is to reduce external dependencies, not trade one for another.

## Decision

We adopt **OpenTofu** as the IaC engine, with a self-hosted execution and state architecture on Hetzner.

### 1. OpenTofu Replaces Terraform

The `terraform` binary is replaced by `tofu`. All HCL code is 100% compatible — no resource, provider, or module changes required.

- **Version pinning**: OpenTofu version managed via mise (`.mise.toml`), pinned in `.org/standards/tool-versions.md`
- **Provider registry**: OpenTofu maintains its own registry; all current providers (GitHub, Cloudflare, Random, Time) are available
- **Lock file**: `.terraform.lock.hcl` is regenerated on `tofu init` (same format, same purpose)

### 2. Hetzner Object Storage Replaces HCP Terraform State

Remote state moves from HCP Terraform (`app.terraform.io`) to Hetzner Object Storage (S3-compatible):

```
Current:  cloud { organization = "the-nash-group" }  →  app.terraform.io
Future:   backend "s3" { ... }                        →  Hetzner Object Storage
```

- **Locking**: OpenTofu native S3 lockfile (`use_lockfile = true`) — no DynamoDB required
- **Encryption**: OpenTofu state encryption at rest (built-in feature)
- **Recovery**: Bucket versioning for state history and rollback
- **Cost**: ~6 EUR/month for Hetzner Object Storage

### 3. GitHub Actions Self-Hosted Runner on Hetzner

The execution plane moves from HCP Terraform's remote runners to a self-hosted GitHub Actions runner on Hetzner:

- **Runner host**: Dedicated VM or container on existing Hetzner infrastructure
- **Isolation**: Runner dedicated to IaC jobs only — no colocated services
- **Approval gate**: GitHub Actions environment protection rules replace HCP manual approval
- **Secrets**: Runner environment provides cloud credentials via OIDC where possible, env vars where not

### 4. Git Repository Remains the Control Plane

The PR-based plan/apply workflow is preserved:

```
Developer creates PR
  → CI runs `tofu plan` on self-hosted runner
  → Plan posted as PR comment
  → Guardian reviews and approves
  → Merge triggers `tofu apply` with environment protection gate
  → Apply runs on self-hosted runner against Hetzner Object Storage state
```

### 5. Developer Tooling

- **VS Code / Cursor**: OpenTofu VS Code extension with IntelliSense and validation
- **LSP**: `tofu-ls` for editor-agnostic language support
- **MCP**: OpenTofu Registry MCP server for AI-assisted development
- **Testing**: `tofu test` for infrastructure assertions (create, check, destroy)

## Multi-Organization IaC Structure

ADR-004 established a federated multi-org architecture with five GitHub organizations. This decision extends naturally: each org gets its own OpenTofu root module with isolated state, while shared governance modules encode the 16 Covenant principles as infrastructure defaults.

### Architecture

```
the-citadel/terraform/
├── modules/                     ← Shared governance (Covenant as code)
│   ├── github-org-baseline/     ← Org settings, security defaults
│   ├── github-repo-standard/    ← Repo creation with Covenant defaults
│   ├── github-rulesets/         ← Branch protection, commit rules
│   └── cloudflare-zone-standard/← Zone security baseline (ADR-003)
├── orgs/                        ← Per-org root modules
│   ├── the-nash-group/          ← Parent (Citadel governance)
│   ├── happy-patterns/          ← LLC (Citadel governance)
│   ├── jefahnierocks/           ← Personal (Stronghold governance)
│   ├── litecky-editing/         ← Small business (Stronghold governance)
│   └── seven-springs/           ← Sandbox (Stronghold governance)
└── global/                      ← Cross-org Cloudflare account settings
```

### Design Rationale

Separate root modules per org (rather than a single monolith) because:

1. **State isolation**: A bad apply in one org cannot corrupt another org's state
2. **Agent-addressable**: A synthetic agent working on `happy-patterns` never needs to read `litecky-editing` config
3. **Independent deployment**: Orgs can be planned/applied independently via CI matrix strategy
4. **Governance mapping**: Different orgs have different approval requirements (Citadel vs Stronghold)

Shared modules enforce Covenant principles by construction — subsidiaries call them, they don't copy-paste. Validation blocks in modules enforce minimums (e.g., at least 1 approval per Principle #3) that cannot be lowered.

### State Layout (Hetzner S3)

```
tng-citadel-tfstate/
├── global/terraform.tfstate
├── orgs/the-nash-group/terraform.tfstate
├── orgs/happy-patterns/terraform.tfstate
├── orgs/jefahnierocks/terraform.tfstate
├── orgs/litecky-editing/terraform.tfstate
└── orgs/seven-springs/terraform.tfstate
```

Full architecture details: `.claude/orchestration/opentofu-migration/MULTI-ORG-IAC-ARCHITECTURE.md`

## Consequences

### Positive

1. **Zero licensing risk**: OpenTofu is MPL-2.0 under the Linux Foundation — no BSL restrictions
2. **No SaaS dependency for state**: Hetzner Object Storage is S3-compatible, portable, and cheap (~6 EUR/month)
3. **No SaaS dependency for execution**: Self-hosted runner eliminates HCP Terraform entirely
4. **Native state encryption**: Built into OpenTofu, not an add-on feature
5. **Native S3 locking**: No DynamoDB or external lock table required
6. **Better AI tooling**: MCP server and LSP support purpose-built for modern development
7. **Full HCL compatibility**: Zero changes to existing infrastructure code
8. **Aligns with ADR-004**: Self-hosted infrastructure (like Authentik, Infisical) rather than SaaS dependencies

### Negative

1. **Self-hosted runner maintenance**: Must monitor, update, and secure the runner VM
2. **No built-in UI for run history**: HCP Terraform's run dashboard is lost; CI logs become the audit trail
3. **Manual approval via GitHub**: Environment protection rules are less granular than HCP's workspace-level gates
4. **Runner security surface**: Self-hosted runners on private repos require careful workflow isolation (no fork PR execution)

### Neutral

1. **State migration**: One-time operation to move state from HCP to Hetzner S3 — reversible, low risk with proper backup
2. **Cost shift**: HCP Terraform cost eliminated; Hetzner Object Storage + runner cost added (net reduction)
3. **POC 1 reframed**: "Multi-Org Terraform" becomes "Multi-Org OpenTofu" — same validation goals, different binary

## Compliance

- **Principle #1** (SSoT): State remains in a single remote backend — Hetzner Object Storage replaces HCP
- **Principle #5** (Infrastructure as Code): All changes still flow through code → plan → review → apply
- **Principle #6** (No Committed Secrets): State encryption at rest; secrets in runner environment, not in code
- **Principle #9** (Zero Trust): Eliminates single-vendor trust for the entire IaC stack; OIDC for runner auth where possible
- **Principle #10** (Least Privilege): Dedicated runner with scoped credentials; no broad cloud access
- **Principle #12** (Executable Runbooks): CI workflows remain the executable runbook for infrastructure changes
- **Principle #14** (Progress Without Breakage): HCL is 100% compatible; migration is incremental and reversible

## References

- [ADR-001: Three-Pillar Repository Architecture](./001-establish-three-pillar-repository-architecture.md)
- [ADR-003: Cloudflare Governance Baseline](./003-establish-cloudflare-governance-baseline.md)
- [ADR-004: Federated Multi-Org Architecture](./004-federated-multi-org-architecture.md)
- [OpenTofu S3 Backend Documentation](https://opentofu.org/docs/language/settings/backends/s3/)
- [OpenTofu State Encryption](https://opentofu.org/docs/language/state/encryption/)
- [GitHub Actions Self-Hosted Runners](https://docs.github.com/actions/hosting-your-own-runners)
- [Hetzner Object Storage](https://docs.hetzner.com/storage/object-storage/overview/)

---

> **Living Documents**: ADRs may be updated when facts change, but changes require Guardian approval. Edit in place and add a changelog entry rather than creating a superseding ADR (reserve that for genuine decision reversals). Preserve the original date in the metadata; use "Last Updated" for the most recent edit.

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2026-03-16 | Agent | Initial creation — documents Terraform → OpenTofu migration, Hetzner Object Storage backend, self-hosted runner architecture |
| 2026-03-16 | Agent | Added Multi-Organization IaC Structure section — per-org root modules, shared governance modules, state isolation layout. References MULTI-ORG-IAC-ARCHITECTURE.md |
| 2026-04-08 | Agent | Marked the ADR accepted and added a current-state note reflecting delivered OpenTofu adoption on Hetzner-backed multi-org infrastructure. |
| 2026-05-02 | Agent | Recorded full Phase 4 delivery cycle: Cloudflare provider v5.18.0 pinned across all workspaces (PR #1, #2, 2026-04-04), multi-org workspace registry live with `jefahnierocks` Cloudflare-first scaffold (PR #3, 2026-04-06), parent and `jefahnierocks` workspaces converged with independent local verification (2026-04-07), FU-5 Forge fix witnessed (PR #5, run 24153173285, 2026-04-08), OPA pinned to 1.15.2 with all active policies migrated to Rego v1 syntax and SEC-003 enforced in CI for the first time (2026-04-09), first Cloudflare public delivery slice landed (PR #7 DNS+DNSSEC for `thenash.group`, 2026-04-10), and Pages project + custom domain codified (PR #8, 2026-04-25). |
