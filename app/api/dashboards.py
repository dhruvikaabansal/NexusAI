@router.get("/{role}")
def get_dashboard_data(role: str):
    role = role.upper()
    conn = get_db_connection()
    
    data = {"role": role, "kpis": [], "charts": [], "actions": []}
    
    try:
        if role == "CEO":
            # CEO: Revenue, Profit, CSAT, Strategy
            sales_df = pd.read_sql("SELECT * FROM sales", conn)
            field_df = pd.read_sql("SELECT * FROM field", conn)
            
            total_revenue = sales_df['revenue'].sum()
            total_profit = sales_df['profit'].sum()
            avg_csat = field_df['customer_satisfaction'].mean()
            
            data["kpis"] = [
                {"label": "Total Revenue", "value": f"${total_revenue:,.0f}", "trend": "+12%"},
                {"label": "Net Profit", "value": f"${total_profit:,.0f}", "trend": "+8%"},
                {"label": "Global CSAT", "value": f"{avg_csat:.1f}/5.0", "trend": "+0.2"},
                {"label": "Market Share", "value": "24%", "trend": "+1.5%"} # Mock
            ]
            
            # Charts: Revenue vs Target (Area), Regional Performance (Radar)
            # Area Chart Data
            sales_df['date'] = pd.to_datetime(sales_df['date'])
            daily_rev = sales_df.groupby('date')['revenue'].sum().reset_index()
            daily_rev['target'] = daily_rev['revenue'] * 1.1 # Mock target
            area_data = daily_rev.tail(14).to_dict('records') # Last 14 days
            
            # Radar Chart Data (Normalize metrics by region)
            # We'll aggregate revenue, profit, and inverse of incidents
            reg_rev = sales_df.groupby('region')['revenue'].sum()
            reg_prof = sales_df.groupby('region')['profit'].sum()
            reg_inc = field_df.groupby('region').size()
            
            radar_data = []
            for region in reg_rev.index:
                radar_data.append({
                    "subject": region,
                    "Revenue": int(reg_rev[region] / reg_rev.max() * 100),
                    "Profit": int(reg_prof[region] / reg_prof.max() * 100),
                    "Efficiency": int((1 - (reg_inc.get(region, 0) / reg_inc.sum())) * 100)
                })
            
            data["charts"] = [
                {"id": "rev_target", "type": "area", "title": "Revenue vs Target (14 Days)", "data": area_data, "x": "date", "keys": ["revenue", "target"], "colors": ["#8884d8", "#82ca9d"]},
                {"id": "reg_perf", "type": "radar", "title": "Regional Performance Matrix", "data": radar_data, "keys": ["Revenue", "Profit", "Efficiency"], "colors": ["#8884d8", "#82ca9d", "#ffc658"]}
            ]

            data["actions"] = [
                {"title": "Approve Q4 Expansion", "priority": "High"},
                {"title": "Review North Region Strategy", "priority": "Medium"},
                {"title": "Investor Briefing Prep", "priority": "High"}
            ]

        elif role == "CFO":
            # CFO: Profitability, Margins, Cost Analysis
            sales_df = pd.read_sql("SELECT * FROM sales", conn)
            mfg_df = pd.read_sql("SELECT * FROM manufacturing", conn)
            
            total_profit = sales_df['profit'].sum()
            avg_margin = sales_df['margin'].mean()
            total_maint_cost = mfg_df['maintenance_cost'].sum()
            
            data["kpis"] = [
                {"label": "Net Profit", "value": f"${total_profit:,.0f}", "trend": "+8%"},
                {"label": "Gross Margin", "value": f"{avg_margin:.1%}", "trend": "+1.2%"},
                {"label": "OpEx (Maint)", "value": f"${total_maint_cost:,.0f}", "trend": "-2%"},
                {"label": "Cash Flow", "value": "$1.2M", "trend": "Stable"}
            ]
            
            # Charts: Profitability Trend (Composed), Cost Breakdown (Pie)
            sales_df['date'] = pd.to_datetime(sales_df['date'])
            daily_fin = sales_df.groupby('date').agg({'revenue': 'sum', 'profit': 'sum'}).reset_index().tail(30)
            daily_fin['margin_pct'] = (daily_fin['profit'] / daily_fin['revenue']) * 100
            composed_data = daily_fin.to_dict('records')
            
            cost_data = [
                {"name": "Maintenance", "value": total_maint_cost},
                {"name": "Energy", "value": mfg_df['energy_consumption'].sum() * 0.12}, # Mock rate
                {"name": "COGS", "value": sales_df['revenue'].sum() - total_profit}
            ]
            
            data["charts"] = [
                {"id": "prof_trend", "type": "composed", "title": "Revenue & Margin Trend", "data": composed_data, "x": "date", "barKey": "revenue", "lineKey": "margin_pct", "colors": ["#8884d8", "#ff7300"]},
                {"id": "cost_breakdown", "type": "pie", "title": "Cost Structure", "data": cost_data, "x": "name", "y": "value", "colors": ["#0088FE", "#00C49F", "#FFBB28"]}
            ]

            data["actions"] = [
                {"title": "Audit Energy Contracts", "priority": "Medium"},
                {"title": "Optimize Inventory Levels", "priority": "High"},
                {"title": "Review Tax Compliance", "priority": "Low"}
            ]

        elif role == "COO":
            # COO: OEE, Energy, Efficiency
            mfg_df = pd.read_sql("SELECT * FROM manufacturing", conn)
            
            avg_throughput = mfg_df['throughput'].mean()
            total_energy = mfg_df['energy_consumption'].sum()
            avg_defect = mfg_df['defect_rate'].mean()
            
            data["kpis"] = [
                {"label": "Avg Throughput", "value": f"{avg_throughput:.0f}", "trend": "+3%"},
                {"label": "Energy Usage", "value": f"{total_energy:,.0f} kWh", "trend": "-1.5%"},
                {"label": "Defect Rate", "value": f"{avg_defect:.2%}", "trend": "-0.2%"},
                {"label": "OEE Score", "value": "87%", "trend": "+2%"} # Mock
            ]
            
            # Charts: Energy vs Output (Scatter), Downtime by Shift (Bar)
            scatter_data = mfg_df[['throughput', 'energy_consumption']].rename(columns={'energy_consumption': 'energy'}).to_dict('records')
            
            shift_dt = mfg_df.groupby('shift_id')['downtime_minutes'].sum().reset_index().to_dict('records')
            
            data["charts"] = [
                {"id": "energy_out", "type": "scatter", "title": "Energy vs Throughput Correlation", "data": scatter_data, "x": "throughput", "y": "energy", "colors": ["#82ca9d"]},
                {"id": "shift_dt", "type": "bar", "title": "Downtime by Shift", "data": shift_dt, "x": "shift_id", "y": "downtime_minutes", "colors": ["#ff8042"]}
            ]

            data["actions"] = [
                {"title": "Investigate Night Shift Downtime", "priority": "High"},
                {"title": "Calibrate Line C Sensors", "priority": "Medium"},
                {"title": "Energy Audit Line A", "priority": "Low"}
            ]

        elif role == "HR":
            # HR: Performance, Tenure, Satisfaction
            users_df = pd.read_sql("SELECT * FROM users", conn)
            
            avg_perf = users_df['performance'].mean()
            avg_tenure = users_df['tenure'].mean()
            headcount = len(users_df)
            
            data["kpis"] = [
                {"label": "Avg Performance", "value": f"{avg_perf:.1f}/5.0", "trend": "+0.1"},
                {"label": "Avg Tenure", "value": f"{avg_tenure:.1f} Yrs", "trend": "Stable"},
                {"label": "Headcount", "value": str(headcount), "trend": "+4"},
                {"label": "eNPS", "value": "42", "trend": "+5"}
            ]
            
            # Charts: Performance Distribution (Bar), Headcount by Dept (Pie)
            # Binning performance
            users_df['perf_bin'] = pd.cut(users_df['performance'], bins=[0, 3, 4, 5], labels=["Needs Imp", "Good", "Excellent"])
            perf_dist = users_df.groupby('perf_bin').size().reset_index(name='count').to_dict('records')
            
            dept_dist = users_df.groupby('department').size().reset_index(name='count').to_dict('records')
            
            data["charts"] = [
                {"id": "perf_dist", "type": "bar", "title": "Performance Distribution", "data": perf_dist, "x": "perf_bin", "y": "count", "colors": ["#8884d8"]},
                {"id": "dept_headcount", "type": "pie", "title": "Headcount by Department", "data": dept_dist, "x": "department", "y": "count", "colors": ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"]}
            ]

            data["actions"] = [
                {"title": "Launch Leadership Training", "priority": "High"},
                {"title": "Review 'Needs Imp' Plans", "priority": "Medium"},
                {"title": "Q4 Hiring Sync", "priority": "Medium"}
            ]
        
        else:
            raise HTTPException(status_code=400, detail="Unknown Role")

    except Exception as e:
        print(f"Error generating dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
        
    return data
