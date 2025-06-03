
# --- File: scripts/remoteok_scraper.py ---

import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv() # Load .env variables

# Add parent directory to sys.path to import dashboard_app correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.dashboard_app import app, db, Job # Import app, db, and Job model

def fetch_jobs_from_remoteok():
    url = "https://remoteok.com/api"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors
        jobs_data = response.json()

        # The first item in the list is usually a metadata object, skip it
        if jobs_data and isinstance(jobs_data, list) and len(jobs_data) > 0 and 'api_version' in jobs_data[0]:
            jobs_data = jobs_data[1:] # Skip the metadata object

        processed_jobs = []
        for job in jobs_data:
            processed_jobs.append({
                'date_posted': job.get('date'),
                'company': job.get('company'),
                'position': job.get('position'),
                'job_type': job.get('job_type'),
                'location': job.get('location'),
                'url': job.get('url'),
                'description': job.get('description')
            })
        return processed_jobs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs from RemoteOK: {e}")
        return []

def save_jobs_to_sqlite(jobs):
    print(f"Saving {len(jobs)} jobs to SQLite...")
    with app.app_context(): # Ensure we are in Flask app context for db operations
        for job_data in jobs:
            # Check if job already exists by URL to prevent duplicates
            existing_job = Job.query.filter_by(url=job_data['url']).first()
            if existing_job:
                # You could update existing_job with new data if applicable
                continue

            new_job = Job(
                date_posted=job_data.get('date_posted'),
                company=job_data.get('company'),
                position=job_data.get('position'),
                job_type=job_data.get('job_type'),
                location=job_data.get('location'),
                url=job_data.get('url'),
                description=job_data.get('description'),
                summary=None # Summary is null initially
            )
            db.session.add(new_job)
        try:
            db.session.commit()
            print(f"Successfully saved {len(jobs)} new jobs to SQLite.")
        except Exception as e:
            db.session.rollback()
            print(f"Error saving jobs to SQLite: {e}")
    print("\nRun 'make enrich-db' to generate summaries for new jobs.")


if __name__ == "__main__":
    print("Fetching jobs from Remote OK...")
    jobs = fetch_jobs_from_remoteok()
    print(f"Fetched {len(jobs)} jobs.")
    save_jobs_to_sqlite(jobs)
