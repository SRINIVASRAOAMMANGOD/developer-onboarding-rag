import os
import requests


def embed(texts: list[str]) -> list[list[float]]:
    api_key = os.getenv("OPENROUTER_API_KEY")

    response = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "model": "text-embedding-3-small",
            "input": texts
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()["data"]

    embeddings = []

    for item in data:
        embeddings.append(item["embedding"])

    return embeddings