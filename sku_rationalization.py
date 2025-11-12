import pandas as pd
import requests

# Load Data
data_path = "C:/Users/KATALA JEETHENDER/OneDrive/Desktop/college project modification/historical data/supply_chain_data.csv"
df = pd.read_csv(data_path)

# STEP 1: Compute Profit, Profit Margin, Sales Velocity
df['Profit'] = df['Revenue generated'] - df['Manufacturing costs']
df['Profit Margin'] = df['Profit'] / df['Revenue generated']
df['Sales Velocity'] = df['Number of products sold'] / (df['Stock levels'] + 1)  # Avoid divide by zero

# STEP 2: Define Rules for Rationalization
def classify_sku(row):
    margin = row['Profit Margin']
    velocity = row['Sales Velocity']
    defect = row['Defect rates']
    
    if margin >= 0.25 and velocity >= 1.0 and defect < 1.5:
        return '✅ Keep'
    elif 0.1 <= margin < 0.25 or 0.5 <= velocity < 1.0 or 1.5 <= defect < 3.5:
        return '♻️ Bundle/Optimize'
    else:
        return '❌ Discontinue'

df['SKU Recommendation'] = df.apply(classify_sku, axis=1)

# STEP 3: Generate structured data for dashboard
def get_sku_structured_data():
    keep_count = len(df[df['SKU Recommendation'] == '✅ Keep'])
    optimize_count = len(df[df['SKU Recommendation'] == '♻️ Bundle/Optimize'])
    discontinue_count = len(df[df['SKU Recommendation'] == '❌ Discontinue'])
    
    return {
        'keep_count': keep_count,
        'optimize_count': optimize_count,
        'discontinue_count': discontinue_count,
        'total_skus': len(df),
        'product_types': df['Product type'].value_counts().to_dict(),
        'avg_profit_margin': float(df['Profit Margin'].mean()),
        'avg_sales_velocity': float(df['Sales Velocity'].mean()),
        'avg_defect_rate': float(df['Defect rates'].mean())
    }

# STEP 4: Generate Prompt for LLM
def generate_rationalization_prompt(df):
    top_discontinue = df[df['SKU Recommendation'] == '❌ Discontinue'].head(3)
    top_bundle = df[df['SKU Recommendation'] == '♻️ Bundle/Optimize'].head(3)
    top_keep = df[df['SKU Recommendation'] == '✅ Keep'].head(3)
    prompt = f"""
You are a supply chain strategy expert. Analyze the following SKU performance data and provide specific actionable insights.

📉 Discontinue Candidates:
{top_discontinue[['SKU', 'Profit Margin', 'Sales Velocity', 'Defect rates']].to_string(index=False)}

♻️ Bundle/Optimize Candidates:
{top_bundle[['SKU', 'Profit Margin', 'Sales Velocity', 'Defect rates']].to_string(index=False)}

📈 High-Performing SKUs:
{top_keep[['SKU', 'Profit Margin', 'Sales Velocity', 'Defect rates']].to_string(index=False)}

Instructions:
1. For each Discontinue candidate, explain why it is underperforming (using actual metrics).
2. For each Bundle/Optimize candidate, suggest what product(s) it could be bundled with or how it can be improved.
3. Highlight any patterns or risks visible from the data.

Format:
- List insights as bullet points per SKU.
- End with a summary paragraph on portfolio health.
"""
    return prompt

# STEP 5: Get Insight from TinyLLaMA
def get_llm_insight(prompt):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()['response'].strip() 

# ✅ FUNCTION to call from LangGraph
def get_sku_summary():
    prompt = generate_rationalization_prompt(df)
    return get_llm_insight(prompt)
    