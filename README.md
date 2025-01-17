# Setup
1. Install uv (See instructions here: https://github.com/astral-sh/uv)
2. `cd` into the project directory for this repo
3. Run `uv venv`
4. Run `source .venv/bin/activate` to enter the virtual environment shell 
5. Run `uv sync`
6. Run `uv run main.py` to start the webserver on port 5000
# Testing
1. `cd` into the project directory for this repo
2. Run `uv venv`
3. Run `source .venv/bin/activate` to enter the virtual environment shell 
4. Run `uv sync`
5. Run `uv run pytest -s` to run the test suite

# Usage
## Uploading New Results (/upload-new-results endpoint)
1. Upload a results file
2. Validate the data:
If errors are found, an error message will be displayed
If no errors are found:
1. The results are stored in the database
2. The newly uploaded results are displayed
## Exploring Stored Results 
1. Access the index page ("/") which will show all stored results, grouped by experiment type.
2. Select an experiment type to view:
- Overall statistics: median, average, and standard deviation.
- A table of results with columns: formulation_id and calculated_value.