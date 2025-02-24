import requests
import streamlit as st
import openai
import pdfplumber

openai_api_key = "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"


def extract_text_with_pdfplumber(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def optimize_resume(resume_text, job_description_text):
    prompt = f"""You are an expert resume writer.. given the resume and job description i want you to modify only the text in the resume keeping the structure and format intact ...\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description_text}"""

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}",
        }
        data = {
            "model": "gpt-4o",  # Or "gpt-4" if you have access
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        response_json = response.json()
        summary = response_json["choices"][0]["message"]["content"].strip()
        return summary

    except requests.exceptions.RequestException as e:
        st.error(f"OpenAI API error: {e}")
        return None
    except (KeyError, IndexError) as e:  # Handle potential JSON parsing errors
        st.error(
            f"Error parsing OpenAI response: {e}. Raw Response: {response.text if 'response' in locals() else 'Not available'}")  # Print raw response for debugging.
        return None


st.title("AI Resume Optimizer")

# Input Section
st.subheader("Resume")
resume_source = st.radio("Resume Source:", ("Upload", "Paste"))
resume_text = ""
if resume_source == "Upload":
    uploaded_file = st.file_uploader("Choose a resume file", type=["txt", "pdf", "docx"])  # Add more types if needed
    if uploaded_file is not None:
        try:
            resume_text = extract_text_with_pdfplumber(uploaded_file)
            # Try UTF-8 first
        except UnicodeDecodeError as e:
            raise "Error when uploading pdf"


elif resume_source == "Paste":
    resume_text = st.text_area("Paste your resume text here")

st.subheader("Job Description")
job_description_source = st.radio("Job Description Source:", ("Upload", "Paste"))
job_description_text = ""
if job_description_source == "Upload":
    uploaded_file = st.file_uploader("Choose a job description file",
                                     type=["txt", "pdf", "docx"])  # Add more types if needed
    if uploaded_file is not None:
        try:
            job_description_text = extract_text_with_pdfplumber(uploaded_file)
            # Try UTF-8 first
        except UnicodeDecodeError as e:
            raise "Error when uploading pdf"

elif job_description_source == "Paste":
    job_description_text = st.text_area("Paste the job description text here")

# Optimization Button
if st.button("Optimize Resume"):
    if not resume_text:
        st.error("Please provide a resume.")
    if not job_description_text:
        st.error("Please provide a job description.")

    if resume_text and job_description_text:
        with st.spinner("Optimizing your resume..."):  # Display a spinner while processing
            try:
                optimized_resume = optimize_resume(resume_text, job_description_text)
                st.subheader("Optimized Resume")
                st.write(optimized_resume)  # Use st.write for formatted output if needed
                st.download_button(
                    label="Download Optimized Resume",
                    data=optimized_resume.encode('utf-8'),
                    file_name="optimized_resume.txt",
                    mime="text/plain",
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
