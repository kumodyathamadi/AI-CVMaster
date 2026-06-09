def calculate_scores(parsed_data):
    """
    Calculates various scores based on the parsed resume data with strict criteria.
    """
    resume_score = 0
    total_weight = 100
    
    # 1. Contact & Social Information (20 points)
    info_score = 0
    if parsed_data.get('email'): info_score += 5
    if parsed_data.get('phone'): info_score += 5
    if parsed_data.get('links', {}).get('linkedin'): info_score += 5
    if parsed_data.get('links', {}).get('github'): info_score += 5
    resume_score += info_score
    
    # 2. Technical Skills Depth (30 points)
    # Stricter: Need at least 10 skills for full points
    tech_skills = parsed_data.get('skills', {}).get('technical', [])
    tech_score = min(len(tech_skills) * 3, 30)
    resume_score += tech_score
    
    # 3. Soft Skills (15 points)
    soft_skills = parsed_data.get('skills', {}).get('soft', [])
    soft_score = min(len(soft_skills) * 3, 15)
    resume_score += soft_score
    
    # 4. Experience & Career Progression (25 points)
    exp_data = parsed_data.get('experience', {})
    exp_score = 0
    years = exp_data.get('years', 0)
    if years > 0:
        exp_score += 10 # Base for having experience
        exp_score += min(years * 2, 10) # Bonus for years (up to 5 years)
    
    if len(exp_data.get('job_titles', [])) > 1:
        exp_score += 5 # Bonus for career progression (multiple roles)
    resume_score += exp_score
    
    # 5. Education & Credentials (10 points)
    edu_score = 0
    if parsed_data.get('education', {}).get('degree') != "Higher Education":
        edu_score += 7
    # Certifications would go here
    resume_score += edu_score

    # 6. ATS Compatibility (Calculated separately but influences overall)
    # Checks for "Standard Sections"
    sections_score = 0
    # In a real scenario, we'd check raw text for section headers
    # Mocking for now based on data presence
    if tech_skills: sections_score += 25
    if exp_data.get('job_titles'): sections_score += 25
    if info_score > 0: sections_score += 25
    if edu_score > 0: sections_score += 25
    
    ats_score = sections_score
    
    # Final Category
    status = "Needs Improvement"
    if resume_score >= 85: status = "Excellent"
    elif resume_score >= 70: status = "Good"
    elif resume_score >= 40: status = "Average"
    
    return {
        "resume_score": round(resume_score),
        "ats_score": round(ats_score),
        "status_badge": status
    }

def generate_insights(parsed_data):
    """
    Generates AI-based insights and recommendations.
    """
    present_tech = [s.lower() for s in parsed_data.get('skills', {}).get('technical', [])]
    
    # Smart Recommendations based on what's missing
    all_target_skills = ['Docker', 'AWS', 'Kubernetes', 'React', 'Python', 'TypeScript', 'SQL']
    missing = [s for s in all_target_skills if s.lower() not in present_tech]
    
    recommendations = {
        "skills": missing[:3],
        "certifications": ["AWS Certified Developer"] if "aws" in [m.lower() for m in missing] else ["Google IT Automation"],
        "projects": ["Full Stack E-commerce"] if "react" in [m.lower() for m in missing] else ["Cloud Native Portfolio"]
    }
    
    # Prediction logic
    prediction = {
        "Backend Developer": 40 + (min(len([s for s in present_tech if s in ['python', 'java', 'sql', 'node.js']]), 4) * 15),
        "Full Stack Developer": 30 + (min(len(present_tech), 10) * 6),
        "Data Analyst": 20 + (50 if 'python' in present_tech and 'sql' in present_tech else 0)
    }
    
    # Ensure scores don't exceed 100
    prediction = {k: min(v, 98) for k, v in prediction.items()}
    
    return {
        "recommendations": recommendations,
        "career_prediction": prediction
    }
