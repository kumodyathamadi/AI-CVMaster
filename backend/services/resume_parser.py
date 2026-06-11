import re
from datetime import datetime
from services.skill_extractor import extract_skills

def extract_name(text):
    """
    Attempts to extract the candidate's name from the resume text.
    """
    resume_keywords = ['resume', 'cv', 'curriculum', 'vitae', 'profile', 'summary', 'contact', 'experience', 'education']
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    
    for line in lines:
        words = line.split()
        if 1 <= len(words) <= 4:
            # Check if any word is a common resume keyword
            if not any(word.lower() in resume_keywords for word in words):
                # Basic check for capitalized words (names usually are)
                if all(word[0].isupper() for word in words if any(c.isalpha() for c in word)):
                    return line
                    
    return "Not Found"

def extract_links(text):
    """
    Extracts LinkedIn and GitHub URLs.
    """
    links = {"linkedin": "Not Found", "github": "Not Found"}
    
    linkedin_pattern = r'(https?://)?(www\.)?linkedin\.com/in/[\w\-\_]+/?'
    github_pattern = r'(https?://)?(www\.)?github\.com/[\w\-\_]+/?'
    
    linkedin_match = re.search(linkedin_pattern, text.lower())
    github_match = re.search(github_pattern, text.lower())
    
    if linkedin_match:
        links["linkedin"] = linkedin_match.group(0)
    if github_match:
        links["github"] = github_match.group(0)
        
    return links

def calculate_years_from_dates(text):
    """
    Attempts to calculate years of experience from date ranges in the text.
    Example: 2018 - 2022, Jan 2020 to Present
    """
    # Pattern for years (e.g., 2015 - 2020, 2018-Present)
    year_range_pattern = r'\b(19|20)\d{2}\s*[-–—to]+\s*((19|20)\d{2}|Present|Current|Now)\b'
    matches = re.finditer(year_range_pattern, text, re.IGNORECASE)
    
    total_months = 0
    current_year = datetime.now().year
    
    found_any = False
    for match in matches:
        found_any = True
        start_year = int(match.group(1) + match.group(0)[2:4]) if len(match.group(1)) == 2 else int(match.group(1) + match.group(0)[2:4]) # This group logic is a bit flawed, let's simplify.
        
        # Simpler: just get all numbers that look like years
        parts = re.split(r'[-–—to]+', match.group(0), flags=re.IGNORECASE)
        if len(parts) == 2:
            try:
                start_str = re.search(r'\b(19|20)\d{2}\b', parts[0])
                end_str = re.search(r'\b(19|20)\d{2}\b', parts[1])
                
                if start_str:
                    s_yr = int(start_str.group(0))
                    if "present" in parts[1].lower() or "current" in parts[1].lower() or "now" in parts[1].lower():
                        e_yr = current_year
                    elif end_str:
                        e_yr = int(end_str.group(0))
                    else:
                        e_yr = s_yr # Single year mentioned?
                        
                    total_months += (e_yr - s_yr) * 12
            except:
                continue
                
    if not found_any:
        # Fallback to "X years of experience" text
        years_text_pattern = r'(\d+)\+?\s*(years?|yrs?)\s+experience'
        match = re.search(years_text_pattern, text.lower())
        if match:
            return int(match.group(1))
        return 0

    return round(total_months / 12, 1)

def extract_job_titles(text):
    """
    Extracts job titles by looking for common patterns.
    Never hallucinates; only returns titles found in text.
    """
    # Common job title suffixes/indicators
    title_indicators = [
        'Engineer', 'Developer', 'Analyst', 'Manager', 'Specialist', 
        'Lead', 'Architect', 'Consultant', 'Assistant', 'Officer',
        'Executive', 'Coordinator', 'Director', 'Trainee', 'Intern',
        'Designer', 'Practitioner', 'Administrator'
    ]
    
    lines = text.split('\n')
    found_titles = []
    
    for line in lines:
        line = line.strip()
        if not line or len(line) > 60: # Job titles are usually short
            continue
            
        # Check if line contains a title indicator and isn't just a header
        if any(indicator in line for indicator in title_indicators):
            # Exclude lines that are clearly section headers
            if line.lower() not in ['experience', 'work experience', 'employment history', 'education', 'skills']:
                # Basic cleaned title
                found_titles.append(line)
                
    # Return unique titles, limit to top 5 to avoid noise
    return list(dict.fromkeys(found_titles))[:5] if found_titles else ["Not Found"]

def extract_experience_summary(text):
    """
    Improved extraction of years and titles.
    """
    years = calculate_years_from_dates(text)
    titles = extract_job_titles(text)
    
    return {
        "years": years,
        "job_titles": titles
    }

def parse_resume_text(text):
    """
    Main extraction pipeline.
    """
    if not text or len(text.strip()) < 10:
        return {"error": "Could not extract sufficient text from PDF."}

    try:
        # Extract basic info
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}?\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
        
        email_match = re.search(email_pattern, text)
        phone_match = re.search(phone_pattern, text)
        
        email = email_match.group(0) if email_match else "Not Found"
        phone = phone_match.group(0).strip() if phone_match else "Not Found"
        
        name = extract_name(text)
        links = extract_links(text)
        skills_data = extract_skills(text)
        exp_data = extract_experience_summary(text)
        
        # Education Level Detection
        education = "Information Not Available"
        if re.search(r'\b(B\.?Sc|Bachelor|B\.?Tech|B\.?E)\b', text, re.I):
            education = "Bachelor's Degree"
        elif re.search(r'\b(M\.?Sc|Master|M\.?Tech|M\.?E|MBA)\b', text, re.I):
            education = "Master's Degree"
        elif re.search(r'\b(PhD|Doctorate)\b', text, re.I):
            education = "PhD"
            
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "links": links,
            "skills": skills_data,
            "experience": exp_data,
            "education": {
                "degree": education
            }
        }
    except Exception as e:
        return {"error": str(e)}
