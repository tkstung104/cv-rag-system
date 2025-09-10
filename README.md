# CV Analysis & Scoring System

Hệ thống phân tích và chấm điểm CV thông minh sử dụng AI, bao gồm tính năng chat với CV và chấm điểm tự động dựa trên yêu cầu công việc.

## 🚀 Tính năng chính

### 1. 💬 Chat với CV (CV Chat)
- **Upload CV PDF**: Hỗ trợ upload nhiều file CV cùng lúc
- **Xử lý thông minh**: Tự động tách CV thành các mục (Education, Skills, Experience...)
- **Hybrid Retrieval**: Kết hợp Vector Search (FAISS) và BM25 để tìm kiếm chính xác
- **Trả lời thông minh**: Sử dụng GPT-4 để trả lời câu hỏi dựa trên CV
- **Hiển thị chunks**: Xem các phần CV đã được tách và xử lý

### 2. 📊 Chấm điểm CV (CV Scoring)
- **Phân tích yêu cầu công việc**: Tự động tách skills và loại project cần thiết
- **Chấm điểm tự động**: Đánh giá CV dựa trên skills (5 điểm) và projects (5 điểm)
- **Xếp hạng CV**: Sắp xếp CV theo điểm số từ cao xuống thấp
- **Báo cáo chi tiết**: Hiển thị điểm từng mục và bảng tổng kết
- **Upload nhiều CV**: So sánh và chấm điểm nhiều CV cùng lúc

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
rag_cv/
├── main.py              # Ứng dụng Streamlit chính với tabs
├── cv_chat.py           # Module chat với CV
├── cv_scoring.py        # Module chấm điểm CV
├── text_processing.py   # Xử lý văn bản CV (tách sections, làm sạch text)
├── requirements.txt     # Dependencies
├── .env                 # Environment variables (tạo từ .env.example)
└── README.md           # Tài liệu này
```

### 📝 Mô tả các file:

- **`main.py`**: File chính chứa giao diện Streamlit với 2 tabs
- **`cv_chat.py`**: Xử lý logic chat với CV (embeddings, retrieval, QA)
- **`cv_scoring.py`**: Xử lý logic chấm điểm CV (phân tích yêu cầu, scoring, ranking)
- **`text_processing.py`**: Các function xử lý text cơ bản (tách sections, làm sạch PDF)

## 🔧 Cấu hình

### Environment Variables

Tạo file `.env` với nội dung:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Cấu hình mặc định

- **Embedding Model**: `text-embedding-3-small`
- **LLM Model**: `gpt-4o-mini`
- **Vector Retriever K**: 8 documents
- **BM25 Retriever K**: 7 documents
- **Hybrid Weights**: [0.7, 0.3] (vector, bm25)
- **Temperature**: 0 (để có kết quả nhất quán)

## 💡 Cách sử dụng

### Tab 1: Chat với CV

1. **Upload CV**: Chọn file PDF CV cần phân tích
2. **Chờ xử lý**: Hệ thống sẽ tự động tách CV thành các mục và tạo embeddings
3. **Xem chunks**: Kiểm tra các phần CV đã được tách
4. **Đặt câu hỏi**: Nhập câu hỏi về CV
5. **Nhận kết quả**: Hệ thống sẽ trả lời dựa trên thông tin trong CV

### Tab 2: Chấm điểm CV

1. **Upload CVs**: Chọn nhiều file PDF CV cần chấm điểm
2. **Nhập yêu cầu công việc**: Mô tả chi tiết về vị trí tuyển dụng
3. **Chấm điểm**: Nhấn nút "Chấm điểm CV"
4. **Xem kết quả**: 
   - Yêu cầu đã phân tích (skills, projects)
   - Điểm từng CV (skills: 5đ, projects: 5đ, tổng: 10đ)
   - Xếp hạng CV từ cao xuống thấp
   - Bảng tổng kết

## 🔍 Ví dụ câu hỏi (Chat với CV)

- "Ứng viên có kinh nghiệm gì?"
- "Trình độ học vấn của ứng viên?"
- "Kỹ năng lập trình nào ứng viên có?"
- "Dự án nào ứng viên đã tham gia?"
- "Ứng viên có chứng chỉ gì?"
- "Ứng viên có kinh nghiệm với Python không?"

## 📝 Ví dụ yêu cầu công việc (CV Scoring)

```
Yêu cầu ứng viên:
- Tốt nghiệp đại học chuyên ngành Công nghệ thông tin
- Có kinh nghiệm 2-3 năm

Kỹ năng cần thiết:
- Thành thạo Python và các thư viện ML: PyTorch, TensorFlow, Transformers
- Có kiến thức cơ bản về các mô hình LLMs như: Qwen, LLaMA
- Kinh nghiệm với database SQL và NoSQL
- Có kinh nghiệm làm việc với Docker và Kubernetes
```

## 🛠️ Công nghệ sử dụng

### Core Technologies
- **Streamlit**: Giao diện web tương tác
- **LangChain**: Framework RAG và LLM orchestration
- **OpenAI**: Embeddings (text-embedding-3-small) và LLM (gpt-4o-mini)

### Vector Search & Retrieval
- **FAISS**: Vector database cho semantic search
- **BM25**: Keyword-based text retrieval
- **Ensemble Retriever**: Kết hợp vector và BM25 search

### PDF Processing
- **PyMuPDF (fitz)**: Xử lý và trích xuất text từ PDF
- **Custom text processing**: Làm sạch và tách sections CV

### Data Processing
- **Pandas**: Xử lý và hiển thị dữ liệu bảng
- **JSON**: Xử lý structured data
- **Regex**: Pattern matching cho text processing

## 🔄 Quy trình hoạt động

### Chat với CV:
1. **PDF Processing**: Trích xuất text từ PDF
2. **Text Cleaning**: Làm sạch và chuẩn hóa text
3. **Section Splitting**: Tách CV thành các mục (Skills, Experience, etc.)
4. **Chunking**: Tạo chunks với metadata
5. **Embedding**: Tạo vector embeddings cho mỗi chunk
6. **Indexing**: Lưu trữ trong FAISS và BM25
7. **Query Processing**: Tìm kiếm relevant chunks
8. **Response Generation**: Tạo câu trả lời với LLM

### CV Scoring:
1. **Job Analysis**: Phân tích yêu cầu công việc thành skills và projects
2. **CV Processing**: Tách CV thành sections
3. **Skills Matching**: So sánh skills CV với yêu cầu (0-5 điểm)
4. **Projects Matching**: Đánh giá độ liên quan projects (0-5 điểm)
5. **Scoring**: Tính tổng điểm (0-10 điểm)
6. **Ranking**: Xếp hạng CV theo điểm số
7. **Reporting**: Tạo báo cáo chi tiết

## 🚀 Tính năng nâng cao

- **Hybrid Retrieval**: Kết hợp semantic và keyword search
- **Smart Section Detection**: Tự động nhận diện các mục CV
- **Multi-CV Support**: Xử lý nhiều CV cùng lúc
- **Real-time Processing**: Xử lý và hiển thị kết quả real-time
- **Detailed Analytics**: Báo cáo chi tiết với metrics và rankings

## 📊 Hiệu suất

- **Embedding Model**: text-embedding-3-small (nhanh, chính xác)
- **LLM Model**: gpt-4o-mini (cân bằng tốc độ và chất lượng)
- **Retrieval**: Hybrid approach tối ưu độ chính xác
- **Caching**: Session state caching để tránh xử lý lại

## 🔧 Troubleshooting

### Lỗi thường gặp:

1. **"No module named 'fitz'"**
   ```bash
   pip install PyMuPDF
   ```

2. **"OpenAI API key not found"**
   - Kiểm tra file `.env` có chứa `OPENAI_API_KEY`
   - Đảm bảo API key hợp lệ

3. **"PDF cannot be processed"**
   - Kiểm tra file PDF không bị lỗi
   - Thử với PDF khác

4. **"No relevant documents found"**
   - Thử câu hỏi khác
   - Kiểm tra CV có chứa thông tin liên quan

## 📞 Liên hệ

Nếu có câu hỏi hoặc góp ý, vui lòng tạo issue trên GitHub.

---

**Lưu ý**: 
- Đảm bảo bạn có OpenAI API key hợp lệ để sử dụng ứng dụng
- Hệ thống sử dụng GPT-4o-mini để tối ưu chi phí và tốc độ
- Kết quả chấm điểm chỉ mang tính tham khảo, cần kết hợp với đánh giá thủ công
