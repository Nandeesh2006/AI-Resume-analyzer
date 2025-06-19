import os
import docx
import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def extract_resume_data(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(filepath)
    elif ext == ".docx":
        text = extract_text_from_docx(filepath)
    else:
        raise ValueError("Unsupported file type")

    parsed_data = {
        "name": "N/A",
        "email": "N/A",
        "skills": [],
        "text": text
    }

    doc = nlp(text)
    for token in doc:
        if "@" in token.text:
            parsed_data["email"] = token.text
            break

    skills_db = ["Python", "Java", "Flask", "Machine Learning", "Data Science"]
    parsed_data["skills"] = [skill for skill in skills_db if skill.lower() in text.lower()]

    return parsed_data
