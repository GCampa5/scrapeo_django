from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    Id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Tag = models.CharField(max_length=150, null=True)
    Author = models.CharField(max_length=150, null=True)
    Date = models.DateField(max_length=10, null=True)
    Link = models.CharField(max_length=255)
    Content = models.TextField(null=True)

class Tag(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)

class UserNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'news')
