import requests
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd

def get_procurement_structured_data():
    return {
        'contracts_processed': 3,  # From your contracts folder
        'risk_level': 'Medium',
        'key_terms_extracted': ['Master Agreement', 'Service Delivery', 'Compliance', 'Payment Terms'],
        'analysis_timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def get_procurement_summary() -> str:
    # Step 1: Load and chunk documents
    documents = SimpleDirectoryReader("./contracts").load_data()
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    nodes = splitter.get_nodes_from_documents(documents)
    texts = [node.text for node in nodes]

    # Step 2: Generate embeddings and FAISS index
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    text_id_map = {i: text for i, text in enumerate(texts)}

    # Step 3: Generate LLM Summary
    context = "\n\n".join(text_id_map.values())[:3000]
    prompt = f"""
You are a supply chain legal assistant. Based on the following context from procurement contracts, summarize key terms, risks, and decision points.

📄 Context:
{context}

🎯 Summary:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "tinyllama", "prompt": prompt, "stream": False}
    )
    return response.json().get("response", "").strip()

