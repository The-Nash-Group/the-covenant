# Secrets Management Specification

**Version:** 1.3.0
**Status:** ACTIVE
**Date:** 2026-04-15
**Implements:** Principle 6 (No Committed Secrets), Principle 9 (Zero Trust), Principle 10 (Least Privilege)
**Policies:** SEC-002 (Secret Scanning), SEC-003 (Least Privilege), SEC-005 (Machine Identity), GOV-003 (Break-Glass)

---

## Purpose

Define how secrets are classified, owned, stored, distributed, rotated, revoked, and audited across the Nash Group — independent of which backend stores them.

This specification does not duplicate the policies it references. SEC-002 defines prevention (no secrets in git). SEC-005 defines machine identity types (GitHub Apps, not Classic PATs). GOV-003 defines emergency access procedures. This specification fills the gap those policies leave: a unified lifecycle and organizational ownership model for the secrets themselves.

> **Current-state note (2026-04-15):** On the managed Guardian workstation, local developer secret reads use environment variables and/or `op read`. Runtime, service, and CI secret authority remain repo-owned and may be GitHub environments, GitHub App auth, OIDC, Infisical, cloud secret managers, or another approved backend. gopass is migration-only cold archive and is not an approved active local backend.

> **Ownership boundary:** This specification defines secret classification, lifecycle requirements, approved distribution channels, and handoff criteria. Exact Citadel files, workflow names, commands, and live backend wiring are Citadel-owned implementation details; references below are current-state evidence or expected contracts, not Covenant-run implementation.

---

## Governing Principles

| Principle | How This Specification Implements It |
|-----------|--------------------------------------|
| **Principle 6: No Committed Secrets** | The secrets vault is the positive counterpart to Principle 6 — where secrets go instead of git |
| **SEC-002: Secret Scanning** | This specification defines the storage and lifecycle side; SEC-002 defines the prevention and detection side |
| **SEC-003: Least Privilege** | Namespace tiers restrict who can provision and read secrets at each organizational level |
| **SEC-005: Machine Identity** | This specification defines storage and rotation requirements for machine credentials; SEC-005 defines which credential types are permitted |
| **GOV-003: Break-Glass** | This specification defines the emergency credential retrieval path; GOV-003 defines the authorization and reconciliation process |

---

## 1. Secret Classification

### 1.1 By Sensitivity

| Class | Description | Examples | Storage Requirement |
|-------|-------------|----------|---------------------|
| **Material** | Grants direct access to infrastructure, data, or identity | Private keys, API tokens, S3 credentials, encryption passphrases | Encrypted vault; never plaintext at rest or in transit |
| **Identifier** | Non-secret but operationally coupled to material secrets | App IDs, installation IDs, zone IDs, account IDs | Vault or non-sensitive variable store; no rotation or access-control requirement beyond operational convenience |

The current local bootstrap contract may store both classes for operational convenience. Identifiers stored alongside material secrets (for example, a GitHub App ID next to its private key) are acceptable but do not require the same rotation or access controls as material secrets.

### 1.2 By Lifespan

| Lifespan | Description | Examples | Rotation Model |
|----------|-------------|----------|----------------|
| **Ephemeral** | Generated on demand, expires automatically | GitHub App Installation Access Tokens (1 hour), OIDC tokens | No manual rotation — built into protocol |
| **Short-lived** | Human-created, mandatory expiry | Fine-grained PATs (90 days max per SEC-005) | Recreate before expiry |
| **Long-lived** | Persists until explicitly rotated | S3 access keys, Cloudflare API tokens, GitHub App PEM | Rotation schedule required (Section 6) |
| **Permanent** | Cannot be rotated without recreating the dependent resource | State encryption passphrases | Documented exception; rotate only on suspected compromise |

---

## 2. Organizational Ownership Model

Three tiers, matching the parent/subsidiary/project hierarchy established in the organizational architecture.

### 2.1 Parent Tier

**Owner:** Guardian

**Scope:** Secrets that govern the shared control plane or cross-subsidiary access.

**Current inventory:**

| Logical Secret Path | Class | Lifespan | Purpose |
|---------------------|-------|----------|---------|
| `infra/hetzner/s3/access-key-id` | Material | Long-lived | S3 state backend authentication |
| `infra/hetzner/s3/secret-access-key` | Material | Long-lived | S3 state backend authentication |
| `infra/opentofu/state-encryption-passphrase` | Material | Permanent | State encryption at rest |
| `infra/github-app/app-id` | Identifier | N/A | GitHub App identification |
| `infra/github-app/installations/the-nash-group` | Identifier | N/A | Parent org installation binding |
| `infra/github-app/private-key` | Material | Long-lived | GitHub App authentication key |
| `cloudflare/zones/thenash-group/zone-id` | Identifier | N/A | Parent zone identification |
| `cloudflare/zones/thenash-group/account-id` | Identifier | N/A | Cloudflare account identification |
| `cloudflare/tokens/projects/citadel/the-nash-group` | Material | Long-lived | Cloudflare API authentication |

**Rule:** Only the Guardian provisions parent-tier secrets. Subsidiaries inherit access through repo-approved runtime injection and project-owned local bootstrap flows, never by assuming direct read access to parent-tier items or backend entries.

### 2.2 Subsidiary Tier

**Owner:** Subsidiary steward (currently also the Guardian in a single-operator org)

**Scope:** Secrets specific to one subsidiary's infrastructure or services.

**Current inventory:** None. The first subsidiary secret will be created when a subsidiary receives its own Cloudflare token or its own service credentials.

**Future examples:**
- `cloudflare/zones/jefahnierocks/zone-id`
- `cloudflare/tokens/projects/citadel/jefahnierocks`

**Rule:** Subsidiary secrets use the subsidiary namespace (Section 3). A subsidiary may add stricter constraints to the parent rotation or access model but may never relax them.

### 2.3 Project Tier

**Owner:** Project maintainer

**Scope:** Secrets specific to a single application or service within a subsidiary.

**Current inventory:** None.

**Future examples:**
- `services/the-tartan/deploy-token`
- `services/the-nexus/api-key`

**Rule:** Project secrets use the project namespace (Section 3). Access is scoped to the project's CI environment and runtime. Material project secrets require Guardian review before provisioning.

---

## 3. Namespace Convention

Provider-agnostic schema:

```
{domain}/{provider-or-resource}/{entity}/{secret-name}
```

Where:
- **domain** — the functional area: `infra`, `cloudflare`, `services`, `break-glass`
- **provider-or-resource** — the platform or system: `hetzner`, `github-app`, `opentofu`
- **entity** — the organizational entity, zone, or project: `the-nash-group`, `thenash-group`, `jefahnierocks`
- **secret-name** — the specific credential: `access-key-id`, `private-key`, `api-token`

The current 9 vault paths already follow this convention. This specification codifies it rather than redesigning it. Any future backend must support these logical paths — either natively (folders, environments) or via a documented mapping layer.

### Namespace by Tier

| Tier | Namespace Pattern | Example |
|------|-------------------|---------|
| Parent | `infra/{provider}/{secret}` or `cloudflare/{resource}/{parent-entity}/{secret}` | `infra/hetzner/s3/access-key-id` |
| Subsidiary | `cloudflare/{resource}/{subsidiary-entity}/{secret}` or `services/{subsidiary}/{secret}` | `cloudflare/tokens/projects/citadel/jefahnierocks` |
| Project | `services/{project-name}/{secret}` | `services/the-tartan/deploy-token` |

---

## 4. Distribution Channels

Three channels for how secrets reach consumers.

### 4.1 CI Injection (GitHub Actions and equivalent managed automation)

CI and automation must read from the repo's approved managed backend. For `the-citadel` today, that means GitHub Actions secrets/variables plus GitHub App authentication.

**Current Citadel-owned mapping snapshot:**

| Repository Secret | Source Vault Path | Consumers |
|-------------------|-------------------|-----------|
| `APP_ID` | `infra/github-app/app-id` | The Forge, The Watcher, The Shield |
| `APP_PEM` | `infra/github-app/private-key` | The Forge, The Watcher, The Shield |
| `AWS_ACCESS_KEY_ID` | `infra/hetzner/s3/access-key-id` | The Forge, The Watcher, The Shield |
| `AWS_SECRET_ACCESS_KEY` | `infra/hetzner/s3/secret-access-key` | The Forge, The Watcher, The Shield |
| `CLOUDFLARE_API_TOKEN` | `cloudflare/tokens/projects/citadel/the-nash-group` | The Forge, The Watcher, The Shield |
| `TOFU_STATE_ENCRYPTION_PASSPHRASE` | `infra/opentofu/state-encryption-passphrase` | The Forge |

**Non-secret repository variables:** `S3_ENDPOINT`, `CLOUDFLARE_ZONE_ID`, `CLOUDFLARE_ACCOUNT_ID`

**Provisioning rule:** The Guardian updates the local bootstrap source and the corresponding runtime secret channel intentionally and separately when both exist. 1Password on the managed workstation does not automatically replace the runtime authority.

### 4.2 Local Workstation Injection (direnv + `op read`)

Citadel currently documents the local workstation injection pattern in its `.envrc.template`. The Covenant contract is that local variables resolve from approved local secret references and never commit plaintext secrets; exact command flow remains Citadel-owned.

**Current mapping note:** The logical namespace in Sections 2 and 3 stays provider-agnostic. The current `op://` item and field mapping for those logical paths is documented in `the-citadel/.envrc.template`, which is the canonical live workstation mapping for Citadel local bootstrap.

**Provisioning rule:** The Guardian maintains the local bootstrap source. The committed `.envrc.template` documents which references are needed. The `.envrc` itself is gitignored and must not become a plaintext long-term secret store.

### 4.3 Runtime Injection (repo-owned managed backend)

Runtime and service secret injection are repo-owned. Approved authorities may include Infisical, GitHub environments, GitHub App auth, OIDC, cloud secret managers, or another governed backend. The parent policy defines the boundary; each repo defines its concrete runtime authority. 1Password on the managed workstation is a local human/agent read path, not the default runtime backend.

### 4.4 Planning Profile: Self-Hosted Infisical via OpenTofu

Self-hosted Infisical is an approved **planning-stage** runtime backend profile within the Nash Group secrets architecture.

This subsection records the current planning assumption for Infrastructure as Code:

- Infisical may serve as a repo-owned runtime secret authority where a repo intentionally adopts it
- OpenTofu may manage Infisical objects declaratively through the Infisical provider
- Adopting a provider-backed Infisical model does **not** automatically replace the managed-workstation local bootstrap contract (`op read` and/or environment variables)
- Human interactive workstation identity policy still belongs to SEC-004 and COM-001
- Machine identity rules for unattended automation still belong to SEC-005
- Each adopting repo must pin the Infisical provider version intentionally and treat the generated lockfile as part of the contract

**Planning intent:** capture Infisical itself as governed infrastructure, not just a manual backend. The provider capability surface makes it possible to manage identity, approvals, dynamic secrets, rotation, sync, certificate issuance, and direct secret objects as code.

**Current planning inventory of Infisical provider capabilities:**

**Group machine identity:**
- `infisical_group_machine_identity`

**App connections:**
- `infisical_app_connection_1password`
- `infisical_app_connection_aws`
- `infisical_app_connection_azure_app_configuration`
- `infisical_app_connection_azure_client_secrets`
- `infisical_app_connection_azure_devops`
- `infisical_app_connection_azure_key_vault`
- `infisical_app_connection_bitbucket`
- `infisical_app_connection_cloudflare`
- `infisical_app_connection_databricks`
- `infisical_app_connection_flyio`
- `infisical_app_connection_gcp`
- `infisical_app_connection_github`
- `infisical_app_connection_gitlab`
- `infisical_app_connection_ldap`
- `infisical_app_connection_mssql`
- `infisical_app_connection_mysql`
- `infisical_app_connection_oracledb`
- `infisical_app_connection_postgres`
- `infisical_app_connection_render`
- `infisical_app_connection_supabase`

**Approval controls:**
- `infisical_access_approval_policy`
- `infisical_secret_approval_policy`

**Certificate management:**
- `infisical_cert_manager_ca_certificate`
- `infisical_cert_manager_certificate`
- `infisical_cert_manager_certificate_policy`
- `infisical_cert_manager_certificate_profile`
- `infisical_cert_manager_external_ca_acme`
- `infisical_cert_manager_external_ca_adcs`
- `infisical_cert_manager_internal_ca`

**Dynamic secrets:**
- `infisical_dynamic_secret_aws_iam`
- `infisical_dynamic_secret_kubernetes`
- `infisical_dynamic_secret_mongo_atlas`
- `infisical_dynamic_secret_mongo_db`
- `infisical_dynamic_secret_sql_database`

**External KMS:**
- `infisical_external_kms_aws`

**Groups:**
- `infisical_group`
- `infisical_groups` (data source)

**Identities and identity auth methods:**
- `infisical_identity`
- `infisical_identity_aws_auth`
- `infisical_identity_azure_auth`
- `infisical_identity_gcp_auth`
- `infisical_identity_jwt_auth`
- `infisical_identity_kubernetes_auth`
- `infisical_identity_oidc_auth`
- `infisical_identity_token_auth`
- `infisical_identity_token_auth_token`
- `infisical_identity_universal_auth`
- `infisical_identity_universal_auth_client_secret`
- `infisical_identity_details` (data source)

**KMS:**
- `infisical_kms_key`
- `infisical_kms_key_public_key` (data source)

**Native integrations (deprecated):**
- `infisical_integration_aws_parameter_store`
- `infisical_integration_aws_secrets_manager`
- `infisical_integration_circleci`
- `infisical_integration_databricks`
- `infisical_integration_gcp_secret_manager`

**Organization role:**
- `infisical_org_role`

**Projects and project access model:**
- `infisical_project`
- `infisical_project_environment`
- `infisical_project_group`
- `infisical_project_identity`
- `infisical_project_identity_specific_privilege`
- `infisical_project_role`
- `infisical_project_template`
- `infisical_project_user`
- `infisical_projects` (data source)

**Secret rotations:**
- `infisical_secret_rotation_aws_iam_user_secret`
- `infisical_secret_rotation_azure_client_secret`
- `infisical_secret_rotation_ldap_password`
- `infisical_secret_rotation_mssql_credentials`
- `infisical_secret_rotation_mysql_credentials`
- `infisical_secret_rotation_oracledb_credentials`
- `infisical_secret_rotation_postgres_credentials`

**Secret syncs:**
- `infisical_secret_sync_1password`
- `infisical_secret_sync_aws_parameter_store`
- `infisical_secret_sync_aws_secrets_manager`
- `infisical_secret_sync_azure_app_configuration`
- `infisical_secret_sync_azure_devops`
- `infisical_secret_sync_azure_key_vault`
- `infisical_secret_sync_bitbucket`
- `infisical_secret_sync_cloudflare_pages`
- `infisical_secret_sync_cloudflare_workers`
- `infisical_secret_sync_databricks`
- `infisical_secret_sync_flyio`
- `infisical_secret_sync_gcp_secret_manager`
- `infisical_secret_sync_github`
- `infisical_secret_sync_gitlab`
- `infisical_secret_sync_render`
- `infisical_secret_sync_supabase`

**Secrets, folders, imports, and tags:**
- `infisical_secret` also appears in the provider surface as an ephemeral resource in the current planning input
- `infisical_secret`
- `infisical_secret_folder`
- `infisical_secret_import`
- `infisical_secret_tag`
- `infisical_secret_folders` (data source)
- `infisical_secret_metadata` (data source)
- `infisical_secrets` (data source)

**Planning implication:** if the Nash Group moves more runtime authority into Infisical, the platform can govern not only static secret values but also identity bootstrap, delegated access, approvals, dynamic credentials, provider sync, and rotation policy as code.

---

## 5. Lifecycle Requirements

### 5.1 Creation

| Tier | Provisioner | Approval Required | Method |
|------|-------------|-------------------|--------|
| Parent | Guardian | None (single operator) | Vault insert |
| Subsidiary | Guardian or designated steward | Guardian review | Vault insert under subsidiary namespace |
| Project | Project maintainer | Guardian review for material secrets; self-service for identifiers | Vault insert under project namespace |

### 5.2 Storage

All material secrets must be encrypted at rest. Approved local and runtime backends must provide strong encryption and access controls appropriate to the secret class and use case.

Secrets must never be stored in:
- Git repositories (Principle 6)
- Plaintext files on disk outside an approved backend (includes `.envrc` files — committed templates may contain references, not secret values)
- Chat messages, email, wikis, or shared documents
- Browser password managers not designated as organizational vault backends

### 5.3 Distribution

Per the three channels defined in Section 4. No other distribution method is permitted for material secrets.

### 5.4 Rotation

| Secret | Current Rotation | Target Rotation | Owner |
|--------|------------------|-----------------|-------|
| Hetzner S3 keys | None | 180 days | Guardian |
| GitHub App PEM | None | 180 days | Guardian |
| Cloudflare API token | None | 180 days | Guardian |
| State encryption passphrase | None | Exception: rotate only on suspected compromise | Guardian |
| Fine-grained PATs | 90-day expiry | Already enforced by SEC-005 | Individual |
| GitHub App IATs | 1-hour expiry | Already enforced by protocol | N/A |

No rotation is currently happening for long-lived material secrets. This specification sets the 180-day target. Enforcement belongs in the Citadel (reminder mechanism, drift detection, or calendar-based process). Automated rotation is a post-centralized-vault goal, not a current requirement.

### 5.5 Revocation

On suspected compromise of a material secret:

1. Immediately revoke or regenerate the credential at the provider (GitHub, Cloudflare, Hetzner)
2. Update the vault with the replacement credential
3. Update all distribution channels (GitHub Actions secrets, `.envrc.template` if paths changed)
4. Audit provider logs for unauthorized use during the exposure window
5. Document the incident per SEC-002 incident response (1-hour revocation, 24-hour root cause)

For GitHub App PEM compromise specifically, follow the procedure in the GitHub Machine Identity Specification.

### 5.6 Audit

| Channel | Current Audit Capability | Gap |
|---------|-------------------------|-----|
| Local workstation bootstrap (`op read`) | Local human/agent read path only; not the runtime system of record | Runtime audit must come from the repo-approved managed backend |
| GitHub Actions / GitHub environments | GitHub audit log records secret updates and workflow use | Adequate for current Citadel automation |
| Managed runtime backend (Infisical, OIDC, cloud secret manager, etc.) | Backend-specific | Each repo must document and review its own runtime audit surface |
| Provider consoles | Per-provider audit logs (GitHub, Hetzner, Cloudflare) | No aggregation |

---

## 6. Current Architecture vs. Target Architecture

| Aspect | Current State | Target State |
|--------|---------------|--------------|
| Local developer reads | Environment variables and/or `op read` on the managed workstation | Same boundary, with clearer item mapping and less manual duplication |
| Runtime / CI authority | Repo-approved managed backend per repo | Same repo-owned model, with stronger automation and auditability |
| Rotation | Manual, no schedule enforced | 180-day schedule with automated reminders; eventual automated rotation where justified |
| Distribution sync | Intentional separation between local bootstrap and runtime authority | Better automation without collapsing all repos into one backend |
| Multi-user access | Single Guardian for most parent-tier flows | Role-based access for multiple Guardians where needed |
| Subsidiary isolation | Namespace convention plus repo-owned runtime boundaries | Backend-enforced access boundaries per subsidiary where justified |
| Cloudflare token scope | Shared across workspaces | Per-subsidiary token (per Cloudflare Ownership Transition Specification exit criteria) |
| Legacy archive | Machine-local gopass residue may still exist | Retired completely |

---

## 7. Legacy Archive Retirement Criteria

gopass is not an approved active backend. It may remain only as machine-local cold archive while a one-time extraction or migration cleanup step is still required.

Before the archive is retired:

1. Active local `.envrc` files and repo-owned wrappers use environment variables and/or `op read`
2. Runtime and CI authorities are documented per repo and remain repo-owned
3. No active docs or code prescribe gopass as current behavior
4. `BREAK_GLASS.md` and related runbooks point to the current backend, with any gopass note marked archive-only
5. A normal-run and break-glass check confirm no active workflow still depends on gopass
6. The machine-local archive is removed or securely destroyed after confirmation

---

## 8. Known Exceptions

| Exception | Reason | Review Trigger |
|-----------|--------|----------------|
| Shared Cloudflare API token across workspaces | POC-era single control account | Per-subsidiary token created per Cloudflare Ownership Transition Specification |
| No rotation schedule enforced for long-lived secrets | Single operator, small inventory (4 material secrets) | Second Guardian joins, or material secret inventory exceeds 20 |
| State encryption passphrase exempt from rotation | Rotating requires re-encrypting all state files across all workspaces | Suspected compromise only |
| Local bootstrap and runtime authority may require separate updates | The boundary is intentional; 1Password does not automatically replace runtime backends | Repo-specific automation or OIDC removes duplicate handling |

---

## 9. Review Cadence

This specification must be reviewed:

- Before onboarding the first subsidiary-tier secret
- After a repo changes its runtime secret authority
- Quarterly while the manual rotation exception remains active

---

## Related Documents

- **Policy:** [SEC-002: Secret Scanning](../sec-002-secret-scanning.md) — prevention and detection
- **Policy:** [SEC-003: Least Privilege Access](../sec-003-least-privilege.md) — permission scoping
- **Policy:** [SEC-005: Machine Identity Management](../sec-005-machine-identity.md) — credential types and identity tiers
- **Policy:** [GOV-003: Emergency Break-Glass](../gov-003-break-glass.md) — emergency access authorization
- **Specification:** [GitHub Machine Identity](./github-machine-identity.md) — GitHub App PEM lifecycle
- **Specification:** [Cloudflare Ownership Transition](./cloudflare-ownership-transition.md) — shared token exception
- **Specification:** [IAM Specification](./iam-specification.md) — identity hierarchy
- **Citadel-owned implementation reference:** `the-citadel/.envrc.template` — local workstation injection pattern
- **Citadel-owned implementation reference:** `the-citadel/BREAK_GLASS.md` — emergency credential retrieval paths
- **Citadel-owned implementation reference:** `the-citadel/.github/workflows/opentofu.yml` — CI secrets consumption

---

## Changelog

### v1.3.0 (2026-04-15)

- Added the planning-stage Infisical backend profile for OpenTofu-based management
- Recorded the current Infisical provider capability inventory for identity, approvals, certificates, dynamic secrets, rotation, sync, KMS, projects, and direct secret resources
- Clarified that adopting Infisical as runtime authority does not replace the managed-workstation local bootstrap contract automatically

### v1.2.0 (2026-04-15)

- Promoted the specification to active organizational authority for secrets lifecycle policy
- Clarified that the live contract is already in force across parent and child guidance
- Added an explicit cross-reference from logical secret paths to the live Citadel `op://` mapping
- Verification note: active Citadel local bootstrap and break-glass retrieval documentation now point to `op read`; final legacy-archive retirement still requires an explicit verification record per Section 7

### v1.1.0 (2026-04-15)

- Reframed the live contract around `op` for managed-workstation local reads and repo-owned runtime authorities
- Marked gopass as legacy archive only
- Preserved logical secret naming independent of backend choice
- Clarified that parent policy does not collapse all repos into one runtime backend

### v1.0.0 (2026-04-11)

- Initial proposed draft defining organizational secret classification, ownership, distribution channels, lifecycle rules, and transition criteria
