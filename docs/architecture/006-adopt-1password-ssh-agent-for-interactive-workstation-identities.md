# ADR-006: Adopt 1Password SSH Agent for Interactive Workstation Identities

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2026-04-15 |
| **Last Updated** | 2026-04-15 |
| **Author** | Agent |
| **Governance Level** | Covenant (2 Watchers + 2 Mentors, 72h debate) |
| **Status** | Accepted |
| **Related ADRs** | ADR-002, ADR-004 |

> **Current-state note (2026-04-15)**: This decision approves the Nash Group workstation pattern for interactive SSH use on the managed Guardian machine and clarifies how existing policies should be interpreted during migration. Citadel enforcement of required commit signatures remains a follow-up implementation step; the policy direction is settled here.

## Context

The current Guardian workstation model still relies on standard OpenSSH or macOS `ssh-agent` behavior with interactive private keys stored as plaintext files on disk. That pattern is common, but it becomes materially weaker on an agentic workstation where local tools and synthetic agents may have broad filesystem and process visibility.

The organization needs a low-friction default for human interactive Git and SSH use that improves key custody without collapsing the boundary between human and machine identities.

Three tensions drove this decision:

1. **Interactive key custody**: Plaintext private keys on disk are easy to copy, back up unintentionally, or expose to local tooling.
2. **Commit-signing ambiguity**: Existing guidance requires signed commits, but implementation language can be misread as "GPG specifically" instead of "verifiable signed provenance."
3. **Human versus machine identity drift**: It is tempting to reuse a convenient human workstation identity for unattended automation, especially during bootstrap. That would erase attribution boundaries and create shared-credential risk.

### Alternatives Considered

**Alternative 1: Keep standard OpenSSH/macOS `ssh-agent` with on-disk private keys** — Rejected. Lowest friction, but it leaves the interactive private key as a plaintext local asset on an increasingly agentic workstation.

**Alternative 2: Mandate GPG-only commit signing** — Rejected. The governing control is signed commits with verifiable provenance. SSH signing satisfies that requirement where the platform verifies it.

**Alternative 3: Use 1Password SSH agent for both humans and automation** — Rejected. Acceptable for interactive human use, unacceptable as the long-term answer for unattended agents, CI, servers, or shared automation.

**Alternative 4: Require hardware tokens only for every interactive user immediately** — Rejected for now. Strong security posture, but too much migration friction for the current bootstrap phase. Hardware-backed remains preferred where practical.

## Decision

We adopt **1Password SSH agent** as the Nash Group default for **interactive workstation SSH authentication** and approve **SSH-based Git commit signing** where it satisfies the repo's signed-commit control.

### 1. Scope: Human Interactive Identities Only

This decision applies to:

- Human interactive workstation SSH identities
- Human-supervised local agent activity using that identity only when a human explicitly approves the action in the loop
- Optional SSH-based Git commit signing for those same interactive identities

This decision does **not** define a machine identity strategy.

### 2. Interactive Key Custody

Interactive private keys on managed workstations must move out of plaintext active storage on disk once migrated.

- Private keys must be held by a vault-backed or hardware-backed agent
- 1Password SSH agent is the default approved custody path for managed workstation interactive use
- Public keys may remain on disk for OpenSSH host mapping, Git SSH signing references, and inventory
- Vault-backed or hardware-backed interactive keys are preferred over plaintext private keys on disk

### 3. Commit Signing Control is Technology-Agnostic

The governing control is:

> **Commits must be signed.**

That control is satisfied by a GitHub-verifiable signing method that meets provenance and enforcement requirements. Unless a higher-level policy explicitly requires GPG-only, the organization accepts:

- GPG-based commit signing
- SSH-based commit signing

SSH signing is therefore an approved way to satisfy signed-commit requirements for interactive workstation users.

### 4. SSH Forwarding Default

SSH agent forwarding must be disabled by default on managed workstations.

- `ForwardAgent no` is the baseline default
- Forwarding may be enabled only for explicitly trusted hosts and explicitly trusted workflows
- Forwarding exceptions must stay narrow and intentional, not convenience defaults

### 5. Human and Machine Identities Stay Separate

Human interactive identities must never become shared automation credentials.

- Unattended agents, CI, servers, cron jobs, and background automation must use separate nonhuman credentials
- Approved machine identity patterns include deploy keys, GitHub Apps, OIDC, short-lived certificates, or equivalent narrowly scoped credentials
- 1Password SSH agent is not the Nash Group machine-identity platform

## Consequences

### Positive

1. **Better workstation key custody**: Interactive private keys no longer need to live as active plaintext files on disk.
2. **Approval in the loop**: SSH use from the workstation requires explicit user approval through the interactive agent flow.
3. **Clearer policy language**: Signed-commit requirements stop being confused with GPG-only requirements.
4. **Cleaner trust boundary**: Human identities and machine identities remain distinct, preserving attribution and revocation clarity.

### Negative

1. **New dependency surface**: Interactive SSH now depends on 1Password client availability and user approval flow.
2. **Migration work**: Existing workstation SSH configs and Git signing configs must be updated deliberately.
3. **Staged enforcement gap**: Citadel rulesets still need to turn on required commit signatures as a follow-up implementation change.

### Neutral

1. **Public key files remain useful**: Public keys may still live on disk without changing the private-key custody model.
2. **Machine identity roadmap unchanged**: Existing GitHub App, OIDC, and scoped token work remains the right path for unattended automation.

## Compliance

- **Principle #6** (Secrets Never Committed): Interactive private keys stay out of git and out of active plaintext workstation storage.
- **Principle #9** (Trust, but Verify Everything): Human SSH use remains explicit, auditable, and approval-gated.
- **Principle #10** (Least Privilege): Human workstation identities are not repurposed into broad, shared automation credentials.
- **DOC-001**: Documents the workstation identity decision as an ADR rather than leaving it as tribal knowledge.
- **SEC-004**: Clarifies workstation baseline controls for interactive SSH identity custody and forwarding defaults.
- **SEC-005**: Preserves the boundary that machine identity policy governs nonhuman credentials, not human workstation flows.
- **COM-001**: Clarifies that signed commits are the control and that SSH signing is acceptable where the platform verifies it.

## References

- [ADR-002: Governed Agentic Development](./002-governed-agentic-development.md)
- [ADR-004: Federated Multi-Org Architecture](./004-federated-multi-org-architecture.md)
- [COM-001: Git Workflow Standards](../../policies/com-001-git-workflow.md)
- [SEC-004: Security Baseline Requirements](../../policies/sec-004-security-baseline.md)
- [SEC-005: Machine Identity Management](../../policies/sec-005-machine-identity.md)
- [Secrets Management Specification](../../policies/specs/secrets-management.md)

---

> **Living Documents**: ADRs may be updated when facts change, but changes require Guardian approval. Edit in place and add a changelog entry rather than creating a superseding ADR (reserve that for genuine decision reversals).

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2026-04-15 | Agent | Initial creation — approves 1Password SSH agent for interactive workstation identities, clarifies signed-commit interpretation, and preserves human-versus-machine identity boundaries |
