# Generated by Django 4.2.5 on 2023-10-06 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ScrapeoApp', '0002_alter_noticia_contenido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='Autor',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='Titulo',
            field=models.CharField(max_length=255),
        ),
    ]
