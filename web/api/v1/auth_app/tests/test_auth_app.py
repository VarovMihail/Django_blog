import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from api.v1.auth_app.services import User

pytestmark = [pytest.mark.django_db]



@pytest.fixture()
def client():
    return APIClient()
#
# def test_get_api(client):
#     # url = '/register/'
#     url = reverse('auth_app:sign_up')
#     response = client.get(url)
#     assert response.status_code == 200

# @pytest.mark.parametrize(
#     ['first_name', 'last_name', 'email', 'password_1', 'password_2', 'status'],
#     (
#         ('Ivan', 'Ivanov', '555@mail.ru', 'python2022', 'python2022', 201),
#         ('Iv', 'Iv', '555@mail.ru', 'python2022', 'python2022', 201),
#         ('Ivan', 'Ivanov', '555@mail', 'python2022', 'python2022', 400),
#         ('Ivan', 'Ivanov', '555@mail.ru', 'python', 'python', 400),
#         ('Ivan', 'Ivanov', '555@mail.ru', 'python2033', 'python2022', 400),
#         ('Ivan', 'Ivanov', '555@mail.ru', 'qwerty22', 'qwerty22', 400),
#     )
# )
# def test_sign_up(client, first_name, last_name, email, password_1, password_2, status):
#     # url = reverse('auth_app:sign-up')
#     url = '/api/v1/auth/sign-up/'
#     data = {
#         'first_name': first_name,
#         'last_name': last_name,
#         'email': email,
#         'password_1': password_1,
#         'password_2': password_2,
#     }
#     response = client.post(url, data)
#     assert response.status_code == status
#     if response.status_code == 201:
#         user = User.objects.get(email=email)
#         assert user

@pytest.mark.parametrize(
    ['email', 'password', 'status'],
    (
        ('555@mail.ru', 'python2022', 201),
        ('555@mail.ru', 'python2022', 201),
        ('555@mail', 'python2022', 400),
        ('555@mail.ru', 'python', 400),
        ('555@mail.ru', 'python2033', 400),
        ('555@mail.ru', 'qwerty22', 400),
    )
)
def test_sign_in(client, email, password, status):
    # url = reverse('auth_app:sign-up')
    url = '/api/v1/auth/sign-up/'
    user = User(email, password)
    data = {
        'email': email,
        'password': password,
    }
    response = client.post(url, data)
    assert response.status_code == status










