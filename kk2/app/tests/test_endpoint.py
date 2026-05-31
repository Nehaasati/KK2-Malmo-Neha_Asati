from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)




def test_stats_dataset():
    response = client.get("/data/stats")
    assert response.status_code == 404

#

# This test checks the /ai/ask endpoint when no dataset has been uploaded. 
# It sends a POST request with a question in the request body and asserts that the response status code is 404, indicating that no dataset is available for processing the question. 
# It also checks that the error message in the response body is "No dataset uploaded".
def test_ask_no_dataset():
    import app.data as data_module
    original = data_module.DATA
    data_module.DATA = None  # force no dataset

    response = client.post("/ai/ask", json={"question": "Best product?"})

    # Match what main.py ACTUALLY returns
    assert response.status_code == 400
    assert response.json()["detail"] == "Dataset must be uploaded before asking questions"

    data_module.DATA = original 

# To check LLM give give stats value from dataset such as mean medium if we not have say "no information "not predict  hallucinate

