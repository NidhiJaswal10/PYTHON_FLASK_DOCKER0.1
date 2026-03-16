import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    """Setup the test client for all test cases"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# --- 1. THE HAPPY PATHS (Normal Functionality) ---

def test_home_page(client):
    """Checks if Home page loads successfully (200 OK)"""
    response = client.get("/")
    assert response.status_code == 200

def test_welcome_page(client):
    """Checks if Welcome page loads successfully (200 OK)"""
    response = client.get("/welcome")
    assert response.status_code == 200

# --- NEW: DATABASE GET TEST ---
def test_getpost_view_ratings(client):
    """Checks if the GETPOST page fetches data from DB"""
    # We mock the database connection to return fake rows
    with patch("app.get_db_connection") as mocked_db:
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchall.return_value = [("Inception", "Great"), ("Batman", "Dark")]
        mocked_db.return_value = mock_conn

        response = client.get("/GETPOST")
        assert response.status_code == 200
        assert b"Inception" in response.data
        assert b"Batman" in response.data

# --- NEW: DATABASE POST TEST ---
def test_add_rating_database_logic(client):
    """Checks if submitting the form sends data to the DB"""
    with patch("app.get_db_connection") as mocked_db:
        mock_conn = MagicMock()
        mocked_db.return_value = mock_conn
        
        # Simulating the form submission
        response = client.post("/add-rating", data={
            "movie_name": "Interstellar",
            "feedback": "Masterpiece"
        })
        
        assert response.status_code == 200
        assert b"Successfully added Interstellar" in response.data

# --- EXISTING MOCKING TEST ---

def test_movies_nidhi_mocked(client):
    """Bypass slow function using mock"""
    with patch("app.getNetflixMovies") as mocked_api:
        mocked_api.return_value = ["Stranger Things", "Dark"]
        response = client.get("/movies/Nidhi")
        assert response.status_code == 200
        mocked_api.assert_called_once_with("Nidhi")

# --- 2. THE EDGE CASES (Boundary Value Analysis) ---

def test_getpost_empty_name(client):
    """Checks what happens if the name field is empty"""
    # Note: Your HTML has 'required', but we test the backend here
    response = client.post("/add-rating", data={"movie_name": "", "feedback": ""})
    assert response.status_code == 200

def test_getpost_numeric_name(client):
    """Checks if numbers are accepted as a name"""
    response = client.post("/add-rating", data={"movie_name": "12345", "feedback": "Good"})
    assert response.status_code == 200

# --- 3. NEGATIVE & SECURITY CASES (Error Handling) ---

def test_page_not_found(client):
    """Verifies that a random URL returns a 404 error"""
    response = client.get("/this-page-does-not-exist")
    assert response.status_code == 404

def test_getpost_method_not_allowed(client):
    """Checks if calling a route with the wrong method fails"""
    response = client.post("/welcome")
    assert response.status_code == 405