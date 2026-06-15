import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from sentence_transformers import SentenceTransformer
from rag.config import EMBEDDING_MODEL

try:
    print("Attempting to load model with local_files_only=True...")
    model = SentenceTransformer(EMBEDDING_MODEL, local_files_only=True)
    print("Success! Model loaded.")
except Exception as e:
    print(f"Error loading model: {e}")
