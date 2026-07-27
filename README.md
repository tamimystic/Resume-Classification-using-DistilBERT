# AI Resume Intelligence 🚀

An advanced, end-to-end NLP-based Resume Screening and Classification system. This project leverages Deep Learning (`DistilBERT`) to automatically categorize resumes into 24 distinct job industries, extracts and cleans text from multiple document formats, and generates an AI summary of the candidate's profile.

## 🔥 Key Features & Technical Work Completed

1. **State-of-the-Art Deep Learning Classification**
   - Implemented a custom `DistilBERT` (Transformer) pipeline for high-accuracy text classification.
   - Built a full training and inference pipeline using `PyTorch` and `Hugging Face Transformers`.
   - The model categorizes resumes into 24 different professional domains (HR, IT, DESIGNER, HEALTHCARE, etc.).

2. **Intelligent Document Parsing & OCR Fallback**
   - Native support for multiple formats: `.pdf`, `.docx`, and `.txt`.
   - **Smart OCR Integration:** If a scanned PDF or image-based resume is uploaded, the system automatically detects empty text and falls back to `EasyOCR` (Computer Vision) to extract the text reliably.

3. **Custom Extractive Summarization**
   - Built a blazing-fast, dependency-free extractive summarization algorithm.
   - Uses TF-IDF based sentence scoring to generate a strict, precise 5-line summary of any resume in milliseconds.

4. **"Ultra Pro Max" UI Dashboard**
   - Completely redesigned the frontend using `Gradio` with advanced custom CSS.
   - Features a stunning dark glassmorphic theme (Zinc 900), animated gradients, glowing accents, and a fully responsive grid layout.
   - Dynamic real-time success cards that display the predicted category along with domain-specific descriptions and the generated summary.

5. **Modular Code Architecture**
   - The codebase is professionally structured following software engineering best practices:
     - `components/`: Handles PDF parsing, data ingestion, and OCR.
     - `pipeline/`: Manages model training, prediction, and summarization logic.
     - `utils/`: Contains constants like job descriptions and helper functions.

---

## 💻 How to Run the Project Locally

### Prerequisites
Make sure you have Python 3.9+ installed and optionally a Conda environment.

### 1. Install Dependencies
Run the following command to install all required libraries:
```bash
pip install -r requirements.txt
pip install easyocr opencv-python-headless
```

### 2. Run the Application
Start the Gradio server by executing:
```bash
python app.py
```
*Note: On the very first run, the system will download the DistilBERT weights and EasyOCR language models. Subsequent runs will be instant.*

### 3. Open in Browser
Once the server starts, open your web browser and go to:
```
http://127.0.0.1:7860
```
Upload a resume or paste text directly to see the AI in action!

---
**Powered by [tamimystic](https://www.linkedin.com/in/tamimystic)**
