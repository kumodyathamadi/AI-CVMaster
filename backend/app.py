from flask import Flask
from flask_cors import CORS
from config import config
from routes.upload_routes import upload_bp
from services.pdf_extractor import extract_text_from_pdf
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    from utils.db import get_db
    # Register Blueprints
    app.register_blueprint(upload_bp, url_prefix='/api')
    
    # Initialize DB connection
    with app.app_context():
        get_db()
    
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)