# OFFICIAL SITE REPOSITORY - IMPLEMENTATION PLAN
**Status**: Planning Document
**Classification**: INFRASTRUCTURE // IMPLEMENTATION
**Created**: 2025-11-21
**Governance Level**: Citadel (1 Mentor + 1 Watcher)

──────────────────────────────────────────────────────────────

## PURPOSE

This document defines the complete plan for implementing The Nash Group official website as a new repository within the organization's infrastructure, adhering to ALL established specifications, standards, and governance requirements.

**Primary References**:
- `nash-site-spec-approved.md` - Architectural specification v2.0
- `nash-site-implementation.md` - Technical implementation guide v2.1
- `nash-site-style-guide.md` - Institutional aesthetic standards
- `PUBLIC-FACING-INSTITUTIONAL-SPEC.md` - Public identity framework
- `ORGANIZATION-SPEC.md` - Organizational structure and naming
- `the-citadel/terraform/` - Infrastructure as Code patterns

──────────────────────────────────────────────────────────────

## I. REPOSITORY SPECIFICATION

### 1.1 Repository Naming (Per ORGANIZATION-SPEC.md)

**Repository Name**: `the-tartan`

**Rationale**:
- **Highlander Lore**: A tartan is the distinctive clan pattern - how a clan is recognized
- **Uniqueness**: "The unique and probably only pure public presence" - a tartan identifies which clan you belong to
- **Public Identity**: A tartan is what others see - perfect metaphor for public-facing site
- **Visual Alignment**: The institutional grid system literally resembles a tartan pattern
- **Cultural Weight**: Tartans have centuries of history, implying permanence and tradition
- **Institutional Authority**: Formal, traditional, authoritative - not casual or modern
- **Lore Translation**: "The Tartan" = Public identity / Clan recognition pattern

**Reserved Alternative**: `the-observatory` (better suited for internal telemetry/observability infrastructure)

**Governance Decision**: Name approved

### 1.2 Repository Metadata

```hcl
resource "github_repository" "the_tartan" {
  name        = "the-tartan"
  description = "🏴󠁧󠁢󠁳󠁣󠁴󠁿 The Clan Pattern - The distinctive public identity and institutional presence of The Nash Group"

  visibility = "public"  # Public site = public repository

  has_issues      = true
  has_discussions = false  # Internal team communication only
  has_projects    = true
  has_wiki        = false  # Documentation lives in repo
  has_downloads   = true

  vulnerability_alerts = true

  # Merge settings (enforce linear history)
  allow_merge_commit     = false
  allow_squash_merge     = true
  allow_rebase_merge     = false
  allow_auto_merge       = false
  delete_branch_on_merge = true

  squash_merge_commit_title   = "PR_TITLE"
  squash_merge_commit_message = "PR_BODY"

  # Cloudflare Pages integration
  homepage_url = "https://thenash.group"

  topics = [
    "astro",
    "wasm",
    "rust",
    "institutional",
    "cloudflare-pages",
    "tartan",
    "public-identity"
  ]

  # Pages configuration (Cloudflare handles actual hosting)
  pages {
    source {
      branch = "main"
      path   = "/dist"  # Astro build output
    }
  }
}
```

### 1.3 Required Repository Files (Per ORGANIZATION-SPEC.md)

```
the-tartan/
├── README.md                 # REQUIRED: Institutional format
├── CONTRIBUTING.md           # REQUIRED: Contribution guidelines
├── LICENSE                   # REQUIRED: License file
├── CHANGELOG.md              # REQUIRED: Change history
├── .gitignore               # REQUIRED: Git ignore rules
├── .editorconfig            # REQUIRED: Editor configuration
└── CLAUDE.md                # REQUIRED: AI assistant context
```

──────────────────────────────────────────────────────────────

## II. GITHUB CONFIGURATION

### 2.1 Branch Protection (Rulesets)

**The Great Charter** (already defined in `rulesets.tf`):
- Applies to: `main` branch
- Linear history required
- Force push disabled
- Deletion disabled
- PR reviews: 1 required
- Dismiss stale reviews: enabled

**Covenant of Commits** (already defined):
- Conventional commit format enforced
- Pattern: `^(feat|fix|docs|chore|refactor|perf|test|build|ci|revert)(\\(.+\\))?: .+`

**Additional Observatory-Specific Rule**:
- Build must pass before merge
- Deployment preview must be successful

### 2.2 GitHub Actions Workflows

**Required Workflows**:

1. **`.github/workflows/build-and-deploy.yml`**
   - Trigger: Push to `main`
   - Jobs:
     - Build Rust WASM module
     - Build Astro site
     - Deploy to Cloudflare Pages
   - Secrets required:
     - `CLOUDFLARE_API_TOKEN`
     - `CLOUDFLARE_ACCOUNT_ID`

2. **`.github/workflows/preview.yml`**
   - Trigger: Pull request
   - Jobs:
     - Build site
     - Deploy to preview environment
     - Comment PR with preview URL

3. **`.github/workflows/security-scan.yml`**
   - Trigger: Push, PR, weekly schedule
   - Jobs:
     - `npm audit`
     - `cargo audit`
     - Dependabot alerts review

4. **`.github/workflows/lighthouse.yml`**
   - Trigger: After deployment
   - Jobs:
     - Run Lighthouse audit
     - Verify 100/100/100/100 scores
     - Fail if below threshold

### 2.3 CODEOWNERS

```
# Default owners for all files
* @the-nash-group/watchers

# Observatory-specific ownership
/src/                  @the-nash-group/mentors
/src/rust/             @the-nash-group/watchers  # WASM security critical
/terraform/            @the-nash-group/watchers  # Infrastructure critical
/src/styles/           @the-nash-group/mentors
/public/               @the-nash-group/mentors

# Documentation
/docs/                 @the-nash-group/mentors
*.md                   @the-nash-group/mentors

# Configuration
astro.config.mjs       @the-nash-group/watchers
package.json           @the-nash-group/watchers
Cargo.toml             @the-nash-group/watchers
```

──────────────────────────────────────────────────────────────

## III. PROJECT STRUCTURE

### 3.1 Directory Structure (Compliant with ORGANIZATION-SPEC.md)

```
the-tartan/
├── README.md                           # Institutional format
├── CONTRIBUTING.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── .editorconfig
├── CLAUDE.md                           # AI context
├── package.json
├── pnpm-lock.yaml
├── astro.config.mjs
├── tsconfig.json
├── biome.json                          # Code formatting
│
├── src/                                # Source code
│   ├── components/                     # Astro components
│   │   ├── SessionMonitor.astro
│   │   ├── StatusIndicator.astro
│   │   ├── LegalFooter.astro
│   │   └── AccessNotice.astro
│   ├── layouts/
│   │   └── InstitutionalLayout.astro
│   ├── pages/
│   │   ├── index.astro                 # Home
│   │   ├── capabilities.astro          # What we do
│   │   ├── governance.astro            # How we operate
│   │   ├── access.astro                # Contact/access
│   │   └── 404.astro                   # Error page
│   ├── lib/                            # TypeScript utilities
│   │   ├── session-engine.ts           # WASM interface
│   │   └── surveillance.ts             # Monitoring system
│   ├── styles/
│   │   └── institutional.css           # CSS framework
│   └── rust/                           # Rust session engine
│       ├── Cargo.toml
│       ├── Cargo.lock
│       └── src/
│           └── lib.rs
│
├── public/                             # Static assets
│   ├── favicon.svg
│   ├── robots.txt
│   └── _headers                        # Cloudflare headers
│
├── terraform/                          # Infrastructure
│   ├── main.tf                         # Zone & DNS
│   ├── variables.tf
│   ├── outputs.tf
│   └── backend.tf                      # R2 state
│
├── docs/                               # Documentation
│   ├── architecture/
│   │   └── 001-hermetic-institutionalism.md
│   ├── deployment/
│   │   └── cloudflare-pages.md
│   └── operations/
│       └── monitoring.md
│
├── scripts/                            # Build scripts
│   ├── build-wasm.sh
│   ├── deploy.sh
│   └── validate-compliance.sh
│
├── tests/                              # Tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
└── .github/                            # GitHub config
    ├── workflows/
    │   ├── build-and-deploy.yml
    │   ├── preview.yml
    │   ├── security-scan.yml
    │   └── lighthouse.yml
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── pull_request_template.md
```

### 3.2 File Naming Compliance

**Per ORGANIZATION-SPEC.md**:
- Documentation: `UPPERCASE.md` (README.md, CONTRIBUTING.md)
- TypeScript/JavaScript: `kebab-case.ts` (session-engine.ts)
- Rust: `snake_case.rs` (lib.rs per Rust convention)
- Scripts: `kebab-case.sh` (build-wasm.sh)
- Astro components: `PascalCase.astro` (SessionMonitor.astro)

──────────────────────────────────────────────────────────────

## IV. CLOUDFLARE INFRASTRUCTURE

### 4.1 Domain Configuration

**Primary Domain**: `thenash.group`
**Zone ID**: `[TO BE DETERMINED]`
**Cloudflare Plan**: Pro (minimum for Cloudflare Pages)

**Required DNS Records**:
```hcl
# Root domain (Cloudflare Pages)
resource "cloudflare_record" "root" {
  zone_id = var.zone_id
  name    = "@"
  content  = "the-tartan.pages.dev"  # Cloudflare Pages CNAME
  type    = "CNAME"
  proxied = true
  comment = "The Tartan - Public Identity"
}

# WWW redirect
resource "cloudflare_record" "www" {
  zone_id = var.zone_id
  name    = "www"
  content  = "the-tartan.pages.dev"
  type    = "CNAME"
  proxied = true
  comment = "The Tartan - WWW Redirect"
}
```

### 4.2 Cloudflare Pages Configuration

**Project Name**: `the-tartan`
**Build Configuration**:
```yaml
Production branch: main
Build command: pnpm run build
Build output directory: /dist
Root directory: /
Node version: 24
Environment variables:
  - NODE_VERSION: 24
  - PNPM_VERSION: 9
```

**Preview Configuration**:
- Enable preview deployments for all branches
- Preview URL pattern: `{branch}.the-tartan.pages.dev`

### 4.3 Zero Trust Security (Per standard_zone module)

**Applied via Module**:
```hcl
module "thenash_group_zone" {
  source = "./modules/standard_zone"

  zone_id = var.thenash_group_zone_id
  domain  = "thenash.group"

  enable_under_attack_mode = false  # Default: medium security
  enable_bot_management    = false  # Requires Enterprise
}
```

**Security Features Applied**:
- SSL: Strict (Full SSL with valid certificate)
- Always Use HTTPS: Enabled
- Min TLS Version: 1.2
- TLS 1.3: Enabled
- HSTS: Enabled (1 year max-age, includeSubDomains, preload)
- WAF: Cloudflare Managed Ruleset + OWASP Core Ruleset
- Browser Integrity Check: Enabled
- Security Level: Medium (escalate to "Under Attack" if needed)

### 4.4 Additional Cloudflare Configuration

**Headers** (via `public/_headers`):
```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'
```

**Cache Rules**:
```hcl
resource "cloudflare_ruleset" "cache_rules" {
  zone_id     = var.zone_id
  name        = "Tartan Cache Rules"
  kind        = "zone"
  phase       = "http_request_cache_settings"

  rules {
    action = "set_cache_settings"
    action_parameters {
      cache = true
      browser_ttl {
        mode = "override_origin"
        default = 14400  # 4 hours
      }
      edge_ttl {
        mode = "override_origin"
        default = 3600   # 1 hour for HTML
      }
    }
    expression = "(http.request.uri.path matches \".*\\.html$\") or (http.request.uri.path eq \"/\")"
    description = "Cache HTML pages for 1 hour"
    enabled = true
  }

  rules {
    action = "set_cache_settings"
    action_parameters {
      cache = true
      edge_ttl {
        mode = "override_origin"
        default = 31536000  # 1 year for immutable assets
      }
    }
    expression = "(http.request.uri.path matches \".*\\.(css|js|wasm|woff2|svg)$\")"
    description = "Cache static assets for 1 year (hashed filenames)"
    enabled = true
  }
}
```

**Rate Limiting**:
```hcl
resource "cloudflare_rate_limit" "tartan_general" {
  zone_id   = var.zone_id
  threshold = 100
  period    = 60
  action {
    mode    = "challenge"
    timeout = 3600
  }
  match {
    request {
      url_pattern = "thenash.group/*"
    }
  }
  description = "General rate limit: 100 requests per minute"
}
```

### 4.5 DNSSEC (Per technical advisory)

**Requirement**: DNSSEC MUST be enabled

**Verification**:
```bash
dig +dnssec thenash.group | grep "ad"
# Should show "ad" flag (authenticated data)
```

**Terraform Configuration**:
```hcl
resource "cloudflare_zone_dnssec" "thenash_group" {
  zone_id = var.zone_id
}
```

### 4.6 Geo-Blocking (Per technical advisory)

**High-Risk Countries Blocked**:
- North Korea (KP)
- Iran (IR)
- Syria (SY)
- Cuba (CU)
- Russia (RU) - If required by sanctions
- China (CN) - If excessive bot traffic

**Implementation**:
```hcl
resource "cloudflare_filter" "block_high_risk_countries" {
  zone_id     = var.zone_id
  description = "Block high-risk countries per security policy"
  expression  = "(ip.geoip.country in {\"KP\" \"IR\" \"SY\" \"CU\"})"
}

resource "cloudflare_firewall_rule" "block_high_risk" {
  zone_id     = var.zone_id
  description = "Block traffic from high-risk countries"
  filter_id   = cloudflare_filter.block_high_risk_countries.id
  action      = "block"
  priority    = 1
}
```

──────────────────────────────────────────────────────────────

## V. TERRAFORM STATE MANAGEMENT

### 5.1 State Backend (Cloudflare R2)

**Per technical advisory**: Use R2 for state sovereignty

```hcl
# terraform/backend.tf
terraform {
  backend "s3" {
    bucket = "nash-group-terraform-state"
    key    = "the-tartan/terraform.tfstate"
    region = "auto"

    endpoints = {
      s3 = "https://<account-id>.r2.cloudflarestorage.com"
    }

    skip_credentials_validation = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
    skip_metadata_api_check     = true
    skip_s3_checksum            = true
  }
}
```

**R2 Bucket Configuration** (in `the-citadel/terraform/`):
```hcl
resource "cloudflare_r2_bucket" "terraform_state" {
  account_id = var.cloudflare_account_id
  name       = "nash-group-terraform-state"
  location   = "WNAM"  # Western North America
}

# Access via API tokens (not long-lived credentials)
```

### 5.2 State Encryption

**Requirement**: State file must be encrypted

**R2 Configuration**:
- Server-side encryption: Enabled (AES-256)
- Access: API token only (stored in GitHub Secrets)
- Versioning: Enabled for rollback capability

──────────────────────────────────────────────────────────────

## VI. COMPLIANCE VERIFICATION

### 6.1 Institutional Specification Compliance

**Public-Facing Content** (Per PUBLIC-FACING-INSTITUTIONAL-SPEC.md):

**README.md Format**:
```markdown
# UNIT: THE-TARTAN
**Classification:** PUBLIC // IDENTITY
**Status:** OPERATIONAL

──────────────────────────────────────────────────────────────

## >> OPERATIONAL DIRECTIVE
The Tartan serves as the distinctive public identity pattern and
institutional presence for The Nash Group.

## >> REQUIREMENTS
| COMPONENT | VERSION |
|:----------|:--------|
| node      | 24.x    |
| pnpm      | 9.x     |
| rust      | 1.75+   |

## >> USAGE
```
pnpm install
pnpm run build
pnpm run dev
```

## >> NOTICE
This pattern is calibrated for external recognition. Internal
operations are documented separately.

──────────────────────────────────────────────────────────────
```

**Language Compliance** (Per nash-site-style-guide.md):
- Passive voice throughout
- No forbidden vocabulary ("excited," "passionate," etc.)
- Approved vocabulary only ("operations," "protocols," "enforcement")
- All Highlander lore translated to corporate euphemisms

### 6.2 Visual Standards Compliance

**Typography** (Per specification):
- IBM Plex Sans: All UI text
- IBM Plex Mono: All data/code
- Headers: UPPERCASE, letter-spacing: 0.1em

**Colors**:
- Background: #FFFFFF
- Text: #000000
- Borders: #E5E5E5
- Status Active: #00FF41
- Status Alert: #FF0000

**Layout**:
- 8px grid system
- Content max-width: 72ch
- No rounded corners
- No box shadows
- 1px solid borders

**Cursors**:
- Body: `crosshair`
- Links/Buttons: `help`

### 6.3 Security Compliance Checklist

```
DNS Security:
[ ] DNSSEC enabled
[ ] `dig +dnssec` shows AD flag
[ ] Nameservers properly configured

Access Control:
[ ] Geo-blocking active (KP, IR, SY, CU)
[ ] WAF rules enabled (Cloudflare Managed + OWASP)
[ ] Rate limiting configured (100 req/min)
[ ] Test with VPN from blocked countries

Headers & CSP:
[ ] HSTS enabled (max-age: 31536000)
[ ] CSP configured (script-src: 'self' 'wasm-unsafe-eval')
[ ] X-Frame-Options: DENY
[ ] Referrer-Policy: no-referrer
[ ] securityheaders.com shows A+ rating

State Management:
[ ] Terraform state in R2
[ ] State file encrypted (AES-256)
[ ] Backup procedures documented
[ ] Access restricted via API tokens

WASM Security:
[ ] Module properly hashed
[ ] MIME type correct (application/wasm)
[ ] Loaded over HTTPS only
[ ] Console logging active
```

──────────────────────────────────────────────────────────────

## VII. IMPLEMENTATION PHASES

### Phase 1: Repository Creation (Day 1)

**Tasks**:
- [ ] Create GitHub repository `the-tartan`
- [ ] Apply repository settings (visibility, features, protection)
- [ ] Create initial directory structure
- [ ] Add required files (README, CONTRIBUTING, LICENSE, etc.)
- [ ] Configure branch protection rules
- [ ] Add CODEOWNERS file
- [ ] Configure GitHub Actions secrets

**Terraform Changes**:
```bash
cd the-citadel/terraform
# Add to repositories.tf
# Run: terraform plan
# Review plan
# Apply: terraform apply
```

**Deliverable**: Empty repository with proper configuration

### Phase 2: Infrastructure Setup (Days 2-3)

**Tasks**:
- [ ] Configure Cloudflare R2 bucket for Terraform state
- [ ] Setup Cloudflare Pages project
- [ ] Configure domain DNS records
- [ ] Enable DNSSEC
- [ ] Apply standard_zone module (WAF, SSL, headers)
- [ ] Configure geo-blocking rules
- [ ] Setup rate limiting
- [ ] Configure cache rules

**Terraform Changes**:
```bash
cd the-tartan/terraform
terraform init  # Initialize with R2 backend
terraform plan
terraform apply
```

**Deliverable**: Infrastructure ready for deployment

### Phase 3: Core Development (Week 1)

**Tasks**:
- [ ] Initialize Astro project
- [ ] Install dependencies (vite-plugin-wasm, IBM Plex fonts)
- [ ] Setup Rust session engine
- [ ] Build WASM module
- [ ] Create TypeScript surveillance system
- [ ] Implement institutional CSS framework
- [ ] Build Astro components (per specification)
- [ ] Create all pages (index, capabilities, governance, access, 404)

**Deliverable**: Functional local development environment

### Phase 4: Testing & Refinement (Week 2)

**Tasks**:
- [ ] Unit tests for session engine
- [ ] Integration tests for surveillance
- [ ] E2E tests for critical flows
- [ ] Visual standards compliance audit
- [ ] Content standards compliance audit
- [ ] Performance testing (Lighthouse 100/100/100/100)
- [ ] Security audit (securityheaders.com A+)

**Deliverable**: Production-ready codebase

### Phase 5: Deployment (Week 3)

**Tasks**:
- [ ] Deploy to Cloudflare Pages (production)
- [ ] Verify DNSSEC
- [ ] Test geo-blocking
- [ ] Verify WAF rules
- [ ] Test rate limiting
- [ ] Run full security verification
- [ ] Monitor for 24 hours
- [ ] Document any issues

**Deliverable**: Live production site at https://thenash.group

──────────────────────────────────────────────────────────────

## VIII. GOVERNANCE & APPROVAL

### 8.1 Decision Authority

**Repository Creation**: Citadel Level (1 Mentor + 1 Watcher)

**Rationale**: Infrastructure change affecting organization presence

### 8.2 Approval Checklist

**Pre-Implementation**:
- [x] This plan reviewed by assigned Mentor
- [x] This plan reviewed by assigned Watcher
- [x] Repository name approved (`the-tartan`)
- [ ] Budget approved (Cloudflare Pro plan)
- [ ] Timeline approved

**Post-Implementation**:
- [ ] Site live and functional
- [ ] All security tests passing
- [ ] Performance targets met
- [ ] Documentation complete
- [ ] Team trained on maintenance

### 8.3 Rollback Plan

**If deployment fails**:
1. Revert DNS to parked domain
2. Delete Cloudflare Pages project
3. Archive GitHub repository
4. Document failure reasons
5. Create post-mortem ADR

**State Rollback**:
```bash
# R2 versioning allows state recovery
cd the-tartan/terraform
terraform state pull > backup.tfstate
terraform state push backup-previous.tfstate
```

──────────────────────────────────────────────────────────────

## IX. OPERATIONAL PROCEDURES

### 9.1 Deployment Process

**Standard Deployment** (via GitHub Actions):
```
1. PR created → Preview deployment to `{branch}.the-tartan.pages.dev`
2. PR reviewed → Mentor approval required
3. PR merged to main → Automatic production deployment
4. Lighthouse audit runs → Must pass 100/100/100/100
5. Site live at https://thenash.group
```

**Emergency Deployment** (manual):
```bash
# Build locally
pnpm run build

# Deploy via wrangler
npx wrangler pages deploy dist --project-name=the-tartan
```

### 9.2 Monitoring

**Daily**:
- Cloudflare Analytics review
- Error log review
- Security alerts check

**Weekly**:
- WAF event log review
- Rate limit trigger analysis
- Performance metrics review

**Monthly**:
- Dependency updates (npm, cargo)
- WASM module rebuild
- Security audit (npm audit, cargo audit)
- Lighthouse audit baseline

### 9.3 Incident Response

**DDoS Attack**:
1. Enable "Under Attack Mode" in Cloudflare
2. Review WAF logs for patterns
3. Adjust rate limiting if needed
4. Document in incident log

**Content Issue**:
1. Hotfix PR created
2. Expedited review (< 1 hour)
3. Merge and deploy
4. Post-mortem within 24 hours

**Infrastructure Failure**:
1. Check Cloudflare status page
2. Verify DNS resolution
3. Check Pages deployment logs
4. Rollback to previous deployment if needed

──────────────────────────────────────────────────────────────

## X. SUCCESS CRITERIA

The Tartan implementation is considered successful when:

1. ✅ Repository created and configured per specifications
2. ✅ Cloudflare infrastructure deployed (DNS, Pages, WAF)
3. ✅ DNSSEC enabled and validated
4. ✅ Geo-blocking active and tested
5. ✅ Site live at https://thenash.group
6. ✅ Lighthouse scores: 100/100/100/100
7. ✅ Security Headers rating: A+
8. ✅ Visual standards 100% compliant
9. ✅ Content standards 100% compliant
10. ✅ All documentation complete
11. ✅ Team trained on operations
12. ✅ 30-day stability period with no critical issues

──────────────────────────────────────────────────────────────

## XI. BUDGET & RESOURCES

**Cloudflare Costs**:
- Pro Plan: $20/month (thenash.group domain)
- R2 Storage: ~$0.015/GB/month (Terraform state)
- R2 Requests: Minimal (state operations only)
- Pages: Free (included in Pro)

**Development Time**:
- Phase 1: 1 day (repository setup)
- Phase 2: 2 days (infrastructure)
- Phase 3: 5 days (development)
- Phase 4: 5 days (testing)
- Phase 5: 2 days (deployment)
- **Total**: ~15 working days (3 weeks)

**Personnel**:
- 1 Mentor (technical oversight)
- 1 Watcher (security oversight)
- 1 Developer (implementation)

──────────────────────────────────────────────────────────────

## XII. REFERENCES

**Specifications**:
- `official-site-plan-approved.md` - Deliverables index
- `nash-site-spec-approved.md` - Architecture v2.0
- `nash-site-implementation.md` - Technical guide v2.1
- `nash-site-style-guide.md` - Institutional aesthetic
- `nash-site-technical-advisory.md` - Security refinements
- `PUBLIC-FACING-INSTITUTIONAL-SPEC.md` - Public identity

**Infrastructure**:
- `the-citadel/terraform/providers/cloudflare/modules/standard_zone/` - Security baseline
- `the-citadel/terraform/repositories.tf` - Repository patterns
- `the-citadel/terraform/rulesets.tf` - Branch protection

**Organizational**:
- `ORGANIZATION-SPEC.md` - Structure and naming
- `the-covenant/PRINCIPLES.md` - Core principles
- `the-covenant/GOVERNANCE.md` - Decision authority

──────────────────────────────────────────────────────────────

**Status**: READY FOR APPROVAL
**Next Step**: Citadel Governance Approval (1M+1W)
**Implementation Start**: Upon approval

*Operations are conducted with precision. Continuity is enforced.*
