import os
import time
import requests

from rag.config import OPENROUTER_MODEL, OPENROUTER_URL
from rag.store import search


def answer_question(question: str) -> dict:
    start = time.time()
    matches = search(question)
    print("Search:", round(time.time() - start, 3), "sec")

    print("\n=== RETRIEVAL DEBUG ===")

    for i, m in enumerate(matches, 1):
        print(f"\nChunk {i}")
        print(f"Source: {m['source']}")
        print(f"Distance: {m['distance']:.4f}")
        print(f"Preview: {m['text'][:200]}")

    if not matches:
        return {"answer": "No indexed documents found.", "sources": []}

    threshold = float(os.getenv("SCORE_THRESHOLD", "1.0"))
    relevant_matches = [m for m in matches if m["distance"] <= threshold]

    if not relevant_matches:
        print(f"\nQuestion: {question}")
        print("=== NO RELEVANT DOCUMENTS FOUND ===")
        print(f"Top match distance: {matches[0]['distance']:.4f} (Threshold: {threshold})")
        return {"answer": "No relevant documents found.", "sources": []}

    context = "\n\n".join(
        f"Source: {m['source']}\n{m['text']}"
        for m in relevant_matches
    )

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {
            "answer": "Set OPENROUTER_API_KEY in your environment first.",
            "sources": [],
        }

    prompt = f"""
You are a helpful assistant.

Answer the question using the provided context.

If the answer is not found in the context, say:
"I do not know based on the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

    start = time.time()

    response = requests.post(
        OPENROUTER_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": os.getenv("OPENROUTER_MODEL", OPENROUTER_MODEL),
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )

    print("LLM:", round(time.time() - start, 3), "sec")

    response.raise_for_status()
    answer = response.json()["choices"][0]["message"]["content"]

    sources = sorted({match["source"] for match in relevant_matches})

    print(question)

    print("\n=== CONTEXT ===")
    print(context)

    print("\n=== SOURCES ===")
    print(sources)

    return {"answer": answer, "sources": sources}