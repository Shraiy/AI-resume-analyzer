import streamlit as st
import requests

BACKEND_URL = "https://ai-resume-analyzer-axpt.onrender.com"  # Replace with your deployed Render URL

st.title("🧠 AI Resume Analyzer")
st.write("Upload your resume and paste a job description to get AI-powered insights.")

# Upload resume
resume_file = st.file_uploader("📄 Upload Resume (PDF only)", type=["pdf"])
job_description = st.text_area("🧾 Paste Job Description")

if st.button("🔍 Analyze") and resume_file and job_description:
    with st.spinner("Analyzing..."):
        response = requests.post(
            f"{BACKEND_URL}/analyze/",
            files={"file": resume_file},
            data={"job_description": job_description}
        )

        if response.ok:
            result = response.json()
            st.success(f"✅ Match Score: {result['match_score']}%")

            st.subheader("📌 Highlighted Keywords from JD:")
            st.write(result["highlighted_words"])

            st.subheader("📈 Resume Improvement Tips:")
            for tip in result["tips"]:
                st.markdown(f"- {tip}")
        else:
            st.error("Something went wrong. Please check your file or input.")

# PDF Export Button
if st.button("📤 Download Enhanced Resume as PDF") and resume_file and job_description:
    with st.spinner("Generating PDF..."):
        response = requests.post(
            f"{BACKEND_URL}/generate-pdf/",
            files={"file": resume_file},
            data={"job_description": job_description}
        )
        if response.ok:
            with open("enhanced_resume.pdf", "wb") as f:
                f.write(response.content)
            with open("enhanced_resume.pdf", "rb") as f:
                st.download_button("⬇️ Download Enhanced Resume", f, file_name="enhanced_resume.pdf")
        else:
            st.error("Failed to generate PDF. Try again.")

# Optional: Analyze against multiple JDs
with st.expander("💼 Analyze Resume Against Multiple Job Descriptions"):
    jd_multi_input = st.text_area("Paste multiple job descriptions (separate with 2 new lines)")
    if st.button("Analyze Multiple JDs") and resume_file and jd_multi_input:
        with st.spinner("Comparing against multiple JDs..."):
            response = requests.post(
                f"{BACKEND_URL}/analyze-multi/",
                files={"file": resume_file},
                data={"jd_text": jd_multi_input}
            )
            if response.ok:
                results = response.json()
                for res in results:
                    st.markdown("----")
                    st.subheader(f"🧾 JD Preview: `{res['jd']}`")
                    st.write(f"Match Score: {res['match_score']}%")
                    st.write("📌 Matching Keywords:", res["keywords_found"])
                    st.write("📈 Suggestions:")
                    for tip in res["tips"]:
                        st.markdown(f"- {tip}")
            else:
                st.error("Could not compare multiple JDs.")
