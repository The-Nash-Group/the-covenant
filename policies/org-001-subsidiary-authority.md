# ORG-001: Subsidiary Authority and Real Boundaries

**Policy ID:** ORG-001
**Category:** Organizational Structure
**Version:** 2.0.1
**Effective Date:** 2026-04-20
**Last Updated:** 2026-11-15

> Formerly titled "Subsidiary Authority and Identity Isolation". A citation by
> that title, or of an invariant or section of version 1.0, resolves through
> [What This Replaces](#what-this-replaces).

## Statement

A boundary between two organizations of this estate is real only where it separates one of five things:

1. another person's interest, or a separate legal entity;
2. money: payers, billing, paid plans, spend;
3. credentials and secret authority: each organization keeps its own machine identity and secret root, and values never cross;
4. customers' and third parties' data, and legal-entity records (tax numbers, bank and address data);
5. public identity: brand, voice, domains, anything the outside world sees.

Nothing may cross a real boundary without the receiving organization's own record, and credentials **must not** cross at all. Everything else is not a boundary.

Two conditions bind this rule. A subsidiary session may read parent files and **must not** write them. Litecky Editing Services stays a real boundary in both directions.

Each organization remains its own authority over its own repositories, its own contract and its own records. Authoring in an organization's repository **must** stay with that organization's own sessions.

## Rationale

Version 1.0 treated every boundary between organizations as a boundary of text. A subsidiary session could not read a parent file, could not carry a parent name in an agent-facing file, and could adopt a parent rule only by rewriting it. Operation since then showed what those rules protected.

- **The agents on both sides belong to one person.** The estate has one natural-person Guardian (GOV-006). Separation of text between his own agents protected no person, payer, credential, customer or public face.
- **Nothing mechanical enforced the text rules.** They were carried by audits, a restatement log, hand-carried relays and acceptance ceremonies. Each was a recurring cost, recorded on the decision issue named in ADR-009.
- **The boundaries that protect something were already separate rules.** Separate organizations, domains and zones; separate secret roots; one payer each; legal-entity records out of agent-readable files. Those stay exactly as they are.

This version keeps what protects something real and retires what protected only the appearance of separation. It is the Guardian's decision, recorded in [ADR-009](../docs/architecture/009-real-boundaries-between-organizations.md).

## Scope

**Terms:**
- **Organization**: the parent (The Nash Group) or an entity in the parent's registry. "Subsidiary" is the registry's word for an entity this policy covers. It makes no claim about who owns a legal entity.
- **The Guardian**: the one natural person of GOV-006. The parent's operating standards call him the owner.
- **Session**: an agent session. It belongs to the organization whose directory it started in. An agent that a session starts belongs to the same organization.
- **Contract**: an organization's own agent-facing governance files, such as its `CLAUDE.md` and `AGENTS.md` and what they name.

**Applies To:**
- The parent and every organization in the parent's registry at `.org/iam/federation/subsidiaries.yaml`, in its directory under `~/Organizations/` and in its GitHub organization. The registry is the record of current directories and slugs.
- Every session and every agent a session starts.
- The router at `~/Organizations/CLAUDE.md`, which is maintained as a parent template and deployed to that path.

**Exceptions:**
- Litecky Editing Services. None of this version's retirements applies to it, except that of the audit series. See [Litecky Editing Services](#litecky-editing-services).
- Break-glass under GOV-003 is unchanged. An emergency write across organizations is logged and reconciled as GOV-003 says.

**Governed Elsewhere:**
- The merge rule, the reserved list and the Guardian's standing directions: the parent's Agentic Workflow Standard (`.org/standards/agentic-workflow.md`, One-Human Operating Contract) and `OWNER-DIRECTIONS.md`
- Session routing mechanics: `.org/standards/subsidiary-governance.md`
- Agreement terms between organizations: `.org/standards/estate-agreements.md`
- Agent role contracts and archetypes: `governance/agent-roles.yaml` and AGT-001
- Machine identity and credentials: SEC-005. Secrets: the Secrets Management Specification
- Operational detail and the per-organization record: Subsidiary Authority Specification

## The Five Real Boundaries

### Boundary 1: Another Person's Interest, or a Separate Legal Entity

What belongs to another person, or to a separate legal entity, is theirs: their obligations, their records, their decisions.

- Each organization keeps its own GitHub organization. This stays exactly as it is.
- An organization's own record is kept in its own repository, by its own sessions.
- What is another person's to decide is never decided by an agent. Litecky Editing Services is the present case.

### Boundary 2: Money

Each organization has one payer. Billing, paid plans and spend are kept per organization. Spend is the Guardian's. This stays exactly as it is.

### Boundary 3: Credentials and Secret Authority

Each organization keeps its own machine identity and its own secret root. No organization authenticates to another organization's instance. Agents hold no provider credential. Values never cross, in either direction, by any route, with or without a record.

This stays exactly as it is. SEC-005, the Secrets Management Specification and the parent's secret-authority standards hold these rules and their existing arrangements. This policy changes none of them and adds none.

### Boundary 4: Customers' and Third Parties' Data, and Legal-Entity Records

Customers' and third parties' data stays with the organization that holds it. Tax numbers, bank data and address data stay out of agent-readable files. This stays exactly as it is. See [Sensitive Metadata Placement](#sensitive-metadata-placement).

### Boundary 5: Public Identity

Brand, voice, domains and anything the outside world sees belong to the organization that presents them. Each organization keeps its own domain and zone. This stays exactly as it is.

The rule against parent names, role names and policy numbers is kept for a subsidiary's public and customer-facing material and its legal documents, and only there. The list of names and the permitted cross-references are those of version 1.0 (Subsidiary Authority Specification §2.1 and §2.2); this version changes only where the list applies. So a legal document may still name another entity where the document itself requires it, such as an operating agreement, a tax filing or a contract, and public press and marketing may still describe a subsidiary's relationship to the parent.

### Crossing a Real Boundary

Nothing crosses a real boundary without the receiving organization's own record: an entry in its own repository or records, made by its own session, that says what crossed. Credentials never cross.

## What Is Not a Boundary

These are the six rules of version 1.0, and of the parent's standards beside it, that protected only separation of text. Items 1 to 4 and 6 are retired or cut back for every organization except Litecky Editing Services. Item 5 is retired for every organization, Litecky included.

1. **Reading.** A subsidiary session may read parent files, and may read and comment on a parent pull request. It **must not** write them: it does not author, push to or merge in the parent's repositories. This is the reading taken of "not write", and it is the conservative one. Any session may read any organization's standards and the Guardian's directions, except that no session of another organization reads into Litecky and Litecky's sessions keep their present rule about parent files.
2. **Names in agent-facing files.** Parent names, role names and policy numbers may appear in a subsidiary's agent-facing files. The rule against them is kept only as Boundary 5 states it.
3. **Adoption.** A subsidiary may cite a parent standard by version. It restates a rule only where it changes the rule. There is no clock and no parent-side log of who adopted what.
4. **Hand-off.** Sessions hand off to each other directly. A record is kept only across a real boundary.
5. **Audits.** The quarterly contamination audit, the semi-annual restatement drift review, the annual isolation audit and the router diff on each template change are replaced by one check of the five real things, for every organization. The parent does not read into Litecky to audit it. See [One Check of the Five Real Things](#one-check-of-the-five-real-things).
6. **Agreements.** An agreement between two of the Guardian's own organizations keeps its terms: the cost owner and the data classes. Two-sided acceptance of it is no longer required.

### Review and Merge Across Organizations

A parent agent may read, review and merge in a subsidiary's repository, and an agent of one subsidiary may do the same in another subsidiary's, under the merge rule. The merge rule is the one in the parent's Agentic Workflow Standard, section One-Human Operating Contract, and is not restated here. The owning repository's own contract may ask for more.

A subsidiary agent does not merge in the parent's repositories. There it may read, and may comment on a pull request.

Authoring stays with the owning organization's sessions. A parent agent does not author in a subsidiary's repository. A subsidiary agent does not author in or push to the parent's repositories, and does not author in another subsidiary's.

The merge rule covers routine work. A change that the owning organization's contract reserves to the Guardian is still his.

This rule grants no access. Whether a session can reach another organization's repository is a fact of the login it runs under, read back from the provider.

None of this applies to Litecky Editing Services.

## Litecky Editing Services

Litecky Editing Services is a sole proprietorship. It belongs to its owner, who is another person. It is not co-owned. The Guardian is its administrator, with full authority over all technical and administrative decisions for Litecky. The Subsidiary Authority Specification §7.3 holds the record, by role. This record names no person. Names belong in the parent's registry.

- **The administrator decides.** For agents, every Litecky decision comes to the administrator.
- No agent contacts Litecky's owner, asks for her approval, or waits on it.
- What is hers to decide as the business owner (her money, her clients, her legal records, her name) the administrator takes to her himself and brings back the answer.
- The parent's registry is to keep a place for an owner governance role, unassigned. Nothing may assume it is filled.
- Litecky is a real boundary: it is another person's business and a separate legal entity from the rest of the estate. Its records, credentials and client data stay separate.

**The reading taken of "in both directions".** None of the retirements in this version applies to Litecky, except that of the audit series. No session from another organization reads into, writes to, reviews or merges in Litecky beyond what Litecky's own contract already allows. Litecky's sessions keep their present rules, including their rule about parent files. The rules of version 1.0 stand for Litecky as they stood. This is the conservative reading.

The same reading ends the parent's audits of Litecky. The parent does not read into Litecky to audit it, so the audit series of version 1.0 is retired for Litecky as for every organization. Litecky's part of the one check is run from inside Litecky, as the next section says.

Recording Litecky's owner here does not make her a Guardian and does not activate multi-human Council mode under GOV-006. No record shows that she has accepted governance authority in this estate, and nothing may assume it.

## One Check of the Five Real Things

One check replaces the audit series of version 1.0. For each organization it asks:

1. **Person and entity.** Is anything that belongs to another person or another legal entity recorded as someone else's? Did a session from another organization author in its repository, or a subsidiary session push to or merge in the parent's?
2. **Money.** Does it have one payer? Did any spend, bill or paid plan cross to another organization?
3. **Credentials.** Does it have its own machine identity and secret root? Does it authenticate to another organization's instance? Does an agent hold a provider credential? Is a value in a tracked file?
4. **Data and records.** Is any customer's or third party's data, or any tax, bank or address data, in an agent-readable file or in another organization's store?
5. **Public identity.** Do its public and customer-facing material and its legal documents carry its own name, brand and domains, free of parent names, role names and policy numbers beyond the permitted cross-references?

This policy sets what the check asks. The parent's operating standards own its procedure, its schedule and its record. Until they define one, the check exists only as this list, and nothing runs it.

Litecky's part of the check is run from inside Litecky, by Litecky's own session, for its administrator. It is reported value-blind: the report says how each of the five questions came out and carries no record, credential, client data or file content out of Litecky. Its administrator carries the report to the parent. No session from another organization reads into Litecky to run it.

## Implementation Boundary

This policy defines the boundaries and the evidence expected. This repository has no technical enforcement power. Router deployment, registry fields, the check's procedure and any automation are owned by the repositories that run them.

### What Refuses, and the Readback

Nothing mechanical in this repository enforces any rule in this policy. Each rule is a declared control unless its row names something that refuses.

| Rule | What refuses | Readback |
|------|--------------|----------|
| A subsidiary session reads parent files and does not author, push to or merge in the parent's repositories | Nothing. The parent's Agentic Workflow Standard records that sessions act through one GitHub login, so the provider cannot tell one organization's session from another's | The authoring session named on the pull request, and the review record on it |
| Authoring stays with the owning organization's sessions | Nothing, for the same reason | The same |
| Review and merge in a subsidiary's repository, by a parent agent or another subsidiary's agent, under the merge rule | A required status check refuses a red head where the repository has one. Whether it has one is a live fact to read back. The read by a non-author is not mechanical | The pull request shows the gate results, the review record and who merged |
| No session from another organization acts in Litecky beyond its contract | Nothing | Litecky's own repository history, read from Litecky's side |
| The administrator decides; no agent contacts Litecky's owner | Nothing | The record of each Litecky decision names the administrator |
| Own machine identity and secret root; no value crosses | Not established here. SEC-005 and the Secrets Management Specification name the intended controls. Whether one is live is a fact of the owning repository and its provider | The provider's own identity and token records |
| One payer per organization | Nothing in this repository | The provider's billing record |
| Legal-entity records out of agent-readable files | Nothing specific to these record classes | A search of tracked files, in the one check |
| Parent names, role names and policy numbers out of public, customer-facing and legal material | Nothing | A read of that material, in the one check |
| A record on the receiving side for what crosses a real boundary | Nothing | The receiving organization's own record |
| Each organization keeps its own GitHub organization, domain and zone | Nothing in this repository | The provider's own records: the organization on the code host, the domain's registration, and the zone |
| An agreement between two of the Guardian's own organizations keeps its terms: the cost owner and the data classes | Nothing | The agreement's record under the parent's Estate Agreements Standard |
| Litecky's part of the check is reported value-blind | Nothing | The report as its administrator carries it to the parent: how each of the five questions came out, and nothing else |
| The owner governance role for Litecky is unassigned | Nothing | Litecky's entry in the parent's registry |

What a session may do follows from where it starts:

| Session started in | Reads | Authors | Reviews and merges |
|--------------------|-------|---------|--------------------|
| The parent | Parent files; any subsidiary's repository except Litecky's | Parent repositories only | Parent repositories, and any subsidiary's repository except Litecky's, under the merge rule |
| A subsidiary other than Litecky, at its shell or in a project | Its own files; parent files, and parent pull requests, on which it may comment; any other subsidiary's repository except Litecky's | Its own organization's repositories only | Its own repositories, and any other subsidiary's except Litecky's, under the merge rule. In the parent's it may comment and does not merge |
| Litecky | As Litecky's own contract says. Its present rules stand | Litecky's repositories only | As Litecky's own contract says |

The router at `~/Organizations/CLAUDE.md` sends a session to its own organization's contract. Its canonical form is maintained as `.org/templates/organizations-router-claude-md.template` in the parent's repository and deployed to that path. The Subsidiary Authority Specification §8 states what it must and must not say.

### Validation

- **The one check of the five real things.** Not automated. Its schedule is the parent's to set.
- **Retired for every organization, Litecky included:** the contamination scan, the restatement drift review and the router integrity check of version 1.0.

### Human Process

1. **New organization onboarding**: The parent registers the organization. The organization's own session authors its contract, which may cite parent standards by version. The one check is run for it.
2. **Standard publication**: The parent publishes a standard with a version. It sets no deadline and keeps no log of adoption. A subsidiary's own session decides whether and when to cite the new version.
3. **A finding from the check**: The finding goes directly to a session of the organization that owns the thing found, which corrects it in its own repository. A finding about a credential, money or a legal-entity record goes to the Guardian. A finding in Litecky stays in Litecky: its own session takes it to the administrator.

## Sensitive Metadata Placement

This section stays as it was in version 1.0, except for its last paragraph. Sessions may now read across organizations, so "an agent's default context chain" is read as any agent-readable file, which is how the decision states the rule.

Subsidiary legal and financial metadata — EIN, entity numbers, formation receipts, bank account details, tax filing deadlines, physical addresses — **must not** be placed in files discoverable through an agent's default context chain. Subsidiaries must:

- Maintain a public operational metadata file (e.g., `.subsidiary.yaml` or equivalent) containing only routing-level fields: display name, parent relationship indicator, governance level (per the subsidiary's own restatement), owned domains, GitHub org reference, billing labels.
- Store legal and financial metadata in the subsidiary's approved secrets authority. On the managed Guardian workstation, local reads use 1Password (`op read`); runtime and CI reads use the repo's approved managed backend (currently Infisical for remote, provider-agnostic per SEC-005 and the Secrets Management Specification).

This rule is carried by secrets policy, not by repo structure; nothing in this repository enforces it. A subsidiary's public metadata file falls under Boundary 5 where it is public; a subsidiary's private legal record is governed by the Secrets Management Specification.

## Multi-Organization Strategy

This section stays as it was in version 1.0, except for the Litecky line and the two notes on live facts and seats.

Each subsidiary operates its own GitHub organization (established in ADR-004 and refined here per ADR-007):

- **`happy-patterns-org`** — Happy Patterns LLC; two-seat teams plan with members `verlyn13` and `happy-patterns`
- **`jefahnierocks`** — Personal creative work
- **`litecky-editing`** — Litecky Editing Services: another person's sole proprietorship, administered by the Guardian
- **`seven-springs`** — Sandbox

Slugs, plans and members are live facts, and the parent's registry is their record. The Identity and Account Management Specification records the Seven Springs locator as `seven-springs-org`.

Parent seats in subsidiary GitHub orgs are held only where required by shared infrastructure responsibilities (currently: the Citadel automation GitHub App). Human parent seats in subsidiary orgs are not retained by default.

This version changes no seat, membership or installation.

## Compliance Verification

**Automated:**
- None in this repository.

**Manual:**
- The one check of the five real things, on the schedule the parent's operating standards set
- For Litecky, its part of the one check, run from inside Litecky by its own session and reported value-blind

**Reporting:**
- Findings are recorded where the parent's operating standards say. This policy names no path.
- Restatement status is no longer tracked per subsidiary, except for Litecky.

## Known Exceptions

| Exception | Reason | Review Trigger |
|-----------|--------|----------------|
| Litecky Editing Services | Another person's business. None of this version's retirements applies, except that of the audit series | A change to Litecky's own contract, which the administrator decides |
| Legal documents | An operating agreement, a tax filing or a contract may name another entity where the document requires it | Always; a document that carries legal-entity records stays out of agent-readable files |
| Break-glass writes across organizations | Emergency authority under GOV-003, unchanged | Per GOV-003 |
| Structural single-Guardian approvals | Current single-natural-person path under GOV-006 may reference both entities in decision records; multiple accounts count once | No expiry or synthetic-council trigger; multi-human mode requires a later Covenant amendment based on distinct natural persons |

## What This Replaces

Version 1.0 is this file as it stood at commit `d19b79a` of this repository. Its rule numbers resolve as follows. Every row marked "stands for Litecky" is unchanged for Litecky Editing Services.

| Version 1.0 | Version 2.0 |
|-------------|-------------|
| Invariant 1, Identity Isolation: forbidden identifiers in any subsidiary-scoped artifact | Retired for agent-facing files. Kept only for public and customer-facing material and legal documents (Boundary 5). Stands for Litecky |
| Invariant 2, Authority Restatement: adopt only by restating, with a restatement obligation on each parent change | A subsidiary may cite a parent standard by version and restates only where it changes the rule. No clock, no parent-side log. Stands for Litecky |
| Invariant 3, Spec Flow, Not Session Flow: a subsidiary session must not traverse into parent files; guidance crosses only by relay | A subsidiary session may read parent files and must not write them: it does not author, push to or merge there. Sessions hand off directly; a record is kept only across a real boundary. Stands for Litecky |
| Forbidden-Identifier Contamination Check | Replaced by the one check of the five real things, for every organization. Litecky's part is run from inside Litecky |
| Automated Validation: contamination scan, restatement drift review, router integrity check | Replaced by the one check, for every organization, Litecky included |
| Human Process 1 to 3: onboarding by migration packet, restatement deadlines per subsidiary, contamination findings as parent-authored pull requests | Rewritten under [Human Process](#human-process). A parent agent no longer authors the correcting pull request |
| Exception: parent agents may read subsidiary repositories for audit; no parent write except by explicit cross-entity approval | A parent agent may read, review and merge in a subsidiary's repository under the merge rule, and does not author there. None of it applies in Litecky, which the parent does not read into even to audit |
| Exception: the registry is not read by subsidiary-scoped agents | Retired with Invariant 3. Stands for Litecky's sessions |
| Exceptions: Guardian-approved cross-entity coordination artifacts and cross-entity audit artifacts live at the parent, never inside a subsidiary repository | No longer exceptions, because an agent-facing file may name both organizations. Billing, legal and security matters cross Boundaries 2 to 4 and need the receiving organization's own record. Stand for Litecky |
| Sensitive Metadata Placement | Unchanged |
| Multi-Organization Strategy | Unchanged, except that Litecky is recorded as a sole proprietorship with an owner and an administrator, not as co-owned |
| Not in version 1.0: two-sided acceptance of an agreement between organizations (the parent's Estate Agreements Standard) | The terms stay; the acceptance ceremony goes. Stands with Litecky |

## Related Documents

- **Source Principles:**
  - [Principle 5: Infrastructure as Code](../PRINCIPLES.md) — Organization structure, registry, and router template are versioned artifacts
  - [Principle 6: No Committed Secrets](../PRINCIPLES.md) — Credential values and legal-entity records stay out of tracked, agent-readable files
  - [Principle 9: Zero Trust](../PRINCIPLES.md) — A boundary is kept where it can be checked: who holds a credential, who pays, where a record lives. A rule nothing checks is named a declared control
  - [Principle 10: Least Privilege](../PRINCIPLES.md) — Each organization has its own machine identity and secret root, and values never cross
  - [Principle 15: Three Circles of Trust](../PRINCIPLES.md) — Parent standards (authority), the subsidiary's own contract (adoption, by citation or restatement), project work (execution)
  - [Principle 16: Living Law](../PRINCIPLES.md) — The text-separation rules came from an earlier moment; this version changes them from operating experience
- **Related Policies:**
  - [AGT-001: Agent Governance](./agt-001-agent-governance.md) — Agent boundary rules, including the organization boundary
  - [GOV-002: Covenant Amendment Process](./gov-002-amendment-process.md) and [GOV-006: Council Decision Quorum](./gov-006-decision-quorum.md) — How this version was decided
  - [GOV-003: Break-Glass Procedures](./gov-003-break-glass.md) — Emergency override for writes across organizations
  - [SEC-005: Machine Identity](./sec-005-machine-identity.md) — Machine identity boundary between parent and subsidiary automation
- **Specifications:**
  - [Subsidiary Authority Specification](./specs/subsidiary-authority.md) — Operational detail, ownership model, per-organization record
  - [Secrets Management Specification](./specs/secrets-management.md) — Storage rules for sensitive subsidiary metadata
- **Architecture:**
  - [ADR-004: Federated Multi-Org Architecture](../docs/architecture/004-federated-multi-org-architecture.md) — Established the multi-org structure
  - [ADR-007: Subsidiary Authority and Identity Isolation](../docs/architecture/007-subsidiary-authority-and-identity-isolation.md) — Decision record for version 1.0; superseded in part by ADR-009
  - [ADR-009: Real Boundaries Between Organizations](../docs/architecture/009-real-boundaries-between-organizations.md) — Decision record for version 2.0
- **Standards:**
  - [Agentic Workflow Standard](../../.org/standards/agentic-workflow.md) — One-Human Operating Contract: the merge rule and the reserved list
  - [Subsidiary Governance Standard](../../.org/standards/subsidiary-governance.md) — Session routing mechanics
  - [Estate Agreements Standard](../../.org/standards/estate-agreements.md) — Agreement terms between organizations
- **Parent-owned implementation references:**
  - `.org/iam/federation/subsidiaries.yaml` — Subsidiary registry
  - `.org/templates/organizations-router-claude-md.template` — Router canonical source
  - `OWNER-DIRECTIONS.md` — The Guardian's standing directions

## Change History

- **2026-04-20** (1.0) — Initial creation establishing the three invariants (identity isolation, authority restatement, spec flow) per ADR-007; implements Principles 5, 9, 10, 15; pairs with the Subsidiary Authority Specification and the Subsidiary Governance Standard.
- **2026-08-29** (1.0, unversioned edit) — The Known Exceptions row for single-Guardian approvals was reconciled to GOV-006 in the pull request that made single-Guardian mode structural. No date or version was recorded then; it is recorded here.
- **2026-11-15** (2.0) — Amended to the five real boundaries per ADR-009, on the Guardian's decision under GOV-006 structural single-Guardian mode. Retired the three invariants as rules about agent-facing text, the restatement clock and hand-carried relay for every organization except Litecky Editing Services, and the audit series for every organization. Allowed a parent agent, and an agent of another subsidiary, to read, review and merge in a subsidiary's repository under the merge rule, with authoring kept to the owning organization's sessions; a subsidiary session reads parent files and does not author, push to or merge there. Recorded Litecky as another person's sole proprietorship that the Guardian administers. Restated that separate organizations, domains and zones, separate secret roots, one payer each, and legal-entity records out of agent-readable files stay as they are. Retitled; implements Principles 5, 6, 9, 10, 15, 16.
- **2026-11-15** (2.0.1) — Wording corrected after the independent read of version 2.0, with no change of rule. The record names no person. The registry's place for an owner governance role is stated as to be kept. A subsidiary session may comment in the parent's repositories and does not merge there. The merge rule is cited from the parent's standard and no longer restated. The Litecky exception to reading is stated in the sentence it limits. Litecky's report reaches the parent carried by its administrator. Readback rows are added for the separate organization, domain and zone, for agreement terms, for the value-blind report and for the unassigned role. The sensitive-metadata rule is described as carried by secrets policy, not enforced here.
