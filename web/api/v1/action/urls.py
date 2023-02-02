from django.urls import path, include
#from .views import ArticleLikeView, CommentLikeView, LikeView
from .views import LikeDislikeView, SubscribeButtonView, FollowersButtonView
from action.models import LikeDislike, Vote
from blog.models import Article, Comment

app_name = 'action'

urlpatterns = [
    path('like/', LikeDislikeView.as_view(), name='like_dislike'),
    path('subscribe-button/', SubscribeButtonView.as_view(), name='subscribe_button'),
    path('followers-following-button/<int:pk>/', FollowersButtonView.as_view(), name='followers_button'),
    #path('following-button/<int:pk>/', FollowingButtonView.as_view(), name='following_button'),

]


