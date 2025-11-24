from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, dashboards, chatbot

app = FastAPI(title="HRCentral API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(dashboards.router, prefix="/dashboards", tags=["Dashboards"])
app.include_router(chatbot.router, prefix="/chat", tags=["Chatbot"])

@app.get("/")
def read_root():
    return {"message": "Welcome to HRCentral API"}
