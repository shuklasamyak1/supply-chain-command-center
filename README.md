# ⚡ Autonomous Multi-Tier Sourcing & Disruption Solver

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://supply-chain-command-center-pgzcwfma9cbbey4zo2zkyj.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

An enterprise-grade Prescriptive Operations Research platform formulating a continuous linear optimization model to autonomously compute optimal purchase order allocations across global multi-tier supplier hubs. Integrates contractual SLA floors, Scope-3 carbon ceilings, 1,000-trial empirical Monte Carlo tail-risk simulations ($\text{VaR}_{95} / \text{CVaR}_{95}$), and continuous LP relaxation dual shadow price microeconomics.

---

## 🎬 System Overview & Live Walkthrough

### Executive Terminal & Decision Engine Demo
https://github.com/user-attachments/assets/Dashboard_Preview.mp4

> **Prescriptive Decision Directives:** Converts raw optimization solution vectors into clear executive procurement mandates (`Priority: Max Allocation`, `Balancing Node`, or `Avoid / Bypassed`) alongside binding bottleneck shadow values ($\pi_i$).

---

## 📸 Platform Previews

### 1. Executive Cockpit & Prescriptive Directives
![Executive Cockpit](Preview.png)

### 2. Sourcing Matrix & Scope-3 ESG Allocations
![Sourcing Matrix](Preview1.png)

### 3. Stochastic Monte Carlo Disruption Engine ($\text{VaR}_{95} / \text{CVaR}_{95}$)
![Monte Carlo Risk](Preview2.png)

---

## 📌 Executive Architecture & Problem Framing

Traditional supply chain planning relies on descriptive dashboards or heuristic rules of thumb (e.g., naive equal splits) that fail to capture the trade-offs between landed unit cost, stochastic disruption penalties, supplier capacities, and sustainability caps.

This system combines:
1. **Continuous Linear Optimization (PuLP / CBC Solver):** Global landed cost minimization under strict multi-dimensional constraints.
2. **Prescriptive Action Layer:** Translates raw LP simplex outputs into direct supplier order mandates.
3. **LP Relaxation Dual Shadow Pricing ($\pi_i$):** Quantifies marginal economic sensitivity, evaluating bottleneck expansion ROI and marginal carbon abatement costs under complementary slackness.
4. **Stochastic Stress Testing (1,000 Monte Carlo Trials):** Simulates disruption distributions without restrictive normality assumptions to compute empirical Value-at-Risk ($\text{VaR}_{95}$) and Conditional Value-at-Risk ($\text{CVaR}_{95}$).
5. **Multi-Objective ESG Pareto Frontier:** Computes the marginal abatement cost curve across stepped carbon caps via the $\epsilon$-constraint method.

---

## 🧮 Mathematical Formulation

### 1. Objective Function (Total Landed Spend Minimization)
$$\min_{\mathbf{x}} \sum_{i=1}^{N} x_i \cdot \left[ C_{\text{base}, i} + C_{\text{freight}, i} + (1 - R_i) \cdot P_i \right]$$

Where:
* $x_i \ge 0$: Continuous volume allocated to supplier hub $i$.
* $C_{\text{base}, i}$: Unit base purchase price.
* $C_{\text{freight}, i}$: Unit freight surcharge (including global macroeconomic shock adders).
* $R_i \in [0, 1]$: Historical fulfillment reliability rate.
* $P_i$: Emergency defect/delay recovery penalty per unit.
* $(1 - R_i) \cdot P_i$: Expected disruption risk charge per unit.

### 2. Operational & Environmental Constraints

* **Demand Equilibrium:**
  $$\sum_{i=1}^{N} x_i = D$$
* **Plant Capacity Upper Bounds:**
  $$0 \le x_i \le K_i \quad \forall i \in \{1, \dots, N\}$$
* **Contractual SLA Reliability Floor:**
  $$\frac{\sum_{i=1}^{N} x_i \cdot R_i}{D} \ge \alpha_{\text{SLA}}$$
* **Scope-3 Carbon Emissions Budget:**
  $$\sum_{i=1}^{N} x_i \cdot \left(\frac{E_i}{1000}\right) \le B_{\text{CO}_2}$$

### 3. Dual Shadow Pricing & Sensitivity Microeconomics
Dual variables ($\pi_i = \frac{\partial \mathcal{L}^*}{\partial b_i}$) are extracted directly from the solved simplex:
* **Demand Shadow Price ($\pi_{\text{demand}}$):** Marginal cost of fulfilling $+1$ additional unit of customer demand.
* **Contractual SLA Shadow Price ($\pi_{\text{sla}}$):** Marginal penalty paid per unit increment in network reliability requirements. Adheres to complementary slackness: if the SLA constraint has positive slack (non-binding), $\pi_{\text{sla}} \equiv 0.00$.
* **Scope-3 Carbon Shadow Price ($\pi_{\text{carbon}}$):** Quantifies marginal economic abatement cost. Tightening the carbon cap by $1\text{ t}$ restricts the feasible region, increasing optimal landed procurement cost by $\vert{}\pi_{\text{carbon}}\vert{}$.

### 4. Empirical Stochastic Tail Risk (Monte Carlo Simulation)
Rather than assuming an idealized parametric normal distribution over portfolio losses, the engine runs $1,000$ stochastic iterations coupling Bernoulli supplier failure shocks with Gaussian freight rate volatility:
$$S_i \sim \text{Bernoulli}(1 - R_i)$$
$$\tilde{C}_{\text{freight}, i} \sim \mathcal{N}\left(C_{\text{freight}, i}, \, (0.15 \cdot C_{\text{freight}, i})^2\right)$$

* **Monte Carlo Value-at-Risk ($\text{VaR}_{95}$):** The 95th percentile worst-case empirical loss threshold across the simulated scenario array.
* **Conditional Value-at-Risk ($\text{CVaR}_{95}$ / Expected Shortfall):** The expectation of tail losses exceeding $\text{VaR}_{95}$:
  $$\text{CVaR}_{95} = \mathbb{E}\left[ L \mid L \ge \text{VaR}_{95} \right]$$

---

## 🚀 Key Modules

| Module | Engine | Description |
| :--- | :--- | :--- |
| **Prescriptive Directives** | Simplex State Classifier | Classifies nodes into `Priority: Max Allocation (100%)`, `Balancing Node (Partial)`, or `Avoid / Bypassed (0%)` to eliminate human ordering bias. |
| **LP Shadow Prices** | Continuous Simplex Duals ($\pi_i$) | Identifies binding bottlenecks and calculates marginal cost sensitivity per unit of capacity expansion or constraint variation. |
| **Monte Carlo Tail Risk** | Empirical Stochastic Engine (1,000 Trials) | Simulates joint supplier failures and freight volatility to compute empirical $\text{VaR}_{95}$ and $\text{CVaR}_{95}$ without restrictive distribution assumptions. |
| **ESG Pareto Frontier** | $\epsilon$-Constraint Method | Solves across 15 stepped carbon ceilings to map the exact trade-off curve between procurement spend and carbon emissions. |

---

## 🛠️ Tech Stack

* **Mathematical Optimization:** `PuLP` (COIN-OR CBC Solver)
* **Statistical Simulation:** `NumPy`
* **Data Transformation & Querying:** `Pandas`
* **Interactive Visualization:** `Plotly Graph Objects`, `Plotly Express`
* **Application Framework & Deployment:** `Streamlit Cloud`

---

## 📦 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shuklasamyak1/supply-chain-command-center.git](https://github.com/shuklasamyak1/supply-chain-command-center.git)
   cd supply-chain-command-center
