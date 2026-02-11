# Definitions & Scope: The Language of Sovereignty

## 2.1 Core Terminology

The License uses precise, battle-hardened definitions to prevent ambiguity. Unlike standard licenses where "Commercial Use" is vague, the Sovereign License defines it **by exclusion**—anything that *isn't* strictly personal or academic is Commercial.

### 2.1.1 "The Software" (The Protected Asset)
The definition of "Software" (Article 1.2) is **omnivorous**. It covers not just the code, but the *entirety* of the project's intellectual output.

**Includes:**
*   **Source Code**: `.py`, `.go`, `.rs`, `.js` files.
*   **Weights & Artifacts**: Trained models, checkpoints, LoRAs, embeddings.
*   **Knowledge**: Architecture diagrams, documentation, "design patterns," and "methodologies."
*   **Logs**: Terminal outputs, training logs, and generated metrics.

> [!WARNING]
> **Behavioral Equivalence (1.17)**:
> The License covers **"Clean Room" implementations**. If you define a system that *behaves* exactly like the Software based on observing it, you have created a "Derivative Work" and are bound by the License. You cannot "rewrite it in Rust" to bypass these terms.

### 2.1.2 "Financial Benefit" (The Poison)
"Financial Benefit" (1.4, 9.3) is the trigger for Commercial status. It is defined broadly to catch modern "growth-first" business models that don't generate immediate revenue.

**It includes:**
*   **Direct Revenue**: Sales, subscriptions.
*   **Valuation Growth**: Increasing the stock price or VC valuation.
*   **Cost Savings**: Using the software to do a job faster (time = money).
*   **Data Harvesting**: Using the software to generate training data for *other* models.
*   **Reputation**: "Clout" that leads to future investment.

### 2.1.3 "Service Deployment" (The SaaS Ban)
Article 1.5 explicitly bans **"As-A-Service"** use without a commercial license. This is the **Anti-SaaS Clause**.

**Prohibited Service Architectures:**
*   **REST APIs**: Wrapping the code in FastAPI/Express and selling access.
*   **Cloud Hosting**: Deploying it on AWS/GCP for internal team use.
*   **Discord Bots**: Public-facing bots that wrap the functionality.
*   **Background Workers**: Using it as a hidden processing engine for a larger app.

## 2.2 The "AI" Definition (Article 1.8)
The License explicitly recognizes "Artificial Intelligence" not just as code, but as **Cognitive Automation**.
*   **Scope**: LLMs, Transformers, Diffusion Models, Reinforcement Learning agents, and "Hybrid Systems."
*   **Implication**: If you use this Software to *train* an AI (e.g., generating synthetic data), that is a restricted activity (Article 4.5).

## 2.3 "Prohibited Party" vs. "Excluded Individual"

| Term | Definition | Implication |
| :--- | :--- | :--- |
| **Prohibited Party** (2.3) | A corporation or entity listed in the "Wall of Shame" (OpenAI, Google, etc.). | Cannot use the software. Period. |
| **Excluded Individual** (1.14, X.2) | A specific human being (Altman, Musk, etc.). | **Radioactive.** If they touch it, or benefit from it, the "Nuclear" liabilities of Article X trigger. |

> [!NOTE]
> The distinction matters because a **Prohibited Party** is a corporate entity (which can be dissolved), but an **Excluded Individual** is a biological person. The ban follows the person *forever*, across any company they start, join, or invest in.
