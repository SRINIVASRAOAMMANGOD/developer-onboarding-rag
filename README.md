# Engineering Intelligence Hub

A lightweight RAG-powered Developer Onboarding Assistant.

New developers can upload project documents and ask questions. The app answers using the uploaded docs and shows citations.

## Stack

- Streamlit frontend
- FastAPI REST API
- ChromaDB vector store
- `BAAI/bge-small-en-v1.5` embeddings
- OpenRouter API
- Gemini through OpenRouter

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your OpenRouter key to `.env`.

Start the API:

```bash
uvicorn api:app --reload --port 8000
```

Start the UI in another terminal:

```bash
streamlit run app.py
```

## Use

1. Upload a PDF, TXT, or Markdown file.
2. Click `Index document`.
3. Ask a question.
4. Read the answer and citations.

## Notes

- PDFs must contain selectable text.
- Uploaded files are stored in `data/uploads`.
- ChromaDB data is stored in `data/chroma`.
- Switch models by changing `OPENROUTER_MODEL` in `.env`.
