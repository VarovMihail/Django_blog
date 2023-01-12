from io import BytesIO
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from PIL import Image

User = get_user_model()


# @pytest.fixture()
# def client():
#     return APIClient()

@pytest.fixture()
def user() -> User:
    user = User.objects.create_user(
        first_name='test',
        last_name='test',
        email='555@mail.ru',
        password='qwerty2021',
        is_active=True,)
    return user


@pytest.fixture()
def authorized_client(client, user):
    refresh = RefreshToken.for_user(user)
    refresh_token = str(refresh)
    access_token = str(refresh.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return client

@pytest.fixture()
def temporary_image():
    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())
