import re

def match_job_description(resume_text, job_description):
    """
    Matches the resume against a job description using keyword overlap.
    """
    if not job_description:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": []
        }
        
    # Predefined skill list to look for in JD
    all_skills = [
        'Python', 'Java', 'React', 'Node.js', 'SQL', 'MongoDB', 'Docker', 
        'AWS', 'Git', 'Kubernetes', 'TypeScript', 'Redux'
    ]
    
    jd_lower = job_description.lower()
    resume_lower = resume_text.lower()
    
    required_skills = [s for s in all_skills if s.lower() in jd_lower]
    matched_skills = [s for s in required_skills if s.lower() in resume_lower]
    missing_skills = [s for s in required_skills if s.lower() not in resume_lower]
    
    score = (len(matched_skills) / len(required_skills) * 100) if required_skills else 0
    
    return {
        "score": round(score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
