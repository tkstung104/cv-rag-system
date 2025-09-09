"""
Cấu hình cho ứng dụng CV RAG
"""
import os
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()

# Cấu hình OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0

# Cấu hình truy xuất thông tin
VECTOR_RETRIEVER_K = 8
BM25_RETRIEVER_K = 7
HYBRID_WEIGHTS = [0.7, 0.3]  # [trọng_số_vector, trọng_số_bm25]

# Từ khóa các mục trong CV
CV_SECTION_KEYWORDS = [
    "Profile", "Objective", "Education", "Work experience",
    "Skills", "Projects", "Certifications", "Honors & Awards",
    "References", "Activities", "Interests"
]

# Cấu hình Streamlit
PAGE_TITLE = "Ask your CV"
PAGE_ICON = "📄"
