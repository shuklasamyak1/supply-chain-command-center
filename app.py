import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pulp

# Page Configuration
st.set_page_config(
    page_title="Autonomous Quantitative Logistics Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Typography & High-Density Terminal Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Space+Grotesk:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp {
        background-color: #050d0a;
        color: #ecfdf5;
    }

    section[data-testid="stSidebar"] {
        background-color: #081611 !important;
        border-right: 1px solid #133326;
    }
    
    section[data-testid="stSidebar"] * {
        color: #ecfdf5 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    div[data-testid="stMetricValue"] div {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 800 !important;
        color: #10b981 !important;
    }

    .terminal-header {
        background-color: #081611;
        border: 1px solid #133326;
        border-left: 4px solid #10b981;
        padding: 1.2rem 1.8rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
    }
    
    .terminal-title {
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: #f0fdf4;
        text-transform: uppercase;
    }

    .terminal-subtitle {
        font-size: 0.8rem;
        color: #6ee7b7;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 0.2rem;
    }

    div[data-testid="stMetric"] {
        background-color: #081611 !important;
        border: 1px solid #133326 !important;
        border-radius: 4px;
        padding: 1rem;
    }
    
    div[data-testid="stMetricLabel"] p {
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #a7f3d0 !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="terminal-header">
        <div class="terminal-title">QUANTITATIVE OPERATIONS RESEARCH & RISK TERMINAL</div>
        <div class="terminal-subtitle">ENGINE: MILP-CBC // STOCHASTIC MONTE CARLO VaR // MULTI-OBJECTIVE PARETO ESG OPTIMIZATION</div>
    </div>
""", unsafe_allow_html=True)

# Default Network Seed Data with Carbon Footprints
default_suppliers = pd.DataFrame([
    {"Node Name": "Hub DACH (Germany)", "Base Price (€)": 38.0, "Freight (€)": 2.5, "Reliability (%)": 98.0, "Max Capacity": 4500, "Risk Penalty (€)": 12.0, "Carbon (kg CO2e/unit)": 4.2},
    {"Node Name": "Hub CEE (Poland)", "Base Price (€)": 32.0, "Freight (€)": 4.5, "Reliability (%)": 92.0, "Max Capacity": 4500, "Risk Penalty (€)": 18.0, "Carbon (kg CO2e/unit)": 6.8},
    {"Node Name": "Hub APAC (East Asia)", "Base Price (€)": 26.0, "Freight (€)": 6.0, "Reliability (%)": 82.0, "Max Capacity": 5500, "Risk Penalty (€)": 24.0, "Carbon (kg CO2e/unit)": 14.5},
])

# Sidebar Controls
st.sidebar.markdown("#### **SYSTEM BOUNDS**")
target_demand = st.sidebar.number_input("Demand Target (Units)", min_value=1000, max_value=50000, value=10000, step=1000)
target_service_level = st.sidebar.slider("SLA Reliability Floor (%)", min_value=70, max_value=98, value=88, step=1) / 100.0

st.sidebar.markdown("---")
st.sidebar.markdown("#### **MULTI-OBJECTIVE & ESG BOUNDS**")
carbon_cap_enabled = st.sidebar.checkbox("Enforce Scope-3 Carbon Emissions Cap", value=False)
max_carbon_budget = st.sidebar.slider("Carbon Budget Cap (Metric Tons CO2e)", min_value=40.0, max_value=150.0, value=85.0, step=5.0)

st.sidebar.markdown("---")
st.sidebar.markdown("#### **STOCHASTIC STRESS TEST**")
global_freight_surcharge = st.sidebar.slider("Global Freight Surcharge (+€/unit)", min_value=0.0, max_value=20.0, value=0.0, step=0.5)

# Interactive Supplier Management Matrix
with st.expander("⚙️ CONFIGURE SOURCING TOPOLOGY & ESG PARAMETERS", expanded=False):
    st.caption("Live node manipulation: update rates, ESG footprints, or add custom fulfillment hubs.")
    edited_suppliers = st.data_editor(
        default_suppliers,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )

if edited_suppliers.empty or edited_suppliers["Node Name"].isnull().all():
    st.error("Network Topology Empty: Please define at least one supplier node.")
    st.stop()

# Convert edited grid into structured dictionary
suppliers = {}
for _, row in edited_suppliers.iterrows():
    if pd.notnull(row["Node Name"]) and str(row["Node Name"]).strip() != "":
        node_name = str(row["Node Name"]).strip()
        suppliers[node_name] = {
            "unit_cost": float(row["Base Price (€)"]),
            "freight_cost": float(row["Freight (€)"]) + global_freight_surcharge,
            "reliability": float(row["Reliability (%)"]) / 100.0,
            "capacity": int(row["Max Capacity"]),
            "risk_penalty": float(row["Risk Penalty (€)"]),
            "carbon": float(row["Carbon (kg CO2e/unit)"])
        }

# --- Mathematical Optimization (MILP) ---
model = pulp.LpProblem("Supply_Optimization", pulp.LpMinimize)

order_vars = {
    s: pulp.LpVariable(f"Order_{idx}", lowBound=0, cat="Continuous")
    for idx, (s, data) in enumerate(suppliers.items())
}

# 1. Objective Function: Landed Cost Minimization
total_cost_expr = []
for idx, (s, data) in enumerate(suppliers.items()):
    risk_charge = (1.0 - data["reliability"]) * data["risk_penalty"]
    landed_unit_cost = data["unit_cost"] + data["freight_cost"] + risk_charge
    total_cost_expr.append(order_vars[s] * landed_unit_cost)

model += pulp.lpSum(total_cost_expr)

# 2. Demand Satisfaction
model += pulp.lpSum([order_vars[s] for s in suppliers]) == target_demand, "Demand_Satisfaction"

# 3. Capacity Bounds
for s, data in suppliers.items():
    model += order_vars[s] <= data["capacity"], f"Capacity_{s.replace(' ', '_')}"

# 4. Service Level Floor
model += pulp.lpSum([order_vars[s] * data["reliability"] for s, data in suppliers.items()]) >= (target_service_level * target_demand), "Service_Level_Floor"

# 5. ESG Carbon Emission Constraint
if carbon_cap_enabled:
    model += pulp.lpSum([order_vars[s] * (data["carbon"] / 1000.0) for s, data in suppliers.items()]) <= max_carbon_budget, "Carbon_Emissions_Cap"

# Solve
model.solve(pulp.PULP_CBC_CMD(msg=False))
is_feasible = pulp.LpStatus[model.status] == "Optimal"

# Baseline Benchmark (Status-Quo Equal Split)
active_node_count = len(suppliers)
equal_share_per_node = target_demand / active_node_count if active_node_count > 0 else 0

naive_benchmark_cost = sum(
    equal_share_per_node * (d["unit_cost"] + d["freight_cost"] + ((1.0 - d["reliability"]) * d["risk_penalty"]))
    for d in suppliers.values()
)

# Results Matrix
results = []
total_carbon_tons = 0.0
for s, data in suppliers.items():
    qty = order_vars[s].varValue if is_feasible else 0.0
    risk_charge = (1.0 - data["reliability"]) * data["risk_penalty"]
    landed_unit_cost = data["unit_cost"] + data["freight_cost"] + risk_charge
    node_carbon = (qty * data["carbon"]) / 1000.0
    total_carbon_tons += node_carbon
    
    results.append({
        "Sourcing Node": s,
        "Max Capacity": data["capacity"],
        "Base Cost (€)": data["unit_cost"],
        "Freight (€)": round(data["freight_cost"], 2),
        "Reliability (%)": f"{int(data['reliability'] * 100)}%",
        "True Landed (€)": round(landed_unit_cost, 2),
        "Allocated Units": round(qty, 0),
        "Carbon Footprint (t)": round(node_carbon, 2),
        "Total Outlay (€)": round(qty * landed_unit_cost, 2)
    })

df_results = pd.DataFrame(results)
total_optimal_spend = pulp.value(model.objective) if is_feasible else 0.0
loss_avoidance = max(0.0, naive_benchmark_cost - total_optimal_spend)

if is_feasible and target_demand > 0:
    achieved_sl = sum(row["Allocated Units"] * suppliers[row["Sourcing Node"]]["reliability"] for _, row in df_results.iterrows()) / target_demand
else:
    achieved_sl = 0.0

# Extract Dual Shadow Prices
shadow_prices = []
if is_feasible:
    for name, constraint in model.constraints.items():
        if "Capacity" in name or "Carbon" in name or "Service" in name:
            clean_node = name.replace("Capacity_", "").replace("_", " ")
            shadow_val = constraint.pi if constraint.pi is not None else 0.0
            shadow_prices.append({
                "Constrained Frontier": clean_node,
                "Marginal Shadow Value (€/unit)": abs(round(shadow_val, 2)),
                "Strategic Interpretation": "Active Bottleneck (Marginal Relaxation ROI)" if abs(shadow_val) > 0 else "Slack Boundary (Non-Binding)"
            })

df_shadow = pd.DataFrame(shadow_prices)

# --- Monte Carlo 1,000 Trial Tail-Risk Simulation ---
np.random.seed(42)
if is_feasible and total_optimal_spend > 0:
    sim_iterations = 1000
    sim_costs = np.zeros(sim_iterations)
    
    for i in range(sim_iterations):
        iter_cost = 0.0
        for s, data in suppliers.items():
            qty = order_vars[s].varValue
            if qty > 0:
                is_disrupted = np.random.binomial(1, 1.0 - data["reliability"])
                freight_jitter = np.random.normal(0, data["freight_cost"] * 0.15)
                unit_run_cost = data["unit_cost"] + max(0, data["freight_cost"] + freight_jitter) + (is_disrupted * data["risk_penalty"])
                iter_cost += qty * unit_run_cost
        sim_costs[i] = iter_cost
    
    var_95 = np.percentile(sim_costs, 95)
    cvar_95 = sim_costs[sim_costs >= var_95].mean()
else:
    var_95, cvar_95, sim_costs = 0.0, 0.0, np.zeros(10)

# KPI Row
k1, k2, k3, k4 = st.columns(4)
k1.metric("OPTIMIZED NETWORK SPEND", f"€{total_optimal_spend:,.2f}" if is_feasible else "€0.00")
k2.metric("CAPITAL ARBITRAGE", f"€{loss_avoidance:,.2f}" if is_feasible else "€0.00", delta=f"{(loss_avoidance / naive_benchmark_cost) * 100:.1f}% vs Status Quo" if is_feasible and naive_benchmark_cost > 0 else None)
k3.metric("PARAMETRIC VaR (95%)", f"€{var_95:,.2f}" if is_feasible else "€0.00", delta=f"+€{max(0, var_95 - total_optimal_spend):,.0f} Tail Risk")
k4.metric("TOTAL CARBON FOOTPRINT", f"{total_carbon_tons:.1f} t CO2e" if is_feasible else "0.0 t", delta="Under ESG Cap" if not carbon_cap_enabled or total_carbon_tons <= max_carbon_budget else "CAP BREACHED")

if not is_feasible:
    st.error("Constraint Violation: Model infeasible under current capacity, SLA reliability, or ESG carbon budget.")

st.markdown("---")

# Analytics Tabs
tab_dispatch, tab_monte_carlo, tab_pareto, tab_shadow = st.tabs([
    "Operational Dispatch Matrix", 
    "Stochastic Monte Carlo & Tail Risk", 
    "Multi-Objective ESG Pareto Frontier", 
    "Dual Shadow Price Engine"
])

with tab_dispatch:
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("#### **NODE CAPACITY VS. DISPATCHED ALLOCATION**")
        fig_util = go.Figure()
        fig_util.add_trace(go.Bar(name="Max Node Capacity", x=df_results["Sourcing Node"], y=df_results["Max Capacity"], marker=dict(color='#133326', line=dict(color='#10b981', width=1))))
        fig_util.add_trace(go.Bar(name="Allocated Units", x=df_results["Sourcing Node"], y=df_results["Allocated Units"], marker=dict(color='#10b981')))
        fig_util.update_layout(barmode='group', template="plotly_dark", paper_bgcolor="#050d0a", plot_bgcolor="#081611", font=dict(family="JetBrains Mono", color="#ecfdf5"), height=320, margin=dict(l=10, r=10, t=10, b=10), yaxis=dict(gridcolor="#133326"), legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        st.plotly_chart(fig_util, use_container_width=True)

    with col_right:
        st.markdown("#### **SCOPE-3 CARBON INTENSITY SHARE (METRIC TONS)**")
        fig_carb = go.Figure(data=[go.Pie(labels=df_results["Sourcing Node"], values=df_results["Carbon Footprint (t)"], hole=0.55, marker=dict(colors=['#10b981', '#047857', '#064e3b']))])
        fig_carb.update_layout(template="plotly_dark", paper_bgcolor="#050d0a", font=dict(family="JetBrains Mono", color="#ecfdf5"), height=320, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        st.plotly_chart(fig_carb, use_container_width=True)

    st.markdown("#### **AUDIT DISPATCH LEDGER**")
    st.dataframe(df_results, use_container_width=True, hide_index=True)

with tab_monte_carlo:
    st.markdown("#### **1,000-ITERATION STOCHASTIC TAIL-RISK DISTRIBUTION**")
    fig_mc = go.Figure()
    fig_mc.add_trace(go.Histogram(x=sim_costs, nbinsx=40, name="Simulated Total Cost", marker_color='#047857', opacity=0.85))
    fig_mc.add_vline(x=total_optimal_spend, line_width=2, line_dash="dash", line_color="#10b981", annotation_text="Expected Baseline")
    fig_mc.add_vline(x=var_95, line_width=2, line_dash="dash", line_color="#f59e0b", annotation_text="95% VaR Threshold")
    fig_mc.add_vline(x=cvar_95, line_width=2, line_dash="dash", line_color="#ef4444", annotation_text="Conditional VaR (Expected Shortfall)")
    fig_mc.update_layout(template="plotly_dark", paper_bgcolor="#050d0a", plot_bgcolor="#081611", font=dict(family="JetBrains Mono", color="#ecfdf5"), height=340, margin=dict(l=10, r=10, t=20, b=10), xaxis=dict(gridcolor="#133326", title="Total Procurement Outlay (€)"), yaxis=dict(gridcolor="#133326", title="Frequency"))
    st.plotly_chart(fig_mc, use_container_width=True)
    st.info(f"**Quant Risk Metrics:** 95% Parametric Value-at-Risk is **€{var_95:,.2f}**. In the worst 5% of disruption shocks, the Conditional VaR (Expected Shortfall) averages **€{cvar_95:,.2f}**.")

with tab_pareto:
    st.markdown("#### **MULTI-OBJECTIVE PARETO FRONTIER: COST VS. DECARBONIZATION**")
    st.caption("Demonstrates the Efficient Frontier tradeoff: Lowering Carbon Intensity forces higher unit procurement spend.")
    
    # Compute Pareto Curve across 10 discrete emission steps
    pareto_points = []
    for carb_target in np.linspace(50.0, 130.0, 10):
        p_model = pulp.LpProblem("Pareto", pulp.LpMinimize)
        p_vars = {s: pulp.LpVariable(f"POrder_{i}", lowBound=0, upBound=d["capacity"]) for i, (s, d) in enumerate(suppliers.items())}
        p_model += pulp.lpSum([p_vars[s] * (d["unit_cost"] + d["freight_cost"] + (1.0 - d["reliability"]) * d["risk_penalty"]) for s, d in suppliers.items()])
        p_model += pulp.lpSum([p_vars[s] for s in suppliers]) == target_demand
        p_model += pulp.lpSum([p_vars[s] * d["reliability"] for s, d in suppliers.items()]) >= (target_service_level * target_demand)
        p_model += pulp.lpSum([p_vars[s] * (d["carbon"] / 1000.0) for s, d in suppliers.items()]) <= carb_target
        p_model.solve(pulp.PULP_CBC_CMD(msg=False))
        if pulp.LpStatus[p_model.status] == "Optimal":
            pareto_points.append({"Carbon Cap (t CO2e)": carb_target, "Min Landed Cost (€)": pulp.value(p_model.objective)})

    df_pareto = pd.DataFrame(pareto_points)
    if not df_pareto.empty:
        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Scatter(x=df_pareto["Carbon Cap (t CO2e)"], y=df_pareto["Min Landed Cost (€)"], mode='lines+markers', line=dict(color='#10b981', width=3), marker=dict(size=8, color='#f59e0b')))
        fig_pareto.update_layout(template="plotly_dark", paper_bgcolor="#050d0a", plot_bgcolor="#081611", font=dict(family="JetBrains Mono", color="#ecfdf5"), height=340, margin=dict(l=10, r=10, t=10, b=10), xaxis=dict(gridcolor="#133326", title="Permitted Carbon Cap (Tons CO2e)"), yaxis=dict(gridcolor="#133326", title="Optimized Cost (€)"))
        st.plotly_chart(fig_pareto, use_container_width=True)

with tab_shadow:
    st.markdown("#### **DUAL SHADOW VALUE SENSITIVITY MATRIX**")
    st.dataframe(df_shadow, use_container_width=True, hide_index=True)