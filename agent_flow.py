from langgraph.graph import StateGraph, END
from langgraph.pregel import Pregel
from typing import TypedDict, Optional, Dict, Any
from load_contracts import get_procurement_summary, get_procurement_structured_data
from scenario_planning import get_scenario_summary, get_scenario_structured_data
from sku_rationalization import get_sku_summary, get_sku_structured_data

# === Define Enhanced Shared State ===
class AgentState(TypedDict):
    # Text summaries
    scenario_summary: Optional[str]
    sku_summary: Optional[str]
    procurement_summary: Optional[str]
    demand_change: Optional[float]
    
    # Structured data for visualizations
    sku_structured_data: Optional[Dict[str, Any]]
    scenario_structured_data: Optional[Dict[str, Any]]
    procurement_structured_data: Optional[Dict[str, Any]]

# === Node 1: Procurement Analysis ===
def procurement_node(state: AgentState) -> AgentState:
    summary = get_procurement_summary()
    structured_data = get_procurement_structured_data()  # Use the new function
    
    return {
        **state, 
        "procurement_summary": "📑 Procurement Summary:\n" + summary,
        "procurement_structured_data": structured_data
    }

# === Node 2: Scenario Planning Analysis ===
def scenario_node(state: AgentState) -> AgentState:
    demand_change = state.get('demand_change', -15)
    summary = get_scenario_summary(demand_change)
    structured_data = get_scenario_structured_data(demand_change)  # Use the new function
    
    return {
        **state, 
        "scenario_summary": "📈 Scenario Planning Summary:\n" + summary,
        "scenario_structured_data": structured_data
    }

# === Node 3: SKU Rationalization ===
def sku_node(state: AgentState) -> AgentState:
    summary = get_sku_summary()
    structured_data = get_sku_structured_data()  # Use the new function
    
    return {
        **state, 
        "sku_summary": "📦 SKU Rationalization Summary:\n" + summary,
        "sku_structured_data": structured_data
    }

# === Node 4: Final Dashboard Aggregation ===
def dashboard_node(state: AgentState) -> AgentState:
    dashboard = (
        "\n🧾 FINAL SUPPLY CHAIN DASHBOARD\n"
        "=====================================\n"
        f"{state.get('procurement_summary', '❗ No procurement summary available.')}\n\n"
        f"{state.get('scenario_summary', '❗ No scenario summary available.')}\n\n"
        f"{state.get('sku_summary', '❗ No SKU summary available.')}\n"
        "=====================================\n"
    )
    return {**state, "final_dashboard": dashboard}