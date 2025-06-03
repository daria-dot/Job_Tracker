

# --- File: scripts/db_enricher.py ---

import os
import sys
import time
import logging
from dotenv import load_dotenv

load_dotenv() # Load .env variables

# Add parent directory to sys.path to import dashboard_app correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.dashboard_app import app, db, Job # Import app, db, and Job model
from scripts.llm_utils import summarize_job # Import summarize_job

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def enrich_jobs_with_summary(limit=None):
    logging.info("Starting job summarization...")
    with app.app_context():
        query = Job.query.filter(
            Job.summary.is_(None),
            Job.description.isnot(None),
            Job.description != ''
        )
        if limit:
            jobs_to_summarize = query.limit(limit).all()
        else:
            jobs_to_summarize = query.all()

        if not jobs_to_summarize:
            logging.info("No new jobs to summarize.")
            return

        jobs_processed_count = 0
        for job in jobs_to_summarize:
            logging.info(f"Summarizing job ID: {job.id} - '{job.position}' by {job.company}...")
            summary_text = summarize_job(job.description)

            if summary_text:
                job.summary = summary_text
                db.session.add(job)
                try:
                    db.session.commit()
                    jobs_processed_count += 1
                    logging.info(f"Updated job {job.id}")
                except Exception as e:
                    db.session.rollback()
                    logging.error(f"Error committing summary for job ID {job.id}: {e}")
            else:
                logging.warning(f"Could not generate summary for job ID: {job.id}")

    logging.info(f"Finished summarizing {jobs_processed_count} jobs.")

if __name__ == "__main__":
    summary_limit = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        summary_limit = int(sys.argv[1])
        print(f"Summarizing up to {summary_limit} jobs.")
    else:
        print("Summarizing all new jobs.")

    enrich_jobs_with_summary(limit=summary_limit)
