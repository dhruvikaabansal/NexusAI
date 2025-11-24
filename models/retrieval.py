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
            # CEO Strategic Content
            {"text": "Risk Assessment: Supply chain volatility in the North region is a critical risk due to recent logistics disruptions. Mitigation: Diversify suppliers and increase buffer inventory.", "source": "Q3 Risk Report", "roles": ["CEO", "COO"]},
            {"text": "Competitor Update: Competitor 'TechGiant' has lowered prices on their entry-level units by 10%, pressuring our margins. Recommendation: Focus on premium features and customer service differentiation.", "source": "Market Intelligence", "roles": ["CEO", "CFO"]},
            {"text": "Revenue Forecast: Q4 revenue is projected to exceed targets by 15%, driven by strong adoption of Gadget_Z in the West region. Expected total: $2.8M for Q4.", "source": "Financial Outlook", "roles": ["CEO", "CFO"]},
            {"text": "Strategic Initiative: 'Project Apollo' aims to automate 50% of the assembly line by next year to reduce overhead costs by 20% and improve throughput by 30%.", "source": "Strategy Doc", "roles": ["CEO", "COO"]},
            {"text": "Regulatory Alert: New safety compliance standards for battery disposal will come into effect next month. All manufacturing lines must be certified by Jan 15.", "source": "Legal Brief", "roles": ["CEO", "COO", "HR"]},
            {"text": "Talent Retention: Engineering turnover has decreased by 5% following the new equity program. Current retention rate: 92% (up from 87%).", "source": "HR Quarterly", "roles": ["CEO", "HR"]},
            
            # CFO Financial Content
            {"text": "Cost Reduction Memo: Analysis shows that energy costs account for 18% of total OpEx. Recommendation: Invest in energy-efficient motors for Lines A and C to save $45K annually.", "source": "CFO Analysis", "roles": ["CFO", "COO"]},
            {"text": "Margin Analysis: Gadget_X has the highest margin at 42%, while Gadget_Y is at 28%. Focus sales efforts on premium products to improve overall profitability.", "source": "Product Profitability Report", "roles": ["CFO"]},
            {"text": "Cash Flow Projection: Operating cash flow is stable at $1.2M/month. Accounts receivable days: 32 (target: 30). Recommend tightening payment terms with enterprise customers.", "source": "Treasury Report", "roles": ["CFO"]},
            {"text": "Maintenance Budget: Total maintenance costs for Q3 were $127K, 8% under budget. Preventive maintenance program is reducing emergency repairs by 15%.", "source": "Finance Dashboard", "roles": ["CFO", "COO"]},
            
            # COO Operations Content
            {"text": "Production Efficiency: Line B has the highest throughput at 485 units/day with only 12 minutes of downtime. Best practice: Implement Line B's maintenance schedule across all lines.", "source": "Operations Review", "roles": ["COO"]},
            {"text": "Energy Consumption Analysis: Night shift (Shift 3) consumes 22% more energy per unit than day shift. Root cause: Older equipment on night crew. Recommendation: Rotate equipment usage.", "source": "Sustainability Report", "roles": ["COO", "CFO"]},
            {"text": "Downtime Root Cause: Line C accounts for 40% of total downtime due to aging conveyor belts. Replacement scheduled for next month, expected to reduce downtime by 60%.", "source": "Maintenance Log", "roles": ["COO"]},
            {"text": "Quality Metrics: Overall defect rate is 2.1%, down from 2.8% last quarter. Line A has the lowest rate at 1.4%. Quality training program showing positive results.", "source": "Quality Assurance Report", "roles": ["COO"]},
            {"text": "Throughput vs Energy Correlation: Analysis shows strong correlation (r=0.78) between energy consumption and throughput. Higher production runs are more energy-efficient per unit.", "source": "Operations Analytics", "roles": ["COO"]},
            
            # HR People Content
            {"text": "Performance Distribution: 68% of employees rated 'Good' or 'Excellent'. Top performers concentrated in Engineering (avg 4.2/5) and Sales (avg 4.0/5). Needs Improvement: 12% of workforce.", "source": "Annual Review Summary", "roles": ["HR"]},
            {"text": "Headcount by Department: Engineering: 18, Sales: 12, Operations: 10, Finance: 5, HR: 4. Total headcount: 49. Hiring plan: Add 6 engineers in Q1.", "source": "HR Dashboard", "roles": ["HR"]},
            {"text": "Safety Incidents: 8 incidents in Q3 (down from 12 in Q2). Severity: 6 minor, 2 moderate, 0 critical. New safety training program reduced incident rate by 33%.", "source": "Safety Report", "roles": ["HR", "COO"]},
            {"text": "Employee Tenure: Average tenure is 4.2 years. High-tenure departments: Finance (6.1 yrs), Engineering (5.3 yrs). New hire retention (1-year): 88%.", "source": "Retention Analysis", "roles": ["HR"]},
            {"text": "Safety Training Program: New comprehensive safety training launched in August. 100% of manufacturing staff certified. Next phase: Advanced equipment handling certification in January.", "source": "Training Memo", "roles": ["HR", "COO"]},
            {"text": "Employee Engagement: eNPS score is 42 (Industry avg: 35). Top drivers: Career growth opportunities, competitive compensation. Improvement area: Work-life balance (score: 6.8/10).", "source": "Engagement Survey", "roles": ["HR", "CEO"]}
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
