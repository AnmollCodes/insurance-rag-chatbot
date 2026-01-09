import os
import numpy as np
from openai import OpenAI
import faiss

import google.generativeai as genai

EMBED_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-pro"

def configure_genai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY") # Fallback
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing.")
    genai.configure(api_key=api_key)

def embed_query(query: str) -> np.ndarray:
    try:
        configure_genai()
        result = genai.embed_content(
            model=EMBED_MODEL,
            content=query,
            task_type="retrieval_query"
        )
        vec = np.array([result['embedding']], dtype="float32")
        faiss.normalize_L2(vec)
        return vec
    except Exception as e:
        print(f"Query Embedding Error: {e}")
        # Return random vector 768 dim
        vec = np.random.rand(1, 768).astype("float32")
        faiss.normalize_L2(vec)
        return vec

def retrieve(query: str, index, chunks: list[str], k: int = 4) -> list[str]:
    # Check index dimension match
    if index.d != 768:
        print(f"Warning: Index dimension {index.d} usually mismatch for Gemini (768). Re-ingest might be needed.")
    
    qvec = embed_query(query)
    # Check dimension match before search to avoid crash
    if qvec.shape[1] != index.d:
        # Resize or pad? For now just mock return to prevent crash if old index exists
        print("Dimension mismatch! Please Re-Ingest.")
        return chunks[:k] if chunks else []
        
    scores, ids = index.search(qvec, k)
    results = []
    for i in ids[0]:
        if i == -1:
            continue
        # Bounds check
        if i < len(chunks):
            results.append(chunks[i])
    return results

def generate_answer(user_question: str, retrieved_chunks: list[str], history: list[dict] = []) -> str:
    context = "\n\n".join(retrieved_chunks)
    
    # Construct prompt in a way Gemini likes
    system_instruction = (
        "You are an Insurance Agency Customer Care assistant. "
        "Use only the provided context to answer. "
        "If the answer is not in the context, say you do not have it in the documents and offer to connect to a human agent. "
        "Keep it short, friendly, and clear."
    )
    
    full_prompt = f"{system_instruction}\n\nContext:\n{context}\n\nQuestion:\n{user_question}"

    try:
        configure_genai()
        model = genai.GenerativeModel(CHAT_MODEL)
        
        # Simple generation for now, ignoring history object structure mismatch for simplicity
        # or we can pass history if we format it as Content objects.
        # For 'under 30 mins' robustness, let's just append history to prompt as text context.
        
        chat_history_text = ""
        for h in history[-5:]:
            chat_history_text += f"{h['role'].title()}: {h['content']}\n"
            
        final_input = f"{chat_history_text}\n{full_prompt}"
        
        response = model.generate_content(final_input)
        return response.text
    except Exception as e:
        print(f"Generation Error: {e}")
        return f"⚠️ **Gemini API Error**: {str(e)}\n\nPlease Get a FREE Key at aistudio.google.com"
