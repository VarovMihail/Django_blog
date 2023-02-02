import logging
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from main.models import User
from . import services
from . import serializers

logger = logging.getLogger(__name__)


def order1(request):
    return 'hello'


def many_to_many_test(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'many_to_many.html', context)
