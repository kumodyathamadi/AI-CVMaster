import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit
    ALLOWED_EXTENSIONS = {'pdf'}
    MONGODB_URI = os.environ.get('MONGODB_URI')
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'resume_analyzer')

config = Config()
