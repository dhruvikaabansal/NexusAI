import pandas as pd
from app.database import engine
import os

DATA_DIR = "data/synthetic"

def debug():
    csv_path = f"{DATA_DIR}/users.csv"
    print(f"Reading {csv_path}...")
    df = pd.read_csv(csv_path)
    print("Data Types:")
    print(df.dtypes)
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nAttempting to insert into users table...")
    try:
        df.to_sql('users', engine, if_exists='append', index=False)
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug()
