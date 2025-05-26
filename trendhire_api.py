from fastapi import FastAPI
import os

app = FastAPI(title="TrendHire API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "TrendHire API is running!", "status": "success"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "bright_data_configured": bool(os.getenv("BRIGHT_DATA_API_KEY"))}

@app.get("/trending-jobs")
def get_trending_jobs():
    # Mock data for demo
    return {
        "trending_jobs": [
            {"title": "AI Safety Engineer", "growth": 340, "avg_salary": 185000, "demand": "Very High"},
            {"title": "Prompt Engineer", "growth": 280, "avg_salary": 145000, "demand": "High"},
            {"title": "MLOps Engineer", "growth": 220, "avg_salary": 155000, "demand": "High"},
            {"title": "Climate Data Scientist", "growth": 190, "avg_salary": 135000, "demand": "Medium"},
            {"title": "Quantum Software Developer", "growth": 150, "avg_salary": 165000, "demand": "Medium"}
        ]
    }

@app.get("/skills-analysis/{skills}")
def analyze_skills(skills: str):
    skill_list = [s.strip() for s in skills.split(",")]
    return {
        "current_skills": skill_list,
        "trending_skills": ["LangChain", "Vector Databases", "MLOps", "Kubernetes", "Rust"],
        "recommendations": [f"Learn {skill} to increase marketability" for skill in ["LangChain", "MLOps"]]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))