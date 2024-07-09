import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit.
    
    # Vertex AI configuration
    VERTEX_PROJECT_ID = os.environ.get('VERTEX_PROJECT_ID')
    VERTEX_LOCATION = os.environ.get('VERTEX_LOCATION', 'us-central1')
    VERTEX_MODEL_NAME = os.environ.get('VERTEX_MODEL_NAME', 'gemini-1.5-flash-001')