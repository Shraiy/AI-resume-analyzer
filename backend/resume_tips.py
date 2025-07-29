def generate_tips(resume_text, job_description):
    tips = []
    if "python" not in resume_text.lower():
        tips.append("Consider adding Python experience.")
    if "team" not in resume_text.lower():
        tips.append("Mention teamwork or collaboration.")
    if "SDLC" not in resume_text.upper():
        tips.append("Add knowledge of software development lifecycle (SDLC).")
    if len(resume_text.split()) < 150:
        tips.append("Resume content looks short; consider expanding details.")
    return tips or ["Resume looks well-aligned!"]
