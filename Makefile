# Define the Python interpreter from the virtual environment
PYTHON = venv/bin/python
PIP = venv/bin/pip

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install    - Set up virtual environment and install dependencies"
	@echo "  run        - Run the CLI script interactively (prompts for phrase)"
	@echo "  runp       - Run the CLI script with a phrase (e.g., make runp phrase=\"Hello world\")"
	@echo "  web        - Run the web application"
	@echo "  init-db    - Initialize the database"
	@echo "  clean      - Remove generated files and directories"
	@echo "  backup-db  - Backup the database"

# Target to set up the environment
.PHONY: install
install: venv/bin/activate

venv/bin/activate:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Virtual environment created and dependencies installed."

# Target to run the CLI script interactively
.PHONY: run
run: install
	$(PYTHON) hangul.py

# Target to run the CLI script with a specific phrase
.PHONY: runp
runp: install
	@if [ -z "$(phrase)" ]; then \
		echo "Error: Please provide a phrase. Usage: make runp phrase=\"Your phrase here\""; \
		exit 1; \
	fi
	$(PYTHON) hangul.py "$(phrase)"

# Target to run the web application
.PHONY: web
web: install
	$(PYTHON) run.py

# Target to initialize the database
.PHONY: init-db
init-db: install
	FLASK_APP=run.py $(PYTHON) -m flask init-db

# Target to backup the database
.PHONY: backup-db
backup-db:
	@mkdir -p backups
	@cp korean_learner.db backups/korean_learner_$(shell date +%Y%m%d%H%M%S).db
	@echo "Database backed up to backups/ directory"

# Target to clean generated files
.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf venv
	rm -rf audio_output
	rm -rf app/static/audio/*
	rm -f korean_learner.db
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	@echo "Cleanup complete." 