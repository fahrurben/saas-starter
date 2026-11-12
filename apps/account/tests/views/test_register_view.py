import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_success(client):
    url = reverse("apps:accounts:register")

    # Arrange
    payload = {
        "email": "user@test.com",
        "password": "secret123",
        "first_name": "Buddy",
        "last_name": "Doe",
        "company_name": "Test2",
        "birthday": "1990-01-01",
        "gender": "M",
    }

    # Act
    response = client.post(url, data=payload)

    # Assert
    assert response.status_code == 200
