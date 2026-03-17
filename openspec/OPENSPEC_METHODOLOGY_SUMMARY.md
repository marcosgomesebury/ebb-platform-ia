# OpenSpec Methodology - Comprehensive Summary

## Overview

OpenSpec is a lightweight, spec-driven development framework designed to help AI coding assistants and humans align on what to build before any code is written. It emphasizes fluid, iterative development over rigid waterfall processes, with a focus on brownfield (existing) codebases.

## 1. Core Principles of Spec-Driven Development

### Philosophy

OpenSpec is built around **four fundamental principles**:

```text
→ fluid not rigid       — no phase gates, work on what makes sense
→ iterative not waterfall — learn as you build, refine as you go
→ easy not complex      — lightweight setup, minimal ceremony
→ brownfield-first      — works with existing codebases, not just greenfield
→ scalable             — from personal projects to enterprises
```

### Why These Principles Matter

- **Fluid not rigid**: Create artifacts in any order that makes sense for your work. No locked phases.
- **Iterative not waterfall**: Requirements change and understanding deepens. OpenSpec embraces this reality.
- **Easy not complex**: Initialize in seconds, start working immediately, customize only if needed.
- **Brownfield-first**: Most work modifies existing systems. OpenSpec's delta-based approach makes it easy to specify changes to existing behavior.

### Actions, Not Phases

Unlike traditional workflows that lock you into sequential phases (Planning → Implementation → Done), OpenSpec provides **actions** you can take at any time:

```text
proposal ──► specs ──► design ──► tasks ──► implement
   ▲           ▲          ▲                    │
   └───────────┴──────────┴────────────────────┘
            update as you learn
```

Dependencies are **enablers**, not gates. They show what's possible to create, not what you must create next.

---

## 2. Directory Structure

### Main Structure

```
openspec/
├── specs/              # Source of truth (current system behavior)
│   └── <domain>/
│       └── spec.md
├── changes/            # Proposed updates (one folder per change)
│   ├── <change-name>/
│   │   ├── proposal.md
│   │   ├── design.md
│   │   ├── tasks.md
│   │   └── specs/      # Delta specs (what's changing)
│   │       └── <domain>/
│   │           └── spec.md
│   └── archive/        # Completed changes (preserved for history)
│       └── YYYY-MM-DD-<change-name>/
├── schemas/            # Custom workflow schemas (optional)
│   └── <schema-name>/
│       └── schema.yaml
└── config.yaml         # Project configuration (optional)
```

### Two Key Directories

#### `specs/` - Source of Truth

- Describes how your system **currently** behaves
- Organized by domain (logical groupings that make sense for your system)
- Common patterns:
  - **By feature area**: `auth/`, `payments/`, `search/`
  - **By component**: `api/`, `frontend/`, `workers/`
  - **By bounded context**: `ordering/`, `fulfillment/`, `inventory/`

#### `changes/` - Proposed Modifications

- Each change gets its own folder with all related artifacts
- Multiple changes can exist simultaneously without conflicting
- When complete, changes merge specs into main `specs/` and move to `archive/`
- Archive preserves full context: proposal, design, tasks, and spec deltas

---

## 3. Best Practices for Documenting Specifications

### Spec Format

A spec contains **requirements**, and each requirement has **scenarios**:

```markdown
# Auth Specification

## Purpose
Authentication and session management for the application.

## Requirements

### Requirement: User Authentication
The system SHALL issue a JWT token upon successful login.

#### Scenario: Valid credentials
- GIVEN a user with valid credentials
- WHEN the user submits login form
- THEN a JWT token is returned
- AND the user is redirected to dashboard

#### Scenario: Invalid credentials
- GIVEN invalid credentials
- WHEN the user submits login form
- THEN an error message is displayed
- AND no token is issued
```

### Key Elements

| Element | Purpose |
|---------|---------|
| `## Purpose` | High-level description of this spec's domain |
| `### Requirement:` | A specific behavior the system must have |
| `#### Scenario:` | A concrete example of the requirement in action |
| SHALL/MUST/SHOULD | RFC 2119 keywords indicating requirement strength |

### Requirements vs Scenarios

- **Requirements are the "what"**: State what the system should do without specifying implementation
- **Scenarios are the "when"**: Provide concrete examples that can be verified

### Good Scenario Characteristics

- Are testable (you could write an automated test for them)
- Cover both happy path and edge cases
- Use Given/When/Then or similar structured format

### RFC 2119 Keywords

- **MUST/SHALL**: Absolute requirement
- **SHOULD**: Recommended, but exceptions exist
- **MAY**: Optional

### What a Spec Is (and Is Not)

✅ **Good spec content:**
- Observable behavior users or downstream systems rely on
- Inputs, outputs, and error conditions
- External constraints (security, privacy, reliability, compatibility)
- Scenarios that can be tested or explicitly validated

❌ **Avoid in specs:**
- Internal class/function names
- Library or framework choices
- Step-by-step implementation details
- Detailed execution plans (those belong in `design.md` or `tasks.md`)

**Quick test**: If implementation can change without changing externally visible behavior, it likely does not belong in the spec.

### Progressive Rigor

Use the lightest level that still makes the change verifiable:

**Lite spec (default):**
- Short behavior-first requirements
- Clear scope and non-goals
- A few concrete acceptance checks

**Full spec (for higher risk):**
- Cross-team or cross-repo changes
- API/contract changes, migrations, security/privacy concerns
- Changes where ambiguity is likely to cause expensive rework

Most changes should stay in **Lite mode**.

---

## 4. Delta Specs - The Key Concept

Delta specs describe **what's changing** relative to current specs, not restating the entire spec.

### The Format

```markdown
# Delta for Auth

## ADDED Requirements

### Requirement: Two-Factor Authentication
The system MUST support TOTP-based two-factor authentication.

#### Scenario: 2FA enrollment
- GIVEN a user without 2FA enabled
- WHEN the user enables 2FA in settings
- THEN a QR code is displayed for authenticator app setup

## MODIFIED Requirements

### Requirement: Session Expiration
The system MUST expire sessions after 15 minutes of inactivity.
(Previously: 30 minutes)

#### Scenario: Idle timeout
- GIVEN an authenticated session
- WHEN 15 minutes pass without activity
- THEN the session is invalidated

## REMOVED Requirements

### Requirement: Remember Me
(Deprecated in favor of 2FA. Users should re-authenticate each session.)
```

### Delta Sections

| Section | Meaning | What Happens on Archive |
|---------|---------|------------------------|
| `## ADDED Requirements` | New behavior | Appended to main spec |
| `## MODIFIED Requirements` | Changed behavior | Replaces existing requirement |
| `## REMOVED Requirements` | Deprecated behavior | Deleted from main spec |

### Why Deltas Instead of Full Specs

- **Clarity**: A delta shows exactly what's changing
- **Conflict avoidance**: Two changes can touch the same spec file without conflicting
- **Review efficiency**: Reviewers see the change, not the unchanged context
- **Brownfield fit**: Most work modifies existing behavior. Deltas make modifications first-class.

---

## 5. Artifacts - Documents Within a Change

### The Artifact Flow

```
proposal ──────► specs ──────► design ──────► tasks ──────► implement
    │               │             │             │
   why            what           how          steps
 + scope        changes       approach      to take
```

### Artifact Types

#### 1. Proposal (`proposal.md`)

Captures **intent**, **scope**, and **approach** at a high level.

```markdown
# Proposal: Add Dark Mode

## Intent
Users have requested a dark mode option to reduce eye strain
during nighttime usage and match system preferences.

## Scope
In scope:
- Theme toggle in settings
- System preference detection
- Persist preference in localStorage

Out of scope:
- Custom color themes (future work)
- Per-page theme overrides

## Approach
Use CSS custom properties for theming with a React context
for state management. Detect system preference on first load,
allow manual override.
```

**When to update:** Scope changes, intent clarifies, or approach fundamentally shifts.

#### 2. Specs (`specs/`)

Delta specs describing **what's changing** relative to current specs.

#### 3. Design (`design.md`)

Captures **technical approach** and **architecture decisions**.

```markdown
# Design: Add Dark Mode

## Technical Approach
Theme state managed via React Context to avoid prop drilling.
CSS custom properties enable runtime switching without class toggling.

## Architecture Decisions

### Decision: Context over Redux
Using React Context for theme state because:
- Simple binary state (light/dark)
- No complex state transitions
- Avoids adding Redux dependency

### Decision: CSS Custom Properties
Using CSS variables instead of CSS-in-JS because:
- Works with existing stylesheet
- No runtime overhead
- Browser-native solution

## Data Flow
```
ThemeProvider (context)
       │
       ▼
ThemeToggle ◄──► localStorage
       │
       ▼
CSS Variables (applied to :root)
```

## File Changes
- `src/contexts/ThemeContext.tsx` (new)
- `src/components/ThemeToggle.tsx` (new)
- `src/styles/globals.css` (modified)
```

**When to update:** Implementation reveals the approach won't work, better solution discovered, or dependencies/constraints change.

#### 4. Tasks (`tasks.md`)

The **implementation checklist** — concrete steps with checkboxes.

```markdown
# Tasks

## 1. Theme Infrastructure
- [ ] 1.1 Create ThemeContext with light/dark state
- [ ] 1.2 Add CSS custom properties for colors
- [ ] 1.3 Implement localStorage persistence
- [ ] 1.4 Add system preference detection

## 2. UI Components
- [ ] 2.1 Create ThemeToggle component
- [ ] 2.2 Add toggle to settings page
- [ ] 2.3 Update Header to include quick toggle

## 3. Styling
- [ ] 3.1 Define dark theme color palette
- [ ] 3.2 Update components to use CSS variables
- [ ] 3.3 Test contrast ratios for accessibility
```

**Best practices:**
- Group related tasks under headings
- Use hierarchical numbering (1.1, 1.2, etc.)
- Keep tasks small enough to complete in one session
- Check tasks off as you complete them

---

## 6. Workflow Commands

### Two Modes

#### Default Quick Path (`core` profile)

New installs default to `core` profile:

```text
/opsx:propose ──► /opsx:apply ──► /opsx:archive
```

Commands:
- `/opsx:propose` - Create change and generate planning artifacts in one step
- `/opsx:explore` - Think through ideas before committing to a change
- `/opsx:apply` - Implement tasks from the change
- `/opsx:archive` - Archive a completed change

#### Expanded Workflow (custom selection)

Enable with `openspec config profile` then `openspec update`:

```text
/opsx:new ──► /opsx:ff or /opsx:continue ──► /opsx:apply ──► /opsx:verify ──► /opsx:archive
```

Additional commands:
- `/opsx:new` - Start a new change scaffold
- `/opsx:continue` - Create next artifact based on dependencies
- `/opsx:ff` - Fast-forward: create all planning artifacts at once
- `/opsx:verify` - Validate implementation matches artifacts
- `/opsx:sync` - Merge delta specs into main specs
- `/opsx:bulk-archive` - Archive multiple changes at once
- `/opsx:onboard` - Guided tutorial through complete workflow

### Command Quick Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/opsx:propose` | Create change + planning artifacts | Fast default path |
| `/opsx:explore` | Think through ideas | Unclear requirements |
| `/opsx:new` | Start a change scaffold | Explicit artifact control |
| `/opsx:continue` | Create next artifact | Step-by-step control |
| `/opsx:ff` | Create all planning artifacts | Clear scope |
| `/opsx:apply` | Implement tasks | Ready to write code |
| `/opsx:verify` | Validate implementation | Before archiving |
| `/opsx:archive` | Complete the change | All work finished |

---

## 7. Common Workflow Patterns

### Quick Feature

When you know what you want to build:

```text
/opsx:new ──► /opsx:ff ──► /opsx:apply ──► /opsx:verify ──► /opsx:archive
```

**Best for:** Small to medium features, bug fixes, straightforward changes.

### Exploratory

When requirements are unclear:

```text
/opsx:explore ──► /opsx:new ──► /opsx:continue ──► ... ──► /opsx:apply
```

**Best for:** Performance optimization, debugging, architectural decisions, unclear requirements.

### Parallel Changes

Work on multiple changes at once:

```text
Change A: /opsx:new ──► /opsx:ff ──► /opsx:apply (in progress)
                                         │
                          context switch
                                         │
Change B: /opsx:new ──► /opsx:ff ──────► /opsx:apply
```

Use `/opsx:bulk-archive` to archive multiple completed changes at once.

**Best for:** Parallel work streams, urgent interrupts, team collaboration.

### Completing a Change

Recommended completion flow:

```text
/opsx:apply ──► /opsx:verify ──► /opsx:archive
              validates          prompts to sync
           implementation       if needed
```

---

## 8. Archive Process

### What Happens When You Archive

1. **Merge deltas**: Each delta spec section (ADDED/MODIFIED/REMOVED) is applied to the corresponding main spec
2. **Move to archive**: The change folder moves to `changes/archive/YYYY-MM-DD-<name>/` with date prefix
3. **Preserve context**: All artifacts remain intact in the archive

### Why Archive Matters

- **Clean state**: Active changes show only work in progress
- **Audit trail**: Full context of every change is preserved
- **Spec evolution**: Specs grow organically as changes are archived

### The Virtuous Cycle

```
1. Specs describe current behavior
2. Changes propose modifications (as deltas)
3. Implementation makes the changes real
4. Archive merges deltas into specs
5. Specs now describe the new behavior
6. Next change builds on updated specs
```

---

## 9. Best Practices

### Keep Changes Focused

One logical unit of work per change. If doing "add feature X and also refactor Y", consider two separate changes.

**Why it matters:**
- Easier to review and understand
- Cleaner archive history
- Can ship independently
- Simpler rollback if needed

### Use `/opsx:explore` for Unclear Requirements

Before committing to a change, explore the problem space to clarify thinking.

### Verify Before Archiving

Use `/opsx:verify` to check implementation matches artifacts. Catches mismatches before you close out the change.

### Name Changes Clearly

Good examples:
- `add-dark-mode`
- `fix-login-redirect`
- `optimize-product-query`
- `implement-2fa`

Avoid:
- `feature-1`
- `update`
- `changes`
- `wip`

### When to Update vs Start Fresh

**Update the existing change when:**
- Same intent, refined execution
- Scope narrows (MVP first, rest later)
- Learning-driven corrections (codebase isn't what you expected)
- Design tweaks based on implementation discoveries

**Start a new change when:**
- Intent fundamentally changed
- Scope exploded to different work entirely
- Original change can be marked "done" standalone
- Patches would confuse more than clarify

---

## 10. Maintaining Context for AI Assistants

### Human + Agent Collaboration

The intended loop:

1. **Human provides**: Intent, context, and constraints
2. **Agent converts**: Into behavior-first requirements and scenarios
3. **Agent keeps**: Implementation detail in `design.md` and `tasks.md`, NOT `spec.md`
4. **Validation confirms**: Structure and clarity before implementation begins

This keeps specs readable for humans and consistent for agents.

### Context Hygiene

- OpenSpec benefits from a clean context window
- Clear your context before starting implementation
- Maintain good context hygiene throughout your session
- Use high-reasoning models (recommended: Opus 4.5, GPT 5.2)

### Schemas Define Workflows

Schemas define artifact types and their dependencies. The default is `spec-driven`:

```yaml
name: spec-driven
artifacts:
  - id: proposal
    generates: proposal.md
    requires: []              # No dependencies

  - id: specs
    generates: specs/**/*.md
    requires: [proposal]

  - id: design
    generates: design.md
    requires: [proposal]

  - id: tasks
    generates: tasks.md
    requires: [specs, design]
```

You can create custom schemas for your team's workflow.

---

## 11. Getting Started

### Installation

```bash
# Requires Node.js 20.19.0 or higher
npm install -g @fission-ai/openspec@latest
```

### Initialize in Project

```bash
cd your-project
openspec init
```

### First Change (Default Path)

```bash
# In your AI assistant:
/opsx:propose add-dark-mode
```

AI will create:
- `openspec/changes/add-dark-mode/`
- `proposal.md`
- `specs/` with delta specs
- `design.md`
- `tasks.md`

Then implement:

```bash
/opsx:apply
```

Finally archive:

```bash
/opsx:archive
```

### CLI Commands

```bash
# List active changes
openspec list

# View change details
openspec show <change-name>

# Validate spec formatting
openspec validate <change-name>

# Interactive dashboard
openspec view

# Update OpenSpec
npm install -g @fission-ai/openspec@latest
openspec update  # Refresh agent instructions
```

---

## 12. Key Concepts Summary

| Term | Definition |
|------|------------|
| **Artifact** | A document within a change (proposal, design, tasks, or delta specs) |
| **Archive** | The process of completing a change and merging its deltas into main specs |
| **Change** | A proposed modification to the system, packaged as a folder with artifacts |
| **Delta spec** | A spec that describes changes (ADDED/MODIFIED/REMOVED) relative to current specs |
| **Domain** | A logical grouping for specs (e.g., `auth/`, `payments/`) |
| **Requirement** | A specific behavior the system must have |
| **Scenario** | A concrete example of a requirement, typically in Given/When/Then format |
| **Schema** | A definition of artifact types and their dependencies |
| **Spec** | A specification describing system behavior, containing requirements and scenarios |
| **Source of truth** | The `openspec/specs/` directory, containing current agreed-upon behavior |

---

## 13. Implementation Checklist for This Project

Based on the existing structure at `/home/marcosgomes/Projects/openspec/`:

- [ ] Run `openspec init` in the project root
- [ ] Review generated `openspec/config.yaml` and customize if needed
- [ ] Organize existing content from `specs/` directory into appropriate domains
- [ ] Convert existing `changes/` content to OpenSpec format if applicable
- [ ] Update project documentation to reference OpenSpec methodology
- [ ] Train team members on OpenSpec workflow
- [ ] Set up AI assistant integration (update skills/prompts)
- [ ] Create first change using `/opsx:propose` workflow
- [ ] Establish team conventions for:
  - Domain organization
  - Change naming
  - Artifact detail level (lite vs full specs)
  - When to use expanded vs core workflow

---

## Resources

- **GitHub**: https://github.com/Fission-AI/OpenSpec
- **Discord**: https://discord.gg/YctCnvvshC
- **Docs**: https://github.com/Fission-AI/OpenSpec/tree/main/docs
- **Email**: teams@openspec.dev (for team access to Slack)

---

*Generated on March 15, 2026*
*Based on OpenSpec main branch documentation*
