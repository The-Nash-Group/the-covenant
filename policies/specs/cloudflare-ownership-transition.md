# Cloudflare Ownership Transition Specification

**Status:** PROPOSED
**Date:** 2026-04-08
**Authority:** Draft Covenant specification for review; parent directive is binding for current execution
**Implements:** Principle 5 (Infrastructure as Code), Principle 9 (Zero Trust), Principle 10 (Least Privilege), ADR-004, ADR-005

---

## Purpose

Define how Cloudflare resources are owned and placed during the current Nash Group transition from a shared POC-era control account to full per-suborg operational separation.

This specification exists to prevent two bad outcomes:

1. Flattening single-zone resources into `terraform/global/` just because Cloudflare scopes them at the account level.
2. Pretending per-suborg Cloudflare accounts already exist when the current POC is still running from one shared control account.

---

## Transitional Stewardship Model

Until dedicated Cloudflare accounts and tokens exist for each active subsidiary, the Nash Group parent operates the current shared Cloudflare account as a **temporary parent control plane**.

This is a stewardship posture, not the desired end state.

- The shared Cloudflare account is a **POC-era exception**
- The **workspace root remains the ownership boundary**
- The account boundary and the ownership boundary are intentionally different during this transition

This means operational ownership is modeled in OpenTofu by workspace root, even when Cloudflare exposes the resource at account scope.

---

## Placement Rule

### Rule 1: Single-zone resources stay with the owning workspace

If a Cloudflare resource serves only one zone or one subsidiary, it **must** live in that workspace root.

Examples:
- `terraform/orgs/the-nash-group/`
- `terraform/orgs/jefahnierocks/`

This rule still applies when Cloudflare models the resource at account scope.

Examples of account-scoped but single-zone resources that still belong in the owning workspace:
- Cloudflare Pages projects used only for one zone
- Cloudflare Pages custom domains bound to one zone
- Tunnels or related configuration used only for one subsidiary's services
- Certificates, hostname resources, or routing resources that serve one zone only

### Rule 2: `terraform/global/` is reserved for truly shared resources

`terraform/global/` may contain only resources that are genuinely shared across multiple zones or multiple subsidiaries.

Examples:
- Account-level resources used by more than one workspace
- Cross-zone shared Workers, lists, account rulesets, or Zero Trust resources
- Shared platform primitives that do not belong to any one subsidiary

### Rule 3: Do not use `global/` as a parking lot

`terraform/global/` must not become a holding area for resources that are merely inconvenient to place elsewhere.

Account scope alone is not enough to justify `global/`.

---

## Current Exception Scope

As of April 8, 2026:

- `thenash.group` and `jefahnierocks.com` are both managed from one shared Cloudflare control account
- The current POC uses one shared Cloudflare API token path for active management
- This means current workspace isolation is enforced by **state separation, placement discipline, review, and process**, not by full Cloudflare IAM isolation

This is acceptable only as a temporary transitional exception.

---

## Risk Acknowledgment

During this transition, one workspace can theoretically affect another if the operator or automation uses the shared token incorrectly. The boundary is therefore weaker than the intended target architecture.

That risk is tolerated only because:

- the current POC is still small
- the current first slice is intentionally narrow
- the placement rule keeps code ownership clear
- full separation is planned as an exit condition, not ignored

---

## First-Writer Rule

When a new Cloudflare resource set is first brought under OpenTofu management:

1. Discovery must be read-only
2. Resource placement must be justified against this specification
3. A reviewed local plan must exist before any first authoritative write
4. Explicit human approval is required before the first authoritative write
5. Default path is a normal Citadel PR and first authoritative write through the paved OpenTofu workflow on `main`
6. If local apply or another exception path is required, the reason must be recorded in parent orchestration notes before execution

The first authoritative write must leave an audit trail that explains:

- why the resource belongs in that workspace
- why it does not belong in `terraform/global/`
- whether the write used the paved Forge path or an approved exception path

---

## Exit Criteria

The shared-account stewardship exception should be retired when all of the following become true for a subsidiary:

1. The subsidiary has a stable, ongoing Cloudflare resource footprint
2. The subsidiary has enough operational value or blast radius to justify separation
3. The subsidiary can be assigned dedicated Cloudflare credentials or a dedicated account without blocking the active POC sequence
4. The migration path is defined for any account-level resources currently stewarded by the parent

The default intended end state is:

- per-suborg Cloudflare account or equivalent credential boundary
- per-suborg workspace continues to own its own Cloudflare resources
- `terraform/global/` shrinks to only genuinely shared parent-level resources

---

## Review Cadence

This transition specification must be reviewed:

- before the first real public Cloudflare delivery slice is implemented
- after the first public POC is operational
- quarterly while the shared-account exception remains active

---

## Near-Term Application

The recommended first implementation slice is:

- `thenash.group`
- DNS records
- DNSSEC
- Cloudflare Pages project and Pages domain for the public site

These resources belong in:

- `the-citadel/terraform/orgs/the-nash-group/`

They do **not** belong in:

- `the-citadel/terraform/global/`

The more heterogeneous `jefahnierocks.com` zone is explicitly deferred until after the Nash public-delivery slice is stable.
