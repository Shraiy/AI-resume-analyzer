# backend/pdf_exporter.py
import pdfkit

def export_resume_with_tips(resume_text, tips, filename="enhanced_resume.pdf"):
    html_content = f"<h1>Resume Content</h1><p>{resume_text}</p><hr><h2>Improvement Tips</h2><ul>"
    for tip in tips:
        html_content += f"<li>{tip}</li>"
    html_content += "</ul>"

    pdfkit.from_string(html_content, filename)

