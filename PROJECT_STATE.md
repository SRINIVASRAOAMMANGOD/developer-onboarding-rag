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

## Local URLs

- Streamlit: `http://localhost:8501`
- FastAPI: `http://localhost:8000`

## Environment

Set `OPENROUTER_API_KEY` in `.env`.
