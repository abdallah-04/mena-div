import streamlit as st
import tempfile
import os
from main import extract_text, analyze_with_llama 

st.set_page_config(page_title="CV Analyzer", layout="centered")

st.title("📄 AI CV Analyzer")

# --- Upload section ---
uploaded_file = st.file_uploader("Upload your CV file", type=["pdf", "docx", "txt", "png", "jpg"])

# --- Input fields ---
st.subheader("Job Requirements")
skills = st.text_input("Required Skills (comma-separated)", placeholder="e.g. Python, Data Analysis, Communication")
languages = st.text_input("Languages (comma-separated)", placeholder="e.g. English, Arabic")
job_title = st.text_input("Job Title", placeholder="e.g. Data Scientist")
years_exp = st.slider("Minimum Years of Experience", 0, 20, 2)

# --- Analyze button ---
if st.button("🔍 Analyze CV"):
    if not uploaded_file:
        st.warning("⚠️ Please upload a CV file first.")
    else:
        try:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            # Extract text from CV
            cv_text = extract_text(tmp_path)

            # Combine job info into one job description string
            job_description = f"""
Job Title: {job_title}
Required Skills: {skills}
Languages: {languages}
Minimum Years of Experience: {years_exp}
"""

            # Analyze using local LLaMA model
            st.info("🧠 Analyzing CV with LLaMA model... Please wait.")
            result = analyze_with_llama(cv_text, job_description)

            st.success("✅ Analysis complete!")
            st.write("### 🏆 AI Analysis Result")
            st.code(result, language="json")

        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
