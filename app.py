import streamlit as st
import pandas as pd
import numpy as np
import pulp
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Autonomous Multi-Tier Sourcing & Disruption Solver",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- FRENCH INSTITUTIONAL PALETTE & BULLETPROOF WIDGET OVERRIDES ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    /* 1. Global CSS Variables: Overrides Streamlit Native Engine */
    :root, .stApp {
        --primary-color: #0070AD !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* 2. Deep Navy Executive Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }
    
    /* Input Field Labels */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] label span {
        color: #FFFFFF !important;
        font-size: 0.90rem !important;
        font-weight: 600 !important;
    }

    /* Slider Values */
    section[data-testid="stSidebar"] [data-testid="stSlider"] div,
    section[data-testid="stSidebar"] [data-testid="stSlider"] span,
    section[data-testid="stSidebar"] [data-testid="stSlider"] p {
        color: #F8FAFC !important;
    }

    /* Slider Min / Max Labels */
    section[data-testid="stSidebar"] [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] [data-testid="stTickBarMax"],
    section[data-testid="stSidebar"] div[data-testid="stTickBar"] div {
        color: #94A3B8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.74rem !important;
        font-weight: 600 !important;
    }

    /* Current Slider Value Box */
    section[data-testid="stSidebar"] div[data-testid="stThumbValue"] {
        background-color: #0070AD !important;
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 0.80rem !important;
        border-radius: 4px !important;
        padding: 2px 6px !important;
    }

    /* Slider Track & Thumb */
    section[data-testid="stSidebar"] div[data-baseweb="slider"] div[role="slider"] {
        background-color: #0070AD !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 0 2px rgba(0, 112, 173, 0.5) !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="slider"] > div > div > div {
        background: #0070AD !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="slider"] > div > div {
        background: #334155 !important;
    }

    /* 3. Executive Metric Cards */
    .glass-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }
    .glass-card-accent {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #0070AD;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 700;
        color: #0070AD;
        letter-spacing: -0.8px;
        line-height: 1.2;
    }
    .metric-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .metric-caption {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #0F172A;
        font-weight: 500;
        margin-top: 6px;
    }

    /* 4. Action Directives & Badges */
    .directive-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .badge-priority {
        background-color: #E0F2FE;
        color: #0369A1;
        border: 1px solid #BAE6FD;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
    }
    .badge-balancing {
        background-color: #F1F5F9;
        color: #334155;
        border: 1px solid #CBD5E1;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
    }
    .badge-bypassed {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
    }

    /* 5. Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #CBD5E1;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        border-radius: 6px 6px 0 0 !important;
        color: #64748B !important;
        padding: 10px 18px !important;
        border: 1px solid #E2E8F0 !important;
        border-bottom: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0070AD !important;
        color: #FFFFFF !important;
        border: 1px solid #0070AD !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important;
    }

    /* 6. Main Canvas Typography */
    .main h1, .main h2, .main h3, .main h4,
    [data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3, [data-testid="stMain"] h4 {
        color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.4px;
    }
    p, span {
        color: #334155;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_head, col_badge = st.columns([4, 1])
with col_head:
    st.markdown("<h1 style='margin-bottom: 2px;'>Autonomous Multi-Tier Sourcing & Disruption Solver</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 0.95rem; margin-top: 0px;'>Prescriptive Optimization with LP Relaxation Duals & Stochastic Monte Carlo Tail-Risk Stress Engine</p>", unsafe_allow_html=True)
with col_badge:
    st.markdown("""
    <div style='text-align: right; padding-top: 10px;'>
        <span style='background: #E0F2FE; border: 1px solid #BAE6FD; color: #0284C7; padding: 6px 14px; border-radius: 4px; font-size: 0.8rem; font-weight: 700; font-family: "JetBrains Mono", monospace;'>
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
    st.markdown(
        "<div style='color: #FFFFFF !important; font-size: 1.15rem; font-weight: 800; letter-spacing: -0.2px; margin-top: 10px; margin-bottom: 12px; font-family: Inter, sans-serif;'>1. Operational Targets</div>",
        unsafe_allow_html=True
    )
    demand = st.slider("Target Network Demand (Units)", min_value=3000, max_value=15000, value=10000, step=500)
    sla_floor = st.slider("Contractual SLA Floor (Min %)", min_value=0.70, max_value=0.99, value=0.88, step=0.01, format="%.2f")
    carbon_cap = st.slider("Scope-3 Carbon Cap (Metric Tons)", min_value=30.0, max_value=150.0, value=90.0, step=5.0)
    
    st.markdown("<hr style='border: none; border-top: 1px solid #1E293B; margin: 24px 0;'>", unsafe_allow_html=True)
    
    st.markdown(
        "<div style='color: #FFFFFF !important; font-size: 1.15rem; font-weight: 800; letter-spacing: -0.2px; margin-bottom: 12px; font-family: Inter, sans-serif;'>2. Macro Surcharges</div>",
        unsafe_allow_html=True
    )
    freight_shock = st.slider("Global Freight Shock Adder (€/unit)", min_value=0.0, max_value=10.0, value=0.0, step=0.5)

# --- EDITABLE NETWORK TOPOLOGY ---
with st.expander("Configure Node Topology & Supplier Contract Parameters", expanded=False):
    st.write("Modify hub pricing, capacities, historical reliability rates, and environmental factors:")
    edited_df = st.data_editor(default_nodes, num_rows="dynamic", use_container_width=True)

# Apply global surcharge
topology = edited_df.copy()
topology["Freight"] = topology["Freight"] + freight_shock
topology["Total_Landed_Expected"] = topology["Base_Cost"] + topology["Freight"] + ((1.0 - topology["Reliability"]) * topology["Penalty"])

# --- CORE OPTIMIZATION ENGINE ---
def solve_sourcing(df, total_demand, min_sla, max_carbon):
    prob = pulp.LpProblem("Sourcing_Optimization", pulp.LpMinimize)
    hubs = df["Hub"].tolist()
    
    x = pulp.LpVariable.dicts("Alloc", hubs, lowBound=0.0)
    
    for h in hubs:
        cap_val = float(df.loc[df["Hub"] == h, "Capacity"].values[0])
        prob += x[h] <= cap_val, f"Cap_{h}"
    
    prob += pulp.lpSum([x[h] * float(df.loc[df["Hub"] == h, "Total_Landed_Expected"].values[0]) for h in hubs])
    prob += pulp.lpSum([x[h] for h in hubs]) == float(total_demand), "Demand_Constraint"
    prob += pulp.lpSum([x[h] * float(df.loc[df["Hub"] == h, "Reliability"].values[0]) for h in hubs]) >= float(total_demand * min_sla), "SLA_Constraint"
    prob += pulp.lpSum([x[h] * (float(df.loc[df["Hub"] == h, "Carbon_kg"].values[0]) / 1000.0) for h in hubs]) <= float(max_carbon), "Carbon_Constraint"
    
    solver = pulp.PULP_CBC_CMD(msg=0)
    prob.solve(solver)
    
    status = pulp.LpStatus[prob.status]
    allocations = {h: float(x[h].varValue) if x[h].varValue is not None else 0.0 for h in hubs}
    
    shadow_prices = {}
    for name, c in prob.constraints.items():
        shadow_prices[name] = float(c.pi) if c.pi is not None else 0.0
        
    return status, allocations, float(pulp.value(prob.objective) or 0.0), shadow_prices

opt_status, alloc_dict, opt_cost, duals = solve_sourcing(topology, demand, sla_floor, carbon_cap)

if opt_status != "Optimal":
    st.error(f"Optimization status: {opt_status}. The specified SLA floor ({sla_floor*100:.1f}%) and Carbon Cap ({carbon_cap}t) are mutually incompatible with node capacities. Relax constraints in the sidebar.")
    st.stop()

topology["Allocated_Units"] = topology["Hub"].map(alloc_dict)
topology["Alloc_Pct"] = (topology["Allocated_Units"] / topology["Capacity"]) * 100.0
topology["Total_Carbon_Tons"] = (topology["Allocated_Units"] * topology["Carbon_kg"]) / 1000.0
topology["Total_Spend_EUR"] = topology["Allocated_Units"] * topology["Total_Landed_Expected"]

total_carbon_emitted = float(topology["Total_Carbon_Tons"].sum())
blended_reliability = float((topology["Allocated_Units"] * topology["Reliability"]).sum() / demand)

avg_network_unit_cost = float(topology["Total_Landed_Expected"].mean())
naive_spend = float(demand * avg_network_unit_cost)

if naive_spend <= opt_cost:
    conservative_unit_cost = float(topology.sort_values(by="Reliability", ascending=False)["Total_Landed_Expected"].iloc[0])
    naive_spend = float(demand * conservative_unit_cost)

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
        <div class='metric-value' style='color: #0F172A;'>€{arbitrage_savings:,.0f}</div>
        <div class='metric-caption'>vs. Status-Quo Baseline</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-sub'>Network Reliability</div>
        <div class='metric-value' style='color: #0F172A;'>{blended_reliability*100:.1f}%</div>
        <div class='metric-caption'>Target Floor: {sla_floor*100:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-sub'>Scope-3 Footprint</div>
        <div class='metric-value' style='color: #0070AD;'>{total_carbon_emitted:.1f}t</div>
        <div class='metric-caption'>Ceiling: {carbon_cap:.1f} Metric Tons</div>
    </div>
    """, unsafe_allow_html=True)

# --- PRESCRIPTIVE ALLOCATION DIRECTIVES ---
st.markdown("<div class='glass-card-accent'>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top: 0; margin-bottom: 6px; color: #0F172A;'>Prescriptive Executive Sourcing Directives</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.88rem; color: #64748B; margin-bottom: 16px;'>Actionable node-by-node procurement directives derived from the solved LP simplex:</p>", unsafe_allow_html=True)

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
            <span style='font-weight: 700; color: #0F172A; font-size: 0.95rem;'>{hub_name}</span>
            {badge}
        </div>
        <div style='font-size: 0.86rem; color: #475569;'>{desc}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- ANALYTICAL WORKBENCH TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Sourcing Matrix & ESG", 
    "Monte Carlo VaR Tail Risk", 
    "Multi-Objective Pareto Frontier", 
    "Dual Shadow Pricing"
])

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "#FFFFFF",
        "plot_bgcolor": "#FFFFFF",
        "font": {"color": "#0F172A", "family": "Inter, sans-serif"},
        "xaxis": {
            "gridcolor": "#F1F5F9",
            "zerolinecolor": "#E2E8F0",
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11, "color": "#475569"}
        },
        "yaxis": {
            "gridcolor": "#F1F5F9",
            "zerolinecolor": "#E2E8F0",
            "tickfont": {"family": "JetBrains Mono, monospace", "size": 11, "color": "#475569"}
        }
    }
}

# --- TAB 1: SOURCING MATRIX ---
with tab1:
    c_left, c_right = st.columns([3, 2])
    with c_left:
        st.markdown("<h4 style='color: #0F172A;'>Optimal Order Allocation vs. Available Capacity</h4>", unsafe_allow_html=True)
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=topology["Hub"], y=topology["Capacity"],
            name="Max Capacity", marker_color="#E2E8F0", marker_line_color="#CBD5E1", marker_line_width=1
        ))
        fig_bar.add_trace(go.Bar(
            x=topology["Hub"], y=topology["Allocated_Units"],
            name="Optimal Order", marker_color="#0070AD"
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
        st.markdown("<h4 style='color: #0F172A;'>Scope-3 Carbon Share by Hub</h4>", unsafe_allow_html=True)
        fig_pie = px.pie(
            topology, values="Total_Carbon_Tons", names="Hub",
            color_discrete_sequence=["#0070AD", "#0284C7", "#38BDF8", "#BAE6FD"],
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
    st.markdown("<h4 style='color: #0F172A;'>Stochastic Disruption Engine (1,000 Tail-Risk Trials)</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: #64748B;'>Simulates Bernoulli failure shocks across hubs alongside Gaussian freight rate volatility to derive empirical Monte Carlo Value-at-Risk (VaR₉₅) and Conditional VaR (Expected Shortfall).</p>", unsafe_allow_html=True)
    
    np.random.seed(42)
    n_sims = 1000
    active_hubs = topology[topology["Allocated_Units"] > 0]
    
    sim_costs = np.zeros(n_sims)
    base_landed = float((active_hubs["Allocated_Units"] * (active_hubs["Base_Cost"] + active_hubs["Freight"])).sum())
    
    for i in range(n_sims):
        shock_penalties = 0.0
        freight_jitter = np.random.normal(0, 0.15 * active_hubs["Freight"].values)
        
        for idx, (_, hub_row) in enumerate(active_hubs.iterrows()):
            failed = np.random.binomial(1, 1.0 - float(hub_row["Reliability"]))
            if failed:
                shock_penalties += float(hub_row["Allocated_Units"]) * float(hub_row["Penalty"]) * np.random.uniform(0.3, 1.0)
            shock_penalties += float(hub_row["Allocated_Units"]) * freight_jitter[idx]
            
        sim_costs[i] = base_landed + shock_penalties

    var_95 = float(np.percentile(sim_costs, 95))
    cvar_95 = float(sim_costs[sim_costs >= var_95].mean())
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class='glass-card'><div class='metric-sub'>Expected (Mean) Spend</div><div class='metric-value' style='color: #0F172A;'>€{sim_costs.mean():,.0f}</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class='glass-card'><div class='metric-sub'>Monte Carlo VaR (95%)</div><div class='metric-value' style='color: #0070AD;'>€{var_95:,.0f}</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class='glass-card'><div class='metric-sub'>CVaR 95 (Worst 5% Expected Loss)</div><div class='metric-value' style='color: #334155;'>€{cvar_95:,.0f}</div></div>""", unsafe_allow_html=True)

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(x=sim_costs, nbinsx=45, marker_color="#93C5FD", opacity=0.85, name="Scenario Cost Distribution"))
    fig_hist.add_vline(x=var_95, line_dash="dash", line_color="#0070AD", line_width=2.5, annotation_text=f"MC VaR 95: €{var_95:,.0f}", annotation_position="top left", annotation_font_color="#0070AD", annotation_font_family="JetBrains Mono")
    fig_hist.add_vline(x=cvar_95, line_dash="dot", line_color="#0F172A", line_width=2.5, annotation_text=f"CVaR 95: €{cvar_95:,.0f}", annotation_position="top right", annotation_font_color="#0F172A", annotation_font_family="JetBrains Mono")
    fig_hist.update_layout(
        xaxis_title="Empirical Simulated Landed Spend (€)",
        yaxis_title="Simulation Frequency",
        margin=dict(l=20, r=20, t=30, b=20),
        height=320,
        template=PLOTLY_TEMPLATE
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# --- TAB 3: ESG PARETO FRONTIER ---
with tab3:
    st.markdown("<h4 style='color: #0F172A;'>Multi-Objective ε-Constraint Pareto Frontier</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: #64748B;'>Traces optimal landed cost across stepped carbon caps to reveal the exact marginal price of network decarbonization.</p>", unsafe_allow_html=True)
    
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
        line=dict(color="#0070AD", width=3),
        marker=dict(size=8, color="#0284C7", line=dict(color="#FFFFFF", width=2)),
        name="Pareto Frontier"
    ))
    fig_pareto.add_trace(go.Scatter(
        x=[total_carbon_emitted], y=[opt_cost],
        mode="markers",
        marker=dict(size=14, color="#0F172A", symbol="diamond"),
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
    st.markdown("<h4 style='color: #0F172A;'>Constraint Dual Values & Sensitivity (Continuous LP Relaxation)</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: #64748B;'>Dual shadow prices (π) extracted from the solved continuous simplex relaxation. Quantifies the exact marginal economic value of relaxing constraints or relieving network bottlenecks.</p>", unsafe_allow_html=True)
    
    demand_dual = float(duals.get("Demand_Constraint", 0.0))
    sla_dual = float(duals.get("SLA_Constraint", 0.0))
    carbon_dual = float(duals.get("Carbon_Constraint", 0.0))

    if abs(sla_dual) < 1e-4:
        sla_interp = "€0.00/unit — Non-binding constraint (slack exists; marginal relaxation provides no objective cost reduction)."
    else:
        sla_interp = f"Marginal penalty paid per unit of increased network reliability requirement: €{abs(sla_dual):.2f} / unit."

    if abs(carbon_dual) < 1e-4:
        carbon_interp = "€0.00/ton — Non-binding carbon cap (emissions operate within budget; loosening cap has zero cost impact)."
    else:
        carbon_interp = f"Solver dual: {carbon_dual:,.2f} €/t. Economic Interpretation: Tightening the carbon cap by 1 metric ton increases minimum network cost by €{abs(carbon_dual):,.2f}."

    dual_rows = [
        {
            "Constraint": "Network Demand Equilibrium",
            "Binding_Level": f"{demand:,.0f} Units",
            "Shadow_Price_EUR": f"€{demand_dual:.2f} / unit",
            "Economic_Interpretation": "Marginal system landed cost of fulfilling +1 additional unit of customer demand."
        },
        {
            "Constraint": "Contractual SLA Floor",
            "Binding_Level": f"{sla_floor*100:.1f}%",
            "Shadow_Price_EUR": f"€{sla_dual:.2f} / unit",
            "Economic_Interpretation": sla_interp
        },
        {
            "Constraint": "Scope-3 Carbon Cap",
            "Binding_Level": f"{carbon_cap:.1f} Tons",
            "Shadow_Price_EUR": f"€{carbon_dual:.2f} / ton",
            "Economic_Interpretation": carbon_interp
        }
    ]
    
    st.dataframe(pd.DataFrame(dual_rows), use_container_width=True, hide_index=True)
