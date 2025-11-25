# PythonAnywhere WSGI Configuration for NexusAI Backend

import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/NexusAI'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'YOUR_GEMINI_API_KEY_HERE'

# Import FastAPI app
from app.main import app as application

# Initialize database on startup
from scripts.init_db import init_db
init_db()
