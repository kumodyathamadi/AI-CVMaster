def extract_skills(text):
    """
    Extracts technical and soft skills from the given text.
    """
    technical_skills_list = [
        'Python', 'Java', 'React', 'Node.js', 'SQL', 'MongoDB', 'Docker', 
        'AWS', 'Git', 'Machine Learning', 'Deep Learning', 'HTML', 'CSS', 
        'JavaScript', 'TypeScript', 'Express', 'Flask', 'Django', 'PostgreSQL',
        'Redis', 'Kubernetes', 'TensorFlow', 'PyTorch', 'C++', 'C#', 'PHP',
        'Azure', 'GCP', 'NoSQL', 'REST API', 'GraphQL', 'Microservices'
    ]
    
    soft_skills_list = [
        'Leadership', 'Communication', 'Problem Solving', 'Teamwork', 
        'Time Management', 'Creativity', 'Adaptability', 'Critical Thinking',
        'Project Management', 'Public Speaking', 'Analytical Skills'
    ]
    
    found_tech_skills = []
    found_soft_skills = []
    
    text_lower = text.lower()
    
    for skill in technical_skills_list:
        if skill.lower() in text_lower:
            found_tech_skills.append(skill)
            
    for skill in soft_skills_list:
        if skill.lower() in text_lower:
            found_soft_skills.append(skill)
            
    return {
        "technical": found_tech_skills,
        "soft": found_soft_skills
    }
