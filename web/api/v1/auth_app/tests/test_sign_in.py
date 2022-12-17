import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]

@pytest.mark.parametrize(
    ['email', 'password', 'status'],
    (
        ['555@mail.ru', 'qwerty2021', 200],
        ['777@mail.ru', 'qwerty2021', 400],
        ['555@mail.ru', 'qwerty2022', 400],
        ['', '', 400],
    )
)
def test_login(client, user, email, password, status):
    url = reverse('api:v1:auth_app:sign-in')
    data = {
        'email': email,
        'password': password
    }
    response = client.post(url, data)
    assert response.status_code == status
