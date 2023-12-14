import pytest
from rest_framework.test import APIClient

client = APIClient()

class TestUserCreation:
    """test the user authentication and user creation of the app"""

    pytestmark = pytest.mark.django_db

    def test_create_user(self):
        payload = {"username": "admin", "password": "admin@123"}
        response = client.post("/auth/users/create/", data=payload)
        assert response.status_code == 201
        assert response.json()['username'] == "admin"
