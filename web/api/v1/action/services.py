from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from typing import Optional

from django.db.models import Count

from action.choices import LikeModel, Vote, LikeStatus, SubscribeStatus
from action.models import LikeDislike, Follower
from blog.models import Article, Comment

User = get_user_model()


class LikeService:
    def __init__(self, user: User, vote: int, model: LikeModel, object_id: int):
        self.user = user
        self.vote = vote
        self.model = model
        self.object_id = object_id
        self.instance = self.get_model_instance()

    def get_contenttype_for_model(self) -> ContentType:
        return ContentType.objects.get_for_model(self.instance)

    def get_model_instance(self) -> Article | Comment:
        if self.model == LikeModel.ARTICLE:
            obj = self.get_article()
        else:
            obj = self.get_comment()
        return obj

    def get_article(self) -> Article:
        return Article.objects.get(pk=self.object_id)

    def get_comment(self) -> Comment:
        return Comment.objects.get(pk=self.object_id)

    def get_like_object(self) -> Optional[LikeDislike]:
        contenttype = self.get_contenttype_for_model()
        return LikeDislike.objects.filter(user=self.user, content_type=contenttype, object_id=self.object_id).first()

    def create_like_object(self) -> LikeDislike:
        return self.instance.votes.create(user=self.user, vote=self.vote)

    def update_like_object(self, obj: LikeDislike) -> LikeDislike:
        obj.vote = self.vote
        obj.save(update_fields=['vote'])
        return obj

    def make_like(self) -> dict:
        if like_obj := self.get_like_object():
            if like_obj.vote is not self.vote:
                # если противоположности, то меняем
                self.update_like_object(like_obj)
                result, like_status = 'reaction changed', self.vote
            else:
                # если одинаковые, то удаляем
                like_obj.delete()
                result, like_status = 'reaction deleted', LikeStatus.EMPTY.value
        else:
            # если не существует, то создаем
            self.create_like_object()
            mess = 'LIKE' if self.vote is Vote.LIKE.value else 'DISLIKE'
            result, like_status = f'add new {mess}', self.vote

        data = {
            'result': result,
            'like_status': like_status,
            'likes': self.instance.votes.likes().count(),
            'dislikes': self.instance.votes.dislikes().count(),
        }
        return data


class FollowService:
    def __init__(self, current_user: User, content_maker_id: int):
        self.follower = current_user
        self.content_maker = FollowService.get_user_object(content_maker_id)
        #self.content_maker = self.get_user_object(content_maker_id)

    def make_follower(self) -> dict:
        if not self.is_subscribed():
            self.create_subscribe_obj()
            #subscribe_status = SubscribeStatus.SUBSCRIBE.value
        else:
            self.delete_subscribe_obj()
            #subscribe_status = SubscribeStatus.UNSUBSCRIBE.value
            # 'followers': self.follower.following.all().count(),

        data = {
            'subscribe_status': self.get_subscribe_status().value,
            'followers_count': self.followers_count(),
            'following_count': self.following_count()
        }
        return data

    @staticmethod
    def get_user_object(id: int) -> User:
        return User.objects.get(pk=id)

    def is_subscribed(self) -> bool:
        return Follower.objects.filter(follower=self.follower, content_maker=self.content_maker).exists()

    def create_subscribe_obj(self) -> Follower:
        return Follower.objects.create(follower=self.follower, content_maker=self.content_maker)

    def delete_subscribe_obj(self) -> None:
        Follower.objects.filter(follower=self.follower, content_maker=self.content_maker).delete()

    def get_subscribe_status(self) -> int:
        if isinstance(self.follower, AnonymousUser):
            return SubscribeStatus.ANONYMOUS
        elif self.follower.id == self.content_maker.id:
            return SubscribeStatus.SELF
        elif self.is_subscribed():
            return SubscribeStatus.SUBSCRIBE
        else:
            return SubscribeStatus.UNSUBSCRIBE

    def followers_count(self) -> int:
        print(1, User.objects.all())
        print(2, User.objects.filter(first_name__startswith='S'))
        print(3, User.objects.values('id', 'first_name'))
        print(4, User.objects.values_list('id', 'first_name'))
        print(5, User.objects.values_list('first_name', flat=True))
        #return User.objects.filter(pk=self.content_maker.id).aggregate(Count('followers', distinct=True))['followers__count']
        return self.content_maker.followers.count()

    def following_count(self) -> int:
        #return User.objects.filter(pk=self.content_maker.id).aggregate(Count('following', distinct=True))['following__count']
        return self.content_maker.following.count()

