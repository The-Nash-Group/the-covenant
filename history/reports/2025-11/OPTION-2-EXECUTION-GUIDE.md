# Option 2: Recommended Cleanup - Execution Guide

**Status**: Ready to Execute
**Created**: 2025-11-22
**Estimated Time**: 10-15 minutes

---

## Quick Start

You have two options:

### Option A: One-Command Execution (Recommended)

```bash
cd /Users/verlyn13/Development/the-nash-group
./execute-option-2.sh
```

This master script orchestrates all steps automatically.

### Option B: Step-by-Step Execution

If you prefer manual control:

```bash
cd /Users/verlyn13/Development/the-nash-group

# Step 1: Remove R/rig (requires sudo)
./cleanup-homebrew-rig.sh

# Step 2: Migrate tools to mise
./migrate-to-mise.sh

# Step 3: Update remaining Homebrew packages
./upgrade-homebrew-remaining.sh
```

---

## What Will Happen

### Phase 1: R/rig Removal (2 minutes)
**Requires**: sudo password

- Uninstalls rig cask
- Removes R.framework
- Removes r-lib/homebrew-rig tap
- **Result**: Eliminates deprecation warnings

### Phase 2: Tool Migration (3-5 minutes)
**No sudo required**

Migrates from Homebrew → mise:
- **pnpm**: Package manager (critical for Nexus monorepo)
- **ruff**: Python linter/formatter
- **biome**: JS/TS formatter (your primary formatter per CLAUDE.md)

**Result**: Aligns with mise-first philosophy

### Phase 3: Homebrew Updates (5-8 minutes)
**No sudo required**

Updates remaining packages:
- System libraries (cmake, ninja, llvm, ffmpeg, etc.)
- CLI tools (awscli, firebase-cli, vercel-cli, etc.)
- Third-party tools (infisical)

**Result**: All packages up to date

---

## After Execution

### 1. Restart Your Shell

**Critical step** - Ensures mise shims are active:

```bash
exec $SHELL
```

Or close and reopen your terminal.

### 2. Verify Tools Work

```bash
# Check versions
pnpm --version    # Should be 10.22.0+
ruff --version    # Should be 0.14.5+
biome --version   # Should be 2.3.6+

# Check locations (should contain 'mise')
which pnpm
which ruff
which biome
```

### 3. Test the-nexus Build

```bash
cd the-nexus
pnpm install
pnpm build
```

If this succeeds, everything is working correctly.

### 4. Review Report

A detailed report will be generated:
```
HOMEBREW-CLEANUP-REPORT-2025-11-22.md
```

This contains:
- Tool migration details
- Homebrew status
- mise configuration
- Verification checklist

---

## Troubleshooting

### Issue: "pnpm: command not found" after migration

**Solution**:
```bash
# Restart shell first
exec $SHELL

# If still not found, manually activate mise
eval "$(mise activate bash)"  # or fish

# Verify mise is in PATH
echo $PATH | grep mise
```

### Issue: Tools still showing Homebrew paths

**Solution**:
```bash
# Check PATH order
echo $PATH

# mise shims should come BEFORE /opt/homebrew/bin
# If not, check your shell config (~/.bashrc or ~/.config/fish/config.fish)

# For fish shell:
mise activate fish | source

# For bash:
eval "$(mise activate bash)"
```

### Issue: Nexus build fails

**Solution**:
```bash
# Clear caches
cd the-nexus
rm -rf node_modules
pnpm store prune

# Reinstall
pnpm install

# Try build again
pnpm build
```

### Issue: Homebrew warnings still appear

**Solution**:
```bash
# Verify rig is completely removed
brew list --cask | grep rig  # Should return nothing
brew tap | grep r-lib        # Should return nothing

# If rig still listed, manually remove
brew untap r-lib/rig --force
```

---

## Expected Output

### Successful Execution

```
=========================================
Option 2: Recommended Homebrew Cleanup
=========================================

==> STEP 1/5: Removing R/rig
✅ R/rig cleanup complete

==> STEP 2/5: Migrating tools to mise
✅ pnpm installed via mise
✅ ruff installed via mise
✅ biome installed via mise
✅ All tools managed by mise!

==> STEP 3/5: Reloading shell environment
✅ mise environment activated

==> STEP 4/5: Updating remaining Homebrew packages
✅ cmake upgraded
✅ ninja upgraded
...
✅ All packages are now up to date!

==> STEP 5/5: Generating cleanup report
✅ Report generated: HOMEBREW-CLEANUP-REPORT-2025-11-22.md

=========================================
Cleanup Complete!
=========================================

⚠️  IMPORTANT: Restart your shell

Duration: 743 seconds
```

---

## Files Created

| File | Purpose | Keep? |
|------|---------|-------|
| `cleanup-homebrew-rig.sh` | R/rig removal | Delete after execution |
| `migrate-to-mise.sh` | Tool migration | Delete after execution |
| `upgrade-homebrew-remaining.sh` | Homebrew updates | Delete after execution |
| `execute-option-2.sh` | Orchestration | Delete after execution |
| `HOMEBREW-CLEANUP-PLAN.md` | Strategy document | Keep for reference |
| `OPTION-2-EXECUTION-GUIDE.md` | This file | Keep for reference |
| `HOMEBREW-CLEANUP-REPORT-*.md` | Execution report | Keep for audit trail |

### Cleanup Command

After successful execution and verification:

```bash
cd /Users/verlyn13/Development/the-nash-group
rm cleanup-homebrew-rig.sh migrate-to-mise.sh upgrade-homebrew-remaining.sh execute-option-2.sh
```

---

## Safety Features

All scripts include:
- ✅ Confirmation prompts before making changes
- ✅ Error handling with descriptive messages
- ✅ Verification steps after each phase
- ✅ Detailed logging of all actions
- ✅ Ability to abort at any time (Ctrl+C)

**No changes are made without your confirmation.**

---

## Pre-flight Checklist

Before running, verify:

- [ ] You're in the correct directory: `/Users/verlyn13/Development/the-nash-group`
- [ ] Scripts are executable: `ls -la *.sh | grep rwx`
- [ ] mise is installed: `which mise`
- [ ] You have sudo password ready (for R/rig removal)
- [ ] No critical work in the-nexus that depends on current tool versions
- [ ] You have time for a 10-15 minute process

---

## Ready to Execute?

**Recommended**:
```bash
cd /Users/verlyn13/Development/the-nash-group
./execute-option-2.sh
```

The script will guide you through each step with clear prompts.

**After completion**: Restart your shell and test tools!

---

**Questions or Issues?**

If anything fails:
1. Check the error message
2. Consult the Troubleshooting section above
3. Review the generated report
4. All scripts are idempotent - safe to re-run

---

*Generated for: Option 2 - Recommended Cleanup*
*Nash Group - the-nash-group repository*
*Aligns with mise-first development philosophy*
