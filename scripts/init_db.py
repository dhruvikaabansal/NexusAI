import sqlite3
import pandas as pd
import os

DB_PATH = "hrcentral.db"
DATA_DIR = "data/synthetic"

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Tables
    create_tables(cursor)
    
    load_csv_to_db(conn, "users", f"{DATA_DIR}/users.csv")
    load_csv_to_db(conn, "manufacturing", f"{DATA_DIR}/manufacturing.csv")
    load_csv_to_db(conn, "sales", f"{DATA_DIR}/sales.csv")
    load_csv_to_db(conn, "field", f"{DATA_DIR}/field.csv")
    
    conn.commit()
    conn.close()
    print("Database initialization complete.")

def create_tables(cursor):
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            role TEXT,
            department TEXT,
            performance REAL,
            tenure INTEGER
        )
    ''')
    
    # Manufacturing Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manufacturing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            line_id TEXT,
            throughput INTEGER,
            downtime_minutes INTEGER,
            defect_rate REAL,
            energy_consumption REAL,
            maintenance_cost REAL,
            shift_id TEXT
        )
    ''')
    
    # Sales Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            product_id TEXT,
            region TEXT,
            units_sold INTEGER,
            revenue INTEGER,
            margin REAL,
            profit REAL,
            customer_segment TEXT,
            lead_source TEXT
        )
    ''')
    
    # Field Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS field (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id TEXT,
            date TEXT,
            product_id TEXT,
            region TEXT,
            severity TEXT,
            description TEXT,
            resolution_time_hours REAL,
            customer_satisfaction INTEGER
        )
    ''')

def load_csv_to_db(conn, table_name, csv_path):
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Skipping {table_name}.")
        return
    
    print(f"Loading {table_name} from {csv_path}...")
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    print(f"Loaded {len(df)} rows into {table_name}.")

if __name__ == "__main__":
    init_db()
