from django.contrib import admin
from .models import News, Movie, SimpleAd, Profile, ForumTopic, ForumResponse
# Register your models here.


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'which_site', 'link')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_of_publication', 'which_site', 'link')


@admin.register(SimpleAd)
class SimpleAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_of_publication', 'thumbnail', 'image_tag')
    readonly_fields = ['image_tag']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo')


@admin.register(ForumTopic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(ForumResponse)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'topic')
