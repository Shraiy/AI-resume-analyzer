# backend/resume_matcher.py

import re
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def highlight_keywords(resume_text, jd_keywords):
    highlighted = {}
    for word in jd_keywords:
        pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)
        matches = pattern.findall(resume_text)
        if matches:
            highlighted[word] = len(matches)
    return highlighted

def get_similarity_score(resume_text, job_description):
    embeddings = model.encode([resume_text, job_description])
    score = util.cos_sim(embeddings[0], embeddings[1]).item()
    score_percent = round(score * 100, 2)
    top_keywords = job_description.split()
    highlighted_words = highlight_keywords(resume_text, top_keywords)
    return score_percent, highlighted_words
