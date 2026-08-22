import pulp
import pandas as pd

def run_supply_chain_optimizer(target_demand=10000, freight_shock_asia=0.0, poland_offline=False):
    """
    Simulates base-case and crisis scenarios, solving for the optimal allocation
    and quantifying economic impact.
    """
    suppliers = {
        "Supplier_Germany (Local/Premium)": {
            "unit_cost": 42.0,
            "freight_cost": 3.5,
            "reliability": 0.98,
            "capacity": 7000,
            "risk_penalty": 15.0
        },
        "Supplier_Poland (Nearshore/Balanced)": {
            "unit_cost": 34.0,
            "freight_cost": 6.0,
            "reliability": 0.91,
            "capacity": 0 if poland_offline else 6000,  # Capacity drops to 0 if disrupted
            "risk_penalty": 20.0
        },
        "Supplier_EastAsia (Overseas/Budget)": {
            "unit_cost": 24.5,
            "freight_cost": 12.0 + freight_shock_asia,  # Freight price shock dynamic
            "reliability": 0.78,
            "capacity": 8000,
            "risk_penalty": 35.0
        }
    }

    model = pulp.LpProblem("Supply_Chain_Cost_Minimization", pulp.LpMinimize)

    order_vars = {
        s: pulp.LpVariable(f"Order_{s}", lowBound=0, upBound=data["capacity"], cat="Continuous")
        for s, data in suppliers.items()
    }

    total_cost_expr = []
    for s, data in suppliers.items():
        expected_risk_cost = (1.0 - data["reliability"]) * data["risk_penalty"]
        effective_unit_cost = data["unit_cost"] + data["freight_cost"] + expected_risk_cost
        total_cost_expr.append(order_vars[s] * effective_unit_cost)

    model += pulp.lpSum(total_cost_expr)
    model += pulp.lpSum([order_vars[s] for s in suppliers]) == target_demand

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    results = []
    for s, data in suppliers.items():
        qty = order_vars[s].varValue or 0.0
        expected_risk_cost = (1.0 - data["reliability"]) * data["risk_penalty"]
        effective_unit_cost = data["unit_cost"] + data["freight_cost"] + expected_risk_cost
        results.append({
            "Supplier": s,
            "Allocated Units": round(qty, 0),
            "True Landed Cost (€)": round(effective_unit_cost, 2),
            "Total Spend (€)": round(qty * effective_unit_cost, 2)
        })

    return pd.DataFrame(results), pulp.value(model.objective)

if __name__ == "__main__":
    print("--- 1. BASE CASE (Normal Operations) ---")
    df_base, cost_base = run_supply_chain_optimizer()
    print(df_base.to_string(index=False))
    print(f"Total Cost: €{cost_base:,.2f}\n")

    print("--- 2. CRISIS: POLAND FACILITY SHUTS DOWN ---")
    df_poland_down, cost_poland_down = run_supply_chain_optimizer(poland_offline=True)
    print(df_poland_down.to_string(index=False))
    print(f"Total Cost: €{cost_poland_down:,.2f}")
    print(f"Disruption Cost Impact: +€{cost_poland_down - cost_base:,.2f}\n")

    print("--- 3. CRISIS: RED SEA ROUTE SPIKES ASIA FREIGHT (+€15/unit) ---")
    df_freight_spike, cost_freight_spike = run_supply_chain_optimizer(freight_shock_asia=15.0)
    print(df_freight_spike.to_string(index=False))
    print(f"Total Cost: €{cost_freight_spike:,.2f}")
    print(f"Optimized Decision: Shifted volume immediately to Germany to prevent €{abs(cost_freight_spike - cost_base):,.2f} overrun.")