from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.v1.auth_app.views import GithubCallbackView
from main.views import TemplateAPIView
from .yasg import urlpatterns as swagger_url

admin_url = settings.ADMIN_URL

urlpatterns = [
    path('', include('main.urls')),
    path('api/', include('api.urls')),
    path('', include('auth_app.urls')),
    path('', include('blog.urls')),
    path('profile/', include('user_profile.urls')),             # добавил
    path('action/', include('action.urls')),     # добавил
    path('', include('contact_us.urls')),
    path(f'{admin_url}/', admin.site.urls),
    path(f'{admin_url}/defender/', include('defender.urls')),
    path('api/', include('rest_framework.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('allauth.urls')),

]

urlpatterns += swagger_url

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if settings.ENABLE_SILK:
        urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))
    if settings.ENABLE_DEBUG_TOOLBAR:
        urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
