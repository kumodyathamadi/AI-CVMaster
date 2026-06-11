def detect_domain(parsed_data):
    """
    Detects the candidate's domain based on extracted skills and job titles.
    """
    domains = parsed_data.get('skills', {}).get('domains', {})
    
    # Count matches in each domain
    counts = {
        "Software Engineering": len(domains.get('tech', [])),
        "Banking": len(domains.get('banking', [])),
        "HR": len(domains.get('hr', [])),
        "Marketing": len(domains.get('marketing', []))
    }
    
    # Also check job titles
    titles = " ".join(parsed_data.get('experience', {}).get('job_titles', [])).lower()
    if 'bank' in titles or 'finance' in titles: counts["Banking"] += 3
    if 'hr' in titles or 'human resources' in titles or 'recruitment' in titles: counts["HR"] += 3
    if 'marketing' in titles or 'seo' in titles: counts["Marketing"] += 3
    if 'engineer' in titles or 'developer' in titles or 'software' in titles: counts["Software Engineering"] += 3
    
    # Return the domain with highest score, default to General if no clear match
    best_domain = max(counts, key=counts.get)
    if counts[best_domain] == 0:
        return "General"
    return best_domain

def calculate_scores(parsed_data):
    """
    Calculates various scores based on the parsed resume data.
    """
    resume_score = 0
    
    # 1. Contact & Social Information (20 points)
    info_score = 0
    if parsed_data.get('email') != "Not Found": info_score += 5
    if parsed_data.get('phone') != "Not Found": info_score += 5
    if parsed_data.get('links', {}).get('linkedin') != "Not Found": info_score += 5
    if parsed_data.get('links', {}).get('github') != "Not Found": info_score += 5
    resume_score += info_score
    
    # 2. Skills Depth (30 points)
    all_skills = parsed_data.get('skills', {}).get('technical', [])
    tech_score = min(len(all_skills) * 3, 30)
    resume_score += tech_score
    
    # 3. Soft Skills (15 points)
    soft_skills = parsed_data.get('skills', {}).get('soft', [])
    soft_score = min(len(soft_skills) * 3, 15)
    resume_score += soft_score
    
    # 4. Experience (25 points)
    exp_data = parsed_data.get('experience', {})
    exp_score = 0
    years = exp_data.get('years', 0)
    if years > 0:
        exp_score += 10 
        exp_score += min(int(years * 2), 10) 
    
    titles = exp_data.get('job_titles', [])
    if titles and titles[0] != "Not Found":
        exp_score += 5 
    resume_score += exp_score
    
    # 5. Education (10 points)
    edu_score = 0
    if parsed_data.get('education', {}).get('degree') != "Information Not Available":
        edu_score += 10
    resume_score += edu_score

    # ATS Compatibility
    ats_score = 0
    if len(all_skills) >= 5: ats_score += 25
    if years > 0: ats_score += 25
    if info_score >= 10: ats_score += 25
    if edu_score > 0: ats_score += 25
    
    status = "Needs Improvement"
    if resume_score >= 80: status = "Excellent"
    elif resume_score >= 60: status = "Good"
    elif resume_score >= 40: status = "Average"
    
    return {
        "resume_score": round(resume_score),
        "ats_score": round(ats_score),
        "status_badge": status
    }

def generate_insights(parsed_data):
    """
    Generates domain-aware insights and recommendations.
    """
    domain = detect_domain(parsed_data)
    
    # Domain-specific recommendations
    domain_content = {
        "Banking": {
            "skills": ['Banking Operations', 'Financial Analysis', 'Risk Management', 'Financial Compliance'],
            "certifications": ["CFA Level 1", "Certified Bank Auditor"],
            "career_roles": ["Financial Analyst", "Branch Operations Executive", "Relationship Manager", "Banking Officer"]
        },
        "HR": {
            "skills": ['Recruitment', 'Employee Relations', 'HR Analytics', 'Labor Law Knowledge'],
            "certifications": ["SHRM-CP", "PHR Certification"],
            "career_roles": ["HR Manager", "Recruitment Specialist", "Talent Acquisition Lead", "Employee Relations Manager"]
        },
        "Marketing": {
            "skills": ['Digital Marketing', 'SEO', 'Content Marketing', 'Analytics'],
            "certifications": ["Google Ads Certification", "HubSpot Content Marketing"],
            "career_roles": ["Marketing Executive", "Brand Manager", "Digital Marketing Specialist", "Content Strategist"]
        },
        "Software Engineering": {
            "skills": ['Cloud Platforms (AWS/Azure)', 'DevOps Tools', 'Software Architecture', 'System Design'],
            "certifications": ["AWS Certified Developer", "Microsoft Certified: Azure Fundamentals"],
            "career_roles": ["Backend Developer", "Full Stack Developer", "DevOps Engineer", "Software Architect"]
        },
        "General": {
            "skills": ['Project Management', 'Data Analysis', 'Strategic Planning'],
            "certifications": ["PMP Certification", "Google IT Automation"],
            "career_roles": ["Project Coordinator", "Operations Manager", "Business Analyst"]
        }
    }
    
    content = domain_content.get(domain, domain_content["General"])
    
    # Filter out skills already present
    present_skills = [s.lower() for s in parsed_data.get('skills', {}).get('technical', [])]
    missing_skills = [s for s in content["skills"] if s.lower() not in present_skills]
    
    recommendations = {
        "skills": missing_skills[:3] if missing_skills else ["Advanced Professional Development"],
        "certifications": content["certifications"][:2],
        "projects": [f"Industry Case Study: {domain}", f"Portfolio Project in {domain}"]
    }
    
    # Career Prediction based on domain
    prediction = {}
    roles = content["career_roles"]
    
    # Calculate a baseline percentage and add variety
    base = 60 if domain != "General" else 40
    prediction[roles[0]] = base + 15
    prediction[roles[1]] = base + 5
    if len(roles) > 2:
        prediction[roles[2]] = base - 10
        
    # Ensure scores stay realistic
    prediction = {k: min(v, 95) for k, v in prediction.items()}
    
    return {
        "recommendations": recommendations,
        "career_prediction": prediction,
        "detected_domain": domain
    }
