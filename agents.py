import os
import streamlit as st
from mistralai.client import MistralClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import json
import tempfile
from utils.resume_parser import parse_resume
from utils.semantic_search import semantic_search_resume

class RecruitmentAgent:
    def __init__(self, api_key):
        self.client = MistralClient(api_key=api_key)
        self.embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.qa_chain = None
        self.resume_data = None
        self.vectorstore = None
        
    def process_resume(self, resume_file):
        """Parse and process resume for analysis"""
        self.resume_data = parse_resume(resume_file)
        documents = self.text_splitter.split_text(self.resume_data['text'])
        self.vectorstore = FAISS.from_texts(documents, self.embeddings)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.client.chat,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5})
        )
        return self.resume_data
    
    def analyze_resume_fit(self, job_title, job_desc=None, skills=None):
        """Analyze resume fit against job requirements"""
        if not self.resume_data:
            return {"fit_score": 0, "status": "fail", "weak_areas": [], "suggestions": []}
        
        prompt = f"""
        Analyze this resume against {job_title} position.
        Job skills required: {skills or 'AI/ML Engineer skills'}
        Job description: {job_desc or ''}
        
        Resume content: {self.resume_data['text'][:2000]}
        
        Return JSON with:
        {{
            "fit_score": 0-100,
            "status": "pass" if >75 else "fail",
            "matching_skills": ["list"],
            "weak_areas": ["list"],
            "suggestions": ["improvement suggestions"]
        }}
        """
        
        response = self.client.chat(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    def generate_interview_questions(self, job_title):
        """Generate behavioral and technical interview questions"""
        prompt = f"""
        Generate 10 interview questions for {job_title} position based on this resume:
        {self.resume_data['text'][:1500]}
        
        Include:
        1. 5 Technical questions
        2. 3 Behavioral questions  
        3. 2 Project-based questions
        
        Format as numbered list with answers based on resume.
        """
        
        response = self.client.chat(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def improve_resume(self, job_title):
        """Generate improved resume version"""
        prompt = f"""
        Improve this resume for {job_title} position:
        {self.resume_data['text']}
        
        Make it more ATS-friendly, add keywords, improve formatting, and highlight relevant skills.
        Return complete improved resume in markdown format.
        """
        
        response = self.client.chat(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def chat_with_resume(self, question):
        """Chat interface with resume context"""
        if self.qa_chain:
            result = self.qa_chain.invoke({"query": question})
            return result['result']
        return "Please upload resume first."
