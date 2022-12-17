import re

import pytest
from django.test import override_settings
from django.core import mail

from django.urls import reverse
from urllib.parse import parse_qs, urlparse
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = [pytest.mark.django_db]

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
def test_sign_up_flow(client):

# проверка регистрации
    mail.outbox = []
    url = reverse('api:v1:auth_app:sign-up')
    data = {
        'first_name': 'ivan',
        'last_name': 'ivanov',
        'email': '555@mail.ru',
        'password_1': 'qwerty2022',
        'password_2': 'qwerty2022',
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert User.objects.filter(email=data['email']).exists()
    user = User.objects.only('is_active').get(email=data['email'])
    assert not user.is_active

# проверка отправки письма
    assert len(mail.outbox) == 1
    msg = mail.outbox[0]
    print(f'{str(msg.message()) =}')
    print(f'{msg =}')

# достать ссылку из текста письма
    text = str(msg.message())
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(pattern, text)
    assert urls

# достать параметры из ссылки(url)
    url = urls[0]
    print(f'{url =}')
    parser = urlparse(url)
    print(f"{parser =}")
    query_params: dict = parse_qs(parser.query)
    print(f"{query_params =}")
    data = {"key": query_params['key']}

# проверка ключа и активации пользователя
    verify_url = reverse('api:v1:auth_app:sign-up-verify')
    response = client.post(verify_url, data)       # почему сработало если {'key': ['NA:1o']}
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_active

# проверка логина
    login_url = reverse('api:v1:auth_app:sign-in')
    data = {
        'email': '555@mail.ru',
        'password': 'qwerty2022',
    }
    response = client.post(login_url, data)
    print(f"{response =}")
    assert response.status_code == 200, response.data

