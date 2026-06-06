# AI Resume Analyzer - Backend

Flask REST API for handling resume uploads and (future) AI analysis.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python app.py
    ```

## API Endpoints

### POST /api/upload
Uploads a resume file (PDF only, max 10MB).
Returns a JSON response with success status and filename.
