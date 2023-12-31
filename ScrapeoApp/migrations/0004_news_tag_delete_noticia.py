# Generated by Django 4.2.5 on 2023-10-11 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ScrapeoApp', '0003_alter_noticia_autor_alter_noticia_titulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=255)),
                ('Author', models.CharField(max_length=150)),
                ('Date', models.DateField(max_length=10)),
                ('Link', models.CharField(max_length=255)),
                ('Content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Noticia',
        ),
    ]
