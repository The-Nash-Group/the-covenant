# Subsidiary Authority Specification

**Version:** 2.0.0
**Status:** ACTIVE
**Date:** 2026-11-15
**Implements:** Principle 5 (Infrastructure as Code), Principle 6 (No Committed Secrets), Principle 9 (Zero Trust), Principle 10 (Least Privilege), Principle 15 (Three Circles of Trust), Principle 16 (Living Law)
**Policies:** ORG-001 (Subsidiary Authority and Real Boundaries), AGT-001 (Agent Governance), GOV-003 (Break-Glass), GOV-006 (Decision Quorum), SEC-005 (Machine Identity)

---

## Purpose

Define how authority, identity, and session context are distributed across the three tiers of The Nash Group's organizational structure — parent, subsidiary, and project — independent of which subsidiary is being described.

This specification does not duplicate ORG-001. ORG-001 defines the rule: the five real boundaries, the two conditions, and what is not a boundary. AGT-001 defines agent boundary rules. SEC-005 defines machine identity boundaries. This specification fills the gap those policies leave: the operational ownership matrix, the onboarding and offboarding flow, how a subsidiary adopts a parent standard, the per-subsidiary record, and the router contract.

> **Current-state note (2026-11-15):** Version 2.0.0 brings this specification into agreement with ORG-001 version 2.0 (ADR-009). It does not amend the parent's operating standards, the router template, the registry, or any organization's own contract. Each of those is changed in its own repository by its own pull request, and until then still carries the earlier rule. Section numbers are those of version 1.0 so that earlier citations resolve; a section that replaces an earlier rule says so. §7 is a dated record and is marked stale where it is.

---

## Governing Principles

| Principle | How This Specification Implements It |
|-----------|--------------------------------------|
| **Principle 5: Infrastructure as Code** | Subsidiary structure, the registry, and the parent router are versioned artifacts under `.org/iam/federation/subsidiaries.yaml` and `.org/templates/organizations-router-claude-md.template`; no subsidiary structural state exists only as runtime configuration |
| **Principle 6: No Committed Secrets** | Credential values and legal-entity records stay out of tracked, agent-readable files (§6) |
| **Principle 9: Zero Trust** | A boundary is kept where it can be checked: who holds a credential, who pays, where a record lives. A rule that nothing checks is named a declared control, not an enforced one |
| **Principle 10: Least Privilege** | Each organization has its own machine identity and secret root, and values never cross |
| **Principle 15: Three Circles of Trust** | Parent standards are L0 (authority), the subsidiary's own contract is L1 (adoption, by citation or restatement), project work is L2 (execution); the three tiers map directly |
| **Principle 16: Living Law** | The text-separation rules of version 1.0 came from an earlier moment; this version changes them from operating experience |
| **ORG-001: Subsidiary Authority** | This specification is the operational counterpart to ORG-001; ORG-001 defines the boundaries, this specification defines how they are realized per subsidiary |
| **AGT-001: Agent Governance** | The agent boundary at the organization edge is declared here and cross-referenced from AGT-001 |

---

## 1. The Three Tiers

### 1.1 Tier Definitions

| Tier | Name | Authority | Location |
|------|------|-----------|----------|
| **L0** | Parent | Publishes standards, specs and principles; governs by exception; holds cross-entity concerns | `~/Organizations/the-nash-group/` |
| **L1** | Subsidiary | Owns its own contract, governance artifacts, brand, voice, CI and seats. Its contract may cite a parent standard by version, and restates a rule only where it changes the rule | `~/Organizations/<subsidiary>/` (shell) + subsidiary's own GitHub organization |
| **L2** | Project / Dev Agent | Owns code, tests, project docs, build and deployment flow, under its organization's contract | `~/Organizations/<subsidiary>/apps/<project>/` and corresponding subsidiary-org repo |

Version 1.0 said a project "sees only L1 identity". That is retired for every organization except Litecky Editing Services: a subsidiary or project session may read parent files and must not write them (ORG-001).

### 1.2 What Each Tier Owns

Authority is allocated per tier. No artifact is owned by more than one tier except where explicitly noted. An artifact is authored only by sessions of the organization that owns it.

**Parent (L0) owns:**

| Artifact Class | Examples |
|----------------|----------|
| Specs | `the-covenant/policies/specs/*.md` |
| Principles & governance policies | `the-covenant/PRINCIPLES.md`, `the-covenant/policies/*.md` |
| ADRs | `the-covenant/docs/architecture/*.md` |
| Cross-cutting standards | `.org/standards/*.md` |
| Templates | `.org/templates/*` |
| Shared infrastructure | `the-citadel` OpenTofu/IaC workspaces; exact layout is Citadel-owned |
| Parent orchestration | `.claude/orchestration/` |
| Subsidiary registry | `.org/iam/federation/subsidiaries.yaml` |
| Cross-entity concerns | Billing label taxonomy, dependency governance tiers (L0/L1/L2 per Principle 15), audit requirements, break-glass procedures |

**Subsidiary Authority (L1) owns:**

| Artifact Class | Examples |
|----------------|----------|
| Subsidiary shell CLAUDE.md | `~/Organizations/<subsidiary>/CLAUDE.md` (authored by the subsidiary's own sessions) |
| Subsidiary shell README.md | `~/Organizations/<subsidiary>/README.md` |
| Subsidiary public metadata | `.subsidiary.yaml` or equivalent — routing-level fields only |
| Its own contract | Citations of parent standards by version; its own rules where it changes or adds to them |
| Team structure | GitHub org teams, branch protection, CI/CD workflows within the subsidiary's GitHub org |
| Brand and voice | Subsidiary's own identity, naming, terminology |
| Subsidiary agents | Any dev-agent contracts, role definitions, and session-scoping rules specific to the subsidiary |

**Project (L2) owns:**

| Artifact Class | Examples |
|----------------|----------|
| Code and tests | All source, test, and build artifacts |
| Project CLAUDE.md | `apps/<project>/CLAUDE.md` with project-specific context |
| Project AGENTS.md | Optional, when definition-of-done or multi-language detail warrants it |
| Build/test/deploy commands | `justfile`, `package.json` scripts, Gradle tasks, etc. |
| Contribution workflow | Project's own PR template, CODEOWNERS, review rules |

### 1.3 Cross-Tier Authority

Some concerns legitimately span tiers. The spec names them explicitly to prevent creep:

| Concern | Owner | How It Crosses |
|---------|-------|----------------|
| The Citadel GitHub App automation identity | Parent (L0) by registration; installed in each subsidiary's GitHub org | SEC-005 defines the single-app, multi-installation pattern; parent holds the app, subsidiaries accept the installation |
| Billing labels | Parent (L0) defines the taxonomy; subsidiaries (L1) apply to their own cloud resources | Taxonomy published as a Nash-authored standard; subsidiaries cite it, or restate it where they change it, and apply |
| Cloudflare zones | Parent controls the transitional stewardship account (per the Cloudflare Ownership Transition spec); workspace root owns per-zone resources | Transitional; long-term goal is per-subsidiary Cloudflare account separation |
| Reading, review and merge across organizations | A parent agent in a subsidiary's repository, and an agent of one subsidiary in another subsidiary's. Never in Litecky's | Under the merge rule of ORG-001: gates green on the exact head, and a recorded read by an agent that did not author it. Authoring stays with the owning organization's sessions. A subsidiary's agent may read parent files and comment on a parent pull request; it does not author, push to or merge in the parent's repositories. Break-glass under GOV-003 is unchanged |

The last row replaces the version 1.0 row "Audit and drift detection", under which the parent could read a subsidiary's repositories for audit and could not write to them except by break-glass.

### 1.4 Semantic Ownership vs Operational Hosting

Authority follows semantic ownership even when current hosting is transitional.

| Term | Meaning | Example |
|------|---------|---------|
| Semantic owner | Entity that owns governance, billing label, long-term GitHub/IaC placement, secrets boundary, and agent context | Happy Patterns LLC owns `scopecam`; Jefahnierocks owns personal projects |
| Operational host | Current place where repository, GitHub features, Cloudflare resources, CI, or runtime infrastructure live | A personal project may remain in lower-cost hosting while paid Jefahnierocks org features are deferred |
| Long-term home | Target authority boundary once migration triggers are met | Active Happy Patterns product work belongs under `happy-patterns-org`; active Jefahnierocks work converges on the Jefahnierocks boundary |

A temporary semantic-owner / operational-host mismatch is permitted only when the parent-scoped registry or orchestration record names:

1. semantic owner
2. current operational host
3. intended long-term home
4. migration trigger
5. controls and claims that remain pending while hosting is transitional

Transitional hosting must not be used to route subsidiary work through parent or global roots as an ownership shortcut.

---

## 2. What Must Not Cross the Boundary

ORG-001 version 2.0 names five real boundaries: another person's interest or a separate legal entity; money; credentials and secret authority; customers' and third parties' data and legal-entity records; public identity. Nothing crosses one without the receiving organization's own record, and credentials never cross.

This section holds the operational detail for the parts that version 1.0 covered here.

### 2.1 Names in Public, Customer-Facing and Legal Material

(Formerly "Forbidden Identifiers in L1 and L2 Artifacts".)

Per ORG-001 Boundary 5, the following must not appear in a subsidiary's public and customer-facing material or in its legal documents, subject to the permitted cross-references of §2.2. They may appear in agent-facing files. The list is that of version 1.0; version 2.0.0 changes only where it applies.

For Litecky Editing Services the version 1.0 rule stands: the list applies to every file a Litecky session reads during normal operation.

| Category | Examples |
|----------|----------|
| Parent entity name | "The Nash Group", "Nash Group", "TNG" |
| Three-pillar archetypes | "Covenant", "Citadel", "Nexus", "Shield", "Tartan" — when used as governance or architecture names |
| Guardian archetypes | "Philosopher", "Architect", "Judge", "Gardener", "Explorer" — when used as governance roles |
| Governance tier names | "Immortals", "Mentors", "Watchers" |
| Principle numbers | "Principle 5", "Principle 9", direct references to `the-covenant/PRINCIPLES.md` |
| ADR references | "ADR-001", "ADR-004", direct paths into `the-covenant/docs/architecture/` |
| Parent policy IDs | SEC-xxx, GOV-xxx, INF-xxx, OPS-xxx, AGT-xxx, ORG-xxx, etc., when used as governing rules |
| Parent-assigned subsidiary prefixes | Any two-letter code assigned by the parent registry (subsidiaries use their full name in their own artifacts) |
| Parent directory references | Paths like `the-covenant/`, `the-citadel/`, `the-nexus/`, `the-shield/`, `the-tartan/` |

### 2.2 Permitted Cross-References

- **Legal documents** (operating agreements, tax filings, formation receipts) may name both entities where the document requires it. They carry legal-entity records, so they belong in paths that agents do not read (e.g., `business/` directory in the subsidiary).
- **Public-facing press and marketing** may describe a subsidiary's relationship to its parent holding company; these artifacts should live in public-content paths (e.g., `public/` or `site/content/`).
- **Agent-facing files** may carry any cross-reference, in every organization except Litecky.
- **Records authored by parent sessions** may reference subsidiaries by name. They live in the parent's repositories, because a parent agent does not author in a subsidiary's.
- **The parent router at `~/Organizations/CLAUDE.md`** names subsidiaries because its function is routing. See §8.

### 2.3 What a Subsidiary Session May Read and Must Not Write

(Formerly "What Subsidiary Agents Must Not Read".)

A session started inside a subsidiary may read, and must not write:

- `~/Organizations/the-nash-group/` and any files within it
- `.org/` within the Nash repo
- `the-covenant/`, `the-citadel/`, `the-nexus/`, `the-shield/`, `the-tartan/` within the Nash repo
- `.claude/orchestration/` within the Nash repo
- The parent router at `~/Organizations/CLAUDE.md`

"Write" is read conservatively, and this is the reading taken: a subsidiary session does not author, push to or merge in the parent's repositories. It may read and comment on a parent pull request.

Reading does not reach what Boundaries 3 and 4 keep out of agent-readable files: credential values, customers' and third parties' data, and legal-entity records.

A session started in Litecky keeps the version 1.0 rule. It does not traverse into any of these.

The Subsidiary Governance Standard (`.org/standards/subsidiary-governance.md`) defines the mechanics.

---

## 3. Adoption: Citation and Restatement

(Formerly "Restatement Workflow".)

A subsidiary adopts a parent standard in its own contract, by its own session, in one of two ways:

- **Citation.** It cites the standard by name and version. The cited version is the rule in that subsidiary until its own session changes the citation.
- **Restatement.** Where it changes the rule, it writes its own rule and names the parent standard and version it departs from.

The parent does not block on adoption and does not track it. A subsidiary's contract stays its own document in its own repository.

For Litecky Editing Services the version 1.0 workflow stands, as §3.1 to §3.3 record it.

### 3.1 Cadence

(Formerly "Restatement Cadence".)

There is no clock. A subsidiary's own session decides whether and when to cite a new version.

The deadlines of version 1.0 are retired for every organization except Litecky. They are kept here because they stand for Litecky and so that citations of this section resolve:

| Spec Change Type | Version 1.0 Restatement Deadline (Litecky only) |
|------------------|--------------------------------|
| New required spec | 90 days from parent publication to subsidiary's own restated policy being in effect |
| Major revision (semantic change to a rule) | 60 days |
| Minor revision (clarification, typo, additional example) | Discretionary; restate at next routine review |
| Security-critical spec (SEC-xxx) | 30 days; parent may issue a Guardian directive compressing this further |
| Break-glass or emergency (GOV-003) | Immediate; out-of-band coordination |

Break-glass and emergency coordination under GOV-003 are unchanged for every organization.

### 3.2 Requirements

(Formerly "Restatement Requirements".)

A citation names the standard and its version.

A restatement states the changed rule and names the parent standard and version it departs from. A subsidiary may add constraints of its own.

The five requirements of version 1.0 are retired for every organization except Litecky. For Litecky a restated policy must still:

1. Be authored in the subsidiary's own voice.
2. Use the subsidiary's own policy identifier (if it uses IDs) or its own natural-language reference.
3. Capture the functional intent of the parent spec, not its literal wording.
4. Reference principles or rationale on the subsidiary's own authority (the subsidiary restates the *reasons* for the rule, not by quoting parent rationale).
5. Record the parent spec version it was restated from, in a Nash-scoped metadata file (not in the subsidiary's dev-agent-facing artifact) so drift can be detected.

### 3.3 Drift

(Formerly "Drift Detection".)

The parent runs no drift review for any organization, Litecky included: it does not read into Litecky to audit it. It keeps no restatement log, except Litecky's rows. Whether a cited version is behind the parent's current one is read from the two files.

The existing log at `.claude/orchestration/subsidiary-authority-migration/restatement-log.md` is a parent record. This specification no longer requires it for any organization except Litecky; what becomes of its other rows is the parent's to record.

For Litecky:

- Each row, as in version 1.0: parent spec, parent version, subsidiary, subsidiary's restated policy identifier, restated-from version, last review date
- The semi-annual parent review of version 1.0 is retired. The parent fills Litecky's rows only from what Litecky's own session reports
- A finding is taken up in Litecky's own repository by its own session. The administrator decides it

### 3.4 What Happens When a Subsidiary Does Not Adopt

A subsidiary may decline to adopt a parent standard if it is not compatible with its own operating model. It records the decline in its own contract. Decline paths:

- **Functional decline**: subsidiary authors its own equivalent with different operational content (permitted).
- **Scope decline**: subsidiary asserts the standard does not apply to its domain (permitted).
- **Full decline**: subsidiary rejects the standard outright. This is a governance question for the Guardian.

There is no parent-side decline log, except as the version 1.0 log stands for Litecky.

A decline does not reach the five real boundaries. ORG-001 applies to every organization, whatever it cites.

---

## 4. Subsidiary Onboarding

When a new subsidiary is added:

1. **Parent registers** the subsidiary in `.org/iam/federation/subsidiaries.yaml` with: display name, legal entity type, GitHub org reference, owned domains, governance level at which the subsidiary operates by default, billing labels. Version 1.0 also required `agent_isolation_required: true`. This specification no longer requires that field; the registry's own schema says whether it remains.
2. **A parent session hands off** directly to the new subsidiary's session, naming the parent standards it may cite. The migration packet of version 1.0 is no longer required.
3. **The subsidiary's own session authors** its CLAUDE.md, README.md, and public subsidiary metadata. It cites parent standards by version and restates only where it changes a rule. A parent agent does not author these files.
4. **Subsidiary establishes or records** its GitHub organization boundary. If paid org features are justified, the subsidiary uses its own plan, team structure, branch protection, and CI. If paid features are deferred, the registry records semantic owner, current operational host, long-term home, and migration trigger under §1.4. Parent provides the Citadel automation GitHub App installation when the subsidiary boundary is active.
5. **The one check of the five real things** (ORG-001) is run for the new subsidiary: its own GitHub organization, domain and zone; its own secret root; one payer; sensitive metadata stored per §6; a public identity of its own. The router at `~/Organizations/CLAUDE.md` sends its sessions to its own contract.

## 5. Subsidiary Offboarding

When a subsidiary is retired or spun out:

1. **Parent marks** the subsidiary as `status: retiring` in the registry with a target date.
2. **Parent and subsidiary** coordinate disposition of: subsidiary's GitHub org (retain, hand off, archive, or delete), subsidiary's domains (transfer or release), subsidiary's infrastructure (migrate out of shared tooling), Citadel automation installation (remove).
3. **Parent removes** the subsidiary directory from `~/Organizations/` once disposition is complete; the subsidiary's own git history and artifacts remain authoritative wherever they live post-offboarding.
4. **Registry update**: the entry transitions to `status: retired` with a final disposition note; record is retained for audit.

---

## 6. Sensitive Metadata Placement

This section is unchanged in version 2.0.0. Sessions may now read across organizations, so "an agent's default context chain" is read as any agent-readable file, as in ORG-001 version 2.0.

Per ORG-001, subsidiary legal and financial metadata must not live in files discoverable through an agent's default context chain.

### 6.1 Classification

| Metadata Class | Examples | Placement |
|----------------|----------|-----------|
| **Public operational** | Display name, parent relationship indicator, GitHub org reference, governance level (per subsidiary's own restatement), owned domains, billing labels, team references | Subsidiary's public metadata file (e.g., `.subsidiary.yaml`) — versioned in the subsidiary's repo |
| **Confidential legal** | EIN, entity registration numbers, formation receipt numbers, filing fees, registered agent, formation date | Subsidiary's approved secrets authority; local reads via 1Password `op read`, runtime/CI via repo's managed backend |
| **Confidential financial** | Bank account details, tax filing deadlines, invoice milestones, tax classification specifics, NAICS specifics | Subsidiary's approved secrets authority |
| **Confidential physical** | Physical business address (if different from public) | Subsidiary's approved secrets authority or a separate non-git-tracked business records path |

### 6.2 Migration

Existing subsidiaries with confidential metadata in their `.subsidiary.yaml` files (inspection as of 2026-04-20 shows this condition in `~/Organizations/happy-patterns/.subsidiary.yaml`) must migrate:

1. Identify confidential fields per §6.1.
2. Move to the subsidiary's secrets authority.
3. Remove from the git-tracked metadata file.
4. Purge from git history via a history rewrite (coordinate with subsidiary's own history-rewrite procedure; out of scope for this spec).

Migration is tracked per subsidiary in the Subsidiary Authority migration campaign.

---

## 7. Current-State Assessment by Subsidiary

> **Staleness note (2026-11-15).** §7.1, §7.2 and §7.4 were last assessed on the dates they carry: 2026-04-20, with the Jefahnierocks rows updated to 2026-05-02. They are kept as a dated record, not as current state. The parent's restatement drift review for the second half of 2026 recorded, as finding F-C2, that rows here no longer matched what it read. Nothing in those three sections was re-read for version 2.0.0, and no new fact is stated in them. §7.3 is rewritten because the Guardian corrected Litecky's ownership.
>
> Version 2.0.0 also retires some of the targets these rows name. A target of "own voice, no Nash identifiers", or of a router that keeps parent naming out of a subsidiary session, is no longer a target for any organization except Litecky (ORG-001 version 2.0).

As of 2026-04-20, the state of each subsidiary against version 1.0 of this specification:

### 7.1 Happy Patterns LLC

**Stale.** Finding F-C2 records that the shell rewrite rows and the public metadata file row were contradicted by the subsidiary content that review read. The shell and router targets are retired. The same dated inspection appears in §6.2.

| Aspect | Current | Target | Delta |
|--------|---------|--------|-------|
| GitHub organization | `happy-patterns-org` (own org, two-seat teams plan with `verlyn13` and `happy-patterns`) | Same | None |
| Project ownership | `scopecam` is a Happy Patterns LLC project | Same | None |
| Primary domain | `happy-patterns.com` (also owns `happy-patterns.co`, landing page pending) | Same | None |
| Subsidiary shell CLAUDE.md | Nash-framed ("subsidiary of The Nash Group", inheritance language) | Authored in Happy Patterns' own voice, no Nash identifiers | Full rewrite needed |
| Subsidiary shell README.md | Nash-framed | Authored in Happy Patterns' own voice | Full rewrite needed |
| Public metadata file | `.subsidiary.yaml` contains EIN, formation receipt, bank deadlines, address — violates §6 | Routing fields only | Extract confidential fields to secrets authority; purge from git history |
| Project-level artifacts | `apps/scopecam/CLAUDE.md` and `AGENTS.md` — clean, no Nash identifiers | Same | None |
| Parent router behavior | `~/Organizations/CLAUDE.md` routes HP sessions into Nash governance naming | Router directs into HP's own CLAUDE.md; no parent naming pulled into HP session | Router template deployment required |

### 7.2 JefahnieRocks (Personal/Creative)

**Dated.** Last updated 2026-05-02. Not re-read. The "own voice" rows are no longer targets.

| Aspect | Current | Target | Delta |
|--------|---------|--------|-------|
| GitHub organization | `jefahnierocks` exists as the intended Free-tier boundary; paid Team-style features are deferred | Use paid org features only when collaboration, compliance, billing, or automation requires them | Track semantic ownership separately from current operational hosting |
| Subsidiary shell repository | Private repo `jefahnierocks/jefahnierocks` exists at initial commit `b3c05716f581138d5fed4088166936e52b11f63d` | Shell repo remains shell-only; child project repos stay independent | None; keep low-frequency and public/private posture subsidiary-owned |
| Primary domain | `jefahnierocks.com` | Same | None |
| Subsidiary shell CLAUDE.md | Authored in own voice | Same | None |
| Subsidiary shell README.md | Authored in own voice | Same | None |
| Public metadata file | `.subsidiary.yaml` intentionally removed; no Jefahnierocks-owned consumer exists yet | Recreate only if a Jefahnierocks-owned consumer exists and keep it public-metadata only | No current file required |
| Project-level artifacts | Various personal projects; some may remain in lower-cost hosting while semantically classified as Jefahnierocks-owned | Clean, Jefahnierocks-owned artifacts once moved into the subsidiary boundary | Per-project audit; record current host and move trigger |

### 7.3 Litecky Editing Services

Rewritten 2026-11-15 from the Guardian's correction of 2026-11-14. The correction supersedes every earlier record of Litecky's ownership, including the "co-owned" entry in the parent's registry and the Litecky paragraph of his answer on the decision issue named in ADR-009. His standing word is kept in the parent's `OWNER-DIRECTIONS.md`; check for the entry there. Personal names are not recorded in this repository. The parent's registry holds them.

| Aspect | Record |
|--------|--------|
| Legal form | Sole proprietorship. It is not co-owned |
| Owner | Its owner, a sole proprietor, who is another person |
| Administrator | The estate's owner, as its administrator, with full authority over all technical and administrative decisions for Litecky |
| Decisions | The administrator decides. For agents, every Litecky decision comes to him. No agent contacts the owner, asks for her approval, or waits on it. What is hers to decide as the business owner (her money, her clients, her legal records, her name) he takes to her himself and brings back the answer |
| Owner governance role | A place is held open for it in the parent's registry. It is unassigned. Nothing may assume it is filled |
| Boundary | Real, in both directions (ORG-001). Litecky is another person's business and a separate legal entity from the rest of the estate. Its records, credentials and client data stay separate. None of the version 2.0.0 retirements applies, except that of the audit series; the version 1.0 rules stand |
| Check | The parent does not read into Litecky to audit it. Litecky's part of the one check of the five real things is run from inside Litecky by its own session, for its administrator, and reported value-blind |
| GitHub organization | `litecky-editing` (own org) |
| Primary domain | **Stale.** This row said "TBD per ADR-004". The parent's registry is the record of Litecky's domains |
| Subsidiary shell artifacts | **Stale.** This row said "Not yet assessed in this cycle", and finding F-C2 records that as contradicted. The Identity and Account Management Specification records a Litecky-authored restatement dated 2026-07-13 as the one known to the parent. Not re-read here: no session from another organization reads into Litecky beyond what its own contract already allows |

### 7.4 Seven Springs (Sandbox)

**Stale.** Finding F-C2 records that the organization slug is not `seven-springs`. The Identity and Account Management Specification gives the locator as `seven-springs-org` and records the entity as a dormant placeholder. The isolation row and its pedagogical exception are moot, because the rule they excepted is retired.

| Aspect | Current | Target | Delta |
|--------|---------|--------|-------|
| GitHub organization | `seven-springs` (own org) | Same | None |
| Purpose | Sandbox, synthetic | Same | None |
| Isolation requirement | Lower — sandbox purpose permits mixed references where clearly pedagogical | Document the sandbox exception explicitly | Minor: add pedagogical-exception annotation |

---

## 8. The Router Contract

The parent router at `~/Organizations/CLAUDE.md` sends a session to its own organization's contract. In version 1.0 it was the enforcement point for the rule that a subsidiary session must not read parent files. That rule is retired for every organization except Litecky. The router lives outside any git repo on disk but its canonical source is Nash-authored.

### 8.1 Canonical Source

- Template: `.org/templates/organizations-router-claude-md.template`
- Deployed to: `~/Organizations/CLAUDE.md`
- Deployment: manual copy or a simple Guardian script; versioning via the Nash repo's git history

### 8.2 Router Requirements

The router must:

1. Send each session to its own organization's contract first.
2. Include a routing table that names organizations by display name and points to their own CLAUDE.md paths.
3. For a session started in Litecky, keep the version 1.0 instruction: read Litecky's own contract and do not traverse into parent files.

The router must not:

1. Tell a subsidiary session, other than Litecky's, that it may not read parent files.
2. Tell any subsidiary session that it may author, push to or merge in the parent's repositories.
3. Tell a session of another organization that it may read into, write to, review or merge in Litecky.

Requirements 1 to 4 of version 1.0 are replaced by these. The router is an instruction file: it delivers context to a session and refuses nothing. The standing diff of the deployed router against its template on every template change is retired with the rest of the audit series (ORG-001, One Check of the Five Real Things).

---

## Known Exceptions

| Exception | Reason | Review Trigger |
|-----------|--------|----------------|
| Litecky Editing Services | Another person's business. None of the version 2.0.0 retirements applies, except that of the audit series; the version 1.0 rules stand | A change to Litecky's own contract, which the administrator decides |
| Legal records inside subsidiary directories | Operating agreements, tax filings, formation receipts legally name both entities | Always; these must live in paths that agents do not read (e.g., `business/`) |
| Structural single-Guardian approvals | Current single-natural-person path under GOV-006 may reference both entities in decision records; multiple accounts count once | No expiry or synthetic-council trigger; multi-human mode requires a later Covenant amendment based on distinct natural persons |
| Cloudflare stewardship account | Transitional parent control plane per the Cloudflare Ownership Transition spec | Per that spec's review cadence; long-term goal is per-subsidiary account separation |

Three exceptions of version 1.0 are gone because the rule they excepted is retired: cross-entity audit artifacts under `.claude/orchestration/`, the registry not being read by subsidiary agents, and the Seven Springs sandbox pedagogical references. The second stands for Litecky.

---

## Review Cadence

| Review | Frequency | Responsible |
|--------|-----------|-------------|
| One check of the five real things (ORG-001) | Set by the parent's operating standards | Parent orchestration |
| Litecky's part of the one check | As its administrator decides. Run from inside Litecky and reported value-blind | Litecky's own session, for its administrator |
| This specification's own review | Semi-annually, or upon Covenant-level amendment | Guardian |

The check replaces, for every organization, Litecky included, the four reviews of version 1.0: the quarterly contamination scan, the semi-annual restatement drift review, the router integrity check on every template change, and the annual per-subsidiary isolation audit. Nothing mechanical runs the check or any of the reviews.

---

## Related Documents

- **Source Principles:**
  - [Principle 5: Infrastructure as Code](../../PRINCIPLES.md)
  - [Principle 6: No Committed Secrets](../../PRINCIPLES.md)
  - [Principle 9: Zero Trust](../../PRINCIPLES.md)
  - [Principle 10: Least Privilege](../../PRINCIPLES.md)
  - [Principle 15: Three Circles of Trust](../../PRINCIPLES.md)
  - [Principle 16: Living Law](../../PRINCIPLES.md)
- **Related Policies:**
  - [ORG-001: Subsidiary Authority and Real Boundaries](../org-001-subsidiary-authority.md) — Paired policy (the rule)
  - [AGT-001: Agent Governance](../agt-001-agent-governance.md) — Agent boundary rules
  - [GOV-003: Break-Glass Procedures](../gov-003-break-glass.md) — Emergency cross-entity writes
  - [GOV-006: Council Decision Quorum](../gov-006-decision-quorum.md) — Structural single-Guardian mode
  - [SEC-005: Machine Identity](../sec-005-machine-identity.md) — Machine identity boundary
- **Specifications:**
  - [Secrets Management Specification](./secrets-management.md) — Storage rules for sensitive subsidiary metadata
  - [Cloudflare Ownership Transition Specification](./cloudflare-ownership-transition.md) — Precedent for parent-held transitional control planes
- **Architecture:**
  - [ADR-004: Federated Multi-Org Architecture](../../docs/architecture/004-federated-multi-org-architecture.md) — Established the multi-org structure
  - [ADR-007: Subsidiary Authority and Identity Isolation](../../docs/architecture/007-subsidiary-authority-and-identity-isolation.md) — Decision record for version 1.0; superseded in part by ADR-009
  - [ADR-009: Real Boundaries Between Organizations](../../docs/architecture/009-real-boundaries-between-organizations.md) — Decision record for version 2.0.0
- **Standards:**
  - [Subsidiary Governance Standard](../../../.org/standards/subsidiary-governance.md) — Session routing mechanics
  - [Agentic Workflow Standard](../../../.org/standards/agentic-workflow.md) — One-Human Operating Contract: the merge rule and the reserved list
  - [Estate Agreements Standard](../../../.org/standards/estate-agreements.md) — Agreement terms between organizations
- **Parent-owned implementation references:**
  - `.org/iam/federation/subsidiaries.yaml` — Subsidiary registry
  - `.org/templates/organizations-router-claude-md.template` — Router canonical source
  - `.claude/orchestration/subsidiary-authority-migration/` — Migration campaign under version 1.0
  - `OWNER-DIRECTIONS.md` — The Guardian's standing directions
- **Directive:**
  - `.claude/orchestration/directives/DIRECTIVE-2026-04-20-subsidiary-authority.md` — Parent operational directive issued under version 1.0; what becomes of it is the parent's to record

---

## Changelog

| Date | Author | Summary |
|------|--------|---------|
| 2026-04-20 | Agent | Initial creation (v1.0.0, ACTIVE) establishing the operational detail for the three-tier authority model per ADR-007 and ORG-001; includes ownership matrix, restatement workflow, onboarding/offboarding, sensitive metadata placement rules, and per-subsidiary current-state assessment. |
| 2026-04-26 | Codex | v1.0.1 — Added semantic ownership vs operational hosting rule; recorded Happy Patterns ownership of `scopecam` and Jefahnierocks paid GitHub org deferral for personal projects. |
| 2026-05-02 | Codex | v1.0.2 — Recorded the Jefahnierocks GitHub Free organization boundary as created, kept paid/team automation deferred, and updated the Jefahnierocks shell/public-metadata current-state rows after the local-authority cleanup. |
| 2026-05-02 | Codex | v1.0.3 — Recorded the private Jefahnierocks shell repository publication and preserved child-project independence. |
| 2026-08-29 | Guardian | Unversioned edit in the pull request that made single-Guardian mode structural: the single-Guardian rows of Known Exceptions and Review Cadence were reconciled to GOV-006. No version or changelog row was recorded then; it is recorded here. |
| 2026-11-15 | Agent, recording the Guardian's decision | v2.0.0 — Brought into agreement with ORG-001 version 2.0 per ADR-009, decided by the Guardian under GOV-006 structural single-Guardian mode. §1: a subsidiary's contract may cite a parent standard by version; a parent agent, or an agent of another subsidiary, may read, review and merge in a subsidiary's repository under the merge rule, with authoring kept to the owning organization. §2: the name list applies only to public, customer-facing and legal material; a subsidiary session may read parent files and comment on a parent pull request, and does not author, push to or merge in the parent's repositories. §3: adoption by citation or restatement, with no clock and no parent-side log. §4: onboarding without a migration packet. §7.3: Litecky recorded by role, without personal names, as a sole proprietorship with an owner and an administrator, not co-owned; other §7 rows marked stale without new facts. §8: router requirements replaced. Review cadence replaced by one check of the five real things for every organization; Litecky's part is run from inside Litecky and reported value-blind. No other retirement applies to Litecky. §5 and §6 unchanged. |
