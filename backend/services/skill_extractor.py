def extract_skills(text):
    """
    Extracts technical, soft, and domain-specific skills from the given text.
    """
    # Technical Skills (General IT)
    technical_skills_list = [
        'Python', 'Java', 'React', 'Node.js', 'SQL', 'MongoDB', 'Docker', 
        'AWS', 'Git', 'Machine Learning', 'Deep Learning', 'HTML', 'CSS', 
        'JavaScript', 'TypeScript', 'Express', 'Flask', 'Django', 'PostgreSQL',
        'Redis', 'Kubernetes', 'TensorFlow', 'PyTorch', 'C++', 'C#', 'PHP',
        'Azure', 'GCP', 'NoSQL', 'REST API', 'GraphQL', 'Microservices'
    ]
    
    # Banking & Finance Skills
    banking_skills_list = [
        'Banking Operations', 'Financial Analysis', 'Risk Management', 
        'Customer Relationship Management', 'Financial Compliance', 
        'Banking Certifications', 'Investment Banking', 'Accounting',
        'Credit Analysis', 'Wealth Management', 'Audit', 'Forex', 'KYC', 'AML'
    ]
    
    # Human Resources Skills
    hr_skills_list = [
        'Recruitment', 'Employee Relations', 'HR Analytics', 'Labor Law Knowledge',
        'Talent Acquisition', 'Onboarding', 'Performance Management', 
        'Payroll Administration', 'Training and Development'
    ]
    
    # Marketing Skills
    marketing_skills_list = [
        'Digital Marketing', 'SEO', 'Content Marketing', 'Analytics',
        'Social Media Marketing', 'Email Marketing', 'Brand Management',
        'Market Research', 'PPC', 'Copywriting'
    ]
    
    soft_skills_list = [
        'Leadership', 'Communication', 'Problem Solving', 'Teamwork', 
        'Time Management', 'Creativity', 'Adaptability', 'Critical Thinking',
        'Project Management', 'Public Speaking', 'Analytical Skills'
    ]
    
    text_lower = text.lower()
    
    def get_matches(skill_list):
        return [skill for skill in skill_list if skill.lower() in text_lower]

    found_tech = get_matches(technical_skills_list)
    found_banking = get_matches(banking_skills_list)
    found_hr = get_matches(hr_skills_list)
    found_marketing = get_matches(marketing_skills_list)
    found_soft = get_matches(soft_skills_list)
    
    # Combine all "domain/technical" skills into one list for the general 'technical' category
    # but keep them categorized internally if needed.
    return {
        "technical": found_tech + found_banking + found_hr + found_marketing,
        "soft": found_soft,
        "domains": {
            "tech": found_tech,
            "banking": found_banking,
            "hr": found_hr,
            "marketing": found_marketing
        }
    }
