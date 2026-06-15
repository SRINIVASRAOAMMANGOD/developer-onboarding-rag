# Project State

## Current Status

Converted to a simple Python-only RAG app.

## Implemented

- Streamlit upload and question UI
- FastAPI `/upload`, `/ask`, and `/health`
- PDF/TXT/Markdown loading
- Text chunking
- BGE embeddings
- ChromaDB persistence
- OpenRouter chat answers
- Model switching through `.env`
- Source citations
- Similarity search score threshold check (`SCORE_THRESHOLD` in `.env`)
- Removed OpenSpec workflows, skills, and configurations (`openspec/`, `.agent/`, `.codex/`, `.opencode/`, `structure.txt`)

## Local URLs

- Streamlit: `http://localhost:8501`
- FastAPI: `http://localhost:8000`

## Environment

Set `OPENROUTER_API_KEY` and `SCORE_THRESHOLD` in `.env`.

