from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_search_resume(resume_text, job_desc, threshold=0.75):
    """Semantic search between resume and job description"""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    resume_sentences = resume_text.split('. ')
    job_sentences = job_desc.split('. ')
    
    resume_emb = model.encode(resume_sentences)
    job_emb = model.encode(job_sentences)
    
    similarities = []
    for r_emb in resume_emb:
        sims = np.dot(job_emb, r_emb) / (np.linalg.norm(job_emb, axis=1) * np.linalg.norm(r_emb))
        similarities.append(np.max(sims))
    
    avg_similarity = np.mean(similarities)
    return {
        "match_score": avg_similarity * 100,
        "status": "PASS" if avg_similarity >= threshold else "FAIL",
        "matched_sentences": len([s for s in similarities if s >= threshold])
    }
