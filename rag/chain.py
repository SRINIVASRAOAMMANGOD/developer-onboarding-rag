import os

import requests

from rag.config import OPENROUTER_MODEL, OPENROUTER_URL
from rag.store import search


def answer_question(question: str) -> dict:
    matches = search(question)
    context = "\n\n".join(f"Source: {m['source']}\n{m['text']}" for m in matches)

    if not matches:
        return {"answer": "No indexed documents found.", "sources": []}

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"answer": "Set OPENROUTER_API_KEY in your environment first.", "sources": []}

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
    response = requests.post(
        OPENROUTER_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": os.getenv("OPENROUTER_MODEL", OPENROUTER_MODEL),
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    response.raise_for_status()
    answer = response.json()["choices"][0]["message"]["content"]

    sources = sorted({match["source"] for match in matches})

    print(question)

    print("\n=== CONTEXT ===")
    print(context)

    print("\n=== SOURCES ===")
    print(sources)

    return {"answer": answer, "sources": sources}