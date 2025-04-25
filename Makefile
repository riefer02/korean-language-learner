# Define the Python interpreter from the virtual environment
PYTHON = venv/bin/python
PIP = venv/bin/pip

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install    - Set up virtual environment and install dependencies"
	@echo "  run        - Run the script interactively (prompts for phrase)"
	@echo "  runp       - Run the script with a phrase (e.g., make runp phrase=\"Hello world\")"
	@echo "  clean      - Remove generated files and directories"

# Target to set up the environment
.PHONY: install
install: venv/bin/activate

venv/bin/activate:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Virtual environment created and dependencies installed."

# Target to run the script interactively
.PHONY: run
run: install
	$(PYTHON) hangul.py

# Target to run the script with a specific phrase
.PHONY: runp
runp: install
	@if [ -z "$(phrase)" ]; then \
		echo "Error: Please provide a phrase. Usage: make runp phrase=\"Your phrase here\""; \
		exit 1; \
	fi
	$(PYTHON) hangul.py "$(phrase)"

# Target to clean generated files
.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf venv
	rm -rf audio_output
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	@echo "Cleanup complete." 