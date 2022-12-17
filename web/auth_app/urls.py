from django.urls import path

from main.views import TemplateAPIView

app_name = 'auth_app'

# ФРОНТЕНД

urlpatterns = [
    path('login/', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
    path('register/', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
    path(
        'password-recovery/',
        TemplateAPIView.as_view(template_name='auth_app/password_recovery.html'),
        name='reset_email_sent',
    ),
    path(
        'verify-email/',
        TemplateAPIView.as_view(template_name='auth_app/verify_email.html'),
        name='account_verification',
    ),
]
