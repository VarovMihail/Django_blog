from rest_framework import serializers


class ResponseLikeDislikeSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    vote = serializers.IntegerField()
    model = serializers.CharField()
    object_id = serializers.IntegerField()


class SubscribeSerializer(serializers.Serializer):
    subscribe_status = serializers.IntegerField()
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()


like_dislike_schema = {
    'operation_description': '## Set like to article/comment',
    'operation_summary': 'set like or dislike to articles and comments',
    'tags': ['Likes'],
    'operation_id': 'get_Likes',
    'responses': {200: ResponseLikeDislikeSerializer},
}


subscribe_schema = {
    'operation_description': '## Subscribe / Unsubscribe to User',
    'operation_summary': 'add / delete user to following',
    'tags': ['Subscribes'],
    'operation_id': 'get_Subscribe',
    'responses': {200: SubscribeSerializer},
}


















