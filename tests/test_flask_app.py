def test_index_route(client):
    """
    Tests the index route and checks if the page renders successfully
    (status code 200) and contains expected content.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Select an experiment type" in response.data  # e.g., if your template includes this text

def test_upload_route_get(client):
    """
    Tests accessing the upload page via GET.
    """
    response = client.get("/upload-new-results")

    assert response.status_code == 200
    assert b"<h1>Upload a new results file</h1>" in response.data  # check for specific page text

def test_upload_route_post_no_file(client):
    """
    Tests a POST to the upload route with no file - should handle gracefully.
    """
    response = client.post("/upload-new-results", data={})
    assert response.status_code == 200 
    assert b"<h1>Upload a new results file</h1>" in response.data
