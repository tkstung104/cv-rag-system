# CV RAG - Hệ thống Hỏi Đáp CV thông minh

Ứng dụng Streamlit sử dụng RAG (Retrieval-Augmented Generation) để phân tích và trả lời câu hỏi về CV.

## 🚀 Tính năng

- **Upload CV PDF**: Hỗ trợ upload nhiều file CV cùng lúc
- **Xử lý thông minh**: Tự động tách CV thành các mục (Education, Skills, Experience...)
- **Hybrid Retrieval**: Kết hợp Vector Search và BM25 để tìm kiếm chính xác
- **Giao diện thân thiện**: Streamlit UI dễ sử dụng
- **Trả lời thông minh**: Sử dụng GPT-4 để trả lời câu hỏi dựa trên CV

## 📋 Yêu cầu hệ thống

- Python 3.9+
- OpenAI API Key
- Các thư viện Python (xem requirements.txt)

## 🛠️ Cài đặt

1. **Clone repository:**
```bash
git clone <your-repo-url>
cd cv-rag
```

2. **Tạo virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

3. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

4. **Cấu hình environment:**
```bash
cp .env.example .env
# Chỉnh sửa .env và thêm OpenAI API key
```

## 🚀 Chạy ứng dụng

```bash
streamlit run main.py
```

Mở trình duyệt và truy cập: `http://localhost:8501`

## 📁 Cấu trúc project

```
cv-rag/
├── main.py              # Ứng dụng Streamlit chính
├── config.py            # Cấu hình ứng dụng
├── text_processing.py   # Xử lý văn bản CV
├── vector_store.py      # Vector store và retrieval
├── prompts.py           # Template prompts
├── requirements.txt     # Dependencies
├── .env.example        # Ví dụ file environment
├── .gitignore          # Git ignore rules
└── README.md           # Tài liệu này
```

## 🔧 Cấu hình

### Environment Variables

Tạo file `.env` với nội dung:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Cấu hình trong config.py

- `EMBEDDING_MODEL`: Model embedding (mặc định: text-embedding-3-small)
- `LLM_MODEL`: Model LLM (mặc định: gpt-4o-mini)
- `VECTOR_RETRIEVER_K`: Số lượng documents vector retrieval
- `BM25_RETRIEVER_K`: Số lượng documents BM25 retrieval
- `HYBRID_WEIGHTS`: Trọng số kết hợp [vector, bm25]

## 💡 Cách sử dụng

1. **Upload CV**: Chọn file PDF CV cần phân tích
2. **Chờ xử lý**: Hệ thống sẽ tự động tách CV thành các mục
3. **Đặt câu hỏi**: Nhập câu hỏi về CV (ví dụ: "Kinh nghiệm làm việc của ứng viên?")
4. **Nhận kết quả**: Hệ thống sẽ trả lời dựa trên thông tin trong CV

## 🔍 Ví dụ câu hỏi

- "Ứng viên có kinh nghiệm gì?"
- "Trình độ học vấn của ứng viên?"
- "Kỹ năng lập trình nào ứng viên có?"
- "Dự án nào ứng viên đã tham gia?"
- "Ứng viên có chứng chỉ gì?"

## 🛠️ Công nghệ sử dụng

- **Streamlit**: Giao diện web
- **LangChain**: Framework RAG
- **OpenAI**: Embeddings và LLM
- **FAISS**: Vector database
- **PyMuPDF (fitz)**: Xử lý PDF
- **BM25**: Text retrieval

## 📞 Liên hệ

Nếu có câu hỏi hoặc góp ý, vui lòng tạo issue trên GitHub.

---

**Lưu ý**: Đảm bảo bạn có OpenAI API key hợp lệ để sử dụng ứng dụng.
