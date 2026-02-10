import PyPDF2
from docx import Document
import re

def parse_resume(file):
    """Parse PDF or DOCX resume"""
    text = ""
    filename = file.name
    
    if filename.endswith('.pdf'):
        with open(filename, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text()
    
    elif filename.endswith('.docx'):
        doc = Document(filename)
        for para in doc.paragraphs:
            text += para.text + "\n"
    
    # Extract key sections
    skills = extract_skills(text)
    experience = extract_experience(text)
    
    return {
        "text": text,
        "skills": skills,
        "experience": experience,
        "filename": filename
    }

def extract_skills(text):
    """Extract skills using regex patterns"""
    skill_patterns = [
        r'(Python|Java|JavaScript|C\+\+|React|Node\.js|AWS|Docker|Kubernetes)',
        r'(Machine Learning|Deep Learning|NLP|Computer Vision|TensorFlow|PyTorch)',
        r'(SQL|MongoDB|PostgreSQL|MySQL|Redis)'
    ]
    skills = []
    for pattern in skill_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        skills.extend(matches)
    return list(set(skills))

def extract_experience(text):
    """Extract work experience"""
    lines = text.split('\n')
    experience = []
    for line in lines:
        if re.search(r'\d{4}', line) and any(word in line.lower() for word in ['year', 'month', 'exp', 'worked']):
            experience.append(line.strip())
    return experience
