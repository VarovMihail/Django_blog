from django.db.models import IntegerChoices, TextChoices


class Vote(IntegerChoices):
    LIKE = (1, 'Нравится')
    DISLIKE = (-1, 'Не нравится')


class LikeStatus(IntegerChoices):
    LIKE = 1
    DISLIKE = -1
    EMPTY = 0


class LikeModel(TextChoices):
    ARTICLE = 'article'
    COMMENT = 'comment'


class SubscribeStatus(IntegerChoices):
    SUBSCRIBE = (1, 'Подписан')
    UNSUBSCRIBE = (-1, 'Не подписан')
    ANONYMOUS = (0, 'Не может подписаться')
    SELF = (2, 'Сам юзер. Не может подписаться и отправить сообщение себе')












