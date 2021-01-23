from datetime import datetime
from ..models import News, SimpleAd
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueForYearValidator


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('title', 'link', 'which_site', 'date_of_publication',)
        validators = [
            UniqueForYearValidator(
                queryset=News.objects.all(),
                field='title',
                date_field='date_of_publication'),
        ]


class SimpleAdSerializer(serializers.ModelSerializer):
    date_of_publication = serializers.DateTimeField()
    class Meta:

        model = SimpleAd
        fields = ('title', 'body', 'price', 'author', 'slug', 'date_of_publication')
        validators = [
            UniqueForYearValidator(
                queryset=SimpleAd.objects.all(),
                field='slug',
                date_field='date_of_publication'),
        ]




