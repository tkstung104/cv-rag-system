"""
Tiền xử lý văn bản cho tài liệu CV
"""

import re
from typing import List, Tuple
from config import CV_SECTION_KEYWORDS


def clean_pdf_text(content: str) -> str:
    """Tiền xử lý text trích xuất từ PDF CV"""
    if not content:
        return ""
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    # Bỏ ký tự ẩn
    content = content.replace("\u00AD", "")   # dấu gạch nối mềm
    content = content.replace("\u00A0", " ")  # khoảng trắng không ngắt
    content = content.replace("\u2028", " ")  # dấu phân cách dòng
    content = content.replace("\u2029", "\n\n")  # dấu phân cách đoạn
    return content.strip()


def split_cv_sections(text: str) -> List[Tuple[str, str]]:
    """
    Tách CV thành các mục lớn. 
    Hỗ trợ cả CV với title in hoa toàn bộ và title thường (Objective, Skills...).
    Trả về list (title, full_text).
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    sections = []

    # 1. Tách theo dòng in hoa toàn bộ
    parts = re.split(r"\n(?=[A-Z ]{3,}\n)", text)
    if len(parts) > 1:
        for part in parts:
            if part.strip():
                lines = part.strip().split("\n", 1)
                if len(lines) == 2:
                    title, body = lines
                else:
                    title, body = lines[0], ""
                full_text = f"{title.strip()}\n{body.strip()}"
                sections.append((title.strip(), full_text))
        return sections

    # 2. Nếu không có -> chuyển sang từ khóa CV phổ biến
    pattern = r"\n(?=(" + "|".join(CV_SECTION_KEYWORDS) + r")\n)"
    parts = re.split(pattern, text)

    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i+1].strip() if (i+1) < len(parts) else ""
        full_text = f"{title}\n{body}"
        sections.append((title, full_text))

    return sections
