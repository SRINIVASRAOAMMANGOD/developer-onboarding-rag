import sys
import os
from pathlib import Path

# Set stdout to use utf-8 encoding to avoid Windows console UnicodeEncodeError
if sys.version_info >= (3, 7):
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

import chromadb
from rag.config import CHROMA_DIR, COLLECTION_NAME

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(COLLECTION_NAME)

print(f"Collection: {COLLECTION_NAME}")
print(f"Number of items: {collection.count()}")

results = collection.get(include=["documents", "metadatas"])
documents = results["documents"]
metadatas = results["metadatas"]

source_counts = {}
for meta in metadatas:
    source = meta.get("source") if meta else "None"
    source_counts[source] = source_counts.get(source, 0) + 1

print("\n--- Chunks per Source ---")
for src, count in sorted(source_counts.items()):
    print(f"- {src}: {count} chunks")

print("\n--- Sample Document Previews ---")
for idx in range(min(5, len(documents))):
    print(f"[{idx}] Source: {metadatas[idx].get('source')} | Length: {len(documents[idx])} | Preview: {repr(documents[idx][:120])}")
