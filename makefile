#----- MAKEFILE -------
.PHONY: all scrape enrich-db run-dashboard clean

all: scrape enrich-db run-dashboard

scrape:
	python3 scripts/remoteok_scraper.py

enrich-db:
	python3 scripts/db_enricher.py $(LIMIT)

run-dashboard:
	# IMPORTANT CHANGE: Use dot (.) instead of slash (/) for module path
	
	FLASK_APP=scripts.dashboard_app flask run --debug

clean:
	rm -f data/jobs.db # Remove the SQLite database file
	rm -rf output/ # Clean up any other output directories if they exist