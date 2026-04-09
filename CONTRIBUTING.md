# Contributing to The Covenant
*The Path to Immortality*

> "Every Immortal was once a mortal who refused to give up."

## Understanding Your Role

Before contributing, understand that The Covenant is not just documentation—it is the constitution of The Nash Group's engineering culture. Changes here ripple through every repository, every workflow, and every decision we make.

## The Sacred Separation

Remember the fundamental architecture:
- **This repository (`the-covenant`)**: Defines the "why" - our principles, standards, and governance
- **The implementation (`the-citadel`)**: Defines the "how" - the Terraform code that enforces our principles

Never confuse the two. We debate philosophy here; we implement machinery there.

## Types of Contributions

### 1. Proposing New Principles

When you've identified a gap in our standards or a new best practice worth codifying:

1. **Search First**: Check if a similar principle already exists in `PRINCIPLES.md`
2. **Document the Problem**: What issue does this principle address?
3. **Provide Evidence**: Share examples, post-mortems, or industry best practices
4. **Define Implementation**: How would this be enforced via Terraform in `the-citadel`?

### 2. Amending Existing Principles

When experience has taught us a principle needs refinement:

1. **Reference the Original**: Link to the principle being amended
2. **Explain the Evolution**: What have we learned since the original was written?
3. **Show the Delta**: Be clear about what's changing and what's staying the same
4. **Update Implementation**: Describe changes needed in `the-citadel`

### 3. Governance Changes

When proposing changes to how we make decisions:

1. **Identify the Gap**: What scenario is not covered by current governance?
2. **Propose the Solution**: How should we handle this scenario?
3. **Consider Edge Cases**: What could go wrong with this governance model?
4. **Seek Broad Input**: Governance affects everyone; ensure wide consultation

### 4. Updating Existing ADRs

ADRs are living documents — they should stay current rather than accumulate stale information. However, ADRs are governance documents and updates follow the same review process as other Covenant changes.

1. **Get Guardian approval first** — ADR updates are not casual edits; propose changes and get human sign-off
2. **Edit in place rather than supersede** — unless the original decision is being genuinely reversed
3. **Add a changelog entry** — append a row to the Changelog table at the bottom with date, author, and summary
4. **Preserve original context** — keep the original Date in metadata; use "Last Updated" for your edit
5. **Ensure self-containment** — a reader encountering the ADR for the first time should get an accurate picture of today's architecture

Only create a *new* superseding ADR when the original decision is genuinely reversed and the old rationale no longer applies.

### 5. Documentation Improvements

When clarifying without changing meaning:

1. **Preserve Intent**: Ensure the original meaning is maintained
2. **Improve Clarity**: Make the language more accessible
3. **Add Examples**: Concrete examples help understanding
4. **Fix Inconsistencies**: Ensure terminology is used consistently

## The Contribution Process

### Step 1: Fork and Branch

```bash
git clone https://github.com/the-nash-group/the-covenant.git
cd the-covenant
git checkout -b proposal/your-descriptive-name
```

Branch naming conventions:
- `proposal/` - For new principles or governance changes
- `amendment/` - For modifications to existing principles
- `docs/` - For documentation improvements
- `archive/` - For moving content to REFERENCE/

### Step 2: Make Your Changes

Follow these guidelines:
- Write in clear, concise language
- Use the established format for principles (Law, Lesson, Implementation)
- Include examples where helpful
- Maintain the mythological tone where appropriate (it's part of our culture)

### Step 3: Submit Your Pull Request

1. Push your branch to your fork
2. Open a Pull Request against `main`
3. Fill out the PR template completely
4. Engage constructively with feedback

### Step 4: The Debate Period

Your proposal enters the public debate phase:
- **Minor changes**: Minimum 72 hours
- **Major changes**: Minimum 1 week

During this time:
- All Immortals may comment
- Address feedback promptly
- Be prepared to refine your proposal
- Build consensus through reasoned argument

### Step 5: Council Review

Once debate settles, the Council reviews:
- 2 Watchers must approve
- 2 Mentors from different clans must approve
- Any blocking concerns must be resolved

## Writing Style Guide

### Tone
- **Authoritative but not authoritarian**: We state principles firmly but explain why
- **Practical over theoretical**: Every principle must be implementable
- **Clear over clever**: Clarity beats wit every time
- **Consistent mythology**: If using our mythological framework, use it consistently

### Structure
- **Principles**: Law → Lesson → Implementation
- **Governance**: Current State → Problem → Solution
- **Documentation**: Context → Content → Consequences

### Language
- Use active voice
- Prefer simple words over complex ones
- Define technical terms on first use
- Include examples for complex concepts

## What Makes a Good Principle?

A strong principle has these characteristics:

1. **Specific**: Clear enough to implement, not vague platitudes
2. **Justified**: Backed by experience or industry best practices
3. **Enforceable**: Can be translated into Terraform/automation
4. **Consistent**: Aligns with our existing principles and values
5. **Valuable**: Solves a real problem or prevents real issues

## Anti-Patterns to Avoid

### In Proposals
- ❌ Vague principles that can't be enforced
- ❌ Solutions looking for problems
- ❌ Personal preferences disguised as best practices
- ❌ Changes that contradict core values
- ❌ Overly complex governance for simple issues

### In Debate
- ❌ Ad hominem attacks
- ❌ Appeals to authority without evidence
- ❌ Refusing to consider feedback
- ❌ Bike-shedding on minor details
- ❌ Pushing through without consensus

## Building Consensus

The strongest principles achieve unanimous support. To build consensus:

1. **Listen First**: Understand objections before defending
2. **Find Common Ground**: Identify shared goals
3. **Compromise When Possible**: Perfect is the enemy of good
4. **Document Dissent**: If consensus can't be reached, document why
5. **Revisit Later**: Some principles need time to mature

## After Your Contribution

Once your change is merged:

1. **Monitor Implementation**: Watch for the corresponding PR in `the-citadel`
2. **Support Adoption**: Help teams understand and adopt the new principle
3. **Gather Feedback**: Real-world usage reveals improvements
4. **Iterate**: Be open to future refinements

## Getting Help

- **Questions**: Open an issue labeled `question`
- **Discussion**: Use issues labeled `discussion` for broader topics
- **Mentorship**: Reach out to `@the-nash-group/mentors` for guidance
- **Governance**: Contact `@the-nash-group/watchers` for process questions

## Recognition

Contributors to The Covenant shape our engineering culture. Your thoughtful contributions are valued and recognized:

- Significant contributions are noted in commit messages
- Substantial improvements may warrant mention in REFERENCE/decisions/
- The best principles outlive their authors—true immortality

---

*"The Covenant is not carved in stone but written in living ink. Each contribution adds to our collective wisdom."*
