import fitz  
from docx import Document
import os
import subprocess  
import json
import tempfile

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


def analyze_with_llama(cv_text, job_description, model="llama3"):
    prompt = f"""
You are a strict CV extractor and job matcher.

Your job:
1. Extract ONLY information that *explicitly appears* in the CV text — do NOT infer or guess anything.
2. If something (like name or experience) cannot be clearly found, set it to null.
3. Never mix or invent data.
4. Extract skills *only* if the exact words appear in the CV text.
5. Return all output as **valid JSON only**, no explanations.

JSON format:
{{
  "name": "<exact name or null>",
  "skills": ["<skill1>", "<skill2>", ...],
  "years_of_experience": <number or null>,
  "job_title": "<job title from JD or null>",
  "match_score": <integer 0-10>,
  "notes": "<explain briefly how the score was computed>"
}}

CV Text:
{cv_text}

Job Description:
{job_description}
"""

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write(prompt)
        temp_path = f.name

    try:
        cmd = f'ollama run {model} < "{temp_path}"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        if result.returncode != 0:
            raise RuntimeError(f"Ollama CLI error: {result.stderr}")

        return result.stdout.strip()

    finally:
        os.remove(temp_path)
