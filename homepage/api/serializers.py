from ..models import News, SimpleAd
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

class AdSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimpleAd