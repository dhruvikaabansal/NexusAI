"""
Vercel Serverless Function Entry Point
This wraps the FastAPI app for Vercel's serverless environment
"""
from app.main import app

# Vercel expects a handler
handler = app
