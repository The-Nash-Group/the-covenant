# Hermetic Institutionalism Style Guide
## Quick Reference for The Nash Group

> "Operations are conducted according to established protocols."

---

## I. LANGUAGE CONVENTIONS

### Voice & Tone

**ALWAYS USE:**
- Passive voice: "Operations are conducted"
- Present tense: "Systems maintain continuity"
- Formal diction: "infrastructure," "protocols," "directives"
- Corporate euphemisms: "continuity," "enforcement," "compliance"

**NEVER USE:**
- First person singular: "I," "me," "my"
- Exclamation points (ever)
- Emojis (ever)
- Marketing language: "excited," "passionate," "love," "community"

### Approved Vocabulary

```
TIER 1 (Use Frequently):
- Operations
- Protocols
- Directives
- Compliance
- Enforcement
- Governance
- Continuity
- Infrastructure
- Surveillance
- Authorization

TIER 2 (Use Contextually):
- Strategic
- Institutional
- Temporal
- Hierarchical
- Systematic
- Observability
- Jurisdiction
- Classification

TIER 3 (Use Sparingly):
- Legacy (implies age/permanence)
- Generational (implies continuity)
- Convergence (replaces "gathering")
- Aggregation (replaces "accumulation")
```

### Forbidden Vocabulary

```
NEVER:
- Excited, passionate, love, hate
- Community, family, team (use "personnel," "operators")
- Welcome, hello, hi (use "Access granted")
- Journey, adventure, experience
- Revolutionary, innovative, cutting-edge
- Modern, contemporary, trendy
- Easy, simple, quick
- Amazing, awesome, incredible
```

---

## II. LORE TRANSLATION MATRIX

### Core Concepts

| Highlander Term | Public Translation | Context |
|-----------------|-------------------|---------|
| Immortal | Personnel / Operator / Contributor | General reference to individuals |
| The Quickening | Cumulative Experience Aggregation | Knowledge transfer |
| The Prize | Apex Asset / Singular Authority | Ultimate goal/achievement |
| The Gathering | Strategic Convergence / Consolidation | Events that bring entities together |
| Watchers | Observability & Audit Division | Monitoring/oversight function |
| Holy Ground | Zero-Trust Exclusion Zone | Protected/neutral territory |
| Decapitation | Asset Retirement / Termination | Ending something |
| Sword | Authorization Instrument | Tool of enforcement |
| The Game | Operational Protocols | Rules of engagement |

### Temporal References

| Year | Public Reference | Usage |
|------|-----------------|--------|
| 1518 | Epoch Alpha / Founding Year | Establishment references |
| 1622 | Epoch Beta | Historical marker |
| 1746 | Epoch Gamma | Historical marker |
| 1985 | Epoch Delta | Recent historical marker |

**Pattern:**
```
// Good
"Operations have maintained continuity since Epoch Alpha (1518)"

// Bad
"We've been around since Connor was born in 1518"
```

---

## III. VISUAL CONVENTIONS

### Color Palette

```css
/* INSTITUTIONAL MONOCHROME */
--bg: #FFFFFF;           /* Absolute white backgrounds */
--text: #000000;         /* Absolute black text */
--border: #E5E5E5;       /* Subtle structural borders */

/* STATUS INDICATORS ONLY */
--status-active: #00FF41;  /* Terminal green - use sparingly */
--status-alert: #FF0000;   /* Terminal red - alerts only */

/* NEVER USE */
/* No gradients, no shadows, no colors beyond these */
```

### Typography

```css
/* HEADINGS: Neo-Grotesque Sans */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
             "Helvetica Neue", Arial, sans-serif;
font-weight: 400; /* Never bold except tables */
letter-spacing: 0.1em; /* Always tracked */
text-transform: uppercase; /* Always caps */

/* BODY/DATA: Monospace */
font-family: "SF Mono", "Consolas", "Liberation Mono",
             "Courier New", monospace;
font-size: 0.875rem; /* Slightly smaller than body */
line-height: 1.4; /* Tighter than body */
```

### Grid System

```
BASE UNIT: 8px

Spacing Scale:
--space-1: 8px   (0.5rem)
--space-2: 16px  (1rem)
--space-3: 24px  (1.5rem)
--space-4: 32px  (2rem)
--space-5: 48px  (3rem)
--space-6: 64px  (4rem)
--space-8: 96px  (6rem)

Rules:
1. Every element aligns to 8px grid
2. Use calc() for perfect alignment
3. No arbitrary pixel values
```

### Borders & Structure

```css
/* ALL BORDERS */
border: 1px solid var(--text);  /* Structural */
border: 1px solid var(--border); /* Subtle */

/* NEVER */
border-radius: 0; /* Always */
box-shadow: none; /* Always */
```

---

## IV. CONTENT PATTERNS

### Page Headers

```markdown
# [PAGE TITLE IN CAPS]

[Single sentence describing purpose using passive voice]

[Optional: Status indicators or classification]
```

**Example:**
```markdown
# GOVERNANCE

Operations are conducted according to The Covenant,
the constitutional framework establishing organizational
principles and operational directives.
```

### Section Headers

```markdown
## [Section Title in Title Case]

[Body text using approved vocabulary]
```

### Tables (Preferred Data Format)

```astro
<table>
  <thead>
    <tr>
      <th>Component</th>
      <th>Status</th>
      <th>Classification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>The Covenant</td>
      <td>ENFORCED</td>
      <td>RESTRICTED</td>
    </tr>
  </tbody>
</table>
```

### Lists (When Tables Won't Work)

```astro
<ul>
  <li>Multi-generational continuity planning</li>
  <li>Cumulative experience aggregation</li>
  <li>Strategic convergence protocols</li>
</ul>
```

**Rules:**
- No checkboxes (use status indicators)
- No numbered lists unless truly sequential
- Bullet marker: `●` (styled via CSS)

### Legal Sections (Required)

```astro
<div class="legal">
  <p><strong>NOTICE:</strong></p>
  <p>
    [Formal legal/compliance language using approved vocabulary]
  </p>
</div>
```

**Templates:**

**Access Restriction:**
```
<strong>ACCESS RESTRICTION:</strong>
Full documentation is available only to authorized personnel.
Requests for elevated access must be submitted through approved
channels and are subject to review.
```

**Monitoring Notice:**
```
<strong>MONITORING NOTICE:</strong>
All interactions with this system are recorded for compliance
and security purposes. Unauthorized access attempts are logged
and may result in restriction.
```

**Classification Notice:**
```
<strong>CLASSIFICATION:</strong>
This content contains information classified as [LEVEL].
Distribution outside authorized channels is prohibited.
```

---

## V. COMPONENT PATTERNS

### Status Indicators

```astro
<!-- Import -->
import StatusIndicator from '../components/StatusIndicator.astro';

<!-- Usage -->
<StatusIndicator label="COVENANT .......... ENFORCED" status="active" />
<StatusIndicator label="ALERT CONDITION .... DETECTED" status="alert" />
```

**Visual Output:**
```
● COVENANT .......... ENFORCED
● ALERT CONDITION ... DETECTED
```

### Session Monitor

```astro
<div id="session-monitor">
SESSION: [ID]
DURATION: [HH:MM:SS]
CLEARANCE: [LEVEL]
REQUESTS: [COUNT]
STATUS: [STATE]
</div>
```

**Rules:**
- Always use monospace font
- Always use uppercase labels
- Always align values with dots
- Always update in real-time

### Access Notices

```astro
<div class="access-notice">
  <pre>
┌──────────────────────────────────────────┐
│ [TITLE IN CAPS]                          │
│                                          │
│ [Body text using formal language]        │
│                                          │
│ [Action required statement]              │
└──────────────────────────────────────────┘
  </pre>
  <button onclick="[handler]">
    [ACTION IN CAPS]
  </button>
</div>
```

---

## VI. REPOSITORY DOCUMENTATION

### README Structure

```markdown
# UNIT: [REPOSITORY-NAME]
**Classification:** [LEVEL]
**Status:** [STATE]

════════════════════════════════════════════════

## >> OPERATIONAL DIRECTIVE
[Purpose and function using passive voice]

## >> REQUIREMENTS
[Table or list of requirements]

## >> USAGE
[Code blocks with formal comments]

## >> COMPLIANCE
[Legal/security notices]

════════════════════════════════════════════════
© THE NASH GROUP. ALL RIGHTS RESERVED.
```

### Classification Levels

```
PUBLIC       - Accessible to general personnel
RESTRICTED   - Requires clearance Beta or higher
CLASSIFIED   - Requires clearance Alpha
INTERNAL     - Organization personnel only
```

### Status Values

```
ACTIVE       - Currently operational
LOCKED       - Secured, changes restricted
ENFORCED     - Rules actively applied
MONITORED    - Under observation
DEPRECATED   - Maintained but not recommended
RETIRED      - No longer in service
```

---

## VII. CODE COMMENTING

### File Headers

```typescript
/**
 * [File Purpose]
 *
 * CLASSIFICATION: [LEVEL]
 * MAINTAINED BY: [TEAM/ROLE]
 *
 * [Brief description using approved vocabulary]
 */
```

### Function Documentation

```typescript
/**
 * [Function purpose using passive voice]
 *
 * @param {Type} name - [Parameter description]
 * @returns {Type} [Return value description]
 */
```

### Inline Comments

```typescript
// Establish jurisdiction for session
// [Use imperative mood, no casual language]
```

**Good:**
```typescript
// Initialize compliance monitoring
// Establish session parameters
// Execute authorization protocol
```

**Bad:**
```typescript
// Let's set up some cool monitoring
// This is where the magic happens
// Making sure everything works
```

---

## VIII. GIT CONVENTIONS

### Commit Messages

**Format:**
```
[type]([scope]): [description]

[optional body using institutional language]

[optional footer]
```

**Types:**
```
feat     - New operational capability
fix      - Correction to existing operations
docs     - Documentation updates
refactor - Restructuring without functional changes
test     - Test coverage additions
chore    - Maintenance operations
```

**Examples:**

Good:
```
feat(session): implement behavioral entropy analysis

Behavioral entropy measurement has been integrated into
the session management engine. Clearance levels are now
determined algorithmically based on interaction patterns.

Refs: COVENANT-156
```

Bad:
```
feat: added cool new feature

Made some changes to make things work better :)
```

### Branch Naming

```
[type]/[brief-description]

Examples:
feat/compliance-monitoring
fix/session-persistence
docs/governance-update
refactor/institutional-styling
```

---

## IX. COMMUNICATION TEMPLATES

### Pull Request Description

```markdown
## OPERATIONAL SUMMARY
[Brief description of changes using passive voice]

## MODIFICATIONS
- [List of changes]
- [Using approved vocabulary]

## COMPLIANCE VERIFICATION
- [ ] Documentation updated
- [ ] Tests passing
- [ ] Security review completed
- [ ] Covenant alignment verified

## GOVERNANCE APPROVAL
Requires: [2W+2M / 1M / etc.]
```

### Issue Template

```markdown
## INCIDENT DESCRIPTION
[Formal description of issue]

## AFFECTED SYSTEMS
- [Component]
- [Component]

## OPERATIONAL IMPACT
[Describe impact using institutional language]

## PROPOSED RESOLUTION
[Describe fix using passive voice]

## PRIORITY
[ ] CRITICAL - Operations disrupted
[ ] HIGH - Compliance at risk
[ ] MEDIUM - Functionality impaired
[ ] LOW - Enhancement opportunity
```

---

## X. QUICK DECISION TREE

### "Should I use casual language?"
```
NO → Always use institutional language
```

### "Should I add personality/humor?"
```
NO → Institutions don't have personalities
```

### "Can I use colors?"
```
Only black, white, and status indicators (green/red)
```

### "Should I add this feature?"
```
Does it serve operational necessity? → YES
Does it add "delight"? → NO
```

### "How do I describe this Highlander concept?"
```
Consult Lore Translation Matrix (Section II)
If not listed, create corporate euphemism
Submit for governance approval
```

### "Is this documentation enough?"
```
Is purpose clear? → Continue
Is classification stated? → Continue
Are legal notices present? → Continue
Is language institutional? → Approved
```

---

## XI. COMMON MISTAKES

### Language Errors

❌ "We're excited to announce..."
✅ "Operations have been expanded to include..."

❌ "Check out our cool new feature!"
✅ "Additional operational capabilities have been deployed."

❌ "Thanks for stopping by!"
✅ "Session concluded. Access logged."

❌ "Feel free to reach out!"
✅ "Authorized personnel may submit inquiries through designated channels."

### Visual Errors

❌ Using `#333` instead of `#000000`
✅ Always use absolute black

❌ Adding `border-radius: 4px`
✅ Borders are always square: `border-radius: 0`

❌ Using casual fonts
✅ System sans (headings) + monospace (data)

❌ Adding box shadows
✅ No shadows, ever

### Content Errors

❌ Blog post titled "Why We Built This"
✅ Architecture Decision Record with formal justification

❌ "Meet the Team" section
✅ "Organizational Structure" with roles and jurisdictions

❌ Easter eggs and hidden messages
✅ Compliance logging and formal notices

❌ Testimonials and quotes
✅ Operational metrics and status reports

---

## XII. APPROVAL CHECKLIST

Before publishing any content:

**Language:**
- [ ] All text uses passive voice
- [ ] No forbidden vocabulary present
- [ ] All Highlander references properly translated
- [ ] Legal notices included where appropriate

**Visual:**
- [ ] Colors are absolute black/white (+ status indicators only)
- [ ] All spacing aligns to 8px grid
- [ ] Typography uses approved font stacks
- [ ] No rounded corners or shadows

**Structure:**
- [ ] Classification level stated
- [ ] Status indicators used appropriately
- [ ] Tables used for structured data
- [ ] Headers follow established hierarchy

**Technical:**
- [ ] Code comments are formal
- [ ] File headers include classification
- [ ] Git conventions followed
- [ ] Documentation is complete

---

## XIII. STYLE EVOLUTION

### When to Update This Guide

This style guide should be updated when:
1. New lore terms need translation
2. New component patterns emerge
3. Governance approves terminology changes
4. Classification system expands

### Amendment Process

1. Identify need for style guide update
2. Draft proposed changes
3. Submit for governance review (2W+2M)
4. Update guide with version number
5. Announce in engineering channels

---

**Current Version:** 2.0.0
**Last Updated:** 2025-11-21
**Status:** ACTIVE

**Maintained By:** The Watchers / Documentation Authority

════════════════════════════════════════════════
© THE NASH GROUP. ALL RIGHTS RESERVED.
UNAUTHORIZED REPRODUCTION PROHIBITED.
════════════════════════════════════════════════
