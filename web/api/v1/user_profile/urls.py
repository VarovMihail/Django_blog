from django.urls import path, include

from api.v1.user_profile.views import ChangePassAPIView, AvatarUpdateView, FillOutView, AllUsersAPIView, UserInfoAPIView
from main.views import TemplateAPIView

app_name = 'user_profile'

urlpatterns = [

    path('fill-out/', FillOutView.as_view(), name='fill_out'),
    path('avatar-update/', AvatarUpdateView.as_view(), name='api_avatar_update'),
    path('change-pass/', ChangePassAPIView.as_view(), name='api_change_pass'),
    path('all-users-list/', AllUsersAPIView.as_view(), name='all_users_list'),
    path('user-info/<int:pk>/', UserInfoAPIView.as_view(), name='user_info'),

]


