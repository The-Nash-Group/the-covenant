# GOV-006: Council Decision Quorum

**Policy ID:** GOV-006
**Category:** Governance
**Effective Date:** 2024-09-30
**Last Updated:** 2026-08-29

## Statement

The normal Council model is 2 Watchers plus 2 Mentors from different clans,
all of whom are distinct natural persons. The Nash Group currently has one
natural-person Guardian. While that fact remains true, the **structural
single-Guardian mode** below is the governing decision path.

This is a permanent constitutional exception, not a temporary deviation. It
has no expiry, review date, synthetic-council dependency, or restoration
project. It changes only through a later Covenant amendment based on direct
evidence that additional natural persons have accepted governance authority.

## Independence rule

Quorum independence is counted by natural person, never by account, login,
credential, role, team membership, seat, agent, or model invocation.

The `verlyn13` and `happy-patterns` GitHub accounts are bindings of the same
`nash-operator` human principal. An approval from one account on work authored
through the other is **operator dual-account continuity**: it may satisfy a
provider's technical non-self-approval rule, but it is not independent review,
consensus, or a second quorum participant.

Synthetic agents may research, challenge, test, and recommend. They are not
natural-person Guardians and cannot manufacture human independence. No quorum
evaluator is required or authorized by this policy; an evaluator could count
account events but could not prove the missing natural-person distinction.

## Structural single-Guardian mode

The current Guardian may make Covenant, Citadel, and Stronghold decisions after
recording:

1. the decision and its scope;
2. the principles it implements;
3. material evidence and contrary considerations;
4. explicit non-effects and unavailable operations; and
5. that the decision had no independent human review.

A pull request remains the durable source-review and publication surface. A
second account may supply required merge mechanics. Neither the PR nor that
account changes the decision's independence classification.

Decisions under this mode are prospective. They do not retroactively cure an
earlier invalid process, turn historical account activity into quorum, or prove
that an unavailable operation occurred.

## Operations that are unavailable

The following are **UNAVAILABLE**, not pending gates, while only one natural
person holds governance authority:

- independent human review, approval, consensus, veto, or attestation;
- a multi-human or separation-of-duties quorum;
- a two-person provider, credential, or break-glass ceremony where the safety
  contract requires distinct natural persons;
- recovery or escrow acceptance whose threshold requires custody by an
  independent natural person;
- a claim that operator dual-account continuity, multiple Guardian role hats,
  or synthetic-agent debate supplies independent oversight; and
- any action whose safety case depends on one natural person being unable to
  act alone.

This exception does not authorize those operations. A proposed action in one
of these classes must be redesigned so its safety does not depend on unavailable
independence, or it must remain unperformed until the needed distinct natural
person exists. Merely identifying an unavailable operation creates no issue,
ledger entry, evaluator, or continuing implementation obligation.

Single-Guardian emergency authority otherwise remains governed by GOV-003 and
the break-glass section of `GOVERNANCE.md`; this policy does not broaden any
provider, credential, host, state, or runtime authority.

## Multi-human Council mode

The 2-Watcher plus 2-Mentor model is dormant, not presumed. It may be activated
only by a later Covenant amendment that records the distinct natural persons,
their accepted roles, and the operations for which their independence is
meaningful. Additional accounts, agents, or seats alone do not activate it.

## Related documents

- [`GOVERNANCE.md`](../GOVERNANCE.md)
- [GOV-002: Covenant Amendment Process](./gov-002-amendment-process.md)
- [GOV-003: Break-Glass Procedures](./gov-003-break-glass.md)
- [Identity and Account Management Specification](./specs/identity-and-account-management.md)

## Change history

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-09-30 | 1.0 | Initial policy creation from `GOVERNANCE.md` Council Review. | Claude Code |
| 2026-08-29 | 2.0 | Established permanent structural single-Guardian mode, natural-person independence, dual-account continuity, and the operations that are unavailable rather than gated. Removed speculative evaluator and implementation obligations. | Guardian |
