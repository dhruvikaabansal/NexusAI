from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

router = APIRouter()

DB_PATH = "hrcentral.db"

class LoginRequest(BaseModel):
    email: str
    password: str # Ignored for demo

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    role: str

@router.post("/login", response_model=UserResponse)
def login(request: LoginRequest):
    # Demo Login: Accept any email ending in @acme.com
    # In a real app, verify password hash
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (request.email,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    else:
        # Auto-create user if not exists (for demo flexibility) or reject
        # For strict demo, we'll reject if not seeded, but let's allow "guest"
        if request.email.endswith("@acme.com"):
             return {
                "user_id": 999,
                "name": "Guest User",
                "email": request.email,
                "role": "CEO" # Default to CEO for exploration
            }
        
        raise HTTPException(status_code=401, detail="Invalid credentials")
