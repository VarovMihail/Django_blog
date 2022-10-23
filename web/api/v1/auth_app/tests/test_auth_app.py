import pytest
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = [pytest.mark.django_db]

def test_api():
    assert 2 == 2

@pytest.fixture()
def client():
    return APIClient

def test_get_api():
    client = APIClient()
    url = reverse('auth_app: sign-up')
    response = client.get(url)
    assert response.status_code == 200





