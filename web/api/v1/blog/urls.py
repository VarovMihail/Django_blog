from django.urls import path
from .views import ArticlesListView, ArticlesDetailView, CommentCreateView, CommentListView, CommentUpdateView

app_name = 'blog'

urlpatterns = [
    path('posts/', ArticlesListView.as_view(), name='posts'),
    path('post/<slug>/', ArticlesDetailView.as_view(), name='post'),
    path('comment/', CommentCreateView.as_view(), name='comment'),
    path('comment-list/<slug>/', CommentListView.as_view(), name='comment-list'),
    path('comment-update/<pk>/', CommentUpdateView.as_view(), name='comment-update'),
]
