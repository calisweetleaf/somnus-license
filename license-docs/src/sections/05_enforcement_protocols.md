# Enforcement Protocols: The Leviathan

## 6.1 The "Strict Liability" Standard (Art. X.7)
Unlike most civil contracts where you argue about "intent" or "mistakes," this License operates on **Strict Liability**.
*   **Did you do it?** Yes.
*   **Are you liable?** Yes.
*   **Did you mean to?** Irrelevant.

This removes the "Innocent Infringement" defense. If you execute the code, you accept the liability.

### 6.1.1 The "Negative Proof" Burden Shift (X.3.6)
In a dispute, the License **reverses the burden of proof**.
1.  **Licensor Shows Use**: The Licensor only needs to show that you used the Software and subsequently made money.
2.  **Burden Shifts**: You must then prove that the Software made **exactly zero contribution** to that income.
3.  **7-Year Presumption**: Any financial benefit realized within **7 years** of using the Software is legally presumed to be caused by the Software. You must disprove this with contemporaneous documentation.

## 6.2 The Liquidated Damages Schedule (5.3)
Because proving "actual financial harm" for software is difficult, the License establishes **Pre-Agreed Penalties**. By using the software, you agree that these amounts are reasonable estimates of the damage caused.

### The Breakdown (USD per Incident)

| Offense | Penalty | Note |
| :--- | :--- | :--- |
| **Unauthorized Commercial Use** | **$100,000** | Basic breach. |
| **Service Deployment (SaaS)** | **$500,000** | Per deployment instance. |
| **AI Model Training** | **$1,000,000** | Per model trained. |
| **Article X Violation** | **$5,000,000** | **The Nuclear Option.** Per quarter. |
| **Prohibited Party Use** | **$2,000,000** | E.g., OpenAI employee use. |

> [!WARNING]
> **Cumulative Penalties**
> These stack. If you are an OpenAI employee (Prohibited Party) who trains a model (AI Training) and deploys it as an API (Service Deployment), your liability is:
> $2M + $1M + $500k = **$3.5 Million USD per incident.**

## 6.3 Enhanced Statutory Damages (5.4)
In addition to the contract damages above, the Licensor can elect **Copyright Damages**.
*   **Willful Infringement**: Up to **$150,000 per work infringed**.
*   **Attorney's Fees**: You pay the Licensor's legal bills (5.7).

## 6.4 Injunctive Relief (No Bond)
Most lawsuits require a "bond" to stop someone from doing business. This License forces you to waive that right. The Licensor can get a court order to **shut down your servers immediately** without putting up cash.

## 6.5 Jurisdiction and Venue
*   **Law**: State of **Alabama**.
*   **Venue**: Northern District of Alabama or Etowah County Courts.
*   **Arbitration**: **Solely at Licensor's Option** (JAMS). You cannot force arbitration; the Licensor can force you into it or drag you to court.

## 6.6 Article X: The "Nuclear" Enforcement
Article X includes explicitly non-severable, non-waivable enforcement logic.
*   **Immutability**: The Licensor cannot even *waive* Article X for you. It's designed to be legally "hard-coded."
*   **Clawback**: Proceeding against the **Estate and Trust** of an Excluded Individual. This means liability follows the money into family trusts.
