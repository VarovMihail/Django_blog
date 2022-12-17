from django.urls import path, include

from main.views import TemplateAPIView


app_name = 'user_profile'

urlpatterns = [
    path('', TemplateAPIView.as_view(template_name='user_profile/profile.html'), name='profile'),
    path('user_list/', TemplateAPIView.as_view(template_name='user_profile/user_list.html'), name='user_list'),
    # path('api_avatar_update/', TemplateAPIView.as_view(template_name='user_profile/api_avatar_update.html'), name='api_avatar_update'),
    # path('api_change_pass/', ChangePassAPIView.as_view(), name='api_change_pass'),


]
