# config.py

import os

# Define BASE_DIR here so it's accessible within this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # This points to the project root

class Config:
    # SQLite database URI
    # This will create a 'jobs.db' file inside a 'data' directory in your project root
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "data", "jobs.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Suppress warning

    # Ensure OPENAI_API_KEY is loaded from .env or system environment
    # It's accessed directly in scripts/llm_utils.py using os.getenv()
