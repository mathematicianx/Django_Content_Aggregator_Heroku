from datetime import datetime
from ..models import News, SimpleAd
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
<<<<<<< HEAD
    date_of_publication = datetime.now()
    class Meta:
<<<<<<< HEAD
        model = SimpleAd
        fields = ('title', 'body', 'price', 'author', 'slug', 'date_of_publication',)
        validators = [ UniqueForYearValidator(
            queryset=SimpleAd.objects.all(),
            field='slug',
            date_field='date_of_publication'),
=======

    class Meta:
        model = SimpleAd
        fields = ('title', 'body', 'price', 'author')
        validators = [ UniqueForYearValidator(
            queryset=SimpleAd.objects.all(),
            field='slug',
            date_field='date_of_publication'
        ),
>>>>>>> bda6e54 (basic functionality of rest api for Simple Advertisements, without using generics)
        ]



<<<<<<< HEAD
# class UserSerializer(serializers.ModelSerializer):
#     user_ads = serializers.PrimaryKeyRelatedField(many=True, queryset=SimpleAd.objects.all())
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'user_ads']
=======
        model = SimpleAd
>>>>>>> 59119d1 (Create news from existing JSON data functionality added)
=======
class UserSerializer(serializers.ModelSerializer):
    user_ads = serializers.PrimaryKeyRelatedField(many=True, queryset=SimpleAd.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'user_ads']
>>>>>>> bda6e54 (basic functionality of rest api for Simple Advertisements, without using generics)
