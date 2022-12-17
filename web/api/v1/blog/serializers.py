from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from blog.models import Article, Category, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'author', 'content', 'updated')


class CategorySerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    author = UserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ('title', 'url', 'author', 'category', 'created', 'updated', 'comments_count')


class FullArticleSerializer(ArticleSerializer):

    comments = CommentSerializer(source='comment_set', many=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + (
            'content',
            'comments',
        )

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    url = serializers.URLField(read_only=True, source='get_absolute_url')
    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'updated', 'created', 'short_content', 'author', 'url', 'comment_set']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Article
        fields = ['id', 'title', 'image', 'updated', 'created', 'content', 'author', 'comment_set']

class CommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=300)
    article = serializers.CharField()

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
        if isinstance(user, AnonymousUser):
            user = None
            email = 'AnonymousUser@mail.ru'
        else:
            email = user.email
        article = Article.objects.get(slug=validated_data['article'])
        data = {
            'author': email,
            'user': user,
            'article': article,
            'content': validated_data['content']
        }
        print(f'{validated_data = }')
        return Comment.objects.create(**data)
        #return super().create(data)



class CommentListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'author', 'user', 'content', 'created', 'updated']


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


