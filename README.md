# Supply Chain Intelligence Dashboard 
An AI-powered responsive dashboard for comprehensive supply chain management with multi-agent worflows where each node is an agent performing individual task.

## 🚀 Overview 
This system provides intelligent supply chain insights through three specialized analysis modules coordinated by an graph-based orchestration framework. This dashboard provides and data-driven demand simulation.

## 🏗️Architecture 
### Core Components:
- **Multi-Agent Workflow**: LangGraph-coordinated analysis pipeline
- **AI Analysis Engine**: TinyLLaMA LLM insights across domains
- **Interactive Dashboard**: Python library Streamlit-based interface

### Analysis Modules:
1. **Procurement Analysis**: Contract document processing and risk assessment from text summarization.
2. **SKU Rationalization**: Product portfolio optimization and classification  
3. **Scenario Planning**: Demand change simulation and revenue impact

## 🔄 Workflow 
1. User Input - Parameters provided via dashboard interface

2. LangGraph Orchestration - Intelligent routing and coordination

3. Multi-Agent Processing - Parallel analysis by specialized modules

4. Dashboard Visualization - Interactive results presentation

5. Shared State Management - Centralized data persistence across all steps 

## Running the System
Start Agent Pipeline (Backend) 
python agent.py

Launch Dashboard (Frontend) 
streamlit run dashboard.py 

## 📊 Dashboard Features
Unified Intelligence Display: Correlated insights across all modules 

Interactive Scenario Controls: Real-time parameter adjustment

Multi-format Output: Text summaries, metrics, and visual charts 

## 🔧 Technology Stack 
Language Model: TinyLLaMA (via Ollama) 

Dashboard: Streamlit  

Visualization: Plotly




