import uuid

import chromadb

from rag.config import CHROMA_DIR, COLLECTION_NAME
from rag.documents import split_text
from rag.embeddings import embed


client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(COLLECTION_NAME)


def add_documents(docs: list[dict]) -> int:
    chunks, metadatas = [], []
    for doc in docs:
        for chunk in split_text(doc["text"]):
            chunks.append(chunk)
            metadatas.append({"source": doc["source"]})

    if not chunks:
        return 0

    collection.add(
        ids=[str(uuid.uuid4()) for _ in chunks],
        documents=chunks,
        embeddings=embed(chunks),
        metadatas=metadatas,
    )
    return len(chunks)


def search(question: str, limit: int = 4) -> list[dict]:
    result = collection.query(
        query_embeddings=embed([question]),
        n_results=limit,
        include=["documents", "metadatas", "distances"],
    )
    documents = result["documents"][0] if result["documents"] else []
    metadatas = result["metadatas"][0] if result["metadatas"] else []
    distances = result["distances"][0] if result["distances"] else []
    return [
        {"text": text, "source": meta["source"], "distance": dist}
        for text, meta, dist in zip(documents, metadatas, distances)
    ]
