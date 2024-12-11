import requests

BASE_URL = "http://127.0.0.1:8080"

def test_home_route():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200, "Home route did not return 200 OK"
    assert response.json() == {"message": "Welcome to the prototype backend!"}, "Unexpected response message"

if __name__ == "__main__":
    print("Starting tests for Iteration 1...")
    test_home_route()
    print("All tests passed!")