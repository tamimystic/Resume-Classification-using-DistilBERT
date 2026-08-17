---
title: Resume Checker
emoji: 📄
colorFrom: indigo
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
license: mit
---

# AI Resume Intelligence

An advanced NLP-based Resume Screening and Classification system designed to automate the categorization of resumes into 24 distinct job industries, extract document text using intelligent OCR fallbacks, and generate concise profile summaries.

## User Guide

This section is for end-users who want to interact with the application to analyze resumes.

### Accessing the Interface
1. Open your web browser and navigate to the provided local URL (typically http://127.0.0.1:7860) when the server is running.
2. You will be greeted by the AI Resume Intelligence dashboard.

### Analyzing a Resume
You have two options to provide a resume for analysis:
- File Upload: Click on the "Upload Document" section. You can upload files in PDF, DOCX, or TXT formats. Scanned PDFs and image-based resumes are also supported.
- Direct Text Input: Paste the raw text of the resume directly into the "Direct Text Input" box.

### Understanding the Results
After clicking "Analyze Resume", the system will process the data and display a result card on the right side containing:
- Predicted Category: The specific industry domain the resume belongs to (e.g., HEALTHCARE, INFORMATION-TECHNOLOGY).
- Overview: A brief description of the predicted professional domain.
- AI Summary: A strictly calculated 5-line extractive summary highlighting the most critical sentences from the provided resume.

---

## Developer Guide

This section is for developers who want to set up the project from scratch on a new machine, understand the underlying architecture, or contribute to the codebase.

### Setup Instructions (Windows Environment)

The following steps assume you are starting with a brand-new Windows machine without prior configurations.

1. Install Python
- Download the latest Python installer (version 3.9 or higher) from the official python.org website.
- Run the installer. Ensure you check the box labeled "Add Python to PATH" before clicking "Install Now".
- Open Command Prompt and type `python --version` to verify the installation.

2. Clone the Repository
- Download and install Git from git-scm.com.
- Open Command Prompt or Git Bash and clone this repository:
  `git clone https://github.com/tamimystic/Resume-Classification-using-DistilBERT.git`
- Navigate into the project directory:
  `cd Resume-Classification-using-DistilBERT`

3. Setup a Virtual Environment
- It is highly recommended to use a virtual environment to isolate project dependencies.
- Create a virtual environment named `env`:
  `python -m venv env`
- Activate the virtual environment:
  `env\Scripts\activate`

4. Install Dependencies
- With the virtual environment activated, install the core requirements:
  `pip install -r requirements.txt`
- Install PyTorch (ensure version >= 2.4.0) and Torchvision. The command may vary based on your hardware (CPU vs CUDA), but the standard command is:
  `pip install --upgrade "torch>=2.4.0" "torchvision>=0.19.0"`
- Install EasyOCR and its dependencies for the OCR fallback capabilities:
  `pip install easyocr opencv-python-headless`

5. Running the Application
- Execute the main application file:
  `python app.py`
- On the initial run, the system will download the DistilBERT pre-trained weights and EasyOCR language models. Subsequent executions will be instantaneous.
- The terminal will provide a local URL (http://127.0.0.1:7860). Open this in your browser to view the application.

### Architecture and Implementation Details

The system was built with a modular architecture to ensure scalability and maintainability.

Directory Structure:
- `components/`: Contains parsing logic. `pdf_parser.py` handles the extraction of text from standard documents and integrates PyMuPDF (fitz). If standard extraction fails or yields empty strings (common in scanned documents), it automatically triggers the EasyOCR fallback mechanism to read text directly from the document images.
- `pipeline/`: Houses the core machine learning logic.
  - `training_pipeline.py`: Manages the fine-tuning of the DistilBERT model.
  - `prediction_pipeline.py`: Loads the trained DistilBERT weights and processes new incoming text for classification.
  - `summarization_pipeline.py`: A dependency-free extractive summarizer utilizing term frequency-inverse document frequency (TF-IDF) logic. It parses sentences, computes word frequencies while ignoring standard stop words, and strictly returns the 5 highest-scoring sentences to avoid heavy generation delays.
- `utils/`: Contains constant mappings such as `job_descriptions.py` which maps the 24 label classes to their respective descriptions.

User Interface:
The frontend is built using Gradio. Standard Gradio elements were overridden using extensive custom CSS to implement a dark glassmorphic theme, responsive grid layouts, and unified component styling to meet modern dashboard standards.
