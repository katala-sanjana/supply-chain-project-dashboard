import pandas as pd 
import requests

data_path = "C:/Users/KATALA JEETHENDER/OneDrive/Desktop/college project modification/historical data/supply_chain_data.csv" 

def load_supply_chain_data():
    return pd.read_csv(data_path)

def simulate_demand_change(df, percentage_change):
    df = df.copy()
    df['Simulated_Sales'] = df['Number of products sold'] * (1 + percentage_change / 100)
    df['Revenue_per_unit'] = df['Revenue generated'] / df['Number of products sold']
    df['Simulated_Revenue'] = df['Simulated_Sales'] * df['Revenue_per_unit']
    return df

def get_scenario_structured_data(percentage_change: float):
    df = load_supply_chain_data()
    scenario_df = simulate_demand_change(df, percentage_change)
    
    original_revenue = df['Revenue generated'].sum()
    simulated_revenue = scenario_df['Simulated_Revenue'].sum()
    revenue_change = ((simulated_revenue - original_revenue) / original_revenue) * 100
    
    lead_time_col = 'Lead time' if 'Lead time' in df.columns else 'Lead times'
    avg_lead_time = float(df[lead_time_col].mean())
    avg_shipping = float(df['Shipping costs'].mean())
    
    return {
        'demand_change': percentage_change,
        'base_revenue': float(original_revenue),
        'simulated_revenue': float(simulated_revenue),
        'revenue_change_percent': float(revenue_change),
        'lead_time': avg_lead_time,
        'shipping_cost': avg_shipping,
        'scenario_label': f"{abs(percentage_change)}% Demand Drop" if percentage_change < 0 else f"{percentage_change}% Demand Increase"
    }

def generate_prompt_from_data(scenario_name, df, percentage_change):
    if 'Simulated_Revenue' in df.columns:
        total_revenue = df['Simulated_Revenue'].sum()
        original_revenue = df['Revenue generated'].sum()
        revenue_change = ((total_revenue - original_revenue) / original_revenue) * 100
    else:
        total_revenue = df['Revenue generated'].sum()
        revenue_change = 0
    
    lead_time_col = 'Lead time' if 'Lead time' in df.columns else 'Lead times'
    avg_lead_time = df[lead_time_col].mean()
    avg_shipping = df['Shipping costs'].mean()

    prompt = f"""
You are a supply chain analyst. The following scenario has been simulated: "{scenario_name}"

📊 Numerical Summary:
- Total Revenue: ${total_revenue:,.2f}
- Revenue Change: {revenue_change:+.1f}%
- Avg Lead Time: {avg_lead_time:.2f} days
- Avg Shipping Cost: ${avg_shipping:.2f}

Please analyze:
1. What is the likely business impact of this scenario?
2. What actionable steps should a supply chain manager take?
3. Are there any risks or opportunities this scenario uncovers?

Respond with practical, business-savvy suggestions.
"""
    return prompt

def get_llm_insight(prompt):
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        return response.json()['response'].strip()
    except Exception as e:
        return f"Error getting LLM insight: {str(e)}"

def get_scenario_summary(percentage_change: float):
    df = load_supply_chain_data()
    scenario_df = simulate_demand_change(df, percentage_change)

    if percentage_change < 0:
        label = f"{abs(percentage_change)}% Demand Drop"
    else:
        label = f"{percentage_change}% Demand Increase"

    prompt = generate_prompt_from_data(label, scenario_df, percentage_change)
    insight = get_llm_insight(prompt)
    return insight


   
