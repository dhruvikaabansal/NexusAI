import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

DATA_DIR = "data/synthetic"
os.makedirs(DATA_DIR, exist_ok=True)

def generate_manufacturing_data(n_rows=100):
    print("Generating Manufacturing Data...")
    dates = [datetime.now() - timedelta(days=x) for x in range(n_rows)]
    data = {
        "date": [d.strftime("%Y-%m-%d") for d in dates],
        "line_id": [random.choice(["Line_A", "Line_B", "Line_C"]) for _ in range(n_rows)],
        "throughput": [random.randint(800, 1200) for _ in range(n_rows)],
        "downtime_minutes": [random.randint(0, 120) for _ in range(n_rows)],
        "defect_rate": [round(random.uniform(0.01, 0.05), 3) for _ in range(n_rows)],
        "shift": [random.choice(["Morning", "Evening", "Night"]) for _ in range(n_rows)]
    }
import pandas as pd
import numpy as np
import os

# Ensure directory exists
os.makedirs("data/synthetic", exist_ok=True)

np.random.seed(42)

# 1. Manufacturing Data
# Added: energy_consumption, maintenance_cost, shift_id
dates = pd.date_range(start="2023-01-01", periods=90, freq="D")
lines = ["Line_A", "Line_B", "Line_C", "Line_D"]
mfg_data = []

for date in dates:
    for line in lines:
        throughput = np.random.normal(1000, 100)
        downtime = np.random.exponential(20) if np.random.rand() > 0.8 else 0
        defect_rate = np.random.beta(2, 50)
        energy = throughput * 0.5 + np.random.normal(50, 5) # kWh
        maint_cost = downtime * 50 # $50 per min of downtime
        
        mfg_data.append({
            "date": date,
            "line_id": line,
            "throughput": int(throughput),
            "downtime_minutes": int(downtime),
            "defect_rate": round(defect_rate, 4),
            "energy_consumption": round(energy, 2),
            "maintenance_cost": round(maint_cost, 2),
            "shift_id": np.random.choice(["Morning", "Evening", "Night"])
        })

pd.DataFrame(mfg_data).to_csv("data/synthetic/manufacturing.csv", index=False)
print("Saved data/synthetic/manufacturing.csv")

# 2. Sales Data
# Added: profit, customer_segment, lead_source
products = ["Gadget_X", "Gadget_Y", "Gadget_Z"]
regions = ["North", "South", "East", "West"]
sales_data = []

for date in dates:
    for _ in range(5): # 5 sales per day
        prod = np.random.choice(products)
        units = np.random.randint(10, 100)
        price = {"Gadget_X": 50, "Gadget_Y": 150, "Gadget_Z": 300}[prod]
        rev = units * price
        margin = np.random.uniform(0.1, 0.4)
        cost = rev * (1 - margin)
        profit = rev - cost
        
        sales_data.append({
            "date": date,
            "product_id": prod,
            "region": np.random.choice(regions),
            "units_sold": units,
            "revenue": rev,
            "margin": round(margin, 2),
            "profit": round(profit, 2),
            "customer_segment": np.random.choice(["Enterprise", "SMB", "Consumer"]),
            "lead_source": np.random.choice(["Web", "Referral", "Partner"])
        })

pd.DataFrame(sales_data).to_csv("data/synthetic/sales.csv", index=False)
print("Saved data/synthetic/sales.csv")

# 3. Field Data (Incidents)
# Added: resolution_time_hours, customer_satisfaction
severities = ["Low", "Medium", "High", "Critical"]
field_data = []

for _ in range(50):
    field_data.append({
        "incident_id": f"INC-{np.random.randint(1000, 9999)}",
        "date": np.random.choice(dates),
        "product_id": np.random.choice(products),
        "region": np.random.choice(regions),
        "severity": np.random.choice(severities, p=[0.4, 0.3, 0.2, 0.1]),
        "description": np.random.choice([
            "Overheating during charge", "Screen flicker", "Battery drain", 
            "Connectivity loss", "Physical damage on arrival"
        ]),
        "resolution_time_hours": round(np.random.exponential(24), 1),
        "customer_satisfaction": np.random.randint(1, 6) # 1-5 Stars
    })

pd.DataFrame(field_data).to_csv("data/synthetic/field.csv", index=False)
print("Saved data/synthetic/field.csv")

# 4. Users (HR Data)
# Added: department, performance_score, tenure_years
users = [
    {"id": 1, "name": "Alice CEO", "email": "alice@acme.com", "role": "CEO", "department": "Executive", "performance": 5.0, "tenure": 5},
    {"id": 2, "name": "Bob CFO", "email": "bob@acme.com", "role": "CFO", "department": "Finance", "performance": 4.8, "tenure": 4},
    {"id": 3, "name": "Carol COO", "email": "carol@acme.com", "role": "COO", "department": "Operations", "performance": 4.5, "tenure": 7},
    {"id": 4, "name": "Dana HR", "email": "dana@acme.com", "role": "HR", "department": "HR", "performance": 4.9, "tenure": 3},
    {"id": 5, "name": "Eve Sales", "email": "eve@acme.com", "role": "Sales", "department": "Sales", "performance": 4.2, "tenure": 2},
]
# Generate random employees
for i in range(6, 50):
    role = np.random.choice(["Engineer", "Sales Rep", "Technician", "Support"])
    dept = {"Engineer": "R&D", "Sales Rep": "Sales", "Technician": "Operations", "Support": "Service"}[role]
    users.append({
        "id": i,
        "name": f"Employee {i}",
        "email": f"emp{i}@acme.com",
        "role": role,
        "department": dept,
        "performance": round(np.random.normal(3.5, 0.8), 1),
        "tenure": np.random.randint(1, 10)
    })

pd.DataFrame(users).to_csv("data/synthetic/users.csv", index=False)
print("Saved data/synthetic/users.csv")
