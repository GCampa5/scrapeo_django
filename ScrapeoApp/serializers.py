from rest_framework import serializers
from .models import News, Tag

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('Id', 'Title', 'Tag', 'Author', 'Date', 'Link', 'Content')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('Id', 'Name')
