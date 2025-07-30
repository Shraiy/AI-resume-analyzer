# backend/main.py

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend.resume_matcher import extract_text_from_pdf, get_similarity_score
from backend.log_writer import save_analysis_log
from backend.resume_tips import generate_tips
from backend.pdf_exporter import export_resume_with_tips
import uvicorn

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze_resume(file: UploadFile, job_description: str = Form(...)):
    resume_text = extract_text_from_pdf(file.file)
    match_score, highlighted_words = get_similarity_score(resume_text, job_description)
    tips = generate_tips(resume_text, job_description)
    save_analysis_log(resume_text, job_description, match_score)
    return {
        "match_score": match_score,
        "highlighted_words": highlighted_words,
        "tips": tips
    }

@app.post("/analyze-multi/")
async def analyze_resume_multi(file: UploadFile, jd_text: str = Form(...)):
    resume_text = extract_text_from_pdf(file.file)
    jd_split = jd_text.strip().split('\n\n')  # Multi-JD separated by two newlines
    results = []
    for jd in jd_split:
        score, highlights = get_similarity_score(resume_text, jd)
        tips = generate_tips(resume_text, jd)
        results.append({
            "jd": jd[:50],
            "match_score": score,
            "keywords_found": highlights,
            "tips": tips
        })
    return results

@app.post("/generate-pdf/")
async def generate_pdf(file: UploadFile, job_description: str = Form(...)):
    resume_text = extract_text_from_pdf(file.file)
    tips = generate_tips(resume_text, job_description)
    
    output_file = "enhanced_resume.pdf"
    export_resume_with_tips(resume_text, tips, output_file)

    return FileResponse(path=output_file, filename="enhanced_resume.pdf", media_type='application/pdf')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
