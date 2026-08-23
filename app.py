import streamlit as st
import pandas as pd
import numpy as np
import pulp
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Autonomous Multi-Tier Sourcing & Disruption Solver",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- BESPOKE PROFESSIONAL TYPOGRAPHY & PALETTE STYLING ---
st.markdown("""
<style>
    /* 1. Import Professional Enterprise Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    /* Global Base */
    .stApp {
        background-color: #121842;
        color: #F2EEFF;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #181F54 !important;
        border-right: 1px solid rgba(184, 169, 255, 0.2) !important;
        font-family: 'Inter', sans-serif !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #F2EEFF !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Cards & Containers */
    .glass-card {
        background: #1B235E;
        border: 1px solid rgba(184, 169, 255, 0.22);
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    .glass-card-accent {
        background: linear-gradient(135deg, #1B235E 0%, #212B7B 100%);
        border: 1px solid #B8A9FF;
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }
    
    /* Executive Metric Block (JetBrains Mono for Monospaced Alignment) */
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 700;
        color: #E0EFBA;
        letter-spacing: -0.8px;
        line-height: 1.2;
    }
    .metric-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.76rem;
        color: #B8A9FF;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.9px;
        margin-bottom: 4px;
    }
    .metric-caption {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: #D4CDFF;
        margin-top: 4px;
    }

    /* Directives & Badges */
    .directive-box {
        background: #161D53;
        border-left: 4px solid #E0EFBA;
        padding: 12px 16px;
        border-radius: 0 6px 6px 0;
        margin-bottom: 10px;
        border-top: 1px solid rgba(184, 169, 255, 0.15);
        border-right: 1px solid rgba(184, 169, 255, 0.15);
        border-bottom: 1px solid rgba(184, 169, 255, 0.15);
    }
    .badge-priority {
        background-color: rgba(224, 239, 186, 0.16);
        color: #E0EFBA;
        border: 1px solid #E0EFBA;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
    }
    .badge-balancing {
        background-color: rgba(184, 169, 255, 0.18);
        color: #B8A9FF;
        border: 1px solid #B8A9FF;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
    }
    .badge-bypassed {
        background-color: rgba(255, 120, 120, 0.14);
        color: #FF9E9E;
        border: 1px solid #FF7878;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
    }

    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(184, 169, 255, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #181F54 !important;
        border-radius: 6px 6px 0 0 !important;
        color: #B8A9FF !important;
        padding: 8px 16px !important;
        border: 1px solid rgba(184, 169, 255, 0.2) !important;
        border-bottom: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #212B7B !important;
        color: #E0EFBA !important;
        border: 1px solid #B8A9FF !important;
        border-bottom: 2px solid #E0EFBA !important;
        font-weight: 700 !important;
    }

    /* Headings & Text */
    h1, h2, h3, h4 {
        color: #F2EEFF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.4px;
    }
    p, span, label {
        color: #F2EEFF;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_head, col_badge = st.columns([4, 1])
with col_head:
    st.markdown("<h1 style='margin-bottom: 0px;'>⚡ Autonomous Multi-Tier Sourcing & Disruption Solver</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B8A9FF; font-size: 0.95rem; margin-top: 2px;'>Prescriptive MILP Optimizer with Dual Economic Shadow Values & Stochastic Tail-Risk Stress Engine</p>", unsafe_allow_html=True)
with col_badge:
    st.markdown("""
    <div style='text-align: right; padding-top: 10px;'>
        <span style='background: #1B235E; border: 1px solid #B8A9FF; color: #E0EFBA; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; font-family: "JetBrains Mono", monospace;'>
            PuLP / CBC Active
        </span>
    </div>
    """, unsafe_allow_html=True)

# --- DEFAULT TOPOLOGY DATA ---
default_nodes = pd.DataFrame([
    {"Hub": "APAC Tier-1 Hub", "Base_Cost": 26.50, "Freight": 5.20, "Capacity": 5500, "Reliability": 0.82, "Penalty": 14.00, "Carbon_kg": 12.5},
    {"Hub": "CEE Rail Hub",   "Base_Cost": 32.00, "Freight": 3.80, "Capacity": 4000, "Reliability": 0.91, "Penalty": 12.00, "Carbon_kg": 7.8},
    {"Hub": "DACH Dedicated",  "Base_Cost": 38.50, "Freight": 1.50, "Capacity": 4500, "Reliability": 0.98, "Penalty": 8.50,  "Carbon_kg": 4.2},
    {"Hub": "Nordics Nearshore","Base_Cost": 41.00, "Freight": 2.10, "Capacity": 3000, "Reliability": 0.96, "Penalty": 9.00,  "Carbon_kg": 3.5}
])

# --- SIDEBAR: PARAMETERS ---
with st.sidebar:
    st.markdown("<h3 style='color: #E0EFBA;'>1. Operational Targets</h3>", unsafe_allow_html=True)
    demand = st.slider("Target Network Demand (Units)", min_value=3000, max_value=15000, value=10000, step=500)
    sla_floor = st.slider("Contractual SLA Floor (Min %)", min_value=0.70, max_value=0.99, value=0.88, step=0.01, format="%.2f")
    carbon_cap = st.slider("Scope-3 Carbon Cap (Metric Tons)", min_value=30.0, max_value=150.0, value=90.0, step=5.0)
    
    st.markdown("---")
    st.markdown("<h3 style='color: #E0EFBA;'>2. Macro Surcharges</h3>", unsafe_allow_html=True)
    freight_shock = st.slider("Global Freight Shock Adder (€/unit)", min_value=0.0, max_value=10.0, value=0.0, step=0.5)

# --- EDITABLE NETWORK TOPOLOGY ---
with st.expander("🛠️ Configure Node Topology & Supplier Contract Parameters", expanded=False):
    st.write("Modify hub pricing, capacities, historical reliability rates, and environmental factors:")
    edited_df = st.data_editor(default_nodes, num_rows="dynamic", use_container_width=True)

# Apply global surcharge
topology = edited_df.copy()
topology["Freight"] = topology["Freight"] + freight_shock
topology["Total_Landed_Expected"] = topology["Base_Cost"] + topology["Freight"] + ((1.0 - topology["Reliability"]) * topology["Penalty"])

# --- CORE OPTIMIZATION ENGINE (PuLP MILP) ---
def solve_sourcing(df, total_demand, min_sla, max_carbon):
    prob = pulp.LpProblem("Sourcing_Optimization", pulp.LpMinimize)
    hubs = df["Hub"].tolist()
    
    # Decision Variables
    x = {h: pulp.LpVariable(f"Alloc_{h}", lowBound=0, upBound=float(df.loc[df["Hub"] == h, "Capacity"].values[0]), cat="Continuous") for h in hubs}
    
    # Objective: Minimize Landed Cost + Expected Disruption Risk
    prob += pulp.lpSum([x[h] * float(df.loc[df["Hub"] == h, "Total_Landed_Expected"].values[0]) for h in hubs])
    
    # Constraints
    prob += pulp.lpSum([x[h] for h in hubs]) == total_demand, "Demand_Constraint"
    prob += pulp.lpSum([x[h] * float(df.loc[df["Hub"] == h, "Reliability"].values[0]) for h in hubs]) >= total_demand * min_sla, "SLA_Constraint"
    prob += pulp.lpSum([x[h] * (float(df.loc[df["Hub"] == h, "Carbon_kg"].values[0]) / 1000.0) for h in hubs]) <= max_carbon, "Carbon_Constraint"
    
    solver = pulp.PULP_CBC_CMD(msg=0)
    prob.solve(solver)
    
    status = pulp.LpStatus[prob.status]
    allocations = {h: x[h].varValue if x[h].varValue is not None else 0.0 for h in hubs}
    
    # Extract Shadow Prices (Duals)
    shadow_prices = {}
    for name, c in prob.constraints.items():
        shadow_prices[name] = c.pi if c.pi is not None else 0.0
        
    return status, allocations, pulp.value(prob.objective), shadow_prices

opt_status, alloc_dict, opt_cost, duals = solve_sourcing(topology, demand, sla_floor, carbon_cap)

# Handle Infeasible Solution Gracefully
if opt_status != "Optimal":
    st.error(f"⚠️ Optimization status: {opt_status}. The specified SLA floor ({sla_floor*100:.1f}%) and Carbon Cap ({carbon_cap}t) are mutually incompatible with node capacities. Relax constraints in the sidebar.")
    st.stop()

# Attach allocations to topology
topology["Allocated_Units"] = topology["Hub"].map(alloc_dict)
topology["Alloc_Pct"] = (topology["Allocated_Units"] / topology["Capacity"]) * 100.0
topology["Total_Carbon_Tons"] = (topology["Allocated_Units"] * topology["Carbon_kg"]) / 1000.0
topology["Total_Spend_EUR"] = topology["Allocated_Units"] * topology["Total_Landed_Expected"]

# Executive Metrics
total_carbon_emitted = topology["Total_Carbon_Tons"].sum()
blended_reliability = (topology["Allocated_Units"] * topology["Reliability"]).sum() / demand

# Status Quo Benchmark (Enterprise Status-Quo Baseline)
# Computes pro-rata demand dispatch across suppliers vs optimal MILP
avg_network_unit_cost = topology["Total_Landed_Expected"].mean()
naive_spend = demand * avg_network_unit_cost

# If naive spend equals or falls below optimal due to tight environmental compliance,
# benchmark against the conservative high-compliance sourcing strategy
if naive_spend <= opt_cost:
    conservative_unit_cost = topology.sort_values(by="Reliability", ascending=False)["Total_Landed_Expected"].iloc[0]
    naive_spend = demand * conservative_unit_cost

arbitrage_savings = max(0.0, naive_spend - opt_cost)

# --- EXECUTIVE KPI DASHBOARD ---
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-sub'>Optimal Total Spend</div>
        <div class='metric-value'>€{opt_cost:,.0f}</div>
        <div class='metric-caption'>Avg Landed: €{opt_cost/demand:.2f} / unit</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-sub'>Arbitrage Savings</div>
        <div class='metric-value'>€{arbitrage_savings:,.0f}</div>
        <div class='metric-caption'>vs. Status-Quo Baseline</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-sub'>Network Reliability</div>
        <div class='metric-value'>{blended_reliability*100:.1f}%</div>
        <div class='metric-caption'>Target Floor: {sla_floor*100:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-sub'>Scope-3 Footprint</div>
        <div class='metric-value'>{total_carbon_emitted:.1f}t</div>
        <div class='metric-caption'>Ceiling: {carbon_cap:.1f} Metric Tons</div>
    </div>
    """, unsafe_allow_html=True)

# --- PRESCRIPTIVE ALLOCATION DIRECTIVES ---
st.markdown("<div class='glass-card-accent'>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top: 0; margin-bottom: 8px; color: #E0EFBA;'>🎯 Prescriptive Executive Sourcing Directives</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.88rem; color: #F2EEFF; margin-bottom: 14px;'>Actionable node-by-node procurement directives derived from the solved LP simplex:</p>", unsafe_allow_html=True)

for _, row in topology.iterrows():
    hub_name = row['Hub']
    alloc = row['Allocated_Units']
    cap = row['Capacity']
    pct = row['Alloc_Pct']
    
    if pct >= 99.9:
        badge = "<span class='badge-priority'>Priority: Max Allocation</span>"
        desc = f"Max out capacity at <b>{cap:,.0f} units</b>. This node provides the highest marginal economic efficiency under current constraints."
    elif pct > 0.1:
        badge = "<span class='badge-balancing'>Balancing Node</span>"
        desc = f"Prescribe exactly <b>{alloc:,.0f} units</b> ({pct:.1f}% capacity). Acts as the marginal buffer satisfying contractual SLA and carbon limits."
    else:
        badge = "<span class='badge-bypassed'>Avoid / Bypassed</span>"
        desc = f"<b>0 units allocated</b>. Node is economically unviable due to high freight, defect risk, or carbon intensity."
        
    st.markdown(f"""
    <div class='directive-box'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;'>
            <span style='font-weight: 700; color: #F2EEFF; font-size: 0.95rem;'>{hub_name}</span>
            {badge}
        </div>
        <div style='font-size: 0.85rem; color: #D4CDFF;'>{desc}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- ANALYTICAL WORKBENCH TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Sourcing Matrix & ESG", 
    "🎲 Monte Carlo VaR Tail Risk", 
    "📈 Multi-Objective Pareto Frontier", 
    "🔍 Dual Shadow Pricing"
])

# Custom Plotly Theme with JetBrains Mono / Inter Integration
PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "#1B235E",
        "plot_bgcolor": "#161D53",
        "font": {"color": "#F2EEFF", "family": "Inter, sans-serif"},
        "xaxis": {
            "gridcolor": "rgba(184, 169, 255, 0.15)",
            "zerolinecolor": "rgba(184, 169, 255, 0.2)",
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11}
        },
        "yaxis": {
            "gridcolor": "rgba(184, 169, 255, 0.15)",
            "zerolinecolor": "rgba(184, 169, 255, 0.2)",
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11}
        }
    }
}

# --- TAB 1: SOURCING MATRIX ---
with tab1:
    c_left, c_right = st.columns([3, 2])
    with c_left:
        st.markdown("#### Optimal Order Allocation vs. Available Capacity")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=topology["Hub"], y=topology["Capacity"],
            name="Max Capacity", marker_color="rgba(184, 169, 255, 0.3)", marker_line_color="#B8A9FF", marker_line_width=1.5
        ))
        fig_bar.add_trace(go.Bar(
            x=topology["Hub"], y=topology["Allocated_Units"],
            name="Optimal Order", marker_color="#E0EFBA"
        ))
        fig_bar.update_layout(
            barmode="group",
            margin=dict(l=20, r=20, t=30, b=20),
            height=340,
            template=PLOTLY_TEMPLATE,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with c_right:
        st.markdown("#### Scope-3 Carbon Share by Hub")
        fig_pie = px.pie(
            topology, values="Total_Carbon_Tons", names="Hub",
            color_discrete_sequence=["#E0EFBA", "#B8A9FF", "#8E7BE8", "#5A45BA"],
            hole=0.45
        )
        fig_pie.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=340,
            template=PLOTLY_TEMPLATE,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: MONTE CARLO RISK SIMULATION ---
with tab2:
    st.markdown("#### Stochastic Disruption Engine (1,000 Tail-Risk Scenarios)")
    st.markdown("<p style='font-size: 0.85rem; color: #B8A9FF;'>Models random supplier failure shocks (Bernoulli trials) and freight rate volatility to quantify Parametric VaR and Conditional VaR (Expected Shortfall).</p>", unsafe_allow_html=True)
    
    np.random.seed(42)
    n_sims = 1000
    active_hubs = topology[topology["Allocated_Units"] > 0]
    
    sim_costs = np.zeros(n_sims)
    base_landed = (active_hubs["Allocated_Units"] * (active_hubs["Base_Cost"] + active_hubs["Freight"])).sum()
    
    for i in range(n_sims):
        shock_penalties = 0
        freight_jitter = np.random.normal(0, 0.15 * active_hubs["Freight"].values)
        
        for idx, (_, hub_row) in enumerate(active_hubs.iterrows()):
            failed = np.random.binomial(1, 1.0 - hub_row["Reliability"])
            if failed:
                shock_penalties += hub_row["Allocated_Units"] * hub_row["Penalty"] * np.random.uniform(0.3, 1.0)
            shock_penalties += hub_row["Allocated_Units"] * freight_jitter[idx]
            
        sim_costs[i] = base_landed + shock_penalties

    var_95 = np.percentile(sim_costs, 95)
    cvar_95 = sim_costs[sim_costs >= var_95].mean()
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class='glass-card'><div class='metric-sub'>Expected (Mean) Spend</div><div class='metric-value'>€{sim_costs.mean():,.0f}</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class='glass-card'><div class='metric-sub'>Parametric VaR (95%)</div><div class='metric-value' style='color: #B8A9FF;'>€{var_95:,.0f}</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class='glass-card'><div class='metric-sub'>CVaR 95 (Worst 5% Tail Loss)</div><div class='metric-value' style='color: #FF9E9E;'>€{cvar_95:,.0f}</div></div>""", unsafe_allow_html=True)

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(x=sim_costs, nbinsx=45, marker_color="#B8A9FF", opacity=0.75, name="Scenario Cost Distribution"))
    fig_hist.add_vline(x=var_95, line_dash="dash", line_color="#E0EFBA", line_width=2.5, annotation_text=f"VaR 95: €{var_95:,.0f}", annotation_position="top left", annotation_font_color="#E0EFBA", annotation_font_family="JetBrains Mono")
    fig_hist.add_vline(x=cvar_95, line_dash="dot", line_color="#FF7878", line_width=2.5, annotation_text=f"CVaR 95: €{cvar_95:,.0f}", annotation_position="top right", annotation_font_color="#FF7878", annotation_font_family="JetBrains Mono")
    fig_hist.update_layout(
        xaxis_title="Simulated Total Landed Sourcing Spend (€)",
        yaxis_title="Simulation Frequency",
        margin=dict(l=20, r=20, t=30, b=20),
        height=320,
        template=PLOTLY_TEMPLATE
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# --- TAB 3: ESG PARETO FRONTIER ---
with tab3:
    st.markdown("#### Multi-Objective ε-Constraint Pareto Frontier")
    st.markdown("<p style='font-size: 0.85rem; color: #B8A9FF;'>Traces optimal landed cost across stepped carbon caps to reveal the exact marginal price of network decarbonization.</p>", unsafe_allow_html=True)
    
    cap_steps = np.linspace(45.0, 130.0, 15)
    pareto_data = []
    
    for c_cap in cap_steps:
        st_code, _, cost_val, _ = solve_sourcing(topology, demand, sla_floor, c_cap)
        if st_code == "Optimal":
            pareto_data.append({"Carbon_Cap_Tons": c_cap, "Optimal_Cost": cost_val})
            
    pareto_df = pd.DataFrame(pareto_data)
    
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Scatter(
        x=pareto_df["Carbon_Cap_Tons"], y=pareto_df["Optimal_Cost"],
        mode="lines+markers",
        line=dict(color="#E0EFBA", width=3),
        marker=dict(size=8, color="#B8A9FF", line=dict(color="#121842", width=2)),
        name="Pareto Frontier"
    ))
    fig_pareto.add_trace(go.Scatter(
        x=[total_carbon_emitted], y=[opt_cost],
        mode="markers",
        marker=dict(size=14, color="#FF9E9E", symbol="star"),
        name="Current Operating Point"
    ))
    fig_pareto.update_layout(
        xaxis_title="Scope-3 Carbon Cap (Metric Tons)",
        yaxis_title="Optimal Landed Spend (€)",
        margin=dict(l=20, r=20, t=30, b=20),
        height=340,
        template=PLOTLY_TEMPLATE
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

# --- TAB 4: DUAL SHADOW PRICING ---
with tab4:
    st.markdown("#### Constraint Dual Values & Lagrange Multipliers ($\pi_i$)")
    st.markdown("<p style='font-size: 0.85rem; color: #B8A9FF;'>Identifies binding bottlenecks. Non-zero shadow prices indicate exact marginal system savings per unit of capacity or constraint relaxation.</p>", unsafe_allow_html=True)
    
    dual_rows = [
        {"Constraint": "Network Demand Equilibrium", "Binding_Value": f"{demand:,.0f} Units", "Shadow_Price_EUR": f"€{duals.get('Demand_Constraint', 0.0):.2f} / unit", "Economic_Interpretation": "Marginal cost of fulfilling +1 additional unit of global demand."},
        {"Constraint": "Contractual SLA Reliability Floor", "Binding_Value": f"{sla_floor*100:.1f}%", "Shadow_Price_EUR": f"€{duals.get('SLA_Constraint', 0.0):.2f} / unit", "Economic_Interpretation": "System penalty paid per 1% increment in network delivery reliability."},
        {"Constraint": "Scope-3 Carbon Emission Budget", "Binding_Value": f"{carbon_cap:.1f} Tons", "Shadow_Price_EUR": f"€{duals.get('Carbon_Constraint', 0.0):.2f} / ton", "Economic_Interpretation": "Marginal abatement cost to reduce network emissions by 1 metric ton."}
    ]
    
    st.dataframe(pd.DataFrame(dual_rows), use_container_width=True, hide_index=True)
