"""
Ứng dụng Streamlit chính cho CV RAG
"""
import streamlit as st
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks.manager import get_openai_callback

from config import PAGE_TITLE, LLM_MODEL, LLM_TEMPERATURE
from vector_store import process_pdf_files, create_chunks_from_documents, create_hybrid_retriever, calculate_pdf_hash
from prompts import get_qa_prompt, get_document_prompt


def initialize_session_state():
    """Khởi tạo các biến trạng thái session của Streamlit"""
    if 'pdf_hash' not in st.session_state:
        st.session_state.pdf_hash = None
    if 'hybrid_retriever' not in st.session_state:
        st.session_state.hybrid_retriever = None
    if 'all_chunks' not in st.session_state:
        st.session_state.all_chunks = []


def process_uploaded_pdfs(pdfs):
    """Xử lý các file PDF đã upload và tạo retriever"""
    if not pdfs:
        return False
    
    # Tính hash để phát hiện thay đổi
    current_pdf_hash = calculate_pdf_hash(pdfs)
    
    # Kiểm tra xem có cần xử lý lại không
    if (st.session_state.pdf_hash != current_pdf_hash or 
        st.session_state.hybrid_retriever is None):
        
        with st.spinner("Đang xử lý CV và tạo embeddings..."):
            # Xử lý các file PDF
            documents = process_pdf_files(pdfs)
            
            # Tạo chunks từ documents
            all_chunks = create_chunks_from_documents(documents)
            
            # Tạo hybrid retriever
            hybrid_retriever = create_hybrid_retriever(all_chunks)
            
            # Cập nhật session state
            st.session_state.pdf_hash = current_pdf_hash
            st.session_state.hybrid_retriever = hybrid_retriever
            st.session_state.all_chunks = all_chunks
        
        st.success("CV đã được xử lý thành công!")
        return True
    
    return True


def display_chunks():
    """Hiển thị tất cả chunks trong giao diện"""
    if 'all_chunks' in st.session_state:
        st.subheader(f"Các chunk CV ({len(st.session_state.all_chunks)} chunks):")
        for i, chunk in enumerate(st.session_state.all_chunks):
            st.write(f"**Chunk {i+1}** (Section: {chunk.metadata.get('section')}, File: {chunk.metadata.get('file_name')}):")
            st.text_area(f"Nội dung chunk {i+1}", chunk.page_content, height=100, key=f"chunk_{i}")
            st.write("---")


def handle_question_answering(user_question):
    """Xử lý việc trả lời câu hỏi với hybrid retriever"""
    if not user_question:
        return
    
    # Lấy các tài liệu liên quan
    docs = st.session_state.hybrid_retriever.get_relevant_documents(user_question)
    
    # Thiết lập LLM và chain
    llm = OpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    qa_prompt = get_qa_prompt()
    doc_prompt = get_document_prompt()
    chain = load_qa_chain(llm, chain_type="stuff", prompt=qa_prompt, document_prompt=doc_prompt)
    
    # Lấy phản hồi
    with get_openai_callback() as cb:
        response = chain.invoke({'input_documents': docs, 'question': user_question})
        print(cb)
    
    # Hiển thị phản hồi
    st.subheader("Trả lời:")
    st.write(response['output_text'])
    st.write(docs)


def main():
    """Hàm ứng dụng chính"""
    st.set_page_config(page_title=PAGE_TITLE)
    st.header(PAGE_TITLE)
    
    # Khởi tạo session state
    initialize_session_state()
    
    # Upload file
    pdfs = st.file_uploader("Upload your CV (PDF)", accept_multiple_files=True, type="pdf")
    
    # Xử lý PDFs
    if not process_uploaded_pdfs(pdfs):
        st.stop()
    
    # Hiển thị chunks
    display_chunks()
    
    # Nhập câu hỏi và trả lời
    user_question = st.text_input("Hãy đặt câu hỏi về CV:")
    handle_question_answering(user_question)


if __name__ == '__main__':
    main()
