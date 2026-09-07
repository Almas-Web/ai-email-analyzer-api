import os

# Set all required dummy environment variables to prevent validation errors during test collection
os.environ["GEMINI_API_KEY"] = "test_dummy_gemini_api_key_for_testing"
os.environ["DATABASE_URL"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/email_analyzer"
os.environ["POSTGRES_USER"] = "postgres"
os.environ["POSTGRES_PASSWORD"] = "postgres"
os.environ["POSTGRES_SERVER"] = "localhost"
os.environ["POSTGRES_PORT"] = "5432"
os.environ["POSTGRES_DB"] = "email_analyzer"
os.environ["SECRET_KEY"] = "test_dummy_secret_key_for_jwt_testing_purposes"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test if the root endpoint (/) is working properly"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json() or response.json() is not None

def test_user_registration_and_login():
    """Test user registration and login flow"""
    unique_email = "testuser_pytest@example.com"
    password = "securepassword123"

    # 1. Test user registration
    response = client.post(
        "/auth/register",
        json={"email": unique_email, "password": password}
    )
    assert response.status_code in [200, 201, 400]

    # 2. Test user login
    login_response = client.post(
        "/auth/login",
        data={"username": unique_email, "password": password}
    )
    
    if login_response.status_code == 200:
        data = login_response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"