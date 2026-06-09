import re
from services.skill_extractor import extract_skills

def extract_name(text):
    """
    Attempts to extract the candidate's name from the resume text.
    Filters out common resume header words.
    """
    resume_keywords = ['resume', 'cv', 'curriculum', 'vitae', 'profile', 'summary', 'contact']
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    
    for line in lines:
        words = line.split()
        if 1 <= len(words) <= 4:
            # Check if any word is a common resume keyword
            if not any(word.lower() in resume_keywords for word in words):
                # Basic check for capitalized words (names usually are)
                if all(word[0].isupper() for word in words if word.isalpha()):
                    return line
                    
    return "Candidate Name"

def extract_links(text):
    """
    Extracts LinkedIn and GitHub URLs using robust regex.
    """
    links = {"linkedin": None, "github": None}
    
    linkedin_pattern = r'(https?://)?(www\.)?linkedin\.com/in/[\w\-\_]+/?'
    github_pattern = r'(https?://)?(www\.)?github\.com/[\w\-\_]+/?'
    
    linkedin_match = re.search(linkedin_pattern, text.lower())
    github_match = re.search(github_pattern, text.lower())
    
    if linkedin_match:
        links["linkedin"] = linkedin_match.group(0)
    if github_match:
        links["github"] = github_match.group(0)
        
    return links

def extract_experience_summary(text):
    """
    Detects years of experience and matches multiple job titles.
    """
    years_pattern = r'(\d+)\+?\s*(years?|yrs?)'
    # Expanded titles list
    titles_list = [
        'Software Engineer', 'Developer', 'Intern', 'Senior Developer', 
        'Product Manager', 'Data Scientist', 'Designer', 'Architect',
        'Backend Developer', 'Frontend Developer', 'Full Stack'
    ]
    
    years_match = re.search(years_pattern, text.lower())
    years = int(years_match.group(1)) if years_match else 0
    
    found_titles = []
    text_lower = text.lower()
    for title in titles_list:
        if title.lower() in text_lower:
            found_titles.append(title)
            
    return {
        "years": years,
        "job_titles": list(set(found_titles)) # Unique titles
    }

def parse_resume_text(text):
    """
    Main extraction pipeline. Processes text into a structured JSON object.
    """
    if not text or len(text.strip()) < 10:
        print("ERROR: Extracted text is too short or empty.")
        return {"error": "Could not extract sufficient text from PDF."}

    print("-" * 50)
    print(f"DEBUG: Processing text (Length: {len(text)})")
    
    try:
        # Extract basic info
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}?\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
        
        email_match = re.search(email_pattern, text)
        phone_match = re.search(phone_pattern, text)
        
        email = email_match.group(0) if email_match else None
        phone = phone_match.group(0).strip() if phone_match else None
        
        name = extract_name(text)
        links = extract_links(text)
        skills_data = extract_skills(text)
        exp_data = extract_experience_summary(text)
        
        print(f"DEBUG: Extracted Name: {name}")
        print(f"DEBUG: Extracted Email: {email}")
        print(f"DEBUG: Tech Skills Found: {len(skills_data.get('technical', []))}")
        
        # Education Level Detection
        education = "Higher Education"
        if re.search(r'\b(B\.?Sc|Bachelor|B\.?Tech|B\.?E)\b', text, re.I):
            education = "Bachelor's Degree"
        if re.search(r'\b(M\.?Sc|Master|M\.?Tech|M\.?E|MBA)\b', text, re.I):
            education = "Master's Degree"
            
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
        print(f"CRITICAL ERROR in parser: {str(e)}")
        return {"error": str(e)}
