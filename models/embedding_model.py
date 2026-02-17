from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class PersianEmbeddingModel:
    """
    مدل تبدیل متن فارسی به بردار (embedding)
    """
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        print(f"در حال بارگذاری مدل {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("مدل با موفقیت بارگذاری شد.")
    
    def encode(self, text: str) -> List[float]:
        """
        تبدیل یک متن به بردار
        """
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        تبدیل چند متن به بردار
        """
        embeddings = self.model.encode(texts)
        return [emb.tolist() for emb in embeddings]
