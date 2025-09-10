"""
Thiết lập vector store và truy xuất thông tin cho tài liệu CV
"""

import fitz
import hashlib
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
from config import EMBEDDING_MODEL, VECTOR_RETRIEVER_K, BM25_RETRIEVER_K, HYBRID_WEIGHTS
from text_processing import clean_pdf_text, split_cv_sections


def process_pdf_files(pdfs) -> List[Document]:
    """
    Xử lý các file PDF đã upload và trả về danh sách đối tượng Document
    """
    documents = []
    
    for pdf in pdfs:
        if pdf is not None:
            file_name = pdf.name if hasattr(pdf, "name") else "Unknown"

            # Mở file PDF với fitz (cần đọc binary từ Streamlit upload)
            with fitz.open(stream=pdf.read(), filetype="pdf") as doc_fitz:
                full_text = ""
                for page in doc_fitz:
                    page_text = page.get_text("text") or ""
                    full_text += page_text + "\n"
                    
            # Làm sạch text
            full_text = clean_pdf_text(full_text)

            documents.append(
                Document(
                    page_content=full_text,
                    metadata={
                        "source": "pdf", 
                        "file_name": file_name
                    }
                )
            )
    
    return documents


def create_chunks_from_documents(documents: List[Document]) -> List[Document]:
    """
    Tạo chunks từ documents bằng cách tách các mục CV
    """
    all_chunks = []
    
    for doc in documents:
        first_line = doc.page_content.strip().split("\n")[0]
        applicant_name = first_line.strip()
        sections = split_cv_sections(doc.page_content)
        
        for title, body in sections:
            if body.strip():
                all_chunks.append(
                    Document(
                        page_content=applicant_name + "\n" + body.strip(),
                        metadata={
                            **doc.metadata, 
                            "section": title, 
                            "applicant_name": applicant_name
                        }
                    )
                )
    
    return all_chunks


def create_hybrid_retriever(all_chunks: List[Document]) -> EnsembleRetriever:
    """
    Tạo hybrid retriever kết hợp vector và BM25 retrieval.
    """
    # Tạo embeddings
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    knowledge_base = FAISS.from_documents(all_chunks, embeddings)

    # Hybrid retriever
    vector_retriever = knowledge_base.as_retriever(search_kwargs={"k": VECTOR_RETRIEVER_K})
    bm25_retriever = BM25Retriever.from_documents(all_chunks)
    bm25_retriever.k = BM25_RETRIEVER_K

    hybrid_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=HYBRID_WEIGHTS,
    )
    
    return hybrid_retriever


def calculate_pdf_hash(pdfs) -> str:
    """
    Tính MD5 hash của nội dung PDF để phát hiện thay đổi
    """
    pdf_content = b""
    for pdf in pdfs:
        if pdf is not None:
            pdf_content += pdf.read()
            pdf.seek(0)  
    
    return hashlib.md5(pdf_content).hexdigest()
