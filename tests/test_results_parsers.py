# tests/test_results_parsers.py
import lab_results_app.results_parsers as results_parsers
import os

def test_parse_file(temp_db, sample_copies_dir):
    # Ensure that the environment variable for LAB_APP_DB_PATH was set correctly
    # and that the temporary database was created correctly
    (flag, db_path) = temp_db
    assert flag == "USING_TEMP_PATH"
    assert os.environ.get("LAB_APP_DB_PATH") == str(db_path)
    assert os.path.isfile(db_path)

    samples = [os.path.join(sample_copies_dir, file) for file in os.listdir(sample_copies_dir)]
    for sample in samples:
        results_parsers.parse_file(sample)
    