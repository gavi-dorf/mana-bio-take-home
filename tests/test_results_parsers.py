# tests/test_results_parsers.py
import lab_results_app.results_parsers as results_parsers
import pytest
import os

def test_parse_file(temp_db, sample_copies_dir):
    """
    Test that the results_parsers.parse_file function works correctly 
    """
    # Ensure that the environment variable for LAB_APP_DB_PATH was set correctly
    # and that the temporary database was created correctly
    (flag, db_path) = temp_db
    assert flag == "USING_TEMP_PATH"
    assert os.environ.get("LAB_APP_DB_PATH") == str(db_path)
    assert os.path.isfile(db_path)

    samples = [os.path.join(sample_copies_dir, file) for file in os.listdir(sample_copies_dir)]
    for sample_file in samples:
        if "invalid" in sample_file: 
            with pytest.raises(results_parsers.ResultsParsingError):
                results_parsers.parse_file(sample_file)
        elif "valid" in sample_file:
            # Iterate over each tuple in the return value and 
            for (formulation_id, calculated_value) in results_parsers.parse_file(sample_file):
                assert isinstance(formulation_id, str)
                assert isinstance(calculated_value, (int, float)) and not isinstance(calculated_value, bool)
        else:
            raise Exception("Invalid test sample file name! {}".format(sample_file))
    