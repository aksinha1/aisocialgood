import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("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")

st.title("Grant Application AI Scorer")

st.markdown("""
This app uses AI to evaluate grant applications based on custom criteria.
- Enter your evaluation criteria below.
- Upload a grant application (PDF or text).
- Receive a short AI-generated summary and a score out of 100.
""")

# Input for custom criteria
criteria = st.text_area("Enter your evaluation criteria:",
                        placeholder="e.g., Community impact, Innovation, Budget clarity")

# File uploader
uploaded_file = st.file_uploader("Upload a grant application (PDF or TXT):", type=["pdf", "txt"])

# Function to extract text from uploaded file
def extract_text(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")
    elif file.type == "application/pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    else:
        return ""

# When file and criteria are submitted
if st.button("Analyze Application") and uploaded_file and criteria:
    with st.spinner("Analyzing grant application..."):
        file_text = extract_text(uploaded_file)

        # Construct prompt for AI
        prompt = f"""
You are an AI assistant helping a grant administrator evaluate a grant application.
The administrator's criteria are: {criteria}

Here is the grant application:
"""
        prompt += f"""
---
{file_text}
---

Please do two things:
1. Summarize the application in 3-4 sentences.
2. Provide a score out of 100 based on how well it meets the criteria, and explain why.
"""

        # Get AI response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI grant evaluator."},
                    {"role": "user", "content": prompt}
                ]
            )
            ai_output = response['choices'][0]['message']['content']
            st.success("Analysis Complete!")
            st.markdown("### AI Summary & Score")
            st.write(ai_output)

        except Exception as e:
            st.error(f"Error: {e}")

elif not uploaded_file and st.button("Analyze Application"):
    st.warning("Please upload a file.")

elif not criteria and st.button("Analyze Application"):
    st.warning("Please enter your evaluation criteria.")
