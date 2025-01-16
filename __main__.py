from flask import Flask, render_template, request
import os
import os.path
import results_parsers
import uuid
from datetime import datetime
import database_helpers

template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)

upload_dir = "file_uploads/"
app.config['UPLOAD_FOLDER'] = upload_dir


@app.route("/")
def index():
    experiment_type = request.args.get('experiment_type', '')

    # Database connection
    (_, cursor) = database_helpers.connect_to_database()

    # Fetch distinct experiment types
    experiment_types = [
        row[0] for row in cursor.execute(
            "SELECT DISTINCT experiment_type FROM results ORDER BY experiment_type;"
        ).fetchall()
    ]

    # Fetch filtered results if experiment_type is provided
    filtered_results = []
    if experiment_type:
        filtered_results = cursor.execute(
            "SELECT formulation_id, calculated_value FROM results WHERE experiment_type = ?;",
            (experiment_type, )).fetchall()

    # Always close the database connection
    cursor.connection.close()

    return render_template(
        "index.html",
        experiment_types=experiment_types,
        experiment_type=experiment_type,
        results=filtered_results,
    )


@app.route("/upload-new-results", methods=["GET", "POST"])
def upload_new_results():
    results = None
    error_message = None
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            upload_timestamp = datetime.now()
            (root, ext) = os.path.splitext(file.filename)
            filename = root + str(uuid.uuid4()) + ext
            filepath = os.path.join(upload_dir, filename)

            os.makedirs(upload_dir, exist_ok=True)

            try:
                file.save(filepath)
                results = results_parsers.parse_file(filepath,
                                                     upload_timestamp)
            except Exception as e:
                error_message = str(e)
            finally:
                os.remove(filepath)

    return render_template("upload.html",
                           results=results,
                           error_message=error_message)


if __name__ == "__main__":
    (_, cursor) = database_helpers.connect_to_database()
    cursor.connection.close()
    os.makedirs(upload_dir, exist_ok=True)
    app.run(debug=True)
