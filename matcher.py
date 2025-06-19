from sentence_transformers import SentenceTransformer, util
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_jobs(filepath="utils/jobs.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def match_jobs(resume_data):
    job_data = load_jobs()
    resume_embedding = model.encode(resume_data["text"], convert_to_tensor=True)

    matches = []
    for job in job_data:
        job_embedding = model.encode(job["description"], convert_to_tensor=True)
        similarity = float(util.cos_sim(resume_embedding, job_embedding))
        job["score"] = round(similarity * 100, 2)
        matches.append(job)

    matches = sorted(matches, key=lambda x: x["score"], reverse=True)
    return matches[:5]

