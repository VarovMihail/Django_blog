from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum, UniqueConstraint

from action.choices import Vote

User = get_user_model()




class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.filter(vote=Vote.LIKE)

    def dislikes(self):
        return self.filter(vote=Vote.DISLIKE)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def articles(self):
        return self.get_queryset().filter(content_type__model='article') #.order_by('-articles__updated')

    def comments(self):
        return self.get_queryset().filter(content_type__model='comment') #.order_by('-comments__updated')

    def exists(self):
        return True

class LikeDislike(models.Model):
    vote = models.SmallIntegerField(choices=Vote.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')     # который поставил оценку
    created = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)          # тип контента, к которому относится запись
    object_id = models.PositiveIntegerField()                                        # ID записи - ID первичного ключа экземпляра модели, для которой создаётся связь.
    content_object = GenericForeignKey()                                             # генерируемый внешний ключ на запись, по сути объект контента

    # content_object содержит поле для связи с любой моделью и он является классом GenericForeignKey
    # Если два предыдущих поля имеют названия отличные от content_type и object_id,
    # то их необходимо передать в качестве аргументов в GenericForeignKey
    # Если не отличаются, то GenericForeignKey самостоятельно их определит и будет использовать для создания полиморфных связей.

    objects = LikeDislikeManager()  # специальный менеджер модели, который облегчит работу по получению отдельно
                                    # Like и Dislike счётчиков, а также их суммарного рейтинга.


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    content_maker = models.ForeignKey(User, on_delete=models.CASCADE)#, related_name='content_maker_set')
    created = models.DateTimeField(auto_now_add=True)

    # related_name позволяет и одному и другому User получить все строки из таблицы Follower

    class Meta:
        # unique_together = [['follower', 'content_maker']]
        # Для удобства unique_together может быть одним списком при работе с одним набором полей:
        # unique_together = ['follower', 'content_maker']
        # ValidationError, возникающее во время проверки модели при нарушении ограничения,
        # имеет код ошибки «unique_together».

        constraints = [
            UniqueConstraint(fields=['follower', 'content_maker'], name='unique_following')
        ]
        ordering = ['-created']

    # def __str__(self):
    #     return self.follower.name




