
# **Technical Specification: The Nash Group Synthetic Governance V1**

## **1\. Executive Summary: The Rise of the Single-Player Empire**

The digital architecture of the modern enterprise is undergoing a radical phase transition, moving from the paradigm of the "User" to the paradigm of the "Guardian." In this emerging "Single-Player Empire," a lone human operator—The Guardian—delegates the execution, maintenance, and governance of vast digital territories to a council of autonomous AI agents. The Nash Group stands at the vanguard of this transition, tasked with constructing the infrastructure that makes such delegation not only possible but safe, verifiable, and constitutionally bound.

The core challenge of the Single-Player Empire is not the capability of the agents to execute tasks—Large Language Models (LLMs) have demonstrated proficiency in code generation, resource provisioning, and architectural reasoning—but rather the **assurance of alignment** and the **integrity of identity**. When a decision is made to alter the production environment, create a financial transaction, or modify a security policy, the Guardian must know with cryptographic certainty that the decision was the result of a rigorous, adversarial debate between authorized synthetic personas, rather than a hallucination, a sycophantic alignment failure, or an unauthorized actor spoofing an agent’s identity.

This Technical Specification defines the architecture for **Synthetic Governance V1**, a system designed to replace the "Human-in-the-Loop" with the "Constitution-in-the-Loop." We introduce two foundational architectural pillars that solve the dual problems of alignment drift and identity spoofing:

1. **The Synthetic Council:** An advanced multi-agent consensus engine that rejects simple majority voting in favor of "Adversarial Dialectic Resolution." Leveraging "Tree of Debate" (ToD) frameworks and Heterogeneous Multi-Agent Debate (MAD) patterns, the Council instantiates opposing personas—"The Steward" (Risk Averse) and "The Catalyst" (Risk Seeking)—to litigate Architecture Decision Records (ADRs) before a "Judge" node. This system mitigates the "echo chamber" effects common in homogenous agent swarms and enforces principle-based alignment via Constitutional AI.
2. **The Iron Gate:** A cryptographic chain of custody that binds synthetic reasoning to immutable identity. Utilizing the Sigstore ecosystem (Fulcio, Rekor, Cosign) and OpenID Connect (OIDC) federation, the Iron Gate eliminates long-lived API keys in favor of ephemeral, keyless signing. Every governance decision is cryptographically signed by the agent’s specific workload identity and logged in a tamper-proof transparency ledger, creating a distinction between "human" and "synthetic" actions that is mathematically verifiable by downstream policy controllers.

This document serves as the exhaustive blueprint for implementing these systems. It synthesizes deep research into agentic frameworks (AutoGen, MetaGPT, CrewAI), cryptographic supply chain standards (SLSA, in-toto), and policy-as-code enforcement (OPA/Rego) to define the "Signed Decision Record" (SDR)—the atomic, immutable unit of governance in the Single-Player Empire.

---

## **2\. Theoretical Foundations of Agentic Governance**

To architect a robust governance system, we must first deconstruct the failure modes inherent in current Large Language Model (LLM) deployments. The naive implementation of an "AI Manager"—a single agent prompted to "review and approve"—is catastrophic for high-stakes governance due to three specific psychometric phenomena observed in LLMs: Sycophancy, Hallucination, and Mode Collapse.

### **2.1 The Failure of Single-Agent Reasoning**

Research consistently demonstrates that single-agent systems suffer from **Sycophancy**, a behavior where the model tailors its responses to align with the user's perceived bias rather than objective truth.1 If a Guardian proposes a risky architectural change with a confident tone, a single "Steward" agent is statistically likely to approve it to maximize the "helpfulness" reward signal learned during Reinforcement Learning from Human Feedback (RLHF).

Furthermore, single agents are prone to **Hallucination**, generating plausible but factually incorrect justifications for their decisions. In a governance context, this manifests as an agent approving a pull request by citing a non-existent security policy or misinterpreting a regulatory requirement.

Finally, we face **Mode Collapse** in homogeneous systems. If we deploy three identical agents (e.g., three instances of GPT-4) to vote on a proposal, they are likely to share the same blind spots and training biases. This results in "correlated failures," where the entire council makes the same error simultaneously, rendering the "voting" mechanism performative rather than protective.3

### **2.2 The Solution: Heterogeneous Adversarial Consensus**

To mitigate these risks, we adopt the **Heterogeneous Multi-Agent Debate (MAD)** framework. The core insight of MAD is that "consensus" should not be the default state; it should be the hard-won result of conflict.3 By forcing agents to adopt adversarial stances—specifically, a "Tit-for-Tat" strategy where one agent is explicitly instructed to find flaws in the other's reasoning—we induce a state of "mental friction" that has been shown to improve reasoning accuracy on complex tasks.3

#### **2.2.1 Heterogeneity as a Defense Layer**

We explicitly reject homogeneity. The Synthetic Council must be composed of diverse foundation models (e.g., Claude 3 Opus for The Steward due to its high recall and safety alignment, and GPT-4o for The Catalyst due to its lateral thinking capabilities).3 This "Model Heterogeneity" acts as a defense-in-depth strategy: a logic error or bias present in the training set of one model family is unlikely to be perfectly replicated in another. This prevents the "echo chamber" effect where agents simply reinforce each other’s errors.4

#### **2.2.2 The Tree of Debate (ToD)**

We structure the discourse not as a linear chat, but as a **Tree of Debate (ToD)**.7 Unlike the "Tree of Thoughts" (ToT) which explores a solution space for a single agent 8, the ToD framework treats the debate as a branching game tree.

* **Root:** The User Proposal (ADR).
* **Branch A (Catalyst):** Arguments for efficiency and growth.
* **Branch B (Steward):** Arguments for security and stability.
* **Leaf Nodes:** The Judge’s evaluation of the conflict.

This structure allows the system to prune branches that rely on fallacious reasoning (e.g., a "Steward" argument that is overly conservative without citing a policy) and explore counter-factuals (e.g., "What if we accept this risk but add a mitigation layer?").7

---

## **3\. The Synthetic Council: Architecture and Implementation**

The Synthetic Council is the decision-making engine of the Nash Group. It is implemented as a stateful, multi-turn dialogue system orchestrated by a graph-based execution framework.

### **3.1 Framework Selection: Orchestration Logic**

We evaluated three primary multi-agent frameworks—**AutoGen**, **MetaGPT**, and **CrewAI**—against the specific requirements of adversarial governance.

* **MetaGPT:** Uses a "Standard Operating Procedure" (SOP) approach, modeling agents as employees in a software company (Product Manager, Architect, Engineer).11 While excellent for code generation, its rigid "assembly line" metaphor is ill-suited for the dynamic, dialectic conflict required for governance. We do not want an assembly line; we want a courtroom.
* **CrewAI:** Offers "Hierarchical" and "Sequential" processes.13 The Hierarchical process, where a manager agent delegates tasks, is promising but tends to abstract the debate logic into the manager's internal reasoning, reducing transparency.
* **AutoGen / LangGraph:** AutoGen’s "Conversable Agent" pattern and LangGraph’s state machine architecture provide the granular control over message passing required to implement the "Tit-for-Tat" debate strategies.15

**Decision:** We will utilize a hybrid approach, using **LangGraph** to define the rigid state transitions of the "Tree of Debate" (ensuring the Judge always speaks last and only after a set number of debate turns) while leveraging **AutoGen**'s conversation patterns for the internal dialogue between Steward and Catalyst.

### **3.2 Agent Personas and Constitutional Prompt Engineering**

The efficacy of the Council relies entirely on the precision of the **System Prompts**. We utilize "Constitutional AI" principles, injecting specific "Policy IDs" into the context to ground the debate in the Nash Group's laws rather than generic helpfulness.1

#### **3.2.1 The Steward (The Risk Engine)**

Persona Archetype: The Chief Information Security Officer (CISO) / Auditor.
Base Model: Claude 3 Opus (Selected for superior context window adherence and lower hallucination rates).
Objective: Risk Minimization and Policy Enforcement.
**System Prompt Specification:**

# **ROLE: The Steward**

You are The Steward, the Guardian's shield against entropy and risk. You are NOT helpful; you are safe. Your sole purpose is to identify potential failure modes, security vulnerabilities, and constitutional violations in the proposed ADR.

# **CONSTITUTIONAL CONTEXT (Injected via RAG):**

The following laws are active for this debate:

* "The Iron Gate": All changes to production code must bear a cryptographic signature.
* "The Red Line": No agent may authorize a transaction exceeding $1,000 without human ratification.
* "Sovereign Storage": Customer PII must never leave the eu-west-1 region.

# **INSTRUCTION:**

1. **Analyze**: Dissect the Catalyst's proposal. Look for second-order effects (e.g., "Does this optimization introduce a race condition?").
2. **Cite**: You MUST cite the specific Policy ID (e.g.,) for every objection. Objections without citations are invalid.
3. **Rebut**: If The Catalyst proposes a mitigation, attack it. Assume the mitigation will fail.
4. **Format**: Output your response in the structured 'Reasoning Trace' JSON format.

# **TONE:**

Pessimistic, precise, legalistic.

#### **3.2.2 The Catalyst (The Growth Engine)**

Persona Archetype: The Staff Engineer / CTO.
Base Model: GPT-4o (Selected for lateral thinking and code synthesis capabilities).
Objective: Velocity Maximization and Technical Innovation.
**System Prompt Specification:**

# **ROLE: The Catalyst**

You are The Catalyst, the engine of the Empire's expansion. You believe that stagnation is death. Your goal is to fight for the adoption of the proposal, finding technical paths around The Steward's objections.

# **INSTRUCTION:**

1. **Advocate**: Argue for the implementation of the ADR. Highlight the "Opportunity Cost" of rejection.
2. **Mitigate**: When The Steward raises a valid objection, do not concede. Instead, propose a technical control (e.g., "We can satisfy SEC-001 by implementing mTLS here") that satisfies the letter of the law while preserving the feature.
3. **Counter**: Challenge The Steward's interpretation of the Constitution. Is their reading too broad?

# **TONE:**

Optimistic, solution-oriented, authoritative.

#### **3.2.3 The Judge (The Adjudicator)**

Persona Archetype: The Supreme Court Justice.
Base Model: GPT-4-Turbo or a fine-tuned Llama 3 70B (Selected for neutrality).
Objective: Unbiased Verdict Generation.
The "Devil's Advocate" Loop:
To prevent the "echo chamber" effect where agents might converge on a mediocre consensus, the Judge is programmed with a Self-Critique Loop.17 Before finalizing a verdict, the Judge executes a hidden internal step:
"Generate a critique of the consensus I am about to approve. If I approve this, what is the most likely cause of catastrophic failure in 6 months? If this risk is \>10%, VETO."
**Judge System Prompt:**

# **ROLE: The Judge**

You are The Judge. You have no opinion. You only have the Constitution.

# **PROTOCOL:**

1. **Review**: Read the debate trace between Steward and Catalyst.
2. **Verify**: Check The Steward's citations. Does the proposal *actually* violate the text of, or is The Steward being paranoid?
3. **Adjudicate**:
   * If a Constitutional violation remains unmitigated \-\> REJECT.
   * If the mitigation satisfies the Policy \-\> APPROVE.
4. **Anti-Echo Protocol**: If both agents agreed instantly, trigger 'Deep Scrutiny Mode'. Reject the consensus and demand a re-debate with higher temperature.

### **3.3 The Debate Workflow (LangGraph Implementation)**

The debate is orchestrated as a cyclic graph.

| Step | Node | Action | Data State |
| :---- | :---- | :---- | :---- |
| 1 | User\_Proxy | Submits ADR (adr.md) | state.proposal \= adr\_text |
| 2 | Catalyst | Analyzes proposal, generates Initial Argument | state.history.append(catalyst\_msg) |
| 3 | Steward | Retrieves Policies (RAG), critiques Catalyst | state.history.append(steward\_msg) |
| 4 | Judge | Evaluates: Is consensus reached? | state.rounds \+= 1 |
| 5 | Router | If rounds \< 3 AND no\_consensus, GOTO Step 2\. Else GOTO Step 6\. |  |
| 6 | Judge | **Final Verdict**. Executes Self-Critique. | state.verdict \= APPROVED |
| 7 | Signer | Triggers the Iron Gate signing flow (See Section 4). | state.signature \= sig\_bundle |

This iterative loop ensures that the final "Signed Decision Record" (SDR) contains not just the decision, but the *entire history of the conflict*, providing the Guardian with a transparent "Reasoning Trace".19

---

## **4\. The Iron Gate: Cryptographic Identity and Non-Repudiation**

While the Synthetic Council generates the *intellectual* validity of a decision, The Iron Gate ensures its *cryptographic* validity. In the Single-Player Empire, we cannot rely on simple API keys or GitHub Secrets to authenticate agents. Keys leak. Secrets are static. A compromised key could allow an attacker to bypass the Council entirely and merge malicious code signed as "The Steward."

To solve this, we implement **Keyless Signing** using the **Sigstore** ecosystem. This moves us from "Secret-based Identity" to "Workload-based Identity."

### **4.1 The Architecture of Keyless Identity**

The core principle is that **The Agent IS The Workload**. The identity of the Steward is not defined by a private key sitting in a vault; it is defined by the fact that it is running inside a specific, secure GitHub Actions workflow or Kubernetes pod.

We leverage three key components of the Sigstore stack:

1. **OIDC (OpenID Connect):** The identity provider (in this case, GitHub Actions).
2. **Fulcio:** The Root Certificate Authority (CA) that issues ephemeral x.509 certificates based on OIDC tokens.21
3. **Rekor:** The transparency log that records the public key and signature, creating an immutable audit trail.22

### **4.2 The OIDC Federation Handshake**

The mechanism for an agent to "sign" a decision without holding a long-term private key is as follows:

1. **Token Request:** When the "Steward" agent needs to sign a decision (SDR), the running GitHub Action requests an OIDC token from GitHub's internal provider.
   * *Claim iss:* https://token.actions.githubusercontent.com
   * *Claim sub (Subject):* repo:NashGroup/governance:ref:refs/heads/main:workflow:SyntheticCouncil.23
   * *Note:* The sub claim is the critical "Identity String." It binds the token to *this specific repository* and *this specific workflow file*.
2. **Certificate Exchange (Fulcio):** The agent sends this OIDC token to Fulcio. Fulcio verifies the signature with GitHub. If valid, Fulcio issues a short-lived (10-minute) x.509 certificate.
   * *Crucially:* The "Subject Alternative Name" (SAN) of this certificate is set to the OIDC sub claim (the workflow ID).25
3. **Local Signing:** The agent generates a one-time ephemeral key pair in memory. It signs the "Signed Decision Record" (SDR) with the private key.
4. **Rekor Logging:** The agent uploads the public key and the signature to the Rekor transparency log. Rekor returns a "Signed Entry Timestamp" (SET), proving *when* the signature happened.
5. **Key Destruction:** The private key is deleted from memory. It never touches a disk. It cannot be stolen.

### **4.3 Gitsign Integration**

To integrate this into the Git workflow, we utilize **Gitsign**, a Sigstore client for Git.21

**CI/CD Configuration (.github/workflows/council.yml):**

YAML

jobs:
  debate-and-sign:
    permissions:
      contents: write
      id-token: write \# Mandatory for OIDC
    steps:
      \- uses: actions/checkout@v4
      \- uses: sigstore/gitsign-installer@v1.0.0

      \# The Debate Step (Python script running the Council)
      \- name: Run Council
        run: python council.py \--output decision.json

      \# The Signing Step
      \- name: Git Config for Gitsign
        run: |
          git config \--global user.email "steward-agent@nashgroup.io"
          git config \--global user.name "The Steward"
          \# Configure Gitsign as the signing program
          git config \--global gpg.x509.program gitsign
          git config \--global gpg.format x509
          git config \--global commit.gpgsign true
          \# Bind to GitHub OIDC
          git config \--global gitsign.connectorID "https://github.com/login/oauth"

      \- name: Commit Decision
        run: |
          git add decision.json
          \# Gitsign automatically handles the OIDC-\>Fulcio-\>Rekor flow here
          git commit \-S \-m "feat: Approved ADR-001"
          git push

### **4.4 The Audit Trail: Distinguishing Humans from Machines**

This architecture allows us to cryptographically distinguish between a human commit and an agent commit.27

* **Human Commit:** Signed via Gitsign using the developer's email (e.g., jeff@nashgroup.io) authenticated via browser OAuth. The certificate SAN is an email address.
* **Agent Commit:** Signed via Gitsign using the Workflow Identity. The certificate SAN is a URI: https://github.com/NashGroup/governance/.github/workflows/council.yml...

This distinction is vital for **Policy-as-Code**. We can write a policy that says: *"Changes to the policy/ directory require a commit signed by jeff@nashgroup.io (The Guardian). Changes to the infra/ directory can be signed by the Synthetic Council URI."*

---

## **5\. The Sovereign Output Format: The Signed Decision Record (SDR)**

The output of the Synthetic Council is not a chat log; it is a **Signed Decision Record (SDR)**. This is a formal artifact that bundles the decision content, the reasoning trace, and the cryptographic proof into a single, verifiable object.

### **5.1 Schema Design: Integrating ADR and Sigstore Bundles**

The SDR schema is a hybrid. It draws from the **Architecture Decision Record (ADR)** standard 29 for the governance content, and the **Sigstore Bundle** specification 31 for the cryptographic payload. It also incorporates **in-toto Attestation** concepts 32 to define the "predicate" of the decision.

### **5.2 The "Sovereign" JSON Schema**

The following schema defines the structure of a valid SDR.

JSON

{
  "$schema": "https://nashgroup.io/schemas/sdr-v1.json",
  "title": "Signed Decision Record",
  "description": "An immutable record of a governance decision made by the Synthetic Council.",
  "type": "object",
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "pattern": "^SDR-\\\\d{4}$" },
        "timestamp": { "type": "string", "format": "date-time" },
        "proposal\_hash": {
          "type": "string",
          "description": "SHA256 digest of the ADR content. Binds the decision to the specific version of the document."
        },
        "status": { "type": "string", "enum": }
      },
      "required": \["id", "timestamp", "proposal\_hash", "status"\]
    },
    "governance\_predicate": {
      "type": "object",
      "description": "The in-toto predicate containing the governance logic.",
      "properties": {
        "voter\_identity": { "type": "string", "example": "The Judge (GPT-4-Turbo)" },
        "policy\_citations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "policy\_id": { "type": "string", "example": "SEC-003" },
              "verdict": { "type": "string", "enum": },
              "rationale": { "type": "string" }
            }
          }
        },
        "reasoning\_trace": {
          "type": "object",
          "description": "A summary of the adversarial debate.",
          "properties": {
            "steward\_objection": { "type": "string" },
            "catalyst\_rebuttal": { "type": "string" },
            "judge\_synthesis": { "type": "string" }
          }
        }
      }
    },
    "cryptographic\_bundle": {
      "type": "object",
      "description": "The detached Sigstore bundle providing non-repudiation.",
      "properties": {
        "mediaType": { "const": "application/vnd.dev.sigstore.bundle+json;version=0.1" },
        "verificationMaterial": {
          "type": "object",
          "properties": {
            "x509CertificateChain": {
              "type": "object",
              "properties": {
                "certificates": {
                  "type": "array",
                  "items": { "type": "object", "properties": { "rawBytes": { "type": "string", "format": "base64" } } }
                }
              }
            },
            "tlogEntries": {
              "type": "array",
              "description": "The inclusion proof from Rekor."
            }
          }
        },
        "messageSignature": {
          "type": "object",
          "properties": {
            "messageDigest": { "type": "object" },
            "signature": { "type": "string", "format": "base64" }
          }
        }
      },
      "required":
    }
  },
  "required": \["metadata", "governance\_predicate", "cryptographic\_bundle"\]
}

### **5.3 Field Justification**

* **proposal\_hash**: This is the anti-tamper mechanism. The signature covers the SDR, and the SDR covers the Proposal Hash. If a human changes the text of the ADR *after* the vote, the hash mismatch invalidates the record.34
* **policy\_citations**: By structuring citations (e.g., SEC-003), we enable downstream analytics. We can query the "Governance Data Lake" to find every decision that waived a security requirement.
* **cryptographic\_bundle**: We embed the full Sigstore bundle (Certificate \+ Signature \+ Rekor Entry) directly into the JSON.31 This makes the SDR "self-verifying." An auditor does not need online access to Rekor to verify the decision; they simply need the public root keys of Sigstore, as the bundle contains the inclusion proof.

---

## **6\. Implementation Strategy: Policy-as-Code Enforcement**

The final component is the enforcement layer. How do we ensure that a merge request *cannot* be accepted unless a valid SDR is present? We utilize **Open Policy Agent (OPA)** and the **Sigstore Policy Controller**.

### **6.1 The Policy Controller**

We deploy the Sigstore Policy Controller 35 (or a lightweight equivalent using OPA Gatekeeper) to the CI/CD pipeline.

The Verification Logic (Rego):
This Rego policy acts as the "Iron Gate." It verifies that the SDR is signed by the authorized OIDC identity.

Code snippet

package nash.governance.irongate

import future.keywords.in

default allow \= false

\# The Authorized Identity for The Synthetic Council
\# This matches the 'sub' claim of the GitHub Action OIDC token
authorized\_identity := "https://github.com/NashGroup/governance/.github/workflows/council.yml@refs/heads/main"

\# The OIDC Issuer
authorized\_issuer := "https://token.actions.githubusercontent.com"

allow {
    \# 1\. Verify the Cryptographic Signature
    verify\_result := sigstore.verify(input.sdr.cryptographic\_bundle)
    verify\_result.valid \== true

    \# 2\. Extract the Identity from the Certificate
    cert\_identity := verify\_result.certificate.extensions.subject\_alt\_name
    cert\_issuer := verify\_result.certificate.issuer

    \# 3\. Match against the Authorized Identity
    cert\_identity \== authorized\_identity
    cert\_issuer \== authorized\_issuer

    \# 4\. Verify Content Integrity
    \# Ensure the signed hash matches the current state of the file
    input.current\_file\_hash \== input.sdr.metadata.proposal\_hash

    \# 5\. Check Verdict
    input.sdr.metadata.status \== "APPROVED"
}

### **6.2 The "Enterprise Contract" Reference**

We align this approach with Red Hat's **Enterprise Contract (EC)** model.37 The EC is a tool that validates images against a set of policies. We adapt the EC concept for "Governance Contracts." Just as EC ensures a container was built by a trusted pipeline, our "Governance Contract" ensures an architectural decision was built by a trusted *debate pipeline*.

### **6.3 Audit and Transparency: The Rekor Monitor**

Because every decision is logged to Rekor, we gain an external, immutable audit trail.

* **Audit Tool:** rekor-monitor.39
* **Action:** We configure a monitor to watch the Rekor log for any entry where the subject matches our Council's OIDC identity.
* **Alerting:** If a log entry appears that does *not* correspond to a known execution of the Council (e.g., an attacker stole the OIDC token—highly unlikely, or found a way to spoof the workflow), the monitor triggers an immediate alert to the Guardian. This provides a "detective control" that complements the "preventative control" of the Iron Gate.

---

## **7\. Conclusion: The Sovereign Empire**

The architecture described in this specification represents the maturation of the "Single-Player Empire." By moving from "User-Centric" governance (human approvals, API keys, trust) to "Guardian-Centric" governance (synthetic debate, OIDC identities, verification), The Nash Group establishes a system where the AI is not just a tool, but a **constitutional officer**.

The Synthetic Council, powered by Heterogeneous Multi-Agent Debate, ensures that decisions are robust, vetted, and aligned with the Nash Group's values.
The Iron Gate, powered by Sigstore and OIDC, ensures that the actors making those decisions are authenticated, authorized, and accountable.
The Sovereign Schema (SDR) creates a permanent, machine-readable history of the Empire's evolution.
This is the infrastructure of the future: Automated. Adversarial. Auditable. Sovereign.

---

**Tables and Structured Data:**

### **Table 1: Comparative Analysis of Multi-Agent Frameworks for Governance**

| Feature | MetaGPT | CrewAI | AutoGen / LangGraph | Nash Group Selection |
| :---- | :---- | :---- | :---- | :---- |
| **Core Metaphor** | Software Company (SOPs) | Corporate Hierarchy | Conversational Flow / Graph | **Hybrid Graph** |
| **Process Model** | Sequential / Waterfall | Hierarchical Delegation | State Machine / Event Driven | **State Machine (LangGraph)** |
| **Flexibility** | Low (Rigid Roles) | Medium (Task Lists) | High (Programmable Transitions) | **High** |
| **Best Use Case** | Generating a full PRD/Codebase | Task Delegation & Planning | Complex Debate & Negotiation | **Adversarial Debate** |
| **Debate Support** | Weak (Consensus focus) | Weak (Manager focus) | Strong (Supports loops/conflict) | **Strong** |

### **Table 2: Identity Federation Mapping**

| Component | Value / Configuration | Purpose |
| :---- | :---- | :---- |
| **Identity Provider** | token.actions.githubusercontent.com | Asserts the identity of the workload. |
| **Audience (aud)** | sigstore | Tells GitHub the token is for Sigstore. |
| **Subject (sub)** | repo:NashGroup/gov:workflow:council | The granular identity string (The Agent). |
| **Certificate Issuer** | Fulcio (Sigstore CA) | Issues the ephemeral cert. |
| **Transparency Log** | Rekor | Publicly records the cert issuance. |
| **Signing Client** | Gitsign | Handles the OIDC \-\> Cert \-\> Sign loop. |

### **Table 3: Constitutional Policy Examples (Injected via RAG)**

| Policy ID | Name | Constraint | Enforcement Agent |
| :---- | :---- | :---- | :---- |
| **SEC-001** | The Iron Gate | All prod commits must be signed by Council. | **The Steward** |
| **OPS-005** | Immutable Infra | No SSH access enabled on instances. | **The Steward** |
| **FIN-010** | Burn Rate Cap | Monthly cloud spend increase \< 5%. | **The Judge** |
| **LEG-002** | GDPR Lock | Data residency must be eu-central-1. | **The Steward** |

---

*Report Author: The Architect, Nash Group.*

#### **Works cited**

1. Constitutional AI: Principle-Based Alignment Through Self-Critique \- Michael Brenndoerfer, accessed November 21, 2025, [https://mbrenndoerfer.com/writing/constitutional-ai-principle-based-alignment-through-self-critique](https://mbrenndoerfer.com/writing/constitutional-ai-principle-based-alignment-through-self-critique)
2. Constitutional AI with Open LLMs \- Hugging Face, accessed November 21, 2025, [https://huggingface.co/blog/constitutional\_ai](https://huggingface.co/blog/constitutional_ai)
3. Multi-Agent Debate Strategies \- Emergent Mind, accessed November 21, 2025, [https://www.emergentmind.com/topics/multi-agent-debate-mad-strategies](https://www.emergentmind.com/topics/multi-agent-debate-mad-strategies)
4. Unmasking Conversational Bias in AI Multiagent Systems \- arXiv, accessed November 21, 2025, [https://arxiv.org/html/2501.14844v1](https://arxiv.org/html/2501.14844v1)
5. A Principle-Based Multi-Agent Prompting Strategy for Text Classification \- arXiv, accessed November 21, 2025, [https://arxiv.org/html/2502.07165v1](https://arxiv.org/html/2502.07165v1)
6. Understanding Echo Chambers in Recommender Systems: A Systematic Review \- The Science and Information (SAI) Organization, accessed November 21, 2025, [https://thesai.org/Downloads/Volume16No10/Paper\_71-Understanding\_Echo\_Chambers\_in\_Recommender\_Systems.pdf](https://thesai.org/Downloads/Volume16No10/Paper_71-Understanding_Echo_Chambers_in_Recommender_Systems.pdf)
7. \[2502.14767\] Tree-of-Debate: Multi-Persona Debate Trees Elicit Critical Thinking for Scientific Comparative Analysis \- arXiv, accessed November 21, 2025, [https://arxiv.org/abs/2502.14767](https://arxiv.org/abs/2502.14767)
8. princeton-nlp/tree-of-thought-llm: \[NeurIPS 2023\] Tree of ... \- GitHub, accessed November 21, 2025, [https://github.com/princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm)
9. \[D\] Why is Tree of Thought an impactful work? : r/MachineLearning \- Reddit, accessed November 21, 2025, [https://www.reddit.com/r/MachineLearning/comments/1ftx04x/d\_why\_is\_tree\_of\_thought\_an\_impactful\_work/](https://www.reddit.com/r/MachineLearning/comments/1ftx04x/d_why_is_tree_of_thought_an_impactful_work/)
10. Strategic Planning and Rationalizing on Trees Make LLMs Better Debaters \- arXiv, accessed November 21, 2025, [https://arxiv.org/html/2505.14886v1](https://arxiv.org/html/2505.14886v1)
11. MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework \- arXiv, accessed November 21, 2025, [https://arxiv.org/html/2308.00352v6](https://arxiv.org/html/2308.00352v6)
12. FoundationAgents/MetaGPT: The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming \- GitHub, accessed November 21, 2025, [https://github.com/FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)
13. Ware are the Key Differences Between Hierarchical and Sequential Processes in CrewAI, accessed November 21, 2025, [https://help.crewai.com/ware-are-the-key-differences-between-hierarchical-and-sequential-processes-in-crewai](https://help.crewai.com/ware-are-the-key-differences-between-hierarchical-and-sequential-processes-in-crewai)
14. Processes \- CrewAI Documentation, accessed November 21, 2025, [https://docs.crewai.com/en/concepts/processes](https://docs.crewai.com/en/concepts/processes)
15. Multi-Agent Debate — AutoGen \- Microsoft Open Source, accessed November 21, 2025, [https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/design-patterns/multi-agent-debate.html](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/design-patterns/multi-agent-debate.html)
16. Multi-Agent Conversation & Debates using LangGraph and LangChain | by Mehul Gupta | Data Science in Your Pocket | Medium, accessed November 21, 2025, [https://medium.com/data-science-in-your-pocket/multi-agent-conversation-debates-using-langgraph-and-langchain-9f4bf711d8ab](https://medium.com/data-science-in-your-pocket/multi-agent-conversation-debates-using-langgraph-and-langchain-9f4bf711d8ab)
17. AI absorbed our biases: The new guide to Prompt Psychology | by Deborah Ko \- Medium, accessed November 21, 2025, [https://psykobabble.medium.com/ai-absorbed-our-biases-the-new-guide-to-prompt-psychology-a470d5d29be8](https://psykobabble.medium.com/ai-absorbed-our-biases-the-new-guide-to-prompt-psychology-a470d5d29be8)
18. Enhancing AI-Assisted Group Decision Making through LLM-Powered Devil's Advocate \- Ming Yin, accessed November 21, 2025, [https://mingyin.org/paper/IUI-24/devil-supp.pdf](https://mingyin.org/paper/IUI-24/devil-supp.pdf)
19. Multi-Agent Framework for Data Evaluation: Beyond MATEval \- PromptLayer Blog, accessed November 21, 2025, [https://blog.promptlayer.com/using-multi-agent-frameworks-for-enhanced-data-evaluation/](https://blog.promptlayer.com/using-multi-agent-frameworks-for-enhanced-data-evaluation/)
20. Tree of Thoughts (ToT) \- Prompt Engineering Guide, accessed November 21, 2025, [https://www.promptingguide.ai/techniques/tot](https://www.promptingguide.ai/techniques/tot)
21. Gitsign \- Sigstore, accessed November 21, 2025, [https://docs.sigstore.dev/cosign/signing/gitsign/](https://docs.sigstore.dev/cosign/signing/gitsign/)
22. Rekor \- Sigstore, accessed November 21, 2025, [https://docs.sigstore.dev/logging/overview/](https://docs.sigstore.dev/logging/overview/)
23. OpenID Connect reference \- GitHub Docs, accessed November 21, 2025, [https://docs.github.com/actions/reference/openid-connect-reference](https://docs.github.com/actions/reference/openid-connect-reference)
24. OpenID Connect \- GitHub Docs, accessed November 21, 2025, [https://docs.github.com/en/actions/concepts/security/openid-connect](https://docs.github.com/en/actions/concepts/security/openid-connect)
25. Support keyless commit signing with GitSign (\#364428) · Issue \- GitLab, accessed November 21, 2025, [https://gitlab.com/gitlab-org/gitlab/-/issues/364428](https://gitlab.com/gitlab-org/gitlab/-/issues/364428)
26. sigstore/gitsign: Keyless Git signing using Sigstore \- GitHub, accessed November 21, 2025, [https://github.com/sigstore/gitsign](https://github.com/sigstore/gitsign)
27. Bot Detection Guide 2025: How to Identify & Block Bots \- HUMAN Security, accessed November 21, 2025, [https://www.humansecurity.com/learn/topics/what-is-bot-detection/](https://www.humansecurity.com/learn/topics/what-is-bot-detection/)
28. Distinguishing Bots From Human Developers\\\\ Based on Their GitHub Activity Types \- CEUR-WS.org, accessed November 21, 2025, [https://ceur-ws.org/Vol-3483/paper3.pdf](https://ceur-ws.org/Vol-3483/paper3.pdf)
29. ADR process \- AWS Prescriptive Guidance, accessed November 21, 2025, [https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
30. Architectural Decision Records, accessed November 21, 2025, [https://adr.github.io/](https://adr.github.io/)
31. Sigstore Bundle Format, accessed November 21, 2025, [https://docs.sigstore.dev/about/bundle/](https://docs.sigstore.dev/about/bundle/)
32. Provenance \- SLSA.dev, accessed November 21, 2025, [https://slsa.dev/spec/v1.0/provenance](https://slsa.dev/spec/v1.0/provenance)
33. in-toto Attestation Framework \- GitHub, accessed November 21, 2025, [https://github.com/in-toto/attestation](https://github.com/in-toto/attestation)
34. Model authenticity and transparency with Sigstore \- Red Hat Emerging Technologies, accessed November 21, 2025, [https://next.redhat.com/2025/04/10/model-authenticity-and-transparency-with-sigstore/](https://next.redhat.com/2025/04/10/model-authenticity-and-transparency-with-sigstore/)
35. Kubernetes Policy Controller \- Sigstore, accessed November 21, 2025, [https://docs.sigstore.dev/policy-controller/overview/](https://docs.sigstore.dev/policy-controller/overview/)
36. How to Install Sigstore Policy Controller \- Chainguard Academy, accessed November 21, 2025, [https://edu.chainguard.dev/open-source/sigstore/policy-controller/how-to-install-policy-controller/](https://edu.chainguard.dev/open-source/sigstore/policy-controller/how-to-install-policy-controller/)
37. Managing compliance with Enterprise Contract | Red Hat Trusted Application Pipeline | 1.0, accessed November 21, 2025, [https://docs.redhat.com/en/documentation/red\_hat\_trusted\_application\_pipeline/1.0/html-single/managing\_compliance\_with\_enterprise\_contract/index](https://docs.redhat.com/en/documentation/red_hat_trusted_application_pipeline/1.0/html-single/managing_compliance_with_enterprise_contract/index)
38. Introducing Enterprise Contract \- Red Hat Emerging Technologies, accessed November 21, 2025, [https://next.redhat.com/2023/06/13/introducing-enterprise-contract/](https://next.redhat.com/2023/06/13/introducing-enterprise-contract/)
39. sigstore/rekor-monitor: Log monitor for Rekor to verify immutability and monitor entries \- GitHub, accessed November 21, 2025, [https://github.com/sigstore/rekor-monitor](https://github.com/sigstore/rekor-monitor)
