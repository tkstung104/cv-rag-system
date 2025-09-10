from dotenv import load_dotenv
import streamlit as st
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import fitz
import json
import pandas as pd
import re
from typing import List, Dict, Tuple
from text_processing import clean_pdf_text, split_cv_sections


def analyze_job_requirements(job_description: str, llm) -> Dict[str, List[str]]:
    """
    Phân tích yêu cầu công việc và tách thành các skills cụ thể
    """
    prompt = PromptTemplate(
        input_variables=["job_description"],
        template=(
            "Phân tích yêu cầu công việc sau và tách thành các skills cụ thể:\n"
            "{job_description}\n\n"
            "Yêu cầu:\n"
            "1. Tìm phần 'Yêu cầu ứng viên' và 'Kỹ năng cần thiết'\n"
            "2. Tách các skills thành danh sách cụ thể (ví dụ: python, pytorch, tensorflow, etc.)\n"
            "3. Trả về JSON với format: {{\"skills\": [\"skill1\", \"skill2\", ...], \"projects_related\": [\"project_type1\", \"project_type2\", ...]}}\n"
            "4. Chỉ trả về JSON, không có text khác"
        )
    )
    
    chain = prompt | llm
    response = chain.invoke({"job_description": job_description})
    
    try:
        # Tìm JSON trong response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result
        else:
            # Fallback nếu không tìm thấy JSON
            return {"skills": [], "projects_related": []}
    except json.JSONDecodeError:
        return {"skills": [], "projects_related": []}


def score_cv_against_requirements(cv_sections: List[Tuple[str, str]], job_requirements: Dict[str, List[str]], llm) -> Dict[str, float]:
    """
    Chấm điểm CV dựa trên yêu cầu công việc
    Trả về: {"skills_score": float, "projects_score": float, "total_score": float}
    """
    # Tách skills và projects từ CV
    skills_section = ""
    projects_section = ""
    
    for title, content in cv_sections:
        title_lower = title.lower()
        if any(keyword in title_lower for keyword in ["skill", "kỹ năng", "technical", "competence"]):
            skills_section = content
        elif any(keyword in title_lower for keyword in ["project", "dự án", "experience", "kinh nghiệm"]):
            projects_section = content
    
    # Chấm điểm skills (tối đa 5 điểm)
    skills_score = 0
    if skills_section and job_requirements.get("skills"):
        skills_prompt = PromptTemplate(
            input_variables=["cv_skills", "required_skills"],
            template=(
                "So sánh skills trong CV với yêu cầu công việc:\n"
                "CV Skills: {cv_skills}\n"
                "Required Skills: {required_skills}\n\n"
                "Đếm số skills trong CV phù hợp với yêu cầu (mỗi skill = 1 điểm, tối đa 5 điểm).\n"
                "Trả về chỉ số điểm (0-5), không có text khác."
            )
        )
        
        chain = skills_prompt | llm
        response = chain.invoke({
            "cv_skills": skills_section,
            "required_skills": ", ".join(job_requirements["skills"])
        })
        
        try:
            skills_score = min(float(re.search(r'\d+', response).group()), 5.0)
        except:
            skills_score = 0
    
    # Chấm điểm projects (tối đa 5 điểm)
    projects_score = 0
    if projects_section and job_requirements.get("projects_related"):
        projects_prompt = PromptTemplate(
            input_variables=["cv_projects", "required_project_types"],
            template=(
                "So sánh projects trong CV với yêu cầu công việc:\n"
                "CV Projects: {cv_projects}\n"
                "Required Project Types: {required_project_types}\n\n"
                "Đánh giá độ liên quan của projects (mỗi project liên quan = 2 điểm, tối đa 5 điểm).\n"
                "Trả về chỉ số điểm (0-5), không có text khác."
            )
        )
        
        chain = projects_prompt | llm
        response = chain.invoke({
            "cv_projects": projects_section,
            "required_project_types": ", ".join(job_requirements["projects_related"])
        })
        
        try:
            projects_score = min(float(re.search(r'\d+', response).group()), 5.0)
        except:
            projects_score = 0
    
    total_score = skills_score + projects_score
    return {
        "skills_score": skills_score,
        "projects_score": projects_score,
        "total_score": total_score
    }


def rank_cvs(cv_scores: List[Dict]) -> List[Dict]:
    """
    Xếp hạng CV từ cao xuống thấp
    """
    return sorted(cv_scores, key=lambda x: x["total_score"], reverse=True)


def process_cvs_for_scoring(pdfs):
    """Xử lý CV cho tính năng chấm điểm"""
    # Nhập yêu cầu công việc
    st.subheader("Yêu cầu công việc")
    job_description = st.text_area(
        "Nhập mô tả công việc (bao gồm yêu cầu ứng viên và kỹ năng cần thiết):",
        height=200,
        placeholder="Ví dụ:\nYêu cầu ứng viên:\n- Tốt nghiệp đại học chuyên ngành Công nghệ thông tin\n- Có kinh nghiệm 2-3 năm\n\nKỹ năng cần thiết:\n- Thành thạo Python và các thư viện ML: PyTorch, TensorFlow, Transformers\n- Có kiến thức cơ bản về các mô hình LLMs như: Qwen, LLaMA\n- Kinh nghiệm với database SQL và NoSQL"
    )
    
    if not job_description.strip():
        st.warning("Vui lòng nhập yêu cầu công việc để chấm điểm CV")
        return
    
    if st.button("Chấm điểm CV", type="primary"):
        with st.spinner("Đang phân tích yêu cầu công việc và chấm điểm CV..."):
            llm = OpenAI(model="gpt-4o-mini", temperature=0)
            
            # Phân tích yêu cầu công việc
            job_requirements = analyze_job_requirements(job_description, llm)
            
            st.subheader("Yêu cầu đã phân tích:")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Skills cần thiết:**")
                for skill in job_requirements.get("skills", []):
                    st.write(f"- {skill}")
            with col2:
                st.write("**Loại project liên quan:**")
                for project_type in job_requirements.get("projects_related", []):
                    st.write(f"- {project_type}")
            
            # Xử lý từng CV
            cv_scores = []
            
            for i, pdf in enumerate(pdfs):
                if pdf is not None:
                    file_name = pdf.name if hasattr(pdf, "name") else f"CV_{i+1}"
                    
                    # Đọc CV
                    with fitz.open(stream=pdf.read(), filetype="pdf") as doc_fitz:
                        full_text = ""
                        for page in doc_fitz:
                            page_text = page.get_text("text") or ""
                            full_text += page_text + "\n"
                    
                    full_text = clean_pdf_text(full_text)
                    sections = split_cv_sections(full_text)
                    
                    # Chấm điểm CV
                    scores = score_cv_against_requirements(sections, job_requirements, llm)
                    
                    # Lấy tên ứng viên (dòng đầu tiên)
                    applicant_name = full_text.strip().split("\n")[0] if full_text.strip() else file_name
                    
                    cv_scores.append({
                        "applicant_name": applicant_name,
                        "file_name": file_name,
                        "skills_score": scores["skills_score"],
                        "projects_score": scores["projects_score"],
                        "total_score": scores["total_score"]
                    })
            
            # Xếp hạng CV
            ranked_cvs = rank_cvs(cv_scores)
            
            # Hiển thị kết quả
            st.subheader("Kết quả chấm điểm và xếp hạng:")
            
            for i, cv in enumerate(ranked_cvs):
                with st.expander(f"#{i+1} - {cv['applicant_name']} (Điểm: {cv['total_score']}/10)"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Skills", f"{cv['skills_score']}/5")
                    with col2:
                        st.metric("Projects", f"{cv['projects_score']}/5")
                    with col3:
                        st.metric("Tổng điểm", f"{cv['total_score']}/10")
                    
                    st.write(f"**File:** {cv['file_name']}")
            
            # Tạo bảng tổng kết
            st.subheader("Bảng tổng kết:")
            
            df_data = []
            for i, cv in enumerate(ranked_cvs):
                df_data.append({
                    "Hạng": i+1,
                    "Tên ứng viên": cv['applicant_name'],
                    "Skills (5đ)": cv['skills_score'],
                    "Projects (5đ)": cv['projects_score'],
                    "Tổng điểm": cv['total_score'],
                    "File": cv['file_name']
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
