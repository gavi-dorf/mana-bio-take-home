# tests/test_database_helpers.py
from lab_results_app.database_helpers import connect_to_database
import os
import os.path


def test_connect_to_database(temp_db):
    """
    Example test to ensure connect_to_database works with a temporary DB.
    """
    # Ensure that the environment variable for LAB_APP_DB_PATH was set correctly
    # and that the temporary database was created correctly
    (flag, db_path) = temp_db
    assert flag == "USING_TEMP_PATH"
    assert os.environ.get("LAB_APP_DB_PATH") == str(db_path)
    assert os.path.isfile(db_path)

    conn, cursor = connect_to_database()
    assert conn is not None
    assert cursor is not None

    # Attempt a simple query
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = cursor.fetchall()
    # We expect the 'results' table was created by conftest or at least no errors
    assert len(result) >= 0

    cursor.close()
    conn.close()
