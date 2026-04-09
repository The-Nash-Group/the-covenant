# Organization Root Directory - Cleanup Plan
**Date**: 2025-10-30
**Purpose**: Maintain clean, enterprise-level organizational root directory

---

## Current Issues Identified

### 🚨 **CRITICAL SECURITY CONCERN**
```
covenant-arbiter.2025-08-12.private-key.pem (1,679 bytes)
```
**Issue**: Private key stored in organization root (unencrypted!)
**Risk**: High - Credentials exposed in filesystem
**Action**: Move to secure location or delete if unused

---

## File Classification

### ✅ **Keep in Root** (Essential)

**Organizational Standards**:
- `CLAUDE.md` - Organizational AI context
- `ORGANIZATION-SPEC.md` - Official standards document

**Tooling**:
- `.org/` - Organizational tooling (validators, generators, etc.)
- `.github/` - GitHub workflows and configuration

**Repositories** (rename nexus):
- `the-covenant/` - Philosophy & policies
- `the-citadel/` - Infrastructure as code
- `nexus/` → **the-nexus/** (rename for consistency)
- `the-citadel-archived/` - Historical reference

**Active Scripts**:
- `bootstrap-org.sh` - Organization bootstrap script
- `migrate-repo.sh` - Repository migration tool

---

### 📦 **Archive** (Move to .archive/)

**Bootstrap/Migration Documentation** (15 files):
```
BOOTSTRAP-SUCCESS-REPORT.md
citadel-investigation-20251030.md
investigate-citadel-confusion.sh
proposed-citadel-resolution-plan.md
REPOSITORY-RESTRUCTURE-PLAN.md
REPOSITORY-RESTRUCTURE-SUCCESS-REPORT.md
DEPLOYMENT-CHECKLIST.md
DEPLOYMENT-GUIDE.md
IMPLEMENTATION-PLAN.md
NASH-GROUP-ACTION-PLAN.md
NASH-GROUP-IMPLEMENTATION-PLAN.md
QUICK-START-GUIDE.md
PATH-VERIFICATION-REPORT.md
NAMING-VALIDATION-ANALYSIS.md
VALIDATOR-COMPATIBILITY-REPORT.md
```

**Reason**: Historical value but clutter active workspace

---

### 🗑️ **Delete** (Obsolete/Duplicate)

**Obsolete Documentation** (9 files):
```
THE-CITADEL-SUMMARY.md          # Superseded by the-citadel/README.md
THE-COVENANT-SUMMARY.md         # Superseded by the-covenant/README.md
TheCitadel.md                   # Old documentation
ORG-CLAUDE.md                   # Superseded by CLAUDE.md
ORG-README.md                   # Superseded by ORGANIZATION-SPEC.md
ORGANIZATION-OVERVIEW.md        # Superseded by ORGANIZATION-SPEC.md
READY-TO-DEPLOY.md             # Superseded by success reports
FINAL-VERIFICATION-SUMMARY.md   # Superseded by success report
MASTER-INDEX.md                 # No longer needed
```

**Temporary/Generated Files** (3 files):
```
repo-setup.zip                  # Bootstrap complete, no longer needed
validate-naming-enhanced.sh     # Superseded by .org/tooling/validators/
initial-compliance-audit.txt    # Empty, superseded by audit reports
```

**Reason**: Duplicates existing documentation or no longer relevant

---

### 🖼️ **Move to org-assets/** (New Repository)

**Images** (2 files, 1.2 MB):
```
Gemini_Generated_Image_gfz8dtgfz8dtgfz8.png  (1,183,463 bytes)
nash-group.png                                   (25,609 bytes)
```

**Proposal**: Create `org-assets` repository for:
- Organization logos and branding
- Documentation images
- Marketing materials
- Design assets

**Benefits**:
- Keeps root directory clean
- Version control for assets
- Proper asset management
- Can add CDN later

---

## Recommended Directory Structure

### After Cleanup:

```
the-nash-group/
├── .github/                    # GitHub workflows
├── .org/                       # Organizational tooling
│   ├── tooling/
│   ├── templates/
│   └── schemas/
│
├── the-covenant/               # Philosophy & policies
├── the-citadel/                # Infrastructure as code
├── the-nexus/                  # Operational tooling (renamed)
├── the-citadel-archived/       # Historical reference
│
├── .archive/                   # Historical documentation
│   ├── bootstrap/
│   ├── migration/
│   └── planning/
│
├── CLAUDE.md                   # Org AI context
├── ORGANIZATION-SPEC.md        # Official standards
├── bootstrap-org.sh            # Bootstrap script
└── migrate-repo.sh             # Migration tool
```

**Total Root Files**: 4 (down from 42!)

---

## Implementation Steps

### Phase 1: Security - Handle Private Key ⚠️

```bash
# Option 1: Move to secure location
mkdir -p ~/.ssh/nash-group
mv covenant-arbiter.2025-08-12.private-key.pem ~/.ssh/nash-group/
chmod 600 ~/.ssh/nash-group/covenant-arbiter.2025-08-12.private-key.pem

# Option 2: Delete if no longer needed
# Verify it's not referenced anywhere first
grep -r "covenant-arbiter" . --exclude-dir=.git
# If unused, delete:
rm covenant-arbiter.2025-08-12.private-key.pem
```

### Phase 2: Rename nexus → the-nexus

```bash
# Rename directory
mv nexus the-nexus

# Update references in documentation
find . -type f \( -name "*.md" -o -name "*.sh" \) -exec sed -i '' 's/\bnexus\b/the-nexus/g' {} \;

# Special handling for paths
find . -type f \( -name "*.md" -o -name "*.sh" \) -exec sed -i '' 's|nexus/|the-nexus/|g' {} \;
```

### Phase 3: Create Archive Directory

```bash
# Create archive structure
mkdir -p .archive/{bootstrap,migration,planning}

# Move bootstrap documentation
mv BOOTSTRAP-SUCCESS-REPORT.md .archive/bootstrap/
mv bootstrap-org.sh .archive/bootstrap/  # Keep copy in root too

# Move migration documentation
mv citadel-investigation-20251030.md .archive/migration/
mv investigate-citadel-confusion.sh .archive/migration/
mv proposed-citadel-resolution-plan.md .archive/migration/
mv REPOSITORY-RESTRUCTURE-PLAN.md .archive/migration/
mv REPOSITORY-RESTRUCTURE-SUCCESS-REPORT.md .archive/migration/

# Move planning documentation
mv DEPLOYMENT-CHECKLIST.md .archive/planning/
mv DEPLOYMENT-GUIDE.md .archive/planning/
mv IMPLEMENTATION-PLAN.md .archive/planning/
mv NASH-GROUP-ACTION-PLAN.md .archive/planning/
mv NASH-GROUP-IMPLEMENTATION-PLAN.md .archive/planning/
mv QUICK-START-GUIDE.md .archive/planning/
mv PATH-VERIFICATION-REPORT.md .archive/planning/
mv NAMING-VALIDATION-ANALYSIS.md .archive/planning/
mv VALIDATOR-COMPATIBILITY-REPORT.md .archive/planning/
```

### Phase 4: Create org-assets Repository

```bash
# Create new repository
mkdir org-assets
cd org-assets

# Initialize repository
git init
git checkout -b main

# Create structure
mkdir -p {logos,images,designs,brand}

# Move images
mv ../Gemini_Generated_Image_gfz8dtgfz8dtgfz8.png images/
mv ../nash-group.png logos/

# Create README
cat > README.md << 'EOF'
# org-assets

Organization assets for The Nash Group.

## Structure

- `logos/` - Organization logos and branding
- `images/` - Documentation images and graphics
- `designs/` - Design files and mockups
- `brand/` - Brand guidelines and assets

## Usage

Reference assets using relative paths from repositories:
```markdown
![Nash Group Logo](../org-assets/logos/nash-group.png)
```

## Governance

Asset changes follow Stronghold governance (1 Mentor approval).
EOF

# Commit
git add .
git commit -m "chore: initialize org-assets repository

- Add organization logos
- Add documentation images
- Establish asset management structure

Part of organizational cleanup per enterprise standards"
```

### Phase 5: Remove Obsolete Files

```bash
# Remove obsolete documentation
rm THE-CITADEL-SUMMARY.md
rm THE-COVENANT-SUMMARY.md
rm TheCitadel.md
rm ORG-CLAUDE.md
rm ORG-README.md
rm ORGANIZATION-OVERVIEW.md
rm READY-TO-DEPLOY.md
rm FINAL-VERIFICATION-SUMMARY.md
rm MASTER-INDEX.md

# Remove temporary files
rm repo-setup.zip
rm validate-naming-enhanced.sh
rm initial-compliance-audit.txt
```

### Phase 6: Update .gitignore

```bash
cat >> .gitignore << 'EOF'

# Private keys and secrets
*.pem
*.key
*.p12
*.pfx

# Temporary files
*.tmp
*.log
*.cache

# Archive directory (optional - keep if you want it versioned)
# .archive/
EOF
```

---

## Validation Checklist

After cleanup:

- [ ] Private key moved to secure location or deleted
- [ ] nexus renamed to the-nexus
- [ ] All references to nexus updated to the-nexus
- [ ] Archive directory created with historical docs
- [ ] org-assets repository created
- [ ] Images moved to org-assets
- [ ] Obsolete files deleted
- [ ] .gitignore updated
- [ ] Root directory has only 4-6 files
- [ ] Compliance audit passing

---

## Expected Results

### Before Cleanup
```
Total Files in Root: 42
├── Documentation: 25 files
├── Images: 2 files (1.2 MB)
├── Scripts: 3 files
├── Private Keys: 1 file ⚠️
├── Repositories: 4 directories
└── Config: 7 files
```

### After Cleanup
```
Total Files in Root: 4-6
├── Documentation: 2 files (CLAUDE.md, ORGANIZATION-SPEC.md)
├── Scripts: 2 files (bootstrap-org.sh, migrate-repo.sh)
├── Repositories: 5 directories
└── Config: 2 directories (.org/, .github/)
```

**Reduction**: ~85% fewer files in root
**Security**: Private keys secured
**Organization**: Logical structure established

---

## Benefits

1. **Security**: Private keys moved to secure location
2. **Clarity**: Root directory purpose is clear
3. **Organization**: Logical separation of concerns
4. **Consistency**: the-nexus matches naming convention
5. **Maintainability**: Less clutter, easier navigation
6. **Scalability**: Clean structure for future growth
7. **Enterprise Standards**: Professional organization

---

## Next Steps After Cleanup

1. Update ORGANIZATION-SPEC.md with:
   - Archive directory policy
   - org-assets repository documentation
   - Root directory standards

2. Create ADR documenting:
   - Archive strategy
   - Asset management approach
   - Root directory policy

3. Update compliance validators to check:
   - No private keys in root
   - Limited files in root directory
   - Proper archive structure

---

**Status**: Plan ready for execution
**Risk Level**: Low (all changes reversible)
**Estimated Time**: 45 minutes
**Security Priority**: Critical (handle private key first)
