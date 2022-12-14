from pprint import pprint

import rest_framework.pagination
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from api.v1.blog.serializers import ArticleSerializer, ArticleDetailSerializer, CommentCreateSerializer, \
    CommentListSerializer, CommentUpdateSerializer
from blog.models import Article, Comment

class ArticlesListViewPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 4

class ArticlesListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = ArticlesListViewPagination

class ArticlesDetailView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ArticleDetailSerializer

    def get(self, request, slug):
        print(request.data, slug)
        article = Article.objects.get(slug=slug)
        serializer = self.get_serializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentCreateSerializer


class CommentListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentListSerializer

    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        self.queryset = Comment.objects.filter(article=article).order_by('-updated')
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CommentUpdateSerializer

    # def patch(self, request, pk):
    #     print(request.data)
    #     return self.partial_update(request, pk)
