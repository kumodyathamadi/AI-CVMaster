import re
from services.skill_extractor import extract_skills

def match_job_description(resume_text, job_description):
    """
    Matches the resume against a job description by extracting skills from both.
    """
    if not job_description or len(job_description.strip()) < 10:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "explanation": "Please provide a valid job description for analysis."
        }
    
    # 1. Extract skills from Job Description
    jd_skills_data = extract_skills(job_description)
    required_skills = jd_skills_data.get('technical', []) + jd_skills_data.get('soft', [])
    
    # Ensure we have unique skills
    required_skills = list(dict.fromkeys(required_skills))
    
    if not required_skills:
        # Fallback: If no specific skills found, use most frequent words as keywords
        # (Very basic keyword extraction)
        words = re.findall(r'\b\w{4,}\b', job_description.lower())
        stop_words = {'with', 'that', 'this', 'from', 'your', 'will', 'must', 'have', 'years', 'working'}
        required_skills = [w.capitalize() for w in words if w not in stop_words][:5]

    # 2. Extract skills from Resume
    resume_skills_data = extract_skills(resume_text)
    candidate_skills = [s.lower() for s in (resume_skills_data.get('technical', []) + resume_skills_data.get('soft', []))]
    
    # 3. Perform Match
    matched_skills = []
    missing_skills = []
    
    for skill in required_skills:
        if skill.lower() in candidate_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    # Calculate Score
    if not required_skills:
        score = 0
    else:
        score = (len(matched_skills) / len(required_skills)) * 100
        
    # Generate Explanation
    strengths = ", ".join(matched_skills[:3]) if matched_skills else "None identified"
    improvements = ", ".join(missing_skills[:3]) if missing_skills else "None identified"
    
    if score > 75:
        explanation = f"Excellent match! You have key strengths in {strengths}."
    elif score > 40:
        explanation = f"Good match. You have experience in {strengths}, but consider improving your knowledge of {improvements}."
    else:
        explanation = f"Low match. The job requires strong skills in {improvements} which are currently missing from your resume."
        
    return {
        "score": round(score, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "strengths": matched_skills[:5],
        "weaknesses": missing_skills[:5],
        "explanation": explanation
    }
