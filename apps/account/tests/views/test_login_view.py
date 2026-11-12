import pytest
from django.urls import reverse

from apps.account.factories import CustomUserFactory, UserProfileFactory


@pytest.mark.django_db
def test_login_success(client):
    url = reverse("apps:accounts:login")
    user = CustomUserFactory.create(email="test@test.com", password="secret123")
    UserProfileFactory.create(user=user)
    # Arrange
    payload = {
        "email": "test@test.com",
        "password": "secret123",
    }

    # Act
    response = client.post(url, data=payload)
    assert response.data.get("access") is not None
    assert response.data.get("refresh") is not None


@pytest.mark.django_db
def test_login_failed_when_wrong_email_password(client):
    url = reverse("apps:accounts:login")
    user = CustomUserFactory.create(email="test@test.com", password="secret123")
    UserProfileFactory.create(user=user)
    # Arrange
    payload = {
        "email": "test@test.com",
        "password": "wrongpassword",
    }

    # Act
    response = client.post(url, data=payload)

    # Assert
    assert response.status_code == 400
