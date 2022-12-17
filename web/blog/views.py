import logging

from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from api.v1.blog import serializers
from api.v1.blog.filters import ArticleFilter
from api.v1.blog.services import BlogService
from blog.models import Article
from main.pagination import BasePageNumberPagination

logger = logging.getLogger(__name__)

class ViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'delete')
    lookup_field = 'slug'
    permission_classes = (AllowAny,)
    pagination_class = BasePageNumberPagination


class ArticleViewSet(ViewSet):
    filterset_class = ArticleFilter

    @property
    def template_name(self):
        if self.action == 'list':
            return 'blog/post_list.html'
        elif self.action == 'retrieve':
            return 'blog/post_detail.html'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ArticleSerializer
        return serializers.FullArticleSerializer

    def get_queryset(self):
        return BlogService.get_active_articles()

    def list(self, request, **kwargs):
        response = super().list(request, **kwargs)
        # response.template_name = self.get_template_name()
        response.template_name = self.template_name
        return response

    def retrieve(self, request, **kwargs):
        response = super().retrieve(request, **kwargs)
        # response.template_name = self.get_template_name()
        response.template_name = self.template_name
        return response
