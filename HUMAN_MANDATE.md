# The Human Mandate
*The Bridge Between Philosophy and Implementation*

> "The machine executes perfectly. The human decides wisely. Together, they create civilization."

## The Sacred Separation

In the realm of The Nash Group, we maintain a fundamental distinction:
- **Machines** execute with perfect consistency but without understanding
- **Humans** provide judgment, context, and wisdom but are prone to inconsistency

This document defines the human side of the equation—the roles, responsibilities, and rituals that ensure our automated systems serve our human purposes.

## The Three-Tiered Architecture

Our governance operates on three interconnected levels:

1. **[The Covenant](./PRINCIPLES.md)** - The "Why"
   - Defines our timeless principles and values
   - Abstract, philosophical, slow-moving
   
2. **The Human Mandate** (this document) - The "Who"
   - Defines Guardian responsibilities and roles
   - Operational, procedural, focused on human judgment
   
3. **[The Citadel](https://github.com/the-nash-group/citadel-config)** - The "How"
   - Contains the Infrastructure as Code
   - Concrete, technical, fast-moving

## The Human/Machine Creed

This creed defines the inviolable boundary between human and machine responsibilities.

### The System Will:
- **Enforce Invariantly:** Apply every rule, permission, and configuration exactly as written
- **Report Deviations:** Detect and report any drift from its defined state, without exception
- **Execute Flawlessly:** Perform the approved sequence of `plan` and `apply` without opinion
- **Automate Toil:** Handle all repetitive checks, scheduled cleanups, and dependency updates

### The Guardians Will:
- **Provide Intent:** Define the principles and philosophy that give the system its purpose
- **Exercise Judgment:** Review the system's plans, triage its alerts, and make decisions on novel situations
- **Assume Command:** Take direct, manual control during emergencies when automation has failed
- **Evolve the System:** Curate and improve the automation itself, ensuring it remains an asset

## The Five Archetypes of Guardianship

These are not job titles but "hats" that Guardians wear depending on the task at hand. A single person may wear multiple hats throughout their day.

### 1. The Philosopher
**Purpose:** To debate and refine the principles that govern our realm

**Responsibilities:**
- Propose new principles or amendments to The Covenant
- Participate in philosophical debates about our direction
- Ensure technical decisions align with our values
- Document the "why" behind our choices

**Key Actions:**
- Opens PRs to `the-covenant`
- Participates in principle discussions
- Writes Architecture Decision Records

### 2. The Architect (The Translator)
**Purpose:** To transform philosophy into machinery

**Responsibilities:**
- Translate Covenant principles into Terraform code
- Design reusable modules and patterns
- Ensure technical implementation matches philosophical intent
- Bridge the gap between abstract and concrete

**Key Actions:**
- Opens PRs to `citadel-config`
- Writes Terraform resources
- Creates module documentation

### 3. The Judge
**Purpose:** To ensure all changes align with our principles and standards

**Responsibilities:**
- Review infrastructure changes for compliance
- Validate that Terraform plans match stated intent
- Ensure security and operational standards are met
- Provide the human checkpoint before automation proceeds

**Key Actions:**
- Reviews PRs in both repositories
- Validates `terraform plan` output
- Approves or requests changes
- Documents decision rationale

### 4. The Gardener
**Purpose:** To maintain the health and efficiency of our systems

**Responsibilities:**
- Keep dependencies updated
- Refactor and optimize Terraform code
- Monitor for drift and reconcile differences
- Improve performance and reduce costs
- Ensure backward compatibility

**Key Actions:**
- Performs regular maintenance
- Updates provider versions
- Refactors modules for reusability
- Monitors state file health

### 5. The Explorer
**Purpose:** To build new capabilities within established boundaries

**Responsibilities:**
- Create new services and repositories
- Innovate within the framework
- Identify gaps in our principles or tooling
- Push the boundaries while respecting the rules

**Key Actions:**
- Creates new repositories using established patterns
- Proposes new principles based on discoveries
- Documents novel solutions
- Shares learnings with the team

## From Mandate to Mission: How Roles Map to Teams

The abstract roles of the Mandate are fulfilled by our formally defined teams. While any Guardian may wear any hat, our teams have primary ownership over specific domains.

### `@the-nash-group/mentors`

**Mission:** To serve as the primary architects and stewards of The Citadel and its governed repositories.

**Primary Hats Worn:**
- **The Judge:** Mentors are the default reviewers for all infrastructure changes in `citadel-config`
- **The Architect:** Mentors translate principles from The Covenant into robust Terraform code
- **The Gardener:** Mentors own the technical health of the automation

**Special Authorities:**
- Required approval for all Citadel changes
- Can merge to protected branches after review
- Define technical standards and patterns

### `@the-nash-group/watchers`

**Mission:** To provide specialized oversight on matters of security, access, and organizational risk.

**Primary Hats Worn:**
- **The Judge (Specialized):** Watchers review changes affecting critical security infrastructure
- **The Philosopher (Specialized):** Watchers lead the definition of security-related principles
- **The Emergency Responder:** Watchers are authorized to execute break-glass procedures

**Special Authorities:**
- Required approval for security-critical changes
- Can bypass certain protections in emergencies
- Access to audit logs and security dashboards

### All Guardians

**Mission:** Every member of the organization is a Guardian of the culture.

**Primary Hats Worn:**
- **The Explorer:** All Guardians can create and innovate within safe boundaries
- **The Philosopher (Participant):** All Guardians contribute to the evolution of The Covenant

**Universal Rights:**
- Propose changes to any accessible repository
- Participate in all public debates
- Raise concerns about principles or implementation

## Rituals of Guardianship

### The Daily Stand
Each Guardian should ask themselves:
1. What hat am I wearing today?
2. Does my work align with The Covenant?
3. Am I automating toil or creating it?

### The Weekly Review
Teams should collectively assess:
1. Are we maintaining the Human/Machine boundary?
2. What manual work should be automated?
3. What automated processes need human oversight?

### The Quarterly Reflection
The organization should evaluate:
1. Are our roles and responsibilities clear?
2. Do our teams have the right authorities?
3. Is the Human Mandate serving its purpose?

## Emergency Protocols

### When Automation Fails
1. **Watchers** assume emergency command
2. **Mentors** diagnose and develop fixes
3. **All Guardians** follow incident response procedures
4. Document lessons learned in The Covenant

### When Humans Fail
1. Automation prevents unauthorized changes
2. Audit logs track all human actions
3. Post-mortems focus on process, not blame
4. Update The Human Mandate with new safeguards

## The Guardian's Oath

*I swear to:*
- **Respect the Boundary:** Never ask the machine to judge, never act without thinking
- **Wear My Hats Consciously:** Know which role I'm fulfilling at each moment
- **Document My Decisions:** Leave a trail of wisdom for those who follow
- **Evolve the System:** Continuously improve both human and machine processes
- **Share Knowledge Freely:** Teach what I learn, learn what others teach

## Evolution of the Mandate

This document, like The Covenant it serves, is living law. As our organization grows and learns, so too must our understanding of human roles evolve. Propose changes through the standard PR process, but remember: changing how humans operate is often harder than changing code.

## Connecting the Layers

- **From Principle to Role:** Every principle in The Covenant implies human responsibilities defined here
- **From Role to Code:** Every human action here results in Terraform code in The Citadel
- **From Code to Principle:** Every line in The Citadel traces back through human decision to philosophical principle

---

*"The Human Mandate is not about limiting human action, but about making it deliberate, principled, and powerful."*

*For the philosophical foundation, see [The Covenant](./README.md)*  
*For the technical implementation, see [The Citadel](https://github.com/the-nash-group/citadel-config)*