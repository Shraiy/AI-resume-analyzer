# backend/log_writer.py
import csv
from datetime import datetime

def save_analysis_log(resume_text, job_description, match_score):
    with open("analysis_logs.csv", mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), resume_text[:100], job_description[:100], match_score])
