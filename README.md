# NexusAI (formerly HRCentral)

NexusAI is an intelligent enterprise dashboard for manufacturing. It centralizes data from Manufacturing, Sales, Field, and HR domains, providing tailored dashboards and an AI assistant for different user roles (CEO, CFO, COO, HR).

## Features

- **Role-Aware Dashboards**: Automatically adapts KPIs and charts based on the user's role.
- **AI Chatbot**: 
    - **Local RAG**: Uses `sentence-transformers` for free, private semantic search.
    - **Cloud LLM**: Integrates **Google Gemini** for natural language answers.
    - **Strategic Knowledge**: Can answer qualitative questions about risks and competitors.
- **Enriched Data**: Includes Profit, Energy Consumption, Customer Satisfaction, and Employee Performance.
- **Modern UI**: Built with React, Tailwind CSS, and Recharts (Area, Radar, Scatter, Composed charts).

## Quick Start (Docker)

1.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```
2.  **Access**:
    - Frontend: [http://localhost:5173](http://localhost:5173)
    - Backend API: [http://localhost:8000](http://localhost:8000)
    - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Local Development

### Backend

1.  Navigate to the project root.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Initialize Data:
    ```bash
    python scripts/ingest_synthetic.py
    python scripts/init_db.py
    ```
4.  Run Server:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend

1.  Navigate to `frontend/`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run Dev Server:
    ```bash
    npm run dev
    ```

## Demo Accounts

- **CEO**: `alice@acme.com` (Strategy, Revenue, Risk)
- **CFO**: `bob@acme.com` (Financials, Margins, Costs)
- **COO**: `carol@acme.com` (Throughput, Downtime, Defects)
- **HR**: `dana@acme.com` (Headcount, Training, Safety)

## Architecture

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + SQLite
- **AI**: Sentence-Transformers (Local) / Template-based fallback
