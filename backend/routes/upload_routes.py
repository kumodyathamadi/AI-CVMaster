from flask import Blueprint, request, jsonify
from backend.utils.validators import validate_file
from backend.services.file_service import save_file
from backend.config import config
from backend.utils.db import get_db
from datetime import datetime
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_resume():
    """
    Endpoint for uploading a resume.
    Validates the file, saves it securely, and stores metadata in MongoDB.
    """
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "message": "No file part in the request"
        }), 400
        
    file = request.files['file']
    original_filename = file.filename
    
    # Validate file
    is_valid, error_message = validate_file(file)
    if not is_valid:
        return jsonify({
            "success": False,
            "message": error_message
        }), 400
        
    try:
        # Save file to disk
        filename = save_file(file, config.UPLOAD_FOLDER)
        
        # Save metadata to MongoDB
        db = get_db()
        if db is not None:
            resume_data = {
                "filename": filename,
                "original_name": original_filename,
                "upload_date": datetime.utcnow(),
                "status": "uploaded",
                "file_path": os.path.join(config.UPLOAD_FOLDER, filename)
            }
            db.resumes.insert_one(resume_data)
            print(f"Metadata for {filename} saved to MongoDB.")
        else:
            print("Warning: Metadata NOT saved to MongoDB (DB connection failed).")
        
        return jsonify({
            "success": True,
            "filename": filename,
            "message": "Resume uploaded and metadata stored successfully"
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred during file upload: {str(e)}"
        }), 500
