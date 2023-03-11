from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from . import views

app_name = 'auth_app'





urlpatterns = [
    path('sing-in/', views.LoginView.as_view(), name='sign-in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-up/verify/', views.VerifyEmailView.as_view(), name='sign-up-verify'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password/reset/', views.PasswordResetView.as_view(), name='reset-password'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('token/', TokenObtainPairView.as_view()),      # добавил посмотреть
    path('github/init/', views.GithubInitView.as_view()),
    path('github/callback/', views.GithubCallbackView.as_view()),


]
