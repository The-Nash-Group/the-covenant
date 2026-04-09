This is a robust Version 1.0.0 specification. You have correctly identified the "Holy Trinity" of modern IAM: **Federation (Identity), Isolation (Boundaries), and Automation (OIDC).**

However, as we look toward **November 2025 and the "Agentic Era,"** there is a distinct gap in this spec: **The Agent Protocol**.

Your current spec treats "Machines" as deterministic CI/CD pipelines (Github Actions, Terraform). But in an Agentic era, you will have autonomous AI agents (The "Explorers" and "Specialists" from your role matrix) that need to spin up resources, run experiments, and tear them down *dynamically* and *probabilistically*. They behave differently than a CI pipeline.

Here is my expert architectural review and the necessary additions to make this "Future-Proof" for 2025.

-----

### 1\. The Missing Tier: "Agentic Identity"

In 2025, an AI Agent is not just a "Service Account." It is a **Synthetic User**.

  * **CI/CD Pipeline:** Deterministic. Runs a script. Needs specific permissions.
  * **AI Agent:** Probabilistic. "Figures out" how to solve a problem. Needs *broader* permissions but *stricter* guardrails (quotas, cost limits).

**Recommendation:** Split "Machine Identities" into **"Automation"** (CI/CD) and **"Synthetic"** (Agents).

#### Add to `1.4 IAM Roles` (The Agent Sandbox)

We need a role specifically for your AI Lab agents that allows them to create infrastructure but prevents them from bankrupting you or breaking the "Covenant."

```hcl
# terraform/aws/iam/agent-roles.tf

resource "aws_iam_role" "ai_researcher_agent" {
  name = "nash-ai-lab-agent-01"

  # Agents authenticate via mTLS or specialized OIDC (e.g., from an orchestration platform)
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.agent_orchestrator.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
    }]
  })

  # CRITICAL: Agents need a stricter boundary than humans
  permissions_boundary = aws_iam_policy.agent_sandbox_boundary.arn

  tags = {
    "nash:clan"        = "explorers"
    "nash:tier"        = "experimental"
    "nash:environment" = "dev"
    "nash:type"        = "synthetic-user" # New Label for 2025
  }
}
```

-----

### 2\. The "Permission Boundary" Logic (Visualized)

Your implementation of Permission Boundaries (Section 1.5) is the single most important security control in this document. It effectively prevents "Privilege Escalation" by ensuring that even if a Mentor has `AdministratorAccess`, they cannot create a user that exceeds the boundary.

To ensure you understand the power of what you defined in `nash-{tenant}-boundary`, here is how the logic flows:

**Critique of Section 1.5:**
Your boundary allows `s3:*`. For 2025 best practices, we should apply **Data Perimeters**.

  * **Change:** Instead of `Resource: "*"`, enforce that S3 actions can only happen on buckets tagged `nash:tenant = personal`.
  * **Reason:** Prevents a compromised tenant role from exfiltrating data to an external S3 bucket (Data Exfiltration protection).

**Revised Snippet for 1.5:**

```hcl
      {
        Sid    = "AllowS3TenantOnly"
        Effect = "Allow"
        Action = "s3:*"
        Resource = "*"
        Condition = {
          StringEquals = {
            "aws:ResourceTag/nash:tenant" = each.key
          }
        }
      }
```

-----

### 3\. The "Break-Glass" Alerting Mechanism

In Section 1.6, you defined the `break_glass` role. In a "Single-Player Empire," relying on logs is not enough. You need to know *instantly* when this happens.

**The 2025 Standard:** The act of assuming a Break-Glass role must trigger an **Immediate PagerDuty/SMS Alert**.

**Add to Spec (Infrastructure Monitoring):**

  * **Event Pattern:** CloudTrail `AssumeRole` event where RoleName = `nash-break-glass-emergency`.
  * **Action:** Trigger Lambda -\> SNS -\> Your Phone.
  * **Why:** If you get that text message and *you* didn't trigger it, you know the empire is breached.

-----

### 4\. GCP Project Factory & Folders

Your GCP structure (Section 2.1) is solid, but managing custom roles (Section 2.2) is high-toil maintenance.

**Expert Advice:**
Instead of maintaining complex custom roles like `nashAdministrator`, leverage **GCP Conditional IAM Bindings**.

  * Grant `roles/owner` or `roles/editor`.
  * Add a Condition: `request.time < timestamp("2025-12-31T00:00:00Z")` (Time Bound) or `resource.name.startsWith("projects/nash-personal")`.

This reduces Terraform code maintenance. Google's standard roles are updated by Google; custom roles rot over time.

-----

### 5\. OIDC Federation Security (Github Actions)

In Section 1.3, you rely on `thumbprint_list`.
**Warning:** As of late 2023/2024, AWS stopped requiring thumbprints for widely known OIDC providers (like GitHub) because certificates rotate. Hardcoding `ffff...` is fine as a placeholder, but for 2025, you should use the explicit **Audience (`aud`)** and **Subject (`sub`)** strictly.

**Refining the Trust Policy (Section 1.4):**
Your `sub` condition is: `"repo:The-Nash-Group/the-citadel:ref:refs/heads/main"`.
**Recommendation:** For the "AI Lab" tenant, allow `pull_request` events too, so Agents can run speculative plans in PRs.

```hcl
"token.actions.githubusercontent.com:sub" = [
  "repo:The-Nash-Group/the-citadel:ref:refs/heads/main",
  "repo:The-Nash-Group/the-citadel:pull_request" # Allow planning on PRs
]
```

-----

### 6\. Summary of Recommended Changes for Version 1.1.0

1.  **Agent Sandbox:** Create specific IAM roles for "Synthetic Users" (Agents) with stricter quota/cost boundaries than CI/CD roles.
2.  **Data Perimeters:** Tighten Section 1.5 to prevent data exfiltration by enforcing tags on `Resource` access, not just Identity.
3.  **Active Alerting:** Add an `EventBridge` rule for the "Break-Glass" role.
4.  **Simplify GCP:** Move away from heavy Custom Roles; use Conditional IAM Bindings with standard roles where possible.

**Would you like me to draft the Terraform code for the "Agent Sandbox" or the "Break-Glass Alerter" next?**

This draft provides the concrete Terraform code for the two "Missing Links" in your architecture.

These files are designed to be dropped into `the-citadel/terraform/aws/iam/` (or a dedicated module). They adhere strictly to **Terraform v1.14+** standards and your **Nash Group** naming conventions.

### 1\. The Agent Sandbox (Synthetic User)

**Purpose:** Defines a "Synthetic User" identity for AI Agents. Unlike CI/CD roles, this role has *broad* read/write permissions (to experiment) but is caged by a **Permissions Boundary** that physically prevents it from spending money or breaking the Covenant.

**File:** `terraform/aws/iam/agent-sandbox.tf`

```hcl
# -----------------------------------------------------------------------------
# AGENT SANDBOX IDENTITY
# Context: The "Explorer" / "Specialist" Synthetic Users
# Policy: SEC-003 (Least Privilege) & FIN-001 (Cost Control)
# -----------------------------------------------------------------------------

# 1. The Sandbox Boundary (The "Cage")
# This policy limits the MAXIMUM permissions an agent can ever have,
# regardless of what policies you attach to it later.
resource "aws_iam_policy" "agent_sandbox_boundary" {
  name        = "nash-agent-sandbox-boundary"
  description = "Hard limits for AI Agents: Cost controls, Region locks, and Anti-Escalation."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # ALLOW: Core Innovation Services (The Sandbox)
      # Agents can spawn compute, store data, and use AI models.
      {
        Sid    = "AllowSandboxServices"
        Effect = "Allow"
        Action = [
          "s3:*",
          "dynamodb:*",
          "lambda:*",
          "bedrock:*", # Generative AI access
          "sqs:*",
          "sns:*",
          "logs:*"
        ]
        Resource = "*"
      },

      # ALLOW: Restricted EC2 (Low Cost Only)
      # Agents can launch instances, but we filter types in a Deny rule below.
      {
        Sid    = "AllowEC2Lifecycle"
        Effect = "Allow"
        Action = [
          "ec2:RunInstances",
          "ec2:TerminateInstances",
          "ec2:Describe*",
          "ec2:CreateTags"
        ]
        Resource = "*"
      },

      # DENY: Cost Anomalies (The "Wallet Guard")
      # Prevent agents from spinning up expensive hardware or committing to contracts.
      {
        Sid    = "DenyExpensiveCompute"
        Effect = "Deny"
        Action = "ec2:RunInstances"
        Resource = "arn:aws:ec2:*:*:instance/*"
        Condition = {
          # Forbid anything larger than 'large' or GPU instances unless explicitly whitelisted
          StringNotLike = {
            "ec2:InstanceType" = ["t3.*", "t4g.*", "m7g.medium", "m7g.large"]
          }
        }
      },
      {
        Sid    = "DenyCostCommitments"
        Effect = "Deny"
        Action = [
          "ec2:Purchase*",
          "ec2:CreateCapacityReservation",
          "savingsplans:*"
        ]
        Resource = "*"
      },

      # DENY: Privilege Escalation (The "Jailbreak" Guard)
      # Agents cannot change their own permissions or create new admins.
      {
        Sid    = "DenyIAMWrite"
        Effect = "Deny"
        Action = [
          "iam:Create*",
          "iam:Delete*",
          "iam:Update*",
          "iam:Put*",
          "iam:Attach*",
          "sso:*"
        ]
        Resource = "*"
      },

      # DENY: Region Lock (The "Geofence")
      # Agents operate only in the designated AI Lab region.
      {
        Sid    = "DenyForeignRegions"
        Effect = "Deny"
        Action = "*"
        Resource = "*"
        Condition = {
          StringNotEquals = {
            "aws:RequestedRegion" = [var.aws_region, "us-east-1"] # us-east-1 required for global services
          }
        }
      }
    ]
  })
}

# 2. The Agent Role (The "Synthetic User")
resource "aws_iam_role" "ai_researcher_agent" {
  name = "nash-ai-lab-agent-01"
  description = "Synthetic User for Autonomous AI Research"

  # Agents authenticate via OIDC (e.g., from a local orchestrator or GitHub Actions)
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.github_actions.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringLike = {
          # Allow PRs to run agents speculatively
          "token.actions.githubusercontent.com:sub" = "repo:The-Nash-Group/ai-lab-agents:*"
        }
      }
    }]
  })

  # ATTACH THE CAGE
  permissions_boundary = aws_iam_policy.agent_sandbox_boundary.arn

  # Standard Governance Tags
  tags = {
    "nash:clan"          = "explorers"
    "nash:tier"          = "experimental"
    "nash:environment"   = "dev"
    "nash:tenant"        = "ai-lab"
    "nash:identity_type" = "synthetic"
    "nash:policy_id"     = "SEC-003"
  }
}

# 3. Permission Assignment
# Give the agent 'PowerUser' access, effectively filtered down by the Boundary above.
resource "aws_iam_role_policy_attachment" "agent_power_user" {
  role       = aws_iam_role.ai_researcher_agent.name
  policy_arn = "arn:aws:iam::aws:policy/PowerUserAccess"
}
```

-----

### 2\. The Break-Glass Alerter

**Purpose:** The "Single-Player Empire" Safety Net. If *anyone* (even you) assumes the Emergency Admin role, your phone receives an SMS immediately.

**File:** `terraform/aws/observability/break-glass-alert.tf`

```hcl
# -----------------------------------------------------------------------------
# BREAK-GLASS ALERTING
# Context: The Watchers / Security Operations
# Policy: OPS-010 (Emergency Response)
# -----------------------------------------------------------------------------

# 1. The SNS Topic (The "Siren")
resource "aws_sns_topic" "security_alerts" {
  name         = "nash-security-alerts-critical"
  display_name = "🛡️ NASH SEC ALERT"

  kms_master_key_id = "alias/aws/sns" # Encrypted at rest

  tags = {
    "nash:clan"        = "watchers"
    "nash:tier"        = "core"
    "nash:environment" = "prod"
  }
}

# 2. Your Phone Subscription
# NOTE: After apply, you MUST click the confirmation link sent to your phone.
resource "aws_sns_topic_subscription" "guardian_sms" {
  topic_arn = aws_sns_topic.security_alerts.arn
  protocol  = "sms"
  endpoint  = var.guardian_phone_number # Define in variables.tf
}

# 3. EventBridge Rule (The "Trigger")
resource "aws_cloudwatch_event_rule" "break_glass_used" {
  name        = "nash-detect-break-glass-usage"
  description = "Triggers when the Emergency Break-Glass role is assumed"
  event_bus_name = "default"

  # Event Pattern: Looks for successful AssumeRole calls on the specific ARN
  event_pattern = jsonencode({
    "source"      = ["aws.iam"],
    "detail-type" = ["AWS API Call via CloudTrail"],
    "detail" = {
      "eventName" = ["AssumeRole"],
      "requestParameters" = {
        "roleArn" = [aws_iam_role.break_glass.arn]
      }
    }
  })

  tags = {
    "nash:policy_id" = "OPS-010"
  }
}

# 4. Connect Rule to SNS
resource "aws_cloudwatch_event_target" "alert_sns" {
  rule      = aws_cloudwatch_event_rule.break_glass_used.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.security_alerts.arn

  # Transform the JSON event into a readable SMS text
  input_transformer {
    input_paths = {
      user = "$.detail.userIdentity.principalId"
      ip   = "$.detail.sourceIPAddress"
      time = "$.time"
    }
    input_template = "\"🚨 CITADEL ALERT: Break-Glass Protocol Activated!\\nUser: <user>\\nIP: <ip>\\nTime: <time>\\nInvestigate Immediately.\""
  }
}

# 5. Allow EventBridge to Publish to SNS
resource "aws_sns_topic_policy" "allow_events" {
  arn = aws_sns_topic.security_alerts.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "AllowEventBridge"
      Effect = "Allow"
      Principal = {
        Service = "events.amazonaws.com"
      }
      Action   = "sns:Publish"
      Resource = aws_sns_topic.security_alerts.arn
    }]
  })
}
```

### 3\. Updated Variables for Context

Add these to your `terraform/aws/variables.tf` to support the new resources.

```hcl
variable "guardian_phone_number" {
  description = "E.164 format phone number for critical security alerts (e.g. +19075550100)"
  type        = string
  sensitive   = true # Will be masked in logs
}
```

### How this meets your November 2025 "Agentic" Needs:

1.  **The Sandbox:** You can unleash an AI agent to "go build an app" in the `ai-lab` tenant. It can create S3 buckets and Lambda functions, but if it tries to spin up a `$5,000/hr` GPU cluster or delete your IAM roles, the **Permissions Boundary** kills the API call instantly.
2.  **The Alerter:** It ensures that the `break_glass` role (which bypasses standard protections) cannot be used silently. This fulfills the **"Single-Player"** requirement—you don't need a 24/7 SOC watching logs; your phone is the SOC.
