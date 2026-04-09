# Homebrew Cleanup & Optimization Plan

**Generated**: 2025-11-22
**Repository**: the-nash-group
**Purpose**: Resolve Homebrew warnings, align with mise-first philosophy, optimize tooling

---

## Executive Summary

**Issues Identified**:
1. ✅ **READY**: R/rig deprecation warnings (cleanup script created)
2. ⚠️ **CONFLICT**: Duplicate tools managed by both Homebrew and mise
3. 📦 **OUTDATED**: 21 Homebrew formulae need updates
4. 📝 **DOCUMENTATION**: macOS version mismatch in CLAUDE.md

---

## Issue 1: R/rig Cleanup (Manual Action Required)

### Status: Cleanup Script Ready

**Action Required**:
```bash
# Review and execute the cleanup script
cd /Users/verlyn13/Development/the-nash-group
./cleanup-homebrew-rig.sh
```

**What it does**:
- Removes rig cask (R Installation Manager)
- Removes r-lib/homebrew-rig tap
- Removes R.framework and binaries
- Eliminates deprecation warnings

**Verification**:
```bash
# After running the script, verify warnings are gone
brew update
brew doctor
```

---

## Issue 2: Homebrew/mise Conflicts

### Philosophy Violation Detected

Per your `~/.claude/CLAUDE.md`:
> **Runtime Management (mise)**: All language runtimes, CLI tools, and version management through mise

### Current Conflicts

| Tool | Homebrew Version | mise Version | Recommended Action |
|------|------------------|--------------|-------------------|
| **pnpm** | 10.22.0 | 10.17.1 (global) | Keep in mise, remove from Homebrew |
| **ruff** | 0.14.5 | 0.14.0 (global) | Keep in mise, remove from Homebrew |

### Analysis

**pnpm Conflict**:
- Homebrew has newer version (10.22.0 vs 10.17.1)
- Currently using Homebrew version: `which pnpm` likely points to `/opt/homebrew/bin/pnpm`
- Nexus project requires pnpm (monorepo tool)
- **Recommendation**: Update mise to latest, remove from Homebrew

**ruff Conflict**:
- Homebrew has newer version (0.14.5 vs 0.14.0)
- Your CLAUDE.md explicitly mentions using ruff
- **Recommendation**: Update mise to latest, remove from Homebrew

### Resolution Steps

```bash
# 1. Update mise versions to latest
mise install pnpm@latest
mise use -g pnpm@latest

mise install ruff@latest
mise use -g ruff@latest

# 2. Verify mise versions are active
which pnpm  # Should show ~/.local/share/mise/installs/...
which ruff  # Should show ~/.local/share/mise/installs/...
pnpm --version  # Should show 10.22.0 or newer
ruff --version  # Should show 0.14.5 or newer

# 3. Remove from Homebrew
brew uninstall pnpm
brew uninstall ruff

# 4. Verify still accessible via mise
pnpm --version
ruff --version
```

---

## Issue 3: Homebrew Tools Assessment

### Category A: Keep in Homebrew (System-level dependencies)

These are typically build dependencies or system-level tools that don't fit mise's model:

| Tool | Current | Latest | Purpose | Action |
|------|---------|--------|---------|--------|
| cmake | Outdated | Latest | Build system | Update |
| ninja | Outdated | Latest | Build system | Update |
| llvm | Outdated | Latest | Compiler infrastructure | Update |
| ffmpeg | Outdated | Latest | Media processing | Update |
| gnutls | Outdated | Latest | TLS library | Update |
| libomp | Outdated | Latest | OpenMP runtime | Update |
| librist | Outdated | Latest | Video streaming | Update |
| mbedtls | Outdated | Latest | Crypto library | Update |

**Rationale**: These are system libraries and build tools, not application runtimes. They should stay in Homebrew.

**Update Command**:
```bash
brew upgrade cmake ninja llvm ffmpeg gnutls libomp librist mbedtls
```

---

### Category B: Evaluate for mise Migration

These CLI tools COULD be managed by mise per your philosophy:

| Tool | Current | Purpose | mise Support? | Recommendation |
|------|---------|---------|---------------|----------------|
| awscli | 2.32.1 | AWS CLI | ❌ No | Keep in Homebrew |
| firebase-cli | Outdated | Firebase CLI | ✅ Yes (npm) | Migrate to mise |
| gemini-cli | Outdated | Google Gemini | ❓ Unknown | Keep in Homebrew |
| vercel-cli | Outdated | Vercel deployment | ✅ Yes (npm) | Migrate to mise |
| nx | Outdated | Monorepo tool | ✅ Yes (npm) | Migrate to mise |
| uv | Outdated | Python packaging | ✅ Yes | Evaluate migration |
| rclone | Outdated | Cloud sync | ❌ No | Keep in Homebrew |
| trufflehog | 3.91.0 | Secret scanning | ❌ No | Keep in Homebrew |
| php | Outdated | PHP runtime | ✅ Yes | Evaluate if needed |

#### Firebase CLI Migration
```bash
# If using Firebase, migrate to mise
mise install "npm:firebase-tools@latest"
mise use -g "npm:firebase-tools@latest"
brew uninstall firebase-cli
```

#### Vercel CLI Migration
```bash
# If using Vercel, migrate to mise
mise install "npm:vercel@latest"
mise use -g "npm:vercel@latest"
brew uninstall vercel-cli
```

#### Nx Migration
```bash
# If using Nx directly (not via pnpm), migrate to mise
mise install "npm:nx@latest"
mise use -g "npm:nx@latest"
brew uninstall nx
```

#### PHP Evaluation
```bash
# Check if PHP is actually used
grep -r "php" the-nexus/ the-citadel/ the-covenant/ --include="*.md" --include="*.yml" --include="*.sh" | head -20

# If not used, remove
brew uninstall php

# If used, migrate to mise
mise install php@latest
mise use -g php@latest
```

---

### Category C: Third-party Taps (Keep & Update)

| Tool | Tap | Purpose | Action |
|------|-----|---------|--------|
| infisical | infisical/get-cli | Secrets management | Update |

**Rationale**: Specialized tools from third-party taps, reasonable to keep in Homebrew.

**Update Command**:
```bash
brew upgrade infisical/get-cli/infisical
```

---

### Category D: Biome (Critical Tool)

**Current Status**:
- Installed: biome 2.3.6 (Homebrew)
- mise support: ✅ Available via npm
- Usage: **CRITICAL** - Mentioned explicitly in your CLAUDE.md as replacement for Prettier

**Your CLAUDE.md States**:
> **Formatter**: Biome (v2.3+) - USE THIS, NOT PRETTIER

**Recommendation**: Migrate to mise for version consistency

```bash
# Migrate biome to mise
mise install "npm:@biomejs/biome@latest"
mise use -g "npm:@biomejs/biome@latest"

# Verify
which biome
biome --version

# Remove from Homebrew
brew uninstall biome
```

---

## Issue 4: Documentation Update

### macOS Version Mismatch

**Current System**:
```
ProductName: macOS
ProductVersion: 26.1
BuildVersion: 25B78
```

**Your CLAUDE.md States**:
> **OS**: macOS 15 Sequoia (Darwin 25.0.0)

**Analysis**: You're running macOS 26.1 (likely beta/preview of macOS 16, successor to Sequoia).

**Action**: Update `~/.claude/CLAUDE.md`

```markdown
## System Configuration
- **OS**: macOS 26.1 Beta (Darwin 25.1.0)
- **Shell**: Fish (primary), Bash (compatibility)
...
```

---

## Comprehensive Cleanup Script

I can create an automated script to handle all of this, or you can execute step-by-step. Which do you prefer?

### Option 1: Automated (Recommended)

Create `cleanup-homebrew-comprehensive.sh` that:
1. Migrates pnpm, ruff, biome to mise
2. Optionally migrates firebase-cli, vercel-cli, nx
3. Updates remaining Homebrew packages
4. Verifies all tools still accessible
5. Generates report

### Option 2: Manual Step-by-Step

Follow this checklist in order:

- [ ] 1. Execute `./cleanup-homebrew-rig.sh` (requires sudo)
- [ ] 2. Migrate pnpm to mise, remove from Homebrew
- [ ] 3. Migrate ruff to mise, remove from Homebrew
- [ ] 4. Migrate biome to mise, remove from Homebrew
- [ ] 5. Evaluate PHP usage, remove if unused
- [ ] 6. Update system-level Homebrew packages (cmake, ninja, etc.)
- [ ] 7. Update third-party tools (infisical)
- [ ] 8. Verify all tools accessible: `brew doctor`
- [ ] 9. Update `~/.claude/CLAUDE.md` with correct macOS version
- [ ] 10. Document changes in Nash Group repo

---

## Expected Outcomes

After completion:

✅ **No deprecation warnings** - rig/R removed
✅ **Aligned with mise-first philosophy** - CLI tools managed consistently
✅ **Up-to-date packages** - Security and feature updates applied
✅ **Reduced duplication** - Single source of truth for tool versions
✅ **Accurate documentation** - CLAUDE.md reflects reality

---

## Next Steps

**Choose your path**:

1. **Quick Fix (Minimal)**:
   - Run `./cleanup-homebrew-rig.sh`
   - Run `brew upgrade` for all outdated packages
   - Call it done

2. **Recommended (Aligned with Philosophy)**:
   - Run `./cleanup-homebrew-rig.sh`
   - Migrate pnpm, ruff, biome to mise
   - Update remaining Homebrew packages
   - Update CLAUDE.md

3. **Comprehensive (Gold Standard)**:
   - All of the above
   - Audit PHP usage
   - Migrate optional tools (firebase, vercel, nx if used)
   - Document all changes
   - Create ADR documenting the cleanup

**What would you like me to do?**
