# Role Mapping Matrix

Cross-reference mapping between governance archetypes, organizational teams, and IAM roles.

**Source**: Extracted from `the-shield/docs/ROLES-AND-POLICIES-ANALYSIS.md` (2026-03-02, organizational consistency audit)
**Authoritative for**: Governance archetype → team mappings
**IAM details**: See `the-shield/docs/iam-roles-analysis.md` for detailed IAM role definitions

---

## Archetypal Hat → Team → IAM Role

| Archetypal Hat | Primary Team | GitHub Permission | IAM Role | Decision Authority |
|----------------|--------------|-------------------|----------|-------------------|
| **The Philosopher** | All Guardians | `read` | N/A (cultural) | Covenant (2W+2M) |
| **The Architect** | Mentors | `maintain` | `tenant_admin`, `citadel_deployer` | Citadel (1M+1W) |
| **The Judge** | Watchers (security), Mentors (technical) | `maintain`/`admin` | `human:watcher`, `human:mentor` | Stronghold (1M), Citadel (1M+1W) |
| **The Gardener** | Mentors, Platform Clan | `maintain` | `tenant_admin`, Bot accounts | Stronghold (1M) |
| **The Explorer** | All Members | `push` (specific repos) | `family_member`, `ai:specialist` | None (propose only) |

## Human Type → IAM Role → Permissions

| Human Type | IAM Role | GitHub Team | Cloud Permissions | Governance |
|------------|----------|-------------|------------------|-----------|
| **Owner** | `human:owner:jeffrey` | @owners | Full (break-glass) | Covenant override |
| **Security Guardian** | `human:watcher:security` | @watchers | Audit logs, security | Citadel+Covenant review |
| **Technical Lead** | `human:mentor:platform` | @mentors, @platform-clan | Domain-specific | Citadel review |
| **Family Admin** | `human:family_admin` | N/A | `family:*:*` | Family governance |
| **Family Member** | `human:family_member` | N/A | `family:{photos,calendar}:view` | None |
| **Child** | `human:family_child` | N/A | `family:education:*` (time-limited) | Parental approval |

---

**Related documents**:
- `HUMAN_MANDATE.md` — Guardian archetype definitions
- `GOVERNANCE.md` — Decision authority matrix
- `the-shield/docs/iam-roles-analysis.md` — IAM role details and service type mappings
