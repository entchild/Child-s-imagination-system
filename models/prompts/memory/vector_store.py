import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

class RealityMemory:
    """
    ذخیره‌سازی و بازیابی "واقعیت‌های" کاربر در ChromaDB
    """
    def __init__(self, persist_directory: str, collection_name: str):
        # راه‌اندازی کلاینت ChromaDB
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # ایجاد یا دریافت collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # استفاده از شباهت کسینوسی
        )
        
        print(f"✅ پایگاه داده در {persist_directory} راه‌اندازی شد.")
    
    def add_reality(self, 
                    user_id: str, 
                    text: str, 
                    embedding: List[float], 
                    analysis: Dict[str, Any]):
        """
        ذخیره یک "واقعیت" جدید در پایگاه داده
        """
        # ایجاد یک شناسه یکتا
        doc_id = f"{user_id}_{datetime.now().timestamp()}"
        
        # متادیتا: اطلاعات همراه بردار
        metadata = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "emotional_state": analysis.get("emotional_state", "unknown"),
            "beliefs": json.dumps(analysis.get("beliefs", [])),  # JSON string
            "cognitive_needs": analysis.get("cognitive_needs", "unknown"),
            "text_sample": text[:100]  # بخشی از متن برای نمایش
        }
        
        # اضافه کردن به ChromaDB
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        print(f"✅ واقعیت جدید برای کاربر {user_id} ذخیره شد.")
        return doc_id
    
    def search_similar_realities(self, 
                                  query_embedding: List[float], 
                                  user_id: Optional[str] = None,
                                  n_results: int = 3) -> List[Dict]:
        """
        جستجوی واقعیت‌های مشابه
        """
        # فیلتر بر اساس user_id اگر داده شده باشد
        where_filter = {"user_id": user_id} if user_id else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        # تبدیل نتایج به فرمت مناسب
        formatted_results = []
        if results['ids'][0]:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if results['distances'] else None
                })
        
        return formatted_results
    
    def get_user_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        دریافت تاریخچه واقعیت‌های یک کاربر
        """
        results = self.collection.get(
            where={"user_id": user_id},
            limit=limit
        )
        
        history = []
        if results['ids']:
            for i in range(len(results['ids'])):
                history.append({
                    'id': results['ids'][i],
                    'text': results['documents'][i],
                    'metadata': results['metadatas'][i]
                })
        
        return history
