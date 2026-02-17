import os
from dotenv import load_dotenv


load_dotenv()


# تنظیمات LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# اگر کلید OpenAI ندارید، می‌توانید از مدل محلی استفاده کنید
USE_LOCAL_LLM = True  # اگر کلید ندارید True بگذارید


# تنظیمات پایگاه داده برداری
CHROMA_PERSIST_DIR = "./chroma_data"
COLLECTION_NAME = "user_realities"


# تنظیمات مدل embedding
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # مدل چندزبانه خوب


# تنظیمات بازیابی
TOP_K_RESULTS = 3
SIMILARITY_THRESHOLD = 0.6