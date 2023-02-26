from django.db.models import Count, Avg, Sum, Max
from django.http import Http404
from django.http import HttpResponseNotFound
from django.shortcuts import render
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser

from main.models import UserType
from api.v1.user_profile.serializers import ChangePassSerializer, AvatarUpdateSerializer, FillOutViewSerializer, \
    UserInfoSerializer, AllUsersSerializer, ChangeDataSerializer

User: UserType = get_user_model()


class ChangeDataAPIView(generics.UpdateAPIView):
    serializer_class = ChangeDataSerializer

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        return self.request.user


class ChangePassAPIView(generics.UpdateAPIView):
    """Смена пароля из профайла"""
    queryset = User.objects.all()
    serializer_class = ChangePassSerializer

    def get_object(self):
        print(f'{self.request.user = }')
        return self.request.user


class AvatarUpdateView(generics.GenericAPIView):
    """Обновление аватара пользователя из профайла"""
    serializer_class = AvatarUpdateSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)

        return Response(serializer.data)



class FillOutView(generics.RetrieveAPIView):
    """Заполнить профайл пользователя"""
    #pagination_class = None
    serializer_class = FillOutViewSerializer

    def get_queryset(self):
        """Динамически добавляем поля в queryset"""
        queryset = User.objects.all().annotate(
            Avg('following__id'),
            Avg('followers__id'),
            following_count=Count('following', distinct=True),
            followers_count=Count('followers', distinct=True),
        )

        print(1, User.objects.aggregate(average_id=Avg('id')))
        print(2, User.objects.aggregate(Avg('id'), Sum('id'), Max('id')))
        print(3, User.objects.annotate(
            Count('following'),
            followers_count=Count('followers'),
        ).aggregate(Avg('following__count')))

        return queryset

    def get_object(self):
        instance = self.get_queryset().get(id=self.request.user.id)

        # following = instance.following.all()
        # print(f'{str(following.query) = }')
        #
        # followers = instance.followers.all()
        # print(f'{str(followers.query) = }')

        return instance


class AllUsersAPIView(generics.ListAPIView):
    """Список всех пользователей"""
    permission_classes = (AllowAny,)
    serializer_class = AllUsersSerializer

    def get_queryset(self):
        return User.objects.order_by('id')

class UserInfoAPIView(generics.RetrieveAPIView):
    """Страница пользователя, которую видят все"""
    permission_classes = (AllowAny,)
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        return User.objects.annotate(
            followers_count=Count('followers', distinct=True),
            following_count=Count('following', distinct=True)
        )


