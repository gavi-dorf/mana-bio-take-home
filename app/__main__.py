"""
Flask Application for Processing and Analyzing Experimental Results

This module implements a web application for uploading, storing, and analyzing experimental 
results data. It provides functionality to:
- Upload new experimental results files
- View existing results filtered by experiment type
- Calculate basic statistical measures for experimental results
- Store results in a database

The application uses Flask for web handling, Polars for data analysis, and SQLite for 
data persistence.

Dependencies:
    - Flask: Web framework
    - Polars: Data analysis library
    - results_parsers: Custom module for parsing experimental results
    - database_helpers: Custom module for database operations
    - uuid: For generating unique filenames
    - os: For file and directory operations
    - datetime: For timestamp generation
"""

from flask import Flask, render_template, request
import os
import os.path
import results_parsers
import uuid
from datetime import datetime
import database_helpers
import polars as pl
from typing import List, Tuple, Dict, Optional
from pathlib import Path

# Configure application paths
template_dir: Path = Path('templates').absolute()
app: Flask = Flask(__name__, template_folder=str(template_dir))

# Configure file upload settings
upload_dir: str = "file_uploads/"
app.config['UPLOAD_FOLDER'] = upload_dir


@app.route("/")
def index() -> str:
    """
    Main route handler for the application's index page.
    
    Displays experimental results and provides filtering capabilities by experiment type.
    Calculates summary statistics for filtered results using Polars.
    
    Query Parameters:
        experiment_type (str, optional): Type of experiment to filter results by
        
    Returns:
        str: Rendered HTML template with experiment data and statistics
        
    Database Schema Expected:
        Table 'results' with columns:
        - experiment_type (str): Type of experiment
        - formulation_id (str): Unique identifier for the formulation
        - calculated_value (float): Numerical result value
    """
    experiment_type: Optional[str] = request.args.get('experiment_type', '')

    # Database connection
    (_, cursor) = database_helpers.connect_to_database()

    try:
        # Fetch distinct experiment types for filtering
        experiment_types: List[str] = [
            row[0] for row in cursor.execute(
                "SELECT DISTINCT experiment_type FROM results ORDER BY experiment_type;"
            ).fetchall()
        ]

        # Fetch filtered results if experiment_type is provided
        filtered_results: List[Tuple[str, float]] = []
        if experiment_type:
            filtered_results = cursor.execute(
                "SELECT formulation_id, calculated_value FROM results WHERE experiment_type = ?;",
                (experiment_type,)
            ).fetchall()

    finally:
        # Always close the database connection
        cursor.connection.close()

    # Convert results to Polars DataFrame for statistical analysis
    df: pl.DataFrame = pl.DataFrame(
        filtered_results, 
        orient="row", 
        schema=["formulation_id", "calculated_value"]
    )

    # Calculate summary statistics
    calculated_value = df.select(pl.col("calculated_value"))
    mean: float = calculated_value.mean().item() if len(df) > 0 else 0.0
    median: float = calculated_value.median().item() if len(df) > 0 else 0.0
    standard_deviation: float = calculated_value.std().item() if len(df) > 0 else 0.0

    # For debugging purposes
    print(f"Summary Stats - Mean: {mean}, Median: {median}, StdDev: {standard_deviation}")

    return render_template(
        "index.html",
        experiment_types=experiment_types,
        experiment_type=experiment_type,
        results=filtered_results,
        summary_stats={
            "mean": mean,
            "median": median,
            "standard_deviation": standard_deviation
        }
    )


@app.route("/upload-new-results", methods=["GET", "POST"])
def upload_new_results() -> str:
    """
    Handles file uploads for new experimental results.
    
    Supports both GET (display form) and POST (process upload) methods.
    Temporarily stores uploaded files, processes them, and then removes them.
    
    Returns:
        str: Rendered HTML template with upload results or error message
        
    File Processing:
        1. Generates unique filename using UUID
        2. Temporarily saves file
        3. Processes file using results_parsers module
        4. Removes temporary file
        5. Returns results or error message
    """
    results: Optional[Dict] = None
    error_message: Optional[str] = None
    
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            upload_timestamp: datetime = datetime.now()
            root, ext = os.path.splitext(file.filename)
            filename: str = f"{root}{str(uuid.uuid4())}{ext}"
            filepath: str = os.path.join(upload_dir, filename)

            # Ensure upload directory exists
            os.makedirs(upload_dir, exist_ok=True)

            try:
                # Save and process file
                file.save(filepath)
                results = results_parsers.parse_file(
                    filepath,
                    upload_timestamp
                )
            except Exception as e:
                error_message = f"Error processing file: {str(e)}"
            finally:
                # Clean up temporary file
                if os.path.exists(filepath):
                    os.remove(filepath)

    return render_template(
        "upload.html",
        results=results,
        error_message=error_message
    )

def run() -> None:
    """
    Application entry point when run directly.
    
    Performs initial setup:
    1. Verifies database connection
    2. Creates upload directory if needed
    3. Starts Flask development server
    """
    # Verify database connection works
    connection, cursor = database_helpers.connect_to_database()
    cursor.connection.close()
    
    # Ensure upload directory exists
    os.makedirs(upload_dir, exist_ok=True)
    
    # Start development server
    app.run(debug=True)

if __name__ == "__main__":
    run()