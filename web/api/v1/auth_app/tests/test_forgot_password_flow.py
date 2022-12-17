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
def test_forgot_password_flow(client, user):

# проверка отправки письма
    #mail.outbox = []
    print(len(mail.outbox))
    url = reverse('api:v1:auth_app:reset-password')
    response = client.post(url, {'email': user.email})
    assert response.status_code == 200, response.data
    assert len(mail.outbox) == 1

# достать ссылку из текста письма
    msg = mail.outbox[0]
    text = str(msg.message())
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(pattern, text)
    print(f'{urls =}')
    url = urls[0]
    print(f'{url =}')
    assert urls

# достать параметры из ссылки(url)
    # url = url.replace('amp;', '')
    parser =urlparse(url)
    print(f'{parser =}')
    query_params: dict = parse_qs(parser.query, separator='&amp;')
    print(f'{query_params =}')

# проверка ключей и смены пароля
    data = {
        'password_1': 'qwerty2022',
        'password_2': 'qwerty2022',
        **query_params
    }
    print(f'{data =}')
    confirm_url = reverse('api:v1:auth_app:reset-password-confirm')
    response = client.post(confirm_url, data)
    assert response.status_code == 200

# проверка логина
    user.refresh_from_db()
    login_url = reverse('api:v1:auth_app:sign-in')
    data = {
        'email': user.email,
        'password': data['password_1'],
    }
    response = client.post(login_url, data)
    assert response.status_code == 200, response.data
