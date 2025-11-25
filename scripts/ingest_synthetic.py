import pandas as pd
import numpy as np
import os

# Ensure directory exists
os.makedirs("data/synthetic", exist_ok=True)

np.random.seed(42)

# 1. Manufacturing Data - EXPANDED
# Increased from 90 days to 180 days, 4 lines, 3 shifts = 2160 records
dates = pd.date_range(start="2023-06-01", periods=180, freq="D")
lines = ["Line_A", "Line_B", "Line_C", "Line_D"]
shifts = ["Morning", "Evening", "Night"]
mfg_data = []

for date in dates:
    for line in lines:
        for shift in shifts:
            # Realistic patterns: Night shift has more downtime, Line_C is older
            base_throughput = 1000
            if shift == "Night": base_throughput *= 0.95
            if line == "Line_C": base_throughput *= 0.90
            
            throughput = int(np.random.normal(base_throughput, 80))
            downtime = int(np.random.exponential(15) if np.random.rand() > 0.7 else 0)
            if line == "Line_C": downtime = int(downtime * 1.5)  # Older line
            
            defect_rate = np.random.beta(2, 50)
            energy = throughput * 0.5 + np.random.normal(50, 5)
            maint_cost = downtime * 50 + np.random.normal(100, 20)
            
            mfg_data.append({
                "date": date,
                "line_id": line,
                "throughput": throughput,
                "downtime_minutes": downtime,
                "defect_rate": round(defect_rate, 4),
                "energy_consumption": round(energy, 2),
                "maintenance_cost": round(maint_cost, 2),
                "shift_id": shift
            })

pd.DataFrame(mfg_data).to_csv("data/synthetic/manufacturing.csv", index=False)
print(f"Saved data/synthetic/manufacturing.csv ({len(mfg_data)} records)")

# 2. Sales Data - EXPANDED
# 6 products, 4 regions, 180 days, 8 sales/day = 1440 records
products = ["Gadget_X", "Gadget_Y", "Gadget_Z", "Widget_A", "Widget_B", "Device_Pro"]
regions = ["North", "South", "East", "West"]
segments = ["Enterprise", "SMB", "Consumer"]
lead_sources = ["Web", "Referral", "Partner", "Direct", "Marketing"]

# Product pricing and margins
product_info = {
    "Gadget_X": {"price": 50, "margin_range": (0.35, 0.45)},
    "Gadget_Y": {"price": 150, "margin_range": (0.25, 0.35)},
    "Gadget_Z": {"price": 300, "margin_range": (0.38, 0.48)},
    "Widget_A": {"price": 80, "margin_range": (0.30, 0.40)},
    "Widget_B": {"price": 200, "margin_range": (0.28, 0.38)},
    "Device_Pro": {"price": 500, "margin_range": (0.40, 0.50)}
}

sales_data = []
for date in dates:
    for _ in range(8):  # 8 sales per day
        prod = np.random.choice(products)
        info = product_info[prod]
        units = np.random.randint(5, 150)
        price = info["price"]
        rev = units * price
        margin = np.random.uniform(*info["margin_range"])
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
            "customer_segment": np.random.choice(segments, p=[0.3, 0.4, 0.3]),
            "lead_source": np.random.choice(lead_sources)
        })

pd.DataFrame(sales_data).to_csv("data/synthetic/sales.csv", index=False)
print(f"Saved data/synthetic/sales.csv ({len(sales_data)} records)")

# 3. Field Data (Incidents) - EXPANDED
# Increased from 50 to 200 incidents with more variety
severities = ["Low", "Medium", "High", "Critical"]
incident_types = [
    "Overheating during charge", "Screen flicker", "Battery drain", 
    "Connectivity loss", "Physical damage on arrival", "Software crash",
    "Button malfunction", "Audio distortion", "Camera failure",
    "Charging port issue", "Water damage", "Performance lag"
]

field_data = []
for _ in range(200):
    severity = np.random.choice(severities, p=[0.4, 0.3, 0.2, 0.1])
    # Resolution time varies by severity
    if severity == "Critical":
        res_time = np.random.uniform(48, 120)
        csat = np.random.randint(1, 4)  # Lower satisfaction for critical
    elif severity == "High":
        res_time = np.random.uniform(24, 72)
        csat = np.random.randint(2, 5)
    elif severity == "Medium":
        res_time = np.random.uniform(8, 48)
        csat = np.random.randint(3, 6)
    else:
        res_time = np.random.uniform(2, 24)
        csat = np.random.randint(4, 6)
    
    field_data.append({
        "incident_id": f"INC-{np.random.randint(10000, 99999)}",
        "date": np.random.choice(dates),
        "product_id": np.random.choice(products),
        "region": np.random.choice(regions),
        "severity": severity,
        "description": np.random.choice(incident_types),
        "resolution_time_hours": round(res_time, 1),
        "customer_satisfaction": csat
    })

pd.DataFrame(field_data).to_csv("data/synthetic/field.csv", index=False)
print(f"Saved data/synthetic/field.csv ({len(field_data)} records)")

# 4. Users (HR Data) - EXPANDED
# Increased from 49 to 100 employees with more departments
departments = ["Executive", "Finance", "Operations", "HR", "Sales", "R&D", "Service", "Marketing", "IT"]
roles_by_dept = {
    "Executive": ["CEO", "CFO", "COO", "CTO"],
    "Finance": ["Accountant", "Financial Analyst", "Controller"],
    "Operations": ["Operations Manager", "Technician", "Quality Inspector"],
    "HR": ["HR Manager", "Recruiter", "Training Specialist"],
    "Sales": ["Sales Rep", "Account Manager", "Sales Engineer"],
    "R&D": ["Engineer", "Researcher", "Product Manager"],
    "Service": ["Support Specialist", "Field Technician"],
    "Marketing": ["Marketing Manager", "Content Creator", "SEO Specialist"],
    "IT": ["System Admin", "Developer", "Security Analyst"]
}

users = [
    {"id": 1, "name": "Alice CEO", "email": "alice@acme.com", "role": "CEO", "department": "Executive", "performance": 5.0, "tenure": 8},
    {"id": 2, "name": "Bob CFO", "email": "bob@acme.com", "role": "CFO", "department": "Finance", "performance": 4.8, "tenure": 6},
    {"id": 3, "name": "Carol COO", "email": "carol@acme.com", "role": "COO", "department": "Operations", "performance": 4.7, "tenure": 7},
    {"id": 4, "name": "Dana HR", "email": "dana@acme.com", "role": "HR", "department": "HR", "performance": 4.9, "tenure": 5},
]

# Generate 96 more employees
for i in range(5, 101):
    dept = np.random.choice(list(roles_by_dept.keys()), p=[0.04, 0.08, 0.15, 0.06, 0.20, 0.25, 0.10, 0.08, 0.04])
    role = np.random.choice(roles_by_dept[dept])
    
    # Performance distribution: mostly good, some excellent, few poor
    perf = np.clip(np.random.normal(3.8, 0.7), 1.0, 5.0)
    tenure = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=[0.15, 0.15, 0.15, 0.12, 0.12, 0.10, 0.08, 0.06, 0.04, 0.03])
    
    users.append({
        "id": i,
        "name": f"{role.replace(' ', '')} {i}",
        "email": f"emp{i}@acme.com",
        "role": role,
        "department": dept,
        "performance": round(perf, 1),
        "tenure": tenure
    })

pd.DataFrame(users).to_csv("data/synthetic/users.csv", index=False)
print(f"Saved data/synthetic/users.csv ({len(users)} records)")

print(f"\n✅ Total records generated: {len(mfg_data) + len(sales_data) + len(field_data) + len(users)}")
