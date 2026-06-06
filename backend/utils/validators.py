from backend.config import config

def allowed_file(filename):
    """
    Check if the file extension is allowed.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def validate_file(file):
    """
    Validate the uploaded file: checks if it exists, is a PDF, and is within size limits.
    Returns: (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No selected file"
    
    if not allowed_file(file.filename):
        return False, "Only PDF files are allowed"
    
    # Check size (Werkzeug's FileStorage doesn't provide easy size access before reading, 
    # but MAX_CONTENT_LENGTH in Flask config handles this globally)
    # However, for a more explicit check if needed:
    # file.seek(0, 2)
    # size = file.tell()
    # file.seek(0)
    # if size > config.MAX_CONTENT_LENGTH:
    #     return False, "File size exceeds 10MB limit"
        
    return True, None
