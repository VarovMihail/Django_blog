from django.contrib import admin
from .models import LikeDislike, Follower


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_id', 'content_type', 'content_object', 'created', 'user', 'vote')
    list_filter = ('user', 'content_type')
    #list_filter = ('user', 'content_object')
    # AttributeError: 'GenericForeignKey' object has no attribute 'choices'


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'content_maker', 'created')
    list_filter = ('id', 'follower', 'content_maker', 'created')


class FollowerInline(admin.TabularInline):
    model = Follower
    #fk_name = 'follower'
    fk_name = 'content_maker'
    extra = 1












