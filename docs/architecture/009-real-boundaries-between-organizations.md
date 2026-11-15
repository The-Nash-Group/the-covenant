# ADR-009: Real Boundaries Between Organizations

## Metadata

| Field | Value |
|-------|-------|
| **Date** | 2026-11-15 |
| **Last Updated** | 2026-11-15 |
| **Author** | Agent, recording the Guardian's decision |
| **Governance Level** | Covenant (GOV-006 structural single-Guardian mode) |
| **Status** | Accepted |
| **Related ADRs** | ADR-001, ADR-002, ADR-004, ADR-007 (superseded in part), ADR-008 |
| **Supersedes** | ADR-007 §2 (the three invariants) and the session-scoping purpose of ADR-007 §4, in part. See [What Is Retired or Cut Back](#3-what-is-retired-or-cut-back) |

> **How this was decided.** This is a Covenant-tier change. Under GOV-006,
> structural single-Guardian mode, a Covenant decision is one recorded decision
> of the one natural-person Guardian. That decision is his answer to issue 368
> of the parent repository, `The-Nash-Group/the-nash-group`, given in a parent
> session on 2026-11-14 local time (2026-11-15 UTC) and recorded on the issue in
> his words. The pull request that carries this record is the publication
> surface that GOV-002 asks for, and its merge is his own. No Council reviewed
> it and no independent human review occurred. Under GOV-002 the 72-hour and
> one-week periods are deliberation defaults in this mode, not elapsed-time
> gates; none is claimed here. This record has effect only as merged text.

## Context

ADR-007 (2026-04-20) drew the boundary between the parent and each subsidiary as a boundary of text. Its three invariants said that parent names must not appear in any file a subsidiary-scoped agent reads, that a subsidiary adopts a parent rule only by restating it, and that a subsidiary session must not read parent files. ORG-001 version 1.0, the Subsidiary Authority Specification version 1.0 and the parent's operating standards carried those rules out with a forbidden-identifier list, a restatement clock and log, relay carried by the human, and a series of audits.

Three things are on record since then.

1. **One human.** GOV-006 (2026-08-29) records that the estate has one natural-person Guardian. His standing direction of 2026-11-14, kept in the parent's `OWNER-DIRECTIONS.md`, says that rules which assume a second human, or which send routine work to him for a signature, are defects in the contract.
2. **What the text rules protected.** An inventory of the rules that police a boundary, recorded on parent issue 368, found six that protect only separation of text between the Guardian's own agents. It found that nothing mechanical enforces any of them. It recorded what each has cost: recurring audits, a restatement log, relays carried by hand, and two-sided acceptance of agreements between his own organizations.
3. **What is real.** The same issue named five things that a boundary can separate and that do matter, and proposed that a boundary be kept only where it separates one of them.

The Guardian answered yes, with two conditions. He then corrected the record of who owns Litecky Editing Services.

### Contrary Considerations

ADR-007 gave three reasons for the text boundary. Each is answered here, not dismissed.

- *Legal identity separation erodes when a file describes a subsidiary as part of the parent.* The decision keeps the name rule where the outside world or the law reads the text: public and customer-facing material and legal documents. It retires the rule for agent-facing files.
- *Dev agents are contaminated by parent vocabulary.* The agents on both sides are one person's. The decision treats what an agent may read as no boundary, and treats what an agent may author as the boundary: authoring stays with the owning organization's sessions.
- *Restatement discipline is lost under inheritance by pointer.* A citation by version is a pointer with a fixed target. The subsidiary's contract stays its own document, and it restates where it changes the rule. The decision accepts that a cited version can fall behind with no clock to catch it.

### What Was Not Established

The issue records these as not established. The decision does not depend on them.

- Two questions about Happy Patterns LLC that the issue names. The LLC's contract stays its own document and its records stay in its own store, so neither has to be answered first.
- What each organization's own contract files say. The inventory read the parent's side only.

Litecky's legal form was recorded as unverified when the issue was written. The Guardian has since stated it (Decision §6).

## Decision

The Guardian's answer on the issue, in his words:

> Issue 368: yes. A boundary is real only where it separates one of your five things. Retire or cut back the six text-only rules as you listed. Two conditions: subsidiary sessions may read parent files but not write them, and Litecky stays a real boundary in both directions.

### 1. The Rule

A boundary between two of the Guardian's organizations is real only where it separates one of:

1. another person's interest, or a separate legal entity;
2. money: payers, billing, paid plans, spend;
3. credentials and secret authority: each organization keeps its own machine identity and secret root, and values never cross;
4. customers' and third parties' data, and legal-entity records (tax numbers, bank and address data);
5. public identity: brand, voice, domains, anything the outside world sees.

Across a real boundary nothing crosses without the receiving organization's own record, and credentials never cross. Everything else is not a boundary.

### 2. The Two Conditions

1. Subsidiary sessions may read parent files but not write them.
2. Litecky stays a real boundary in both directions.

### 3. What Is Retired or Cut Back

Six rules protected only separation of text between the Guardian's own agents.

| Rule before | Under this decision |
|-------------|---------------------|
| A subsidiary session must not read any parent file | Retired. It may read parent files; it never writes them |
| Parent names, role names and policy numbers must not appear in subsidiary agent-facing files | Kept only for public and customer-facing material and legal documents |
| A subsidiary adopts a parent rule only by rewriting it in its own words, on a 90, 60 or 30 day clock, logged parent-side | A subsidiary may cite a parent standard by version. It restates only where it changes the rule. No clock |
| Guidance crosses only when the human carries it | Sessions hand off to each other directly. A record is kept only across a real boundary |
| Quarterly contamination audit, semi-annual restatement drift review, annual isolation audit, router diff on each template change | Replaced by one check of the five real things |
| Two-sided acceptance of an agreement between two of his own organizations | The terms (cost owner, data classes) stay. The acceptance ceremony goes |

### 4. What Stays Exactly As It Is

- Each organization's own GitHub organization, domain and zone.
- Each organization's own secret root. No organization authenticates to another's instance. Agents hold no provider credential.
- One payer per organization. Spend is the Guardian's.
- Tax, bank and address data out of agent-readable files.

### 5. One Change to an Existing Rule

A parent agent may read, review and merge in a subsidiary's repository, and an agent of one subsidiary may do the same in another subsidiary's, under the merge rule of the parent's Agentic Workflow Standard, section One-Human Operating Contract. Authoring stays with the owning organization's sessions. Parent agents do not author in a subsidiary's repository.

A subsidiary session does not merge in the parent's repositories. That follows from the first condition (§7, reading 2).

This does not apply to Litecky.

### 6. Litecky Editing Services

The Guardian corrected the record minutes after that answer, on the same day. The correction supersedes the paragraph of that answer about Litecky, and every earlier record, including the parent registry's "co-owned" entry.

- Litecky Editing Services is a sole proprietorship. It belongs to its owner, who is another person. It is not co-owned.
- The Guardian is its administrator, with full authority over all technical and administrative decisions for Litecky.
- For agents, every Litecky decision comes to the administrator. No agent contacts the owner, asks for her approval, or waits on it. His direction is that the "both owners" approval rule be removed from Litecky's reserved list and replaced with "the administrator decides". That list is in Litecky's own contract, which this record does not edit.
- What is hers to decide as the business owner (her money, her clients, her legal records, her name) he takes to her himself and brings back the answer.
- Litecky stays a real boundary: it is a separate legal entity and another person's business. Its records, credentials and client data stay separate from the rest of the estate.
- The registry keeps a place for an owner governance role, unassigned. He intends to involve her later. Nothing may assume it now.

The Subsidiary Authority Specification §7.3 holds the record, by role. This record names no person. Names belong in the parent's registry.

### 7. Readings Taken

Four places in the decision needed a reading. Each is stated so that the Guardian can correct it in one sentence.

1. **"In both directions."** None of the retirements in §3, and not the change in §5, applies to Litecky, except the retirement of the audits (reading 3). No session from another organization reads into, writes to, reviews or merges in Litecky beyond what Litecky's own contract already allows. Litecky's sessions keep their present rules. This is the conservative reading.
2. **"Not write."** It is read conservatively. A subsidiary session may read the parent's files, and may read and review a parent pull request. It does not author, push to or merge in the parent's repositories. Parent sessions, and sessions of the other organizations among themselves, may read, review and merge across organizations under the merge rule, except in Litecky.
3. **The audits, for Litecky.** A real boundary in both directions means the parent does not read into Litecky to audit it. So the audit series is retired for every organization, Litecky included. Litecky's part of the one check is run from inside Litecky by its own session, for its administrator, and reported value-blind.
4. **The list.** The table in §3 states the six rules more fully than the table on the issue. Two differences are readings: the router diff on each template change is counted with the audit series and retired with it, and the name rule is kept for legal documents as well as public and customer-facing material.

## Consequences

### Positive

1. **One set of directions can be read everywhere.** A subsidiary session can read the Guardian's standing directions and the parent's standards where they are, without a relay.
2. **Sessions hand off directly.** The Guardian is no longer the path between two of his own agents.
3. **The audit series ends** for every organization, and the restatement clock ends for every organization except Litecky. One check asks about the five things that matter.
4. **A subsidiary's pull request can be read and merged by a parent agent or by an agent of another subsidiary.** Review no longer waits for a session of the owning organization. The parent's own pull requests are still merged only by parent sessions.
5. **The boundaries that protect something are named.** Another person's interest, money, credentials, data and records, and public identity are stated as the reasons, so a later rule can be tested against them.

### Negative

1. **Parent text is now readable by subsidiary sessions,** including the parent's records about other organizations. What must not be read has to be kept out of agent-readable files, as Boundaries 3 and 4 already require.
2. **The structural correlate of legal separation in agent-facing files is gone.** ADR-007 counted it as a benefit for Happy Patterns LLC. What remains is the separation of records, money, credentials and public identity.
3. **A citation can fall behind.** With no clock and no log, nothing notices a subsidiary that cites an old version.
4. **Two regimes run side by side.** Litecky keeps the version 1.0 rules while the other organizations do not, and its part of the check is reported from inside, not read by the parent. An agent has to know which organization it is in.
5. **The cross-organization merge rests on a declared control.** The parent's Agentic Workflow Standard records that sessions act through one GitHub login, so the provider cannot tell an author from a reviewer or one organization's session from another's.

### Neutral

1. **Nothing mechanical changes.** This repository has no enforcement power, and no rule here was mechanically enforced before.
2. **The three tiers stand.** Parent, subsidiary and project, what each owns, the transitional hosting rule and sensitive metadata placement are unchanged from ADR-007.
3. **Each organization still has its own contract.** Its own sessions amend it. A parent agent does not.

## Decision Record

GOV-006 asks that a decision in structural single-Guardian mode record five things. GOV-002 asks for the same record on an amendment.

1. **The decision and its scope.** The Decision section above. Its scope in this repository is ORG-001, the Subsidiary Authority Specification, the entity-boundary rule of AGT-001, and the sentences in other Covenant documents that restated them.
2. **The principles it implements.** The Compliance section below.
3. **Material evidence and contrary considerations.** The Context section above. The evidence is the inventory and the costs recorded on parent issue 368; this record did not repeat the inventory.
4. **Non-effects and unavailable operations.**
   - No provider, account, seat, credential, payer, host, state or runtime action is taken or authorized. No access is granted.
   - No file outside this repository is changed: not the parent's standards, router template, registry, restatement log or action ledger, and no organization's own contract.
   - Nothing about credentials, secret authority, payers or legal-entity records changes.
   - Litecky's own contract and reserved list are not edited.
   - Recording Litecky's owner does not make her a Guardian and does not activate multi-human Council mode. No record shows that she has accepted governance authority in this estate, and nothing may assume it.
   - Independent human review remains unavailable under GOV-006. The read by an agent that did not author a change, which the merge rule asks for, is not independent human review.
   - AGT-001 still names a Synthetic Council debate, a Council verdict and a 72-hour period for Covenant decisions, and a test in Seven Springs before a change to agent governance. None took place. GOV-002 and GOV-006 govern this decision; AGT-001's older text is not amended here.
5. **No independent human review.** This decision had none.

## Compliance

- **Principle #5** (Infrastructure as Code): Organization structure, the registry and the router template remain versioned artifacts.
- **Principle #6** (No Committed Secrets): Credential values and legal-entity records stay out of tracked, agent-readable files.
- **Principle #9** (Zero Trust): A boundary is kept where it can be checked: who holds a credential, who pays, where a record lives. A rule that nothing checks is named a declared control.
- **Principle #10** (Least Privilege): Each organization keeps its own machine identity and secret root, and values never cross.
- **Principle #13** (Code Without Docs is Incomplete): The decision is recorded here, in the policy and in the specification together.
- **Principle #16** (Living Law): ADR-007 came from an earlier moment. This record changes it from operating experience.

## Implementation Path

This record changes Covenant text only. The rest is done where it lives, each in its own pull request:

1. **The parent's operating standards**: the Agentic Workflow Standard's scope sentence about Litecky, the Subsidiary Governance Standard, and the Estate Agreements Standard.
2. **The router template** and its deployed copy.
3. **The parent's registry**: Litecky's ownership, and the place held for an owner governance role.
4. **The parent's audit obligations**: the entries for the audits that the one check replaces, and the definition of the check.
5. **Each organization's own contract**, amended by its own session.

Until each of these merges, that file still carries the earlier rule. This record does not track their state.

## References

- [ADR-004: Federated Multi-Org Architecture](./004-federated-multi-org-architecture.md)
- [ADR-007: Subsidiary Authority and Identity Isolation](./007-subsidiary-authority-and-identity-isolation.md): superseded in part by this record
- [ADR-008: Policy Authority Topology](./008-policy-authority-topology.md)
- [ORG-001: Subsidiary Authority and Real Boundaries](../../policies/org-001-subsidiary-authority.md): version 2.0
- [Subsidiary Authority Specification](../../policies/specs/subsidiary-authority.md): version 2.0.0
- [AGT-001: Agent Governance](../../policies/agt-001-agent-governance.md)
- [GOV-002: Covenant Amendment Process](../../policies/gov-002-amendment-process.md)
- [GOV-006: Council Decision Quorum](../../policies/gov-006-decision-quorum.md)
- Parent issue 368, `The-Nash-Group/the-nash-group`: the decision
- `OWNER-DIRECTIONS.md` in the parent repository: the Guardian's standing directions
- `.org/standards/agentic-workflow.md` in the parent repository, One-Human Operating Contract: the merge rule and the reserved list

---

> **Living Documents**: ADRs may be updated when facts change, but changes require Guardian approval. Edit in place and add a changelog entry rather than creating a superseding ADR (reserve that for genuine decision reversals). Preserve the original date in the metadata; use "Last Updated" for the most recent edit.

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2026-11-15 | Agent, recording the Guardian's decision | Initial creation. Records the Guardian's decision on parent issue 368 under GOV-006 structural single-Guardian mode: a boundary is real only where it separates one of five things; six text-only rules are retired or cut back, the audit series for every organization; a parent agent, or an agent of another subsidiary, may read, review and merge in a subsidiary's repository under the merge rule, and a subsidiary session does not author, push to or merge in the parent's repositories; Litecky Editing Services is another person's sole proprietorship that the Guardian administers and stays a real boundary in both directions. Supersedes ADR-007 §2 and the session-scoping purpose of §4 in part. No independent human review. |
| 2026-11-15 | Agent, after a read by an agent that did not write the change | Wording corrected, with no change to the decision. Where and when the decision was given is stated exactly. A fourth reading is added, on the list of retired rules. The record now says what AGT-001 still names for such a decision and that none of it took place. Two open questions the issue names are referred to and not restated. The merge rule is cited from the parent's standard. Reading 2 follows the reading recorded on the decision issue and carried in the parent's standard: a subsidiary session may review a parent pull request, where the reading said comment. The record names no person. |
| 2026-11-15 | Agent, after a read by an agent that did not write the change | Corrected the row above: it said reading 2 follows a ruling, where the record is a reading recorded on the decision issue and carried in the parent's standard. This corrects who decided, not the decision. |
