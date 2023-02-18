from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

from . import swagger_schemas
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from action.models import Follower
from api.v1.action.serializers import LikeDislikeSerializer, SubscribeButtonSerializer, FollowersFollowingButtonSerializer
from api.v1.action.services import LikeService, FollowService
from blog.models import Article, Comment

User = get_user_model()


class LikeDislikeView(generics.GenericAPIView):
    """Поставить лайк/дизлайк на статью или комментарий"""
    serializer_class = LikeDislikeSerializer

    @swagger_auto_schema(**swagger_schemas.like_dislike_schema)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        like_service = LikeService(
            user=request.user,
            vote=serializer.validated_data['vote'],
            model=serializer.validated_data['model'],
            object_id=serializer.validated_data['object_id']
        )
        data: dict = like_service.make_like()
        return Response(data, status.HTTP_200_OK)


class SubscribeButtonView(generics.GenericAPIView):
    """Подписаться/отписаться на пользователя"""
    serializer_class = SubscribeButtonSerializer

    @swagger_auto_schema(**swagger_schemas.subscribe_schema)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        follow_service = FollowService(
            current_user=request.user,
            content_maker_id=serializer.validated_data['content_maker_id'],
        )
        data = follow_service.make_follower()
        return Response(data, status.HTTP_200_OK)


class FollowersButtonView(generics.ListAPIView):  # Или нужно Retrieve ??
    """Вернуть тех, кто подписан на меня, или тех, на кого подписан я"""
    serializer_class = FollowersFollowingButtonSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):

        print(1, self.request.query_params)
        print(2, self.kwargs)

        if self.request.query_params['button_name'] == 'followingButton':
            """Вернуть записи, где я подписчик"""
            return User.objects.filter(followers__id=self.kwargs['pk'])
        elif self.request.query_params['button_name'] == 'followersButton':
            """Вернуть моих подписчиков, те записи, где я content-maker"""
            return User.objects.filter(following__id=self.kwargs['pk'])
























