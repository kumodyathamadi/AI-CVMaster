from flask import Flask
from flask_cors import CORS
from backend.config import config
from backend.routes.upload_routes import upload_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register Blueprints
    app.register_blueprint(upload_bp, url_prefix='/api')
    
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
