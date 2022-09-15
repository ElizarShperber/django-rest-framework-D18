from django.core.cache import cache
from django.db import models

from django.db.models import Sum
from django.utils.translation import gettext as _

class Author(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_post_author = self.post_set.all().aggregate(sum_rating=Sum('rating') * 3)['sum_rating']
        rating_comment = self.user.comment_set.all().aggregate(sum_rating=Sum('rating'))['sum_rating']
        rating_comment_post = Post.objects.filter(author=self).values('rating')
        a = 0
        for i in range(len(rating_comment_post)):
            a = a + rating_comment_post[i]['rating']
        self.rating = rating_post_author + rating_comment + a
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField('auth.User', through='Subscriber')

    def __str__(self):
        return self.category

    def get_subscribers_emails(self):
        result = set()
        for user in self.subscribers.all():
            result.add(user.email)
        return result


class Post(models.Model):
    news = 'NW'
    article = 'AL'

    TYPES = [
        (news, 'Новость'),
        (article, 'Статья'),

    ]

    type_of_post = models.CharField(max_length=2,
                                    choices=TYPES,
                                    default=article)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100, help_text=_('title of post'))
    body = models.CharField(max_length=1000,  help_text=_('body of post'))
    rating = models.IntegerField(default=0,  help_text=_('rating of post'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview_body = self.body[:125] + '...'
        return preview_body

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, help_text=_('post of comment'))
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, help_text=_('user of comment'))
    comment = models.CharField(max_length=200, help_text=_('text of comment'))
    date_time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.comment


class Subscriber(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, help_text=_('user of subscriber'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text=_('category of subscriber'))
