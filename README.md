# Job_Tracker
A makefile that web-scrapes into SQLite databse, calling upon OpenAI API for automated summaries, and deploying locally with Flask
Overview of the project:

1. Scrape Job Postings: The system automatically fetches job data from online sources (used RemoteOK.com in this Python script). Call with make-scrape

2. Store Raw Data: The scraped job details are initially saved into a local SQLite database (data/jobs.db). An empty data folder is needed.

3. Enrich with AI Summaries: An AI model (OpenAI's GPT-3.5-turbo) reads the job descriptions and generates concise summaries for each, which are then added back to the SQLite database. Call with make enrich-db. An OpenAI API key is needed in .env
   
4. Manage Data: All raw and summarised job information is persistently stored and managed within the SQLite database.
   
5. Display on Dashboard: A Flask web application provides a user-friendly dashboard (http://localhost:5000) where you can view all the scraped jobs and their AI-generated summaries.


Project Structure:

Job_Tracker/
├── .venv/                   # Python Virtual Environment (isolated dependencies)

├── data/                    # Stores the SQLite database file (jobs.db)

│   └── jobs.db              # The actual SQLite database file

├── scripts/                 # Contains all Python backend logic

│   ├── __init__.py          # (Empty file) Marks 'scripts' as a Python package

│   ├── dashboard_app.py     # Main Flask application, defines DB model, web routes

│   ├── db_enricher.py       # Summarizes job descriptions using AI

│   ├── llm_utils.py         # Handles OpenAI API calls (for summarization)

│   └── remoteok_scraper.py  # Fetches job data from online sources

├── templates/               # HTML templates for the web interface

│   └── index.html           # Main dashboard UI to display jobs

├── .env                     # Stores environment variables (e.g., OPENAI_API_KEY)

├── .gitignore               # Tells Git which files/folders to ignore

├── config.py                # Application configuration settings (e.g., database URI)

├── Makefile                 # Automation script for common tasks (scrape, enrich, run, clean)

└── requirements.txt         # Lists all Python package dependencies

The html formatting end result:

<img width="1109" alt="Screenshot 2025-06-03 at 11 51 04" src="https://github.com/user-attachments/assets/87f7c075-537d-447f-a6a5-23652653101e" />
