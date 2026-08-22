Autonomous Quantitative Logistics Intelligence Terminal

An institutional-grade Operations Research (OR) and Quantitative Decision Intelligence Terminal built to solve multi-echelon procurement allocation problems under capacity bounds, freight volatility, contractual Service Level Agreements (SLA), and Scope-3 ESG carbon constraints.

🔗 Live Interactive App: supply-chain-command-center.streamlit.app

📌 Executive Summary & Key Highlights

Traditional enterprise procurement often relies on naive sticker-price sorting or unoptimized status-quo equal-split sourcing. This terminal formulates procurement allocation as a Mixed-Integer Linear Program (MILP) and solves it in real time, capturing Capital Arbitrage and quantifying supply-chain tail risks.

Prescriptive MILP Solver Engine: Real-time rebalancing of sourcing allocations via the COIN-OR CBC solver (PuLP).

Dual Value Shadow Price Matrix: Calculates the exact marginal return (€/unit) of expanding capacity constraints ($\pi_j = \partial Z^* / \partial b_j$) for contract negotiations.

Stochastic Monte Carlo Risk Engine: 1,000-trial simulation calculating 95% Value-at-Risk ($\text{VaR}_{95}$) and Conditional Value-at-Risk ($\text{CVaR}_{95}$ / Expected Shortfall).

Multi-Objective ESG Pareto Frontier: Sweeps $\epsilon$-constraint thresholds to model the efficient tradeoff between procurement outlay and Scope-3 carbon footprints ($\text{t CO}_2\text{e}$).

Dynamic Topology Manipulation: Full CRUD capability via an interactive matrix allowing users to rename nodes, inject rate shocks, alter reliability floors, or add custom fulfillment hubs.

📐 Mathematical Formulation

1. Objective Function (Landed Cost Minimization)

$$\min Z = \sum_{i=1}^N x_i \cdot \left[ P_i + F_i + (1 - R_i) \cdot K_i \right]$$

Where:

$x_i$: Units allocated to sourcing node $i$ ($x_i \ge 0$)

$P_i$: Base unit purchase price (€)

$F_i$: Freight and logistics surcharge per unit (€)

$R_i$: Historical delivery reliability score ($0 \le R_i \le 1$)

$K_i$: Financial penalty fee per unfulfilled/delayed unit (€)

2. Network Constraints

Demand Balance: $\sum_{i=1}^N x_i = D$

Node Capacity Upper Bounds: $x_i \le C_i \quad \forall i$

Contractual SLA Reliability Floor: $\sum_{i=1}^N R_i x_i \ge \text{SLA}_{\text{target}} \cdot D$

Scope-3 Carbon Cap: $\sum_{i=1}^N \left(\frac{E_i}{1000}\right) x_i \le B_{\text{carbon}}$ (where $E_i$ is $\text{kg CO}_2\text{e}/\text{unit}$)

🛠️ Technology Stack

Core Language: Python 3.10+

Linear Programming Engine: PuLP (COIN-OR CBC Solver)

Stochastic & Matrix Analytics: NumPy, Pandas

Data Visualization: Plotly Graph Objects

Web Framework & UI: Streamlit

🚀 Local Installation & Setup

Clone the Repository:

git clone https://github.com/shuklasamyak1/supply-chain-command-center.git
cd supply-chain-command-center


Create a Virtual Environment (Optional but Recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:

pip install -r requirements.txt


Run the Application:

streamlit run app.py


📊 Module Walkthrough

1. Operational Dispatch Matrix

Visualizes allocated units vs. maximum node capacity side-by-side, alongside a stacked breakdown of unit landed cost components (Base Sticker + Freight + Disruption Risk Penalty).

2. Stochastic Monte Carlo & Tail-Risk

Runs 1,000 randomized disruption trials to map the risk distribution curve, identifying the 95th percentile Value-at-Risk ($\text{VaR}_{95}$) and tail expected shortfall ($\text{CVaR}_{95}$).

3. Multi-Objective ESG Pareto Frontier

Illustrates the non-dominated tradeoff curve between Total Cost (€) and Scope-3 Carbon Intensity ($\text{t CO}_2\text{e}$) under varying corporate emissions budgets.

4. Dual Shadow Price Engine

Exposes solver dual values ($\pi_j$) to highlight binding bottlenecks, providing procurement leads with numerical leverage during contract negotiations.

📜 License

Distributed under the MIT License. Built for quantitative portfolio demonstration and enterprise decision-intelligence benchmarking.