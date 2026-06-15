# Project Specification

## Goal

Build a simple Developer Onboarding Assistant for new software developers.

## Features

- Upload PDF, TXT, and Markdown documents.
- Split documents into chunks.
- Store chunks in ChromaDB.
- Ask questions about indexed documents.
- Generate answers with Gemini 2.5 Flash.
- Return citations from source files.

## Architecture

```text
Streamlit
  |
FastAPI
  |
RAG helpers
  |
ChromaDB + BGE embeddings
  |
Gemini 2.5 Flash
```

## Out Of Scope

- Java
- Spring Boot
- React
- JWT
- PostgreSQL
- Docker
- Ollama
- OCR
- User accounts
