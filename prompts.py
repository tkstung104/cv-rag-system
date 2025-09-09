"""
template prompt cho ứng dụng CV RAG
"""
from langchain.prompts import PromptTemplate


def get_qa_prompt() -> PromptTemplate:
    """
    Lấy template prompt cho việc trả lời câu hỏi
    """
    return PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "Bạn là trợ lý phân tích CV. Dựa trên ngữ cảnh sau:\n"
            "{context}\n\n"
            "Câu hỏi: {question}\n"
            "Yêu cầu:\n"
            "- Trả lời chính xác, ngắn gọn.\n"
            "- Khi tìm kiếm hãy tìm đúng các mục 'section' kết hợp với 'applicant_name'trong metadata.\n"
            "- Trích dẫn mục trong CV (SECTION) nếu có.\n"
            "- Nếu CV không có thông tin, hãy trả lời: 'Không thấy trong CV'."
        )
    )


def get_document_prompt() -> PromptTemplate:
    """
    Lấy template prompt cho việc định dạng các tài liệu được truy xuất
    """
    return PromptTemplate.from_template(
        "SOURCE: file={file_name}; section={section}\n{page_content}"
    )
