from django.urls import path
from . import views

appname = 'chat'

urlpatterns = [
    path('open/', views.OpenChatView.as_view(), name='open_chat'),
    path('verify-jwt/', views.CheckUserTokenView.as_view(), name='verify_jwt'),
]





