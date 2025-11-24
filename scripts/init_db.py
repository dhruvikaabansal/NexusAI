import pandas as pd
import os
import sys

# Add project root to path to import app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, metadata
from sqlalchemy import Table, Column, Integer, String, Float, MetaData

DATA_DIR = "data/synthetic"

def init_db():
    print("Initializing database...")
    
    # Define Tables using SQLAlchemy Core (Database Agnostic)
    metadata.drop_all(engine)
    
    users = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('email', String),
        Column('role', String),
        Column('department', String),
        Column('performance', Float),
        Column('tenure', Integer)
    )
    
    manufacturing = Table('manufacturing', metadata,
        Column('id', Integer, primary_key=True),
        Column('date', String),
        Column('line_id', String),
        Column('throughput', Integer),
        Column('downtime_minutes', Integer),
        Column('defect_rate', Float),
        Column('energy_consumption', Float),
        Column('maintenance_cost', Float),
        Column('shift_id', String)
    )
    
    sales = Table('sales', metadata,
        Column('id', Integer, primary_key=True),
        Column('date', String),
        Column('product_id', String),
        Column('region', String),
        Column('units_sold', Integer),
        Column('revenue', Integer),
        Column('margin', Float),
        Column('profit', Float),
        Column('customer_segment', String),
        Column('lead_source', String)
    )
    
    field = Table('field', metadata,
        Column('id', Integer, primary_key=True),
        Column('incident_id', String),
        Column('date', String),
        Column('product_id', String),
        Column('region', String),
        Column('severity', String),
        Column('description', String),
        Column('resolution_time_hours', Float),
        Column('customer_satisfaction', Integer)
    )
    
    metadata.create_all(engine)
    print("Tables created.")
    
    # Load Data
    load_csv_to_db(engine, "users", f"{DATA_DIR}/users.csv")
    load_csv_to_db(engine, "manufacturing", f"{DATA_DIR}/manufacturing.csv")
    load_csv_to_db(engine, "sales", f"{DATA_DIR}/sales.csv")
    load_csv_to_db(engine, "field", f"{DATA_DIR}/field.csv")
    
    print("Database initialization complete.")

def load_csv_to_db(engine, table_name, csv_path):
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Skipping {table_name}.")
        return
    
    print(f"Loading {table_name} from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Sanitize types for SQLite/SQLAlchemy compatibility
    # Convert numpy types to python types
    object_cols = df.select_dtypes(include=['object']).columns
    for col in object_cols:
        df[col] = df[col].astype(str)
        
    # Drop id if present to let DB handle auto-increment (optional, but safer)
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
        
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} rows into {table_name}.")

if __name__ == "__main__":
    init_db()
