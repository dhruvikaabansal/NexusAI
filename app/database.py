import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Default to SQLite for local dev, use DATABASE_URL for prod
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hrcentral.db")

# Fix for Render's Postgres URL (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

def get_db_connection():
    """Returns a raw connection for pandas read_sql"""
    return engine.connect()
