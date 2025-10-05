# ====== Imports ======
from extractor import extract_text
import fitz  
from docx import Document
import os
import subprocess  # Use subprocess to call Ollama CLI
import json

# ====== CV Extraction (keep as is) ======
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text.strip()

def extract_text_from_pdf(file_path):
    pdf = fitz.open(file_path)
    text = ""
    for page in pdf:
        text += page.get_text("text")
    return text.strip()

def extract_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Please use PDF or DOCX.")


# ====== LLaMA Offline Analysis via CLI ======
import subprocess
import tempfile
import os

def analyze_with_llama(cv_text, job_description, model="llama3"):
    prompt = f"""
You are a CV analyzer AI. Extract and compare data from the following CV and job description.

Return the result as JSON with this structure:
{{
  "name": "",
  "skills": [],
  "achievements": [],
  "match_score": "",
  "notes": ""
}}

CV Text:
{cv_text}

Job Description:
{job_description}
"""

    # Create a temporary file with the prompt
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write(prompt)
        temp_path = f.name

    try:
        # Run Ollama with the file as input
        cmd = f'ollama run {model} < "{temp_path}"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        if result.returncode != 0:
            raise RuntimeError(f"Ollama CLI error: {result.stderr}")

        return result.stdout.strip()

    finally:
        # Clean up temp file
        os.remove(temp_path)

# ====== MAIN PROGRAM ======
if __name__ == "__main__":
    file_path = r"C:\Users\abdal\OneDrive\Desktop\mena-div\Copy of  Resume.pdf"

    try:
        # Step 1: Extract text
        cv_text = extract_text(file_path)
        print("✅ CV text extracted successfully!\n")
        print("Extracted CV Text:\n", cv_text)

        # Step 2: HR job description
        job_description = """
We are looking for a Software Engineer skilled in Python, Machine Learning, and problem-solving.
"""

        # Step 3: Analyze with LLaMA
        print("\nAnalyzing CV with local LLaMA model...")
        result = analyze_with_llama(cv_text, job_description)

        print("\n===== LLaMA Output =====\n")
        print(result)

    except Exception as e:
        print(f"Error: {e}")
