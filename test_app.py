import pytest
from unittest.mock import patch # <--- Yeh line top par add karein
from app import app 

@pytest.fixture
def client():
    """Setup the test client for all test cases"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- 1. THE HAPPY PATHS (Normal Functionality) ---

def test_home_page(client):
    """Checks if Home page loads successfully (200 OK)"""
    response = client.get('/')
    assert response.status_code == 200
    # assert b"REST API" in response.data # Isse check kar lein agar HTML mein hai

def test_welcome_page(client):
    """Checks if Welcome page loads successfully (200 OK)"""
    response = client.get('/welcome')
    assert response.status_code == 200

def test_getpost_submission_valid(client):
    """Checks if a standard name submission works"""
    response = client.post('/GETPOST', data={'name': 'Nidhi'})
    assert response.status_code == 200
    assert b"Hello, Nidhi!" in response.data

# --- NEW: MOCKING TEST (Isse aapke app ka slow function bypass ho jayega) ---

def test_movies_nidhi_mocked(client):
    """
    Scenario: 'Nidhi' ke liye movies check karna.
    Hum 'getNetflixMovies' ko mock karenge taaki 5 second ka wait na karna pade.
    """
    # 'app.getNetflixMovies' ko patch kar rahe hain
    with patch('app.getNetflixMovies') as mocked_api:
        # Fake data set kar diya
        mocked_api.return_value = ["Stranger Things", "Dark"]
        
        response = client.get('/movies/Nidhi')
        
        assert response.status_code == 200
        # Verification: Kya function call hua?
        mocked_api.assert_called_once_with('Nidhi')

# --- 2. THE EDGE CASES (Boundary Value Analysis) ---

def test_getpost_empty_name(client):
    """Checks what happens if the name field is empty"""
    response = client.post('/GETPOST', data={'name': ''})
    assert response.status_code == 200
    assert b"Hello, !" in response.data

def test_getpost_numeric_name(client):
    """Checks if numbers are accepted as a name"""
    response = client.post('/GETPOST', data={'name': '12345'})
    assert response.status_code == 200
    assert b"Hello, 12345!" in response.data

def test_getpost_special_characters(client):
    """Checks if symbols/emojis are accepted"""
    response = client.post('/GETPOST', data={'name': '@#$% 😊'})
    assert response.status_code == 200
    assert b"Hello, @#$% \xf0\x9f\x98\x8a!" in response.data

# --- 3. NEGATIVE & SECURITY CASES (Error Handling) ---

def test_page_not_found(client):
    """Verifies that a random URL returns a 404 error"""
    response = client.get('/this-page-does-not-exist')
    assert response.status_code == 404

def test_getpost_method_not_allowed(client):
    """Checks if calling a route with the wrong method fails"""
    response = client.post('/welcome')
    assert response.status_code == 405 

def test_getpost_missing_payload(client):
    """Checks what happens if the 'name' key is missing entirely"""
    response = client.post('/GETPOST', data={})
    # Aapka app abort(400) karta hai
    assert response.status_code == 400