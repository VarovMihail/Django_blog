from django.urls import path, include

from api.v1.user_profile.views import ChangePassAPIView, AvatarUpdateView
from main.views import TemplateAPIView

app_name = 'user_profile'

urlpatterns = [

    path('avatar-update/', AvatarUpdateView.as_view(), name='api_avatar_update'),
    path('change-pass/', ChangePassAPIView.as_view(), name='api_change_pass'),

]


