# The Covenant
*The Constitution of The Nash Group*

> "In the beginning was the Word, and the Word was Code, and the Code was Law."

## The Three Pillars of Governance

Welcome to the philosophical heart of The Nash Group. Our governance is built on three interconnected pillars that answer the fundamental questions of our organization:

### 1. **[The Covenant](./PRINCIPLES.md)** - The "Why"
Our core values, principles, and sacred laws. The philosophical foundation that defines why we operate as we do.

### 2. **[The Human Mandate](./HUMAN_MANDATE.md)** - The "Who"
The responsibilities and roles of the Guardians who interpret our principles and operate our systems. The bridge between philosophy and implementation.

### 3. **[The Citadel](https://github.com/The-Nash-Group/citadel-config)** - The "How"
The technical engine for infrastructure enforcement. OpenTofu-backed Infrastructure as Code and Policy as Code translate principles into reality where current Citadel evidence proves the control is live.

This is `the-covenant` - the philosophical foundation, where human wisdom guides machine execution.

## Repository Structure

```
the-covenant/
├── README.md                     # This scroll - The gate inscription
├── CLAUDE.md                     # AI assistant context
├── HUMAN_MANDATE.md              # The Bridge - Guardian roles and responsibilities
├── GOVERNANCE.md                 # The Laws of the Clans
├── PRINCIPLES.md                 # The Art of the Duel (technical standards)
├── CONTRIBUTING.md               # The Path to Immortality
├── CHANGELOG.md                  # Change history
├── LICENSE                       # License
├── docs/
│   ├── role-mapping.md           # Guardian role mapping
│   └── architecture/             # Architecture Decision Records (canonical home)
│       ├── 000-template.md
│       ├── 001-establish-three-pillar-repository-architecture.md
│       ├── 002-governed-agentic-development.md
│       └── 003-establish-cloudflare-governance-baseline.md
├── policies/                     # Formal policy framework
│   ├── README.md                 # Policy index and mapping
│   ├── sc-*.md                   # Source Control policies
│   ├── sec-*.md                  # Security policies
│   ├── gov-*.md                  # Governance policies
│   ├── ops-*.md                  # Operations policies
│   ├── inf-*.md, doc-*.md, ...   # Infrastructure, Documentation, etc.
│   ├── agt-*.md                  # Agent Governance policies
│   ├── guides/                   # Policy implementation guides
│   │   └── policy-enforcement.md
│   └── specs/                    # Policy specifications
│       └── iam-specification.md
├── history/                      # Historical reports and research
│   ├── reports/2025-11/          # November 2025 governance and strategy artifacts
│   └── research/                 # Research documents
├── schemas/                      # JSON schemas (e.g., ADR schema)
├── REFERENCE/                    # The Archives
│   ├── index.md                  # The Archivist's Guide
│   ├── legacy-safe-settings/     # The Old Ways (archived YAML)
│   └── decisions/                # Legacy decision records (archived)
└── .github/
    └── PULL_REQUEST_TEMPLATE.md  # The Ritual of Amendment
```

## The Mission, Vision, and Values

### Our Quest (Mission)
To build a single, unified platform that is timeless, secure, and self-aware—The Prize we all seek. We forge not just code, but a legacy that outlives its creators.

### The Prophecy (Vision)
A future where development is a focused, creative act, unburdened by toil and anchored by a single source of truth for every component, from documentation to defense. Where every stronghold operates by the same sacred principles, yet maintains its unique identity.

### The Code (Values)

#### Immortality through Code
We write software designed to outlive its creators—durable, well-documented, and backwards-compatible. Every line is written as if it will be read by our successors a decade hence.

#### There Can Be Only One Source of Truth
We abhor ambiguity. For every asset—a secret, a setting, a document—there is one, and only one, authoritative source. Duplication is the path to drift, and drift is the path to chaos.

#### The Quickening is Knowledge
We treat every event, especially failure, as a source of power. We are zealous about observability, post-mortems, and learning from our mistakes. Each incident makes us stronger.

## The Workflow: From Philosophy to Reality

The Covenant defines the **why**. The owning lower layer implements the **how**: Citadel for infrastructure enforcement, Shield for identity contracts, Nexus for runtime admission once wired, and subsidiaries/projects for local restatements. Here is the sacred workflow:

### 1. The Philosophical Debate
A change in principle is proposed via Pull Request to `the-covenant`. This might be:
- A new engineering standard (e.g., "All services shall implement structured logging")
- A governance change (e.g., "Platform services require two approving reviews")
- An architectural principle (e.g., "We shall prefer boring technology")

### 2. The Council's Deliberation
The PR is debated openly. All Immortals may voice their wisdom. The proposal must be approved according to the rules in `GOVERNANCE.md`.

### 3. The Ratification
Once approved and merged, the principle becomes law. The document is updated, the chronicle recorded.

### 4. The Translation
A Mentor opens a PR in the owning lower-layer repo, translating the ratified
principle without changing its meaning:
- A governance change may become a `github_repository_ruleset` in Citadel
- A security principle may become a `cloudflare_ruleset` in Citadel
- An identity invariant may become a Shield contract and Citadel/Nexus consumer
  evidence
- A subsidiary rule becomes a local restatement in that subsidiary's own voice

### 5. The Scrying
The OpenTofu/IaC plan reveals exactly what will change in our infrastructure. No surprises, no hidden consequences.

### 6. The Forging
Upon approval and merge, the approved IaC or policy change is applied. The philosophy becomes reality.

## The Sacred Documents

### `GOVERNANCE.md`
Defines the clans, their powers, and the rituals of change. Who may propose, who may approve, and how decisions are made.

### `PRINCIPLES.md`
Our technical playbook. Specific, actionable standards for how we build. Each principle includes:
- **The Law**: The rule itself
- **The Lesson**: The hard-fought wisdom behind it
- **The Implementation**: How it maps to enforcement or evidence in the owning lower layer

### `REFERENCE/`
The archives of our journey. Historical context, deprecated practices, and the evolution of our thinking. Not a graveyard, but a museum.

## The Law of Laws

This Covenant is living law. It evolves through structured debate and careful consideration. But certain truths are immutable:

1. **Changes to philosophy precede changes to implementation**
   - First we agree on the principle
   - Then we encode it in OpenTofu/IaC, Policy as Code, Shield/Nexus contracts, or local restatements in the owning lower layer
   - Never the reverse

2. **Documentation is prophecy**
   - What we write here shapes what we build
   - Clarity in word leads to clarity in code
   - Ambiguity in principle leads to chaos in practice

3. **The Covenant has no technical power**
   - This repository contains no automation
   - It triggers no deployments
   - Its authority is moral and directive, not mechanical

## Contributing to the Covenant

To propose a change to our constitution:

1. **Fork and Branch**: Create your proposal in a new branch
2. **Document Clearly**: State the principle, the rationale, and the expected implementation
3. **Open the Debate**: Submit a Pull Request using our template
4. **Defend Your Position**: Engage with feedback, refine your proposal
5. **Await the Council**: The approval process defined in `GOVERNANCE.md`

Remember: You are not just changing a document. You are shaping the future of our engineering culture.

## The Keepers of the Covenant

The Covenant is maintained by the collective wisdom of The Nash Group, with special responsibilities held by:

- **The Watchers** (`@the-nash-group/watchers`): Guardians of governance and process
- **The Mentors** (`@the-nash-group/mentors`): Keepers of technical standards
- **The Immortals** (all contributors): The voice of experience and innovation

## The Bridge to Implementation

While this repository holds no technical enforcement, it maintains a sacred link to the owning implementation layers:

- Every principle here should map to an enforcement or evidence home
- Every OpenTofu/IaC resource, policy rule, runtime-admission claim, identity
  contract, or local restatement should trace back to a principle here
- Regular audits ensure alignment between philosophy and implementation

## The Ancient Wisdom

> "The Covenant without the Citadel is mere words.
> The Citadel without the Covenant is mere machinery.
> Together, they are civilization."

---

*For infrastructure implementation of these principles, see [`the-citadel`](https://github.com/The-Nash-Group/citadel-config)*

*For questions about this governance model, raise an issue or consult the archives in `REFERENCE/`*
