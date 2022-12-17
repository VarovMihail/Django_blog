import pytest
from freezegun import freeze_time
import datetime
from django.contrib.auth import get_user_model

User: 'UserType' = get_user_model()

pytestmark = [pytest.mark.django_db]

def test_time_key(user):
    initial_time = datetime.datetime(2022, 11, 3)
    control_time = datetime.datetime(2022, 11, 6)

    with freeze_time(initial_time):
        key = user.confirmation_key
        assert User.get_user_from_key(key)   # вернет user|None

    with freeze_time(control_time):
        assert not User.get_user_from_key(key)


def test_bad_key(user):
    key = user.confirmation_key
    assert User.get_user_from_key(key)
    bad_key = key + 'salt'
    assert not User.get_user_from_key(bad_key)

def test_delete_user(user):
    key = user.confirmation_key
    assert User.get_user_from_key(key)
    user.delete()
    assert not User.get_user_from_key(key)
