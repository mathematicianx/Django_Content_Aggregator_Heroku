from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views


app_name = 'api'

urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<pk>/', views.DetailedView.as_view(), name='news_detail'),
    path('news-create/', views.CreateNewsView.as_view(), name='news_create'),
    path('news-update/<pk>/', views.UpdateNewsView.as_view(), name='news_update'),
    path('news-delete/<pk>/', views.DeleteNewsView.as_view(), name='news_delete'),
    path('advertisement/', views.AdListView.as_view(), name='advertisement'),
    path('advertisement/<pk>/', views.SimpleAdDetailedView.as_view(), name='simplead_detail'),
    path('advertisement-create/', csrf_exempt(views.CreateSimpleAdView.as_view()), name='simplead_create'),
]