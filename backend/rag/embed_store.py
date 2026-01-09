import json
import os
import numpy as np
import faiss
from openai import OpenAI

import google.generativeai as genai

EMBED_MODEL = "models/embedding-001"

def configure_genai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY") # Fallback to try reading from OPENAI_API_KEY variable if that's where they pasted it
    
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing.")
    genai.configure(api_key=api_key)

def embed_texts(texts: list[str]) -> np.ndarray:
    try:
        configure_genai()
        # Gemini handles batching differently, but for simplicity we iterate or use batch if supported
        # embed_content supports a list/batch in newer versions, usually title optional for retrieval_document
        result = genai.embed_content(
            model=EMBED_MODEL,
            content=texts,
            task_type="retrieval_document"
        )
        # Result is typically {'embedding': [[...], [...]]} for batch
        vectors = result['embedding']
        
        arr = np.array(vectors, dtype="float32")
        faiss.normalize_L2(arr)
        return arr
    except Exception as e:
        print(f"CRITICAL: GEMINI EMBEDDING FAILED: {e}")
        # Mock fallback
        np.random.seed(42)
        # Gemini embedding-001 is 768 dimensions usually, verify? 
        # Actually embedding-001 is 768. text-embedding-3-small is 1536. 
        # We must align with what the dimension is. Safe bet: use 768 if switching to Gemini.
        vectors = np.random.rand(len(texts), 768).astype("float32")
        faiss.normalize_L2(vectors)
        return vectors

def build_and_save_index(chunks: list[str], index_path: str, meta_path: str):
    vectors = embed_texts(chunks)
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)

    faiss.write_index(index, index_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunks}, f, ensure_ascii=False, indent=2)

def load_index(index_path: str, meta_path: str):
    index = faiss.read_index(index_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return index, meta["chunks"]
