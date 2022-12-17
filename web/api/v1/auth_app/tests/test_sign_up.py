import pytest

from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    ['first_name', 'last_name', 'email', 'password_1', 'password_2', 'status'],
    (
        ('Ivan', 'Ivanov', '555@mail.ru', 'python2022', 'python2022', 201),
        ('Iv', 'Iv', '555@mail.ru', 'python2022', 'python2022', 201),
        ('Ivan', 'Ivanov', '555@mail', 'python2022', 'python2022', 400),
        ('Ivan', 'Ivanov', '555@mail.ru', 'python', 'python', 400),
        ('Ivan', 'Ivanov', '555@mail.ru', 'python2033', 'python2022', 400),
        ('Ivan', 'Ivanov', '555@mail.ru', 'qwerty22', 'qwerty22', 400),
    )
)
def test_sign_up(client, first_name, last_name, email, password_1, password_2, status):
    # url = reverse('api:v1:auth_app:sign-up')
    url = '/api/v1/auth/sign-up/'
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password_1': password_1,
        'password_2': password_2,
    }
    response = client.post(url, data)
    assert response.status_code == status
    if response.status_code == 201:
        assert User.objects.filter(email=email).exists()
        user = User.objects.only('is_active').get(email=email)
        assert not user.is_active












