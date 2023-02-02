from django.urls import path
from . import views
from .views import many_to_many_test

app_name = 'action'

urlpatterns = [
        path('many-to-many/', many_to_many_test),
]

