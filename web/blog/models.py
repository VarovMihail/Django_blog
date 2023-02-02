from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse_lazy

from action.models import LikeDislike
from .choices import ArticleStatus

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('-id',)

    def save(self, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(**kwargs)


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='article_set')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='article_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=ArticleStatus.choices, default=ArticleStatus.INACTIVE)
    image = models.ImageField(upload_to='articles/', blank=True, default='no-image-available.jpg')
    objects = models.Manager()
    votes = GenericRelation(LikeDislike, related_query_name='articles')

    def likes(self) -> int:
        return self.votes.likes().count()

    def dislikes(self) -> int:
        return self.votes.dislikes().count()

    @property
    def short_title(self):
        return self.title[:30]

    @property
    def short_content(self):
        return self.content[:300]

    def __str__(self):
        return '{title} - {author}'.format(title=self.short_title, author=self.author)

    def save(self, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(**kwargs)

    def get_absolute_url(self):
        return reverse_lazy('blog:post-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-updated', '-created', 'id')


class Comment(models.Model):
    author = models.EmailField()
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='comment_set', blank=True
    )
    content = models.TextField(max_length=300)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    votes = GenericRelation(LikeDislike, related_query_name='comments')

    objects = models.Manager()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def likes(self):
        return self.votes.count()


# class Like(models.Model):
#     class Vote(models.IntegerChoices):
#         LIKE = 1
#         DISLIKE = -1
#
#     article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
#     created = models.DateTimeField(auto_now=True)
#     vote = models.SmallIntegerField(choices=Vote.choices)


