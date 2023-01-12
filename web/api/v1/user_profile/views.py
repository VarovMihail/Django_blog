from django.shortcuts import render
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser

from main.models import UserType
from api.v1.user_profile.serializers import ChangePassSerializer, AvatarUpdateSerializer, FillOutViewSerializer

User: UserType = get_user_model()

class ChangePassAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePassSerializer

    def get_object(self):
        print(f'{self.request.user = }')
        return self.request.user



class AvatarUpdateView(generics.GenericAPIView):
    serializer_class = AvatarUpdateSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)

        return Response(serializer.data)


class FillOutView(generics.RetrieveUpdateAPIView):
    serializer_class = FillOutViewSerializer

    def get_object(self):
        return self.request.user




