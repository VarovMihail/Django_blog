from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from action.models import Vote
from blog.models import Article, Category, Comment
from action.choices import LikeStatus

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'avatar')


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ('id', 'user', 'author', 'content', 'updated')


class CategorySerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


# class ArticleSerializer(serializers.ModelSerializer):
#     url = serializers.CharField(source='get_absolute_url')
#     author = UserSerializer()
#     category = CategorySerializer()
#     comments_count = serializers.IntegerField()
#
#     class Meta:
#         model = Article
#         fields = ('title', 'url', 'author', 'category', 'created', 'updated', 'comments_count')



class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    url = serializers.URLField(read_only=True, source='get_absolute_url')
    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'updated', 'created', 'short_content', 'author', 'url', 'comment_set', 'likes']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    like_status = serializers.SerializerMethodField(method_name='get_like_status')
    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'updated', 'created', 'content', 'author', 'likes', 'dislikes', 'like_status']

    def get_like_status(self, obj: Article) -> int:
        print(f'{obj = }')                           #  obj = <Article: В Австралии объявили о "серьез - test@test.com>
        user = self.context['request'].user
        result = LikeStatus.EMPTY
        if not user.is_authenticated:
            return result
        if like_dislike_obj := obj.votes.filter(user=user).first():
            result = LikeStatus.LIKE if like_dislike_obj.vote == Vote.LIKE else LikeStatus.DISLIKE
        # if obj.votes.filter(user=user).exists():
        #     if obj.votes.get(user=user).vote == Vote.LIKE:
        #         result = 1
        #     else:
        #         result = -1
        return result

class CommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=300)
    article = serializers.CharField()
    parent = serializers.IntegerField(write_only=True, allow_null=True)
# TypeError: int() argument must be a string, a bytes-like object or a real number, not 'Comment'
# поэтому     write_only=True

    def validate_article(self, article: str):
        if not Article.objects.filter(slug=article).exists():
            raise ValidationError('Article does not exist')
        return article

    def validate_content(self, text:str):
        print('validate_text')
        if 'bomb' in text:
            raise ValidationError('Forbidden word')
        return text

    def create(self, validated_data:dict):
        user = self.context['request'].user
        print(f'{validated_data["parent"] = }')
        if isinstance(user, AnonymousUser):
            user = None
            email = 'AnonymousUser@mail.ru'
        else:
            email = user.email
        article = Article.objects.get(slug=validated_data['article'])
        if validated_data['parent']:
            parent = Comment.objects.get(id=validated_data['parent'])
        else:
            parent = None
        data = {
            'author': email,
            'user': user,
            'article': article,
            'content': validated_data['content'],
            'parent': parent,
        }
        print(f'{validated_data = }')
        return Comment.objects.create(**data)
        #return super().create(data)


class ChildrenCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    like_status = serializers.SerializerMethodField(method_name='get_like_status')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'user', 'content', 'created', 'updated', 'parent', 'likes', 'like_status']

    def get_like_status(self, obj: Comment) -> LikeStatus:
        user = self.context['request'].user
        result = LikeStatus.EMPTY
        if not user.is_authenticated:
            return result
        result = LikeStatus.LIKE if obj.votes.filter(user=user) else LikeStatus.EMPTY
        return result


class CommentListSerializer(ChildrenCommentsSerializer):
    children = ChildrenCommentsSerializer(many=True)

    class Meta(ChildrenCommentsSerializer.Meta):
        fields = ChildrenCommentsSerializer.Meta.fields + ['children']

    def get_like_status(self, obj: Comment) -> LikeStatus:
        return super().get_like_status(obj)


class CommentUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField(max_length=300)

    def validate_content(self, text: str):            # и сюда всю валидацию контента?
        print('validation works')
        if 'bomb' in text:
            raise ValidationError('Forbidden word')
        return text

    def update(self, instance, validated_data):
        print(validated_data)
        print(instance)
        instance.content = validated_data['content']
        instance.save(update_fields=['content'])
        #instance.update(content=validated_data['content']) только в Моделсериалайзер?
        return instance


