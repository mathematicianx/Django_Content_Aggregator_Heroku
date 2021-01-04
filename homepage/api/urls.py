from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<pk>/', views.NewsDetailView.as_view(), name='news_detail'),
]