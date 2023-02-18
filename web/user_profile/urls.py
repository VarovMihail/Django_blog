from django.urls import path, include

from main.views import TemplateAPIView


app_name = 'user_profile'

urlpatterns = [
    path('', TemplateAPIView.as_view(template_name='user_profile/profile.html'), name='profile'),
    path('user-list/', TemplateAPIView.as_view(template_name='user_profile/user_list.html'), name='user_list'),
    # path('user-list/<str:user>/', TemplateAPIView.as_view(template_name='user_profile/user_info.html'), name='user'),
    path('user-list/<pk>/', TemplateAPIView.as_view(template_name='user_profile/user_info.html'), name='user'),



]
