# Next Steps

## 1. Connect Real LLM
To replace the template-based chatbot with a real LLM (OpenAI/Anthropic/HF):
1.  Obtain an API Key (e.g., `OPENAI_API_KEY`).
2.  Update `app/api/chatbot.py`:
    - Import an LLM client (e.g., `openai`).
    - In the `chat` function, instead of `get_role_template`, construct a prompt with the retrieved data rows and send it to the LLM.
    - Example Prompt:
      ```text
      System: You are an assistant for the {role}.
      Context: Here is the recent data: {data_rows}
      User: {query}
      ```

## 2. Real Data Ingestion
To use real data instead of synthetic CSVs:
1.  Replace `scripts/ingest_synthetic.py` with ETL scripts that connect to your ERP/CRM/HRIS.
2.  Update `scripts/init_db.py` to match your actual schema.
3.  Ensure the `dashboards.py` queries match the new schema.

## 3. Advanced Retrieval (RAG)
1.  Uncomment the code in `models/retrieval.py`.
2.  Install `faiss-cpu` and `sentence-transformers`.
3.  Generate embeddings for your data rows and save them to a FAISS index.
4.  In `chatbot.py`, use `Retriever.search(query)` to find the most relevant rows before generating the answer.

## 4. Authentication
1.  Replace the mock `auth.py` with real Firebase Admin SDK verification or OAuth2 flow.
2.  Enforce role-based access control (RBAC) on API endpoints using `Depends`.
