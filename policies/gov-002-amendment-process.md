# GOV-002: Covenant Amendment Process

**Policy ID:** GOV-002
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2026-08-29

## Statement

Every Covenant amendment requires a reviewable proposal, a recorded human
decision, and publication through the repository. The process must identify
what changes, why it changes, its operational effect, and what it does not
authorize.

GOV-006 determines who can decide. Its structural single-Guardian mode is the
current path. While that mode applies, fixed Council-member counts, mandatory
multi-human consensus, and automated debate or quorum evaluators are not
amendment prerequisites.

## Amendment record

A governed amendment records:

1. **Change** — the exact normative text being added, changed, or retired.
2. **Rationale** — the evidence and principles supporting the decision.
3. **Impact** — present effects, compatibility consequences, and unavailable
   operations.
4. **Non-effects** — provider, credential, host, state, runtime, subsidiary, or
   other actions the source change does not authorize.
5. **Decision** — the Guardian's prospective approval, amendment, or rejection,
   including an explicit statement when no independent human review occurred.

The issue and pull request may carry this record; a second narrative packet is
not required. An implementation issue is created only when the decision leaves
a concrete executable obligation. A decision that retires work must not create
a replacement queue merely to preserve the appearance of progress.

## Deliberation

In multi-human Council mode, the normal debate period is 72 hours for a minor
change and one week for a major change. In structural single-Guardian mode,
those periods are deliberation defaults, not elapsed-time gates. The Guardian
may decide after the proposal and material evidence are reviewable and must
record that the single-Guardian path was used.

Historical debate time from a procedurally invalid change does not retroactively
validate that change. A later decision may nevertheless ratify the same text
prospectively under the governance rules effective for the later decision.

## Publication

- Use a conventional commit and a pull request.
- Reference the Covenant principles implemented.
- Keep the decision and source status consistent at merge.
- Preserve material objections and historical defects; do not rewrite them as
  approvals that never occurred.
- Treat technical approval or merge events from another account of the same
  natural person as operator continuity, not independent review.

No workflow, timer, quorum counter, decision tracker, announcement bot, or
automatic downstream issue is required by this policy. Such controls require
their own present consumer and separately reviewed implementation authority.

## Exceptions

- Typographical and formatting corrections that do not change meaning may use
  the ordinary repository process.
- Emergency action is governed by GOV-003. Any later constitutional lesson is
  still published through this amendment process.

## Related documents

- [`GOVERNANCE.md`](../GOVERNANCE.md)
- [GOV-003: Break-Glass Procedures](./gov-003-break-glass.md)
- [GOV-006: Council Decision Quorum](./gov-006-decision-quorum.md)

## Change history

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-09-30 | 1.0 | Initial policy creation from `GOVERNANCE.md` Ritual of Amendment. | Claude Code |
| 2026-08-29 | 2.0 | Reduced the amendment contract to proposal, human decision, and publication; aligned it with structural single-Guardian mode; retired speculative timer, quorum-evaluator, and auto-issue obligations. | Guardian |
