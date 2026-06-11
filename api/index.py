import os
import sys

# Add the project root and backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.app import app

# Vercel's Python runtime expects 'app' to be exposed at the module level
# Our backend/app.py creates 'app' at the module level, so it should work.
