from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):  # наследуемся от класса Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        p1 = self.post_set.filter(user=self).aggregate(Sum('rating_news'))
        rating_post_author: int = p1['rating_news__sum']*3
        p2 = self.user.comment_set.all().aggregate(Sum('rating_comment'))
        rating_all_comment_author: int = p2['rating_comment__sum']
        p3 = self.user.comment_set.filter(post__in=Post.objects.filter(user=self).values('id')).aggregate(Sum('rating_comment'))
        rating_post_comment_author: int = p3['rating_comment__sum']
        self.rating_author = rating_post_author+rating_all_comment_author+rating_post_comment_author
        self.save()
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=128)
    pass

class Post(models.Model):
    types = [
        ('N', 'Новость'),
        ('S', 'Статья'),
        ]
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=1, choices=types)
    post = models.TextField()
    date_time_create = models.DateField(auto_now_add=True)
    title_news = models.CharField(max_length=255)
    rating_news = models.IntegerField(default=0)

    def like(self):
        self.rating_news += 1
        self.save()

    def dislike(self):
        self.rating_news -= 1
        self.save()

    def preview(self):
        return self.post[0:124] + '...'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/post/{self.id}'
    pass

class PostCategory(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pass

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_create = models.DateField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()
    pass