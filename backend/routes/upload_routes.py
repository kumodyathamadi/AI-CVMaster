from flask import Blueprint, request, jsonify
from utils.validators import validate_file
from services.file_service import save_file
from config import config
from services.pdf_extractor import extract_text_from_pdf
from services.resume_parser import parse_resume_text
from services.resume_scorer import calculate_scores, generate_insights
from services.job_matcher import match_job_description
from utils.db import get_db
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
        file_path = os.path.join(config.UPLOAD_FOLDER, filename)
        
        # 1. Extract text from PDF
        resume_text = extract_text_from_pdf(file_path)
        print(f"Extracted {len(resume_text)} characters from {filename}")
        if len(resume_text) > 0:
            print(f"Text Snippet: {resume_text[:200]}...")
        
        # 2. Parse information
        parsed_data = parse_resume_text(resume_text)
        
        # 3. Calculate Scores
        scores = calculate_scores(parsed_data)
        
        # 4. Generate Insights
        insights = generate_insights(parsed_data)
        
        # Full Analysis Object
        analysis_data = {
            **scores,
            "candidate": {
                "name": parsed_data.get("name"),
                "email": parsed_data.get("email"),
                "phone": parsed_data.get("phone"),
                "links": parsed_data.get("links")
            },
            "skills": parsed_data.get("skills"),
            "experience": parsed_data.get("experience"),
            "education": parsed_data.get("education"),
            "recommendations": insights.get("recommendations"),
            "career_prediction": insights.get("career_prediction")
        }
        
        # Save metadata and parsed data to MongoDB
        db = get_db()
        if db is not None:
            resume_data = {
                "filename": filename,
                "original_name": original_filename,
                "upload_date": datetime.utcnow(),
                "status": "processed",
                "file_path": file_path,
                "analysis": analysis_data
            }
            db.resumes.insert_one(resume_data)
        
        # Return the expected JSON response format
        return jsonify({
            "success": True,
            "message": "Resume analyzed successfully",
            "data": analysis_data
        }), 201
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }), 500
