# tests/conftest.py
import os
import pytest
from lab_results_app.flask_app import app as flask_app
from lab_results_app.database_helpers import connect_to_database
import shutil

@pytest.fixture
def client():
    """
    Provides a Flask test client for route testing.
    """
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def temp_db(tmp_path):
    """
    Creates a temporary SQLite database file in a pytest-provided temp directory.
    Yields the path, and cleans up after tests finish.
    """
    db_path = tmp_path / "test_results.db"
    os.environ["LAB_APP_DB_PATH"] = str(db_path)

    connect_to_database()
    yield ("USING_TEMP_PATH", db_path)

    # Cleanup is automatic since tmp_path is ephemeral

@pytest.fixture
def sample_copies_dir(tmp_path, request):
    # Use this hack to get the original path of the samples folder
    filename = request.module.__file__
    test_dir = os.path.dirname(filename)
    from_samples = os.path.join(test_dir, "samples")
    to_samples = tmp_path / "samples"
    shutil.copytree(from_samples, to_samples)
    print(from_samples, to_samples)
    yield to_samples

