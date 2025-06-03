# --- File: scripts/dashboard_app.py ---

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv() # Load .env variables at the very beginning

# IMPORTANT CHANGE: Only import summarize_job as get_chat_response is no longer needed
from .llm_utils import summarize_job

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
# Define the path for the SQLite database file
# This must match SQLALCHEMY_DATABASE_URI in config.py
DB_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DB_DIR, exist_ok=True) # Ensure the data directory exists

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
# Import Config from the root directory
import sys
sys.path.insert(0, BASE_DIR) # Add project root to path for importing config
from config import Config
app.config.from_object(Config)

db = SQLAlchemy(app)

# Define your Job model
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.String(50))
    company = db.Column(db.String(255))
    position = db.Column(db.String(255))
    job_type = db.Column(db.String(50))
    location = db.Column(db.String(255))
    url = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    summary = db.Column(db.Text)

    def __repr__(self):
        return f'<Job {self.id} {self.position}>'

# --- Database Initialization (for SQLite) ---
# This block ensures tables are created when the app starts
with app.app_context():
    # For SQLite, db.create_all() will create the database file and tables if they don't exist
    print("Ensuring SQLite database and tables exist...")
    db.create_all()
    print("Database setup complete.")

@app.route('/')
def index():
    """Renders the main job listing dashboard."""
    jobs = Job.query.order_by(Job.date_posted.desc()).all()
    return render_template('index.html', jobs=jobs)

@app.route('/run-scrape')
def run_scrape():
    """
    Triggers the job scraping and summarization process.
    This is a simplified way to trigger from the web.
    In a real app, this might be an async task or a CLI command.
    """
    print("Scraping and summarization initiated via web request...")
    return "Scraping and summarization initiated. Please run 'make scrape' and 'make enrich-db' in your terminal.", 200

# Removed chatbot routes: /chatbot and /chat

if __name__ == '__main__':
    app.run(debug=True)
