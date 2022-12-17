import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()

@pytest.fixture()
def client():
    return APIClient()

@pytest.fixture()
def user(client):
    user = User.objects.create_user(first_name='test', last_name='test', email='555@mail.ru',password='qwerty2021',)
    user.is_active = True
    user.save()
    return user

    # url = reverse('api:v1:auth_app:sign-up')
    # data = {
    #     'first_name': 'ivan',
    #     'last_name': 'ivanov',
    #     'email': '555@mail.ru',
    #     'password_1': 'qwerty2021',
    #     'password_2': 'qwerty2021',
    # }
    # client.post(url, data)
    # user = User.objects.get(email=data['email'])
    # user.is_active = True
    # return user



