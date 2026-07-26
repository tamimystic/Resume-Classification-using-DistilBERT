import fitz
import numpy as np
from docx import Document

try:
    import easyocr
    reader = easyocr.Reader(['en'])
except ImportError:
    reader = None
    print("EasyOCR not installed. OCR fallback will be disabled.")

def extract_text_from_file(file_path):
    if not file_path:
        return ""
    text = ""
    try:
        if file_path.endswith('.pdf'):
            with fitz.open(file_path) as pdf_doc:
                for page in pdf_doc:
                    text += page.get_text()
            
            if len(text.strip()) < 50 and reader is not None:
                ocr_text = ""
                with fitz.open(file_path) as pdf_doc:
                    for page in pdf_doc:
                        pix = page.get_pixmap()
                        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
                        if pix.n == 4:
                            img = img[:, :, :3]
                        results = reader.readtext(img, detail=0)
                        ocr_text += " ".join(results) + "\n"
                return ocr_text
            return text
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "Unsupported file format."
    except Exception as e:
        return f"Error reading file: {str(e)}"
