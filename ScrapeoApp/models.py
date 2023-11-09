from django.db import models

# Create your models here.
# Crear vista con autores

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


