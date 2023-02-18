from typing import Optional, TypeVar

from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from src import settings

from .managers import UserManager

UserType = TypeVar('UserType', bound='User')


def upload_avatar_path(instance, filename):
    print(instance, instance.pk, filename)
    return f'avatar/{instance.pk}/{filename}'


class User(AbstractUser):

    class Gender(models.IntegerChoices):
        UNKNOWN = (0, 'Unknown')
        MALE = (1, 'Male')
        FEMALE = (2, 'Female')

    username = None  # type: ignore
    email = models.EmailField(_('Email address'), unique=True)
    gender = models.PositiveSmallIntegerField('пол', choices=Gender.choices, default=Gender.UNKNOWN)
    birthday = models.DateField(blank=True, null=True)
    #avatar = models.ImageField(default='default.jpg', blank=True, upload_to=upload_avatar_path)
    avatar = models.ImageField(null=True, blank=True, upload_to=upload_avatar_path)
    following = models.ManyToManyField('self',
                                       through='action.Follower',
                                       # through_fields=('follower', 'content_maker'),
                                       related_name='followers',
                                       symmetrical=False)

    # user.following - список тех на кого я подписан
    # user.followers - получить список тех кто подписан на меня:
    # follower.followers.all, content_maker.followers.all

    # Spider Man / test3 @ test.com
    # Я подписан на(user.following.all):
    # < QuerySet[ < User: test @ test.com >, < User: test2 @ test.com >, < User: test1 @ test.com >] >
    #
    # Я подписан на(user.following_to.all):
    # < QuerySet[ < Follower: Follower object(8) >, < Follower: Follower object(7) >, < Follower: Follower object(1) >] >
    #
    # Они подписаны на меня - моя роль - контентмейкер(user.content_maker.all):
    # < QuerySet[ < Follower: Follower object(3) >] >


    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return super().get_full_name()

    @property  # создать hmac signed base64 compressed JSON string
    def confirmation_key(self) -> str:
        print(f'{self.pk = }')
        return signing.dumps(obj=self.pk, key=settings.SECRET_KEY, salt='salt')

    @classmethod
    def get_user_from_key(cls, key: str) -> Optional[UserType]:
        max_age = 100_000
        try:
            user_id = signing.loads(key, key=settings.SECRET_KEY, salt='salt', max_age=max_age)
            user = cls.objects.get(id=user_id)
        except (signing.SignatureExpired, signing.BadSignature, cls.DoesNotExist):
            return None
        return user

    def get_absolute_url(self):
        return reverse_lazy('user_profile:user', kwargs={'pk': self.id})
