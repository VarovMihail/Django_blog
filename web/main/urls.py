from django.urls import path

from .views import SetUserTimeZone, TemplateAPIView

urlpatterns = [
    path('', TemplateAPIView.as_view(template_name='index.html'), name='index'),
    path('timezone/', SetUserTimeZone.as_view(), name='set_user_timezone'),
    path('callback/github/', TemplateAPIView.as_view(template_name='auth_app/github_callback.html')),
]
