# Google Cloud IAM Implementation Summary
**Version**: 1.0.0
**Created**: 2025-11-10
**Status**: PROPOSED - Awaiting Citadel-level approval

> "A visual, executive-level summary of The Nash Group's Google Cloud IAM strategy."

---

## Executive Summary

This document provides The Nash Group's comprehensive Google Cloud IAM implementation strategy, aligning GCP identity and access management with our three-pillar architecture, Five Guardian governance model, and zero-trust security principles.

**Implementation Timeline**: 12 weeks (3 months)
**Governance Level**: Citadel (requires 1 Mentor + 1 Watcher approval)
**Documents**:
- **Strategy**: `GOOGLE-CLOUD-IAM-STRATEGY.md` (complete 25-page strategy)
- **Quick Start**: `GOOGLE-CLOUD-IAM-QUICK-START.md` (hands-on implementation guide)
- **Summary**: This document (visual overview)

---

## Architecture Overview

### The Nash Group Three-Pillar Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     THE COVENANT                            │
│                    (Level 1: Philosophy)                    │
│  • 16 Core Principles (esp. #9: Zero Trust, #10: Least     │
│    Privilege)                                                │
│  • GOVERNANCE.md (decision authority)                       │
│  • HUMAN_MANDATE.md (5 Guardian roles)                      │
└─────────────────────────────────────────────────────────────┘
                            ↓ defines
┌─────────────────────────────────────────────────────────────┐
│                   SPECIFICATIONS                            │
│              (Level 2: Standards & Governance)              │
│  • IAM Standards (WebAuthn, mTLS, OIDC)                    │
│  • Service Standards (health checks, metrics)               │
│  • Multi-tenant architecture                                │
└─────────────────────────────────────────────────────────────┘
                            ↓ implements
┌──────────────────────┐           ┌──────────────────────────┐
│   THE CITADEL        │           │      THE NEXUS           │
│ (Level 3a: IaC)      │           │ (Level 3b: Operations)   │
│ • Terraform for GCP  │           │ • Services authenticate  │
│ • Workload Identity  │◄─────────►│   via Workload Identity  │
│ • Resource provision │           │ • OPA runtime policies   │
└──────────────────────┘           └──────────────────────────┘
```

---

## Google Cloud IAM Hierarchy

### Resource Organization

```
Organization: nash-group.example (ID: 123456789012)
├── Google Groups (Identity Layer)
│   ├── nash-group-owners@nashgroup.example (Break-Glass)
│   ├── nash-group-watchers@nashgroup.example (Security)
│   ├── nash-group-mentors@nashgroup.example (Infrastructure)
│   ├── nash-group-platform@nashgroup.example (Developers)
│   └── nash-group-explorers@nashgroup.example (All Members)
│
├── Folder: personal-infra
│   ├── IAM: nash-group-personal-admin@ = roles/editor
│   ├── Project: nash-personal-prod
│   │   ├── VPC: personal-prod-vpc
│   │   ├── Service Accounts:
│   │   │   ├── citadel-deployer@nash-personal-prod.iam.gserviceaccount.com
│   │   │   ├── nexus-deployer@nash-personal-prod.iam.gserviceaccount.com
│   │   │   └── observability-bridge@nash-personal-prod.iam.gserviceaccount.com
│   │   └── Labels: tenant=personal, environment=prod, governance=citadel
│   └── Project: nash-personal-dev
│       ├── VPC: personal-dev-vpc
│       └── IAM: nash-group-explorers@ = nash.explorer
│
├── Folder: family-infra
│   ├── IAM: nash-group-family-admin@ = roles/editor
│   ├── IAM: nash-group-family-member@ = roles/viewer (prod only)
│   ├── Project: nash-family-prod
│   │   ├── VPC: family-prod-vpc (Shared Services VPC)
│   │   ├── Parental Control Proxy
│   │   └── Labels: tenant=family, environment=prod, governance=citadel
│   └── Project: nash-family-dev
│       └── VPC: family-dev-vpc
│
├── Folder: university-infra
│   ├── IAM: nash-group-university-admin@ = roles/editor
│   └── Project: nash-university-research
│       ├── VPC: university-vpc
│       └── Labels: tenant=university, compliance=academic
│
└── Folder: ai-lab-infra
    ├── IAM: nash-group-ai-lab-admin@ = roles/editor
    ├── Project: nash-ai-lab-prod
    │   ├── VPC: ai-lab-prod-vpc
    │   ├── GPU Quotas: Enforced via OPA
    │   ├── AI Agent Service Accounts (OPA-managed)
    │   └── Labels: tenant=ai-lab, environment=prod
    └── Project: nash-ai-lab-dev
        └── IAM: nash-group-explorers@ = nash.explorer
```

---

## Identity and Access Management

### Google Groups → Guardian Roles Mapping

| Google Group | Nash Guardian Role | GCP IAM Roles | Access Scope | Members |
|--------------|-------------------|---------------|--------------|---------|
| **nash-group-owners@** | Break-Glass Super Admin | `roles/owner` | Organization | Jeffrey (Owner) |
| **nash-group-watchers@** | Watchers (Security) | `roles/securityadmin`, `roles/iam.securityReviewer`, `roles/logging.viewer` | Organization | Primary Watcher, Secondary Watcher |
| **nash-group-mentors@** | Mentors (Architects) | `roles/editor` (Project), `roles/iam.roleAdmin` (Folder) | Folder/Project | Senior engineers, architects |
| **nash-group-platform@** | Platform Clan (Developers) | `roles/compute.instanceAdmin.v1`, `roles/container.developer` | Project | Service owners, developers |
| **nash-group-explorers@** | All Guardians | `roles/viewer`, Custom: `nash.explorer` | Project (dev only) | All Nash Group members |

---

### Guardian Hat → GCP Role Mapping

| Guardian Hat | GCP Role(s) | Scope | Use Case |
|--------------|------------|-------|----------|
| **Super Admin (Break-Glass)** | `roles/owner` | Organization | Emergency full control |
| **Watcher (Security)** | `roles/securityadmin`, `roles/iam.securityReviewer` | Organization | Security audits, IAM oversight |
| **Watcher (Emergency)** | `roles/compute.instanceAdmin.v1`, `roles/container.admin` | All projects | Incident response |
| **Mentor (Architect)** | `roles/editor`, `roles/iam.roleAdmin` | Folder | Design and implement infrastructure |
| **Mentor (Judge)** | `roles/iam.securityReviewer`, `roles/logging.viewer` | Organization | Review IAM changes, audit logs |
| **Mentor (Gardener)** | `roles/editor`, `roles/monitoring.admin` | Project | Maintain services, update dependencies |
| **Platform Clan (Explorer)** | `roles/compute.instanceAdmin.v1`, `roles/cloudfunctions.developer` | Project (dev) | Deploy services, manage applications |
| **Explorer (All Guardians)** | `roles/viewer`, Custom: `nash.explorer` | Project (dev) | Read-only, limited experimentation |

---

## Workload Identity Federation (Zero-Trust CI/CD)

### Authentication Flow

```
┌──────────────────────────────────────────────────────────────┐
│              GitHub Actions Workflow                         │
│  (Repository: the-citadel)                                   │
│  Trigger: push to main branch                                │
└──────────────────────────────────────────────────────────────┘
                            ↓
                   Request OIDC Token
                            ↓
┌──────────────────────────────────────────────────────────────┐
│           GitHub OIDC Token Service                          │
│  https://token.actions.githubusercontent.com                 │
│  Issues short-lived JWT token with claims:                   │
│    - sub: repo:the-nash-group/the-citadel:ref:refs/heads/main
│    - actor: jeffrey                                          │
│    - repository: the-nash-group/the-citadel                  │
└──────────────────────────────────────────────────────────────┘
                            ↓
                   Exchange OIDC Token
                            ↓
┌──────────────────────────────────────────────────────────────┐
│         GCP Workload Identity Pool                           │
│  Pool ID: github-actions-pool                                │
│  Provider: github-oidc-provider                              │
│  Validates token, maps attributes:                           │
│    - google.subject = assertion.sub                          │
│    - attribute.repository = assertion.repository             │
└──────────────────────────────────────────────────────────────┘
                            ↓
              Impersonate Service Account
                            ↓
┌──────────────────────────────────────────────────────────────┐
│           Service Account: citadel-deployer@                 │
│  Email: citadel-deployer@nash-personal-prod.iam...           │
│  Permissions:                                                │
│    - roles/editor (Project-level)                            │
│    - roles/iam.serviceAccountAdmin                           │
│  Allowed impersonators:                                      │
│    - principalSet://...github-actions-pool/attribute.        │
│      repository/the-nash-group/the-citadel                   │
└──────────────────────────────────────────────────────────────┘
                            ↓
              Execute Terraform Apply
                            ↓
┌──────────────────────────────────────────────────────────────┐
│              GCP Resources Created/Updated                   │
│  (Compute instances, VPCs, IAM policies, etc.)               │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                  Cloud Audit Logs                            │
│  Logs all actions by citadel-deployer@                       │
│  Exported to Observability Bridge                            │
└──────────────────────────────────────────────────────────────┘
```

**Key Benefits**:
- ✅ No long-lived service account keys
- ✅ Short-lived tokens (minutes)
- ✅ Repository-scoped access
- ✅ Complete audit trail
- ✅ Zero secrets in GitHub repository

---

## Multi-Tenant Isolation

### Tenant Architecture

```
┌─────────────────────────────────────────────────────────────┐
│          Organization: nash-group.example                    │
└─────────────────────────────────────────────────────────────┘
          │                 │                 │
          │                 │                 │
   ┌──────┴────┐    ┌──────┴──────┐   ┌─────┴──────┐
   │ personal  │    │   family    │   │   ai-lab   │
   │   Folder  │    │   Folder    │   │   Folder   │
   └───────────┘    └─────────────┘   └────────────┘
        │                  │                  │
        │                  │                  │
   ┌────┴─────┐      ┌─────┴──────┐    ┌─────┴──────┐
   │nash-     │      │nash-family-│    │nash-ai-lab-│
   │personal- │      │prod        │    │prod        │
   │prod      │      │            │    │            │
   │Project   │      │Project     │    │Project     │
   └──────────┘      └────────────┘    └────────────┘
        │                  │                  │
   ┌────┴─────┐      ┌─────┴──────┐    ┌─────┴──────┐
   │personal- │      │Parental    │    │GPU Quotas  │
   │prod-vpc  │      │Control     │    │AI Agent SA │
   │          │      │Proxy       │    │OPA Policies│
   │10.0.0.0/ │      │Content     │    │            │
   │24        │      │Filter      │    │            │
   └──────────┘      └────────────┘    └────────────┘
```

**Isolation Mechanisms**:
1. **Folder-Level IAM Policies**: Each tenant has dedicated folder with restricted access
2. **VPC Isolation**: Each tenant has separate VPC (no default peering)
3. **Resource Labels**: Mandatory labels (tenant, environment, governance-level) on all resources
4. **VPC Service Controls**: Data exfiltration prevention between tenants
5. **OPA Policies**: Runtime enforcement of tenant boundaries

---

## Security and Compliance

### Cloud Audit Logs

```
┌──────────────────────────────────────────────────────────────┐
│                   GCP Resources                              │
│  (Compute, IAM, Storage, etc.)                               │
│  All actions logged automatically                            │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                 Cloud Audit Logs                             │
│  Log Types:                                                  │
│    - Admin Activity (always on)                              │
│    - Data Access (explicitly enabled)                        │
│    - System Events (always on)                               │
│  Retention: 1 year minimum                                   │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                 Cloud Logging Sink                           │
│  Filter: resource.type="audited_resource"                    │
│  Destination: Pub/Sub topic (audit-logs)                     │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                 Pub/Sub Subscription                         │
│  Push to: https://observability-bridge.thenash.group/        │
│           ingest/gcp-audit-logs                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│            The Nexus: Observability Bridge                   │
│  • Correlates GCP events with GitHub/Cloudflare events       │
│  • Real-time alerting to nash-group-watchers@                │
│  • Unified dashboard                                         │
│  • Compliance reports (weekly/monthly/quarterly)             │
└──────────────────────────────────────────────────────────────┘
```

---

### Alerting Policies

| Alert Type | Trigger Condition | Severity | Response |
|------------|------------------|----------|----------|
| **Break-Glass Access** | nash-group-owners@ member performs ANY action | CRITICAL | Immediate investigation |
| **IAM Policy Change** | SetIamPolicy method called | HIGH | Review audit logs, verify authorization |
| **Service Account Key Created** | CreateServiceAccountKey method called | MEDIUM | Verify requester, check Workload Identity alternative |
| **Privilege Escalation** | User granted roles/owner or roles/editor at Org level | CRITICAL | Immediate revocation, incident investigation |
| **Tenant Boundary Violation** | Service account from tenant A accesses tenant B | HIGH | OPA policy review, access revocation |

**Alert Destinations**:
- Email: nash-group-watchers@nashgroup.example
- Slack: #security-alerts channel (optional)
- PagerDuty: On-call Watcher rotation (optional)

---

### Compliance Frameworks

| Framework | Requirement | Nash Group Implementation | Status |
|-----------|-------------|--------------------------|--------|
| **SOC 2 Type II** | Access controls | Least privilege IAM, periodic reviews | ✅ Compliant |
| **SOC 2 Type II** | Audit trails | Cloud Audit Logs, immutable storage | ✅ Compliant |
| **SOC 2 Type II** | Change management | Terraform IaC, peer review, manual approval | ✅ Compliant |
| **GDPR** | Data subject rights | Audit logs provide access trail | ✅ Compliant |
| **GDPR** | Data protection | Encryption at rest, TLS in transit | ✅ Compliant |
| **NIST 800-63** | IAL2 | WebAuthn (passkeys) for humans | ✅ Compliant |
| **NIST 800-63** | AAL2 | OIDC tokens (short-lived) | ✅ Compliant |
| **CIS GCP Foundation** | IAM best practices | Google Groups, MFA, service account rotation | ✅ Compliant |

---

## Implementation Phases

### Phase Overview (12 Weeks)

```
Week 1-2: Phase 1 - Foundation
├── Create GCP Organization
├── Create Google Groups (5 groups)
├── Assign Organizational Roles
├── Enable Audit Logging
└── Terraform Setup (the-citadel/terraform/gcp/)

Week 3-4: Phase 2 - Multi-Tenant Structure
├── Create Folders (personal, family, university, ai-lab)
├── Create Projects (prod/dev per tenant)
├── Assign Folder-Level IAM Policies
├── Configure Network Isolation (VPCs)
└── Apply Resource Labels

Week 5-6: Phase 3 - Workload Identity Federation
├── Create Workload Identity Pool
├── Create Service Accounts (citadel, nexus, shield deployers)
├── Configure IAM Bindings (repo → SA)
├── Grant Service Account Permissions
└── Update GitHub Actions Workflows

Week 7-8: Phase 4 - Monitoring and Alerting
├── Configure Log Sinks (Pub/Sub)
├── Create Alerting Policies (5 critical alerts)
├── Implement Compliance Reports (weekly/monthly/quarterly)
├── Integrate with Observability Bridge
└── Test Incident Response

Week 9-10: Phase 5 - OPA Policy Enforcement
├── Deploy OPA to GCP (Cloud Run)
├── Implement OPA Policies (tenant boundaries, AI quotas)
├── Integrate OPA with GCP (Cloud Functions)
├── Test OPA Policies
└── Document OPA Integration

Week 11-12: Phase 6 - Integration and Hardening
├── Harden Service Accounts (audit, rotate keys)
├── Implement VPC Service Controls
├── Review IAM Policies (remove over-privileged)
├── Create Runbooks (break-glass, incident response)
├── Document Architecture (ADRs)
└── Conduct Security Review
```

---

### Success Metrics

**Short-term (30 days)**:
- ✅ All human identities use WebAuthn
- ✅ All services use mTLS or OIDC Workload Identity
- ✅ OPA policies deployed and enforced
- ✅ Complete audit trail operational

**Medium-term (90 days)**:
- ✅ AI agent governance fully implemented
- ✅ Family safety controls active
- ✅ Tenant isolation verified
- ✅ Zero password-based authentication
- ✅ Zero long-lived service account keys

**Long-term (1 year)**:
- ✅ 100% IAM compliance across all systems
- ✅ Zero security incidents due to IAM failures
- ✅ Self-service identity management operational
- ✅ Complete SOC 2 Type II compliance

---

## Cost Estimate

### Initial Setup Costs (One-Time)

| Item | Cost | Notes |
|------|------|-------|
| Google Workspace (domain) | $6/user/month | Required for Google Groups |
| GCP Organization Setup | $0 | No charge for organization creation |
| Google Groups | $0 | Included in Workspace |
| Workload Identity Pool | $0 | No charge for identity federation |
| Cloud Audit Logs (Admin Activity) | $0 | Always free |
| Cloud Audit Logs (Data Access) | ~$0.50/GB | Estimated 5GB/month = $2.50/month |
| Cloud Logging Storage | $0.50/GB/month | 1-year retention, ~10GB = $5/month |
| Pub/Sub | $0.40/million messages | ~10K messages/month = $0.004/month |

**Estimated Total**: ~$50/month for 5 users

---

### Ongoing Operational Costs

| Item | Cost | Notes |
|------|------|-------|
| Compute Engine (dev/test) | ~$50/month | Small instances for experimentation |
| Cloud Storage (audit logs) | ~$5/month | 100GB at $0.05/GB/month |
| Cloud Monitoring | $0 | First 50GB/month free |
| OPA on Cloud Run | ~$10/month | Minimal usage |
| VPC Peering | $0 | No additional charge |

**Estimated Total**: ~$115/month

---

## Key Decisions and Trade-offs

### Decision: Use Google Groups for Identity

**Rationale**:
- Centralized membership management
- Cross-platform consistency (GitHub, GCP, Google Workspace)
- Easier onboarding/offboarding
- Aligns with Nash Group team structure

**Trade-offs**:
- Requires Google Workspace subscription ($6/user/month)
- Adds dependency on Google ecosystem

**Decision Authority**: Citadel (1 Mentor + 1 Watcher approval)

---

### Decision: Workload Identity Federation over Service Account Keys

**Rationale**:
- Zero long-lived credentials (Covenant Principle 9: Zero Trust)
- Short-lived tokens (minutes vs. 90 days)
- Repository-scoped access
- Automatic rotation

**Trade-offs**:
- More complex initial setup
- Requires GitHub Actions OIDC token support

**Decision Authority**: Citadel (1 Mentor + 1 Watcher approval)

---

### Decision: Folder-Level Tenant Isolation

**Rationale**:
- Strong boundaries via GCP resource hierarchy
- Inherited IAM policies (DRY principle)
- Audit trail per tenant
- Cost tracking per tenant

**Trade-offs**:
- More complex resource hierarchy
- Requires careful folder structure planning

**Decision Authority**: Citadel (1 Mentor + 1 Watcher approval)

---

### Decision: OPA for Runtime Authorization

**Rationale**:
- Policy-as-code (aligned with Covenant Principle 5: IaC)
- Testable policies
- Runtime enforcement (beyond GCP IAM)
- Tenant boundary validation

**Trade-offs**:
- Additional service to maintain (OPA on Cloud Run)
- Policy development learning curve

**Decision Authority**: Citadel (1 Mentor + 1 Watcher approval)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Break-glass over-use** | Erosion of zero-trust model | Weekly audit, strict documentation requirements, quarterly review |
| **Service account key leakage** | Credential compromise | Eliminate keys via Workload Identity, mandatory 90-day rotation for legacy |
| **Tenant boundary violation** | Cross-tenant data access | OPA policies, VPC isolation, real-time alerting |
| **Over-privileged service accounts** | Excessive permissions | Principle of least privilege, quarterly access review |
| **Audit log overflow** | High storage costs | Filter low-risk reads, 1-year retention policy |
| **Workload Identity misconfiguration** | CI/CD authentication failure | Comprehensive testing, clear documentation, fallback procedures |

---

## Next Steps

### Immediate Actions

1. **Review Strategy**: Present `GOOGLE-CLOUD-IAM-STRATEGY.md` to 1 Mentor + 1 Watcher
2. **Create ADR**: Document decision in Architecture Decision Record
3. **Allocate Budget**: Approve ~$115/month operational budget
4. **Assign Owner**: Designate implementation owner (Mentor or Watcher)

---

### Implementation Sequence

1. **Week 1-2**: Foundation (Organization, Google Groups, Terraform)
2. **Week 3-4**: Multi-Tenant Structure (Folders, Projects, VPCs)
3. **Week 5-6**: Workload Identity Federation (Zero-trust CI/CD)
4. **Week 7-8**: Monitoring and Alerting (Audit logs, compliance reports)
5. **Week 9-10**: OPA Policy Enforcement (Runtime authorization)
6. **Week 11-12**: Integration and Hardening (Security review, runbooks)

---

### Post-Implementation

- **Weekly**: Access review, break-glass audit
- **Monthly**: Compliance reports, cost optimization
- **Quarterly**: Full access audit, IAM policy review, security assessment

---

## References

### Documentation

- **Complete Strategy**: `GOOGLE-CLOUD-IAM-STRATEGY.md` (25 pages)
- **Quick Start Guide**: `GOOGLE-CLOUD-IAM-QUICK-START.md` (hands-on implementation)
- **Nash Group Principles**: `the-covenant/PRINCIPLES.md`
- **IAM Framework**: `.org/IAM-FRAMEWORK.md`
- **Organizational Standards**: `ORGANIZATION-SPEC.md`

---

### External Resources

- **GCP IAM Best Practices**: https://cloud.google.com/iam/docs/best-practices
- **Workload Identity Federation**: https://cloud.google.com/iam/docs/workload-identity-federation
- **CIS GCP Benchmark**: https://www.cisecurity.org/benchmark/google_cloud_computing_platform
- **Terraform Google Provider**: https://registry.terraform.io/providers/hashicorp/google/latest/docs

---

## Approval

**Required Approvals** (Citadel-level governance):
- [ ] 1 Mentor
- [ ] 1 Watcher

**Approval Date**: _____________

**Implementation Owner**: _____________

**Target Completion Date**: _____________

---

**Version History**:
- v1.0.0 (2025-11-10): Initial summary document

**Next Review**: 2026-02-10 (Quarterly)

---

*"In Google Cloud, as in all realms of The Nash Group, identity is the foundation. Zero trust, least privilege, and complete audit trails ensure our infrastructure remains secure, compliant, and aligned with our principles."*

**The Shield protects all pillars. There can be only one identity source of truth.**
