from dotenv import load_dotenv
import streamlit as st
from cv_chat import process_cvs_for_chat
from cv_scoring import process_cvs_for_scoring


def main():
    load_dotenv()
    st.set_page_config(page_title="CV Analysis & Scoring System")
    st.header("CV Analysis & Scoring System")
    
    # Tạo tabs
    tab1, tab2 = st.tabs(["Chat with CV", "CV Scoring"])

    if 'pdf_hash' not in st.session_state:
        st.session_state.pdf_hash = None
    if 'hybrid_retriever' not in st.session_state:
        st.session_state.hybrid_retriever = None

    with tab1:
        st.subheader("Chat with CV")
        pdfs = st.file_uploader("Upload your CV (PDF)", accept_multiple_files=True, type="pdf")
        
        if not pdfs:
            st.info("Vui lòng upload CV để sử dụng tính năng chat")
        else:
            # Logic xử lý CV cho tab chat
            process_cvs_for_chat(pdfs)
    
    with tab2:
        st.subheader("CV Scoring System")
        pdfs_scoring = st.file_uploader("Upload CVs for scoring (PDF)", accept_multiple_files=True, type="pdf", key="scoring_pdfs")
        
        if not pdfs_scoring:
            st.info("Vui lòng upload CV để chấm điểm")
        else:
            # Logic chấm điểm CV
            process_cvs_for_scoring(pdfs_scoring)


if __name__ == '__main__':
    main()