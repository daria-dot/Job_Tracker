# Job_Tracker
A makefile that web-scrapes into SQLite databse, calling upon OpenAI API for automated summaries, and deploying locally with Flask
Overview of the project:

1. Scrape Job Postings: The system automatically fetches job data from online sources (used RemoteOK.com in this Python script). Call with make-scrape

2. Store Raw Data: The scraped job details are initially saved into a local SQLite database (data/jobs.db). An empty data folder is needed.

3. Enrich with AI Summaries: An AI model (OpenAI's GPT-3.5-turbo) reads the job descriptions and generates concise summaries for each, which are then added back to the SQLite database. Call with make enrich-db. An OpenAI API key is needed in .env
   
4. Manage Data: All raw and summarised job information is persistently stored and managed within the SQLite database.
   
5. Display on Dashboard: A Flask web application provides a user-friendly dashboard (http://localhost:5000) where you can view all the scraped jobs and their AI-generated summaries.


Project Structure:
