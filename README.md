# 📄 AI CV Analyzer

A Python Streamlit application to analyze CVs against a job description using text extraction and a local LLaMA model. The app supports PDF, DOCX, and image files (PNG, JPG) and evaluates candidate skills, experience, and match score.

---

## 🛠️ Features

* Upload CV files (PDF, DOCX, PNG, JPG).
* Extract text from CVs using PyMuPDF, python-docx, and Tesseract OCR.
* Input job requirements (job title, skills, languages, years of experience).
* Analyze CV with a local LLaMA model.
* Return a structured JSON result with:

  * Candidate name
  * Extracted skills
  * Years of experience
  * Job title match
  * Match score (0–10)
  * Notes on the match
* Download analysis as JSON.

---

## 📦 Requirements

Install Python packages:

```bash
pip install streamlit python-docx PyMuPDF pytesseract opencv-python python-dotenv
```

* **Tesseract OCR** must be installed for image text extraction.
  Download from: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
  Update `pytesseract.pytesseract.tesseract_cmd` in `extractor.py` with your installation path.

* **Ollama CLI** should be installed and working locally to run the LLaMA model.

---

## 🗂️ Project Structure

```
mena-div/
│
├─ app.py              # Streamlit UI
├─ main.py             # Core logic: text extraction & LLaMA analysis
├─ extractor.py        # Text extraction module
├─ .env                # Optional environment variables
├─ requirements.txt    # Python dependencies
```

---

## ⚡ Usage

### 1. Run the Streamlit app:

```bash
streamlit run app.py
```

### 2. Upload a CV:

* Click “Browse files” and select a PDF, DOCX, or image file.

### 3. Enter Job Requirements:

* **Job Title**: e.g., Data Scientist
* **Required Skills**: e.g., Python, SQL, Machine Learning
* **Languages**: e.g., English, Arabic
* **Minimum Years of Experience**: 0–20

### 4. Analyze CV:

* Click **Analyze CV**
* Wait for the AI analysis to complete.
* Results will show in JSON format in the app.

### 5. Download Result:

* Download the full JSON report for further processing.

---

## 🔧 Notes

* The app supports only PDF, DOCX, and images. Other file types are not supported.
* The LLaMA model runs locally via the Ollama CLI; ensure the model (`llama3`) is installed and accessible.
* For large PDFs or images, processing may take a few seconds.

---

## 👨‍💻 Example

**Job Input:**

```
Job Title: Senior Product Manager
Skills: Product Management, Team Leadership, Communication
Languages: English
Minimum Years of Experience: 5
```

**Output JSON:**

```json
{
  "name": "John Doe",
  "skills": ["Product Management", "Team Leadership"],
  "years_of_experience": 6,
  "job_title": "Senior Product Manager",
  "match_score": 8,
  "notes": "Matched skills found, experience sufficient, job title matches"
}
```

Do you want me to do that?
