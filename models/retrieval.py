from sentence_transformers import SentenceTransformer, util
import pandas as pd
from app.database import get_db_connection
import os

class Retriever:
    def __init__(self):
        self.model = None
        self.cache = {} # Cache embeddings for demo speed
        
        # Static Knowledge Base for qualitative/strategic queries (Mocking external documents)
        self.knowledge_base = [
            {"text": "Risk Assessment: Supply chain volatility in the North region is a critical risk due to recent logistics disruptions.", "source": "Q3 Risk Report", "roles": ["CEO", "COO"]},
            {"text": "Competitor Update: Competitor 'TechGiant' has lowered prices on their entry-level units by 10%, pressuring our margins.", "source": "Market Intelligence", "roles": ["CEO", "Sales"]},
            {"text": "Revenue Forecast: Q4 revenue is projected to exceed targets by 15%, driven by strong adoption of Gadget_Z.", "source": "Financial Outlook", "roles": ["CEO", "CFO"]},
            {"text": "Strategic Initiative: 'Project Apollo' aims to automate 50% of the assembly line by next year to reduce overhead.", "source": "Strategy Doc", "roles": ["CEO", "COO"]},
            {"text": "Regulatory Alert: New safety compliance standards for battery disposal will come into effect next month.", "source": "Legal Brief", "roles": ["CEO", "COO", "HR"]},
            {"text": "Talent Retention: Engineering turnover has decreased by 5% following the new equity program.", "source": "HR Quarterly", "roles": ["CEO", "HR"]}
        ]

    def load_model(self):
        if not self.model:
            print("Loading embedding model (all-MiniLM-L6-v2)...")
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                print("Model loaded.")
            except Exception as e:
                print(f"Failed to load model: {e}")
                self.model = None

    def search(self, query, role, top_k=3):
        if not self.model:
            self.load_model()
        
        if not self.model:
            return [] # Fallback if model fails

        results = []
        
        # 1. Search Knowledge Base (Qualitative)
        kb_docs = [doc for doc in self.knowledge_base if role in doc['roles']]
        if kb_docs:
            kb_texts = [doc['text'] for doc in kb_docs]
            kb_embeddings = self.model.encode(kb_texts, convert_to_tensor=True)
            query_embedding = self.model.encode(query, convert_to_tensor=True)
            
            kb_scores = util.cos_sim(query_embedding, kb_embeddings)[0]
            
            for idx, score in enumerate(kb_scores):
                if score > 0.25: # Slightly lower threshold for semantic matches
                    results.append({
                        "score": score.item(),
                        "text": kb_docs[idx]['text'],
                        "source": kb_docs[idx]['source']
                    })

        # 2. Search Database (Quantitative)
        # Identify relevant tables based on role/query (Heuristic to narrow scope)
        tables = []
        q_lower = query.lower()
        if role == "CEO":
            tables = ["sales", "field", "manufacturing"]
        elif role == "CFO":
            tables = ["sales"]
        elif role == "COO":
            tables = ["manufacturing"]
        elif role == "HR":
            tables = ["users", "field"]
        
        # Overrides based on keywords
        if "sales" in q_lower or "revenue" in q_lower or "profit" in q_lower or "margin" in q_lower: tables.append("sales")
        if "production" in q_lower or "throughput" in q_lower or "energy" in q_lower or "maintenance" in q_lower: tables.append("manufacturing")
        if "incident" in q_lower or "safety" in q_lower or "satisfaction" in q_lower: tables.append("field")
        if "employee" in q_lower or "performance" in q_lower or "headcount" in q_lower: tables.append("users")
        
        tables = list(set(tables))
        
        conn = get_db_connection()
        
        for table in tables:
            df = pd.read_sql(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 50", conn) # Limit for demo speed
            if df.empty: continue
            
            # Create text representation of rows
            # e.g. "Revenue: 5000, Region: North"
            if table == "sales":
                df['text'] = df.apply(lambda x: f"Sales: Product {x['product_id']} sold {x['units_sold']} units. Revenue: ${x['revenue']}, Profit: ${x['profit']}, Margin: {x['margin']}, Region: {x['region']}", axis=1)
            elif table == "manufacturing":
                df['text'] = df.apply(lambda x: f"Mfg: Line {x['line_id']} (Shift: {x['shift_id']}). Throughput: {x['throughput']}, Energy: {x['energy_consumption']}kWh, Maint Cost: ${x['maintenance_cost']}, Downtime: {x['downtime_minutes']}m", axis=1)
            elif table == "field":
                df['text'] = df.apply(lambda x: f"Incident: {x['severity']} issue on {x['product_id']}. Desc: {x['description']}. Resolution: {x['resolution_time_hours']}h, CSAT: {x['customer_satisfaction']}/5", axis=1)
            elif table == "users":
                df['text'] = df.apply(lambda x: f"User: {x['name']} ({x['role']}, {x['department']}). Performance: {x['performance']}/5, Tenure: {x['tenure']} yrs", axis=1)
            
            # Embed and search
            embeddings = self.model.encode(df['text'].tolist(), convert_to_tensor=True)
            query_embedding = self.model.encode(query, convert_to_tensor=True)
            
            scores = util.cos_sim(query_embedding, embeddings)[0]
            
            # Get top matches
            top_results = []
            for idx, score in enumerate(scores):
                if score > 0.3: # Threshold
                    top_results.append({
                        "score": score.item(),
                        "text": df.iloc[idx]['text'],
                        "source": table
                    })
            
            results.extend(top_results)
            
        conn.close()
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
