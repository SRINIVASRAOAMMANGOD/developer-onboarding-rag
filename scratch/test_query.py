import sys
from pathlib import Path

# Set stdout to use utf-8 encoding
if sys.version_info >= (3, 7):
    sys.stdout.reconfigure(encoding='utf-8')

# Dynamically patch SentenceTransformer before importing rag modules
import sentence_transformers
original_init = sentence_transformers.SentenceTransformer.__init__

def patched_init(self, *args, **kwargs):
    kwargs["local_files_only"] = True
    original_init(self, *args, **kwargs)

sentence_transformers.SentenceTransformer.__init__ = patched_init

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from rag.store import search

# Run a test query
question = "What's the PDF about?"
matches = search(question, limit=5)

print(f"Query: {question}")
print("--- Search Results ---")
for idx, match in enumerate(matches):
    print(f"[{idx}] Source: {match['source']}")
    print(f"    Distance: {match['distance']:.4f}")
    print(f"    Text: {repr(match['text'][:200])}")
    print("-" * 40)
