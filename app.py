try:
    import spaces
    USING_SPACES_GPU = True
except ImportError:
    USING_SPACES_GPU = False

import gradio as gr
import os
from resume_classifier.pipeline.prediction_pipeline import PredictionPipeline
from resume_classifier.pipeline.training_pipeline import TrainingPipeline
from resume_classifier.pipeline.summarization_pipeline import SummarizationPipeline
from resume_classifier.components.pdf_parser import extract_text_from_file
from resume_classifier.utils.job_descriptions import JOB_DESCRIPTIONS

if not os.path.exists("final_models"):
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()

try:
    prediction_pipeline = PredictionPipeline()
except Exception as e:
    prediction_pipeline = None

summarization_pipeline = SummarizationPipeline()

def _predict_resume(text_input, file_input):
    if not prediction_pipeline:
        return "<div class='error-msg'>Model not loaded successfully. Please check the logs.</div>"
    
    final_text = ""
    if file_input:
        final_text = extract_text_from_file(file_input)
    elif text_input and text_input.strip():
        final_text = text_input
    else:
        return "<div class='warning-msg'>Please provide either resume text or upload a resume file.</div>"

    if not final_text.strip():
        return "<div class='warning-msg'>Extracted text is empty. Please provide valid text.</div>"

    try:
        prediction = prediction_pipeline.predict(final_text)
        desc = JOB_DESCRIPTIONS.get(prediction, "A specialized professional in this industry.")
        
        summary = summarization_pipeline.summarize(final_text, num_sentences=5)
        
        return f"""
        <div class='result-container'>
            <div class='result-header'>
                <span class='result-subtitle'>Predicted Category</span>
                <h2 class='result-title'>{prediction}</h2>
            </div>
            <div class='result-body'>
                <p class='result-desc'><b>Overview:</b> {desc}</p>
                <div class='result-summary'>
                    <div class='summary-tag'>AI SUMMARY (MAX 5 LINES)</div>
                    {summary}
                </div>
            </div>
        </div>
        """
    except Exception as e:
        return f"<div class='error-msg'>Error during prediction: {str(e)}</div>"

if USING_SPACES_GPU:
    predict_resume = spaces.GPU(_predict_resume)
else:
    predict_resume = _predict_resume

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --text-main: #ffffff;
    --text-muted: #94a3b8;
    --glass-bg: rgba(255, 255, 255, 0.03);
    --glass-border: rgba(255, 255, 255, 0.08);
}

body {
    background: linear-gradient(125deg, #020617 0%, #0f172a 40%, #1e1b4b 100%) !important;
    background-attachment: fixed !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text-main) !important;
    margin: 0;
    padding: 0;
}

footer { display: none !important; }

.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

.main-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 60px 30px;
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 4rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(to right, #38bdf8, #c084fc, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
    letter-spacing: -0.04em;
    animation: gradientShift 8s ease infinite;
    background-size: 200% auto;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-subtitle {
    text-align: center;
    font-size: 1.25rem;
    color: #cbd5e1;
    font-weight: 300;
    max-width: 800px;
    margin: 0 auto 15px auto;
    line-height: 1.6;
}

.supported-categories {
    text-align: center;
    font-size: 0.95rem;
    color: #94a3b8;
    max-width: 1000px;
    margin: 0 auto 60px auto;
    line-height: 1.8;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    padding: 20px 30px;
    border-radius: 16px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}
.supported-categories span {
    color: #f8fafc;
    font-weight: 600;
    margin-right: 8px;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-size: 0.85rem;
}

.panel {
    background: rgba(15, 23, 42, 0.4) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 24px !important;
    padding: 40px !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
}

.panel-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 30px;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 10px;
}

.file-upload, .text-input {
    background: rgba(0, 0, 0, 0.2) !important;
    border: 1px dashed rgba(255,255,255,0.15) !important;
    border-radius: 16px !important;
    transition: all 0.3s ease !important;
}

.file-upload:hover, .text-input:hover {
    border-color: #38bdf8 !important;
    background: rgba(56, 189, 248, 0.05) !important;
}

.analyze-btn {
    background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899) !important;
    color: white !important;
    border: none !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.25rem !important;
    padding: 18px 30px !important;
    border-radius: 16px !important;
    width: 100% !important;
    margin-top: 30px !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.5) !important;
    background-size: 200% auto !important;
}

.analyze-btn:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 20px 35px -5px rgba(168, 85, 247, 0.6) !important;
    background-position: right center !important;
}

.result-container {
    background: linear-gradient(145deg, rgba(16, 185, 129, 0.1), rgba(4, 120, 87, 0.05));
    border: 1px solid rgba(52, 211, 153, 0.2);
    border-radius: 20px;
    overflow: hidden;
    animation: fadeInScale 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 0 40px rgba(16, 185, 129, 0.1);
}

@keyframes fadeInScale {
    0% { opacity: 0; transform: scale(0.95) translateY(20px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

.result-header {
    background: rgba(6, 78, 59, 0.3);
    padding: 40px;
    border-bottom: 1px solid rgba(52, 211, 153, 0.1);
    text-align: center;
}

.result-subtitle {
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #6ee7b7;
    font-weight: 600;
}

.result-title {
    font-family: 'Outfit', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: #10b981;
    margin: 15px 0 0 0;
    text-shadow: 0 0 30px rgba(16, 185, 129, 0.4);
    letter-spacing: -0.02em;
}

.result-body {
    padding: 40px;
}

.result-desc {
    font-size: 1.15rem;
    color: #d1fae5;
    line-height: 1.7;
    margin-bottom: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid rgba(52, 211, 153, 0.15);
}

.result-desc b {
    color: #34d399;
}

.result-summary {
    font-size: 1.05rem;
    color: #a7f3d0;
    line-height: 1.8;
    background: rgba(0, 0, 0, 0.2);
    padding: 25px;
    border-radius: 16px;
    border: 1px solid rgba(52, 211, 153, 0.1);
}

.summary-tag {
    display: inline-block;
    background: #065f46;
    color: #a7f3d0;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.1em;
    margin-bottom: 15px;
}

.error-msg, .warning-msg {
    padding: 20px;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 500;
    text-align: center;
    backdrop-filter: blur(10px);
}
.error-msg { background: rgba(220, 38, 38, 0.15); border: 1px solid rgba(239, 68, 68, 0.3); color: #fca5a5; }
.warning-msg { background: rgba(217, 119, 6, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); color: #fde68a; }

.ultra-footer {
    text-align: center;
    margin-top: 80px;
    padding-top: 30px;
    border-top: 1px solid var(--glass-border);
    font-size: 1rem;
    color: #94a3b8;
}

.ultra-footer a {
    color: #f8fafc;
    text-decoration: none;
    font-weight: 700;
    border-bottom: 2px solid #38bdf8;
    padding-bottom: 2px;
    transition: all 0.2s ease;
}

.ultra-footer a:hover {
    color: #38bdf8;
    text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
}
"""

with gr.Blocks(title="AI Resume Intelligence") as demo:
    gr.HTML("<div class='main-wrapper'>")
    
    gr.HTML("""
    <div class='hero-title'>AI Resume Intelligence</div>
    <div class='hero-subtitle'>Advanced NLP analysis combining text extraction, intelligent OCR fallback, deep learning classification, and ultra-fast AI summarization.</div>
    """)
    
    categories_html = ", ".join(JOB_DESCRIPTIONS.keys())
    gr.HTML(f"""
    <div class='supported-categories'>
        <span>Supported Categories:</span> {categories_html}
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1, elem_classes="panel"):
            gr.Markdown("<div class='panel-title'>Input Source</div>")
            file_upload = gr.File(label="Upload Document (PDF, DOCX, TXT)", type="filepath", elem_classes="file-upload")
            gr.Markdown("<div style='text-align: center; margin: 20px 0; color: #64748b; font-size: 0.95rem; font-weight: 500;'>— OR —</div>")
            text_box = gr.Textbox(label="Direct Text Input", lines=8, placeholder="Paste resume contents here...", elem_classes="text-input")
            
            predict_btn = gr.Button("Analyze Resume", elem_classes="analyze-btn")
            
        with gr.Column(scale=1, elem_classes="panel"):
            gr.Markdown("<div class='panel-title'>Analysis Results</div>")
            output_html = gr.HTML("<div style='text-align:center; padding: 100px 20px; color: #64748b; font-size: 1.1rem;'>Awaiting input... Upload a file or paste text to see AI predictions.</div>")

    predict_btn.click(fn=predict_resume, inputs=[text_box, file_upload], outputs=output_html, api_name=False)
    
    gr.HTML("""
        <div class='ultra-footer'>
            Powered by <a href='https://www.linkedin.com/in/tamimystic' target='_blank'>tamimystic</a>
        </div>
    </div>
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, css=custom_css)