#Smart ATS APP
#import the libraries
import os
import PyPDF2 as pdf
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

#load the environment variables
load_dotenv ()

#configure the the api
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to generate ai
def genai_generate(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    keywords = response.text
    return keywords

#function to read and extract the resume 
def extract_pdf(upload_resume):
    reader = pdf.PdfReader(upload_resume)
    text = " "
    text = ' '.join([str(page.extract_text()) for page in reader.pages])
    return text


def main():
    st.title("Simple ATS")
    job_description = st.sidebar.text_area("PasteJob Description")
    upload = st.sidebar.file_uploader("Upload Resume", type= "pdf", help="please upload your resume")
    submit = st.sidebar.button("Submit")
    
    if submit:
        if upload is not None:
            text = extract_pdf(upload)
            prompt = """
                Please act as ATS (Application Tracking system):
                Task:
                
                   1. Resume evaluation Based on the Highlighted keywords:
                    - Analyze and evaluate the upload resume based on the highlight keywords from the job description
                
                Output:
                   2. Percentage matching and missing keywords based on the Resume Evaluation 1:
                    -Design a percentage matching score each, based on the comparison between the resume and the keywords in the job description.
                    - Use a format Resume | Missing Keywords to do the percentage of matching keyWords and missing keywords from the job_description and the resume.
                    - Ensure high accuracy in identifying missing keywords to provide comprehensive feedback to the user.
                    
                   3. Consider the Competitive Job Market and Provide Best Assistance for Resume Improvement:
                    - Recognize the competitiveness of the job market and aim to provide the best assistance for enhancing the quality of resumes.   
            """
            
            keywords = genai_generate(prompt + str((job_description, text)))
            st.write(keywords)
        else:
            st.write("please upload your resume")
    
    
if __name__ == "__main__":
    main()