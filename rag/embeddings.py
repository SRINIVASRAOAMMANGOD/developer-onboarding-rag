from sentence_transformers import SentenceTransformer

from rag.config import EMBEDDING_MODEL


model = SentenceTransformer(EMBEDDING_MODEL)


def embed(texts: list[str]) -> list[list[float]]:
    return model.encode(texts, normalize_embeddings=True).tolist()
