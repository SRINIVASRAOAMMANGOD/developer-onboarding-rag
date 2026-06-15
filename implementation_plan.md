# RAG Retrieval Fix Implementation Plan

This plan aims to address issues with incorrect chunk retrieval, duplicate chunks, poor chunking quality, and incorrect responses to high-level document-summary questions.

## User Review Required

> [!IMPORTANT]
> **Database Reset Required**:
> To clear existing duplicates and apply the new `chunk_index` metadata format, we will reset the ChromaDB database collection during the execution phase. All uploaded documents will need to be re-indexed (which can be done via the UI or a script).

> [!NOTE]
> **Minimal UI Design Changes**:
> As per the rules, we will not touch the Streamlit UI design. All changes will be limited to backend RAG retrieval logic (`rag/` modules) and logging/printing retrieval debugging details to standard output (terminal).

## Open Questions

None. The requirements are clear, and the proposed changes directly resolve the observed retrieval quality issues.

---

## Proposed Changes

### RAG Core Modules

#### [MODIFY] [embeddings.py](file:///c:/Users/HP/Desktop/Engineering%20Intelligence%20Hub/rag/embeddings.py)
- Pass `local_files_only=True` to `SentenceTransformer` constructor. This fixes the offline load failure (`[Errno 11001] getaddrinfo failed`) by ensuring the model is loaded purely from local cache.

#### [MODIFY] [documents.py](file:///c:/Users/HP/Desktop/Engineering%20Intelligence%20Hub/rag/documents.py)
- Improve `split_text` to split on word/space boundaries instead of character slicing. This prevents cutting words in half and increases chunk readability.

#### [MODIFY] [store.py](file:///c:/Users/HP/Desktop/Engineering%20Intelligence%20Hub/rag/store.py)
- Set collection distance metric to `cosine` using metadata `{"hnsw:space": "cosine"}`.
- Implement a deduplication helper `delete_document(doc_name)` that removes any existing chunks for a document before inserting new ones.
- Add `chunk_index` to metadata when chunking in `add_documents`.

#### [MODIFY] [chain.py](file:///c:/Users/HP/Desktop/Engineering%20Intelligence%20Hub/rag/chain.py)
- Add retrieval debugging to print retrieved chunks, distance scores, and sources to standard output.
- Add `is_summary_query(question)` helper to detect high-level summary/overview queries.
- Add a specialized retrieval logic `get_summary_context(question)` for summary queries that fetches introductory chunks (first 2-3 chunks) of document(s) instead of relying on standard semantic search.

---

## Verification Plan

### Automated / Semi-Automated Verification
We will run custom scripts to:
1. Verify document ingestion and check that duplicate chunks are not created upon re-uploading.
2. Run sample queries (e.g. "What's the PDF about?", "Summarize NBayesLogReg.pdf") and inspect printed debug outputs (chunks, distance scores, sources).

### Manual Verification
1. Run the FastAPI backend and Streamlit frontend.
2. Upload `NBayesLogReg.pdf` and `RAG_Learning_Journey_Carousel.pdf`.
3. Ask "What's the PDF about?" and confirm the answer is generated from the introduction/overview chunks of the documents.
