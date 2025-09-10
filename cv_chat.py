import streamlit as st
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks.manager import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
import hashlib
import fitz
from text_processing import clean_pdf_text, split_cv_sections


def process_cvs_for_chat(pdfs):
    """Xử lý CV cho tính năng chat"""
    # Hash để detect thay đổi file
    pdf_content = b""
    for pdf in pdfs:
        if pdf is not None:
            pdf_content += pdf.read()
            pdf.seek(0)  
    
    current_pdf_hash = hashlib.md5(pdf_content).hexdigest()
    
    if (st.session_state.pdf_hash != current_pdf_hash or 
        st.session_state.hybrid_retriever is None):
        
        with st.spinner("Đang xử lý CV và tạo embeddings..."):
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

            # Chunking theo section + bullet
            all_chunks = []
            for doc in documents:
                first_line = doc.page_content.strip().split("\n")[0]
                applicant_name = first_line.strip()
                sections = split_cv_sections(doc.page_content)
                for title, body in sections:
                    if body.strip():
                        all_chunks.append(
                            Document(
                                page_content=applicant_name + "\n" + body.strip(),   # giữ nguyên cả section (có cả title)
                                metadata={
                                    **doc.metadata, 
                                    "section": title, 
                                    "applicant_name": applicant_name
                                }
                            )
                        )

            # Tạo embeddings
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            knowledge_base = FAISS.from_documents(all_chunks, embeddings)

            # Hybrid retriever
            vector_retriever = knowledge_base.as_retriever(search_kwargs={"k": 8})
            bm25_retriever = BM25Retriever.from_documents(all_chunks)
            bm25_retriever.k = 7

            hybrid_retriever = EnsembleRetriever(
                retrievers=[vector_retriever, bm25_retriever],
                weights=[0.7, 0.3],
            )
            
            st.session_state.pdf_hash = current_pdf_hash
            st.session_state.hybrid_retriever = hybrid_retriever
            st.session_state.all_chunks = all_chunks

        st.success("CV đã được xử lý thành công!")

    qa_prompt = PromptTemplate(
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

    doc_prompt = PromptTemplate.from_template(
        "SOURCE: file={file_name}; section={section}\n{page_content}"
    )

    if 'all_chunks' in st.session_state:
        st.subheader(f"Các chunk CV ({len(st.session_state.all_chunks)} chunks):")
        for i, chunk in enumerate(st.session_state.all_chunks):
            st.write(f"**Chunk {i+1}** (Section: {chunk.metadata.get('section')}, File: {chunk.metadata.get('file_name')}):")
            st.text_area(f"Nội dung chunk {i+1}", chunk.page_content, height=100, key=f"chunk_{i}")
            st.write("---")

    user_question = st.text_input("Hãy đặt câu hỏi về CV:")
    if user_question:
        docs = st.session_state.hybrid_retriever.get_relevant_documents(user_question)

        llm = OpenAI(model="gpt-4o-mini", temperature=0)
        chain = load_qa_chain(llm, chain_type="stuff", prompt=qa_prompt, document_prompt=doc_prompt)
        with get_openai_callback() as cb:
            response = chain.invoke({'input_documents': docs, 'question': user_question})
            print(cb)

        # response = chain.invoke({'input_documents': docs, 'question': user_question})
        st.subheader("Trả lời:")
        st.write(response['output_text'])
        st.write(docs)
