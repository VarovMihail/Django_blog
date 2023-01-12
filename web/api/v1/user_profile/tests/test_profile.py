import pytest
from django.contrib.auth import get_user_model
from PIL import Image
import tempfile


User = get_user_model()
pytestmark = [pytest.mark.django_db]

@pytest.mark.parametrize(
    ['current_password', 'new_password', 'confirm_password', 'status'],
    (
        ('qwerty2021', 'tester30', 'tester30', 200),
        ('qwerty2021', 'tester30', 'tester30000', 400),
        ('qwerty2021', 'tester', 'tester', 400),
        ('qwerty2020000', 'tester30', 'tester30', 400),
    )
)
def test_change_password(authorized_client,
                         current_password,
                         new_password,
                         confirm_password,
                         status):
    url = '/api/v1/user-profile/change-pass/'
    data = {
        'old_password': current_password,
        'new_password1': new_password,
        'new_password2': confirm_password,

    }

    response = authorized_client.put(url, data, content_type='application/json')
    assert response.status_code == status

@pytest.mark.parametrize(
    ['first_name', 'last_name', 'gender', 'birthday', 'status'],
    (
        ('Tor', 'Odinson', 1, '2022-10-10', 200),
        ('Tor', 'Odinson', 5, '2022-10-10', 400),
        ('T', 'Odinson', 1, '2022-10-10', 400),
        ('Tor', 'O', 1, '2022-10-10', 400),

    )
)
def test_change_profile_data(authorized_client,
                             first_name,
                             last_name,
                             gender,
                             birthday,
                             status):
    url = '/api/v1/user-profile/fill-out/'
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'gender': gender,
        'birthday': birthday,
    }

    response = authorized_client.put(url, data, content_type='application/json')
    assert response.status_code == status


# def test_change_avatar(authorized_client):
#
#     image = Image.new('RGB', (200, 200))
#     tmp = tempfile.NamedTemporaryFile(suffix='.jpg', prefix='test')
#     image.save(tmp, 'jpeg')
#     tmp.seek(0)
#
#     url = '/api/v1/user-profile/avatar-update/'
#     data = {
#         'avatar': tmp,
#     }
#     response = authorized_client.post(url, data, content_type='multipart/form-data')
#     print(f'{response.data = }')
#
#     assert response.status_code == 200
