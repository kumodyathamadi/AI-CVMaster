import os
from werkzeug.utils import secure_filename

def get_unique_filename(directory, filename):
    """
    Generates a unique filename by appending a counter if the file already exists.
    Example: resume.pdf -> resume_1.pdf -> resume_2.pdf
    """
    name, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{name}_{counter}{ext}"
        counter += 1
        
    return unique_filename

def save_file(file, upload_dir):
    """
    Saves the file to the specified directory with a secure and unique filename.
    """
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    filename = secure_filename(file.filename)
    unique_filename = get_unique_filename(upload_dir, filename)
    file_path = os.path.join(upload_dir, unique_filename)
    
    file.save(file_path)
    return unique_filename
