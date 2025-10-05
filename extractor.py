# extractor.py
import fitz  # PyMuPDF
from docx import Document
import cv2
import pytesseract
import os
import re
from dotenv import load_dotenv

# Load environment variables (for image paths, optional)
load_dotenv()
pytesseract.pytesseract.tesseract_cmd = r"C://Program Files (x86)//Tesseract-OCR//tesseract.exe"


# ====== DOCX Extraction ======
def extract_text_from_docx(file_path):
    """Extract all text from a DOCX file."""
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text.strip()


# ====== PDF Extraction ======
def extract_text_from_pdf(file_path):
    """Extract all text from a PDF file."""
    pdf = fitz.open(file_path)
    text = ""
    for page in pdf:
        text += page.get_text("text")
    return text.strip()


# ====== IMAGE OCR Extraction ======
def extract_text_from_image(file_path):
    """Extract text from an image using OCR."""
    img = cv2.imread(file_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {file_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    gray = cv2.adaptiveThreshold(gray, 255,
                                 cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.THRESH_BINARY, blockSize=11, C=2)
    text = pytesseract.image_to_string(gray, lang='eng')

    # Clean text
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'[\u2022•�+*]', '-', text)
    return text.strip()


# ====== Automatic Extractor ======
def extract_text(file_path):
    """Detect file type and extract text accordingly (PDF, DOCX, or Image)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_path = file_path.strip('"')  # remove accidental quotes

    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
        return extract_text_from_image(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, or image.")


# ====== Test Block ======
if __name__ == "__main__":
    # Example path (change as needed)
    file_path = r"C:\Users\abdal\OneDrive\Desktop\mena-div\Copy of  Resume.pdf"

    try:
        text = extract_text(file_path)
        print("\n===== Extracted Text =====\n")
        print(text)
    except Exception as e:
        print(f"Error: {e}")
