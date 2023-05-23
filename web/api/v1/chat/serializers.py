from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CheckUserTokenSerializer(serializers.Serializer):
    jwt = serializers.CharField()

class JWTUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'avatar']
