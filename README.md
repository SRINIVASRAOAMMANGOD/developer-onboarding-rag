# Developer Onboarding Assistant

A lightweight Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions grounded in those documents.

The project was built to learn and understand the complete RAG pipeline through hands-on implementation using FastAPI, Streamlit, ChromaDB, Embedding APIs, and OpenRouter.

---

# Features

* Upload PDF, TXT, and Markdown files
* Automatic text extraction
* Recursive document chunking
* Embedding generation via Embedding API
* ChromaDB vector storage
* Semantic search retrieval
* LLM-powered question answering via OpenRouter
* Source citations
* Duplicate document prevention
* Retrieval debugging
* Hallucination prevention
* Latency measurement

---

# Architecture

```text
User Question
      ↓
Embedding API
      ↓
Semantic Search (ChromaDB)
      ↓
Relevant Chunks Retrieved
      ↓
Context Creation
      ↓
OpenRouter LLM
      ↓
Final Answer + Sources
```

---

# Tech Stack

## Backend

* FastAPI

## Frontend

* Streamlit

## Vector Database

* ChromaDB

## Embeddings

* Embedding API (OpenAI/OpenRouter Compatible)

## LLM

* OpenRouter

## PDF Processing

* PyPDF

## Chunking

* LangChain RecursiveCharacterTextSplitter

---

# Project Structure

```text
Developer Onboarding Assistant/
│
├── api.py
├── app.py
├── requirements.txt
├── .env
│
├── data/
│   ├── uploads/
│   └── chroma/
│
└── rag/
    ├── chain.py
    ├── documents.py
    ├── embeddings.py
    ├── store.py
    └── config.py
```

---

# File Responsibilities

## api.py

FastAPI backend.

Responsibilities:

* File upload endpoint
* Question answering endpoint
* Health check endpoint

### Interactive API Documentation Routes

* **Swagger UI** (interactive documentation to test the endpoints directly from the browser):
  - URL: `http://localhost:8000/docs`
* **ReDoc** (clean, responsive 3-column API specification documentation):
  - URL: `http://localhost:8000/redoc`
* **OpenAPI Schema** (the raw OpenAPI spec in JSON format):
  - URL: `http://localhost:8000/openapi.json`

### API Endpoints

* **`GET /`**
  - **Description**: Welcome health check message confirming the API is running.
  - **Response**: `{"message": "Developer Onboarding Assistant API Running"}`

* **`GET /health`**
  - **Description**: Backend service health status check.
  - **Response**: `{"status": "ok"}`

* **`POST /upload`**
  - **Description**: Upload a PDF, TXT, or Markdown document. It parses, chunks, generates embeddings, and indexes the document in the vector store.
  - **Request**: Multipart Form Data with `file` field.
  - **Response**: `{"filename": "document.pdf", "chunks": 12, "message": "indexed"}`

* **`POST /ask`**
  - **Description**: Answer questions based on the uploaded documents using search and LLM context.
  - **Request Body**:
    ```json
    {
      "question": "What is RAG?"
    }
    ```
  - **Response**:
    ```json
    {
      "answer": "RAG stands for...",
      "sources": ["document.pdf, page 1"]
    }
    ```

---

## app.py

Streamlit frontend.

Responsibilities:

* Upload files
* Ask questions
* Display answers
* Display sources

---

## rag/config.py

Stores application configuration.

Examples:

* OpenRouter URL
* OpenRouter model
* Upload directory
* Chroma directory
* Score threshold

---

## rag/documents.py

Handles document loading and chunking.

Responsibilities:

* PDF text extraction
* TXT loading
* Markdown loading
* Chunk generation

Uses:

```python
RecursiveCharacterTextSplitter
```

instead of manual character slicing.

---

## rag/embeddings.py

Generates embeddings.

Responsibilities:

```text
Text
 ↓
Embedding API
 ↓
Embedding Vector
```

Benefits:

* No local embedding model
* Lower memory usage
* Faster deployment
* Better cloud compatibility

---

## rag/store.py

Handles ChromaDB operations.

Responsibilities:

* Store chunks
* Store embeddings
* Semantic search
* Duplicate prevention

Functions:

* add_documents()
* search()

---

## rag/chain.py

Core RAG pipeline.

Responsibilities:

```text
Question
 ↓
Retrieve Chunks
 ↓
Build Context
 ↓
Call OpenRouter
 ↓
Return Answer
```

This is the main orchestration layer.

---

# RAG Workflow

## 1. Upload Document

```text
PDF
 ↓
Extract Text
 ↓
Split Into Chunks
 ↓
Generate Embeddings
 ↓
Store In ChromaDB
```

---

## 2. Ask Question

```text
Question
 ↓
Question Embedding
 ↓
Vector Search
 ↓
Relevant Chunks
 ↓
Prompt Construction
 ↓
LLM
 ↓
Answer
```

---

# Problems Encountered & Solutions

## Problem 1: Poor Chunking

### Issue

Initial implementation used manual character slicing.

```python
text[start:start+size]
```

Problems:

* Words cut in half
* Context broken
* Poor retrieval quality

### Solution

Replaced with:

```python
RecursiveCharacterTextSplitter
```

### Benefits

* Better chunk boundaries
* Preserves context
* Improved retrieval quality

---

## Problem 2: Duplicate Indexing

### Issue

Uploading the same PDF multiple times created duplicate chunks.

Example:

```text
Page 1
Page 1
Page 2
Page 2
```

appeared during retrieval.

### Solution

Before indexing:

```python
collection.delete(
    where={"source": doc["source"]}
)
```

Then reinsert fresh chunks.

### Result

No duplicate chunks.

---

## Problem 3: Retrieval Quality Debugging

### Issue

Could not determine why answers were incorrect.

### Solution

Added retrieval debugging.

Example:

```python
print(source)
print(distance)
print(chunk_preview)
```

### Benefits

* Inspect retrieved chunks
* Verify semantic search
* Debug incorrect answers

---

## Problem 4: Deployment Memory Limit

### Issue

Render Free Tier provides:

```text
512 MB RAM
```

The SentenceTransformer model and Torch dependencies exceeded the available memory during startup.

Result:

```text
Out of memory (used over 512Mi)
```

### Solution

Replaced local embedding generation with an Embedding API.

Before:

```text
Document
 ↓
SentenceTransformer
 ↓
Embeddings
```

After:

```text
Document
 ↓
Embedding API
 ↓
Embeddings
```

### Benefits

* Lower RAM usage
* Faster startup
* Easier deployment on free hosting platforms
* No local model downloads

---

# Performance Measurements

Measured Latency:

```text
Search: 0.07 sec
LLM: 3.466 sec
```

Observation:

```text
Retrieval ≈ 2%
LLM ≈ 98%
```

Conclusion:

The primary latency comes from the LLM, not ChromaDB.

---

# Hallucination Prevention

Prompt includes:

```text
If the answer is not found in the context,
say:

"I do not know based on the uploaded documents."
```

Example:

Question:

```text
What is AI?
```

Answer:

```text
I do not know based on the uploaded documents.
```

This prevents unsupported answers.

---

# Current Status

## P1 — Incorrect Answers (Solved)

### Recursive Chunking

Replaced manual chunking with `RecursiveCharacterTextSplitter` to preserve context and improve retrieval quality.

### Retrieval Debugging

Logged retrieved chunks, similarity scores, and sources to identify why incorrect answers were returned.

### Duplicate Prevention

Removed duplicate vectors/chunks that were polluting retrieval results.

### Chroma Reset

Reset collections during uploads to prevent old documents from contaminating new searches.

### Retrieval Testing

Tested different queries and analyzed retrieved context before changing prompts or models.

### Hallucination Prevention

Added `SCORE_THRESHOLD` filtering so low-confidence retrievals return "I don't know" instead of generating incorrect answers.

---

## P2 — Latency (Solved)

### Search Timing

Measured vector search latency separately.

### LLM Timing

Measured OpenRouter response generation time separately.

### Bottleneck Identification

Identified that most delay came from LLM inference rather than ChromaDB retrieval, helping focus optimization efforts on the right component.

---


## P3 — UI

In Progress

Planned:

* Upload summary card
* Document statistics
* Automatic document summaries
* Better source display

---

# Future Improvements

* Summary query handling
* Metadata filtering
* Page-level retrieval
* Reranking
* Hybrid search
* Embedding caching
* Query expansion
* Streaming responses
* Multi-user support
* Authentication
* Document deletion API
* Cloud vector database deployment

---

# How to Run Locally

Follow these steps to run the backend API and frontend UI locally.

## 1. Setup Virtual Environment and Install Dependencies

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=google/gemini-2.5-flash-lite
SCORE_THRESHOLD=1.0
```

## 3. Run the FastAPI Backend

Run the FastAPI application using Uvicorn:

```bash
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

The API will be available at `http://localhost:8000`.

## 4. Run the Streamlit Frontend

Run the Streamlit frontend:

```bash
streamlit run app.py
```

The Streamlit UI will be available at `http://localhost:8501`.

---

# Deployment

## Frontend

Streamlit Cloud

## Backend

FastAPI

## Environment Variables

```env
OPENROUTER_API_KEY=
OPENROUTER_MODEL=
SCORE_THRESHOLD=
```

---

# Learning Outcomes

Through this project I learned:

* RAG architecture
* Embeddings
* Vector databases
* ChromaDB
* Semantic search
* Chunking strategies
* Retrieval debugging
* Prompt grounding
* OpenRouter integration
* FastAPI
* Streamlit
* End-to-end RAG system design

---

# Live Demo

Frontend:

https://engineering-intelligence-rag.streamlit.app/

---

# Key Takeaway

This project demonstrates a complete end-to-end RAG pipeline, from document ingestion and vector storage to semantic retrieval and grounded answer generation, while addressing real-world challenges such as chunking quality, duplicate indexing, hallucination prevention, deployment constraints, and performance analysis.
