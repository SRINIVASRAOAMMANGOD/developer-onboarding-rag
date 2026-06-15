from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

DATA_DIR = Path("data")
UPLOAD_DIR = DATA_DIR / "uploads"
CHROMA_DIR = DATA_DIR / "chroma"
COLLECTION_NAME = "developer_docs"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
OPENROUTER_MODEL = "google/gemini-2.5-flash-lite"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
